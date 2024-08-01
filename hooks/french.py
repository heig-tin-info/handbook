""" Rename admonitions to "Note" and "Warning" in French. """
import logging
import re

log = logging.getLogger('mkdocs')

RE_ADMONITION = re.compile(r'^(?P<pre>!!!\s*(?P<type>[\w\-]+)(?P<extra>(?: +[\w\-]+)*))(?: +"(?P<title>.*?)")? *$')
RE_PUNCT = re.compile(r'(<code>.*?</code>|<[^>]+>)', re.DOTALL)

translations = {}


def on_config(config):
    global translations
    translations = config['extra']['admonition_translations']


def on_page_markdown(markdown, page, config, files):
    out = []
    for line in markdown.splitlines():
        m = RE_ADMONITION.match(line)

        if m:
            type = m.group('type')
            if (
                m.group('title') is None or m.group('title').strip() == ''
            ) and type in translations:
                title = translations[type]
                line = m.group('pre') + f' "{title}"'
        out.append(line)
    markdown = "\n".join(out)
    return markdown


RE_PUNCT = re.compile(r'(?<=\w) ?([!?:;])')
RE_IGNORE = re.compile(r'<code[^>]*>.*?</code>|<[^>]+>|&\w+;|\w://|[!?:;]\w', re.DOTALL)

def process_html(html):
    parts = RE_IGNORE.split(html)
    entities = RE_IGNORE.findall(html)

    processed_parts = [
        RE_PUNCT.sub(r'&thinsp;\1', part)
        if not RE_IGNORE.fullmatch(part) else part
        for part in parts
    ]

    # Reconstruct the html with entities
    result = processed_parts[0]
    for entity, part in zip(entities, processed_parts[1:]):
        result += entity + part

    return result

def on_page_content(html, page, config, files):
    return process_html(html)
