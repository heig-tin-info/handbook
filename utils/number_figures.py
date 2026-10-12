#!/usr/bin/env python3
r"""Give the images that deserve a number a TMark figure caption.

``mkdocs-caption`` wrapped every ``<p>`` image of the site in a
``<figure>`` whose ``<figcaption>`` was the image's alt text. It was a
MkDocs plugin and Zensical runs none, so the web lost the wrapper; the
book never needed it, because TMark's LaTeX writer already promotes a
lone image paragraph to a ``figure`` float and captions it with the alt.

What both media read is the caption line of the syntax itself::

    ![Comparaison Harvard et Von Neumann](/assets/images/von-neumann-harvard.drawio)

    Figure: Comparaison Harvard et Von Neumann {#fig:von-neumann-harvard}

The line makes the float on the web — ``<figure>`` with a
``<figcaption>`` — and the ``{#fig:…}`` label is what gives it a number
there (``<span class="ts-caption-label">Figure N:</span>``); in the book
it becomes ``\caption[alt]{caption}\label{fig:…}``, so the figure keeps
the number LaTeX already gave it and gains an anchor and a line in the
list of figures.

Which images deserve one is ``mkdocs-caption``'s own rule, as
``mkdocs.yml`` configured it on ``master`` (``figure: {ignore_classes:
[nocaption]}``): an image alone in its paragraph, with a non-empty alt,
that is not marked ``nocaption``. Three restrictions come on top:

* the pages under ``docs/assets/`` are sources of other pages, not
  reading matter, and stay out;
* a link-wrapped image (``[![alt](img)](url)``) is not a figure for the
  web lowering, which promotes a paragraph made of one *image*; a caption
  line next to one would leak into the page as a paragraph;
* an image already carrying a caption line keeps it, and only gains the
  ``{#fig:…}`` it lacks.

The label is derived from the image's file name, so a rerun writes the
same one; an id already taken is suffixed. An image carrying an ``{#id}``
of its own hands it to its caption line, where the anchor belongs::

    python utils/number_figures.py            # caption docs/**/*.md
    python utils/number_figures.py --check    # report, change nothing
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import unicodedata

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
IMAGE = re.compile(
    r"^(?P<indent>\s*)!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?P<title>\s+\"[^\"]*\")?\)"
    r"(?P<attrs>\s*\{[^}]*\})?\s*$"
)
CAPTION = re.compile(r"^(?P<indent>\s*)Figure:\s*(?P<text>.*?)(?P<attrs>\s*\{[^}]*\})?\s*$")
IDENTIFIER = re.compile(r"#(?P<id>[^\s{}]+)")


def slugify(text: str) -> str:
    """``von-neumann-harvard`` from ``von-neumann-harvard.drawio``."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", ascii_text.lower())).strip("-")


def has_class(attrs: str, name: str) -> bool:
    """Whether an attribute list carries ``.name``."""
    return bool(re.search(rf"(?<![\w.]){re.escape('.' + name)}\b", attrs))


def identifier(attrs: str) -> str | None:
    """The ``#id`` of an attribute list, if it has one."""
    match = IDENTIFIER.search(attrs)
    return match.group("id") if match else None


def drop_identifier(attrs: str) -> str:
    """*attrs* without its ``#id``, emptied when nothing else is left."""
    rest = IDENTIFIER.sub("", attrs).strip().strip("{}").strip()
    return " {" + rest + "}" if rest else ""


def taken_ids(root: Path) -> set[str]:
    """Every ``{#…}`` identifier written under *root*."""
    found: set[str] = set()
    for path in sorted(root.rglob("*.md")):
        for attrs in re.findall(r"\{[^}]*\}", path.read_text(encoding="utf-8")):
            name = identifier(attrs)
            if name:
                found.add(name)
    return found


def reserve(stem: str, used: set[str]) -> str:
    """A ``fig:`` label derived from *stem* that nothing else claims."""
    base = f"fig:{slugify(stem) or 'figure'}"
    name = base
    index = 2
    while name in used:
        name = f"{base}-{index}"
        index += 1
    used.add(name)
    return name


