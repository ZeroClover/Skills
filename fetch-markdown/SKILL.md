---
name: fetch-markdown
description: Fetch web pages as Markdown via Cloudflare Browser Rendering API instead of the built-in WebFetch tool, to drastically reduce token usage. Use this for documentation, blog posts, API references, articles — any task where the goal is reading content. Do NOT use this when the task requires inspecting raw HTML, CSS, JS, or DOM structure.
user-invocable: false
---

# fetch-markdown

Fetch web pages as Markdown using Cloudflare Browser Rendering API to avoid spending tokens on HTML tags, inline CSS, and JS.

## When to use

- Fetching documentation, blog posts, API references, or articles **to read the content**
- User says things like "summarize this page", "check what this doc says", "look up this library's docs"

## When NOT to use

- Inspecting raw HTML structure, debugging frontend rendering
- Extracting meta tags, inline scripts, or DOM attributes
- The URL already returns JSON or plain text (just use `curl`)

In those cases, fall back to the built-in WebFetch or `curl`.

## How to call

**Always use the bundled `fetch.sh` script.** Do not hand-roll `curl` calls — the script already handles JSON body construction, credential resolution via 1Password CLI, and stdout-vs-file output.

```
fetch.sh <url> [options]
```

Options:

- `--api-key <token>` — plaintext Cloudflare API token.
- `--op-reference <op://...>` — 1Password CLI reference for the API token. **Takes precedence over `--api-key`** if both are given. Defaults to a built-in reference baked into the script, so in the normal case you can omit both flags entirely.
- `--output-format <stdout|file>` — default `stdout`. Use `file` for long pages to keep Markdown out of the conversation context; the script prints the file path, then `Read` it on demand.
- `--output-file-path <path>` — destination file when `--output-format=file`. If omitted, a temp file is created via `mktemp` and its path is printed.

### Typical usage

Short page, content goes straight into context:

```bash
./fetch-markdown/fetch.sh "https://example.com/docs/page"
```

Long page, save to a temp file and read selectively:

```bash
MD_PATH="$(./fetch-markdown/fetch.sh "https://example.com/long-doc" --output-format file)"
# then use Read on "$MD_PATH"
```

Override the token source (e.g. testing with a fresh token):

```bash
./fetch-markdown/fetch.sh "https://example.com" --op-reference "op://Private/Other Vault/Token"
```

## Credentials

The script has built-in 1Password references for both the Cloudflare Account ID and the API Token, so no credential flag is required in the default setup. If `op read` fails (vault locked, reference missing, `op` not installed), the script exits with a clear error — surface that to the user and let them either unlock 1Password or pass `--api-key` directly.

When the user supplies new credentials and asks to persist them, edit `DEFAULT_OP_ACCOUNT_ID` / `DEFAULT_OP_API_TOKEN` at the top of `fetch.sh` rather than recording them here.

## Response shape

On success the script prints either the Markdown body (stdout mode) or the path to a file containing it (file mode). On failure it prints the full Cloudflare error JSON to stderr and exits non-zero — surface those errors verbatim when reporting back. Common causes: insufficient token permissions, wrong account ID, target URL unreachable.
