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
import mimetypes
from html import unescape

log = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent

def fetch_image(url, output_path=Path()):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch image: {response.status_code}")

    mime_type = response.headers['Content-Type']
    extension = mimetypes.guess_extension(mime_type)
    if not extension:
        raise ValueError(f"Unknown mime type: {mime_type}")
    content = response.content
    filename = output_path / (sha256(content).hexdigest() + extension)
    with open(filename, 'wb') as fp:
        fp.write(content)
    return filename

def get_class(element, regex):
    return next((c for c in element.get('class', []) if regex.match(c)), None)

def svg2pdf(svg, output_path=Path()):
    # Create temporary svg file
    filename = Path(sha256(svg.encode()).hexdigest() + '.svg')
    svgpath = Path(os.path.join(tempfile.mkdtemp(), filename))
    with open(svgpath, 'w') as fp:
        fp.write(svg)

    pdfpath = output_path / filename.with_suffix('.pdf')

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
            '--export-area-drawing',
            '--export-dpi', '300',
            '--export-pdf',
            pdfpath,
            svgpath
            ]
    else:
        command = [
            'inkscape', svgpath,
            '--export-area-drawing',
            '--export-dpi', '300',
            '--export-type=pdf',
            '--export-filename',
            pdfpath
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

def get_depth(element):
    depth = 0
    while element.parent is not None:
        element = element.parent
        depth += 1
    return depth

def find_all_dfs(soup, *args, **kwargs):
    items = []
    for el in soup.find_all(*args, **kwargs):
        level = get_depth(el)
        items.append((level, el))
    return [item for _, item in sorted(items, key=lambda x: x[0], reverse=True)]

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
        self.output_path = Path()
        self.acronyms = {}

    def set_output_path(self, path):
        self.output_path = path

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
        pdfpath = svg2pdf(svg, self.output_path)
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

    def acronym(self, tag, text):
        self.acronyms[tag] = text
        return self.templates['acronym'].render(text=text, tag=tag.lower())

    def keystroke(self, keys):
        return self.templates['keystroke'].render(keys=keys)

    def mermaid(self, code):
        return self.templates['codeblock'].render(
            code=code,
            language='text'
        )

    def figure(self, caption, path):
        if (path.startswith('http')):
            path = fetch_image(path, self.output_path)
        return self.templates['figure'].render(caption=caption, path=path)

    def get_glossary(self):
        acronyms = [(tag.lower(), tag, text) for tag, text in self.acronyms.items()]

        return self.templates['glossary'].render(glossary=acronyms)

class LaTeXRenderer:
    def __init__(self, output_path=Path('build')):
        self.formatter = LaTeXFormatter()
        self.formatter.set_output_path(output_path)

    def extract_code_inline(self, soup):
        if soup.name != 'code' and 'highlight' not in soup.get('class', []):
            raise ValueError(f"Expected code block, got {soup.name} {soup.get('class', [])}")

        language = get_code_language(soup)
        listing = []
        for code in soup.find_all("code"):
            for i, span_line in enumerate(code.find_all('span', id=lambda x: x and x.startswith('__'))):
                listing.append(''.join([span.get_text() for span in span_line.find_all('span')]))
        return {
            'language': language,
            'code': '\n'.join(listing)
        }

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
        has_lineno = bool(soup.find(class_='linenos'))

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

    def render_format(self, soup):
        mapper = {
            'del': self.formatter.strikethrough,
            'em': self.formatter.italic,
            'ins': self.formatter.underline,
            'mark': self.formatter.highlight,
            'strong': self.formatter.strong,
            'sub': self.formatter.subscript,
            'sup': self.formatter.superscript,
        }
        for el in soup.find_all(mapper.keys()):
            if el.name == 'sup' and el.get('id'):
                # This is a footnote, we will handle it later
                continue
            el.replace_with(mapper[el.name](el.get_text()))

    def render_inlines(self, soup):
        for inline in soup.find_all(['pre', 'abbr', 'span', 'span', 'a']):
            text = inline.get_text()
            match inline.name:
                case 'abbr':
                    inline.replace_with(
                        self.formatter.acronym(text,
                                               inline.get('title', '')))
                case 'a':
                    if 'headerlink' in inline.get('class', []):
                        inline.extract()
                    elif 'footnote-backref' in inline.get('class', []):
                        inline.extract()
                    elif 'glightbox' in inline.get('class', []):
                        inline.unwrap()

                case 'pre':
                    if 'mermaid' in inline.get('class', []):
                        code = inline.find('code').get_text()
                        inline.replace_with(self.formatter.mermaid(code))

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
                    elif 'critic' in classes:
                        # Critic markup
                        if 'add' in classes:
                            inline.replace_with(self.formatter.add(text))
                        elif 'del' in classes:
                            inline.replace_with(self.formatter.delete(text))
                        elif 'comment' in classes:
                            inline.replace_with(self.formatter.comment(text))
                        else:
                            log.warning(f"Ignoring critic span {inline}")
                    else:
                        log.warning(f"Ignoring span {self.get_route(inline)} {inline}")
                case _:
                    raise ValueError(f"Unknown tag: {inline.name}")

    def render_smart_symbols(self, str):
        mapping = {
            '½': '\\nicefrac{1}{2}',
            '¼': '\\nicefrac{1}{4}',
            '¾': '\\nicefrac{3}{4}',
            '⅓': '\\nicefrac{1}{3}',
            '⅔': '\\nicefrac{2}{3}',
            '⅛': '\\nicefrac{1}{8}',
            '⅜': '\\nicefrac{3}{8}',
            '⅝': '\\nicefrac{5}{8}',
            '⅞': '\\nicefrac{7}{8}',
            '⅕': '\\nicefrac{1}{5}',
            '⅖': '\\nicefrac{2}{5}',
            '⅗': '\\nicefrac{3}{5}',
            '⅘': '\\nicefrac{4}{5}',
            '⅙': '\\nicefrac{1}{6}',
            '⅚': '\\nicefrac{5}{6}'
        }
        for key, value in mapping.items():
            str = str.replace(key, value)

        str = re.sub(r'\b(\d+)\/(\d+)\b', r'\\nicefrac{\1}{\2}', str)

        return str

    def render(self, html, output_path, base_level=0):
        soup = BeautifulSoup(html, 'html.parser')


        # Code block
        for el in soup.find_all('div', class_=['highlight']):
            if code := self.extract_code_block(el):
                el.replace_with(self.formatter.codeblock(**code))

        # Code inline
        for el in soup.find_all('code', class_=['highlight']):
            if code := self.extract_code_inline(el):
                el.replace_with(
                    self.formatter.codeinline(**code))

        # Keystrokes
        for span in soup.find_all('span', class_='keys'):
            keys = []
            for key in span.find_all(['kbd']):
                key_class = get_class(key, re.compile(r'^key-(.*)$'))
                if not key_class:
                    log.warning(f"Unknown key type: {key.get('class', [])}")
                keys.append(key_class[4:])
            span.replace_with(self.formatter.keystroke(keys))

        # Strong, italic, underline, ...
        self.render_format(soup)

        # All inline
        self.render_inlines(soup)

        # Headings
        for inline in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            title = inline.get_text()
            level = int(inline.name[1:]) + base_level
            ref = inline.get('id', None)
            inline.replace_with(self.formatter.heading(title, level=level, ref=ref))

        # Get footnotes
        footnotes = {}
        for footnote in soup.find_all(['div'], class_='footnote'):
            for li in footnote.find_all('li'):
                footnote_id = re.sub(r'^fn:(\d+)', r'\1', li.get('id', ''))
                if not footnote_id:
                    raise ValueError(f"Missing id in footnote: {li}")
                footnotes[footnote_id] = li.get_text()
            footnote.extract()

        for sup in soup.find_all('sup', id=True):
            footnote_id = re.sub(r'^fnref:(\d+)', r'\1', sup.get('id', ''))
            sup.replace_with(self.formatter.footnote(footnotes[footnote_id]))

        # Lists must be processed deep first
        for el in find_all_dfs(soup, ['ol', 'ul']):
            items = [li.get_text() for li in el.find_all('li')]
            checkboxes = [
                {'[ ]': False, '[x]': True}.get(item[:3], False) for item in items
            ]
            match el.name:
                case 'ul':
                    if any([item.startswith('[ ]') or item.startswith('[x]') for item in items]):
                        items = [item[4:] for item in items]
                        el.replace_with(self.formatter.choices(items=zip(checkboxes, items)))
                    else:
                        el.replace_with(self.formatter.unordered_list(items=items))
                case 'ol':
                    el.replace_with(self.formatter.ordered_list(items=items))

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

        # Tabbed item rendered linearly
        for div in soup.find_all(['div'], class_='tabbed-set'):
            # Get titles
            titles = []
            for label in div.find_all(['label']):
                titles.append(label.get_text())

            # Get content
            tabbed_content = div.find('div', class_='tabbed-content')
            for i, tab in enumerate(tabbed_content.find_all(['div'], class_='tabbed-block')):
                content = tab.get_text()
                tab.replace_with(self.formatter.tabbed(content, title=titles[i]))
            tabbed_content.unwrap()

            for el in div.find_all(['input'], recursive=False):
                el.extract()
            for el in div.find_all(['div'], class_=['tabbed-labels']):
                el.extract()
            div.unwrap()

        for math_block in soup.find_all(['div'], class_='arithmatex'):
            math_block.replace_with(f"\n{math_block.get_text()}\n")

        for figure in soup.find_all(['figure']):
            image = figure.find('img')
            if not image:
                raise ValueError(f"Missing image in figure {figure}")
            image_src = image.get('src')
            caption = figure.find('figcaption')
            caption_text = caption.get_text() if caption else image.get('alt', '')
            figure.replace_with(self.formatter.figure(caption=caption_text, path=image_src))

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
            p.replace_with(f"{text}\n")

        document = unescape(str(soup).replace('&thinsp;', '~').replace(' ', '~'))

        return self.formatter.template(content=document, glossary=self.formatter.get_glossary())
