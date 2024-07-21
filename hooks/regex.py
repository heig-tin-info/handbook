"""
To identify unicode codes in the markdown content, this hook replaces

U+XXXX with a tag
"""
import os
import re
import shutil

RE = re.compile(r"<code>\/(.*?)/([igmsx]*)</code>")

def on_page_content(html, page, config, files):
    return RE.sub(r'<a href="https://regex101.com/?regex=\1&flags=\2&flavor=pcre2" class="ycr-callout ycr-regex" target="_blank">/\1/\2</a>', html)
