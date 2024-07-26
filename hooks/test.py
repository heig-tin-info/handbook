from bs4 import BeautifulSoup
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
from html import unescape

log = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent

def get_class(element, regex):
    return next((c for c in element.get('class', []) if regex.match(c)), None)

def svg2pdf(svg):
    # Create temporary svg file
    filename = Path(sha256(svg.encode()).hexdigest() + '.svg')
    svgpath = Path(os.path.join(tempfile.mkdtemp(), filename))
    with open(svgpath, 'w') as fp:
        fp.write(svg)

    pdfpath = svgpath.with_suffix('.pdf')

    inkscape_version = subprocess.check_output(
        ['inkscape', '--version'], universal_newlines=True)
    log.debug(inkscape_version)

    # Convert
    # - 'Inkscape 0.92.4 (unknown)' to [0, 92, 4]
    # - 'Inkscape 1.1-dev (3a9df5bcce, 2020-03-18)' to [1, 1]
    # - 'Inkscape 1.0rc1' to [1, 0]
    inkscape_version = re.findall(r'[0-9.]+', inkscape_version)[0]
    inkscape_version_number = [int(part) for part in inkscape_version.split('.')]

    # Right-pad the array with zeros (so [1, 1] becomes [1, 1, 0])
    inkscape_version_number += [0] * (3 - len(inkscape_version_number))

    # Tuple comparison is like version comparison
    if inkscape_version_number < [1, 0, 0]:
        command = [
            'inkscape',
            '--export-area-page',
            '--export-dpi', '300',
            '--export-pdf', pdfpath,
            '--export-latex', svgpath
            ]
    else:
        command = [
            'inkscape', svgpath,
            '--export-area-page',
            '--export-dpi', '300',
            '--export-type=pdf',
            '--export-latex',
            '--export-filename', pdfpath
            ]

    log.debug('Running command:')
    log.debug(textwrap.indent(' '.join(str(e) for e in command), '    '))

    # Recompile the svg file
    completed_process = subprocess.run(command)

    if completed_process.returncode != 0:
        log.error('Return code %s', completed_process.returncode)
    else:
        log.debug('Command succeeded')

    return pdfpath


def optimize_list(numbers):
    """Optimize a list of numbers to a list of ranges.
    >>> optimize_list([1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16])
    ['1-6', '8-10', '12', '14-16']
    """
    if not numbers:
        return []

    numbers = sorted(numbers)
    optimized = []
    start = end = numbers[0]

    for num in numbers[1:]:
        if num == end + 1:
            end = num
        else:
            optimized.append(f"{start}-{end}" if start != end else str(start))
            start = end = num

    optimized.append(f"{start}-{end}" if start != end else str(start))
    return optimized


def get_code_language(element):
    """Extract code language from a <div class="highlight"> object.
    They should be in the form of 'language-<lang>'.
    """
    if 'highlight' not in element.get('class', []):
        return None
    return next((c[9:]
                 for c in element.get('class', [])
                 if c.startswith('language-')), 'text')


class LaTeXFormatter:
    def __init__(self, template_dir=SCRIPT_DIR / 'templates'):
        self.env = Environment(
            block_start_string=r'\BLOCK{',
            block_end_string=r'}',
            variable_start_string=r'\VAR{',
            variable_end_string=r'}',
            comment_start_string=r'\COMMENT{',
            comment_end_string=r'}',
            loader=FileSystemLoader(template_dir))

        self.templates = {
            Path(filename).stem: self.env.get_template(filename)
            for filename in os.listdir(template_dir)
        }

        self.acronyms = {}

    def __getattr__(self, method):

        template = self.templates.get(method)
        if method in self.__dict__:
            template = self.__dict__[method]
        if method in self.templates:
            template = self.templates[method]
        else:
            raise AttributeError(f"'LaTeXFormatter' object has no template for '{method}'")

        def render_template(*args, **kwargs):
            if len(args) > 1:
                raise ValueError(f"Expected at most 1 argument, got {len(args)}")
            if args:
                kwargs['text'] = args[0]
            return template.render(**kwargs)
        return render_template

    def svg(self, svg):
        pdfpath = svg2pdf(svg)
        return f"\\includegraphics[width=1em]{{{pdfpath }}}"

    def codeblock(self, code, language='text', filename=None, lineno=False,
                  highlight=[]):
        return self.templates['codeblock'].render(
            code=code,
            language=language,
            linenos=lineno,
            highlight=optimize_list(highlight),
            filename=filename
        )

    def acronym(self, text, tag):
        self.acronyms[tag] = text
        return self.templates['acronym'].render(text=text, tag=tag)

    def keystroke(self, keys):
        return self.templates['keystroke'].render(keys=keys)

    def mermaid(self, code):
        return self.templates['codeblock'].render(
            code=code,
            language='text'
        )

