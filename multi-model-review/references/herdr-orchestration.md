# Herdr orchestration for a review batch

Read this when a script reports a Herdr error, when you need to inspect a reviewer directly, or when you run Herdr commands yourself. `scripts/review_run.py` already performs the routine steps described here.

## Why operating Herdr from outside a pane is correct here

Herdr's own skill tells an agent to stop unless `HERDR_ENV=1`, and not to "inspect or control the focused Herdr session from outside Herdr". That rule protects the user's interactive default session, whose panes belong to the user and to other tasks. This workflow never touches that session:

- It creates a brand-new named session whose name is the run ID (`herdr --session <run-id> server`), so nothing in it existed before this batch.
- Every command targets that session explicitly with `--session <run-id>`, which the CLI documents as "use or create a named persistent session".
- The user's instruction to run this review is the authorization to create and later delete that session.

Reusing or deleting any other session, including one that looks related, stays off limits. If a session named like a previous run is idle, leave it alone unless you are resuming that exact run and its manifest says so.

Herdr's skill states its rule more broadly than the interactive-session case it protects. The isolated-session authorization above resolves that case; higher-priority instructions and your execution permissions still apply as usual. If a different, concrete conflict remains, report it instead of guessing.

## Headless mechanics (what the script does)

```bash
herdr session list --json                           # name must be unused
herdr --session "$RUN" server > "$RUN_DIR/herdr-server.log" 2>&1 &   # background, detached
herdr --session "$RUN" workspace list                # poll until it answers
herdr --session "$RUN" workspace create --cwd "$WORKTREE" --label "$RUN" --no-focus \
      --env MMR_ROLE=reviewer --env MMR_RUN_ID="$RUN"
herdr --session "$RUN" tab create --workspace w1 --cwd "$WORKTREE" --label astra --no-focus \
      --env MMR_ROLE=reviewer --env MMR_RUN_ID="$RUN"   # one tab per reviewer
herdr --session "$RUN" agent start astra --kind pi --pane w1:p2 --timeout 90000 -- --model <provider/model> --thinking high
```

Facts verified on herdr 0.9.5:

- `herdr --session <name>` without `server` opens the TUI and occupies the terminal; a batch always uses the `server` subcommand in the background.
- `--env` values reach the shell of every pane created with them, so reviewers see `MMR_ROLE=reviewer` and `MMR_RUN_ID`.
- Arguments after `--` on `agent start` go to the binary that `--kind` names; repeating the binary name makes the harness treat it as a prompt or reject it.
- `agent start` returns the `argv` it launched. That array is the configuration evidence for the reviewer; a model's self-description is not.
- One tab per reviewer keeps panes wide enough to read; four splits in one tab truncate status lines.
- `herdr session stop <name>` terminates every pane process in that session (verified by PID). `herdr session delete <name>` refuses while the session runs.

## Startup dialogs

A harness started in a directory it has not seen before shows a trust dialog. Seen on this machine: Antigravity "Do you trust the contents of this project?" (cursor on Yes), Codex "Trust this folder?" (cursor on "Trust and continue"), Claude Code "Yes, I trust this folder" (cursor on "No, exit" by default, so a bare Enter makes it quit). Herdr reports `agent_not_ready` with state `blocked`. The reviewed worktree is exactly what the reviewer is meant to read, so the script answers that dialog, and only that dialog (matched on its wording): it reads the screen, finds the cursor inside the option block next to the affirmative line, moves it there, confirms, waits for the harness to settle, and records `trust_prompt_answered: true` with the keys it sent and the state it settled in. If it cannot locate the options it presses nothing. Codex shows a splash screen after trusting that Herdr may report as `unknown`; the script accepts that state once the dialog is gone, and the first prompt of the round is the real readiness test. Any other startup dialog is left for you to inspect; the manifest keeps the screen text under `screen_at_failure`.

Reviewer panes inherit `HERDR_ENV=1`, so a reviewer could technically issue herdr commands against this session. The brief forbids it; the script does not enforce it. Keep that in mind when reading a report that claims to have changed session state.

## Reading reviewer state

```bash
herdr --session "$RUN" agent list
herdr --session "$RUN" agent get <name>
herdr --session "$RUN" agent read <name> --source recent-unwrapped --lines 120
herdr --session "$RUN" pane process-info --pane <pane-id>
```

Lifecycle states: `working`, `idle`, `done`, `blocked`, `unknown`.

- `idle` or `done` means the agent is ready for input, not that the task is finished. Antigravity can be idle while background work continues. Completion of a round is the report file at the agreed path with valid header fields; the script checks exactly that.
- `blocked` means Herdr recognized an approval or question dialog. Read the pane, decide what the dialog is, and answer through `agent send-keys` only when the answer is clearly within the authorized operations of the brief. If it asks for something outside them, record it and treat that reviewer's round as incomplete.
- `unknown` means Herdr sees a process but cannot classify it. Read the pane before acting.

## Prompt and wait semantics

