# Implementation stage

Read this when the batch reviews an applied OpenSpec change, or work under stage `other` (apply the rules below where they fit the user's stated criteria).

## Entry condition

The implementation is finished when every task of the change is checked (or the user declared this implementation stage complete) and your own verification ran, passed, and is recorded for the brief. A session that leaves tasks open is still in progress.

## Question the review answers

Does the actual implementation satisfy the effective user requirements, the OpenSpec change, and the acceptance conditions agreed for this task?

## Criteria for the brief

Paste this section into the brief's "Stage criteria" block, and apply it yourself when triaging reports.

Compare all three pairs:

- Effective user requirements versus actual implementation behavior.
- OpenSpec change (specs, design, tasks) versus actual implementation.
- Verification evidence (tests, runs, observed results) versus completion claims.

Rules:

- Establish each requirement from observed behavior and outputs; treat a checked task, a document statement, or a zero exit code as a claim to verify.
- Verification covers this task and the dependencies it affects. Problems that belong to other unfinished tasks are reported as such and charged to those tasks.
- When the implementation revealed that the plan conflicted with facts, the related artifacts should have been corrected with the reasons stated. Lowering a requirement, shrinking scope, or weakening acceptance to fit existing code without that correction is a blocking issue.

## Final decision

The final report states whether the implementation meets the agreed acceptance.
