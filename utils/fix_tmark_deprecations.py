#!/usr/bin/env python3
r"""Rewrite the four Python-Markdown spellings TMark reports as deprecated.

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

References
    ``[text][id]`` is Python-Markdown's reference-style link with no
    definition: brackets to every Markdown renderer, a link only because
    ``mkdocs-autorefs`` makes one of it. TMark reports ``deprecated:
    `[text][id]` is deprecated, write `[text](#id)``` and wants the
    canonical textual reference, which both media read — ``\hyperref`` in
    the book, an anchor on the page or a cross-page link on the site.

    The core's own fix reaches only what it resolves: a key that is a label
    of the *same file*, and a link text made of plain words (a text holding
    a code span — ``[`#include`][preprocessor-include]`` — is not read as a
    reference link at all, and lands in the PDF as literal brackets). The
    corpus is mostly the other two cases, so the rewrite here is textual and
    site-wide: every page is resolved once for its labels, and a
    ``[text][key]`` is rewritten only when *key* names a label somewhere
    under ``docs/``. That is what leaves ``matrice[3][4]`` and ``tab[i][j]``
    alone — their key is no label — and code spans are skipped as well.
    An empty text is kept empty: ``[](#id)`` is the number of the target
    (``\ref``), which is what ``La table [][anglisismes]`` asked for.

All four rewrites are textual and idempotent. The anchor and container ones
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
REFERENCE = re.compile(r"\[(?P<text>[^\[\]]*)\]\[(?P<key>[^\[\]]+)\]")
CODE_SPAN = re.compile(r"`[^`]*`")


def _attributes(spec: str) -> str:
    """``class="x" style="y"`` from pymdownx's ``[class='x' style='y']``."""
    parts = []
    for match in ATTRIBUTE.finditer(spec):
        value = match.group(3) if match.group(3) is not None else match.group(4)
        parts.append(f'{match.group(1)}="{value}"')
    return " ".join(parts)


def site_labels(root: Path) -> dict[str, list[str]]:
    """Every label declared under *root*, with the pages declaring it."""
    import tmark

    labels: dict[str, list[str]] = {}
    for path in sorted(root.rglob("*.md")):
        try:
            resolved = tmark.resolve(tmark.parse(path.read_text(encoding="utf-8")))
        except Exception as error:  # a page that does not parse declares nothing
            print(f"{path}: {error}", file=sys.stderr)
            continue
        for label in resolved["labels"]:
            labels.setdefault(label["id"], []).append(str(path))
    return labels


def _references(line: str, labels: dict[str, list[str]]) -> tuple[str, int]:
    """*line* with every ``[text][key]`` naming a known label made ``(#key)``."""
    spans = [span.span() for span in CODE_SPAN.finditer(line)]
    pieces: list[str] = []
    last = 0
    count = 0
    for match in REFERENCE.finditer(line):
        key = match.group("key")
        if key not in labels:
            continue
        if any(start <= match.start() < end for start, end in spans):
            continue
        pieces.append(line[last : match.start()])
        pieces.append(f"[{match.group('text')}](#{key})")
        last = match.end()
        count += 1
    pieces.append(line[last:])
    return "".join(pieces), count


def convert(
    text: str, labels: dict[str, list[str]] | None = None
) -> tuple[str, int, int, int, int]:
    """*text* rewritten, with the anchor, container, listing and reference counts."""
    lines = text.split("\n")
    out: list[str] = []
    fence: str | None = None
    open_blocks: list[str] = []
    anchors = 0
    containers = 0
    listings = 0
    references = 0
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
        if labels:
            rewritten, count = _references(rewritten, labels)
            references += count
        out.append(rewritten)
        index += 1
    return "\n".join(out), anchors, containers, listings, references


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
    parser.add_argument(
        "--no-references",
        action="store_true",
        help="skip the [text][id] rewrite, which resolves every page for its labels",
    )
    args = parser.parse_args(argv)

    paths = args.paths or sorted(args.docs.rglob("*.md"))
    labels = {} if args.no_references else site_labels(args.docs)
    total_anchors = 0
    total_containers = 0
    total_listings = 0
    total_references = 0
    total_files = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        converted, anchors, containers, listings, references = convert(text, labels)
        if not anchors and not containers and not listings and not references:
            continue
        total_anchors += anchors
        total_containers += containers
        total_listings += listings
        total_references += references
        total_files += 1
        print(
            f"{path}: {anchors} anchors, {containers} containers, "
            f"{listings} listings, {references} references"
        )
        if not args.check:
            path.write_text(converted, encoding="utf-8")
    verb = "would change" if args.check else "changed"
    print(
        f"{verb} {total_anchors} anchors, {total_containers} containers, "
        f"{total_listings} listings and {total_references} references "
        f"in {total_files} files"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
