import re
import xml.etree.ElementTree as etree

from markdown.extensions.abbr import (
    AbbrBlockprocessor,
    AbbrExtension,
    AbbrTreeprocessor,
)
from markdown.util import AtomicString
from mkdocs.utils import log


class AbbrWikiExtension(AbbrExtension):
    """Markdown extension to process abbreviations with Wikipedia links."""

    def extendMarkdown(self, md):
        """Insert `AbbrTreeprocessor` and `AbbrBlockprocessor`."""
        if self.config["glossary"][0]:
            self.load_glossary(self.config["glossary"][0])
        self.abbrs.update(self.glossary)
        md.registerExtension(self)
        # Priority must be higher than standard `abbr` extension.
        md.treeprocessors.register(AbbrWikiTreeprocessor(md, self.abbrs), "abbrwiki", 8)
        md.parser.blockprocessors.register(
            AbbrWikiBlockprocessor(md.parser, self.abbrs), "abbrwiki", 17
        )


class AbbrWikiTreeprocessor(AbbrTreeprocessor):
    """Process the document tree to find abbreviations and wrap them in `abbr` tags."""

    def create_element(self, title: str, text: str, tail: str) -> etree.Element:
        abbr = etree.Element("a", {"href": title, "class": "ycr-abbr"})
        abbr.text = AtomicString(text)
        abbr.tail = tail
        return abbr

    def iter_element(
        self, el: etree.Element, parent: etree.Element | None = None
    ) -> None:
        """Recursively iterate over elements, run regex on text and wrap matches in `abbr` tags."""
        for child in reversed(el):
            self.iter_element(child, el)

        if text := el.text:
            for m in reversed(list(self.RE.finditer(text))):
                if self.abbrs[m.group(0)]:
                    if el.tag == "a":
                        if el.text == m.group(0):
                            # Parent is already a link, we can't wrap it in another link
                            log.warning(
                                "Can't wrap abbreviation in existing link: %s, ignoring!",
                                m.group(0),
                            )
                    else:
                        abbr = self.create_element(
                            self.abbrs[m.group(0)], m.group(0), text[m.end() :]
                        )
                        el.insert(0, abbr)
                        text = text[: m.start()]
            el.text = text
        if parent is not None and el.tail:
            tail = el.tail
            index = list(parent).index(el) + 1
            for m in reversed(list(self.RE.finditer(tail))):
                abbr = self.create_element(
                    self.abbrs[m.group(0)], m.group(0), tail[m.end() :]
                )
                parent.insert(index, abbr)
                tail = tail[: m.start()]
            el.tail = tail


class AbbrWikiBlockprocessor(AbbrBlockprocessor):
    """Process the markdown to find abbreviation definitions with Wikipedia links."""

    RE = re.compile(
        r"^[*]\[(?P<abbr>[^\\]*?)\][ ]?:[ ]*\n?[ ]*(?P<title>https?://[a-z]{2,}\.wikipedia\.org/.*)$",
        re.MULTILINE,
    )


def makeExtension(**kwargs):  # pragma: no cover
    return AbbrWikiExtension(**kwargs)


def on_config(config):
    config["markdown_extensions"].append(AbbrWikiExtension())
