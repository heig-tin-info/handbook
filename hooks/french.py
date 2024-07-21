""" Rename admonitions to "Note" and "Warning" in French. """
import logging
import re

log = logging.getLogger('mkdocs')

RE_ADMONITION = re.compile(r'^(!!! ?)([\w\-]+(?: +[\w\-]+)*)(?: +"(.*?)")? *$')
RE_PARAGRAPH = re.compile(r'(<p>)(.*?)(</p>)')

translations = {}


def on_config(config):
    global translations
    translations = config['extra']['admonition_translations']


def on_page_markdown(markdown, page, config, files):
    out = []
    for line in markdown.splitlines():
        m = RE_ADMONITION.match(line)
        if m:
            type = m.group(2)
            if (
                m.group(3) is None or m.group(3).strip() == ''
            ) and type in translations:
                title = translations[type]
                line = m.group(1) + m.group(2) + f' "{title}"'
        out.append(line)
    markdown = "\n".join(out)
    return markdown


def on_page_content(html, page, config, files):
    def french_colon(match):
        return match.group(1) + \
            re.sub(r'(?<=\w) ?([!?:;])', r'&thinsp;\1',
                   match.group(2)) + \
            match.group(3)

    return RE_PARAGRAPH.sub(french_colon, html)
