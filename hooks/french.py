"""French typography helpers for MkDocs.

This plugin adds some French typography rules to your MkDocs project:

- Add a thin space before `!`, `?`, `:` and `;` punctuation marks.
- Use french quote (« and ») around quoted text.
- Use long dash (—) lists.
- Translate admonition titles.
"""

from __future__ import annotations

import re
from typing import Mapping

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

RE_ADMONITION = re.compile(
    r'^(?P<pre>!!!\s*(?P<type>[\w\-]+)(?P<extra>(?: +[\w\-]+)*))(?: +"(?P<title>.*?)")? *$'
)
RE_IGNORE = re.compile(r"<code[^>]*>.*?</code>|<[^>]+>|&\w+;|\w://|[!?:;]\w", re.DOTALL)
RE_PUNCT = re.compile(r"(?<=\w) ?([!?:;])")

translations: Mapping[str, str] = {}


def on_config(config: MkDocsConfig) -> None:
    """Load the admonition translations from the MkDocs configuration."""

    global translations
    extra = config.get("extra", {})
    translations = extra.get("admonition_translations", {})


def on_page_markdown(
    markdown: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Translate admonition titles when none are explicitly provided."""

    del page, config, files

    out: list[str] = []
    for line in markdown.splitlines():
        if match := RE_ADMONITION.match(line):
            admonition_type = match.group("type")
            title = match.group("title")
            if (title is None or not title.strip()) and admonition_type in translations:
                translated = translations[admonition_type]
                line = f"{match.group('pre')} \"{translated}\""
        out.append(line)
    return "\n".join(out)


def _process_html_segment(segment: str) -> str:
    """Apply punctuation and quote fixes to a plain HTML fragment."""

    segment = RE_PUNCT.sub(r"&thinsp;\1", segment)
    return re.sub(r'"([^"]+)"', r"«&thinsp;\1&thinsp;»", segment)


def process_html(html: str) -> str:
    """Adjust punctuation spacing while ignoring code blocks and HTML tags."""

    parts = RE_IGNORE.split(html)
    entities = RE_IGNORE.findall(html)

    processed_parts = [
        _process_html_segment(part) if not RE_IGNORE.fullmatch(part) else part
        for part in parts
    ]

    result = processed_parts[0]
    for entity, part in zip(entities, processed_parts[1:], strict=False):
        result += entity + part

    return result


def on_page_content(
    html: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Apply typographic fixes to the rendered HTML."""

    del page, config, files
    return process_html(html)
