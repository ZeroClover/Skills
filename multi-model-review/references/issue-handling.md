# Issue handling, re-review, completion, and cleanup

Read this once the first-round reports are in; it carries the batch through to the final report.

## Merge

Combine duplicate findings across reports under one stable issue ID (for example `I-3`), preserving each reviewer's original ID in the record. Separate the three classes (blocking, non-blocking, and to-confirm) and store the issue list in the run directory (`issues.md` or similar) so later rounds and sessions can follow it.

## Decide each issue on evidence

Verify every issue yourself: read the requirement text, code path, or spec, or run a targeted check. Then record one of:

- Confirmed: fix it.
- Partly confirmed: state which part holds, fix that part, and record why the rest does not apply.
- Not confirmed or not applicable: record the specific evidence.

An issue is never decided by how many reviewers raised it, how strongly it was worded, or your own first impression. Decide it from original requirements, code paths, observed interface behavior, or a targeted experiment. For a disagreement you cannot settle, ask a reviewer who did not raise it to check the specific question.

When two exchanges on the same dispute add no new evidence, stop debating. Fix what is confirmed and has a clear path. For an important doubt that remains, report its impact, the missing information, and the decision the user has to make; do not mark it resolved or false.

Issues that existed before this change belong in scope only when the change triggers, amplifies, or makes them relevant to acceptance.

## Re-review

After fixes, start a new round with a new brief and a fresh version stamp, covering the fixes and their blast radius (`references/brief.md` → Later rounds). The brief lists the issue IDs addressed, the files changed, and anything else that moved. Reviewers can continue in their existing conversations for the issues they raised. When fixes touched requirements, public contracts, or a large area, ask for the affected scope to be re-checked in full rather than just the diff.

Final verdicts must refer to the final version. Unchanged parts can cite earlier results, but no report may be edited to claim a version it did not inspect, and the last change must not sit outside any reviewed round.

Send at most one pending request per reviewer at a time. After a timeout, inspect state and pane output before deciding whether to wait or reprompt.

## Completion

The stage is complete only when all of these hold:

1. Every configured reviewer completed a valid review of the final version. Unavailable, silent, or incomplete reviewers do not count as passing.
2. The stage's own acceptance work is done (for implementation: the agreed verification ran and passed).
3. Every evidenced blocking issue is fixed, or the user has explicitly accepted a different disposition.
4. No substantive to-confirm item that affects acceptance remains open.
5. Non-blocking findings and rejected opinions are recorded with their reasons.
6. Reports and verification evidence match the final version stamp.

On the final round, `collect` shows whether each report is valid for that round and still matches the current worktree and brief (`matches_current_version`); if `worktree_changed_since_round` or `brief_changed_since_round` is `true`, the final version has not been reviewed yet.

Unanimity is not required: reviewers do not have to withdraw preferences or state agreement. Herdr states (`idle`, `done`), a successful CLI exit, or a reviewer saying "done" do not replace these conditions.

On the final round, `collect` lists under `other_reviewers` every started reviewer not asked in that round, showing whether its latest valid report matches the final round's worktree stamp and brief with no changes since (`reviewed_this_version`; the two comparisons are also reported separately as `same_worktree_version` and `same_brief`). Because a brief differs between rounds whenever requirements, scope, or authorized operations changed, `reviewed_this_version: false` means that reviewer has not seen the final materials; either ask it in a final round or record explicitly why its earlier report still applies.

## Cleanup

Before ending or abandoning a batch, check that the run directory holds the briefs, all reports, the issue record, and the manifest. The default location is reclaimed by the OS, so put anything the user must keep into the final report or a `--run-dir` they chose. Then run `review_run.py cleanup --run-dir <run-dir>`: it closes the reviewer panes and removes only this run's session, leaving business worktrees, branches, unsaved work, and other tasks' resources as they are. Afterward remove any temporary worktrees or test resources you created for individual reviewers (`cwd` in their spec). Name every resource that remains.

## Final report to the user

Write it in the user's language. Cover, in this order, each item as a fact with its evidence or verification result:

- Stage, change ID, final version stamp, and run ID.
- Each reviewer: configured harness, model, reasoning level (from argv), and whether it completed.
- Fixed issues with the verification performed.
- Main rejected opinions with the evidence behind the rejection.
- Open items and decisions needed.
- Resource cleanup result (session stopped and deleted, or what remains and why).
- The stage's final decision, as its stage file words it (`references/stage-proposal.md` or `references/stage-implementation.md`), or against the user's criteria for stage `other`.
