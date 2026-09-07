---
name: find-skills
description: Discover and install agent skills from the open agent skills ecosystem (npx skills). Use when the user asks to search for, discover, or install an agent skill or capability package.
---

# Find Skills

Discover and install skills from the open agent skills ecosystem.

## When to Use This Skill

Use this skill when the user:

- Asks to find or recommend a skill for a given task or framework (e.g. "find a skill for Next.js", "is there a skill for Playwright?")
- Expresses interest in extending agent capabilities with external skills
- Wants to search for or install community tools and workflows via `npx skills`

Do not use this skill for general programming questions that can be answered directly.

## Skills CLI Commands

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem:

- `npx skills find [query] [--owner <owner>]` — Search for skills interactively or by keyword.
- `npx skills add <package>` — Install a skill (e.g. `npx skills add <owner/repo@skill> -g -y`).
- `npx skills check` — Check installed skills for updates.
- `npx skills update` — Update all installed skills.
- Browse online: https://skills.sh/

## Workflow

### 1. Search for Skills

Run the find command with specific domain keywords:

```bash
npx skills find [query] [--owner <owner>]
```

For well-known domains (React, Tailwind, Playwright), also check the [skills.sh leaderboard](https://skills.sh/) for battle-tested options from established maintainers (e.g. `vercel-labs`, `anthropics`).

### 2. Evaluate Quality

Before recommending or installing, verify:

- **Install count** — Prefer skills with 1K+ installs; exercise caution with low-adoption skills.
- **Source reputation** — Well-known organizations or verified maintainers provide safer, higher quality guidance.
- **Source repository** — Inspect the underlying repo's activity, issues, and star count when uncertain.

### 3. Present and Install

Provide the user with:
- The skill package name and a brief summary of what it does.
- Its install count and source repository.
- The command to install it.

When authorized to install directly, run:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally and `-y` proceeds non-interactively.

### 4. When No Matching Skill Exists

If no suitable skill is found, state that directly, address the user's task using your existing capabilities, and mention that a custom skill can be created with `npx skills init <skill-name>` if needed.
