---
name: fetch-markdown
description: Fetch rendered web pages as Markdown via Cloudflare Browser Rendering API to reduce context usage. Use this for reading documentation, blog posts, API references, articles, and other page content. Do not use it when the task requires raw HTML/CSS/JS, DOM attributes, browser UI interaction, local HTML files, or frontend rendering inspection.
---

# fetch-markdown

Fetch rendered web pages as Markdown, so agents can read content without filling the context window with HTML, CSS, and JavaScript noise.

## When to use

- Reading documentation, blog posts, API references, articles, or rendered site content.
- User asks to summarize a page, check what docs say, compare article content, or look up library documentation.
- A normal HTTP fetch would miss content because the page needs JavaScript rendering.

## When not to use

- Inspecting raw HTML structure, CSS, JavaScript, meta tags, scripts, DOM attributes, or frontend rendering behavior.
- Clicking through UI, filling forms, debugging local browser layout, taking screenshots, or interacting with a page.
- Processing local HTML files or raw HTML strings. If the HTML is already local, read or convert it with ordinary local tooling instead.
- URLs that already return JSON, plain text, or another machine-readable API response; use the current environment's HTTP or browser tools instead.

## How to call

Use the bundled `scripts/fetch.sh` script from this Skill directory. Resolve the path relative to `SKILL.md`; do not assume the current working directory is the Skill parent. In examples, `$SKILL_DIR` means the resolved directory containing this `SKILL.md`.

```bash
"$SKILL_DIR/scripts/fetch.sh" "https://example.com/docs/page"
```

For long pages, write Markdown to a file and read only the needed sections:

```bash
MD_PATH="$("$SKILL_DIR/scripts/fetch.sh" "https://example.com/long-doc" --output-format file)"
```

## Inputs and output

- Input: a web URL, passed positionally or with `--url <url>`.
- Output: default `stdout`; use `--output-format file` and optionally `--output-file-path <path>` for long pages.

## Credentials

The script accepts credentials from flags, environment variables, or 1Password references.

- API token: `--op-reference <op://...>` > `--api-key <token>` > `CLOUDFLARE_API_TOKEN` > built-in 1Password reference.
- Account ID: `--op-account-reference <op://...>` > `--account-id <id>` > `CLOUDFLARE_ACCOUNT_ID` > built-in 1Password reference.
- Prefer 1Password or environment variables for secrets. `--api-key` is useful for testing, but command-line arguments may appear in shell history or process lists.
- If the user asks to persist new defaults, edit `DEFAULT_OP_ACCOUNT_ID` or `DEFAULT_OP_API_TOKEN` at the top of `scripts/fetch.sh`; do not record secrets in `SKILL.md`.

Cloudflare's quick-action docs call the token permission `Browser Rendering - Edit`; the API reference lists the accepted permission as `Browser Rendering Write`. Use an API token with that Browser Rendering write/edit permission.

## Page loading options

The script intentionally exposes only the loading options that usually help when reading web content:

- `--wait-until load|domcontentloaded|networkidle0|networkidle2` tunes the browser navigation wait. Default is `networkidle0`, which is a good default for rendered docs. A JSON array of those values is also accepted.
- `--wait-for-selector <css>` waits for a known content selector, such as `main article`, when a documentation site is a SPA or renders content late.
- `--wait-for-selector-timeout <ms>` adjusts that selector wait, up to Cloudflare's documented 120000 ms limit.
- `--goto-timeout <ms>` adjusts the navigation timeout, up to Cloudflare's documented 60000 ms limit.
- `--cache-ttl <seconds>` controls Cloudflare's endpoint cache via the API query parameter; `0` disables the cache, and the documented maximum is 86400 seconds.

Do not add one-off Cloudflare Browser Rendering options unless they directly improve the core task of reading page content as Markdown and are reviewed as part of the Skill contract. For browser debugging or interaction, use a browser-specific tool instead.

## Examples

JavaScript-heavy page with a known content selector:

```bash
"$SKILL_DIR/scripts/fetch.sh" "https://example.com/app-docs" \
  --wait-for-selector "main article" \
  --output-format file
```

Disable endpoint caching when checking changing documentation:

```bash
"$SKILL_DIR/scripts/fetch.sh" "https://example.com/latest-docs" --cache-ttl 0
```

Use environment credentials without 1Password:

```bash
CLOUDFLARE_ACCOUNT_ID="..." CLOUDFLARE_API_TOKEN="..." \
  "$SKILL_DIR/scripts/fetch.sh" "https://example.com"
```

## Dependencies and failures

Required commands: `bash`, `curl`, and `jq`. `op` is required only when resolving `op://` references.

On success, stdout contains either the Markdown body or the output file path. On failure, the script exits non-zero and prints Cloudflare's error JSON to stderr when available. Common causes are missing dependencies, locked or missing 1Password references, insufficient Browser Rendering permission, wrong account ID, rate limiting, target URL failures, or page load timeouts.

Official references: [Cloudflare Markdown quick action](https://developers.cloudflare.com/browser-run/quick-actions/markdown-endpoint/) and [Cloudflare Markdown API reference](https://developers.cloudflare.com/api/resources/browser_rendering/subresources/markdown/methods/create/).
