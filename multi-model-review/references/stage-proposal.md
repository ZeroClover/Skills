# Proposal stage

Read this when the batch reviews an OpenSpec change proposal.

## Entry condition

The proposal is finished when every artifact the schema requires exists: `openspec status --change <id> --json` shows each artifact `done` or `skipped`. Unchecked tasks and missing implementation code are expected at this stage.

## Question the review answers

Is the change plan complete, sound, and implementable, so that following it would satisfy the user's requirements?

## Criteria for the brief

Paste this section into the brief's "Stage criteria" block, and apply it yourself when triaging reports.

- Every effective user requirement appears in the specs accurately; each is carried over at full strength and with its original meaning.
- The artifacts the project's schema requires (with the default spec-driven schema: `proposal.md`, `specs/**/spec.md`, `design.md`, `tasks.md`) exist and agree with each other.
- Key API capabilities, environment conditions, and technical assumptions the design relies on are backed by evidence (docs, probes, code), or are explicitly marked as unverified.
- The plan is implementable as written, and each task states how it will be verified.
- Necessary edge cases, compatibility concerns, and monorepo or shared-module dependencies are covered.
- The change stays within the capabilities and complexity the requirements call for.
- Judge the plan as a plan: unchecked tasks, absent implementation code, and tests that can only run after implementation are expected.

## Final decision

The final report states whether implementation can start.
