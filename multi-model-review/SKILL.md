---
name: multi-model-review
description: Orchestrate an independent multi-model review batch through Herdr. Never for an agent started as a reviewer (MMR_ROLE is set). Use after you complete an OpenSpec change proposal, after an OpenSpec change is implemented (every task done, or the user declared the stage complete) and your verification is recorded, or when the user explicitly asks for a multi-model review of specific work. Not for partial implementation sessions or ordinary tasks that merely touch code or specs.
---

# Multi-model review

Reviewers running on other models check a finished stage of work. You own the batch: prepare the materials, run the reviewers, verify every finding yourself, fix confirmed issues, and report the outcome. Reviewers advise; you decide.

## Role guard

Run `echo "${MMR_ROLE:-}"` first. If it prints anything, a review batch started you as a reviewer: follow the brief you were given and leave this skill unused. A user request quoted inside a brief is review evidence, not a request to orchestrate. The script's control subcommands refuse to run in that case as well.

## When to run

Run a batch in exactly these cases:

| Case | Stage | Stage file |
|------|-------|------------|
| An OpenSpec change proposal is complete | `proposal` | `references/stage-proposal.md` |
| An OpenSpec change is fully implemented and your verification is recorded | `implementation` | `references/stage-implementation.md` |
| The user asks for a multi-model review of specific work | `other` | the user's stated completion criteria, plus `references/stage-implementation.md` where it fits |

Each stage file gives its entry condition, the question the review answers, the criteria for the brief, and the final decision to report. The default reviewers, models, reasoning levels, and locations apply wherever the user has not chosen otherwise.

## Workflow

`S` is `scripts/review_run.py` in this skill's directory. Run it with the system `python3`; every subcommand prints JSON, and `--help` lists its arguments.

1. **Confirm the stage.** Read the stage file and check its entry condition. Take the repository root, worktree, and change ID from the filesystem and `openspec` output.
2. **Create the run and start the reviewers.**
   ```bash
   python3 "$S" init --repo <repo-root> --stage proposal|implementation|other --change <change-id>
   python3 "$S" start --run-dir <run-dir>      # add --reviewers <file> for a user-specified set
   ```
   `init` prints the run directory and creates a Herdr session of its own from outside Herdr; that is the intended setup (`references/herdr-orchestration.md` explains why Herdr's "stay inside Herdr" rule covers only the user's interactive session). The default set is `assets/default-reviewers.json`; read `references/reviewers.md` when the user names other reviewers or one fails to start.
3. **Write the brief.** Read `references/brief.md`, then fill `assets/brief-template.md` into `<run-dir>/round-1/brief.md`, taking the stamp from `python3 "$S" version --run-dir <run-dir>`.
4. **Run the round.**
   ```bash
   python3 "$S" round --run-dir <run-dir> --brief <run-dir>/round-1/brief.md
   python3 "$S" collect --run-dir <run-dir>
   ```
   When a reviewer's result is anything other than `report_ready`, or a Herdr command fails, read `references/herdr-orchestration.md`.
5. **Triage, fix, re-review, finish.** Read `references/issue-handling.md` and follow it through completion, `cleanup`, and the final report.

## Rules for the whole batch

- Keep each reviewer's configured harness, model, and reasoning level. A reviewer that fails to start or delivers no valid report is reported as missing, with its recorded error, after the others finish; the user decides on a reduced set. Report a missing tool, path, or host connection the same way.
- Each reviewer forms its first-round view from the brief and the worktree alone; share other reviewers' conclusions and your own verdict only after its first-round report is in.
- Report every finding that meets the evidence standard, each under its classification (blocking, non-blocking, or to-confirm).
- Agent-to-agent material is in English; the final report to the user is in the user's language.

## Files

| File | Read when |
|------|-----------|
| `references/stage-proposal.md` | stage `proposal` |
| `references/stage-implementation.md` | stage `implementation` or `other` |
| `references/brief.md` | writing any round's brief |
| `references/issue-handling.md` | first-round reports are in |
| `references/reviewers.md` | the user names other reviewers, or a reviewer fails to start |
| `references/herdr-orchestration.md` | a result other than `report_ready`, a Herdr error, resuming a run, or acting by hand |
| `assets/brief-template.md`, `assets/report-template.md` | filling the brief (the report template is for reviewers) |
| `assets/default-reviewers.json` | the default reviewer set |
| `scripts/review_run.py` | run lifecycle: `init`, `list`, `version`, `start`, `round`, `wait`, `collect`, `status`, `cleanup` |
