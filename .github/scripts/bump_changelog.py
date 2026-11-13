#!/usr/bin/env python3
"""Release the [Unreleased] section of a Keep a Changelog file as a new version.

Upstream bump (run by .github/workflows/update-upstream.yml):
    bump_changelog.py CHANGELOG.md 3.27.0 2026-11-20 \\
        --upstream https://github.com/statico/remoteterm-meshcore \\
        --app-repo https://github.com/bhaggs/ha-remoteterm-app \\
        --ha-changelog remoteterm/CHANGELOG.md

App-only revision (run by hand, see .claude/skills/release/SKILL.md):
    bump_changelog.py CHANGELOG.md 3.26.8.1 2026-11-20 \\
        --app-repo https://github.com/bhaggs/ha-remoteterm-app \\
        --ha-changelog remoteterm/CHANGELOG.md

- Moves everything under "## [Unreleased]" into a new "## [VERSION] - DATE"
  section and removes the [Unreleased] heading. The heading only exists while
  there are committed changes waiting for a release; it may be absent.
- With --upstream, adds a "Track upstream ..." bullet as the first entry under
  "### Changed" (creating that subsection if needed).
- Without --upstream (app-only revision), refuses to run if [Unreleased] is
  empty, since there would be nothing to release.
- Orders subsections as Keep a Changelog lists them.
- Adds a compare link for the new version and drops any [Unreleased] link.
- With --ha-changelog, regenerates the Home Assistant copy of the changelog
  (see render_ha_changelog.py).
"""

import argparse
import re
import sys
from pathlib import Path

CATEGORY_ORDER = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("changelog")
    parser.add_argument("version", help="new app version, e.g. 3.27.0 or 3.26.8.1")
    parser.add_argument("date", help="release date, YYYY-MM-DD")
    parser.add_argument("--app-repo", required=True, help="https URL of this repository")
    parser.add_argument("--upstream", help="https URL of the upstream repo; omit for an app-only revision")
    parser.add_argument("--ha-changelog", help="path of the Home Assistant copy to regenerate, e.g. remoteterm/CHANGELOG.md")
    args = parser.parse_args()
    version = args.version

    text = Path(args.changelog).read_text()
    head, sep, rest = text.partition("## [Unreleased]\n")
    if sep:
        # Split the remainder into the unreleased body and everything after it.
        match = re.search(r"^## \[", rest, flags=re.M)
        unreleased = rest[: match.start()] if match else rest
        after = rest[match.start():] if match else ""
    else:
        # No [Unreleased] section: nothing pending; insert above the newest version.
        match = re.search(r"^## \[", text, flags=re.M)
        head = text[: match.start()] if match else text
        after = text[match.start():] if match else ""
        unreleased = ""

    # Split off the trailing link reference definitions.
    links_match = re.search(r"^\[[^\]]+\]: ", after, flags=re.M)
    older = after[: links_match.start()] if links_match else after
    links = after[links_match.start():] if links_match else ""

    prev_match = re.match(r"## \[([^\]]+)\]", older)
    prev_version = prev_match.group(1) if prev_match else None
    if prev_version == version:
        sys.exit(f"CHANGELOG already has a [{version}] section")

    # Parse unreleased subsections: {category: [lines]}. Text before the first
    # subsection (e.g. a "**Before updating:**" paragraph) is kept as a preamble.
    sections: dict[str, list[str]] = {}
    preamble: list[str] = []
    current = None
    for line in unreleased.splitlines():
        heading = re.match(r"^### (\w+)", line)
        if heading:
            current = heading.group(1)
            sections.setdefault(current, [])
        elif current and line.strip():
            sections[current].append(line)
        elif current is None:
            preamble.append(line)
    sections = {k: v for k, v in sections.items() if v}
    preamble_text = "\n".join(preamble).strip()

    if args.upstream:
        track_line = (
            f"- Track upstream RemoteTerm for MeshCore [{version}]({args.upstream}/releases/tag/{version}). "
            f"See the [upstream changelog]({args.upstream}/blob/main/CHANGELOG.md) for details."
        )
        sections.setdefault("Changed", []).insert(0, track_line)
    elif not sections and not preamble_text:
        sys.exit("Nothing to release: add a '## [Unreleased]' section with entries for the app-only changes first")

    ordered = [c for c in CATEGORY_ORDER if c in sections] + [
        c for c in sections if c not in CATEGORY_ORDER
    ]
    body = "".join(f"### {c}\n\n" + "\n".join(sections[c]) + "\n\n" for c in ordered)
    intro = f"{preamble_text}\n\n" if preamble_text else ""
    new_section = f"## [{version}] - {args.date}\n\n{intro}{body}"

    # Rebuild link references.
    app_repo = args.app_repo
    link_lines = [l for l in links.splitlines() if l.strip() and not l.startswith("[Unreleased]:")]
    new_link = (
        f"[{version}]: {app_repo}/compare/v{prev_version}...v{version}"
        if prev_version
        else f"[{version}]: {app_repo}/releases/tag/v{version}"
    )
    link_lines = [new_link, *link_lines]

    out = f"{head.rstrip()}\n\n{new_section}{older.rstrip()}\n\n" + "\n".join(link_lines) + "\n"
    Path(args.changelog).write_text(out)

    if args.ha_changelog:
        from render_ha_changelog import render  # same directory as this script

        Path(args.ha_changelog).write_text(render(out))


if __name__ == "__main__":
    main()
