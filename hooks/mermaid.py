r"""Wrap Mermaid diagrams with figures when a title comment is present.

<figure id="_figure-1"><a class="glightbox" data-desc-position="bottom" data-height="auto" data-type="image"
data-width="auto" href="http://127.0.0.1:8000/handbook/assets/images/thompson-kernighan-ritchie.webp">

<img alt="Les p�res fondateurs du C" src="http://127.0.0.1:8000/handbook/assets/images/thompson-kernighan-ritchie.webp"></a>

<figcaption> Les p�res fondateurs du C</figcaption></figure>

<div class="mermaid"></div>

"""

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
