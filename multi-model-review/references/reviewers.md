# Reviewer configuration

Read this when choosing the reviewer set, when a reviewer fails to start, or when the user asks for a different harness or model mix.

## Default set

`assets/default-reviewers.json` holds the default four. They apply only when the user has not named harnesses or models for this review; an explicit user choice replaces the set, including reasoning levels. A run keeps the set it started with: `start` without `--reviewers` on an existing run reuses that set rather than the defaults.

| Name | Harness | Model | Reasoning | Extra |
|------|---------|-------|-----------|-------|
| astra | pi | zero-aicoding-codex/gpt-6-astra | high | |
| argon | agy (Antigravity CLI) | gemini-4-argon-high | high | `--dangerously-skip-permissions` |
| fable | pi | zero-aicoding-claude/claude-fable-5-1 | high | |
| deepseek | pi | ollama-cloud/deepseek-v4.1-flash:1017 | max | |

The Antigravity flag only reduces approval dialogs inside that reviewer. It does not widen what the reviewer may do, which the brief defines, and it does not change any permission set on the outer task.

## Spec format

Pass `--reviewers <file>` to `review_run.py start` with a JSON list:

```json
[
  {"name": "astra", "harness": "pi", "model": "zero-aicoding-codex/gpt-6-astra", "reasoning": "high",
   "focus": "requirement omissions and acceptance evidence"},
  {"name": "argon", "harness": "agy", "model": "gemini-4-argon-high", "reasoning": "high",
   "extra_args": ["--dangerously-skip-permissions"]},
  {"name": "custom", "harness": "opencode", "model": "provider/model", "reasoning": "high",
   "args": ["--model", "provider/model", "--variant", "high"]}
]
```

- `name`: unique within the run, matching `[a-z][a-z0-9_-]{0,31}` (Herdr's agent-name rule).
- `harness`: a Herdr agent kind (`herdr agent start --help` lists the possible values of `--kind`). Templates exist for `pi`, `agy`, `codex`, and `claude`; any other kind needs explicit `args`.
- `model`, `reasoning`: always required, even when `args` is set explicitly, because the manifest and report header record them.
- `cwd`: optional working directory for this reviewer's tab, used when its verification writes files (default: the run's worktree). Any temporary worktree you create for this is a batch resource: remove it after `cleanup`, or name it as remaining. A temporary worktree must contain the same content as the reviewed version: with uncommitted changes, `git worktree add` alone gives a clean checkout, so apply the diff and copy untracked files, or commit first. `start` records `cwd_version` and `cwd_matches_worktree_version` for such a reviewer (with the same exclusions mapped into the temporary worktree); `false` means its report describes different content than the round's stamp.
- `focus`: optional extra emphasis for the shared brief's reviewer-to-focus table. It adds to the full review and never narrows it.

Argument templates the script uses (all four verified on this machine through `herdr agent start`):

| Harness | Arguments after `--` |
|---------|----------------------|
| pi | `--model <provider/model> --thinking <off,minimal,low,medium,high,xhigh,max>` |
| agy | `--model <id from agy models> --effort <low,medium,high,xhigh,max>` |
| codex | `-m <model> -c model_reasoning_effort="<level>"` |
| claude | `--model <model> --effort <level>` |

## Verifying configuration

Evidence of what a reviewer runs, strongest first:

1. `argv` returned by `agent start`, recorded in `manifest.json` under `reviewers[].argv` (`argv_source` indicates whether it came from Herdr's response or, after a trust dialog, from the requested arguments; `agent get` does not return `argv`, so after a dialog the requested arguments plus the status line are the strongest evidence available).
2. The harness status line in the pane, for example `gpt-6-astra • high` in pi, `Gemini 4 Argon · high` in Antigravity, or `GPT-6-Astra high` in Codex; `start` stores the pane's last lines under `screen_after_start`.
3. The process command line (`process_cmdline`), only where the harness keeps it: Antigravity does; pi rewrites it to a bare `pi`.
4. Never the model's own statement about what it is.

`start` also records `preflight`: `listed` when `pi --offline --list-models` (pi's cached catalog, which includes online providers once fetched) or `agy models` shows the exact model; `not_listed` when it does not; `not_checked` for other harnesses; or `check_failed: <reason>` when the catalog command itself failed. `not_listed` usually means the provider catalog was never cached or failed to load, and the agent may still fail at its first prompt. The first round's result is the real availability check.

## When a reviewer is unavailable

A reviewer that fails to start, never produces a report, or reports on the wrong version does not count as a completed review. Keep the configured identity: do not swap in another model or lower the reasoning level on your own. Run the remaining reviewers, finish their rounds, then report the missing reviewer with the recorded error (`manifest.json` → `reviewers[].error`, `screen_at_failure`, or `failed_starts`). The user decides whether to accept a reduced set or to retry. Running `start` again (without `--reviewers`, so the run's own set is used) retries any reviewer whose previous attempt failed: it closes the failed pane to free the agent name and starts again in a fresh tab. To change the harness, model, or reasoning of a reviewer that already started, give it a new name (and a new focus row) or start a new run; `start` refuses to alter or drop a started reviewer, so the manifest never disagrees with what is running.
