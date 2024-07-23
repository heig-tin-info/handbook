""" Adds a class to drawio images to prevent GLightbox to process them.
It is useful for drawio which is provided by the diagram render on the
frontend."""
import re


def on_page_markdown(markdown, page, config, files):
    img_regex = r'(!\[.*?\]\(.*?\.drawio.*?\))(\s*\{.*?\})?'

    def add_class(match):
        img_tag = match.group(1)
        content = match.group(2) if match.group(2) else ''
        if 'drawio-diagram' in content:
            return img_tag + content
        elif content:
            return f'{img_tag}{content.rstrip("}")} .drawio-diagram}}'
        else:
            return f'{img_tag}{{.drawio-diagram}}'

    return re.sub(img_regex, add_class, markdown)