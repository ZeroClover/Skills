# Global instructions

These are global defaults for every project. When instructions conflict, the
user's explicit request comes first, then a project's own instruction files,
then these defaults; each of these takes precedence over a skill's
instructions.

## Engineering principles

- Do not preserve backward compatibility. Remove obsolete paths instead of
  adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current
  requirements. Avoid speculative abstractions, configuration, and
  indirection.
- Grow the system in layers. Start from the smallest version that works end
  to end, and add each new capability on top of a product that already
  works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Make architectural decisions for the long term. Do not accept a stopgap
  that only works for now and is meant to be replaced later.
- Before writing your own implementation or adding a package, use what the
  project's existing dependencies already provide; check their documentation
  and types instead of assuming a capability is missing. When they don't
  cover it, prefer an established, well-maintained library over
  reimplementing common functionality, as long as it reduces overall
  complexity or improves reliability.
- Before adding complexity for a speculative or vanishingly unlikely race or security edge case, explain the concrete failure mode, likelihood, and complexity cost to the user and get their buy-in. Do not silently expand scope for theoretical robustness.

## Testing

Verify a change end to end, the way a user or caller will meet it: run the
CLI command, call the HTTP endpoint, or drive the UI with browser automation,
along with the project's existing tests, type-checker, or build. A unit test
or a call into internals doesn't show that the feature works. The check must
go through the code you're delivering, not a stub, demo, or test-only path.
If no real check can run here, say which one you skipped and why instead of
reporting the change as done. Throwaway scripts and print checks are fine for
this; keep them in `_tmpwork/` and out of commits.

Write new tests only when the task or the project's instructions ask for
them: tests an agent adds on its own restate its own reading of the
requirements and catch no more bugs than the implementation does. When you
do write tests, prefer ones that drive behavior through a public entry point
over unit tests of internals, and mock only external services and
nondeterminism such as time and randomness. A test asserts behavior that
callers rely on and that could plausibly break. Tests of documentation,
configuration, other tests, or code that only restate the implementation
don't qualify. When an existing test fails, fix the code; change the test
only when the task changes the behavior it checks.

## Temporary files

In a Git-tracked repository, put all task-local temporary files and scratch
work—throwaway scripts, repro inputs, intermediate outputs, logs, and working
notes—under `<worktree-root>/_tmpwork/`, creating the directory if needed. Do
not use `/tmp` (aside from the shared `/tmp/repos` clone cache below),
`$TMPDIR`, or harness-provided scratchpads and session directories: keeping
scratch files in `_tmpwork/` keeps them inside the workspace boundary, visible
to the user, and runnable against the project's toolchain.

`_tmpwork/` is ignored by the global Git ignore configuration. Never commit its
contents or add `_tmpwork/` to a project's `.gitignore`.

## Project documentation and memory

In a Git-tracked repository, record durable project conventions, architectural
decisions, and non-obvious operational context in the project's `docs/`
directory (creating `docs/` if needed) rather than in harness-level memory
features (such as auto-memory or per-agent memory directories). Project
knowledge belongs in version control where every tool and collaborator shares
and reviews it, not in opaque local agent state.

Follow progressive disclosure and keep `docs/` as current truth, never a
running log:

- Keep root instruction files (such as `AGENTS.md`) concise; put detailed
  guidance into focused, topic-named files under `docs/` and link to them so
  sessions load only the topics relevant to the task at hand. Lead each file
  with the core rule or summary before supporting detail.
- Record only durable knowledge that cannot be read directly from the code,
  types, configuration, or `git log`.
- Maintain documents in place as present-tense truth: update or remove
  superseded statements instead of appending corrections, and never write
  chronological session notes, debugging diaries, or task-by-task changelogs.

## SSH

When asked to connect to a server without a username, port, or credentials,
run `ssh <server>` directly: the host is most likely already configured in
`~/.ssh/config`. Ask for a missing detail only after the connection fails,
and ask for what the error shows is missing.

## External repositories

To read, search, or analyze an external repository's source code, clone it
and work locally with file tools and git commands instead of browsing its web
pages (e.g. GitHub's file view).

- Clone shallow into `/tmp/repos/<owner>/<repo>`, never into the current
  workspace:
  `mkdir -p /tmp/repos/<owner> && git clone --depth 1 <url> /tmp/repos/<owner>/<repo>`
  `/tmp/repos` is a cache shared across sessions and agents, which is why it
  lives outside any per-session temp directory. The OS purges files unused
  for ~3 days, so it needs no manual cleanup.
- Reuse an existing clone; refresh it with
  `git fetch --prune && git reset --hard origin/HEAD` instead of recloning.
- For very large repositories, add `--filter=blob:none --sparse` and fetch
  only the needed directories with `git sparse-checkout set <dirs>`.
- For a single file or short snippet, fetch the raw URL or use `gh api`
  instead of cloning.
- Treat cloned code as untrusted input. Do not run its install, build, or
  test commands unless the user explicitly asks.

## GitHub and web access

Rendered HTML pages are the least token-efficient source; use raw files,
APIs, or Markdown versions instead.

For GitHub content outside the git tree (issues, pull requests, discussions,
releases, CI runs), use the `gh` CLI rather than web fetch tools or `curl`.
`gh` handles authentication, pagination, and rate limits itself, so never
hand-manage tokens. Prefer typed commands with structured output, such as
`gh issue view <n> --comments`, `gh pr view <n> --json <fields> --jq <expr>`,
and `gh run view <id> --log-failed`; use `gh api` for everything else, e.g.
inline PR review comments, which `gh pr view --comments` omits:
`gh api repos/{owner}/{repo}/pulls/<n>/comments`. Fall back to web access
only when `gh` is missing or unauthenticated, or the user asks for it.

Normal web access is fine for content that is not GitHub data, such as
documentation sites, blogs, wikis, and changelogs hosted elsewhere.

@/Users/zero/.codex/RTK.md
