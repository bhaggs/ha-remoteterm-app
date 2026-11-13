#!/usr/bin/env python3
"""Add a released version to remoteterm/CHANGELOG.md.

Upstream bump (run by .github/workflows/update-upstream.yml):
    bump_changelog.py remoteterm/CHANGELOG.md 3.27.0 2026-11-20 \\
        --upstream https://github.com/statico/remoteterm-meshcore

App-only revision (run by hand, see .claude/skills/release/SKILL.md):
    bump_changelog.py remoteterm/CHANGELOG.md 3.26.8.1 2026-11-20

Format (what Home Assistant needs): the Supervisor shows this file in the
app's update dialog, and Home Assistant trims it to the versions being
installed only when each version heading is exactly the bare version, so:

    ## 3.26.8

    _Released 2026-11-12_

    **Before updating:** ...   (optional)

    ### Changed
    - ...

What the script does:
- Moves the entries under "## Unreleased" (which only exists while changes are
  pending) into a new "## VERSION" section above the newest version, and
  removes the Unreleased heading.
- With --upstream, adds a "Track upstream ..." bullet as the first entry under
  "### Changed".
- Without --upstream (app-only revision), refuses to run if nothing is pending.
- Keeps text above the first ### category (e.g. a "**Before updating:**"
  paragraph) and orders categories Added, Changed, Deprecated, Removed, Fixed,
  Security.
"""

import argparse
import re
import sys
from pathlib import Path

CATEGORY_ORDER = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
UNRELEASED = re.compile(r"^## Unreleased[ \t]*\n", re.M)
VERSION_HEADING = re.compile(r"^## ", re.M)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("changelog")
    parser.add_argument("version", help="new app version, e.g. 3.27.0 or 3.26.8.1")
    parser.add_argument("date", help="release date, YYYY-MM-DD (Pacific time)")
    parser.add_argument("--upstream", help="https URL of the upstream repo; omit for an app-only revision")
    args = parser.parse_args()
    version = args.version

    text = Path(args.changelog).read_text()
    if re.search(rf"^## {re.escape(version)}[ \t]*$", text, flags=re.M):
        sys.exit(f"CHANGELOG already has a '## {version}' section")

    # Take out the Unreleased section, if there is one.
    unreleased = ""
    match = UNRELEASED.search(text)
    if match:
        nxt = VERSION_HEADING.search(text, match.end())
        end = nxt.start() if nxt else len(text)
        unreleased = text[match.end():end]
        text = text[: match.start()] + text[end:]

    # Parse it: text before the first ### category is kept as a preamble.
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
        sys.exit("Nothing to release: add a '## Unreleased' section with entries for the app-only changes first")

    ordered = [c for c in CATEGORY_ORDER if c in sections] + [c for c in sections if c not in CATEGORY_ORDER]
    body = "\n\n".join(f"### {c}\n\n" + "\n".join(sections[c]) for c in ordered)
    intro = f"{preamble_text}\n\n" if preamble_text else ""
    new_section = f"## {version}\n\n_Released {args.date}_\n\n{intro}{body}\n\n"

    # Insert above the newest released version (or at the end).
    first = VERSION_HEADING.search(text)
    if first:
        out = text[: first.start()].rstrip() + "\n\n" + new_section + text[first.start():]
    else:
        out = text.rstrip() + "\n\n" + new_section
    Path(args.changelog).write_text(out.rstrip() + "\n")


if __name__ == "__main__":
    main()
