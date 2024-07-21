""" Rename admonitions to "Note" and "Warning" in French. """
import logging
import stopwatch as sw
from bs4 import BeautifulSoup
import re
log = logging.getLogger('mkdocs')

TRANSLATIONS = {
    'note': 'Note',
    'warning': 'Attention',
    'tip': 'Astuce',
    'danger': 'Danger',
    'info': 'Information',
    'example': 'Exemple',
    'cite': 'Citation',
}

RE_ADMONITION = re.compile(r'^(!!! ?)([\w\-]+(?: +[\w\-]+)*)(?: +"(.*?)")? *$')
RE_PARAGRAPH = re.compile(r'<p>(.*?)</p>')
stopwatch = sw.Stopwatch()

translations = {}

def on_config(config):
    global translations
    stopwatch.reset()
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
        text = match.group(1)
        return re.sub(r'(?<=\w) ?([!?:;])', r'&thinsp;\1', text)

    return RE_PARAGRAPH.sub(french_colon, html)
# def on_page_content(html, page, config, files):
#     stopwatch.start()
#     soup = BeautifulSoup(html, 'lxml')

#     admonitions_list = set(TRANSLATIONS.keys())
#     for tag in soup.select('div.admonition'):
#         admonition_types = set(tag.attrs.get('class')).intersection(admonitions_list)
#         if not admonition_types:
#             continue
#         key = admonition_types.pop()

#         title = tag.select_one('p.admonition-title')
#         text = title.get_text()

#         # Default title, just translate the content
#         if text == key.capitalize():
#             title.string = TRANSLATIONS[key]
#         # Append a title to existing content
#         else:
#             # Add tag to put the title in bold
#             heading = BeautifulSoup(f"<strong>{TRANSLATIONS[key]}&nbsp;:</strong>&nbsp;{text}", 'html.parser')
#             title.clear()
#             title.append(heading)
#     html = str(soup)
#     stopwatch.lap()
#     return html

def on_post_build(config):
    log.info(f"Hooks French done in {stopwatch.total:.2f} seconds.")
