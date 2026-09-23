---
name: create-commit
description: "Interactively draft and execute Git commits with user confirmation. Selects files from explicit input, staged changes, or workspace diffs; follows Conventional Commits in English."
allowed-tools: Bash(git *)
---

# Create Commit

## Goal

- Create commits in any Git repository, auto-selecting files when the user does not.
- Follow the repository's `COMMIT_GUIDELINES.md` when it exists.
- Otherwise, default to **Conventional Commits**, **English**, and a **single-line subject**.

## File selection rules

Stop at the first matching rule:

1. User explicitly named files → commit only those files.
2. User did not name files, but the staging area has changes → commit only what is staged.
3. User did not name files and staging is empty → stage and commit all workspace changes (`git add -A`).

## Commit message rules

1. Read `COMMIT_GUIDELINES.md` at the repository root.
2. If it exists, follow it strictly. For any aspect it does **not** constrain, fall back to the defaults below.
3. If it does not exist, apply the defaults below. Read recent subjects (`git log -n 20 --pretty=format:'%s'`) only to learn which scopes the repository uses (e.g. `api`, `ui`, `cli`, package names); the defaults govern everything else.

### Defaults (apply when `COMMIT_GUIDELINES.md` is absent or silent on a given aspect)

- **Style — Conventional Commits.** Format: `<type>(<scope>)?: <subject>`. Common types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `revert`. Scope is optional; include it only when it adds clarity, and prefer scopes the repo already uses.
- **Language — English.** Subject and body are written in English regardless of the conversation language. Switch only when the user explicitly requests another language, or `COMMIT_GUIDELINES.md` mandates one.
- **Length — about 72 characters.** Treat 72 as a target, not a cap: an accurate longer subject is better than a vague short one.
- **Body — subject-only by default.** Add a body when the change spans multiple components or the *why* does not fit in the subject. Small fixes, single-file refactors, doc tweaks, and routine chores get a single line.

## Execution flow

1. Detect whether the user explicitly named file paths.
2. Apply the file selection rule.
3. Check for `COMMIT_GUIDELINES.md`. If absent, skim recent commits for scope conventions.
4. Prepare the concrete proposal: diff statistics (`git diff --stat`) and the drafted commit message.
5. Decide how to proceed based on the current execution mode:
   - **Non-interactive** (e.g. Codex `never` approval policy, or any headless/auto mode where the user cannot reply): **commit directly without printing a draft or waiting for confirmation.**
   - **Interactive** (any mode where the user can reply): run the interactive flow below before committing.
6. Run the commit, then print a summary: `git show --stat --oneline -1`.

## Interactive flow

### Present concrete reviewable results first

Before invoking any question tool:
- Print or display the concrete diff preview: files affected and summary of changes (`git diff --stat` or `git status --short`).
- Display the complete drafted commit message (subject and body if warranted).
- Ensure the user is approving a concrete, fully formed result.

### Asking the user — structured question tools first

- Ask through the agent's structured question tool (e.g. `AskUserQuestion`, or the equivalent the current agent exposes) so the user answers by picking an option. Ask in plain text only when no such tool is available.
- Every question you ask through the tool must present clear actionable choices:
  1. **Approve / Agree** — accept the proposal.
  2. **Reject / Disagree** — refuse the proposal.
  3. **Other** — free-form input for the user (only if the tool requires explicit addition; omit if the platform UI provides write-in input automatically).
  4. Any additional options you consider useful (optional).
- If the question tool does **not** support free-form user input and the user picks **Reject**, follow up by asking the user for direction (e.g. what to change).

### Step 1 — Confirm the commit split (only when rule 3 fired)

If the user did not specify a scope and you are about to commit **all** workspace changes, first judge whether those changes would be better handled as **multiple logical commits** (e.g. unrelated features, or a fix mixed with a refactor).

- If yes, use the question tool to ask whether the user agrees with the proposed split, presenting the planned commits. On approval, create the commits one by one; on rejection, commit everything as a single commit (or ask for direction if the user provided feedback).
- If the changes belong together, proceed directly to Step 2.

### Step 2 — Confirm the draft message and the push action in one session

In a **single question session** (one tool call), ask:

1. **Commit message** — present the draft message(s) and ask whether the user accepts them, with the standard options above (Approve / Reject / Other / extras).
2. **After committing** — ask what to do next, with at least these options:
   1. **Push** — push to the current branch's upstream.
   2. **Create PR and push** — push, then open a pull request.
   3. **Create draft PR and push** — push, then open a draft pull request.
   4. **Don't push** — stop after committing.
   5. **Other** (optional) and any extra options you find necessary.

### Step 3 — Branch handling for PR options

If the user chose **Create PR and push** or **Create draft PR and push**:

- Check whether HEAD is on a branch.
  - **On a branch** → use the question tool to ask whether to push under the current branch name (offer alternatives only if you have a reason, e.g. the branch is `main`).
  - **Not on a branch (detached HEAD)** → generate **several meaningful branch name suggestions** and let the user pick via the question tool. Branch names must:
    - Be descriptive of the change.
    - Use the Conventional Commits type as prefix (e.g. `feat/`, `fix/`, `refactor/`).
    - **Never** use the agent's or model's name as a prefix.
- Then push and create the PR (e.g. `gh pr create` / `gh pr create --draft`).

## Suggested commands

Commit specific files only:

```bash
git commit --only -- <file1> <file2>
```

Commit staged changes:

```bash
git commit -m "<subject>"
```

Commit all workspace changes:

```bash
git add -A
git commit -m "<subject>"
```

Commit with a body (only when justified):

```bash
git commit -F - <<'MSG'
<subject>

<body paragraph explaining the why>
MSG
```

## Output requirements

- State which file-selection rule fired.
- Show the final commit message (subject, plus body only if one was warranted).
- After committing, print a one-line summary with file stats.

## Error handling

- Nothing to commit → stop and report the state of the staging area and worktree.
- Explicitly named files don't exist or have no diff → stop and ask the user to adjust the list.
- Commit failure → return the raw error and a concrete next step.
