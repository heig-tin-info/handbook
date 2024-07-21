"""
To identify unicode codes in the markdown content, this hook replaces

U+XXXX with a tag
"""
import os
import re
import shutil

RE = re.compile(r"\bU\+([0-9A-F]{4,5})\b")

def on_page_content(html, page, config, files):
    return RE.sub(r'<a href="https://symbl.cc/en/\1" class="ycr-callout ycr-unicode" target="_blank">\1</a>', html)
