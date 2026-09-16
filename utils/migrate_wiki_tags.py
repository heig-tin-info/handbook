#!/usr/bin/env python3
r"""Rewrite the ``[[tag]]`` index markers of ``hooks/tags.py`` as TMark entries.

``hooks/tags.py`` reads four shapes, all of them a *visible text* plus an
*index entry*:

===========================  ==========  ==================================
source                       visible     index entry
===========================  ==========  ==================================
``[[Zig]]``                  ``Zig``     ``Zig``
``[[||void]]``               —           ``void``
``[[|heraldique]]``          —           ``heraldique``
``[[Mayenne|Mayenne, Duc]]`` ``Mayenne`` ``Mayenne, Duc``
``[[Shadocks||Shadocks,…]]`` ``Shadocks``  ``Shadocks,…``
``[[bit|bit|bit, le]]``      ``bit``     ``bit, le``
===========================  ==========  ==================================

so the entry is the last non-empty field and the visible text is the first
one. The hook also kebab-cased the middle field into a ``data-tag`` for
Material's search index; ``texsmith site search`` keys the entry itself, so
that normalisation disappears with the hook.

TMark's index entry is the ``#[term]`` shorthand of the ``index`` role: a
zero-width node (the whitespace around it collapses, and it vanishes before
punctuation), an ``\index{}`` entry in the PDF and a ``ts-index`` marker on
the web that ``texsmith site search`` collects. Because it is zero-width, the
visible half of a ``[[…]]`` has to be written out as ordinary text:

.. code-block:: md

    Le langage [[Zig]] est récent.      →  Le langage Zig #[Zig] est récent.
    …historique. [[||ordinateur]]       →  …historique. #[ordinateur]

Markers inside a fenced block or a code span are left alone, as the hook's
inline processor left them.

Usage::

    python utils/migrate_wiki_tags.py            # rewrite docs/**/*.md
    python utils/migrate_wiki_tags.py --check    # report, change nothing
    python utils/migrate_wiki_tags.py path.md …  # restrict to some files
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

TAG = re.compile(r"\[\[([^\]|]*)(?:\|([^\]]*?)(?:\|([^\]]+))?)?\]\]")
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)", re.DOTALL)


def replacement(match: re.Match[str]) -> str:
    """The TMark spelling of one ``[[…]]`` marker."""
    visible, tag, entry = (group or "" for group in match.groups())
    term = entry or tag or visible
    if not term:
        return match.group(0)
    return f"{visible} #[{term}]" if visible else f"#[{term}]"


def convert_line(line: str) -> str:
    """Rewrite the markers of *line* that sit outside a code span."""
    spans = [m.span() for m in CODE_SPAN.finditer(line)]

    def guarded(match: re.Match[str]) -> str:
        start, end = match.span()
        if any(a <= start and end <= b for a, b in spans):
            return match.group(0)
        return replacement(match)

    return TAG.sub(guarded, line)


def convert(text: str) -> tuple[str, int]:
    """Rewrite every marker of *text*; return the text and how many changed."""
    lines = text.split("\n")
    out: list[str] = []
    fence: str | None = None
    front_matter = lines and lines[0].strip() == "---"
    count = 0

    for index, line in enumerate(lines):
        if front_matter:
            out.append(line)
            if index and line.strip() in {"---", "..."}:
                front_matter = False
            continue

        if fence is not None:
            out.append(line)
            if line.strip().startswith(fence):
                fence = None
            continue

        if opening := FENCE.match(line):
            fence = opening.group(1)
            out.append(line)
            continue

        converted = convert_line(line)
        count += len(TAG.findall(line)) if converted != line else 0
        out.append(converted)

    return "\n".join(out), count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument(
        "--check", action="store_true", help="report the markers, change nothing"
    )
    parser.add_argument("--root", type=Path, default=Path("docs"))
    args = parser.parse_args(argv)

    paths = args.paths or sorted(args.root.rglob("*.md"))
    total = 0
    touched = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        converted, count = convert(text)
        if not count:
            continue
        total += count
        touched += 1
        print(f"{path}: {count} marker{'s' if count > 1 else ''}")
        if not args.check:
            path.write_text(converted, encoding="utf-8")

    verb = "would rewrite" if args.check else "rewrote"
    print(f"{verb} {total} markers in {touched} files")
    return 1 if (args.check and total) else 0


if __name__ == "__main__":
    sys.exit(main())
