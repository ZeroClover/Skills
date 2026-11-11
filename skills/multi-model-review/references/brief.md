# Writing the round brief

Read this before writing each round's brief. Every reviewer in a round receives the same brief.

## What identifies a reviewed version

One run ID covers the whole batch: first round, discussion, fixes, and re-review. Every round records two values that together identify what was reviewed: the worktree version stamp (HEAD plus a hash of every uncommitted change and untracked file, so dirty content always has its own stamp) and the SHA-256 of that round's brief, which carries the requirement materials. `review_run.py version --run-dir <run-dir>` prints the stamp; `round` records both and refuses a brief whose "Version under review" line differs from the stamp; `collect` reports whether either changed afterward.

## Filling the template

Copy `assets/brief-template.md` to `<run-dir>/round-N/brief.md` and fill it from existing documents (OpenSpec artifacts, the conversation, recorded verification), so the brief points at one source of truth. The brief carries:

- The user's original requests, verbatim and in order, inside the tagged block. The reviewers' first job is to check your effective-requirements list against this original text, so it stays complete alongside your summary.
- The effective-requirements table: source, status (effective, superseded, or inferred), and the spec or acceptance method for each. A later request replaces an earlier one only where the two conflict or where it says so; compatible earlier requirements stay in force. Mark anything you could not settle from the original text as inferred.
- The change under review, its dependencies, non-goals, and related concurrent work.
- Field evidence: environment facts, observed interface behavior, timestamps, redacted results, and still-unverified assumptions. Redact credential values and describe what they grant. When a reviewer must re-probe, provide access through the existing controlled channel; secrets stay out of OpenSpec files, reports, and prompts.
- Your self-verification: commands, actual results, and what remains unverified.
- The operations reviewers may run this round and where they may write.
- The stage criteria: the "Criteria for the brief" section of `references/stage-proposal.md` or `references/stage-implementation.md`, or the user's stated criteria for stage `other`.
- The reviewer-to-focus table from the reviewer specs; each reviewer applies its own row on top of the full review.

Keep the template's header lines and its fixed passages ("Your role", "Issue standard", "Done when") as written, so every reviewer in every run reads the same instructions. The script parses report headers, hashes the brief, and checks its "Version under review" line; it reads nothing else from the brief.

## Language

Write all agent-to-agent material in English: the brief, prompts, reports, and issue record. Quote the user's original requests verbatim in their original language.

## Reviewer access

Reviewers read the worktree and run only the operations the brief authorizes; implementation, spec, and planning files stay unchanged by them. Read-only reviewers can share one worktree at a fixed version. A reviewer whose verification writes files or competes for a resource gets its own temporary worktree or test resource, set through the `cwd` field of its spec (`references/reviewers.md`).

## Later rounds

A later round's brief lists the issue IDs addressed, the files changed, and anything else that moved (`references/issue-handling.md` → Re-review). When deriving it from an earlier brief, re-check every run-scoped value against the current manifest: run ID, run directory, round, version header (HEAD, dirty state), report and scratch paths, and authorized operations. Each value must name the current run and round, so reviewer output lands in this run's directory.
