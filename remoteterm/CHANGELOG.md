# Changelog

## 3.11.3

- Track upstream RemoteTerm for MeshCore 3.11.3
- See upstream [CHANGELOG](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/blob/main/CHANGELOG.md) for details


## 3.11.1

- Track upstream RemoteTerm for MeshCore 3.11.1
- See upstream [CHANGELOG](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/blob/main/CHANGELOG.md) for details


## 3.11.0

- Track upstream RemoteTerm for MeshCore 3.11.0
- See upstream [CHANGELOG](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/blob/main/CHANGELOG.md) for details


## 3.9.0

- Track upstream RemoteTerm for MeshCore 3.9.0
- See upstream [CHANGELOG](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/blob/main/CHANGELOG.md) for details


## 3.8.0

- Track upstream RemoteTerm for MeshCore 3.8.0 (2026-04-03)
- Per-channel hop width override
- Motion packet display on map
- Map dark mode
- Auto-resend for byte-perfect message transmission
- RSSI/SNR attachment to received packets
- Python 3.11+ now required (handled by upstream image)

## 1.0.0

- Initial Home Assistant app release
- Wraps upstream `docker.io/jkingsman/remoteterm-meshcore` image
- All `MESHCORE_*` environment variables configurable via app options
- SQLite database persisted to `/data/meshcore.db`
- Serial, TCP, and BLE connection modes supported
