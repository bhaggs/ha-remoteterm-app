---
name: release
description: How this repo versions and releases its two Home Assistant apps — the production app (remoteterm/) and the experimental Dev app (remoteterm-dev/). Use when bumping a version, shipping an app-only fix, merging an upstream-update PR, editing remoteterm/CHANGELOG.md, writing or debugging release notes, triggering or troubleshooting the build/release workflows, or deciding whether a change goes to Dev or production first.
---

# Releasing the RemoteTerm Home Assistant apps

This repo publishes two Home Assistant apps built on the upstream RemoteTerm for MeshCore image (`ghcr.io/statico/remoteterm-meshcore`, a continuation of the paused `jkingsman/Remote-Terminal-for-MeshCore`). They are released in completely different ways:

| | Production — `remoteterm/` | Dev — `remoteterm-dev/` |
|---|---|---|
| Audience | Everyone | Testers only (`stage: experimental`) |
| Built on upstream | Release tag matching the app version | `:edge` (upstream `main`) |
| Version format | `X.Y.Z` or `X.Y.Z.N` | `YYYY.MM.DD.N`, stamped by CI |
| Who sets the version | A person (or the upstream-update PR) | The workflow, on every build |
| Changelog | `remoteterm/CHANGELOG.md` (shown in HA's update dialog) | None |
| Git tag and GitHub Release | `vX.Y.Z[.N]`, notes from the changelog | None |
| Image | `ghcr.io/bhaggs/ha-remoteterm-app/remoteterm-app` | `ghcr.io/bhaggs/ha-remoteterm-app/remoteterm-app-dev` |
| Workflow | `.github/workflows/build-publish.yml` | `.github/workflows/build-publish-dev.yml` |

Home Assistant only offers an update when the `version` in an app's `config.yaml` changes, so **a change reaches existing users only when the version is bumped.**

---

## Production versioning

The production version tracks the upstream release it packages:

- **`X.Y.Z`**: packages upstream release `X.Y.Z` with no app-only changes on top of it. Set automatically by the upstream-update PR.
- **`X.Y.Z.N`**: app-only revision `N` (starting at 1) of upstream `X.Y.Z`. It ships changes to `run.sh`, `config.yaml`, `Dockerfile` or docs without a new upstream release. Bump it by hand.
- The next upstream release drops the revision: `3.26.8` → `3.26.8.1` → `3.26.8.2` → `3.27.0`.

The build uses the first three parts as the upstream image tag, so `3.26.8.2` is built `FROM ghcr.io/statico/remoteterm-meshcore:3.26.8`.

**Never use `X.Y.Z-N`** (e.g. `3.26.8-1`). Home Assistant compares versions with AwesomeVersion, which reads a `-N` suffix as a semver *pre-release*. It ranks `3.26.8-1` *below* `3.26.8`, so the HA Updates page would not offer it, and `-10` would also sort below `-9`. The four-part form sorts correctly: `3.26.8 < 3.26.8.1 < 3.26.8.10 < 3.27.0`.

The build workflow rejects any other version format.

## Production changelog

`remoteterm/CHANGELOG.md` is the one changelog. Home Assistant shows it in the app's update dialog, and the GitHub release notes come from it. Its format is set by what HA needs, not by Keep a Changelog, though it borrows that standard's categories.

**Why the headings look the way they do.** The Supervisor reads `CHANGELOG.md` only from the app's own folder. HA trims it to the versions being installed only when each heading is exactly the bare version: the pattern is `^#* <version>\n`. A heading like `## [3.26.8] - 2026-11-12` never matches, and HA then shows the whole file. That happened with 3.26.8 at first. So:

```markdown
## Unreleased                  <- only while changes are pending

### Fixed

- ...

## 3.26.8

_Released 2026-11-12_

**Before updating:** ...       <- only when users must act first

### Changed

- ...
```

Rules:

- **Version headings are the bare version** (`## 3.26.8`), with `_Released YYYY-MM-DD_` on the next line, in the maintainer's local time (Pacific). Never put anything else on the heading line.
- **`## Unreleased` exists only while committed changes are waiting for a release.** Leave it out when nothing is pending. Add it above the newest version when you record the first change after a release. The bump script turns it into the new version's section.
- Every change to the app itself is recorded under `## Unreleased` **in the same PR as the change**, grouped under `### Added`, `### Changed`, `### Deprecated`, `### Removed`, `### Fixed` or `### Security`.
- Write entries for HA users rather than developers: say what changes for them, not which file changed. Call out anything that can't be undone, such as database migrations, in **bold**.
- Anything users must do *before* updating (backups, manual steps) goes in a bold **Before updating:** paragraph above the categories, so it leads both the HA dialog and the release notes.
- Changes to upstream RemoteTerm itself are not listed; each version's "Track upstream …" line links to the upstream release.
- Changes that affect only the Dev app don't belong here.
- `.github/scripts/bump_changelog.py` writes new version sections. Use it rather than writing them by hand.

**HA quirk:** HA shows everything from the new version's heading down to the first heading that *starts with* the installed version. Going from `3.26.8` straight to `3.27.0`, it stops at `## 3.26.8.1`, so that revision's notes don't appear in the dialog. They're still in the GitHub releases. Nothing in the heading format can avoid this.

## Production release notes

The `release` job in `build-publish.yml` builds the GitHub Release body from:

1. A line naming the upstream release it packages, e.g. "Packages upstream RemoteTerm for MeshCore 3.26.8".
2. The body of the version's `## X.Y.Z[.N]` section in `remoteterm/CHANGELOG.md`, copied word for word except the `_Released …_` line, since the GitHub release has its own date.

To fix release notes, edit the changelog *before* the version merges, or edit the GitHub Release by hand afterwards. Re-running the workflow does not regenerate the notes of a version that has already been released.

---

## Production release procedures

### A. Upstream release (automatic PR)

1. `update-upstream.yml` runs daily at 06:00 UTC, or can be started by hand. It compares the latest upstream release with the first three parts of `remoteterm/config.yaml`'s version.
2. If upstream is newer, it opens an `update/remoteterm-<version>` PR that:
   - sets `version:` to the upstream version, dropping any `.N` revision;
   - runs `bump_changelog.py --upstream …`, which adds a `## <version>` section (including any `Unreleased` entries) with the "Track upstream" line first under `### Changed`.
3. Before merging, read the upstream release notes. Look for:
   - new `MESHCORE_*` settings worth exposing as app options (`config.yaml` `options`/`schema`, `run.sh`, `DOCS.md`);
   - changes to the `/api/health`, `/api/fanout` or `mqtt_ha` behaviour that `run.sh` depends on;
   - database migrations or other changes that can't be undone, which deserve a bold note in the changelog.

   Add any of these to the PR branch, and add a changelog entry under the new version's section.
4. Merge. Production release then runs (see "What happens on merge").

When upstream releases faster than PRs get merged, close the stale bump PR. The next daily run opens one for the newest version.

### B. App-only release (`X.Y.Z.N`)

Use this to ship changes to the app itself without waiting for an upstream release.

1. Make sure the changes and their `## Unreleased` entries are already on `main`, or are part of this PR.
2. Pick the next revision: if the current version is `3.26.8`, use `3.26.8.1`; if it is `3.26.8.1`, use `3.26.8.2`.
3. Release the changelog:
   ```bash
   python3 .github/scripts/bump_changelog.py remoteterm/CHANGELOG.md 3.26.8.1 "$(TZ=America/Los_Angeles date +%Y-%m-%d)"
   ```
   Leave out `--upstream`; that is what makes it an app-only revision. The script stops if there is no `## Unreleased` section with entries.
4. Set `version: "3.26.8.1"` in `remoteterm/config.yaml`.
5. Open a PR titled e.g. `release: 3.26.8.1` and merge it.

### What happens on merge (both kinds)

A push to `main` that touches `remoteterm/Dockerfile`, `run.sh` or `config.yaml` runs `build-publish.yml`:

1. **prepare** reads the version and works out the upstream tag (first three parts). It checks whether tag `v<version>` already exists, and fails if `remoteterm/CHANGELOG.md` has no `## <version>` section for a new version.
2. **build-and-push** builds amd64 and arm64 images `FROM ghcr.io/statico/remoteterm-meshcore:<upstream>` and pushes `:<version>` and `:latest`.
3. **release** creates tag `v<version>` and the GitHub Release.

HA users see the update the next time the Supervisor refreshes the app store, or straight away after **Check for updates**.

**Already-released versions are never rebuilt by a push.** If you push changes to the app without bumping the version, the workflow posts a notice and skips the build. The changes wait in `## Unreleased` for the next release. Starting the workflow by hand (`workflow_dispatch`) does rebuild and overwrite an existing version's image, but creates no new release. Only do that to recover a broken build, such as an upstream image pulled after release. Users who already installed that version won't get the rebuilt image.

---

## Dev app

The Dev app is for trying upstream `main` and riskier changes to the app. It has no changelog, tags or GitHub Releases.

- **Upstream:** `FROM ghcr.io/statico/remoteterm-meshcore:edge`, which upstream rebuilds on every push to its `main`. The build always pulls a fresh `edge`.
- **Triggers:** a push to `main` touching `remoteterm-dev/Dockerfile`, `run.sh` or `config.yaml`, or starting `build-publish-dev.yml` by hand. It does **not** rebuild when upstream `edge` changes. Start it by hand to pick up the latest upstream `main`.
- **Versioning:** the workflow sets `YYYY.MM.DD.N` (UTC date, then `N` from 0 upwards) to the first value not already used as an image tag. It writes that into `remoteterm-dev/config.yaml` and commits `chore: stamp dev version …` to `main` as `github-actions[bot]`. Never edit the Dev version by hand.
  - If `main` moved during the build, the stamp commit fails to push, and the failure is ignored. The image is still published, but `config.yaml` on `main` then holds the previous version and HA won't offer the update. Start the workflow again to fix it.
  - Pull `main` after a Dev build, or your next push will conflict with the stamp commit.
- **Images:** `:<YYYY.MM.DD.N>` and `:latest`.

## Moving changes between Dev and production

`run.sh` is meant to stay **identical** in both apps, and so is everything in the two Dockerfiles below the `FROM` line. The two `config.yaml` files differ only in `name`, `version`, `slug`, `description`, `stage`, `image` and `panel_title`.

- **Risky runtime changes** (`run.sh`, start-up, signal handling, device access): change `remoteterm-dev/` first, run a Dev build, and test it on real hardware. Then copy the same change into `remoteterm/` with an `## Unreleased` entry, and ship it in an app-only or upstream release. Example: the SIGTERM fix went to Dev on 2026-05-22 and production on 2026-05-26.
- **Simple option or permission changes in `config.yaml`**, and docs: change both apps in the same commit.
- **Upstream changes:** Dev already runs upstream `main`, so it is where new upstream behaviour shows up first. Check it there before an upstream-update PR lands in production.
- After moving a change across, confirm the copies still match: `diff remoteterm/run.sh remoteterm-dev/run.sh` should print nothing.

## Checklist before merging a production release

- [ ] `config.yaml` version is `X.Y.Z` (upstream) or `X.Y.Z.N` (app-only), and higher than the current release.
- [ ] `remoteterm/CHANGELOG.md` has a bare `## <version>` heading with `_Released <date>_` below it, and no `## Unreleased` heading.
- [ ] For an upstream bump, the upstream image tag exists (`docker buildx imagetools inspect ghcr.io/statico/remoteterm-meshcore:<X.Y.Z>`).
- [ ] `remoteterm/run.sh` and `remoteterm-dev/run.sh` match, unless a change is deliberately being tried in Dev first.
- [ ] Anything users must act on, or that can't be undone, is in bold in the changelog and, if lasting, in `remoteterm/DOCS.md`.

## Troubleshooting

- **No upstream-update PRs for a while:** GitHub disables scheduled workflows after 60 days without repository activity. Check with `gh workflow list --all`; a state of `disabled_inactivity` on "Check upstream and update version" means it stopped. Re-enable it with `gh workflow enable update-upstream.yml`, then run it once with `gh workflow run update-upstream.yml`. This happened on 2026-10-11, 60 days after the last commit.
- **Pushed a fix but HA offers no update:** the version wasn't bumped, so the build was skipped (look for the notice in the workflow run). Do an app-only release.
- **`prepare` fails with "must be X.Y.Z or X.Y.Z.N":** `config.yaml` has some other format, e.g. `3.26.8-1`.
- **`prepare` fails with "has no '## [<version>]' section":** the version was bumped without releasing the changelog. Run `bump_changelog.py`.
- **Build fails pulling the base image:** the upstream tag doesn't exist. Upstream may not have published it yet, or the first three parts of the version are wrong.
- **Upstream-update PR wants to "downgrade" from `X.Y.Z.N` to `X.Y.Z`:** it shouldn't, because the check compares only the first three parts. If it happens, look at the `Get current app version` step in `update-upstream.yml`.
