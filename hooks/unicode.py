"""
To identify unicode codes in the markdown content, this hook replaces

U+XXXX with a tag
"""

from xml.etree import ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

BASE_URL = "https://symbl.cc/fr/"


class UnicodeProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        unicode_code = m.group(1)
        el = etree.Element("a")
        el.set("href", f"{BASE_URL}/{unicode_code}")
        el.set("class", "ycr-callout ycr-unicode")
        el.set("target", "_blank")
        el.text = f"{unicode_code}"
        return el, m.start(0), m.end(0)


class UnicodeExtension(Extension):
    def extendMarkdown(self, md):
        UNICODE_RE = r"\bU\+([0-9A-F]{4,5})\b"
        unicode_pattern = UnicodeProcessor(UNICODE_RE, md)
        md.inlinePatterns.register(unicode_pattern, "unicode", 175)


def on_config(config):
    config["markdown_extensions"].append(UnicodeExtension())
