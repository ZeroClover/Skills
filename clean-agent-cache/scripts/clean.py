#!/usr/bin/env python3
"""clean-agent-cache: reclaim disk used by AI coding agents.

Reads the structured registry at ../references/targets.toml and removes
safe-to-delete caches, logs, temp files, and (opt-in) history/sessions.

Safety model
------------
- DRY-RUN by default. Nothing is deleted unless you pass --apply.
- Only `safe` targets run by default. Add `--include history,aggressive`
  (or `--include all`) to opt into history/session data and large
  re-downloadable bundles.
- A `protected` allow-never list in the registry is enforced as
  defense-in-depth: the engine refuses to delete any path that equals,
  contains, or is contained by a protected path.
- Targets flagged `requires_app_closed` are skipped while the matching
  agent process is running (quit the app, then re-run).

Usage
-----
  uv run python clean.py                      # dry-run, safe targets, all agents
  uv run python clean.py --apply --yes        # actually delete safe targets
  uv run python clean.py --agent codex,claude-code
  uv run python clean.py --include history --older-than 30
  uv run python clean.py --include all --apply --yes
  uv run python clean.py --list-agents
  uv run python clean.py --list-targets
  uv run python clean.py --json               # machine-readable plan/result
"""
from __future__ import annotations

import argparse
import fnmatch
import glob as globmod
import json
import math
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    sys.stderr.write("This tool requires Python 3.11+ (tomllib).\n")
    sys.exit(2)

REGISTRY = Path(__file__).resolve().parent.parent / "references" / "targets.toml"
RISK_ORDER = ("safe", "history", "aggressive")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def current_os() -> str:
    return {"Darwin": "darwin", "Linux": "linux", "Windows": "windows"}.get(
        platform.system(), platform.system().lower()
    )


def expand(pattern: str) -> str:
    return os.path.expanduser(pattern)


def iglob(pattern: str) -> list[str]:
    ep = expand(pattern)
    return globmod.glob(ep, recursive=("**" in ep))


def mtime(path: str) -> float:
    try:
        return os.lstat(path).st_mtime
    except OSError:
        return 0.0


def path_size(path: str) -> int:
    """Apparent size in bytes for a file or directory tree."""
    p = Path(path)
    if p.is_symlink() or p.is_file():
        try:
            return p.lstat().st_size
        except OSError:
            return 0
    total = 0
    for root, _dirs, files in os.walk(path, onerror=lambda _e: None):
        for f in files:
            fp = os.path.join(root, f)
            try:
                total += os.lstat(fp).st_size
            except OSError:
                pass
    return total


def human(n: int) -> str:
    f = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if f < 1024 or unit == "TB":
            return f"{f:.0f} {unit}" if unit == "B" else f"{f:.1f} {unit}"
        f /= 1024
    return f"{f:.1f} TB"


# --------------------------------------------------------------------------- #
# Protected-path enforcement (defense-in-depth)
# --------------------------------------------------------------------------- #
def build_protected(patterns: list[str]) -> list[str]:
    return [os.path.abspath(expand(p)) for p in patterns]


def _has_glob(s: str) -> bool:
    return any(ch in s for ch in "*?[")


def is_protected(candidate: str, protected: list[str]) -> bool:
    """True if deleting `candidate` would touch a protected path.

    Covers three overlap cases for each protected pattern P:
      1. candidate matches P, or sits inside a dir matching P;
      2. candidate is an ancestor of a concrete path matched by P
         (deleting candidate would nuke the protected child);
      3. literal P sits inside candidate.
    """
    c = os.path.abspath(candidate).rstrip("/")
    for p in protected:
        p = p.rstrip("/")
        # 1. candidate equals/inside protected
        if fnmatch.fnmatch(c, p) or fnmatch.fnmatch(c, p + "/*"):
            return True
        parent = os.path.dirname(c)
        while parent and parent != os.path.dirname(parent):
            if fnmatch.fnmatch(parent, p):
                return True
            parent = os.path.dirname(parent)
        # 2. candidate is an ancestor of something protected
        for concrete in globmod.glob(p, recursive=("**" in p)):
            cc = os.path.abspath(concrete).rstrip("/")
            if cc == c or cc.startswith(c + "/"):
                return True
        # 3. literal protected under candidate
        if not _has_glob(p) and (p == c or p.startswith(c + "/")):
            return True
    return False


