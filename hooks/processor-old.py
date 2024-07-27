from bs4 import BeautifulSoup, Tag
import os
import logging
from jinja2 import Environment, FileSystemLoader
import textwrap
import tempfile
from pathlib import Path
from hashlib import sha256
import subprocess
import re
import requests
import shutil
import mimetypes
import urllib.parse
import cairosvg
from IPython import embed
from html import unescape
from PIL import Image
from typing import Union
from latex.utils import escape_all_latex_chars, escape_latex_chars

log = logging.getLogger(f"mkdocs.plugins.latex")

SCRIPT_DIR = Path(__file__).resolve().parent


class LaTeXRenderer:
    def __init__(self, output_path=Path('build')):
        self.formatter = LaTeXFormatter()
        self.formatter.set_output_path(output_path / 'images')

        # Mkdir if not exists
        self.formatter.output_path.mkdir(parents=True, exist_ok=True)

        # Metadata
        self.glossary = {}
        self.acronyms = {}

    def extract_code_inline(self, soup):
        if soup.name != 'code':
            raise ValueError(f"Expected code block, got {soup.name}")

        language = get_code_language(soup)
        language = language if language else 'text'
        # listing = []
        # for code in soup.find_all("code"):
        #     for i, span_line in enumerate(code.find_all('span', id=lambda x: x and x.startswith('__'))):
        #         listing.append(''.join([span.get_text() for span in span_line.find_all('span')]))
        return {
            'language': language,
            'text': soup.get_text()
        }



    def get_route(self, element):
        """ Get position of an element in the document
        a > b > c...
        """
        def fetch(element):
            el = element
            yield element.name
            while el.parent:
                el = el.parent
                yield el.name

        return '/'.join(reversed(list(fetch(element))))

    def get_table_styles(self, cell):
        if not cell:
            return ''
        style = cell.get('style', '')
        if 'text-align: right' in style:
            return 'right'
        if 'text-align: center' in style:
            return 'center'
        return 'left'

    def extract_table(self, table):
        """Extract table from a <table> object.
        Format is
        {
            columns: ['left', 'center', 'right'],
            rows: [
                ['row1', 'row2', 'row3'],
                ['row4', 'row5', 'row6'],
            ]
        }
        """
        if not table or table.name != 'table':
            return
        table_data = []
        styles = []
        for row in table.find_all('tr'):
            row_data = []
            row_styles = []
            cells = row.find_all(['td', 'th'])
            for cell in cells:
                row_data.append(cell.get_text().strip())
                row_styles.append(self.get_table_styles(cell))
            table_data.append(row_data)
            styles.append(row_styles)

        return {
            'columns': styles[0],
            'rows': table_data
        }

    # def render_format(self, soup):
    #     mapper = {
    #         'del': self.formatter.strikethrough,
    #         'em': self.formatter.italic,
    #         'ins': self.formatter.underline,
    #         'mark': self.formatter.highlight,
    #         'strong': self.formatter.strong,
    #         'sub': self.formatter.subscript,
    #         'sup': self.formatter.superscript,
    #     }
    #     for el in soup.find_all(mapper.keys()):
    #         if el.name == 'sup' and el.get('id'):
    #             # This is a footnote, we will handle it later
    #             continue
    #         el.replace_with(mapper[el.name](el.get_text()))

    def render_inlines(self, soup):
        for inline in soup.find_all(['pre', 'abbr', 'span', 'span', 'a']):
            text = inline.get_text()
            match inline.name:
                # case 'abbr':
                #     inline.replace_with(
                #         self.formatter.acronym(text,
                #                                inline.get('title', '')))
                # case 'a':
                #     if 'headerlink' in inline.get('class', []):
                #         inline.extract()
                #     elif 'footnote-backref' in inline.get('class', []):
                #         inline.extract()
                #     elif 'glightbox' in inline.get('class', []):
                #         inline.unwrap()

                # case 'pre':
                #     if 'mermaid' in inline.get('class', []):
                #         code = inline.find('code')
                #         if not code:
                #             log.warning(f"Missing code in mermaid pre {self.get_route(inline)}")
                #         else:
                #             code = code.get_text()
                #             inline.replace_with(self.formatter.mermaid(code))

                # case 'span':
                #     classes = inline.get('class', [])
                #     if 'twemoji' in classes:
                #         if inline.children:
                #             svg = next(inline.children)
                #             if svg and svg.name == 'svg':
                #                 svg_code = svg.prettify()
                #                 inline.replace_with(
                #                     self.formatter.svg(svg_code))
                #             else:
                #                 raise ValueError(f"Expected svg, got {svg}")
                #         else:
                #             raise ValueError(f"No children in span")
                    # elif 'arithmatex' in classes:
                    #     # Direct MathJax format, no need to process
                    #     inline.replace_with(text)
                    # elif 'critic' in classes:
                    #     # Critic markup
                    #     if 'add' in classes:
                    #         inline.replace_with(self.formatter.add(text))
                    #     elif 'del' in classes:
                    #         inline.replace_with(self.formatter.delete(text))
                    #     elif 'comment' in classes:
                    #         inline.replace_with(self.formatter.comment(text))
                    #     else:
                    #         log.warning(f"Ignoring critic span {inline}")
                    else:
                        log.warning(f"Ignoring span {self.get_route(inline)} {inline}")
                case _:
                    raise ValueError(f"Unknown tag: {inline.name}")

    # def render_smart_symbols(self, str):
    #     mapping = {
    #         '½': '\\nicefrac{1}{2}',
    #         '¼': '\\nicefrac{1}{4}',
    #         '¾': '\\nicefrac{3}{4}',
    #         '⅓': '\\nicefrac{1}{3}',
    #         '⅔': '\\nicefrac{2}{3}',
    #         '⅛': '\\nicefrac{1}{8}',
    #         '⅜': '\\nicefrac{3}{8}',
    #         '⅝': '\\nicefrac{5}{8}',
    #         '⅞': '\\nicefrac{7}{8}',
    #         '⅕': '\\nicefrac{1}{5}',
    #         '⅖': '\\nicefrac{2}{5}',
    #         '⅗': '\\nicefrac{3}{5}',
    #         '⅘': '\\nicefrac{4}{5}',
    #         '⅙': '\\nicefrac{1}{6}',
    #         '⅚': '\\nicefrac{5}{6}'
    #     }
    #     for key, value in mapping.items():
    #         str = str.replace(key, value)

    #     str = re.sub(r'\b(\d+)\/(\d+)\b', r'\\nicefrac{\1}{\2}', str)

    #     return str

    def render(self, html, output_path, file_path, base_level=0):
        soup = BeautifulSoup(html, 'html.parser')


        # Regex101 links
        # <a href="https://regex101.com/?regex='([^']|\\[nrftvba'])'&flags=&flavor=pcre2" class="ycr-callout ycr-regex" target="_blank">/'([^']|\\[nrftvba'])'/</a>
        # for a in soup.find_all('a', class_=['ycr-regex']):
        #     regex = escape_all_latex_chars(a.get_text())
        #     href = a.get('href')
        #     url = escape_all_latex_chars(urllib.parse.quote(href, safe=':/?&='))
        #     a.replace_with(self.formatter.regex(regex, url=url))

        # Keystrokes
        # for span in soup.find_all('span', class_='keys'):
        #     keys = []
        #     for key in span.find_all(['kbd']):
        #         key_class = get_class(key, re.compile(r'^key-(.*)$'))
        #         if not key_class:
        #             log.warning(f"Unknown key type: {key.get('class', [])}")
        #         keys.append(key_class[4:])
        #     span.replace_with(self.formatter.keystroke(keys))

        # Strong, italic, underline, ...
        # self.render_format(soup)

        # # All inline
        # self.render_inlines(soup)

        # Headings
        # for inline in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        #     title = inline.get_text()
        #     level = int(inline.name[1:]) + base_level
        #     ref = inline.get('id', None)
        #     inline.replace_with(self.formatter.heading(title, level=level, ref=ref))

        # Autorefs with key data-autorefs-identifier
        # for autoref in soup.find_all('span', attrs={'data-autorefs-identifier': True}):
        #     identifier = autoref.get('data-autorefs-identifier')
        #     autoref.replace_with(self.formatter.ref(autoref.get_text(), ref=identifier))

        # Get footnotes
        # footnotes = {}
        # for footnote in soup.find_all(['div'], class_='footnote'):
        #     for li in footnote.find_all('li'):
        #         footnote_id = re.sub(r'^fn:(\d+)', r'\1', li.get('id', ''))
        #         if not footnote_id:
        #             raise ValueError(f"Missing id in footnote: {li}")
        #         footnotes[footnote_id] = li.get_text()
        #     footnote.extract()

        # for sup in soup.find_all('sup', id=True):
        #     footnote_id = re.sub(r'^fnref:(\d+)', r'\1', sup.get('id', ''))
        #     sup.replace_with(self.formatter.footnote(footnotes[footnote_id]))

        # Lists must be processed deep first
        # for el in find_all_dfs(soup, ['ol', 'ul']):
        #     items = [li.get_text() for li in el.find_all('li')]
        #     checkboxes = [
        #         {'[ ]': False, '[x]': True}.get(item[:3], False) for item in items
        #     ]
        #     match el.name:
        #         case 'ul':
        #             if any([item.startswith('[ ]') or item.startswith('[x]') for item in items]):
        #                 items = [item[4:] for item in items]
        #                 el.replace_with(self.formatter.choices(items=zip(checkboxes, items)))
        #             else:
        #                 el.replace_with(self.formatter.unordered_list(items=items))
        #         case 'ol':
        #             el.replace_with(self.formatter.ordered_list(items=items))

        # for dl in soup.find_all(['dl']):
        #     items = []
        #     title = None
        #     for el in soup.find_all(['dt', 'dd']):
        #         if el.name == 'dt':
        #             title = el.get_text()
        #         elif el.name == 'dd':
        #             content = el.get_text()
        #             items.append((title, content))

        #     dl.replace_with(self.formatter.description_list(items=items))

        # Tabbed item rendered linearly
        # for div in soup.find_all(['div'], class_='tabbed-set'):
        #     # Get titles
        #     titles = []
        #     for label in div.find_all(['label']):
        #         titles.append(label.get_text())

        #     # Get content
        #     tabbed_content = div.find('div', class_='tabbed-content')
        #     for i, tab in enumerate(tabbed_content.find_all(['div'], class_='tabbed-block')):
        #         content = tab.get_text()
        #         tab.replace_with(self.formatter.tabbed(content, title=titles[i]))
        #     tabbed_content.unwrap()

        #     for el in div.find_all(['input'], recursive=False):
        #         el.extract()
        #     for el in div.find_all(['div'], class_=['tabbed-labels']):
        #         el.extract()
        #     div.unwrap()

        # for math_block in soup.find_all(['div'], class_='arithmatex'):
        #     math_block.replace_with(f"\n{math_block.get_text()}\n")

        # for figure in soup.find_all(['figure']):
        #     image = figure.find('img')
        #     if not image:
        #         raise ValueError(f"Missing image in figure {figure}")
        #     image_src = image.get('src')
        #     if not image_src:
        #         raise ValueError(f"Missing src in image {image}")
        #     if not image_src.startswith('http'):
        #         if file_path.name == 'index.md':
        #             file_path = file_path.parent
        #         image_src = (file_path / image_src).resolve()
        #         if not image_src.exists():
        #             raise ValueError(f"Image not found: {image_src}")

        #     caption = figure.find('figcaption')
        #     caption_text = caption.get_text() if caption else image.get('alt', '')
        #     figure.replace_with(self.formatter.figure(caption=caption_text, path=image_src))

        for table in soup.find_all(['table']):
            data = self.extract_table(table)
            if data:
                table.replace_with(self.formatter.table(**data))

        # Emoji
        for emoji in soup.find_all('img', class_='twemoji'):
            response = requests.get(emoji.get('src'))
            if response.status_code != 200:
                raise ValueError(f"Failed to fetch emoji: {response.status_code}")
            svg = response.text
            emoji.replace_with(self.formatter.svg(svg))

        # Admonitions with callout
        for admonition in soup.find_all(['div'], class_='admonition'):
            classes = admonition.get('class', [])
            filtered_classes = [cls for cls in classes if cls not in ['admonition', 'annotate', 'inline', 'end', 'left', 'right']]
            if len(filtered_classes) > 1:
                raise ValueError(f"Multiple classes in admonition: {filtered_classes}")
            admonition_type = filtered_classes[0]
            title = admonition.find('p', class_='admonition-title')
            if title:
                title = title.get_text()
            content = admonition.get_text()

            admonition.replace_with(
                self.formatter.callout(content,
                                       title=title,
                                       type=admonition_type))

        # Foldable admonitions are implemented with details/summary
        for admonition in soup.find_all(['details']):
            classes = admonition.get('class', [])
            if len(classes) > 1:
                raise ValueError(f"Multiple classes in details: {classes}")
            admonition_type = classes[0]

            if summary := admonition.find('summary'):
                title = summary.get_text()
                summary.extract()

            content = admonition.get_text()

            admonition.replace_with(
                self.formatter.callout(content,
                                       title=title,
                                       type=admonition_type))

        # Links
        for a in soup.find_all('a'):
            if a.get('href', '').startswith('http'):
                a.replace_with(self.formatter.url(a.get_text(), url=a.get('href')))
            else:
                a.replace_with(f"\\href{{{a.get('href')}}}{{{a.get_text()}}}")

        def has_children(element):
            for child in element.children:
                if isinstance(child, Tag):
                    return True
            return False

        # Eventually get rid of the p tags
        for p in find_all_dfs(soup, 'p', class_=[]):
            if has_children(p):
                raise ValueError(f"Unexpected children in p tag: {p}")

            text = self.render_smart_symbols(p.get_text())
            text = escape_latex_chars(text)

            p.replace_with(f"{text}\n")

        document = unescape(str(soup).replace('&thinsp;', '~').replace(' ', '~'))

        #return self.formatter.template(content=document, glossary=self.formatter.get_glossary())
        return document
