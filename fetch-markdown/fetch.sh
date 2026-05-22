#!/usr/bin/env bash
set -euo pipefail

DEFAULT_OP_ACCOUNT_ID="op://Private/Cloudflare API Token Set/Account ID"
DEFAULT_OP_API_TOKEN="op://Private/Cloudflare API Token Set/Browser Rendering RW"

usage() {
  cat <<'EOF' >&2
Usage: fetch.sh <url> [options]

Options:
  --url <url>                 URL to render. Also accepted as the first positional argument.
  --api-key <token>           Plaintext Cloudflare API token.
  --op-reference <op://...>   1Password CLI reference for the API token.
                              Takes precedence over --api-key.
                              Default: CLOUDFLARE_API_TOKEN, then built-in reference.
  --account-id <id>           Cloudflare account ID.
  --op-account-reference <op://...>
                              1Password CLI reference for the Cloudflare account ID.
                              Takes precedence over --account-id.
                              Default: CLOUDFLARE_ACCOUNT_ID, then built-in reference.
  --output-format <stdout|file>
                              Where to write the Markdown. Default: stdout.
  --output-file-path <path>   Destination file when --output-format=file.
                              If omitted, a temp file is created via mktemp.
  --cache-ttl <seconds>       Cloudflare cacheTTL query parameter. Use 0 to disable.
  --wait-until <event|json>   gotoOptions.waitUntil. Default: networkidle0.
                              Accepts load, domcontentloaded, networkidle0, networkidle2,
                              or a JSON array of those values.
  --goto-timeout <ms>         gotoOptions.timeout.
  --wait-for-selector <css>   waitForSelector.selector.
  --wait-for-selector-timeout <ms>
                              waitForSelector.timeout.
  -h, --help                  Show this help.
EOF
}

URL=""
API_KEY=""
OP_REFERENCE=""
ACCOUNT_ID=""
OP_ACCOUNT_REFERENCE=""
OUTPUT_FORMAT="stdout"
OUTPUT_FILE_PATH=""
CACHE_TTL=""
WAIT_UNTIL="networkidle0"
GOTO_TIMEOUT=""
WAIT_FOR_SELECTOR=""
WAIT_FOR_SELECTOR_TIMEOUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --url) URL="${2:?--url requires a value}"; shift 2 ;;
    --api-key) API_KEY="${2:?--api-key requires a value}"; shift 2 ;;
    --op-reference) OP_REFERENCE="${2:?--op-reference requires a value}"; shift 2 ;;
    --account-id) ACCOUNT_ID="${2:?--account-id requires a value}"; shift 2 ;;
    --op-account-reference) OP_ACCOUNT_REFERENCE="${2:?--op-account-reference requires a value}"; shift 2 ;;
    --output-format) OUTPUT_FORMAT="${2:?--output-format requires a value}"; shift 2 ;;
    --output-file-path) OUTPUT_FILE_PATH="${2:?--output-file-path requires a value}"; shift 2 ;;
    --cache-ttl) CACHE_TTL="${2:?--cache-ttl requires a value}"; shift 2 ;;
    --wait-until) WAIT_UNTIL="${2:?--wait-until requires a value}"; shift 2 ;;
    --goto-timeout) GOTO_TIMEOUT="${2:?--goto-timeout requires a value}"; shift 2 ;;
    --wait-for-selector) WAIT_FOR_SELECTOR="${2:?--wait-for-selector requires a value}"; shift 2 ;;
    --wait-for-selector-timeout) WAIT_FOR_SELECTOR_TIMEOUT="${2:?--wait-for-selector-timeout requires a value}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    --) shift; break ;;
    -*) echo "Unknown option: $1" >&2; usage; exit 2 ;;
    *)
      if [[ -z "$URL" ]]; then
        URL="$1"
        shift
      else
        echo "Unexpected positional argument: $1" >&2
        exit 2
      fi
      ;;
  esac
done

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: '$1' is required." >&2
    exit 1
  fi
}

require_command curl
require_command jq

if [[ -z "$URL" ]]; then
  echo "Error: <url> is required." >&2
  usage
  exit 2
fi

case "$OUTPUT_FORMAT" in
  stdout|file) ;;
  *) echo "Error: --output-format must be 'stdout' or 'file'." >&2; exit 2 ;;
esac

validate_number() {
  local name="$1"
  local value="$2"
  if [[ -n "$value" ]] && ! jq -n -e --arg value "$value" '$value | tonumber | type == "number"' >/dev/null 2>&1; then
    echo "Error: $name must be numeric." >&2
    exit 2
  fi
}

