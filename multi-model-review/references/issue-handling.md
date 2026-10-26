# Issue handling, re-review, and completion

Read this once the first-round reports are in.

## Merge

Combine duplicate findings across reports under one stable issue ID (for example `I-3`), keeping each reviewer's original ID in the record. Keep the three classes apart: blocking, non-blocking, to-confirm. Keep the issue list in the run directory (`issues.md` or similar) so later rounds and later sessions can follow it.

## Decide each issue on evidence

For every issue, verify it yourself: read the requirement text, the code path, the spec, or run the targeted check. Then record one of:

- Confirmed: fix it.
- Partly confirmed: state which part holds, fix that part, record why the rest does not apply.
- Not confirmed or not applicable: record the specific evidence.

What does not decide an issue: how many reviewers raised it, how strongly it was worded, or your own first impression. What does: original requirements, code paths, observed interface behavior, or a targeted experiment. For a disagreement you cannot settle, ask a reviewer who did not raise it to check the specific question.

When two exchanges on the same dispute add no new evidence, stop debating. Fix what is confirmed and has a clear path. For an important doubt that remains, report its impact, the missing information, and the decision the user has to make; do not mark it resolved or false.

Issues that already existed before this change belong in scope only when the change triggers, amplifies, or makes them relevant to acceptance.

## Re-review

After fixes, start a new round with a new brief and a fresh version stamp. The brief lists the issue IDs addressed, the files changed, and anything else that moved. Reviewers can continue in their existing conversations for the issues they raised. When fixes touched requirements, public contracts, or a large area, ask for the affected scope to be re-checked in full rather than just the diff.

The final verdicts must refer to the final version. Unchanged parts can cite earlier results, but no report may be edited to claim a version it did not inspect, and the last change must not sit outside any reviewed round.

One pending request per reviewer at a time. After a timeout, read state and output before deciding whether to wait or re-prompt.

## Completion

The stage is complete only when all of these hold:

1. Every configured reviewer completed a valid review of the final version. Unavailable, silent, or incomplete reviewers do not count as passing.
2. The stage's own acceptance work is done (for implementation: the agreed verification ran and passed).
3. Every evidenced blocking issue is fixed, or the user has explicitly accepted a different disposition.
4. No substantive to-confirm item that affects acceptance remains open.
5. Non-blocking findings and rejected opinions are recorded with their reasons.
6. Reports and verification evidence match the final version stamp.

Unanimity is not required: reviewers do not have to withdraw preferences or state agreement. Herdr states (`idle`, `done`), a successful CLI exit, or a reviewer saying "done" do not replace these conditions.

`collect` on the final round lists, under `other_reviewers`, every started reviewer that was not asked in that round, with whether its latest valid report matches the final round's worktree stamp and brief and nothing has changed since (`reviewed_this_version`; the two comparisons are also reported separately as `same_worktree_version` and `same_brief`). A brief differs between rounds whenever requirements, scope, or authorized operations changed, so `reviewed_this_version: false` means that reviewer has not seen the final materials; either ask it in a final round or record explicitly why its earlier report still applies.

## Final report to the user

Cover, in this order:

- Stage, change ID, final version stamp, and run ID.
- Each reviewer: configured harness, model, reasoning level (from argv), and whether it completed.
- Fixed issues with the verification performed.
- Main rejected opinions with the evidence behind the rejection.
- Open items and decisions needed.
- Resource cleanup result (session stopped and deleted, or what remains and why).
- For a proposal: whether implementation can start. For an implementation: whether the agreed acceptance is met.
