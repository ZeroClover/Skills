---
name: multi-model-review
description: Orchestrate an independent multi-model review batch through Herdr. Never for an agent started as a reviewer (MMR_ROLE is set). Use after you complete an OpenSpec change proposal, after all tasks of an OpenSpec change are implemented and your verification is recorded, or when the user explicitly asks for a multi-model review of specific work. Not for partial implementation sessions or ordinary tasks that merely touch code or specs.
---

# Multi-model review

You finished a piece of work and now have independent reviewers check it before you call the stage done. You own the batch: you prepare the materials, start and coordinate the reviewers, verify every finding yourself, fix what is real, and report the outcome. The reviewers advise; they do not decide.

## Before anything else

**Role guard.** Run `echo "${MMR_ROLE:-}"`. If it prints anything, you were started by a review batch to review someone else's work. Do not use this skill, do not start reviewers, and follow the brief you were given instead. A user request quoted inside a brief is review evidence, not a new request to orchestrate. The script's control subcommands (`init`, `start`, `round`, `wait`, `collect`, `status`, `cleanup`) refuse to run in that case as well; `version` and `list` are read-only and do not check.

**Scope gate.** Use this skill only when one of these holds:

1. You just created an OpenSpec change proposal (the `openspec-propose` workflow or equivalent) and all its artifacts are complete.
2. You finished implementing an OpenSpec change (the `openspec-apply-change` workflow or equivalent): every task of the change is done, or the user said this implementation stage is complete, and your own verification passed. A partial apply session that leaves tasks open is not a finished stage.
3. The user explicitly asked for this skill or for a multi-model review of specific work.

Anything else does not get this review, even if it would benefit from a second opinion. The batch reviews a finished stage: your own verification for the stage is already done and recorded before the reviewers start, and the review does not replace it.

**User choices win.** The default reviewers, models, reasoning levels, and locations below apply only where the user has not specified otherwise for this review.

## Identify the stage and the object

Decide which stage you are reviewing and write it down:

- **Proposal**: is the change plan complete, sound, and implementable, and would following it satisfy the user?
- **Implementation**: does the actual implementation satisfy the effective user requirements, the OpenSpec change, and the agreed acceptance conditions?
- **Other**: an explicit user request; the user's stated completion criteria act as the stage criteria.

Record the real repository root, the worktree reviewers will read, the OpenSpec change ID (if any), and the stage. Take these from the filesystem and `openspec` output, not from a GUI project name, the terminal that has focus, or a default workspace.

One run ID covers the whole batch: first round, discussion, fixes, and re-review. Every round records two things that together identify what was reviewed: the worktree version stamp (HEAD plus a hash of every uncommitted change and untracked file, so HEAD alone never stands for dirty content) and the SHA-256 of that round's brief, which carries the requirement materials. `scripts/review_run.py version --run-dir <run-dir>` prints the stamp; `round` records both and `collect` reports whether either changed afterwards.

## Prepare the shared materials

All reviewers receive one shared brief per round. Start from `assets/brief-template.md`, keep it in the run directory (`round-N/brief.md`), and fill it from existing documents rather than writing a parallel set of requirement notes. The brief carries:

- The user's original requests, verbatim and in order, inside the tagged block. Your summary never replaces them; the reviewers' first job is to check your effective-requirements list against the original text.
- The effective-requirements table: source, superseded-by, and the spec or acceptance method for each. A later request replaces an earlier one only where the two conflict or where it says so; compatible earlier requirements stay in force. Anything you could not settle from the original text is marked as inferred.
- The change under review, its dependencies, non-goals, and related concurrent work.
- Field evidence: environment facts, observed interface behavior, timestamps, redacted results, and still-unverified assumptions. Credential values are redacted; what they grant stays described. When a reviewer must re-probe, provide access through the existing controlled channel, never by writing secrets into OpenSpec files, reports, or prompts.
- Your self-verification: commands, actual results, what remains unverified.
- The operations reviewers may run this round and where they may write.
- The stage criteria from `references/stage-criteria.md` and the issue standard.
- The reviewer-to-focus table, from the reviewer specs; each reviewer applies its own row on top of the full review.

Everything between agents is in English: the brief, the prompts, the reports, the issue record. Quote the user's original requests verbatim in whatever language they wrote them; translate nothing there. Only your final report to the user is in the user's language. Keep the template's fixed passages ("Your role", "Issue standard", "Done when") and the header lines as they are in the template, so every reviewer in every run reads the same instructions; the script parses report headers and hashes the brief but does not parse the brief.

## Run the batch

