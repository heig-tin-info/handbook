"""Generate tags from inline code blocks for the search index."""

from __future__ import annotations

import re
from typing import Match

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

RE_KEYWORD: re.Pattern[str] = re.compile(
    r"<code>(<?[_\w.]{3,}>?)</code>", re.IGNORECASE
)
RE_IGNORE: re.Pattern[str] = re.compile(r"0[xb].+|[.\d-]+")


def _wrap_keyword(match: Match[str]) -> str:
    """Wrap eligible inline code blocks in a tag span."""

    keyword = match.group(1)
    if RE_IGNORE.match(keyword) or len(keyword) > 15:
        return match.group(0)
    return (
        f'<span class="ycr-hashtag" data-index-entry="{keyword}" '
        f'data-tag="{keyword}">{match.group(0)}</span>'
    )


def on_page_content(
    html: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Inject tag spans around inline code keywords."""

    del page, config, files
    return RE_KEYWORD.sub(_wrap_keyword, html)
