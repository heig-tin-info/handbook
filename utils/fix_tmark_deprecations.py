#!/usr/bin/env python3
"""Rewrite the two Python-Markdown spellings TMark reports as deprecated.

Anchors
    ``[](){#id}`` is Python-Markdown's: an empty link the ``attr_list``
    extension decorates with an ``id``. TMark reports ``deprecated:
    `[](){…}` is deprecated, write `[]{…}``` and wants an empty anonymous
    span carrying the attribute list. Both lower to ``<span id="…"></span>``.

Containers
    ``/// html | div[class='x']`` is ``pymdownx.blocks.html``'s container. Its
    body is Markdown, so TMark's advice, a ```` ```html ```` raw fence, does
    not apply: a raw fence would turn the body into literal text. The
    container that both a Python-Markdown site and TMark understand is
    ``<div class="x" markdown>`` … ``</div>``: ``md_in_html`` renders it on
    the site, and TMark keeps the body and drops the two tags in the PDF.

Both rewrites are textual, skip fenced code blocks, and are idempotent::

    python utils/fix_tmark_deprecations.py            # rewrite docs/**/*.md
    python utils/fix_tmark_deprecations.py --check    # report, change nothing

The third deprecation of this corpus, ``--8<-- "file"`` inside a fence, is
deliberately left alone: ``include="file"`` is spliced by the PDF pipeline
only, so converting it would empty every one of those listings on the site.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
ANCHOR = re.compile(r"\[\]\(\)\{\s*(#[^\s{}]+)\s*\}")
HTML_OPEN = re.compile(r"^(\s*)/// html \| (\w+)\[(.*)\]\s*$")
HTML_CLOSE = re.compile(r"^(\s*)///\s*$")
ATTRIBUTE = re.compile(r"""(\w+)=('([^']*)'|"([^"]*)")""")


def _attributes(spec: str) -> str:
    """``class="x" style="y"`` from pymdownx's ``[class='x' style='y']``."""
    parts = []
    for match in ATTRIBUTE.finditer(spec):
        value = match.group(3) if match.group(3) is not None else match.group(4)
        parts.append(f'{match.group(1)}="{value}"')
    return " ".join(parts)


def convert(text: str) -> tuple[str, int, int]:
    """Return *text* rewritten, with the anchor and container counts."""
    lines = text.split("\n")
    fence: str | None = None
    open_blocks: list[str] = []
    anchors = 0
    containers = 0
    for index, line in enumerate(lines):
        match = FENCE.match(line)
        if match:
            if fence is None:
                fence = match.group(1)[0] * 3
            elif line.strip().startswith(fence):
                fence = None
            continue
        if fence is not None:
            continue

        opening = HTML_OPEN.match(line)
        if opening:
            indent, tag, spec = opening.groups()
            attributes = _attributes(spec)
            head = f"<{tag} {attributes}".rstrip()
            lines[index] = f"{indent}{head} markdown>"
            open_blocks.append(f"{indent}</{tag}>")
            containers += 1
            continue
        if open_blocks and HTML_CLOSE.match(line):
            lines[index] = open_blocks.pop()
            continue

        rewritten, count = ANCHOR.subn(r"[]{\1}", line)
        if count:
            lines[index] = rewritten
            anchors += count
    return "\n".join(lines), anchors, containers


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="files to rewrite")
    parser.add_argument("--check", action="store_true", help="report only")
    parser.add_argument(
        "--docs", type=Path, default=Path("docs"), help="tree to walk by default"
    )
    args = parser.parse_args(argv)

    paths = args.paths or sorted(args.docs.rglob("*.md"))
    total_anchors = 0
    total_containers = 0
    total_files = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        converted, anchors, containers = convert(text)
        if not anchors and not containers:
            continue
        total_anchors += anchors
        total_containers += containers
        total_files += 1
        print(f"{path}: {anchors} anchors, {containers} containers")
        if not args.check:
            path.write_text(converted, encoding="utf-8")
    verb = "would change" if args.check else "changed"
    print(
        f"{verb} {total_anchors} anchors and {total_containers} containers "
        f"in {total_files} files"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
