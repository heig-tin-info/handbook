#!/usr/bin/env python3
"""Rewrite the three Python-Markdown spellings TMark reports as deprecated.

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

Listings
    A fence whose whole body is ``--8<-- "file"`` is ``pymdownx.snippets``
    splicing a file into a code block. TMark reports ``deprecated:
    `--8<-- "file" in a fence` is deprecated, write `include="file"``` and
    wants the path in the info string, which both media read: the site
    pre-pass resolves it against the page's directory, the ``--include-path``
    entries and the snippet base paths, and the book pass resolves it the
    same way. Wave 2 tried this conversion and put it back, because the site
    resolved the path from the wrong root and an unresolved include left the
    fence raw enough to swallow the paragraph after it. Both halves are
    fixed: TeXSmith searches the snippet base paths, and the core drops an
    ``include=`` it could not resolve from the lowered info string, so the
    worst case is an empty code block instead of a lost paragraph.

    Block-level ``--8<--`` outside a fence is left to ``pymdownx.snippets``,
    which the site still needs for ``auto_append``.

All three rewrites are textual and idempotent. The anchor and container ones
skip fenced code blocks; the listing one reads a fence, but rewrites it only
when its entire body is the include line::

    python utils/fix_tmark_deprecations.py            # rewrite docs/**/*.md
    python utils/fix_tmark_deprecations.py --check    # report, change nothing
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
SNIPPET = re.compile(r'^\s*--8<--\s+"(?P<path>[^"]+)"\s*$')
ANY_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def _attributes(spec: str) -> str:
    """``class="x" style="y"`` from pymdownx's ``[class='x' style='y']``."""
    parts = []
    for match in ATTRIBUTE.finditer(spec):
        value = match.group(3) if match.group(3) is not None else match.group(4)
        parts.append(f'{match.group(1)}="{value}"')
    return " ".join(parts)


def convert(text: str) -> tuple[str, int, int, int]:
    """Return *text* rewritten, with the anchor, container and listing counts."""
    lines = text.split("\n")
    out: list[str] = []
    fence: str | None = None
    open_blocks: list[str] = []
    anchors = 0
    containers = 0
    listings = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        marker = ANY_FENCE.match(line)
        if marker:
            ticks = marker.group(1)[0] * 3
            if fence is None:
                listing = _listing(lines, index, ticks)
                if listing is not None:
                    path, closing = listing
                    out.append(f'{line.rstrip()} include="{path}"')
                    out.append(lines[closing])
                    listings += 1
                    index = closing + 1
                    continue
                # Only a fence Python-Markdown itself would open — three
                # spaces of indentation at most — hides the two other
                # rewrites from this pass; a deeper one is a fence inside an
                # admonition, and its body holds nothing they read.
                if FENCE.match(line):
                    fence = ticks
            elif line.strip().startswith(fence):
                fence = None
            out.append(line)
            index += 1
            continue
        if fence is not None:
            out.append(line)
            index += 1
            continue

        opening = HTML_OPEN.match(line)
        if opening:
            indent, tag, spec = opening.groups()
            attributes = _attributes(spec)
            head = f"<{tag} {attributes}".rstrip()
            out.append(f"{indent}{head} markdown>")
            open_blocks.append(f"{indent}</{tag}>")
            containers += 1
            index += 1
            continue
        if open_blocks and HTML_CLOSE.match(line):
            out.append(open_blocks.pop())
            index += 1
            continue

        rewritten, count = ANCHOR.subn(r"[]{\1}", line)
        anchors += count
        out.append(rewritten)
        index += 1
    return "\n".join(out), anchors, containers, listings


def _listing(lines: list[str], index: int, ticks: str) -> tuple[str, int] | None:
    """The include path and closing index of a fence made of one ``--8<--``."""
    if index + 2 >= len(lines):
        return None
    snippet = SNIPPET.match(lines[index + 1])
    if snippet is None or not lines[index + 2].strip().startswith(ticks):
        return None
    return snippet.group("path"), index + 2


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
    total_listings = 0
    total_files = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        converted, anchors, containers, listings = convert(text)
        if not anchors and not containers and not listings:
            continue
        total_anchors += anchors
        total_containers += containers
        total_listings += listings
        total_files += 1
        print(f"{path}: {anchors} anchors, {containers} containers, {listings} listings")
        if not args.check:
            path.write_text(converted, encoding="utf-8")
    verb = "would change" if args.check else "changed"
    print(
        f"{verb} {total_anchors} anchors, {total_containers} containers and "
        f"{total_listings} listings in {total_files} files"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
