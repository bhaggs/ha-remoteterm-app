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

[ -n "$SERIAL_PORT" ]     && export MESHCORE_SERIAL_PORT="$SERIAL_PORT"
[ -n "$SERIAL_BAUDRATE" ] && export MESHCORE_SERIAL_BAUDRATE="$SERIAL_BAUDRATE"
[ -n "$TCP_HOST" ]        && export MESHCORE_TCP_HOST="$TCP_HOST"
[ -n "$TCP_PORT" ]        && export MESHCORE_TCP_PORT="$TCP_PORT"
[ -n "$BLE_ADDRESS" ]     && export MESHCORE_BLE_ADDRESS="$BLE_ADDRESS"
[ -n "$BLE_PIN" ]         && export MESHCORE_BLE_PIN="$BLE_PIN"

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
[ -n "$AUTH_USER" ] && export MESHCORE_BASIC_AUTH_USERNAME="$AUTH_USER"
[ -n "$AUTH_PASS" ] && export MESHCORE_BASIC_AUTH_PASSWORD="$AUTH_PASS"

# ---------------------------------------------------------------------------
# Persist the database inside the HA /data volume so it survives restarts
# and app updates.
# ---------------------------------------------------------------------------
export MESHCORE_DATABASE_PATH="/data/meshcore.db"

# ---------------------------------------------------------------------------
# Fetch Mosquitto credentials from the HA Supervisor services API.
# This works automatically when the app declares `services: mqtt:want` and
# `hassio_api: true` in config.yaml — no user configuration needed.
# ---------------------------------------------------------------------------
MQTT_HOST=""
MQTT_PORT="1883"
MQTT_USER=""
MQTT_PASS=""

if [ -n "${SUPERVISOR_TOKEN:-}" ]; then
    MQTT_RESPONSE=$(curl -sf \
        -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
        http://supervisor/services/mqtt 2>/dev/null || true)

    if [ -n "$MQTT_RESPONSE" ]; then
        MQTT_HOST=$(echo "$MQTT_RESPONSE" | jq -r '.data.host // empty')
        MQTT_PORT=$(echo "$MQTT_RESPONSE" | jq -r '.data.port // 1883')
        MQTT_USER=$(echo "$MQTT_RESPONSE" | jq -r '.data.username // empty')
        MQTT_PASS=$(echo "$MQTT_RESPONSE" | jq -r '.data.password // empty')
    fi
fi

# ---------------------------------------------------------------------------
# Start the application in the background so we can bootstrap MQTT config
# ---------------------------------------------------------------------------
cd /app
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &
APP_PID=$!

# ---------------------------------------------------------------------------
# Wait for RemoteTerm to be ready (up to 60 seconds)
# ---------------------------------------------------------------------------
echo "Waiting for RemoteTerm to start..."
for i in $(seq 1 60); do
    if curl -sf http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "RemoteTerm is ready."
        break
    fi
    sleep 1
done

# ---------------------------------------------------------------------------
# Bootstrap the mqtt_ha fanout config on first run only.
# If a config already exists (including any manual changes made in the UI),
# it is left completely untouched — user settings are always preserved.
# ---------------------------------------------------------------------------
if [ -n "$MQTT_HOST" ]; then
    EXISTS=$(curl -sf http://localhost:8000/api/fanout 2>/dev/null \
        | jq '[.[] | select(.type == "mqtt_ha")] | length' 2>/dev/null || echo "0")

    if [ "${EXISTS}" -eq 0 ]; then
        echo "Configuring mqtt_ha fanout against ${MQTT_HOST}:${MQTT_PORT}..."
        curl -sf -X POST http://localhost:8000/api/fanout \
            -H "Content-Type: application/json" \
            -d "{
                \"type\": \"mqtt_ha\",
                \"name\": \"Home Assistant\",
                \"config\": {
                    \"broker_host\": \"${MQTT_HOST}\",
                    \"broker_port\": ${MQTT_PORT},
                    \"username\": \"${MQTT_USER}\",
                    \"password\": \"${MQTT_PASS}\"
                },
                \"scope\": {\"messages\": \"all\", \"raw_packets\": \"none\"},
                \"enabled\": true
            }" > /dev/null
        echo "mqtt_ha fanout configured — RemoteTerm will now publish entities to Home Assistant."
    else
        echo "mqtt_ha fanout already configured, skipping bootstrap."
    fi
else
    echo "Mosquitto not found via Supervisor API — configure MQTT manually in the RemoteTerm UI if needed."
fi

# ---------------------------------------------------------------------------
# Hand off to the app process
# ---------------------------------------------------------------------------
wait $APP_PID
