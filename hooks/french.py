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

def process_unbreakable_space(segment):
    """Adds unbreakable spaces before colons and semi-colons in French."""
    def french_colon(match):
        return match.group(1) + \
            re.sub(r'(?<=\w) ?([!?:;])', r'&thinsp;\1',
                   match.group(2)) + \
            match.group(3)

    return RE_PARAGRAPH.sub(french_colon, segment)

def on_page_content(html, page, config, files):
    result = []
    inside_code_block = False
    start_pos = 0

    while True:
        if inside_code_block:
            end_code_tag = html.find('</code>', start_pos)
            if end_code_tag == -1:
                # No more closing code tags
                result.append(html[start_pos:])
                break
            result.append(html[start_pos:end_code_tag + len('</code>')])
            start_pos = end_code_tag + len('</code>')
            inside_code_block = False
        else:
            start_code_tag = html.find('<code>', start_pos)
            if start_code_tag == -1:
                # No more code tags
                result.append(process_unbreakable_space(html[start_pos:]))
                break
            result.append(process_unbreakable_space(html[start_pos:start_code_tag]))
            end_code_tag = html.find('</code>', start_code_tag)
            if end_code_tag == -1:
                # Malformed HTML, assume everything after start_code_tag is code
                result.append(html[start_code_tag:])
                break
            result.append(html[start_code_tag:end_code_tag + len('</code>')])
            start_pos = end_code_tag + len('</code>')

    return ''.join(result)
