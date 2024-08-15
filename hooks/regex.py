import re
import urllib.parse
from xml.etree import ElementTree as etree

from IPython import embed
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor


class CustomBacktickProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        BASE_URL = "https://regex101.com"

        code_content = m.group(2)
        rm = re.search(
            r"(?:\/(?P<pattern>.*?)|s\/(?P<search>.*?)\/(?P<sub>.*?))/(?P<flags>[igmsx]*)",
            code_content,
        )
        if not rm:
            return m.group(0), m.start(0), m.end(0)

        flavor = "pcre2"
        classes = "ycr-callout ycr-regex"
        target = "_blank"

        if rm.group("pattern"):
            pattern = rm.group("pattern")
            href = f"{BASE_URL}/?regex={urllib.parse.quote(pattern)}"
            regex = f"/{pattern}/"
        else:
            search = rm.group("search")
            sub = rm.group("sub")
            href = f"{BASE_URL}/?regex={urllib.parse.quote(search)}&substitution={urllib.parse.quote(sub)}"
            regex = f"s/{search}/{sub}/"

        flags = rm.group("flags")
        regex += flags
        href += f"&flags={flags}&flavor={flavor}"

        el = etree.Element("a")
        el.set("href", href)
        el.set("class", classes)
        el.set("target", target)
        el.text = f"`{regex}`"
        return el, m.start(0), m.end(0)


class RegexExtension(Extension):
    def extendMarkdown(self, md):
        # increase priority to be after pymdownx.inlinehilite
        md.inlinePatterns.register(
            CustomBacktickProcessor(
                r"(?<!\\)(`+)#!re(?:gex)?\s*(.+?)(?<!`)\1(?!`)", md
            ),
            "inline-regex",
            200,
        )


def on_config(config):
    config["markdown_extensions"].append(RegexExtension())
