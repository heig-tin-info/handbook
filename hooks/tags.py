r"""Adds custom cats to the search index.

MkDocs Material only supports tags for a whole document, not for individual sections.
This hook adds the syntax [[tag]] or [[text|tag]] to the markdown files which only
applies in non-code blocks.

Custom tags can be added, for example to use a different name for the tag than the text.

Example: This shadder has several [[vertices|vertex]] and [[faces|face]].

Found tags are injected to the search_index.json in the hard way, because this
is not configurable in the Material theme.

## Why this feature?

When generating a printed version of the document, interactive
search is obvously not available. Tags can be used to create an index of the document.
For example with LaTeX, it is easy to adds \index{tag}.

## Syntax

- [[tag]]: The tag is the same as the text.
- [[text|tag]]: The tag is different from the text.
- [[|tag]]: The tag is used without text.
- [[text|tag|entry]]: The third part is only used for printed version, it is the entry
  in the index table for example [[The Matrix|Matrix|Matrix, The]].

## HTML output

The tags are rendered as:

```html
<span class="ycr-hashtag" data-tag="tag">text</span>.
```

The class purpose is to style the tags.
"""

from __future__ import annotations

import json
import os
import re
import xml.etree.ElementTree as etree
from collections import defaultdict
from typing import Match

import inflection
from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from mkdocs import plugins
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


class TagInlineProcessor(InlineProcessor):
    """Render the ``[[tag]]`` syntax as styled span elements."""

    def _to_kebab_case(self, text: str) -> str:
        """Convert the provided text to kebab case."""

        return inflection.parameterize(text)

    def handleMatch(
        self,
        match: Match[str],
        data: str,
    ) -> tuple[etree.Element, int, int]:
        """Transform the Markdown match into a span element."""

        del data

        text = match.group(1)
        tag = self._to_kebab_case(text if match.group(2) is None else match.group(2))
        attrib = {"class": "ycr-hashtag", "data-tag": tag}
        entry = next(x for x in (match.group(3), text, tag) if x is not None)
        attrib["data-index-entry"] = entry
        element = etree.Element("span", attrib=attrib)
        element.text = text
        return element, match.start(0), match.end(0)


class TagExtension(Extension):
    """Register the inline processor for tag syntax."""

    def extendMarkdown(self, md: Markdown) -> None:
        pattern = r"\[\[([^\]|]*)(?:\|([^\]]*?)(?:\|([^\]]+))?)?\]\]"
        tag_processor = TagInlineProcessor(pattern, md)
        md.inlinePatterns.register(tag_processor, "tag_inline", 175)


hashtags: defaultdict[str, set[str]] = defaultdict(set)

RE_HEADERLINK: re.Pattern[str] = re.compile(
    r'<a\s*[^>]*?headerlink[^>]*?href="(#[^"]+)"[^>]*?>'
)
RE_DATATAG: re.Pattern[str] = re.compile(r'<\w+\s+[^>]*data-tag="([^"]+)"[^>]*>')


def on_config(config: MkDocsConfig) -> None:
    """Enable the custom Markdown extension."""

    config.markdown_extensions.append(TagExtension())


def on_page_content(
    html: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Collect tag occurrences for later injection into the search index."""

    del config, files

    last_heading_tag = ""
    headings = 0
    for line in html.split("\n"):
        if heading := RE_HEADERLINK.search(line):
            last_heading_tag = heading.group(1)
            headings += 1

        for tag in RE_DATATAG.findall(line):
            location = f"{page.url}{last_heading_tag}" if headings > 1 else page.url
            hashtags[location].add(tag)

    return html


@plugins.event_priority(-100)
def on_post_build(config: MkDocsConfig) -> None:
    """Inject collected tags into ``search_index.json`` after the build."""

    base = os.path.join(config.site_dir, "search")
    path = os.path.join(base, "search_index.json")
    with open(path, "r", encoding="utf-8") as fh:
        search_index = json.load(fh)

    for entry in search_index["docs"]:
        if tags := hashtags.get(entry["location"]):
            entry.setdefault("tags", [])
            entry["tags"].extend(sorted(tags))

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(search_index, fh)
