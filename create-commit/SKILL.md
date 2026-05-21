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
4. Draft the commit message and present it to the user before committing.
5. Run the commit, then print a summary: `git show --stat --oneline -1`.

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
