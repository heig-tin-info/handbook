#!/usr/bin/env python3
r"""Turn the ``!!! exercise`` admonitions into numbered TMark callouts.

`mkdocs-plugin-exercises` numbers the exercises of a page in its
``on_page_content``, a hook Zensical has not got, so under Zensical the 123
blocks are plain, unnumbered admonitions. TMark numbers them on both media
instead, with a site-wide counter, declared once under
``plugins.texsmith.declare`` in ``mkdocs.yml`` —

.. code-block:: yaml

    declare:
      counters:
        ex: {name: Exercice, format: "Exercice {n}", scope: document}
      admonitions:
        exercise: {name: Exercice}

— and printed in the callout's title:

.. code-block:: md

    !!! exercise "Mot du jour"       ::: exercise {title="#(ex:mot-du-jour) : Mot du jour"}
                                →
        Écrire un programme…         Écrire un programme…
                                     :::

The counter item has to sit in the title of a **container** callout, whose
kind has to be declared; both declarations are site-wide, so the pages carry
nothing but the rewrite itself. TeXSmith merges the site's ``declare`` under
each page's own ``press.declare`` before parsing, on the site path and the
book path alike — which is what wave 2 was missing, and why this script was
committed unapplied then.

Two things the ``exercises`` plugin did have no TMark equivalent and are lost
whatever this script does: the multiple-choice quizzes it built from a
``- [x]`` list, and the fill-in-the-blank inputs it built from ``{{word}}``.

The numbering is continuous over the whole corpus, where the plugin restarted
at 1 on every page.

Usage::

    python utils/number_exercises.py            # report, change nothing
    python utils/number_exercises.py --apply    # rewrite docs/**/*.md
    python utils/number_exercises.py path.md …  # restrict to some files
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import unicodedata

OPENING = re.compile(
    r'^(?P<fence>!!!|\?\?\?\+?) +exercise(?P<mods>(?: +[\w-]+)*?)'
    r'(?: +"(?P<title>[^"]*)")? *$'
)

def slug(text: str) -> str:
    """A key made of ``[a-z0-9-]`` only."""
    folded = unicodedata.normalize("NFKD", text)
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", folded.lower())).strip("-")


def convert(text: str, keys: dict[str, str], stem: str) -> tuple[str, int]:
    """Rewrite every exercise block of *text*; return the text and how many."""
    lines = text.split("\n")
    out: list[str] = []
    index = 0
    count = 0

    while index < len(lines):
        opening = OPENING.match(lines[index])
        if opening is None:
            out.append(lines[index])
            index += 1
            continue

        body: list[str] = []
        index += 1
        while index < len(lines):
            line = lines[index]
            if line.strip() and not line.startswith("    "):
                break
            body.append(line[4:] if line.startswith("    ") else line)
            index += 1
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()

        title = (opening.group("title") or "").strip()
        key = base = slug(title) or f"{stem}-{count + 1}"
        suffix = 1
        while key in keys:
            suffix += 1
            key = f"{base}-{suffix}"
        keys[key] = title

        label = f"#(ex:{key}) : {title}" if title else f"#(ex:{key})"
        attributes = [f'title="{label}"']
        attributes += [f".{mod}" for mod in opening.group("mods").split()]
        if opening.group("fence").startswith("???"):
            attributes.append("collapsed=true")

        out.append(f"::: exercise {{{' '.join(attributes)}}}")
        out.extend(body)
        out.append(":::")
        # The admonition ended where its indentation did, so the line after
        # it may sit right against the closing marker.
        if index < len(lines) and lines[index].strip():
            out.append("")
        count += 1

    return "\n".join(out), count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--apply", action="store_true", help="write the rewrite")
    parser.add_argument("--root", type=Path, default=Path("docs"))
    args = parser.parse_args(argv)

    paths = args.paths or sorted(args.root.rglob("*.md"))
    keys: dict[str, str] = {}
    total = 0
    touched = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        stem = slug(str(path.with_suffix("")).replace(str(args.root), "", 1))
        converted, count = convert(text, keys, stem)
        if not count:
            continue
        total += count
        touched += 1
        print(f"{path}: {count} exercise{'s' if count > 1 else ''}")
        if args.apply:
            path.write_text(converted, encoding="utf-8")

    verb = "rewrote" if args.apply else "would rewrite"
    print(f"{verb} {total} exercises in {touched} files")
    return 0 if args.apply else 1


if __name__ == "__main__":
    sys.exit(main())
