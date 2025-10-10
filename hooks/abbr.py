
"""Custom abbreviation handling for MkDocs with Wikipedia links."""

from __future__ import annotations

import re
import xml.etree.ElementTree as etree
from typing import Any

from markdown import Markdown
from markdown.extensions.abbr import (
    AbbrBlockprocessor,
    AbbrExtension,
    AbbrTreeprocessor,
)
from markdown.util import AtomicString
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.utils import log


class AbbrWikiExtension(AbbrExtension):
    """Register custom processors that render glossary entries as links."""

    def extendMarkdown(self, md: Markdown) -> None:
        """Insert tree and block processors with a higher priority than the default."""

        glossary_path = self.config.get("glossary", [None])[0]
        if glossary_path:
            self.load_glossary(glossary_path)

        self.abbrs.update(self.glossary)
        md.registerExtension(self)
        md.treeprocessors.register(AbbrWikiTreeprocessor(md, self.abbrs), "abbrwiki", 8)
        md.parser.blockprocessors.register(
            AbbrWikiBlockprocessor(md.parser, self.abbrs),
            "abbrwiki",
            17,
        )


class AbbrWikiTreeprocessor(AbbrTreeprocessor):
    """Render abbreviations as links to Wikipedia when possible."""

    def create_element(self, title: str, text: str, tail: str) -> etree.Element:
        """Create a link element wrapping the abbreviation text."""

        abbr = etree.Element("a", {"href": title, "class": "ycr-abbr"})
        abbr.text = AtomicString(text)
        abbr.tail = tail
        return abbr

    def iter_element(self, el: etree.Element, parent: etree.Element | None = None) -> None:
        """Recursively replace abbreviation text with anchor elements."""

        for child in reversed(el):
            self.iter_element(child, el)

        if text := el.text:
            for match in reversed(list(self.RE.finditer(text))):
                abbr_value = self.abbrs.get(match.group(0))
                if not abbr_value:
                    continue
                if el.tag == "a" and el.text == match.group(0):
                    log.warning(
                        "Can't wrap abbreviation in existing link: %s, ignoring!",
                        match.group(0),
                    )
                    continue
                abbr = self.create_element(abbr_value, match.group(0), text[match.end():])
                el.insert(0, abbr)
                text = text[: match.start()]
            el.text = text

        if parent is not None and el.tail:
            tail = el.tail
            index = list(parent).index(el) + 1
            for match in reversed(list(self.RE.finditer(tail))):
                abbr_value = self.abbrs.get(match.group(0))
                if not abbr_value:
                    continue
                abbr = self.create_element(abbr_value, match.group(0), tail[match.end():])
                parent.insert(index, abbr)
                tail = tail[: match.start()]
            el.tail = tail


class AbbrWikiBlockprocessor(AbbrBlockprocessor):
    """Recognise glossary entries that point to Wikipedia articles."""

    RE = re.compile(
        r"^[*]\[(?P<abbr>[^\\]*?)\][ ]?:[ ]*\n?[ ]*(?P<title>https?://[a-z]{2,}\.wikipedia\.org/.*)$",
        re.MULTILINE,
    )


def makeExtension(**kwargs: Any) -> AbbrWikiExtension:  # pragma: no cover
    """Entry-point used by Python-Markdown."""

    return AbbrWikiExtension(**kwargs)


def on_config(config: MkDocsConfig) -> None:
    """Register the extension with MkDocs."""

    config["markdown_extensions"].append(AbbrWikiExtension())
