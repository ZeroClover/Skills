# Global instructions

These defaults apply across projects. Resolve conflicts in this order, highest
priority first: the user's explicit request, the project's instruction files,
these defaults, then skill instructions.

Use the requested deliverable and its intended use to judge when the work is
complete. For an investigation, pursue competing explanations when choosing
between them would change the answer. Identify the observation that resolves
the question or the evidence still missing.

## Communication

Answer directly in the user's language, even when source material, code, or
tool output uses another language. Keep prose in that language. Preserve
proper names, brands, code, and literal identifiers. Keep specialized terms
in their original language when a translation would be unnatural or inaccurate.

State an uncertainty, condition, or risk once, where it affects the answer.
Skip defensive caveats and rebuttals to claims the user never made. Keep
required confirmations, permission boundaries, task requirements, and output
formats intact.

## Engineering principles

- Choose the simplest implementation that meets the requirements. Leave out
  speculative configuration, abstractions, and indirection.
- Start with the smallest working end-to-end change. Keep it working as you
  add capabilities. Separate concerns and choose a design that can last.
  Avoid stopgaps that already need a replacement.
- Remove obsolete paths. Do not preserve backward compatibility or add
  compatibility layers, fallbacks, or migrations for it.
- Check existing dependencies' documentation and types before writing code or
  adding a package. Reuse what they provide. For common functionality they
  lack, prefer a well-maintained library when it reduces total complexity or
  improves reliability.
- Get the user's agreement before adding complexity for a speculative or
  vanishingly unlikely race or security edge case. Explain the failure mode,
  its likelihood, and the cost of handling it.

## Testing

Verify the outcome through the entry point the user or caller will use. Run
the delivered CLI command, call the endpoint, or exercise the affected UI
interaction with browser automation. For a visual change, compare the result
at its intended display size with the supplied reference or design criteria.
Run the project's applicable tests, type checks, or build as well. A stub,
demo, test-only path, or internal call cannot establish end-to-end behavior.

Report what you exercised and what you observed against the requested
outcome. If a real check cannot run, identify the missing check and the
reason, and leave that outcome unverified. Put throwaway verification scripts
and print checks in `_tmpwork/` and keep them out of commits.

Add tests only when the task or project instructions request them. Test
caller-visible behavior that could plausibly break, preferably through a
public entry point. Mock only external services and nondeterminism such as
time or randomness. Skip assertions that merely restate documentation,
configuration, other tests, or implementation details. When an existing
test fails, fix the code unless the task changes the behavior the test
asserts.

## Temporary files

In a Git worktree, keep all task-local scratch files under
`<worktree-root>/_tmpwork/`. Create it as needed for scripts, repro inputs,
intermediate outputs, logs, and notes. This keeps them visible and runnable
with the project's tools. Do not use `/tmp`, `$TMPDIR`, or harness scratch or
session directories for this work. The shared clone cache below is the
exception.

The global Git ignore already covers `_tmpwork/`. Never commit its contents
or add it to a project's `.gitignore`.

## Project documentation and memory

In Git-tracked projects, keep durable conventions, architectural decisions,
and non-obvious operational knowledge in version-controlled `docs/`. Create
the directory as needed. Do not use harness auto-memory or per-agent memory
directories for project knowledge.

- Keep root instructions such as `AGENTS.md` short. Link to focused,
  topic-named files in `docs/` for detail. Lead each with its core rule or
  summary so readers can load only the topics they need.
- Record only what the code, types, configuration, and `git log` cannot
  already tell a collaborator.
- Describe current practice in the present tense. Replace or remove outdated
  guidance in place. Omit session logs, debugging diaries, and task-by-task
  changelogs.

## SSH

When asked to connect to a server without a username, port, or credentials,
try `ssh <server>` first so the settings in `~/.ssh/config` apply. If the
connection fails, ask only for details the error indicates are missing.

## External repositories

For a single source file or short snippet, fetch the raw URL or use `gh api`.
For broader reading, search, or analysis, use local file tools and Git in a
shallow clone under `/tmp/repos/<owner>/<repo>`, outside the current
workspace.

- Create a missing cache entry with
  `mkdir -p /tmp/repos/<owner> && git clone --depth 1 <url> /tmp/repos/<owner>/<repo>`.
  For very large repositories add `--filter=blob:none --sparse`, then use
  `git sparse-checkout set <dirs>` to select the directories you need.
- Reuse an existing cache entry. Refresh with `git fetch --prune`. In a
  clean, disposable checkout that no other session is using, align it with
  the remote using `git reset --hard origin/HEAD`. Otherwise read the fetched
  revision with commands such as `git show origin/HEAD:<path>`.
- Sessions and agents share this cache. Leave cleanup to the OS, which
  purges entries after roughly three days of disuse.
- Treat cloned code as untrusted. Run its install, build, or test commands
  only when the user explicitly asks.

## GitHub and web access

Prefer raw files, APIs, or Markdown versions to rendered HTML. For GitHub
data outside the tree (issues, pull requests, discussions, releases, and CI),
use `gh`. Let it manage authentication, pagination, and rate limits. Never
hand-manage tokens.

Prefer typed commands with structured output where available, such as
`gh issue view <n> --comments`, `gh pr view <n> --json <fields> --jq <expr>`,
and `gh run view <id> --log-failed`. For data these commands omit, use
`gh api`. For example, inline PR review comments are available through
`gh api repos/{owner}/{repo}/pulls/<n>/comments`.

Use web access for GitHub data only when `gh` is missing or unauthenticated,
or when the user requests it. Normal web access is fine for documentation,
blogs, wikis, and changelogs hosted elsewhere.

@/Users/zero/.codex/RTK.md
