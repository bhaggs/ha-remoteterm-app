# Changelog

All notable changes to this Home Assistant app are documented in this file.

Version numbers match the upstream RemoteTerm for MeshCore release that the app packages.
A fourth number (e.g. `3.26.8.1`) marks a release with changes to this app only, on the same upstream release.
For changes to RemoteTerm itself, follow the upstream release linked in each entry.

## 3.26.9

_Released 2026-11-12_

### Changed

- Track upstream RemoteTerm for MeshCore [3.26.9](https://github.com/statico/remoteterm-meshcore/releases/tag/3.26.9). See the [upstream changelog](https://github.com/statico/remoteterm-meshcore/blob/main/CHANGELOG.md) for details.
- The iPhone header fix from 3.26.8 now comes from upstream RemoteTerm itself, so this app no longer modifies RemoteTerm's web page. Nothing changes in how it looks.

## 3.26.8

_Released 2026-11-12_

**Before updating:** this version upgrades the RemoteTerm database, and the upgrade can't be undone. If you might want to roll back, take a Home Assistant backup of this app first (**Settings → System → Backups**).

### Changed

- **Upstream source moved to the [statico/remoteterm-meshcore](https://github.com/statico/remoteterm-meshcore) fork.** Development of the original [jkingsman/Remote-Terminal-for-MeshCore](https://github.com/jkingsman/Remote-Terminal-for-MeshCore) project is paused; the fork continues from its 3.17.1 release with the same configuration and data format. The app image is now built on `ghcr.io/statico/remoteterm-meshcore` instead of `docker.io/jkingsman/remoteterm-meshcore`.
- Track upstream RemoteTerm for MeshCore [3.26.8](https://github.com/statico/remoteterm-meshcore/releases/tag/3.26.8). This covers every upstream release from 3.18.0 to 3.26.8; see the [upstream changelog](https://github.com/statico/remoteterm-meshcore/blob/main/CHANGELOG.md) for details.
- The upstream image now runs on Python 3.14 (previously 3.12).
- Each update now contains exactly the upstream release named in its version number. Fixes to this app between upstream releases get a fourth number (e.g. `3.26.8.1`) so Home Assistant offers them as updates.

### Fixed

- Stopping the app no longer shows it as "error" in Home Assistant. RemoteTerm shut down cleanly, but its web server deliberately ends with the stop signal's exit code (143), and the start-up script passed that on to Home Assistant as a failure. A real crash is still reported as an error.
- The app no longer downloads upstream's development tools (about 17 MB) on every start, so it starts faster and doesn't need internet access to start.
- Stopping the app during its first minute now shuts RemoteTerm down cleanly too, and a crash during start-up is reported immediately instead of after 60 seconds.
- On iPhone, the empty band between the Home Assistant header and the RemoteTerm header is gone. RemoteTerm's padding for the iPhone status bar was also applied inside Home Assistant, which already accounts for it. Opening RemoteTerm directly or as an installed web app is unchanged.

## 3.17.1

_Released 2026-08-04_

### Changed

- Track upstream RemoteTerm for MeshCore [3.17.1](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.17.1).

## 3.16.2

_Released 2026-07-17_

### Changed

- Track upstream RemoteTerm for MeshCore [3.16.2](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.16.2).

## 3.16.0

_Released 2026-07-10_

### Changed

- Track upstream RemoteTerm for MeshCore [3.16.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.16.0).

## 3.15.2

_Released 2026-06-25_

### Changed

- Track upstream RemoteTerm for MeshCore [3.15.2](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.15.2).

## 3.15.0

_Released 2026-06-17_

### Changed

- Track upstream RemoteTerm for MeshCore [3.15.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.15.0).

## 3.14.1

_Released 2026-06-03_

### Changed

- Track upstream RemoteTerm for MeshCore [3.14.1](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.14.1).

## 3.14.0

_Released 2026-05-14_

### Changed

- Track upstream RemoteTerm for MeshCore [3.14.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.14.0).

## 3.13.0

_Released 2026-05-01_

### Changed

- Track upstream RemoteTerm for MeshCore [3.13.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.13.0).

## 3.12.3

_Released 2026-04-24_

### Changed

- Track upstream RemoteTerm for MeshCore [3.12.3](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.12.3).

## 3.12.2

_Released 2026-04-22_

### Changed

- Track upstream RemoteTerm for MeshCore [3.12.2](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.12.2).

## 3.12.1

_Released 2026-04-19_

### Changed

- Track upstream RemoteTerm for MeshCore [3.12.1](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.12.1).

## 3.12.0

_Released 2026-04-17_

### Changed

- Track upstream RemoteTerm for MeshCore [3.12.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.12.0).

## 3.11.3

_Released 2026-04-13_

### Changed

- Track upstream RemoteTerm for MeshCore [3.11.3](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.11.3).

## 3.11.1

_Released 2026-04-12_

### Changed

- Track upstream RemoteTerm for MeshCore [3.11.1](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.11.1).

## 3.11.0

_Released 2026-04-11_

### Changed

- Track upstream RemoteTerm for MeshCore [3.11.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.11.0).

## 3.9.0

_Released 2026-04-07_

### Changed

- Track upstream RemoteTerm for MeshCore [3.9.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.9.0).

## 3.8.0

_Released 2026-04-05_

### Changed

- Track upstream RemoteTerm for MeshCore [3.8.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.8.0), which adds:
  - Per-channel hop width override
  - Motion packet display on map
  - Map dark mode
  - Auto-resend for byte-perfect message transmission
  - RSSI/SNR attachment to received packets
  - Python 3.11+ requirement (handled by the upstream image)

## 1.0.0

_Released 2026-04-05_

### Added

- Initial Home Assistant app release.
- Wraps the upstream `docker.io/jkingsman/remoteterm-meshcore` image.
- All `MESHCORE_*` environment variables configurable via app options.
- SQLite database persisted to `/data/meshcore.db`.
- Serial, TCP, and BLE connection modes supported.
