r""" Adds custom cats to the search index.

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
import os
import json
import re
from mkdocs import plugins
from collections import defaultdict
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
import inflection


class TagInlineProcessor(InlineProcessor):
    def _to_kebab_case(self, text):
        return inflection.parameterize(text)

    def handleMatch(self, m, data):
        text = m.group(1)
        tag = self._to_kebab_case(text if m.group(2) is None else m.group(2))
        attrib = {
            'class': 'ycr-hashtag',
            'data-tag': tag
        }

        entry = [x for x in [m.group(3), text, tag] if x is not None][0]

        attrib['data-index-entry'] = entry

        el = etree.Element('span', attrib=attrib)

        el.text = text
        return el, m.start(0), m.end(0)

class TagExtension(Extension):
    def extendMarkdown(self, md):
        TAG_RE = r'\[\[([^\]|]*)(?:\|([^\]]*?)(?:\|([^\]]+))?)?\]\]'
        tag_processor = TagInlineProcessor(TAG_RE, md)
        md.inlinePatterns.register(tag_processor, 'tag_inline', 175)


hashtags = defaultdict(set)

RE_HEADERLINK = re.compile(r'<a\s*[^>]*?headerlink[^>]*?href="(#[^"]+)"[^>]*?>')
RE_DATATAG = re.compile(r'<\w+\s+[^>]*data-tag="([^"]+)"[^>]*>')

def on_config(config):
    config.markdown_extensions.append(TagExtension())

def on_page_content(html, page, config, files):
    global hashtags

    last_heading_tag = ''
    headings = 0
    for line in html.split('\n'):
        if heading := RE_HEADERLINK.search(line):
            last_heading_tag = heading.group(1)
            headings += 1

        for tag in RE_DATATAG.findall(line):
            if headings > 1:
                location = f'{page.url}{last_heading_tag}'
            else:
                location = page.url
            hashtags[location].add(tag)

    return html

@plugins.event_priority(-100)
def on_post_build(config):
    """ Must be called after the search index has been generated. """
    base = os.path.join(config.site_dir, "search")
    path = os.path.join(base, "search_index.json")
    with open(path, 'r', encoding='utf-8') as f:
        search_index = json.load(f)

    for entry in search_index["docs"]:
        if entry["location"] in hashtags:
            if "tags" not in entry:
                entry["tags"] = []
            entry["tags"] += list(hashtags[entry["location"]])

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f)