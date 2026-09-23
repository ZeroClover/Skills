---
name: clean-agent-cache
description: "Reclaim disk space by auditing or deleting caches, logs, and temp files from AI coding agents (Claude Code, Codex, Cursor, etc.). Safe and dry-run by default; history cleanup is opt-in."
---

# Clean Agent Cache

Reclaim disk used by AI coding agents. A structured registry lists every
safe-to-delete item per agent; a Python engine reads it and removes them.

- **Registry (edit this to maintain):** `references/targets.toml`
- **Engine (run this):** `scripts/clean.py`

## Core safety rules

1. **Dry-run first, always.** The engine defaults to dry-run. Show the user the
   plan and the reclaimable total before deleting.
2. **Tiers are opt-in.** Only `safe` items (caches/logs/temp) run by default.
   Conversation/session/command **history** and large **aggressive**
   (re-downloadable) items run only when the user explicitly asks, via
   `--include`.
3. **Never delete config/credentials/memory/skills/plugins/login state.** These
   are not in the registry and are additionally guarded by a `protected`
   allow-never list the engine enforces.
4. **Quit the app for `requires_app_closed` items.** Desktop Electron caches and
   live SQLite DBs are skipped while the agent is running; tell the user to quit
   the app to reclaim that space.

## Workflow

Run everything through the repo's `uv` environment.

1. **Preview (dry-run).** Default is all agents, safe tier only:
   ```bash
   uv run python clean-agent-cache/scripts/clean.py
   ```
   Scope it when asked:
   ```bash
   uv run python clean-agent-cache/scripts/clean.py --agent claude-code,codex
   ```

2. **Report to the user** the reclaimable total, anything held back by a running
   app, and — if they want history/aggressive — what those tiers would add:
   ```bash
   uv run python clean-agent-cache/scripts/clean.py --include all
   ```

3. **Apply** only after the user confirms. Use `--yes` (the engine refuses to
   apply non-interactively without it):
   ```bash
   uv run python clean-agent-cache/scripts/clean.py --apply --yes
   ```
   History is opt-in and can keep recent data with `--older-than`:
   ```bash
   uv run python clean-agent-cache/scripts/clean.py --include history --older-than 30 --apply --yes
   ```

## Engine options

| Flag | Effect |
| --- | --- |
| `--agent a,b` | Limit to agent keys (see `--list-agents`). |
| `--category c,b` | Limit to categories (cache, logs, sessions, …). |
| `--include history,aggressive` | Add risk tiers beyond `safe` (`all` = everything). |
| `--older-than DAYS` | Only delete items older than DAYS (great for history). |
| `--apply` / `--yes` | Actually delete / skip the confirm prompt. |
| `--json` | Machine-readable plan/result. |
| `--list-agents`, `--list-targets` | Inspect the registry. |

## Risk tiers

- **safe** — caches, GPU caches, logs, telemetry, temp, shell snapshots,
  prunable backups. Cleaned by default; regenerated automatically.
- **history** — conversation transcripts, sessions, archived sessions, command
  history, file-edit history. Deletion loses records but is otherwise safe.
- **aggressive** — large re-downloadable/rebuildable data (e.g. old bundled
  runtime versions, OpenCode snapshots, Cursor semantic index). Big wins, but a
  rebuild/re-download cost on next use.

## Maintaining the registry

`references/targets.toml` is the single source of truth — the engine hard-codes
no paths. To add an agent or item, add a `[[target]]` (and `[[agent]]` if new)
following the schema documented at the top of the file. Keep destructive items
in the correct tier and add anything credential/config/memory-like to the
`protected` list. After editing, validate:

```bash
uv run python /Users/zero/.codex/skills/.system/skill-creator/scripts/quick_validate.py clean-agent-cache
```

## Notes per agent

- **Claude Code / Codex** are first-class and verified on this machine. Codex's
  `logs*.sqlite` log DB (often GBs of TRACE rows) is the biggest win: it is
  pruned in place with `DELETE` + `VACUUM` (not deleted), so the schema and any
  rows you keep via `--older-than` survive. VACUUM needs exclusive access, so
  quit Codex first. The Claude desktop VM bundle is intentionally **not** a
  target — deleting it just forces a large re-download.
- **Conductor**: never delete `~/conductor/workspaces` — worktrees may hold
  uncommitted code. Use Conductor's in-app Archive instead.
- **Antigravity**: `~/.gemini/antigravity*/conversations` and `brain` are chat
  history and agent memory, not cache — protected, never auto-deleted.
- **Grok**: `~/.grok` is shared by xAI's official CLI and a third-party tool;
  only clearly-safe, source-confirmed items are listed.
- Paths absent on the current machine are silently skipped.
