""" Generate tags from inline code blocks. They will be used
with tags hook to generate a search index."""
import re

from mkdocs.utils import log

RE_KEYWORD = re.compile(r"<code>(<?[_\w.]{3,}>?)</code>", re.IGNORECASE)

# Ignore numbers and hexadecimals
RE_IGNORE = re.compile(r"0[xb].+|[.\d-]+")

def on_page_content(html, page, config, files):
    def replace_code(m):
        if RE_IGNORE.match(m.group(1)) or len(m.group(1)) > 15:
            return m.group(0)
        return f'<span class="ycr-hashtag" data-index-entry="{m.group(1)}" data-tag="{m.group(1)}">{m.group(0)}</span>'

    return RE_KEYWORD.sub(replace_code, html)
