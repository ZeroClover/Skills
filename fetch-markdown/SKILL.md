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

## Credentials

Credentials declared for this skill:

<!--
Fill in the references below to enable non-interactive use. Example:

- Account ID: `op://Private/Cloudflare API Token Set/Account ID`
- API Token: `op://Private/Cloudflare API Token Set/Browser Rendering RW`

Plaintext values are also accepted but discouraged for the API Token.
-->

- Account ID: _(not declared)_
- API Token: _(not declared)_

**If either credential above is missing from this section, or no retrieval method is declared**, use `AskUserQuestion` to ask the user for:

1. Cloudflare Account ID (plaintext or `op://...` reference)
2. Cloudflare API Token (strongly prefer an `op://...` reference to keep the token out of conversation context)

After the user answers, offer to persist the values into this section so future invocations skip the prompt.

## How to call

**Always inject credentials via `op run` or `op read`** when they are `op://...` references. Never paste the token inline, never print it to stdout.

Use `op run` with an env file so credentials stay out of process args, and build the JSON body with `jq` to avoid shell-quoting bugs:

```bash
TARGET_URL="https://example.com/docs/page"

op run --no-masking --env-file=<(cat <<'EOF'
ACCOUNT_ID=op://Private/Cloudflare API Token Set/Account ID
API_TOKEN=op://Private/Cloudflare API Token Set/Browser Rendering RW
EOF
) -- bash -c '
  jq -n --arg url "'"$TARGET_URL"'" \
    "{url: \$url, gotoOptions: {waitUntil: \"networkidle0\"}}" \
  | curl -sS -X POST \
      "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/browser-rendering/markdown" \
      -H "Authorization: Bearer $API_TOKEN" \
      -H "Content-Type: application/json" \
      --data-binary @-
' | jq -r 'if .success then .result else . end'
```

Notes:

- `op run` resolves `op://...` references into env vars; the token never appears in process args or shell history.
- **Do NOT** pass `TARGET_URL=... op run ...` as an inline prefix — that env var is only exported to `op run`'s process, not available for `"$TARGET_URL"` expansion in the outer shell. Set it as a separate statement first, as shown above.
- Building the JSON body with `jq -n --arg` escapes the URL correctly, avoiding the `Invalid url` error caused by nested single/double-quote interpolation.
- Use `--data-binary @-` to stream the JSON body via stdin, sidestepping `-d` argument-length and quoting issues.
- The trailing `jq` emits only `.result` (the Markdown body) on success, or the full JSON on failure for easier debugging.
- If credentials are plaintext (not `op://...`), drop the `op run` wrapper and export them directly — but still avoid echoing the token.

## Response shape

Success:

```json
{
  "success": true,
  "result": "# Example Domain\n\nThis domain is for use..."
}
```

`.result` is the Markdown content of the target URL — use it directly.

On failure, `success` is `false`; inspect the `errors` field. Common causes: insufficient token permissions, wrong account ID, target URL unreachable.
