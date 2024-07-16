""" Rename admonitions to "Note" and "Warning" in French. """
import logging
import stopwatch as sw
from bs4 import BeautifulSoup

log = logging.getLogger('mkdocs')

TRANSLATIONS = {
    'note': 'Note',
    'warning': 'Attention',
    'tip': 'Astuce',
    'danger': 'Danger',
    'info': 'Information',
    'example': 'Exemple',
}

stopwatch = sw.Stopwatch()

def on_config(config):
    stopwatch.reset()

def on_page_content(html, page, config, files):
    stopwatch.start()
    soup = BeautifulSoup(html, 'lxml')

    admonitions_list = set(TRANSLATIONS.keys())
    for tag in soup.select('div.admonition'):
        admonition_types = set(tag.attrs.get('class')).intersection(admonitions_list)
        if not admonition_types:
            continue
        key = admonition_types.pop()

        title = tag.select_one('p.admonition-title')
        text = title.get_text()

        # Default title, just translate the content
        if text == key.capitalize():
            title.string = TRANSLATIONS[key]
        # Append a title to existing content
        else:
            # Add tag to put the title in bold
            heading = BeautifulSoup(f"<strong>{TRANSLATIONS[key]}&nbsp;:</strong>{text}", 'html.parser')
            title.clear()
            title.append(heading)
    html = str(soup)
    stopwatch.lap()
    return html

def on_post_build(config):
    log.info(f"Hooks French done in {stopwatch.total:.2f} seconds.")
