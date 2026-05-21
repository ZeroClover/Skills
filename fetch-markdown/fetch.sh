#!/usr/bin/env bash
set -euo pipefail

DEFAULT_OP_ACCOUNT_ID="op://Private/Cloudflare API Token Set/Account ID"
DEFAULT_OP_API_TOKEN="op://Private/Cloudflare API Token Set/Browser Rendering RW"

usage() {
  cat <<'EOF' >&2
Usage: fetch.sh <url> [options]

Options:
  --api-key <token>            Plaintext Cloudflare API token.
  --op-reference <op://...>    1Password CLI reference for the API token.
                               Takes precedence over --api-key.
                               Default: built-in reference.
  --output-format <stdout|file>
                               Where to write the Markdown. Default: stdout.
  --output-file-path <path>    Destination file when --output-format=file.
                               If omitted, a temp file is created via mktemp.
  -h, --help                   Show this help.
EOF
}

URL=""
API_KEY=""
OP_REFERENCE=""
OUTPUT_FORMAT="stdout"
OUTPUT_FILE_PATH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --api-key)          API_KEY="${2:?--api-key requires a value}"; shift 2 ;;
    --op-reference)     OP_REFERENCE="${2:?--op-reference requires a value}"; shift 2 ;;
    --output-format)    OUTPUT_FORMAT="${2:?--output-format requires a value}"; shift 2 ;;
    --output-file-path) OUTPUT_FILE_PATH="${2:?--output-file-path requires a value}"; shift 2 ;;
    -h|--help)          usage; exit 0 ;;
    --) shift; break ;;
    -*) echo "Unknown option: $1" >&2; usage; exit 2 ;;
    *)
      if [[ -z "$URL" ]]; then URL="$1"; shift
      else echo "Unexpected positional argument: $1" >&2; exit 2
      fi
      ;;
  esac
done

if [[ -z "$URL" ]]; then
  echo "Error: <url> is required." >&2
  usage
  exit 2
fi

case "$OUTPUT_FORMAT" in
  stdout|file) ;;
  *) echo "Error: --output-format must be 'stdout' or 'file'." >&2; exit 2 ;;
esac

# --op-reference always wins. If neither flag is given, fall back to the
# built-in op reference so the script works with zero credential flags.
if [[ -z "$OP_REFERENCE" && -z "$API_KEY" ]]; then
  OP_REFERENCE="$DEFAULT_OP_API_TOKEN"
fi

resolve_via_op() {
  if ! command -v op >/dev/null 2>&1; then
    echo "Error: 'op' (1Password CLI) is required to resolve op:// references." >&2
    exit 1
  fi
  op read --no-newline -- "$1"
}

if [[ -n "$OP_REFERENCE" ]]; then
  RESOLVED_TOKEN="$(resolve_via_op "$OP_REFERENCE")"
else
  RESOLVED_TOKEN="$API_KEY"
fi

# Account ID currently has no flag — always resolved from the built-in op
# reference. Override by editing DEFAULT_OP_ACCOUNT_ID at the top of the file.
RESOLVED_ACCOUNT_ID="$(resolve_via_op "$DEFAULT_OP_ACCOUNT_ID")"

if [[ -z "$RESOLVED_TOKEN" || -z "$RESOLVED_ACCOUNT_ID" ]]; then
  echo "Error: failed to resolve credentials." >&2
  exit 1
fi

REQUEST_BODY="$(jq -n --arg url "$URL" \
  '{url: $url, gotoOptions: {waitUntil: "networkidle0"}}')"

RESPONSE="$(curl -sS -X POST \
  "https://api.cloudflare.com/client/v4/accounts/${RESOLVED_ACCOUNT_ID}/browser-rendering/markdown" \
  -H "Authorization: Bearer ${RESOLVED_TOKEN}" \
  -H "Content-Type: application/json" \
  --data-binary @- <<<"$REQUEST_BODY")"

if ! echo "$RESPONSE" | jq -e '.success == true' >/dev/null 2>&1; then
  echo "Cloudflare Browser Rendering request failed:" >&2
  echo "$RESPONSE" | jq . >&2 || echo "$RESPONSE" >&2
  exit 1
fi

MARKDOWN="$(echo "$RESPONSE" | jq -r '.result')"

if [[ "$OUTPUT_FORMAT" == "stdout" ]]; then
  printf '%s\n' "$MARKDOWN"
else
  if [[ -z "$OUTPUT_FILE_PATH" ]]; then
    OUTPUT_FILE_PATH="$(mktemp -t fetch-markdown.XXXXXX.md)"
  fi
  printf '%s\n' "$MARKDOWN" > "$OUTPUT_FILE_PATH"
  printf '%s\n' "$OUTPUT_FILE_PATH"
fi
