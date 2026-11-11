# Repository Guidelines

This repository stores reusable agent skills and global agent instructions:

```text
.
├── instructions/
│   └── instructions.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        ├── scripts/
        ├── references/
        ├── assets/
        └── ...
```

Only create optional directories inside a skill when they contain files the skill actually needs.

Keep global instructions in `instructions/instructions.md`. Do not place `SKILL.md` in `instructions/` (so skill tooling never treats it as a skill), and do not name files in `instructions/` `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` (so agents do not auto-load them as directory-scoped workspace rules while editing).

## Python and uv

- Do not install Python packages into the system Python.
- Use this repository's `uv` project for Python tooling.
- Keep `.python-version` committed so agents use the same interpreter family.
- Let `uv` create and manage `.venv/`; do not commit `.venv/`.
- Add Python tooling dependencies with `uv add --dev <package>`.
- On cross-filesystem workspaces, set `UV_LINK_MODE=copy` if `uv` warns that hardlinking is unavailable.
- Run Python tools with `uv run ...`, for example:

```bash
uv run python /Users/zero/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/create-commit
```

## Skill Maintenance

- Keep `SKILL.md` frontmatter limited to validator-supported fields.
- Prefer concise `SKILL.md` instructions and move detailed, task-specific material into `references/` only when needed.
- Put executable helper code in `scripts/`.
- Put templates and reusable output resources in `assets/`.
- Do not add README, changelog, install guides, or process notes inside skill directories unless the user explicitly asks for them.

## Validation

After changing a skill, validate it from the repository root:

```bash
uv run python /Users/zero/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

For shell helpers, also run syntax checks such as:

```bash
bash -n skills/<skill-name>/scripts/<script>.sh
```

## Autonomous Execution and Boundaries

- Running validation (`quick_validate.py`, `bash -n`, repo unit tests) is completely safe, local, and read-only. Run these checks, fix any reported issues autonomously, and re-verify without stopping for user approval at each step.
- Consider a task complete only when all changed skills pass validation.

