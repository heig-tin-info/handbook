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


def on_page_content(html, page, config, files):
    return ''.join([
        re.sub(r'(?<=\w) ?([!?:;])', r'&thinsp;\1', part)
        if not re.fullmatch(RE_PUNCT, part) else part
        for part in RE_PUNCT.split(html)
    ])