# Changelog

All notable changes to this Home Assistant app are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version numbers match the upstream RemoteTerm for MeshCore release that the app packages.
A fourth number (e.g. `3.26.8.1`) marks a release with changes to this app only, on the same upstream release.
For changes to RemoteTerm itself, follow the upstream release linked in each entry.

## [Unreleased]

## [3.26.8] - 2026-11-12

### Added

- Fixes to this app can now ship between upstream releases as a four-part version (e.g. `3.26.8.1`), so Home Assistant offers them as an update.

### Changed

- **Upstream source moved to the [statico/remoteterm-meshcore](https://github.com/statico/remoteterm-meshcore) fork.** Development of the original [jkingsman/Remote-Terminal-for-MeshCore](https://github.com/jkingsman/Remote-Terminal-for-MeshCore) project is paused; the fork continues from its 3.17.1 release with the same configuration and data format. The app image is now built on `ghcr.io/statico/remoteterm-meshcore` instead of `docker.io/jkingsman/remoteterm-meshcore`.
- Track upstream RemoteTerm for MeshCore [3.26.8](https://github.com/statico/remoteterm-meshcore/releases/tag/3.26.8). This covers every upstream release from 3.18.0 to 3.26.8; see the [upstream changelog](https://github.com/statico/remoteterm-meshcore/blob/main/CHANGELOG.md) for details.
- **One-way database upgrade:** on first start, this version applies new database migrations to `/data/meshcore.db`. Older versions of the app cannot reliably read the upgraded database. Take a Home Assistant backup of this app before updating if you might want to roll back.
- The upstream image now runs on Python 3.14 (previously 3.12).

### Fixed

- Release images are now built from the upstream image tag matching the app version. Previously every build used the upstream `latest` image, so an app version could contain a different upstream release than its number suggested.
- Pushing changes to the app no longer silently rebuilds an already-released version's image. Previously, existing installs never received those changes and new installs got a different image under the same version number.
- Stopping the app no longer shows it as "error" in Home Assistant. The app shut down cleanly, but the start-up script exited with code 143 instead of the app's own exit code.
- The app no longer downloads upstream's development tools (about 17 MB) on every start, so it starts faster and doesn't need internet access to start.
- Stopping the app during its first minute now shuts RemoteTerm down cleanly too, and a crash during start-up is reported immediately instead of after 60 seconds.
- On iPhone, the empty band between the Home Assistant header and the RemoteTerm header is gone. RemoteTerm's padding for the iPhone status bar was also applied inside Home Assistant, which already accounts for it. Opening RemoteTerm directly or as an installed web app is unchanged.

## [3.17.1] - 2026-08-04

### Changed

- Track upstream RemoteTerm for MeshCore [3.17.1](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.17.1).

## [3.16.2] - 2026-07-17

### Changed

- Track upstream RemoteTerm for MeshCore [3.16.2](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.16.2).

## [3.16.0] - 2026-07-10

### Changed

- Track upstream RemoteTerm for MeshCore [3.16.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.16.0).

## [3.15.2] - 2026-06-25

### Changed

- Track upstream RemoteTerm for MeshCore [3.15.2](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.15.2).

## [3.15.0] - 2026-06-17

### Changed

- Track upstream RemoteTerm for MeshCore [3.15.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.15.0).

## [3.14.1] - 2026-06-03

### Changed

- Track upstream RemoteTerm for MeshCore [3.14.1](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.14.1).

## [3.14.0] - 2026-05-14

### Changed

- Track upstream RemoteTerm for MeshCore [3.14.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.14.0).

## [3.13.0] - 2026-05-01

### Changed

- Track upstream RemoteTerm for MeshCore [3.13.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.13.0).

## [3.12.3] - 2026-04-24

### Changed

- Track upstream RemoteTerm for MeshCore [3.12.3](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.12.3).

## [3.12.2] - 2026-04-22

### Changed

- Track upstream RemoteTerm for MeshCore [3.12.2](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.12.2).

## [3.12.1] - 2026-04-19

### Changed

- Track upstream RemoteTerm for MeshCore [3.12.1](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.12.1).

## [3.12.0] - 2026-04-17

### Changed

- Track upstream RemoteTerm for MeshCore [3.12.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.12.0).

## [3.11.3] - 2026-04-13

### Changed

- Track upstream RemoteTerm for MeshCore [3.11.3](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.11.3).

## [3.11.1] - 2026-04-12

### Changed

- Track upstream RemoteTerm for MeshCore [3.11.1](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.11.1).

## [3.11.0] - 2026-04-11

### Changed

- Track upstream RemoteTerm for MeshCore [3.11.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.11.0).

## [3.9.0] - 2026-04-07

### Changed

- Track upstream RemoteTerm for MeshCore [3.9.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.9.0).

## [3.8.0] - 2026-04-05

### Changed

- Track upstream RemoteTerm for MeshCore [3.8.0](https://github.com/jkingsman/Remote-Terminal-for-MeshCore/releases/tag/3.8.0), which adds:
  - Per-channel hop width override
  - Motion packet display on map
  - Map dark mode
  - Auto-resend for byte-perfect message transmission
  - RSSI/SNR attachment to received packets
  - Python 3.11+ requirement (handled by the upstream image)

## [1.0.0] - 2026-04-05

### Added

- Initial Home Assistant app release.
- Wraps the upstream `docker.io/jkingsman/remoteterm-meshcore` image.
- All `MESHCORE_*` environment variables configurable via app options.
- SQLite database persisted to `/data/meshcore.db`.
- Serial, TCP, and BLE connection modes supported.

[Unreleased]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.26.8...HEAD
[3.26.8]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.17.1...v3.26.8
[3.17.1]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.16.2...v3.17.1
[3.16.2]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.16.0...v3.16.2
[3.16.0]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.15.2...v3.16.0
[3.15.2]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.15.0...v3.15.2
[3.15.0]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.14.1...v3.15.0
[3.14.1]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.14.0...v3.14.1
[3.14.0]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.13.0...v3.14.0
[3.13.0]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.12.3...v3.13.0
[3.12.3]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.12.2...v3.12.3
[3.12.2]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.12.1...v3.12.2
[3.12.1]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.12.0...v3.12.1
[3.12.0]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.11.3...v3.12.0
[3.11.3]: https://github.com/bhaggs/ha-remoteterm-app/compare/v3.11.1...v3.11.3
[3.11.1]: https://github.com/bhaggs/ha-remoteterm-app/releases/tag/v3.11.1
