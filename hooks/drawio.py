"""Adds a class to drawio images to prevent GLightbox to process them.
GraphViwer will process them instead."""

import re

RE_IMG = re.compile(r"(!\[.*?\]\(.*?\.drawio.*?\))(\s*\{.*?\})?")


def on_page_markdown(markdown, page, config, files):
    def add_class(match):
        img_tag = match.group(1)
        content = match.group(2) if match.group(2) else ""
        if "drawio-diagram" in content:
            return img_tag + content
        elif content:
            return f'{img_tag}{content.rstrip("}")} .drawio-diagram}}'
        else:
            return f"{img_tag}{{.drawio-diagram}}"

    return RE_IMG.sub(add_class, markdown)