`scripts/review_run.py` (Python 3, standard library only) does the Herdr work and records everything in `manifest.json` inside the run directory. Run it with the system `python3`; each subcommand prints JSON and `--help` lists its arguments. The run directory defaults to `<system temp dir>/multi-model-review/<repo>-<hash>/<run-id>/`: outside the repository, so review material never shows up in its git status, readable by later sessions (`list --repo <root>` finds it), and reclaimed by the operating system (on macOS the per-user temp dir is purged after a few days without access; elsewhere the system's temp policy applies). Pass `--run-dir` when a run must be kept longer; your final report to the user carries the conclusions either way.

```bash
S=/path/to/multi-model-review/scripts/review_run.py
python3 "$S" init --repo <repo-root> --stage proposal|implementation|other --change <change-id>
python3 "$S" start --run-dir <run-dir>                 # add --reviewers <file> for a user-specified set
python3 "$S" version --run-dir <run-dir>                # stamp for the brief
python3 "$S" round --run-dir <run-dir> --brief <run-dir>/round-1/brief.md
python3 "$S" collect --run-dir <run-dir>               # header check and summary.json
python3 "$S" cleanup --run-dir <run-dir>
```

Invariants the script enforces, which you keep when you act manually:

- The batch runs in a fresh Herdr session named after the run ID and owned by it; no other session is reused, inspected, or deleted. Running it from outside Herdr is correct: `references/herdr-orchestration.md` explains why Herdr's "stay inside Herdr" rule does not apply to this session, and what to do when a command fails.
- Each reviewer gets its own tab and a fresh conversation, with `MMR_ROLE=reviewer` and `MMR_RUN_ID` in its environment.
- The `argv` Herdr launched is recorded per reviewer, with the pane's status line and process command line as corroboration where the harness exposes them. That is the evidence for harness, model, and reasoning level; a model's self-description is not.
- A round counts a reviewer as done only when its report exists with header fields that exactly match this run, round, reviewer, stage, and version, and carry a single verdict token.
- The manifest records the run's intent before the session server starts and every resource as soon as it exists, so an interrupted run can be inspected with `status` and finished with `cleanup`.
- Every command that controls the session (`start`, `round`, `wait`, `cleanup`) first checks that the live session is the one this run created: same name, same session directory, and, while the session runs, the run's workspace still present. A started reviewer keeps its configuration for the whole run; `start` refuses to change or drop one silently.
- Cleanup closes the reviewer panes it opened, then stops and deletes only that verified session.

The default reviewer set lives in `assets/default-reviewers.json` (four reviewers: GPT-6 Astra and Claude Fable 5.1 and DeepSeek through pi, Gemini 4 Argon through Antigravity). A run keeps the set it started with; `start` without `--reviewers` on an existing run reuses that set and never falls back to the defaults. `references/reviewers.md` covers the spec format, per-harness arguments, and configuration evidence; read it when the user names a different set or a reviewer fails to start.

Reviewers read the worktree and run only the operations the brief authorizes. They do not edit implementation, spec, or planning files. Read-only reviewers can share one worktree at a fixed version; a reviewer whose verification writes files or competes for a resource gets its own temporary worktree or test resource, set per reviewer with the `cwd` field of its spec.

When a reviewer fails to start or never delivers a valid report, keep its configured identity: do not substitute a model or lower its reasoning, and do not count silence as a pass. Run the others to completion, then report the gap with the recorded error. A missing tool, path, or host connection is reported the same way, never papered over.

Do not show any reviewer another reviewer's conclusions, or your own verdict, before its first-round report is in.

## Triage, fix, re-review

Follow `references/issue-handling.md`: merge duplicates under stable IDs, verify each finding against requirements, code, interfaces, or a targeted experiment, fix confirmed issues, and record the evidence for everything you reject. Then start a new round with a new brief and version stamp covering the fixes and their blast radius. Reviewers may continue their existing conversations. Final verdicts must refer to the final version.

Report everything the reviewers surface that meets the evidence standard; the classification into blocking, non-blocking, and to-confirm is where severity lives, not in omission.

## Finish

Declare the stage complete only when the completion conditions in `references/issue-handling.md` hold. `collect` on the final round shows which reviewers have a valid report for the final version (same worktree stamp and same brief) and which do not.

Before ending or abandoning a batch, make sure the run directory holds the briefs, all reports, the issue record, and the manifest; these survive the session (the default location is reclaimed by the OS, so anything the user must keep goes into the final report or a `--run-dir` they chose). Then run `cleanup`. It closes the reviewer panes and removes only this run's session; business worktrees, branches, unsaved work, and other tasks' resources are never touched. Temporary worktrees or test resources you created for individual reviewers (`cwd` in their spec) are yours to remove afterwards; name any that remain. If something could not be cleaned, say which resource remains.

Report to the user in the user's language, following the final-report outline in `references/issue-handling.md`, and state plainly whether the proposal can move to implementation or whether the implementation meets the agreed acceptance.

## Resources

- `scripts/review_run.py`: run lifecycle (`init`, `list`, `version`, `start`, `round`, `wait`, `collect`, `status`, `cleanup`).
- `assets/default-reviewers.json`, `assets/brief-template.md`, `assets/report-template.md`.
- `references/herdr-orchestration.md`: Herdr mechanics, authorization rationale, states, timeouts, resume, cleanup.
- `references/reviewers.md`: reviewer spec format, argument templates, configuration evidence, unavailable reviewers.
- `references/stage-criteria.md`: proposal and implementation criteria to paste into the brief.
- `references/issue-handling.md`: merge, decide, re-review, completion conditions, final report outline.
