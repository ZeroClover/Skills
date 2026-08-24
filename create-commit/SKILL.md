---
name: create-commit
description: "Create Git commits for any repository by choosing files from explicit user selection, existing staged changes, or all workspace changes. Drafts messages following repository-level COMMIT_GUIDELINES.md when present; otherwise defaults to Conventional Commits, in English, with a single-line subject."
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
3. If it does not exist, **do not imitate the repository's existing commit style wholesale.** Skim recent commits **only** to learn the repository's `scope` conventions, then apply the defaults below for everything else.
   - Suggested probe: `git log -n 20 --pretty=format:'%s'`
   - Extract recurring scopes (e.g. `api`, `ui`, `cli`, package names) and reuse them when relevant. Ignore the rest of the prior style.

### Defaults (apply when `COMMIT_GUIDELINES.md` is absent or silent on a given aspect)

- **Style — Conventional Commits.** Format: `<type>(<scope>)?: <subject>`. Common types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `revert`. Scope is optional; include it only when it adds clarity, and prefer scopes the repo already uses.
- **Language — English.** Subject and body are written in English regardless of the conversation language. Switch only when the user explicitly requests another language, or `COMMIT_GUIDELINES.md` mandates one.
- **Length — not bound by the legacy 50-character myth.** Aim for ≤72 characters when natural, but this is **not** a hard cap. A longer, accurate subject beats a vague short one — write what the change actually needs, not what an ancient 80-column terminal allowed.
- **Body — prefer subject-only (single-line) commits.** Add a body **only** when the change is large and spans multiple components, or when the *why* is non-obvious and cannot fit in the subject. Small fixes, single-file refactors, doc tweaks, and routine chores should be a single line. Never pad a body just to fill space.

## Execution flow

1. Detect whether the user explicitly named file paths.
2. Apply the file selection rule.
3. Check for `COMMIT_GUIDELINES.md`. If absent, skim recent commits **only** for scope conventions.
4. Decide how to proceed based on the current execution mode:
   - **Non-interactive** (e.g. Codex `never` approval policy, or any headless/auto mode where the user cannot reply): **commit directly without printing a draft or waiting for confirmation.**
   - **Interactive** (any mode where the user can reply): run the interactive flow below before committing.
5. Run the commit, then print a summary: `git show --stat --oneline -1`.

## Interactive flow

### Asking the user — structured question tools first

- **Always prefer a structured question tool** (e.g. `Ask User Question`, or an equivalent mechanism the current agent exposes) over asking in plain conversation. Never end a turn with a plain-text question and expect the user to reply with a normal prompt, unless **no question tool is available at all**.
- Every question you ask through the tool must include at least:
  1. **Approve / Agree** — accept the proposal.
  2. **Reject / Disagree** — refuse the proposal.
  3. **Other** — free-form input for the user (optional; only if the tool supports it).
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
