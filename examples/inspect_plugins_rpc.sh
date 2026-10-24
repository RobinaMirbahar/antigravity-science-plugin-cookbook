#!/usr/bin/env bash
# Language Server RPC Inspector & Plugin Toggler for Google Antigravity
set -euo pipefail

: "${ANTIGRAVITY_LS_ADDRESS:=localhost:5387}"

lsrpc() {
  local method="$1"
  local body="${2:-{}}"
  curl -sS -X POST \
    "http://${ANTIGRAVITY_LS_ADDRESS}/exa.language_server_pb.LanguageServerService/${method}" \
    -H "Content-Type: application/json" \
    -H "x-codeium-csrf-token: ${ANTIGRAVITY_CSRF_TOKEN:-}" \
    -d "${body}"
}

echo "[*] Querying installed Antigravity plugins (filtered safely via jq)..."
lsrpc GetAllPlugins '{}' | jq '[.plugins[] | {
  name,
  dir: (.path | split("/") | last),
  disabled: (.disabled // false),
  skills: (.skills | length),
  mcp: [.mcpServers[]?.name]
}]'