validate_number_range() {
  local name="$1"
  local value="$2"
  local min="$3"
  local max="$4"
  validate_number "$name" "$value"
  if [[ -n "$value" ]] && ! jq -n -e \
    --arg value "$value" \
    --argjson min "$min" \
    --argjson max "$max" \
    '($value | tonumber) as $n | $n >= $min and $n <= $max' >/dev/null 2>&1; then
    echo "Error: $name must be between $min and $max." >&2
    exit 2
  fi
}

normalize_wait_until() {
  local value="$1"
  if ! jq -c -n --arg value "$value" '
    def valid_event:
      . == "load" or . == "domcontentloaded" or . == "networkidle0" or . == "networkidle2";

    (try ($value | fromjson) catch $value) as $parsed
    | if ($parsed | type) == "array" then
        if (($parsed | length) > 0 and all($parsed[]; type == "string" and valid_event)) then
          $parsed
        else
          halt_error(1)
        end
      elif (($parsed | type) == "string" and ($parsed | valid_event)) then
        $parsed
      else
        halt_error(1)
      end
  ' 2>/dev/null; then
    echo "Error: --wait-until must be load, domcontentloaded, networkidle0, networkidle2, or a JSON array of those values." >&2
    exit 2
  fi
}

validate_number_range "--cache-ttl" "$CACHE_TTL" 0 86400
validate_number_range "--goto-timeout" "$GOTO_TIMEOUT" 0 60000
validate_number_range "--wait-for-selector-timeout" "$WAIT_FOR_SELECTOR_TIMEOUT" 0 120000
NORMALIZED_WAIT_UNTIL="$(normalize_wait_until "$WAIT_UNTIL")"

read_op_reference() {
  if ! command -v op >/dev/null 2>&1; then
    echo "Error: 'op' (1Password CLI) is required to resolve op:// references." >&2
    exit 1
  fi
  op read --no-newline -- "$1"
}

resolve_credential() {
  local op_reference="$1"
  local plaintext="$2"
  local env_value="$3"
  local default_op_reference="$4"

  if [[ -n "$op_reference" ]]; then
    read_op_reference "$op_reference"
  elif [[ -n "$plaintext" ]]; then
    printf '%s' "$plaintext"
  elif [[ -n "$env_value" ]]; then
    printf '%s' "$env_value"
  else
    read_op_reference "$default_op_reference"
  fi
}

RESOLVED_TOKEN="$(resolve_credential "$OP_REFERENCE" "$API_KEY" "${CLOUDFLARE_API_TOKEN:-}" "$DEFAULT_OP_API_TOKEN")"
RESOLVED_ACCOUNT_ID="$(resolve_credential "$OP_ACCOUNT_REFERENCE" "$ACCOUNT_ID" "${CLOUDFLARE_ACCOUNT_ID:-}" "$DEFAULT_OP_ACCOUNT_ID")"

if [[ -z "$RESOLVED_TOKEN" || -z "$RESOLVED_ACCOUNT_ID" ]]; then
  echo "Error: failed to resolve credentials." >&2
  exit 1
fi

REQUEST_BODY="$(jq -n \
  --arg url "$URL" \
  --argjson wait_until "$NORMALIZED_WAIT_UNTIL" \
  --arg goto_timeout "$GOTO_TIMEOUT" \
  --arg wait_for_selector "$WAIT_FOR_SELECTOR" \
  --arg wait_for_selector_timeout "$WAIT_FOR_SELECTOR_TIMEOUT" \
  '
  def number_or_empty($value): if $value == "" then empty else ($value | tonumber) end;

  {url: $url, gotoOptions: {waitUntil: $wait_until}}
  | if $goto_timeout != "" then .gotoOptions.timeout = number_or_empty($goto_timeout) else . end
  | if $wait_for_selector != "" then
      .waitForSelector = {selector: $wait_for_selector}
      | if $wait_for_selector_timeout != "" then .waitForSelector.timeout = number_or_empty($wait_for_selector_timeout) else . end
    else . end
  ')"

API_URL="https://api.cloudflare.com/client/v4/accounts/${RESOLVED_ACCOUNT_ID}/browser-rendering/markdown"
if [[ -n "$CACHE_TTL" ]]; then
  API_URL="${API_URL}?cacheTTL=${CACHE_TTL}"
fi

RESPONSE="$(curl -sS -X POST \
  "$API_URL" \
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
