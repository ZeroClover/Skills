# Stage criteria

Paste the relevant section into the brief's "Stage criteria" block, and apply it yourself when triaging reports.

## Proposal review (OpenSpec change)

Question answered: is the change plan complete, sound, and implementable, so that following it would satisfy the user's requirements?

Check:

- Every effective user requirement appears in the specs accurately; nothing is silently dropped, weakened, or reinterpreted.
- The artifacts the project's schema requires (with the default spec-driven schema: `proposal.md`, `specs/**/spec.md`, `design.md`, `tasks.md`) exist and agree with each other.
- Key API capabilities, environment conditions, and technical assumptions the design relies on are backed by evidence (docs, probes, code), or are explicitly marked as unverified.
- The plan is implementable as written, and each task states how it will be verified.
- Necessary edge cases, compatibility concerns, and monorepo or shared-module dependencies are covered.
- The change does not add capabilities beyond the requirements or complexity the requirements do not need.

Not grounds for failing a proposal: implementation code does not exist yet, tasks are unchecked, or tests that can only run after implementation have not run.

## Implementation review (OpenSpec change applied)

Question answered: does the actual implementation satisfy the effective user requirements, the OpenSpec change, and the acceptance conditions agreed for this task?

Compare all three pairs:

- Effective user requirements versus actual behavior of the implementation.
- OpenSpec change (specs, design, tasks) versus actual implementation.
- Verification evidence (tests, runs, observed results) versus the completion claims.

Rules:

- A checked task, a document statement, or a zero exit code is not proof that a requirement is met; look at behavior and outputs.
- Verification covers this task and the dependencies it affects. Problems that belong to other unfinished tasks are reported as such, not charged to this task.
- When the implementation revealed that the plan conflicted with facts, the related artifacts should have been corrected with the reasons stated. Silently lowering a requirement, shrinking scope, or weakening acceptance to fit existing code is a blocking issue.

## Other stage (explicit user request)

Use the completion criteria the user stated for the task. Record them in the brief as the stage criteria, and apply the implementation rules above where they fit.