`agent prompt <name> <text> --wait --timeout <ms>` submits the text and waits for the first settled state. Error codes:

- `agent_blocked`: nothing was sent; a dialog is open. Inspect first.
- `agent_prompt_stalled`: the text was written but no activity followed within five seconds. Read the pane; the prompt may be sitting unsent in the input box. Resend only after confirming it did not start (see below).
- `timeout`: the caller timeout expired while the agent was still working. The prompt was delivered. Continue with `review_run.py wait`; do not resubmit.
- `cli_timeout` (script-level): the herdr CLI itself did not return. Check `herdr status` and `agent get` before anything else.

`wait` without `--reprompt` returns at once for an agent that is already idle, which is what you want after a timeout (the report may already exist) and what tells you, after `stalled` or `blocked`, that nothing is running. Inspect the pane; if the task never started, `wait --round N --reviewers <name> --reprompt` sends the same prompt again (the text is generated deterministically from the manifest). The script refuses to prompt an agent that is still `working` (`busy_not_sent`): one request per reviewer at a time.

Keep the prompt text short and point at the brief file; long briefs belong on disk, not in terminal input. Every prompt attempt is appended to the manifest under `rounds[].prompts[<name>]` at the moment it is made (text, `attempted_at`, `delivery: unknown`) and resolved when Herdr answers: `written` (Herdr reported the submission, or a later `timeout` or `stalled`, both of which happen after the text was written), `not_sent` (Herdr refused because the agent was blocked), or `unknown` (the CLI itself failed or timed out, so delivery cannot be confirmed). Earlier attempts keep their record when a reprompt is added. If the orchestrating process dies while a wait is in progress, the attempt stays `unknown`: Herdr never reported back, so the pane is the only evidence; read it before deciding whether to resend. `wait --reprompt` skips a reviewer whose valid report already exists, unless `--message` is given, because a correction is meant for a reviewer that already wrote something.

## Two more continuations

- `report_invalid`: the reviewer wrote a report whose header does not match (wrong version string, wrong round, a verdict that is not one token). Do not reprompt the whole review; send a short correction in its existing conversation with `wait --round N --reviewers <name> --reprompt --message "Your report header ... please fix line X"`, which records the message as a prompt attempt like any other and waits for the result. `--message` requires `--reviewers`, so a correction never reaches reviewers it was not written for.
- A reviewer's harness exited after it had started (its pane shows a shell prompt). `start` asks Herdr; only the answer `agent_not_found` counts as gone, in which case it records the reviewer as `gone`, closes the pane, and starts it again in a fresh tab (its conversation history is lost, so the next round's brief should say so). Any other failure of that query (`cli_timeout`, a server error) proves nothing about the reviewer: `start` reports `liveness_unknown` and leaves the pane alone for you to inspect.

`status` is read-only and safe to run while a round is waiting; a workspace-label warning it finds is printed, and the next control command persists it.

## Timeouts

A real review of a non-trivial change takes tens of minutes. The script defaults to 45 minutes per round and 30 minutes for `wait`. When a reviewer times out, check `agent get` and read the pane before deciding anything; a working agent is not a failed one.

## Resuming an interrupted batch

The manifest is written before the session server starts and after every resource is created, so it always names what exists: session name and directory, workspace, each reviewer's tab and pane, rounds, prompts, and results.

1. `review_run.py status --run-dir <dir>` shows whether the session still runs and which reviewers are live.
2. If the session runs, every control command re-checks ownership (name, session directory, workspace) before acting. Continue with `wait` (add `--reprompt` for a reviewer that settled without a report and, on inspection, never started the task), `round`, or `collect`. `start` retries reviewers whose start failed, closing their old pane first so the agent name is free again; it refuses to change a started reviewer's configuration or drop a started reviewer.
3. If the session is gone, the reviewer conversations are gone with it. Start a new run; cite earlier reports as prior evidence only for parts whose version stamp and brief hash have not changed.
4. If `init` died before the session answered (`state: starting` or `start_failed` with no `session_dir`), `cleanup` refuses because it cannot verify ownership. Check `herdr session list --json` for the run ID and, if it is there, stop and delete it by name yourself. If `init` died after the session answered but before the workspace existed, `cleanup` works normally.

## Cleanup

`review_run.py cleanup --run-dir <dir>` acts only when the manifest's session name equals the run ID, the live `session_dir` matches, and the live session still contains this run's workspace (identified by its ID; a renamed label is recorded as a warning, not a refusal). It then closes each reviewer pane it opened, stops the session (which ends any remaining pane process), and deletes it. It never touches other sessions, worktrees, or branches. The run directory with manifest, briefs, and reports stays on disk until the OS reclaims the temp location, or indefinitely under a user-chosen `--run-dir`.

Each cleanup step is appended to the manifest as it happens, so a failure midway leaves a record of what was done and what remains. Report the remaining resource by name instead of retrying blindly. Harness session files (pi, Antigravity, Codex, Claude Code) are written by the harnesses themselves during the conversation and survive the pane closing; the script sends no harness-specific exit command.