def eligible(match: re.Match[str]) -> bool:
    """Whether an image paragraph is one ``mkdocs-caption`` would caption."""
    if not match.group("alt").strip():
        return False
    return not has_class(match.group("attrs") or "", "nocaption")


def opens_block(line: str) -> bool:
    """Whether *line* opens a container or a callout, so a paragraph follows."""
    return line.strip().startswith((":::", "!!!", "???"))


def alone(lines: list[str], index: int) -> bool:
    """Whether the image of ``lines[index]`` is the whole of its paragraph."""
    before = lines[index - 1] if index else ""
    after = lines[index + 1] if index + 1 < len(lines) else ""
    if index and before.strip() and not opens_block(before):
        return False
    return not after.strip() or after.strip() in {":::", "///"}


def convert(text: str, used: set[str]) -> tuple[str, int, int]:
    """*text* with its figures captioned, and the caption and label counts."""
    lines = text.split("\n")
    out: list[str] = []
    fence: str | None = None
    captions = 0
    labels = 0
    for index, line in enumerate(lines):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token[0] * 3
            elif token.startswith(fence):
                fence = None
            out.append(line)
            continue
        image = None if fence else IMAGE.match(line)
        if not image or not eligible(image) or not alone(lines, index):
            out.append(line)
            continue

        # A caption line is a paragraph of its own, so it is the line two
        # above the image or the line two below it.
        gap = index >= 2 and not lines[index - 1].strip()
        before = CAPTION.match(lines[index - 2]) if gap else None
        after = CAPTION.match(lines[index + 2]) if index + 2 < len(lines) else None
        own = identifier(image.group("attrs") or "")
        line = _without_own_id(line, image) if own else line
        if own:
            used.add(own)

        if before or after:
            # The caption is already there; what it lacks is the label
            # that numbers it. An image carrying an `{#id}` of its own
            # hands it over, so that one figure has one anchor.
            caption = before or after
            assert caption is not None
            out.append(line)
            if identifier(caption.group("attrs") or ""):
                continue
            name = own or reserve(Path(image.group("src")).stem, used)
            captioned = f"{caption.group('indent')}Figure: {caption.group('text')} {{#{name}}}"
            if before:
                out[-3] = captioned
            else:
                lines[index + 2] = captioned
            labels += 1
            continue

        name = own or reserve(Path(image.group("src")).stem, used)
        out.append(line)
        out.append("")
        out.append(f"{image.group('indent')}Figure: {image.group('alt')} {{#{name}}}")
        captions += 1
        labels += 1
    return "\n".join(out), captions, labels


def _without_own_id(line: str, image: re.Match[str]) -> str:
    """*line* with the image's ``{#id}`` removed: the caption carries it now."""
    attrs = image.group("attrs") or ""
    return line[: image.start("attrs")] + drop_identifier(attrs) if attrs else line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="files to convert")
    parser.add_argument("--docs", type=Path, default=Path("docs"), help="the documentation root")
    parser.add_argument("--check", action="store_true", help="report, change nothing")
    parser.add_argument(
        "--include-assets",
        action="store_true",
        help="caption the pages under docs/assets/ too",
    )
    args = parser.parse_args(argv)

    paths = args.paths or sorted(args.docs.rglob("*.md"))
    if not args.include_assets:
        assets = args.docs / "assets"
        paths = [path for path in paths if assets not in path.parents]
    used = taken_ids(args.docs)
    total_captions = 0
    total_labels = 0
    total_files = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        converted, captions, labels = convert(text, used)
        if not captions and not labels:
            continue
        total_captions += captions
        total_labels += labels
        total_files += 1
        print(f"{path}: {captions} captions, {labels} labels")
        if not args.check:
            path.write_text(converted, encoding="utf-8")
    verb = "would caption" if args.check else "captioned"
    print(f"{verb} {total_captions} images and labelled {total_labels} figures in {total_files} files")
    return 1 if args.check and total_labels else 0


if __name__ == "__main__":
    sys.exit(main())