# --------------------------------------------------------------------------- #
# Running-process detection
# --------------------------------------------------------------------------- #
def ps_snapshot() -> str:
    try:
        out = subprocess.run(
            ["ps", "-A", "-o", "command"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        return out.lower()
    except Exception:
        return ""


def agent_running(meta: dict, ps_text: str) -> bool:
    return any(m.lower() in ps_text for m in meta.get("process_match", []))


# --------------------------------------------------------------------------- #
# Planning
# --------------------------------------------------------------------------- #
def plan_target(target: dict, protected: list[str], older_cutoff: float | None):
    """Return (items, blocked) where items is [(path, size)]."""
    op = target["op"]
    items: list[tuple[str, int]] = []
    blocked: list[str] = []

    def consider(path: str) -> None:
        if is_protected(path, protected):
            blocked.append(path)
            return
        if older_cutoff is not None and mtime(path) > older_cutoff:
            return
        items.append((path, path_size(path)))

    if op == "delete-contents":
        for pat in target["paths"]:
            for match in iglob(pat):
                if os.path.isdir(match) and not os.path.islink(match):
                    for child in sorted(os.listdir(match)):
                        consider(os.path.join(match, child))
                elif os.path.exists(match) or os.path.islink(match):
                    consider(match)
    elif op in ("delete-glob", "delete-path"):
        for pat in target["paths"]:
            for match in iglob(pat):
                consider(match)
    elif op == "keep-recent":
        keep = int(target.get("keep", 1))
        matched: list[str] = []
        for pat in target["paths"]:
            matched.extend(iglob(pat))
        matched = sorted(set(matched), key=mtime, reverse=True)
        for match in matched[keep:]:
            consider(match)
    else:  # unknown op
        blocked.append(f"<unknown op: {op}>")
    return items, blocked


def delete_path(path: str) -> bool:
    p = Path(path)
    try:
        if p.is_dir() and not p.is_symlink():
            shutil.rmtree(p, ignore_errors=False)
        else:
            p.unlink()
        return True
    except OSError as e:
        sys.stderr.write(f"  ! failed to delete {path}: {e}\n")
        return False


# --------------------------------------------------------------------------- #
# SQLite pruning (for huge log databases — reclaim disk without deleting the file)
# --------------------------------------------------------------------------- #
def _table_exists(con: sqlite3.Connection, table: str) -> bool:
    cur = con.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    )
    return cur.fetchone() is not None


def count_rows(files: list[str], table: str) -> int | None:
    """Total rows in `table` across the given DB files (read-only). None if absent."""
    if not table:
        return None
    total, found = 0, False
    for f in files:
        try:
            uri = f"file:{os.path.abspath(f)}?mode=ro"
            con = sqlite3.connect(uri, uri=True, timeout=10)
            try:
                if _table_exists(con, table):
                    total += con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                    found = True
            finally:
                con.close()
        except sqlite3.Error:
            pass
    return total if found else None


def _detect_ts_scale(con: sqlite3.Connection, table: str, ts_col: str) -> float:
    """Return multiplier converting epoch-seconds to the column's unit (1/1e3/1e6/1e9)."""
    try:
        row = con.execute(f'SELECT MAX("{ts_col}") FROM "{table}"').fetchone()
        mx = float(row[0]) if row and row[0] else 0.0
    except sqlite3.Error:
        return 1.0
    if mx <= 0:
        return 1.0
    now = time.time()
    return min((1.0, 1e3, 1e6, 1e9),
               key=lambda s: abs(math.log10(mx) - math.log10(now * s)))


def sqlite_prune(dbfile: str, table: str, ts_col: str | None,
                 older_cutoff: float | None) -> tuple[int, str | None]:
    """DELETE rows (older than cutoff, else all) from `table`, then VACUUM.

    Returns (bytes_reclaimed, error). Requires exclusive access (app closed).
    """
    try:
        before = os.path.getsize(dbfile)
    except OSError as e:
        return 0, str(e)
    try:
        con = sqlite3.connect(dbfile, isolation_level=None, timeout=15)
    except sqlite3.Error as e:
        return 0, str(e)
    try:
        con.execute("PRAGMA busy_timeout=15000")
        if not _table_exists(con, table):
            return 0, f"table '{table}' not found"
        if older_cutoff is not None and ts_col:
            scale = _detect_ts_scale(con, table, ts_col)
            cutoff = int(older_cutoff * scale)
            con.execute(f'DELETE FROM "{table}" WHERE "{ts_col}" < ?', (cutoff,))
        else:
            con.execute(f'DELETE FROM "{table}"')
        # In WAL mode VACUUM writes the compacted image into the WAL and leaves
        # the main file at its old size. Fold the WAL, drop to rollback-journal
        # mode so VACUUM truncates the main file, then restore the original mode.
        prev_mode = con.execute("PRAGMA journal_mode").fetchone()[0]
        try:
            con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        except sqlite3.Error:
            pass
        con.execute("PRAGMA journal_mode=DELETE")
        con.execute("VACUUM")
        if str(prev_mode).lower() == "wal":
            con.execute("PRAGMA journal_mode=WAL")
    except sqlite3.Error as e:
        return 0, str(e)
    finally:
        con.close()
    try:
        after = os.path.getsize(dbfile)
    except OSError:
        after = before
    return max(0, before - after), None


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def load_registry() -> dict:
    with open(REGISTRY, "rb") as fh:
        return tomllib.load(fh)


def parse_args(argv):
    ap = argparse.ArgumentParser(
        prog="clean.py",
        description="Reclaim disk used by AI coding agents (dry-run by default).",
    )
    ap.add_argument("--agent", default="", help="comma-separated agent keys to limit to")
    ap.add_argument("--category", default="", help="comma-separated categories to limit to")
    ap.add_argument(
        "--include", default="",
        help="extra risk tiers beyond 'safe': history, aggressive, or all",
    )
    ap.add_argument(
        "--older-than", type=float, default=None, metavar="DAYS",
        help="only delete items whose mtime is older than DAYS",
    )
    ap.add_argument("--apply", action="store_true", help="actually delete (default: dry-run)")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt with --apply")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--list-agents", action="store_true", help="list known agents and exit")
    ap.add_argument("--list-targets", action="store_true", help="list known targets and exit")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    reg = load_registry()
    agents = {a["key"]: a for a in reg.get("agent", [])}
    targets = reg.get("target", [])
    protected = build_protected(reg.get("protected", []))
    cur_os = current_os()

    if args.list_agents:
        for k, a in agents.items():
            print(f"{k:14s} {a['label']}")
        return 0
    if args.list_targets:
        for t in targets:
            print(f"{t['agent']:14s} {t['id']:26s} {t['risk']:10s} {t['category']:18s} {t['description']}")
        return 0

    # filters
    risk_set = {"safe"}
    inc = {x.strip() for x in args.include.split(",") if x.strip()}
    if "all" in inc:
        risk_set = set(RISK_ORDER)
    else:
        risk_set |= inc
    bad = risk_set - set(RISK_ORDER)
    if bad:
        sys.stderr.write(f"Unknown risk tier(s): {', '.join(sorted(bad))}\n")
        return 2
    agent_filter = {x.strip() for x in args.agent.split(",") if x.strip()}
    cat_filter = {x.strip() for x in args.category.split(",") if x.strip()}
    older_cutoff = None if args.older_than is None else time.time() - args.older_than * 86400

    ps_text = ps_snapshot()
    running = {k: agent_running(a, ps_text) for k, a in agents.items()}

    plans = []  # dicts describing each actionable/skipped target
    for t in targets:
        if agent_filter and t["agent"] not in agent_filter:
            continue
        if t["risk"] not in risk_set:
            continue
        if cat_filter and t["category"] not in cat_filter:
            continue
        t_os = t.get("os")
        if t_os and cur_os not in t_os:
            continue

        needs_closed = bool(t.get("requires_app_closed"))
        is_running = running.get(t["agent"], False)
        skipped = needs_closed and is_running
        detail = ""

        if t["op"] == "sqlite-prune":
            files, blocked = [], []
            for pat in t["paths"]:
                for f in iglob(pat):
                    (blocked if is_protected(f, protected) else files).append(f)
            size = sum(path_size(f) for f in files)
            count = len(files)
            if not files:
                status = "empty"
            elif skipped:
                status = "skip-running"
            else:
                status = "plan"
                rows = count_rows(files, t.get("table", ""))
                if rows is not None:
                    detail = f"{rows:,} rows in '{t.get('table')}' (reclaim shown is full file size)"
            item_paths = files
        else:
            items, blocked = plan_target(t, protected, older_cutoff)
            size = sum(s for _p, s in items)
            count = len(items)
            item_paths = [p for p, _s in items]
            if skipped:
                status = "skip-running"
            elif not items:
                status = "empty"
            else:
                status = "plan"

        plans.append({
            "agent": t["agent"], "id": t["id"], "risk": t["risk"],
            "category": t["category"], "surface": t.get("surface", ""),
            "op": t["op"], "table": t.get("table"), "ts_column": t.get("ts_column"),
            "description": t["description"], "note": t.get("note", ""),
            "detail": detail, "status": status, "size": size, "count": count,
            "items": item_paths, "blocked": blocked, "reclaimed": 0,
        })

    actionable = [p for p in plans if p["status"] == "plan"]
    total = sum(p["size"] for p in actionable)
    blocked_running = sum(p["size"] for p in plans if p["status"] == "skip-running")
    all_blocked = [b for p in plans for b in p["blocked"]]

    if args.json:
        out = {
            "os": cur_os, "apply": args.apply, "risk_tiers": sorted(risk_set),
            "reclaimable_bytes": total, "blocked_by_running_bytes": blocked_running,
            "targets": plans,
        }
        # apply happens below for json too, but print plan first for safety
    # ---- apply confirmation ----
    did_apply = False
    if args.apply and actionable:
        if not args.yes:
            if not sys.stdin.isatty():
                sys.stderr.write("Refusing to --apply without --yes in non-interactive mode.\n")
                return 3
            resp = input(f"Delete {sum(p['count'] for p in actionable)} items "
                         f"(~{human(total)}) across {len(actionable)} targets? type 'yes': ")
            if resp.strip().lower() != "yes":
                print("Aborted.")
                return 1
        did_apply = True
        for p in actionable:
            if p["op"] == "sqlite-prune":
                for dbf in p["items"]:
                    if is_protected(dbf, protected):
                        p["blocked"].append(dbf)
                        continue
                    reclaimed, err = sqlite_prune(
                        dbf, p["table"], p["ts_column"], older_cutoff)
                    if err:
                        sys.stderr.write(f"  ! sqlite prune {dbf}: {err}\n")
                    p["reclaimed"] += reclaimed
            else:
                for path in p["items"]:
                    # re-check protection at delete time
                    if is_protected(path, protected):
                        p["blocked"].append(path)
                        continue
                    if delete_path(path):
                        p["reclaimed"] += 0  # size already accounted
            p["status"] = "deleted"

    if args.json:
        out["applied"] = did_apply
        print(json.dumps(out, indent=2))
        return 0

    # ---- human report ----
    mode = "APPLYING" if did_apply else ("APPLY (no-op)" if args.apply else "DRY-RUN")
    print(f"clean-agent-cache  [{mode}]  os={cur_os}  tiers={','.join(sorted(risk_set))}")
    print(f"registry: {REGISTRY}")
    print("=" * 78)

    by_agent: dict[str, list[dict]] = {}
    for p in plans:
        by_agent.setdefault(p["agent"], []).append(p)

    for agent_key, group in by_agent.items():
        label = agents.get(agent_key, {}).get("label", agent_key)
        run_tag = "  (running)" if running.get(agent_key) else ""
        shown = [p for p in group if p["status"] != "empty" or p["blocked"]]
        if not shown:
            continue
        print(f"\n▸ {label}{run_tag}")
        for p in group:
            if p["status"] == "empty" and not p["blocked"]:
                continue
            tag = {
                "plan": "would delete", "deleted": "deleted",
                "skip-running": "SKIP (quit app)", "empty": "—",
            }.get(p["status"], p["status"])
            shown_size = p["reclaimed"] if (did_apply and p["op"] == "sqlite-prune") else p["size"]
            unit = "db file(s)" if p["op"] == "sqlite-prune" else "item(s)"
            print(f"    [{p['risk']:>10}] {p['id']:26s} {human(shown_size):>9}  "
                  f"{tag:15s} {p['count']} {unit}")
            if p["detail"]:
                print(f"                 ↳ {p['detail']}")
            if p["note"]:
                print(f"                 ↳ {p['note']}")
            if p["blocked"]:
                print(f"                 ↳ BLOCKED by protected list: {len(p['blocked'])} path(s)")

    print("\n" + "=" * 78)
    if did_apply:
        reclaimed_total = sum(
            p["reclaimed"] if p["op"] == "sqlite-prune" else p["size"]
            for p in actionable)
        print(f"Reclaimed: {human(reclaimed_total)} across {len(actionable)} target(s).")
    else:
        print(f"Reclaimable: {human(total)} across {len(actionable)} target(s).")
    if blocked_running:
        print(f"Held back by running apps: {human(blocked_running)} "
              f"(quit the app, then re-run).")
    if all_blocked:
        print(f"Protected paths skipped: {len(all_blocked)}.")
    if not args.apply and total:
        print("Re-run with --apply --yes to delete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
