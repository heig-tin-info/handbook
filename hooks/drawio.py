"""Ensure Draw.io diagrams bypass GLightbox processing."""

from __future__ import annotations

import re
from typing import Match

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

RE_IMG: re.Pattern[str] = re.compile(r"(!\[.*?\]\(.*?\.drawio.*?\))(\s*\{.*?\})?")


def _add_class(match: Match[str]) -> str:
    """Append the ``.drawio-diagram`` class to a Markdown image."""

    img_tag = match.group(1)
    content = match.group(2) or ""
    if "drawio-diagram" in content:
        return img_tag + content
    if content:
        return f"{img_tag}{content.rstrip('}')} .drawio-diagram}}"
    return f"{img_tag}{{.drawio-diagram}}"


def on_page_markdown(
    markdown: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Update Markdown images that refer to ``.drawio`` assets."""

    del page, config, files
    return RE_IMG.sub(_add_class, markdown)
