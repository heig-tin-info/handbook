"""Wrap Mermaid diagrams with figures when a title comment is present."""

from __future__ import annotations

import re

from bs4 import BeautifulSoup, Tag
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

TITLE_PATTERN = re.compile(r"^%%\s*(.+)$", re.MULTILINE)


def on_page_content(
    html: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Convert Mermaid ``pre`` blocks to figures when a title is provided."""

    del page, config, files

    soup = BeautifulSoup(html, "html.parser")
    for block in soup.find_all("pre", class_="mermaid"):
        title: str | None = None
        if code := block.find("code"):
            if match := TITLE_PATTERN.match(code.get_text()):
                title = match.group(1)

        if not title:
            continue

        figure = Tag(name="figure", attrs={"class": "mermaid-figure"})
        figcaption = Tag(name="figcaption")
        figcaption.string = title

        block.wrap(figure)
        figure.append(figcaption)

    return str(soup)
