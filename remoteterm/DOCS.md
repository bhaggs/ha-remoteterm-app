# RemoteTerm for MeshCore

A Home Assistant app that runs [RemoteTerm for MeshCore](https://github.com/statico/remoteterm-meshcore) — a web-based terminal and management interface for MeshCore mesh radio networks.

Once started, RemoteTerm appears in the Home Assistant sidebar for one-click access. All traffic is routed through HA's ingress proxy — no port is exposed externally.

> **Security notice:** RemoteTerm is designed for trusted networks only. The bot system executes arbitrary Python code. If this app is exposed beyond your local network, enable Basic Auth and consider `disable_bots: true`.

---

## Radio connection

Exactly **one** connection method must be configured at a time.

### Serial (USB)

Connect your radio via USB. Set `serial_port` to the device path, e.g. `/dev/ttyUSB0`.  
Leave `serial_port` empty to let RemoteTerm auto-detect the device.

Any USB serial device on the host (e.g. `/dev/ttyUSB0`, `/dev/ttyACM5`) is automatically accessible to the app — set `serial_port` to whatever path your radio actually enumerates as.

### TCP (network)

Set `tcp_host` to the IP address of the remote radio host and `tcp_port` to its port (default `5000`). Leave `serial_port`, `ble_address`, and `ble_pin` empty.

### Bluetooth LE

Set `ble_address` (e.g. `AA:BB:CC:DD:EE:FF`) and `ble_pin`. This app requests host Bluetooth access, but BLE in Docker is inherently fragile and may require additional host-side configuration to work. TCP or serial are recommended over BLE where possible.

---

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `serial_port` | _(auto)_ | Serial device path. Empty = auto-detect. |
| `serial_baudrate` | `115200` | Serial baud rate. |
| `tcp_host` | _(none)_ | TCP host for remote radio. |
| `tcp_port` | `5000` | TCP port for remote radio. |
| `ble_address` | _(none)_ | BLE device MAC address. |
| `ble_pin` | _(none)_ | BLE PIN (required when `ble_address` is set). |
| `log_level` | `INFO` | Log verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |
| `disable_bots` | `false` | Disable the Python bot/agent system. |
| `basic_auth_username` | _(none)_ | Username for HTTP Basic Auth. |
| `basic_auth_password` | _(none)_ | Password for HTTP Basic Auth. Both must be set together. |
| `enable_message_poll_fallback` | `false` | Enable fallback message polling. |
| `force_channel_slot_reconfigure` | `false` | Force channel slot reconfiguration on connect. |
| `skip_post_connect_sync` | `false` | Skip post-connection radio sync. |

---

## Data persistence

The SQLite database is stored at `/data/meshcore.db` inside the app's persistent data volume. It survives restarts and app updates.

---

## Updating

This app tracks upstream RemoteTerm releases. When a new version is published, update from the **Settings → Apps** page. The app version number matches the upstream RemoteTerm release it packages. A fourth number (e.g. `3.26.8.1`) means an update to this app only, on the same upstream release.

Upstream releases may include database migrations, which run automatically on first start and can't be undone. If you might want to roll back to an older version, take a backup of this app first (**Settings → System → Backups**) and restore it to roll back.

### Upstream source

Development of the original [jkingsman/Remote-Terminal-for-MeshCore](https://github.com/jkingsman/Remote-Terminal-for-MeshCore) project is paused. Starting with app version 3.26.8, this app packages the [statico/remoteterm-meshcore](https://github.com/statico/remoteterm-meshcore) fork, which continues from the original's 3.17.1 release. Your options, radio settings and message history carry over unchanged.
