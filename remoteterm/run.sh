#!/bin/bash
set -euo pipefail

OPTIONS="/data/options.json"

# Helper: read a string option; emit nothing if null or empty
get_str() { jq -r ".$1 // empty" "$OPTIONS"; }

# Helper: read a value that must always be present (numbers, bools)
get_val() { jq -r ".$1" "$OPTIONS"; }

# ---------------------------------------------------------------------------
# Connection settings — only export non-empty values so the app's own
# auto-detection logic (e.g. serial auto-scan) fires when fields are blank.
# ---------------------------------------------------------------------------
SERIAL_PORT=$(get_str serial_port)
SERIAL_BAUDRATE=$(get_val serial_baudrate)
TCP_HOST=$(get_str tcp_host)
TCP_PORT=$(get_val tcp_port)
BLE_ADDRESS=$(get_str ble_address)
BLE_PIN=$(get_str ble_pin)

[ -n "$SERIAL_PORT" ]   && export MESHCORE_SERIAL_PORT="$SERIAL_PORT"
[ -n "$SERIAL_BAUDRATE" ] && export MESHCORE_SERIAL_BAUDRATE="$SERIAL_BAUDRATE"
[ -n "$TCP_HOST" ]      && export MESHCORE_TCP_HOST="$TCP_HOST"
[ -n "$TCP_PORT" ]      && export MESHCORE_TCP_PORT="$TCP_PORT"
[ -n "$BLE_ADDRESS" ]   && export MESHCORE_BLE_ADDRESS="$BLE_ADDRESS"
[ -n "$BLE_PIN" ]       && export MESHCORE_BLE_PIN="$BLE_PIN"

# ---------------------------------------------------------------------------
# General settings
# ---------------------------------------------------------------------------
export MESHCORE_LOG_LEVEL="$(get_val log_level)"
export MESHCORE_DISABLE_BOTS="$(get_val disable_bots)"
export MESHCORE_ENABLE_MESSAGE_POLL_FALLBACK="$(get_val enable_message_poll_fallback)"
export MESHCORE_FORCE_CHANNEL_SLOT_RECONFIGURE="$(get_val force_channel_slot_reconfigure)"
export MESHCORE_SKIP_POST_CONNECT_SYNC="$(get_val skip_post_connect_sync)"

# ---------------------------------------------------------------------------
# Auth (both must be set together or neither)
# ---------------------------------------------------------------------------
AUTH_USER=$(get_str basic_auth_username)
AUTH_PASS=$(get_str basic_auth_password)
[ -n "$AUTH_USER" ]  && export MESHCORE_BASIC_AUTH_USERNAME="$AUTH_USER"
[ -n "$AUTH_PASS" ]  && export MESHCORE_BASIC_AUTH_PASSWORD="$AUTH_PASS"

# ---------------------------------------------------------------------------
# Persist the database inside the HA /data volume so it survives restarts
# and app updates.
# ---------------------------------------------------------------------------
export MESHCORE_DATABASE_PATH="/data/meshcore.db"

# ---------------------------------------------------------------------------
# Start the application
# ---------------------------------------------------------------------------
cd /app
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
