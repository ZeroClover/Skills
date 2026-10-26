#!/usr/bin/env python3
"""Orchestrate a multi-model review batch through a dedicated Herdr session.

Standard library only. Every subcommand reads and updates ``manifest.json`` in
the run directory, saving it before and after each external side effect so a
later session can resume, inspect, or clean up the batch. Each subcommand
prints one JSON object; ``--help`` lists its arguments.

Subcommands:
  init     Create run ID, exclusive Herdr session, workspace, and manifest.
  list     List the runs recorded for a repository under the temp run root.
  version  Print the version stamp of a worktree (HEAD + dirty diff + untracked).
  start    Open one tab per reviewer and start the configured agents.
  round    Record a round (worktree stamp + brief hash), prompt, wait for reports.
  wait     Wait again (or --reprompt) for reviewers without a valid report.
  collect  Check report headers for a round and write summary.json.
  status   Show manifest state and live agents in the session.
  cleanup  Close reviewer panes, stop and delete the run-owned session.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time

ROLE_ENV = "MMR_ROLE"
RUN_ENV = "MMR_RUN_ID"
MANIFEST = "manifest.json"
AGENT_NAME_RE = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_REVIEWERS = os.path.join(SKILL_DIR, "assets", "default-reviewers.json")
REQUIRED_REPORT_FIELDS = ("Run ID", "Round", "Reviewer", "Stage", "Version", "Verdict")
VERDICTS = ("PASS", "CHANGES_REQUIRED", "INCOMPLETE")
# First-run trust dialogs seen on this machine: agy "Do you trust the contents of
# this project?" (cursor on Yes), codex "Trust this folder?" (cursor on Trust and
# continue), claude "Yes, I trust this folder" (cursor on "No, exit" by default).
# Nothing else is answered automatically.
TRUST_RE = re.compile(r"trust (this|the) (folder|project|files|contents)|trust and continue", re.IGNORECASE)
CURSOR_RE = re.compile(r"^\s*[❯›>]\s*\S")
YES_RE = re.compile(r"\b(yes|trust and continue)\b", re.IGNORECASE)
NO_RE = re.compile(r"\b(no|quit|exit|cancel)\b", re.IGNORECASE)


class Fail(Exception):
    pass


class Unverified(Fail):
    """A check could not be performed; it proves neither ownership nor mismatch."""


# ----------------------------------------------------------------- helpers --

def now():
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def out(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def run(cmd, cwd=None, timeout=None, check=True, binary=False):
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise Fail("command did not return within %ss: %s" % (timeout, " ".join(cmd)))
    if not binary:
        proc.stdout = proc.stdout.decode("utf-8", "surrogateescape")
        proc.stderr = proc.stderr.decode("utf-8", "surrogateescape")
    if check and proc.returncode != 0:
        raise Fail("command failed (%s): %s\nstdout: %s\nstderr: %s" % (
            proc.returncode, " ".join(cmd), str(proc.stdout).strip()[-2000:], str(proc.stderr).strip()[-2000:]))
    return proc


def herdr(session, args, timeout=None, check=True):
    """Run a herdr API command against the named session and parse its JSON.

    A CLI that does not return within ``timeout`` seconds becomes an error
    dict with code ``cli_timeout`` instead of an exception, so callers can
    record it per reviewer and continue.
    """
    cmd = ["herdr", "--session", session] + list(args)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        data = {"error": {"code": "cli_timeout", "message": "herdr CLI did not return within %ss" % timeout}}
        if check:
            raise Fail("herdr %s: %s" % (" ".join(args[:2]), json.dumps(data)))
        return data
    text = proc.stdout.strip() or proc.stderr.strip()
    try:
        data = json.loads(text) if text else {}
    except json.JSONDecodeError:
        data = {"raw": text}
    if proc.returncode != 0:
        data.setdefault("error", {}).setdefault("message", text)
        data["exit_code"] = proc.returncode
        if check:
            raise Fail("herdr %s failed: %s" % (" ".join(args[:2]), json.dumps(data, ensure_ascii=False)))
    return data


def session_list():
    proc = run(["herdr", "session", "list", "--json"])
    return json.loads(proc.stdout).get("sessions", [])


def find_session(name):
    for s in session_list():
        if s.get("name") == name:
            return s
    return None


def load_manifest(run_dir):
    path = os.path.join(run_dir, MANIFEST)
    if not os.path.isfile(path):
        raise Fail("no %s in %s" % (MANIFEST, run_dir))
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_manifest(run_dir, manifest):
    manifest["updated_at"] = now()
    path = os.path.join(run_dir, MANIFEST)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def refuse_if_reviewer():
    role = os.environ.get(ROLE_ENV)
    if role:
        raise Fail("%s=%s is set: this process was started as a reviewer of run %s. "
                   "Reviewers do not operate review batches. Follow your brief instead."
                   % (ROLE_ENV, role, os.environ.get(RUN_ENV, "?")))


def require_tool(name):
    if shutil.which(name) is None:
        raise Fail("required tool not found in PATH: %s" % name)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def run_root(repo):
    """Per-repository directory for review runs, outside any worktree.

    ``<system temp dir>/multi-model-review/<repo-name>-<hash of path>``: never
    part of the repository's git status, readable by later sessions (``list``
    finds it), and reclaimed by the operating system instead of accumulating
    forever (macOS purges the per-user temp dir after a few days without
    access; elsewhere the system's temp policy applies). Pass ``--run-dir`` to
    keep a run.
    """
    base = tempfile.gettempdir()
    real = os.path.realpath(repo)
    slug = "%s-%s" % (os.path.basename(real.rstrip(os.sep)) or "repo", hashlib.sha256(real.encode()).hexdigest()[:8])
    return os.path.join(base, "multi-model-review", slug)


def cmd_list(a):
    repo = os.path.abspath(a.repo)
    root = run_root(repo)
    runs = []
    if os.path.isdir(root):
        for name in sorted(os.listdir(root)):
            mp = os.path.join(root, name, MANIFEST)
            if not os.path.isfile(mp):
                continue
            try:
                m = json.load(open(mp, encoding="utf-8"))
            except (OSError, ValueError):
                continue
            rounds = m.get("rounds", [])
            runs.append({"run_id": m.get("run_id"), "run_dir": os.path.join(root, name), "stage": m.get("stage"),
                         "change_id": m.get("change_id"), "created_at": m.get("created_at"),
                         "session_state": (m.get("session") or {}).get("state"), "rounds": len(rounds),
                         "last_version": rounds[-1]["version"]["stamp"] if rounds else None})
    out({"repo": repo, "run_root": root, "runs": runs})


def latest_round(m):
    if not m["rounds"]:
        raise Fail("no rounds recorded yet; run `round` first")
    return max(r["round"] for r in m["rounds"])


def get_round(m, rnd):
    rec = next((r for r in m["rounds"] if r["round"] == rnd), None)
    if not rec:
        raise Fail("no round %d" % rnd)
    return rec


def reviewer_rec(m, name):
    return next((r for r in m["reviewers"] if r["name"] == name), None)


def verify_session(m, require_running=True):
    """Check that the live session is the one this run created before controlling it.

    Returns the live session record. Raises when the name is missing, the
    session directory differs, or the run's workspace is not in the session.
    """
    sess = m["session"]
    name = sess["name"]
    if name == "default" or name != m["run_id"]:
        raise Fail("refusing: session %r is not the run-owned session %r" % (name, m["run_id"]))
    if not sess.get("session_dir"):
        raise Fail("refusing: manifest has no session_dir for %s (init did not get that far); "
                   "check `herdr session list --json` and stop/delete it by name if it is yours" % name)
    live = find_session(name)
    if live is None:
        if require_running:
            raise Fail("session %s no longer exists; the batch cannot continue, start a new run" % name)
        return None
    if live.get("session_dir") != sess["session_dir"]:
        raise Fail("refusing: session_dir mismatch (manifest %s, live %s)" % (sess["session_dir"], live.get("session_dir")))
    if not live.get("running"):
        if require_running:
            raise Fail("session %s is not running; resume is not possible, start a new run" % name)
        return live
    mine = m.get("workspace")
    if mine:
        answer = herdr(name, ["workspace", "list"], timeout=30, check=False)
        if "error" in answer or "result" not in answer:
            err = answer.get("error") or {"message": "no result in response"}
            raise Unverified("workspace query failed (%s); ownership of session %s could not be verified, retry or check `herdr status`"
                             % (err.get("code") or err.get("message"), name))
        ws = answer["result"].get("workspaces", [])
        match = next((w for w in ws if w.get("workspace_id") == mine.get("workspace_id")), None)
        if match is None:
            raise Fail("refusing: live session does not contain this run's workspace %s" % mine.get("workspace_id"))
        if match.get("label") != mine.get("label"):  # renamed in the TUI; identity is the id, note it once
            msg = "workspace %s label is now %r (recorded %r)" % (mine.get("workspace_id"), match.get("label"), mine.get("label"))
            if not any(w.endswith(msg) for w in m.get("warnings", [])):
                m.setdefault("warnings", []).append("%s %s" % (now(), msg))
    return live


# ----------------------------------------------------------------- version --

def version_stamp(worktree, exclude=()):
    """HEAD plus every uncommitted change, so a dirty tree never hides behind HEAD.

    ``exclude`` lists paths (absolute or worktree-relative) left out of the
    stamp, normally the directory that holds review runs, so briefs and
    reports do not change the version they describe. Paths are read with
    ``-z`` so non-ASCII names are hashed like any other file.
    """
    worktree = os.path.realpath(worktree)
    rels = []
    for e in exclude:
        ap = os.path.realpath(e) if os.path.isabs(e) else os.path.realpath(os.path.join(worktree, e))
        if ap.startswith(worktree + os.sep):
            rels.append(os.path.relpath(ap, worktree))
    spec = ["--", "."] + [":(exclude)%s" % r for r in rels] if rels else []
    git = ["git", "-C", worktree]
    head = run(git + ["rev-parse", "HEAD"]).stdout.strip()
    branch = run(git + ["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    diff = run(git + ["diff", "HEAD", "--binary"] + spec, binary=True).stdout
    status_z = run(git + ["diff", "HEAD", "--name-status", "-z"] + spec).stdout
    parts = [p for p in status_z.split("\0") if p]
    changed = []
    i = 0
    while i < len(parts):
        code = parts[i]
        if code[:1] in ("R", "C") and i + 2 < len(parts):
            changed.append("%s %s -> %s" % (code, parts[i + 1], parts[i + 2]))
            i += 3
        else:
            changed.append("%s %s" % (code, parts[i + 1] if i + 1 < len(parts) else "?"))
            i += 2
    untracked = sorted(p for p in run(git + ["ls-files", "--others", "--exclude-standard", "-z"]).stdout.split("\0")
                       if p and not any(p == r or p.startswith(r + "/") for r in rels))
    h = hashlib.sha256()
    h.update(head.encode())
    h.update(diff)
    untracked_hashes = {}
    for rel in untracked:
        p = os.path.join(worktree, rel)
        if os.path.isfile(p) and not os.path.islink(p):
            untracked_hashes[rel] = sha256_file(p)
        elif os.path.islink(p):
            untracked_hashes[rel] = "symlink:" + os.readlink(p)
        else:
            continue
        h.update(rel.encode("utf-8", "surrogateescape"))
        h.update(untracked_hashes[rel].encode("utf-8", "surrogateescape"))
    dirty = bool(changed or untracked_hashes)
    stamp = head[:12] + ("+" + h.hexdigest()[:12] if dirty else "")
    return {"stamp": stamp, "head": head, "branch": branch, "dirty": dirty,
            "changed_files": changed, "untracked_files": untracked_hashes,
            "excluded": rels, "computed_at": now()}


def round_version(m, run_dir):
    return version_stamp(m["worktree"], exclude=m.get("version_exclude") or [])


# --------------------------------------------------------------------- init --

def cmd_init(a):
    refuse_if_reviewer()
    require_tool("herdr")
    require_tool("git")
    repo = os.path.abspath(a.repo)
    worktree = os.path.abspath(a.worktree) if a.worktree else repo
    for p in (repo, worktree):
        if not os.path.isdir(p):
            raise Fail("not a directory: %s" % p)
    run(["git", "-C", worktree, "rev-parse", "--git-dir"])

    run_id = "mmr-%s-%s" % (dt.datetime.now().strftime("%Y%m%d-%H%M%S"), secrets.token_hex(2))
    session = run_id
    if find_session(session):
        raise Fail("session %s already exists; refusing to reuse" % session)

    if a.run_dir:
        run_dir = os.path.abspath(a.run_dir)
    else:
        run_dir = os.path.join(run_root(repo), run_id)
    # review material is not part of the reviewed content; if the run dir sits
    # inside the worktree anyway, keep it out of the version stamp
    version_exclude = [run_dir] if os.path.realpath(run_dir).startswith(os.path.realpath(worktree) + os.sep) else []
    os.makedirs(run_dir, exist_ok=False)
    log_path = os.path.join(run_dir, "herdr-server.log")

    manifest = {
        "run_id": run_id, "stage": a.stage, "change_id": a.change,
        "repo_root": repo, "worktree": worktree, "run_dir": run_dir,
        "version_exclude": version_exclude, "created_at": now(),
        "created_by": {"pid": os.getpid(), "cwd": os.getcwd(), "user": os.environ.get("USER")},
        "session": {"name": session, "session_dir": None, "socket_path": None,
                    "server_log": log_path, "state": "starting"},
        "workspace": None, "reviewer_specs": None, "reviewers": [], "rounds": [], "cleanup": None,
    }
    save_manifest(run_dir, manifest)  # intent on disk before the first side effect

    log = open(log_path, "ab")
    subprocess.Popen(["herdr", "--session", session, "server"], stdin=subprocess.DEVNULL,
                     stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    deadline = time.time() + 30
    while True:
        r = herdr(session, ["workspace", "list"], timeout=10, check=False)
        if "error" not in r:
            break
        if time.time() > deadline:
            late = find_session(session) or {}
            manifest["session"].update({"state": "start_failed", "session_dir": late.get("session_dir"),
                                        "socket_path": late.get("socket_path")})
            save_manifest(run_dir, manifest)
            raise Fail("herdr session %s did not answer within 30s; see %s. If `herdr session list` shows it, "
                       "stop and delete it by name." % (session, log_path))
        time.sleep(0.5)
    info = find_session(session) or {}
    manifest["session"].update({"session_dir": info.get("session_dir"), "socket_path": info.get("socket_path"),
                                "state": "running"})
    save_manifest(run_dir, manifest)

    env = ["--env", "%s=reviewer" % ROLE_ENV, "--env", "%s=%s" % (RUN_ENV, run_id)]
    ws = herdr(session, ["workspace", "create", "--cwd", worktree, "--label", run_id, "--no-focus"] + env,
               timeout=60)
    res = ws["result"]
    manifest["workspace"] = {"workspace_id": res["workspace"]["workspace_id"], "tab_id": res["tab"]["tab_id"],
                             "root_pane_id": res["root_pane"]["pane_id"], "label": run_id}
    save_manifest(run_dir, manifest)
    out({"run_id": run_id, "run_dir": run_dir, "session": manifest["session"], "workspace": manifest["workspace"],
         "stage": a.stage, "worktree": worktree, "version_exclude": version_exclude,
         "version": version_stamp(worktree, exclude=version_exclude)["stamp"]})


# -------------------------------------------------------------------- start --

def build_args(spec):
    """Arguments that follow ``--`` on ``agent start``; Herdr launches the binary."""
    if spec.get("args"):
        return list(spec["args"])
    harness, model, level = spec["harness"], spec["model"], spec["reasoning"]
    extra = list(spec.get("extra_args", []))
    if harness == "pi":
        return ["--model", model, "--thinking", level] + extra
    if harness == "agy":
        return ["--model", model, "--effort", level] + extra
    if harness == "codex":
        return ["-m", model, "-c", 'model_reasoning_effort="%s"' % level] + extra
    if harness == "claude":
        return ["--model", model, "--effort", level] + extra
    raise Fail("no argument template for harness %r; give the reviewer explicit args" % harness)


def preflight_model(spec):
    """Best-effort check that the harness lists the requested model. Never blocks."""
    harness, model = spec.get("harness"), spec.get("model")
    try:
        if harness == "pi" and model and "/" in model:
            provider, mid = model.split("/", 1)
            proc = run(["pi", "--offline", "--list-models", mid], timeout=60, check=False)
            if proc.returncode != 0:
                return "check_failed: exit %d: %s" % (proc.returncode, proc.stderr.strip()[-200:])
            for line in proc.stdout.splitlines():
                cols = line.split()
                if len(cols) >= 2 and cols[0] == provider and cols[1] == mid:
                    return "listed"
            return "not_listed"
        if harness == "agy" and model:
            proc = run(["agy", "models"], timeout=60, check=False)
            if proc.returncode != 0:
                return "check_failed: exit %d: %s" % (proc.returncode, proc.stderr.strip()[-200:])
            ids = [l.split("\t")[0].strip() for l in proc.stdout.splitlines() if "\t" in l]
            return "listed" if model in ids else "not_listed"
    except Exception as exc:
        return "check_failed: %s" % exc
    return "not_checked"


def pane_text(session, pane_id, source="visible", lines=None):
    args = ["pane", "read", pane_id, "--source", source]
    if lines:
        args += ["--lines", str(lines)]
    r = herdr(session, args, timeout=30, check=False)
    return r.get("raw") or ""


def foreground_cmdline(session, pane_id):
    """OS view of the pane's foreground process. Some harnesses (pi) rewrite it to a bare name."""
    info = herdr(session, ["pane", "process-info", "--pane", pane_id], timeout=30, check=False)
    procs = info.get("result", {}).get("process_info", {}).get("foreground_processes", [])
    if not procs:
        return None
    pid = min(p["pid"] for p in procs)
    proc = run(["ps", "-o", "command=", "-p", str(pid)], check=False)
    return proc.stdout.strip() or None


def trust_keys(text):
    """Keys that select the affirmative option of a trust dialog, read from the screen.

    Finds the cursor line and the "yes" option line; moves the cursor by the
    line distance between them, then confirms. Returns None when either line
    cannot be identified, so nothing is pressed blindly.
    """
    lines = text.splitlines()
    yes = next((i for i, l in enumerate(lines) if YES_RE.search(l) and not NO_RE.search(l)
                and (CURSOR_RE.match(l) or l.startswith(" "))), None)
    if yes is None:
        return None
    # the cursor line must sit in the same option block: within three lines of
    # the yes line with no blank line in between, so stray ">" output elsewhere
    # on the screen is never mistaken for the cursor
    cursor = None
    for d in range(0, 4):  # nearest cursor line first, so a stray ">" further away never wins
        for i in (yes - d, yes + d):
            if 0 <= i < len(lines) and CURSOR_RE.match(lines[i]):
                block = lines[min(i, yes):max(i, yes) + 1]
                if all(l.strip() for l in block):
                    cursor = i
                    break
        if cursor is not None:
            break
    if cursor is None:
        return None
    step = yes - cursor
    return (["down"] * step if step > 0 else ["up"] * (-step)) + ["enter"]


def answer_trust_dialog(session, name, rec):
    """Accept a harness's first-run trust dialog for the reviewed worktree.

    The worktree is what the reviewer must read, so trusting it is within the
    review's authorization. Any other dialog is left to the orchestrating
    agent; the start fails with the screen text recorded.
    """
    text = pane_text(session, rec["pane_id"])
    rec["screen_before_trust"] = text[-2000:]
    if not TRUST_RE.search(text):
        return {"error": {"code": "agent_not_ready",
                          "message": "blocked during startup by a dialog that is not a recognized trust prompt"},
                "screen": text[-2000:]}
    keys = trust_keys(text)
    if keys is None:
        return {"error": {"code": "agent_not_ready",
                          "message": "trust prompt recognized but its options could not be read; answer it by hand"},
                "screen": text[-2000:]}
    rec["trust_prompt_keys"] = keys
    herdr(session, ["agent", "send-keys", rec["pane_id"]] + keys, timeout=30)
    # Codex shows a splash screen after trusting that Herdr may classify as
    # `unknown` for a while; accept it, settle, and let the first prompt decide.
    settled = ["--until", "idle", "--until", "done", "--until", "unknown"]
    waited = herdr(session, ["agent", "wait", rec["pane_id"], "--timeout", "90000"] + settled, timeout=120, check=False)
    if "error" in waited:
        return waited
    time.sleep(3)  # harnesses re-initialize after trusting; a prompt sent at once can stall
    waited = herdr(session, ["agent", "wait", rec["pane_id"], "--timeout", "30000"] + settled, timeout=60, check=False)
    if "error" in waited:
        return waited
    rec["trust_prompt_answered"] = True
    rec["state_after_trust"] = waited["result"]["agent"].get("agent_status")
    if pane_text(session, rec["pane_id"]) and TRUST_RE.search(pane_text(session, rec["pane_id"])):
        return {"error": {"code": "agent_not_ready", "message": "trust dialog still visible after answering"}}
    return {"result": {"agent": waited["result"]["agent"], "argv": None}}


def load_reviewers(path):
    with open(path, encoding="utf-8") as fh:
        specs = json.load(fh)
    validate_specs(specs)
    return specs


def validate_specs(specs):
    if not isinstance(specs, list) or not specs:
        raise Fail("reviewer list must be a non-empty JSON list")
    names = set()
    for s in specs:
        for key in ("name", "harness", "model", "reasoning"):
            if not s.get(key):
                raise Fail("reviewer entry missing %r (model and reasoning are recorded even with explicit args): %s"
                           % (key, s))
        if not AGENT_NAME_RE.match(s["name"]):
            raise Fail("reviewer name %r must match %s" % (s["name"], AGENT_NAME_RE.pattern))
        if s["name"] in names:
            raise Fail("duplicate reviewer name %r" % s["name"])
        names.add(s["name"])


def cmd_start(a):
    refuse_if_reviewer()
    if not 1000 <= a.start_timeout_ms <= 300000:
        raise Fail("--start-timeout-ms must be between 1000 and 300000 (herdr agent start caps at 300000)")
    m = load_manifest(a.run_dir)
    if not m.get("workspace"):
        raise Fail("run has no workspace recorded; init did not finish")
    session = m["session"]["name"]
    verify_session(m)
    if a.reviewers:
        specs = load_reviewers(a.reviewers)
        started = {r["name"]: r for r in m["reviewers"] if r["status"] == "started"}
        by_name = {sp["name"]: sp for sp in specs}
        for name, rec in started.items():  # a started reviewer keeps its configuration for the whole run
            sp = by_name.get(name)
            if sp is None:
                raise Fail("refusing: reviewer %r is already started in this run but missing from %s; "
                           "a started reviewer cannot be removed, start a new run for a different set" % (name, a.reviewers))
            changed = [k for k in ("harness", "model", "reasoning", "args", "extra_args", "cwd")
                       if (sp.get(k) or None) != (next((o.get(k) for o in m.get("reviewer_specs") or [] if o["name"] == name), None) or None)]
            if changed:
                raise Fail("refusing: reviewer %r is already started with a different %s; a running reviewer's "
                           "configuration cannot change, use a new name or a new run" % (name, ", ".join(changed)))
        m["reviewer_specs"] = specs
        m["reviewer_specs_source"] = os.path.abspath(a.reviewers)
    elif m.get("reviewer_specs"):
        specs = m["reviewer_specs"]  # the run's own configuration, never the defaults again
    else:
        specs = load_reviewers(DEFAULT_REVIEWERS)
        m["reviewer_specs"] = specs
        m["reviewer_specs_source"] = DEFAULT_REVIEWERS
    save_manifest(a.run_dir, m)

    env = ["--env", "%s=reviewer" % ROLE_ENV, "--env", "%s=%s" % (RUN_ENV, m["run_id"])]
    results = []
    for spec in specs:
        prev = reviewer_rec(m, spec["name"])
        if prev and prev["status"] == "started":
            alive = herdr(session, ["agent", "get", spec["name"]], timeout=30, check=False)
            code = (alive.get("error") or {}).get("code")
            if "error" not in alive:
                results.append({"name": spec["name"], "status": "already_started"})
                continue
            if code != "agent_not_found":  # the CLI failed, which proves nothing about the agent: leave it alone
                results.append({"name": spec["name"], "status": "liveness_unknown",
                                "error": (alive.get("error") or {}).get("message") or code})
                continue
            prev["status"] = "gone"  # Herdr confirms the agent is no longer present: retry like a failed start
            prev["error"] = "agent no longer present: %s" % (alive.get("error") or {}).get("message")
        if prev:  # retry: free the name by closing the failed pane, keep the attempt on record
            m["reviewers"].remove(prev)
            m.setdefault("failed_starts", []).append(prev)
            if prev.get("pane_id"):
                prev["pane_closed_on_retry"] = "error" not in herdr(session, ["pane", "close", prev["pane_id"]],
                                                                    timeout=30, check=False)
            save_manifest(a.run_dir, m)
        rec = {"name": spec["name"], "harness": spec["harness"], "model": spec["model"],
               "reasoning": spec["reasoning"], "cwd": spec.get("cwd") or m["worktree"],
               "requested_args": None, "argv": None, "argv_source": None, "preflight": None,
               "tab_id": None, "pane_id": None, "status": "starting", "error": None, "started_at": None}
        m["reviewers"].append(rec)
        try:
            args = build_args(spec)
            rec["requested_args"] = args
            rec["preflight"] = preflight_model(spec)
            tab = herdr(session, ["tab", "create", "--workspace", m["workspace"]["workspace_id"],
                                  "--cwd", rec["cwd"], "--label", spec["name"], "--no-focus"] + env, timeout=60)
            rec["tab_id"] = tab["result"]["tab"]["tab_id"]
            rec["pane_id"] = tab["result"]["root_pane"]["pane_id"]
            save_manifest(a.run_dir, m)  # pane is ours now; record it before the long start
            time.sleep(1.0)
            started = herdr(session, ["agent", "start", spec["name"], "--kind", spec["harness"], "--pane",
                                      rec["pane_id"], "--timeout", str(a.start_timeout_ms), "--"] + args,
                            timeout=a.start_timeout_ms / 1000 + 30, check=False)
            if started.get("error", {}).get("code") == "agent_not_ready":
                started = answer_trust_dialog(session, spec["name"], rec)
            if "error" in started:
                raise Fail("herdr agent start failed: %s" % json.dumps(started, ensure_ascii=False))
            rec["argv"] = started["result"].get("argv")
            rec["argv_source"] = "agent_start response"
            if not rec["argv"]:
                rec["argv"] = [spec["harness"]] + args
                rec["argv_source"] = "requested args (start returned no argv after a trust dialog)"
            if os.path.realpath(rec["cwd"]) != os.path.realpath(m["worktree"]):
                wt = os.path.realpath(m["worktree"])
                mapped = [os.path.join(rec["cwd"], os.path.relpath(os.path.realpath(e), wt))
                          for e in (m.get("version_exclude") or [])]
                try:
                    cv = version_stamp(rec["cwd"], exclude=mapped)["stamp"]
                except Fail as exc:
                    cv = "error: %s" % exc
                rec["cwd_version"] = cv
                rec["cwd_matches_worktree_version"] = cv == round_version(m, a.run_dir)["stamp"]
            rec["process_cmdline"] = foreground_cmdline(session, rec["pane_id"])
            rec["screen_after_start"] = pane_text(session, rec["pane_id"])[-600:]
            rec["agent_kind_detected"] = started["result"]["agent"].get("agent")
            rec["status"] = "started"
            rec["started_at"] = now()
        except Exception as exc:
            rec["status"] = "start_failed"
            rec["error"] = "%s: %s" % (type(exc).__name__, exc)
            if rec["pane_id"]:
                rec["screen_at_failure"] = pane_text(session, rec["pane_id"])[-2000:]
        save_manifest(a.run_dir, m)
        results.append({k: rec.get(k) for k in ("name", "harness", "model", "reasoning", "status", "preflight",
                                                 "pane_id", "argv", "argv_source", "trust_prompt_answered", "error")})
    out({"run_id": m["run_id"], "session": session, "reviewer_specs_source": m.get("reviewer_specs_source"),
         "reviewers": results})


# -------------------------------------------------------------------- round --

def report_path(run_dir, rnd, name):
    return os.path.join(run_dir, "round-%d" % rnd, "report-%s.md" % name)


def parse_report(path):
    if not os.path.isfile(path):
        return None
    fields = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            mt = re.match(r"^\s*[-*]?\s*\**([A-Za-z ]+?)\**\s*:\**\s*(.+?)\s*$", line)
            if mt:
                key = mt.group(1).strip()
                if key in REQUIRED_REPORT_FIELDS and key not in fields:
                    fields[key] = mt.group(2).strip().strip("`*").strip()
            if len(fields) == len(REQUIRED_REPORT_FIELDS):
                break
    return fields


def normalize_verdict(text):
    """Exactly one of the three tokens, after removing code or bold markers only."""
    t = text.strip().strip("`*").strip()
    return t if t in VERDICTS else None


def check_report(path, m, rnd, name):
    """Exact header check: identity, round, stage, version, and a single verdict token."""
    fields = parse_report(path)
    if fields is None:
        return {"status": "missing", "problems": ["report file not found"]}
    problems = []
    for key in REQUIRED_REPORT_FIELDS:
        if key not in fields:
            problems.append("missing field: %s" % key)
    rr = next((r for r in m["rounds"] if r["round"] == rnd), None)
    if "Run ID" in fields and fields["Run ID"] != m["run_id"]:
        problems.append("Run ID mismatch: %s" % fields["Run ID"])
    if "Round" in fields and fields["Round"] != str(rnd):
        problems.append("Round mismatch: %s" % fields["Round"])
    if "Reviewer" in fields and not re.match(r"^%s(\s|\(|$)" % re.escape(name), fields["Reviewer"]):
        problems.append("Reviewer is not %s: %s" % (name, fields["Reviewer"]))
    if "Stage" in fields and fields["Stage"].lower() != str(m["stage"]).lower():
        problems.append("Stage mismatch: report=%s run=%s" % (fields["Stage"], m["stage"]))
    if rr and "Version" in fields and fields["Version"] != rr["version"]["stamp"]:
        problems.append("Version mismatch: report=%s round=%s" % (fields["Version"], rr["version"]["stamp"]))
    verdict = normalize_verdict(fields["Verdict"]) if "Verdict" in fields else None
    if "Verdict" in fields and not verdict:
        problems.append("Verdict must be exactly one of PASS / CHANGES_REQUIRED / INCOMPLETE: %s" % fields["Verdict"])
    return {"status": "ok" if not problems else "invalid", "fields": fields, "verdict": verdict,
            "problems": problems, "size": os.path.getsize(path)}


def brief_version_line(path):
    """The stamp named in the brief header's "Version under review" line, if present."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            mt = re.match(r"^\s*[-*]?\s*\**Version under review\**\s*:\**\s*`?([^\s`(]+)", line)
            if mt:
                return mt.group(1).rstrip(".,;:)*")
    return None


def prompt_text(m, rnd, name, brief, report):
    rec = reviewer_rec(m, name) or {}
    ident = "%s / %s / %s" % (rec.get("harness"), rec.get("model"), rec.get("reasoning"))
    return ("Multi-model review run %s, round %d. You are reviewer '%s', configured as %s "
            "(use this in the Reviewer header line). You are a reviewer in this batch: do not invoke "
            "the multi-model-review skill or start reviewers of your own. Read the brief at %s and follow it. "
            "Write your report to %s (Markdown, starting with the six header lines the brief specifies; "
            "Verdict is exactly one of PASS, CHANGES_REQUIRED, INCOMPLETE), plus any reproduction material "
            "the brief authorizes under its scratch path; modify no other file. "
            "Reply with one line when the report is written."
            % (m["run_id"], rnd, name, ident, brief, report))


def wait_one(session, name, timeout_ms, send_text=None, on_send=None):
    """Prompt (optional) and wait for a settled state. Always returns a dict."""
    t0 = time.time()
    if send_text is not None:
        cur = herdr(session, ["agent", "get", name], timeout=30, check=False)
        state = cur.get("result", {}).get("agent", {}).get("agent_status")
        if state == "working":
            return {"status": "busy_not_sent", "agent_status": state, "elapsed_s": 0,
                    "detail": "agent is still working on a previous request; one request at a time"}
        if "error" in cur:
            return {"status": "error", "detail": cur["error"].get("message") or cur["error"].get("code"), "elapsed_s": 0}
        if on_send:
            on_send()
        r = herdr(session, ["agent", "prompt", name, send_text, "--wait", "--timeout", str(timeout_ms)],
                  timeout=timeout_ms / 1000 + 60, check=False)
    else:
        r = herdr(session, ["agent", "wait", name, "--timeout", str(timeout_ms)],
                  timeout=timeout_ms / 1000 + 60, check=False)
    elapsed = round(time.time() - t0, 1)
    err = r.get("error")
    delivery = None
    if send_text is not None:
        code = (err or {}).get("code")
        if err is None:
            delivery = "written"           # Herdr reported the submission and a settled state
        elif code == "agent_blocked":
            delivery = "not_sent"          # Herdr refused before writing anything
        elif code in ("timeout", "agent_prompt_stalled"):
            delivery = "written"           # Herdr wrote the text; stalled means no activity followed
        else:
            delivery = "unknown"           # CLI timeout or an unstructured failure: cannot be confirmed
    if err:
        code = err.get("code") or ""
        status = {"agent_blocked": "blocked", "agent_prompt_stalled": "stalled", "timeout": "timeout",
                  "cli_timeout": "cli_timeout"}.get(code, "error")
        return {"status": status, "detail": err.get("message") or code, "elapsed_s": elapsed, "delivery": delivery}
    agent = r.get("result", {}).get("agent", {})
    return {"status": "settled", "agent_status": agent.get("agent_status"), "elapsed_s": elapsed, "delivery": delivery}


def wait_reviewers(m, run_dir, rnd, names, timeout_ms, send, message=None):
    session = m["session"]["name"]
    rr = get_round(m, rnd)
    results = {}
    lock = threading.Lock()

    def worker(name):
        rp = report_path(run_dir, rnd, name)
        text = (message or prompt_text(m, rnd, name, rr["brief"], rp)) if send else None
        attempt = {}

        def on_send():  # the exact text and the moment it goes out, on disk before the long wait
            with lock:
                attempt.update({"text": text, "attempted_at": now(), "delivery": "unknown"})
                rr.setdefault("prompts", {}).setdefault(name, []).append(attempt)
                save_manifest(run_dir, m)

        if text is not None and message is None and check_report(rp, m, rnd, name)["status"] == "ok":
            res = dict(rr.get("results", {}).get(name) or {})  # keep the earlier result; nothing to add
            res.update({"detail": "valid report already present; nothing sent"})
        else:
            try:
                res = wait_one(session, name, timeout_ms, text, on_send)
            except Exception as exc:  # a reviewer must never vanish from the results
                res = {"status": "error", "detail": "%s: %s" % (type(exc).__name__, exc), "elapsed_s": None}
        if attempt:  # resolve only the attempt this call made; earlier attempts keep their record
            with lock:
                attempt["delivery"] = res.get("delivery") or "unknown"
                attempt["result"] = res.get("status")
        check = check_report(rp, m, rnd, name)
        if check["status"] == "ok":
            res["status"] = "report_ready"
        elif check["status"] == "invalid":
            res["status"] = "report_invalid"
        elif res["status"] == "settled" and res.get("agent_status") == "blocked":
            res["status"] = "blocked"  # Herdr counts a dialog as settled; the orchestrator must inspect it
        elif res["status"] == "settled":
            res["status"] = "settled_no_report"
        res.update({"report": rp, "report_check": check, "finished_at": now()})
        with lock:
            results[name] = res

    threads = [threading.Thread(target=worker, args=(n,), daemon=True) for n in names]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    rr.setdefault("results", {}).update(results)
    save_manifest(run_dir, m)
    return results


def brief_results(results):
    summary = {}
    for name, res in results.items():
        item = {k: v for k, v in res.items() if k != "report_check"}
        item["problems"] = res["report_check"].get("problems", [])
        summary[name] = item
    return summary


def cmd_round(a):
    refuse_if_reviewer()
    m = load_manifest(a.run_dir)
    brief = os.path.abspath(a.brief)
    if not os.path.isfile(brief):
        raise Fail("brief not found: %s" % brief)
    verify_session(m)
    rnd = a.round or (max([r["round"] for r in m["rounds"]] + [0]) + 1)
    if any(r["round"] == rnd for r in m["rounds"]):
        raise Fail("round %d already exists; use `wait` (with --reprompt if needed) to continue it" % rnd)
    started = [r["name"] for r in m["reviewers"] if r["status"] == "started"]
    names = a.reviewers.split(",") if a.reviewers else started
    missing = [n for n in names if n not in started]
    if missing:
        raise Fail("reviewers not started in this run: %s" % ", ".join(missing))
    if not names:
        raise Fail("no started reviewer to prompt; run `start` first")
    os.makedirs(os.path.join(a.run_dir, "round-%d" % rnd), exist_ok=True)
    version = round_version(m, a.run_dir)
    stated = brief_version_line(brief)
    if stated and stated != version["stamp"]:
        raise Fail("the brief says 'Version under review: %s' but the worktree stamp is now %s; "
                   "regenerate the brief header (or revert the change) before prompting" % (stated, version["stamp"]))
    m["rounds"].append({"round": rnd, "brief": brief, "brief_sha256": sha256_file(brief), "version": version,
                        "reviewers": names, "prompted_at": now(), "timeout_min": a.timeout_min,
                        "prompts": {}, "results": {}})
    save_manifest(a.run_dir, m)
    results = wait_reviewers(m, a.run_dir, rnd, names, int(a.timeout_min * 60000), send=True)
    out({"run_id": m["run_id"], "round": rnd, "version": version["stamp"], "dirty": version["dirty"],
         "brief_sha256": m["rounds"][-1]["brief_sha256"], "results": brief_results(results)})


def cmd_wait(a):
    refuse_if_reviewer()
    m = load_manifest(a.run_dir)
    if a.message is not None:
        if not a.message.strip():
            raise Fail("--message must not be blank")
        if not a.reprompt or not a.reviewers:
            raise Fail("--message requires --reprompt and --reviewers (a correction is addressed to named reviewers)")
    verify_session(m)
    rnd = a.round or latest_round(m)
    rr = get_round(m, rnd)
    if a.reviewers:
        names = a.reviewers.split(",")
        unknown = [n for n in names if n not in rr["reviewers"]]
        if unknown:
            raise Fail("not reviewers of round %d: %s (round has: %s)" % (rnd, ", ".join(unknown), ", ".join(rr["reviewers"])))
    else:
        names = [n for n in rr["reviewers"] if rr["results"].get(n, {}).get("status") != "report_ready"]
    if not names:
        out({"round": rnd, "message": "all reviewers of this round already have valid reports"})
        return
    results = wait_reviewers(m, a.run_dir, rnd, names, int(a.timeout_min * 60000), send=a.reprompt, message=a.message)
    out({"run_id": m["run_id"], "round": rnd, "reprompted": a.reprompt, "results": brief_results(results)})


def cmd_collect(a):
    refuse_if_reviewer()
    m = load_manifest(a.run_dir)
    rnd = a.round or latest_round(m)
    rr = get_round(m, rnd)
    summary = {"run_id": m["run_id"], "stage": m["stage"], "round": rnd, "version": rr["version"]["stamp"],
               "brief": rr["brief"], "reports": {}, "other_reviewers": {}}
    for name in rr["reviewers"]:
        summary["reports"][name] = check_report(report_path(a.run_dir, rnd, name), m, rnd, name)
    current = round_version(m, a.run_dir)
    wt_changed = current["stamp"] != rr["version"]["stamp"]
    brief_changed = (not os.path.isfile(rr["brief"])) or sha256_file(rr["brief"]) != rr.get("brief_sha256")
    # reviewers started in this run but not asked in this round: where do they stand?
    for rec in m["reviewers"]:
        if rec["status"] != "started" or rec["name"] in rr["reviewers"]:
            continue
        latest = None
        for prev in sorted(m["rounds"], key=lambda r: r["round"], reverse=True):
            res = prev.get("results", {}).get(rec["name"])
            if res and res.get("status") == "report_ready":
                latest = {"round": prev["round"], "version": prev["version"]["stamp"],
                          "brief_sha256": prev.get("brief_sha256"), "verdict": res["report_check"].get("verdict")}
                break
        same_wt = bool(latest and latest["version"] == rr["version"]["stamp"])
        same_brief = bool(latest and latest["brief_sha256"] == rr.get("brief_sha256"))
        summary["other_reviewers"][rec["name"]] = {
            "latest_valid_report": latest, "same_worktree_version": same_wt, "same_brief": same_brief,
            "reviewed_this_version": same_wt and same_brief and not wt_changed and not brief_changed}
    summary["worktree_version_now"] = current["stamp"]
    summary["worktree_changed_since_round"] = wt_changed
    summary["brief_changed_since_round"] = brief_changed
    for rep in summary["reports"].values():  # valid for the round, and still describing the current worktree?
        rep["matches_current_version"] = rep["status"] == "ok" and not wt_changed and not brief_changed
    path = os.path.join(a.run_dir, "round-%d" % rnd, "summary.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    summary["summary_file"] = path
    out(summary)


def cmd_status(a):
    refuse_if_reviewer()
    m = load_manifest(a.run_dir)
    session = m["session"]["name"]
    live = find_session(session)
    agents = None
    try:  # read-only: a warning found here is printed, and persisted by the next control command
        verify_session(m, require_running=False)
        ownership = "ok" if live else "session absent"
    except Unverified as exc:
        ownership = "unverified: %s" % exc
    except Fail as exc:
        ownership = "mismatch: %s" % exc
    if ownership == "ok" and live.get("running"):  # never read inside a session that is not verified ours
        agents = herdr(session, ["agent", "list"], timeout=30, check=False).get("result", {}).get("agents")
    out({"run_id": m["run_id"], "stage": m["stage"], "session": live or {"name": session, "missing": True},
         "ownership": ownership, "warnings": m.get("warnings", []), "manifest_session_state": m["session"].get("state"),
         "reviewers": [{k: r.get(k) for k in ("name", "harness", "model", "reasoning", "status", "pane_id")}
                       for r in m["reviewers"]],
         "rounds": [{"round": r["round"], "version": r["version"]["stamp"],
                     "results": {n: x.get("status") for n, x in r.get("results", {}).items()}} for r in m["rounds"]],
         "live_agents": agents, "cleanup": m.get("cleanup")})


def cmd_version(a):
    exclude = list(a.exclude or [])
    worktree = a.worktree
    if a.run_dir:
        m = load_manifest(a.run_dir)
        exclude += m.get("version_exclude") or []
        worktree = worktree or m["worktree"]
    if not worktree:
        raise Fail("give --worktree or --run-dir")
    out(version_stamp(os.path.abspath(worktree), exclude=exclude))


# ------------------------------------------------------------------ cleanup --

def cmd_cleanup(a):
    refuse_if_reviewer()
    m = load_manifest(a.run_dir)
    sess = m["session"]
    name = sess["name"]
    record = m.get("cleanup") or {"actions": []}
    record["started_at"] = now()
    m["cleanup"] = record

    def note(msg):
        record["actions"].append("%s %s" % (now(), msg))
        save_manifest(a.run_dir, m)

    try:
        live = verify_session(m, require_running=False)
        if live is None:
            note("session already absent")
        else:
            if live.get("running"):
                r = herdr(name, ["agent", "list"], timeout=30, check=False)
                record["agents_at_cleanup"] = [x.get("name") for x in r.get("result", {}).get("agents", [])]
                for rec in m["reviewers"]:  # orderly exit: close each reviewer pane we opened
                    if rec.get("pane_id"):
                        res = herdr(name, ["pane", "close", rec["pane_id"]], timeout=30, check=False)
                        note("pane %s (%s) %s" % (rec["pane_id"], rec["name"],
                                                   "closed" if "error" not in res else "close failed: %s" % res.get("error")))
                run(["herdr", "session", "stop", name, "--json"], timeout=120)
                sess["state"] = "stopped"
                note("session stopped")
            run(["herdr", "session", "delete", name, "--json"], timeout=60)
            sess["state"] = "deleted"
            note("session deleted")
        record["outcome"] = "complete"
    except Fail as exc:
        record["outcome"] = "failed"
        record["error"] = str(exc)
        save_manifest(a.run_dir, m)
        raise
    save_manifest(a.run_dir, m)
    out({"run_id": m["run_id"], "session": name, "cleanup": record, "run_dir_kept": a.run_dir})


# --------------------------------------------------------------------- main --

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create run, session, workspace, manifest")
    s.add_argument("--repo", required=True, help="repository root")
    s.add_argument("--stage", required=True, choices=["proposal", "implementation", "other"])
    s.add_argument("--change", help="OpenSpec change ID, recorded in the manifest")
    s.add_argument("--worktree", help="worktree reviewers read (default: --repo)")
    s.add_argument("--run-dir", help="override the run directory (default: a per-repo folder under the system temp dir, see `list`)")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("list", help="list review runs recorded for a repository")
    s.add_argument("--repo", required=True, help="repository root")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("version", help="print the version stamp of a worktree")
    s.add_argument("--run-dir", help="use the worktree and exclusions recorded in this run's manifest")
    s.add_argument("--worktree", help="worktree to stamp (default: the run's worktree)")
    s.add_argument("--exclude", action="append", help="extra path left out of the stamp (repeatable)")
    s.set_defaults(fn=cmd_version)

    s = sub.add_parser("start", help="start reviewer agents, one tab each; retries failed ones")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--reviewers", help="JSON list of reviewer specs; omitted = this run's recorded set, "
                                       "or assets/default-reviewers.json for a new run")
    s.add_argument("--start-timeout-ms", type=int, default=90000, help="1000 to 300000 (Herdr's cap)")
    s.set_defaults(fn=cmd_start)

    s = sub.add_parser("round", help="record a round, prompt reviewers, wait for reports")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--brief", required=True, help="brief file reviewers must read")
    s.add_argument("--round", type=int, help="round number (default: next)")
    s.add_argument("--reviewers", help="comma-separated subset (default: all started)")
    s.add_argument("--timeout-min", type=float, default=45)
    s.set_defaults(fn=cmd_round)

    s = sub.add_parser("wait", help="wait again for reviewers without a valid report")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--round", type=int)
    s.add_argument("--reviewers", help="comma-separated subset")
    s.add_argument("--timeout-min", type=float, default=30)
    s.add_argument("--reprompt", action="store_true",
                   help="send the round prompt again before waiting (only after confirming the agent never started it); "
                        "skips reviewers whose report already validates unless --message is given")
    s.add_argument("--message", help="with --reprompt and --reviewers: send this text instead of the round prompt, "
                                     "for example a header correction; recorded as a prompt attempt like any other")
    s.set_defaults(fn=cmd_wait)

    s = sub.add_parser("collect", help="check report headers and write summary.json")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--round", type=int)
    s.set_defaults(fn=cmd_collect)

    s = sub.add_parser("status", help="show manifest and live agents")
    s.add_argument("--run-dir", required=True)
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("cleanup", help="close reviewer panes, stop and delete the run-owned session")
    s.add_argument("--run-dir", required=True)
    s.set_defaults(fn=cmd_cleanup)

    a = p.parse_args(argv)
    try:
        a.fn(a)
    except Fail as exc:
        out({"error": str(exc)})
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
