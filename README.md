# ha-remoteterm-app

A Home Assistant app repository for [RemoteTerm for MeshCore](https://github.com/statico/remoteterm-meshcore) — a web-based terminal and management interface for MeshCore mesh radio networks.

> **Upstream source:** Development of the original [jkingsman/Remote-Terminal-for-MeshCore](https://github.com/jkingsman/Remote-Terminal-for-MeshCore) project is paused. Starting with app version 3.26.8, this app packages the [statico/remoteterm-meshcore](https://github.com/statico/remoteterm-meshcore) fork, which continues from the original's 3.17.1 release. Updating from 3.17.1 upgrades the RemoteTerm database, and the upgrade can't be undone, so back up the app before updating if you might want to roll back. See the [changelog](remoteterm/CHANGELOG.md).

## Installation

1. In Home Assistant, go to **Settings → Apps → App Store**.
2. Click the menu (⋮) in the top right and choose **Repositories**.
3. Add this repository URL:
   ```
   https://github.com/bhaggs/ha-remoteterm-app
   ```
4. Find **RemoteTerm for MeshCore** in the store and click **Install**.
5. Configure your radio connection in the app options, then click **Start**.

## Radio connection

RemoteTerm supports three ways to connect to a radio device. **TCP and serial are the recommended options** when running inside Home Assistant.

| Method | Recommended | Notes |
|--------|-------------|-------|
| Serial (USB) | ✅ Yes | Plug your radio into the HA host via USB and set `serial_port` (e.g. `/dev/ttyUSB0`), or leave it blank for auto-detection. |
| TCP | ✅ Yes | Set `tcp_host` and `tcp_port` to connect to a radio accessible over the network. No hardware passthrough needed. |
| BLE | ⚠️ Best-effort | BLE in Docker is inherently fragile. The app requests host Bluetooth access, but depending on your hardware and host configuration it may not work reliably. TCP or serial are strongly preferred. |

## Home Assistant MQTT integration

If you have the [Mosquitto broker app](https://github.com/home-assistant/addons/tree/master/mosquitto) installed, RemoteTerm will automatically connect to it on first start and create mesh network devices and sensors in Home Assistant — no manual MQTT configuration needed. The app detects Mosquitto via the HA Supervisor and wires itself up automatically.

For full details on the entities created and how to configure them, see the [upstream MQTT integration documentation](https://github.com/statico/remoteterm-meshcore/blob/main/README_HA.md).

If Mosquitto is not installed, RemoteTerm works as normal — MQTT is entirely optional.

## Bot file output and shared storage

RemoteTerm bots can write files to `/share` inside the container, which maps to the Home Assistant shared volume (`/share` on the host). This volume is accessible to all HA add-ons, making it a convenient place to write log files or data that other add-ons or automations can read.

For example, a bot script can write to `/share/remoteterm/my-bot.log` and the file will be visible in the HA file system.

## External access via reverse proxy

By default, RemoteTerm is only accessible through the Home Assistant sidebar via ingress. If you want to expose it on your network or through your own reverse proxy (e.g. Nginx, Traefik, Cloudflare Tunnel), you can map port 8000 in the add-on's **Network** settings.

In the add-on UI, go to the **Network** tab and set the host port for **8000/tcp** to any available port on your HA host (e.g. `8000`). RemoteTerm will then be reachable at `http://<ha-host>:<port>` in addition to the sidebar. Leave the field blank to keep it inaccessible from outside HA.

Sidebar access via ingress continues to work regardless of whether a host port is set.

> **Note:** Exposing the port bypasses HA authentication. If you use this option, enable RemoteTerm's built-in basic auth (via the `basic_auth_username` and `basic_auth_password` options) or protect the endpoint with your reverse proxy.

## Architecture

This app wraps the upstream `ghcr.io/statico/remoteterm-meshcore` Docker image with a thin Home Assistant integration layer:

- The [Dockerfile](remoteterm/Dockerfile) uses the upstream image as its base. Each app release is built on the upstream image tag that matches its version.
- The [run.sh](remoteterm/run.sh) translates Home Assistant app options into `MESHCORE_*` environment variables consumed by the app.
- The SQLite database is stored in the app's persistent `/data` volume so it survives restarts and updates.

## Issues and feature requests

This repository only maintains the Home Assistant app packaging. For bugs or feature requests related to RemoteTerm itself — the UI, radio connectivity, messaging, bots, etc. — please open an issue in the [upstream repository](https://github.com/statico/remoteterm-meshcore/issues). Issues specific to the HA app wrapper (installation, sidebar access, options not applying, etc.) can be filed here.

## Keeping up with upstream

A [GitHub Actions workflow](.github/workflows/update-upstream.yml) checks for new RemoteTerm upstream releases daily and opens a pull request when one is found. Merging the PR bumps the app version — no manual tracking required.

## Versioning and releases

The app version matches the upstream RemoteTerm release it packages (e.g. `3.26.8`). Fixes to the app itself that ship between upstream releases get a fourth number (`3.26.8.1`, `3.26.8.2`, …), which resets at the next upstream release. The Dev app uses date-based versions (`2026.11.12.0`) set automatically on each build.

The app's [CHANGELOG](remoteterm/CHANGELOG.md) follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and each GitHub release's notes are taken from it. For the full release process, see the [release skill](.claude/skills/release/SKILL.md).

## Apps in this repository

| App | Description |
|-----|-------------|
| [RemoteTerm for MeshCore](remoteterm/) | Web terminal for MeshCore mesh radio networks |
| [RemoteTerm for MeshCore (Dev)](remoteterm-dev/) | Experimental build on upstream's `edge` image (latest `main`) — for testing only |

---

> **Note:** This app was built with the assistance of [Claude Code](https://claude.ai/code). While the generated code has been reviewed, AI-assisted output can contain errors or omissions. Review all configuration, scripts, and workflows before deploying in your environment, and exercise the usual caution when running third-party apps with access to your Home Assistant instance or serial devices.