class LaTeXRenderer:
    def __init__(self):
        self.formatter = LaTeXFormatter()

    def extract_code_block(self, soup):
        """Extract code block from a <div class="highlight"> object.
        Assumptions:
        - Filename may be in a span with class 'filename'
        - Lines are identified with span r'^__span-.*'
        - Links can be ignored
        - Other span elements: cp, w, cpf, kt, nf, p, mi
        are code elements, they can be merged.
        """

        if soup.name != 'div' and 'highlight' not in soup.get('class', []):
            return None

        language = get_code_language(soup)
        span_filename = soup.find(class_='filename')
        filename = span_filename.get_text() if span_filename else None
        has_lineno = bool(soup.find(class_='lineno'))

        listing = []
        hl_lines = []
        for code in soup.find_all("code"):
            for i, span_line in enumerate(code.find_all('span', id=lambda x: x and x.startswith('__'))):
                hl = span_line.find('span', class_='hll')
                if hl:
                    hl_lines.append(i + 1)
                    span_line = hl

                listing.append(''.join([span.get_text() for span in span_line.find_all('span')]))
        return {
            'language': language,
            'lineno': has_lineno,
            'filename': filename,
            'highlight': hl_lines,
            'code': '\n'.join(listing)
        }

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
            'columns': styles,
            'rows': table_data
        }

    def render_inlines(self, soup):
        tags = [
            'abbr', 'span', 'sub', 'ins', 'del', 'kbd', 'mark',
            'span', 'strong', 'em', 'code', 'a', 'sup']
        for inline in soup.find_all(tags):
            text = inline.get_text()
            mapper = {
                'sub': self.formatter.subscript,
                'sup': self.formatter.superscript,
                'ins': self.formatter.underline,
                'del': self.formatter.strikethrough,
                'mark': self.formatter.highlight,
                'strong': self.formatter.strong,
                'ul': self.formatter.underline,
                'em': self.formatter.italic,
                'kbd': self.formatter.keystroke,
            }
            if inline.name in mapper:
                inline.replace_with(mapper[inline.name](text))
                continue
            match inline.name:
                case 'abbr':
                    tag = text
                    description = inline.get('title', '')
                    inline.replace_with(self.formatter.acronym(tag, description))
                case 'a':
                    inline.replace_with('')

                case 'code':
                    language = get_code_language(inline)
                    inline.replace_with(
                        self.formatter.codeinline(text=text, language=language))
                case 'span':
                    classes = inline.get('class', [])
                    if 'twemoji' in classes:
                        if inline.children:
                            svg = next(inline.children)
                            if svg and svg.name == 'svg':
                                svg_code = svg.prettify()
                                inline.replace_with(
                                    self.formatter.svg(svg_code))
                            else:
                                raise ValueError(f"Expected svg, got {svg}")
                        else:
                            raise ValueError(f"No children in span")
                    elif 'arithmatex' in classes:
                        # Direct MathJax format, no need to process
                        inline.replace_with(text)
                    elif 'keys' in classes:
                        keys = []
                        for key in inline.find_all('kbd'):
                            key_class = get_class(key, re.compile(r'^key-(.*)$'))
                            if not key_class:
                                log.warning(f"Unknown key type: {key.get('class', [])}")
                            keys.append(key_class[4:])
                        inline.replace_with(self.formatter.keystroke(keys))
                    elif 'critic' in classes:
                        # Critic markup
                        if 'add' in classes:
                            inline.replace_with(self.formatter.add(text))
                        elif 'del' in classes:
                            inline.replace_with(self.formatter.delete(text))
                        elif 'comment' in classes:
                            inline.replace_with(self.formatter.comment(text))
                        else:
                            log.warning(f"Ignoring span {inline}")
                    else:
                        log.warning(f"Ignoring span {inline}")
                case _:
                    raise ValueError(f"Unknown tag: {inline.name}")

    def render(self, html, base_level=0):
        soup = BeautifulSoup(html, 'html.parser')

        # Start with more sensible elements: codeblocks
        # They contains a lot of inline elements that need to be processed first
        for el in soup.find_all('div', class_=['highlight']):
            if code := self.extract_code_block(el):
                el.replace_with(self.formatter.codeblock(**code))

        # All inline (strong, italic...) elements are processed here
        self.render_inlines(soup)

        # Headings
        for inline in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            title = inline.get_text()
            level = int(inline.name[1:]) + base_level
            ref = inline.get('id', None)
            inline.replace_with(self.formatter.heading(title, level=level, ref=ref))

        # Lists
        for ul in soup.find_all('ul'):
            items = []
            for li in ul.find_all('li'):
                items.append(li.get_text())
            ul.replace_with(self.formatter.unordered_list(items=items))

        for ol in soup.find_all('ol'):
            items = []
            for li in ul.find_all('li'):
                items.append(li.get_text())
            ol.replace_with(self.formatter.ordered_list(items=items))

        for dl in soup.find_all(['dl']):
            items = []
            title = None
            for el in soup.find_all(['dt', 'dd']):
                if el.name == 'dt':
                    title = el.get_text()
                elif el.name == 'dd':
                    content = el.get_text()
                    items.append((title, content))

            dl.replace_with(self.formatter.description_list(items=items))

        for math_block in soup.find_all(['div'], class_='arithmatex'):
            math_block.replace_with(f"\n{math_block.get_text()}\n")

        for table in soup.find_all(['table']):
            data = self.extract_table(table)
            if data:
                table.replace_with(self.formatter.table(**data))

        # Mermaid
        for mermaid in soup.find_all('pre', class_='mermaid'):
            code = mermaid.get_text()
            mermaid.replace_with(self.formatter.mermaid(code))

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
            admonition_title = admonition.find('p', class_='admonition-title')
            if title:
                title = admonition_title.get_text()

            content = admonition.get_text()
            admonition.replace_with(
                self.formatter.callout(content,
                                          title=admonition_title,
                                          type=admonition_type))

        # Eventually get rid of the p tags
        for p in soup.find_all('p'):
            p.replace_with(f"{p.get_text()}\n")

        document = unescape(str(soup).replace('&thinsp;', '~'))

        return self.formatter.template(content=document)
