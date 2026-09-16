#!/usr/bin/env python3
r"""Turn the ``!!! exercise`` admonitions into numbered TMark callouts.

.. warning::

   **Do not apply this yet.** The rewrite is correct and the PDF renders it,
   but two TeXSmith defects make the *site* render it as literal text. See
   "What is missing" below; `NOTES-zensical.md` (Wave 2, H7) carries the same
   two items. The script reports by default and only writes with ``--apply``.

`mkdocs-plugin-exercises` numbers the exercises of a page in its
``on_page_content``, a hook Zensical has not got, so under Zensical the 123
blocks are plain, unnumbered admonitions. TMark numbers them on both media
instead, with a site-wide counter — declared under
``plugins.texsmith.declare.counters`` in ``mkdocs.yml`` —

.. code-block:: yaml

    declare:
      counters:
        ex: {name: Exercice, format: "Exercice {n}", scope: document}

printed in the callout's title:

.. code-block:: md

    !!! exercise "Mot du jour"       ::: exercise {title="#(ex:mot-du-jour) : Mot du jour"}
                                →
        Écrire un programme…         Écrire un programme…
                                     :::

The counter item has to sit in the title of a **container** callout, and the
container's kind has to be declared, which no site-wide option carries today,
so the script also writes into the front matter of every page that has an
exercise:

.. code-block:: yaml

    press:
      declare:
        admonitions:
          exercise: {name: Exercice}

## What is missing

1. ``texsmith.site.index`` parses a page's **body**
   (``SiteIndex.register`` / ``lower``: ``tmark.parse(padded)``) and attaches
   a front-matter node afterwards, so the parser never sees the page's own
   declarations. ``press.declare.admonitions`` is therefore invisible to it:
   ``::: exercise`` raises ``container-unknown`` and the lowering leaves the
   fence as literal text on the page. Parsing the whole page text, or
   re-parsing once the declarations are merged, is what the site path needs.
2. The ``!!!`` spelling — which needs no declaration, since the PyMdownX
   profile takes any word as a callout kind — cannot carry the counter
   either: ``tmark.lower_web`` splices a ``#(ex:key)`` written in a ``!!!``
   title at the start of the line instead of at the marker, and
   ``!!! exercise "#(ex:un) : T"`` lowers to
   ``<span class="ts-counter">Exercice 1</span>cise "#(ex:un) : T"``. The
   offsets of a node inside a `!!!` title look relative to the title rather
   than to the file.

Either one fixed is enough: with (1), run this script; with (2), the counter
can go in the ``!!!`` title and the sources barely move.

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
DECLARATION = """press:
  declare:
    admonitions:
      exercise: {name: Exercice}
"""


def slug(text: str) -> str:
    """A key made of ``[a-z0-9-]`` only."""
    folded = unicodedata.normalize("NFKD", text)
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", folded.lower())).strip("-")


def declare(text: str) -> str:
    """Add the ``exercise`` callout declaration to *text*'s front matter."""
    if re.search(r"^ *admonitions:", text[: text.find("\n---", 3) + 1], re.M):
        return text
    if text.startswith("---\n"):
        end = text.index("\n---", 3) + 1
        return text[:end] + DECLARATION + text[end:]
    return f"---\n{DECLARATION}---\n\n{text}"


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
        count += 1

    return "\n".join(out), count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the rewrite (broken on the site until the two defects "
        "documented in this file are fixed)",
    )
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
            path.write_text(declare(converted), encoding="utf-8")

    verb = "rewrote" if args.apply else "would rewrite"
    print(f"{verb} {total} exercises in {touched} files")
    return 0 if args.apply else 1


if __name__ == "__main__":
    sys.exit(main())
