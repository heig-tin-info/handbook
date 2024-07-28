from bs4 import BeautifulSoup, NavigableString, ProcessingInstruction, Tag, PageElement
from .formatters import LaTeXFormatter
from pathlib import Path
from typing import Union
import re
from urllib.parse import quote
from hashlib import sha256
import requests
import mimetypes
from html import unescape
from IPython import embed
from .transformers import fetch_image, image2pdf, svg2pdf

def get_class(element, pattern: Union[str, re.Pattern]):
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    return next((c for c in element.get('class', [])
                 if pattern.match(c)), None)

def get_depth(element: PageElement):
    depth = 0
    while element.parent is not None:
        element = element.parent
        depth += 1
    return depth

def find_all_dfs(soup: Tag, *args, **kwargs):
    items = []
    for el in soup.find_all(*args, **kwargs):
        level = get_depth(el)
        items.append((level, el))
    return [item for _, item in sorted(items, key=lambda x: x[0], reverse=True)]


def image2pdf(filename, output_path=Path()):
    log.info("Converting webp to PDF...")

    pdfpath = output_path / get_filename(filename).with_suffix('.pdf')

    if not pdfpath.exists() or pdfpath.stat().st_mtime < filename.stat().st_mtime:
        log.debug('Running command:')
        image = Image.open(filename)
        image.save(pdfpath, 'PDF')

    return pdfpath

def escape_latex_chars(text):
    mapping = [
        ('&', r'\&'),
        ('%', r'\%'),
        ('#', r'\#'),
        ('$', r'\$'),
        ('_', r'\_'),
        ('\\', r'\textbackslash'),
    ]
    return ''.join([c if c not in dict(mapping) else dict(mapping)[c]
                    for c in text])

class LaTeXString(NavigableString):
    """Same as NavigableString, but escapes LaTeX special characters.
    Replaced NavigableString with LaTeXString indicates that the string
    is ready to be rendered in LaTeX."""
    def __new__(cls, value, escape=False):
        if escape:
            value = escape_latex_chars(value)
        return super().__new__(cls, value)

    def get_text(self, separator='', strip=False):
        return str(self)

class LaTeXRenderer:
    def __init__(self, output_path=Path('build')):
        self.formatter = LaTeXFormatter()
        self.output_path = Path(output_path) / 'assets'
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Metadata
        self.abbreviations = {}
        self.acronyms = {}
        self.glossary = {}

        self.level = 0

    def get_filename_from_content(self, content: str):
        """Generate a filename from content.
        This renderer, store assets with files sometime
        generated from content. This function will generate
        a unique filename based on the content.
        """
        digest = sha256(content.encode()).hexdigest()
        return self.output_path / digest

    def discard_unwanted(self, soup: Tag):
        # Headerlink and Footnote-backref only useful on HTML
        for el in soup.find_all('a', class_=['headerlink', 'footnote-backref']):
            el.extract()

        # Glighbox plugin wraps images in a span, we don't need it
        for el in soup.find_all('span', class_=['glightbox']):
            el.unwrap()
        return soup

    def get_safe_text(self, element: Union[PageElement, NavigableString]):
        """Extract text from a PageElement object.
        This is a recursive function that will extract text from
        all children elements.

        Expected no Tag objects, only NavigableString
        """
        if not all(isinstance(c, NavigableString) for c in element.children):
            raise ValueError("Expected only NavigableString children")

        return element.get_text()

    def get_code_language(self, soup: Tag):
        """Extract code language from a Tag object.
        They should be in the form of 'language-<lang>'.
        """
        prefix = 'language-'
        if 'highlight' not in soup.get('class', []):
            return None
        return next((c[len(prefix):]
                    for c in soup.get('class', [])
                    if c.startswith(prefix)), 'text') or 'text'

    def render_litterals(self, s: str):
        """ Markdown SmartSymbols extension offers support
        for litteral, they are not all supported in LaTeX. So they
        need to be replaced accordingly.
        """
        mapping = {
            '½': '\\nicefrac{1}{2}', '¼': '\\nicefrac{1}{4}',
            '¾': '\\nicefrac{3}{4}', '⅓': '\\nicefrac{1}{3}',
            '⅔': '\\nicefrac{2}{3}', '⅛': '\\nicefrac{1}{8}',
            '⅜': '\\nicefrac{3}{8}', '⅝': '\\nicefrac{5}{8}',
            '⅞': '\\nicefrac{7}{8}', '⅕': '\\nicefrac{1}{5}',
            '⅖': '\\nicefrac{2}{5}', '⅗': '\\nicefrac{3}{5}',
            '⅘': '\\nicefrac{4}{5}', '⅙': '\\nicefrac{1}{6}',
            '⅚': '\\nicefrac{5}{6}'
        }
        # Litteral chars
        for key, value in mapping.items():
            s = s.replace(key, value)

        # Litteral fractions e.g. 23/43 -> \nicefrac{23}{43}
        s = re.sub(r'\b(\d+)\/(\d+)\b', r'\\nicefrac{\1}{\2}', s)

        return s

    def render_navigable_string(self, soup: Tag):
        """Replace all NavigableString to escape LaTeX special characters.
        This should not be on code blocks, only on text elements.
        """
        for el in soup.find_all(string=True):
            if not isinstance(el, NavigableString):
                continue
            # pylint: disable=unidiomatic-typecheck (Exact match)
            #print(el)
            if not isinstance(el, LaTeXString):
                print(el.get_text())
            #     # First escape all special characters
                # text = LaTeXString(el.get_text(), escape=True)
                # # Then replace litterals
                # text = LaTeXString(self.render_litterals(text))
                el.replace_with(LaTeXString(el.get_text()))
        return soup

    def render_regex(self, soup: Tag):
        """Replace all regex elements with LaTeX formatted strings.
        This is not markdown standard, YCR uses the syntax `:regex:...`
        plugin will replace with:

        <a href="https://regex101.com/?regex='...'&flags=...&flavor=pcre2"
            class="ycr-regex" target="_blank">/.../</a>
        """
        for a in soup.find_all('a', class_=['ycr-regex']):
            a.replace_with(self.formatter.regex(
                regex=self.get_safe_text(a),
                url=quote(a.get('href', ''), safe=':/?&=')))
        return soup

    def render_codeinline(self, soup: Tag):
        """Extract code from a <code> object."""
        for el in soup.find_all('code'):
            if get_class(el, 'highlight'):
                code = ''.join([e.get_text() for e in el.find_all('span')])
            else:
                code = self.get_safe_text(el)
            language = self.get_code_language(el)

            el.replace_with(
                LaTeXString(
                    self.formatter.codeinline(code, language=language)))
        return soup

    def render_mermaid(self, soup: Tag):
        """Extract mermaid diagrams from a <code> object
        to be rendered as images."""
        for el in soup.find_all('pre', class_=['mermaid']):
            code = el.find('code')
            if not code:
                raise ValueError("No code block found in mermaid")

            diagram = self.get_safe_text(code)
            filename = self.get_filename_from_content(diagram) / '.mmd.pdf'
            self.files[filename] = diagram

            el.replace_with(self.formatter.image(filename))
        return soup

    def render_codeblock(self, soup: BeautifulSoup):
        """Extract code block from a <div class="highlight"> object.
        Assumptions:
        - Filename may be in a span with class 'filename'
        - Lines are identified with span r'^__span-.*'
        - Links can be ignored
        - Other span elements: cp, w, cpf, kt, nf, p, mi
        are code elements, they can be merged.
        """
        for el in soup.find_all('div', class_=['highlight']):
            language = self.get_code_language(el)
            lineno = bool(soup.find(class_='linenos'))

            filename = None
            if el_filename := soup.find(class_='filename'):
                self.render_inlines(el_filename)
                filename = el_filename.get_text()

            code = soup.find("code")

            if not code:
                raise ValueError("No code block found in codeblock")

            listing = []
            highlight = []
            spans = code.find_all('span', id=lambda x: x and x.startswith('__'))
            for i, span_line in enumerate(spans):
                if hl := span_line.find('span', class_='hll'):
                    highlight.append(i + 1)
                    span_line = hl
                tokens = span_line.find_all('span')
                listing.append(''.join([span.get_text() for span in tokens]))

            el.replace_with(LaTeXString(self.formatter.codeblock(
                code='\n'.join(listing),
                language=language,
                lineno=lineno,
                filename=filename,
                highlight=highlight
            )))
        return soup

    def render_heading(self, soup: Tag, base_level=0):
        for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            self.render_inlines(el)
            title = self.get_safe_text(el)
            level = int(el.name[1:]) + base_level
            ref = el.get('id', None)
            el.replace_with(LaTeXString(self.formatter.heading(
                title,
                level=level, ref=ref)))
        return soup

    def render_autoref(self, soup: Tag):
        for el in soup.find_all('span', attrs={'data-autorefs-identifier': True}):
            identifier = el.get('data-autorefs-identifier')
            self.render_inlines(el)
            text = self.get_safe_text(el)
            el.replace_with(LaTeXString(self.formatter.ref(text, ref=identifier)))
        return soup

    def render_math(self, soup: Tag):
        """Replace all math elements.

        <span class="arithmatex">...</span>
        """
        for el in soup.find_all('span', class_=['arithmatex']):
            text = self.get_safe_text(el)
            el.replace_with(LaTeXString(text))
        return soup

    def render_math_block(self, soup: Tag):
        for math_block in soup.find_all(['div'], class_='arithmatex'):
            text = self.get_safe_text(math_block)
            math_block.replace_with(LaTeXString(f"\n{text}\n"))
        return soup

    def render_abbreviation(self, soup: Tag):
        for abbr in soup.find_all('abbr'):
            text = escape_latex_chars(abbr.get('title'))
            short = self.get_safe_text(abbr)
            short = escape_latex_chars(short)

            # Discard any special characters not allowed in glossary references
            tag = 'acr:' + re.sub(r'[^a-zA-Z0-9]', '', short).lower()

            self.acronyms[tag] = (short, text)
            abbr.replace_with(self.formatter.acronym(tag))
        return soup

    def render_emoji(self, soup: Tag):
        """ Twemoji can be rendered as inline SVG or CDN link.

        <img alt="🙋‍♂️" class="twemoji" src="img.svg" title=":man_raising_hand:"/>

        <span class="twemoji">
            <svg viewbox="0 0 24 24">
                <path></path>
            </svg>
        </span>
        """
        for img in soup.find_all('img', class_=['twemoji']):
            src = img.get('src')
            if not src.startswith('http'):
                raise ValueError(f"Expected URL, got {src}")
            filename = fetch_image(src, self.output_path)
            img.replace_with(self.formatter.icon(filename))

        for span in soup.find_all('span', class_=['twemoji']):
            svg = span.find('svg')
            if not svg:
                raise ValueError("Expected SVG element in twemoji")
            svgdata = str(svg)
            filename = svg2pdf(svgdata, self.output_path)
            span.replace_with(self.formatter.icon(filename))
        return soup

    def render_critics(self, soup: Tag):
        """Critics from CriticMarkup are rendered as follows"""

        # Strikethrough with red background
        for el in soup.find_all('del', class_=['critic']):
            self.render_inlines(el)
            el.replace_with(self.formatter.deletion(self.get_safe_text(el)))

        # Underline with green background
        for el in soup.find_all('ins', class_=['critic']):
            self.render_inlines(el)
            el.replace_with(self.formatter.addition(self.get_safe_text(el)))

        # Gray with /* */ comment
        for el in soup.find_all('span', class_=['critic', 'comment']):
            self.render_inlines(el)
            el.replace_with(self.formatter.comment(self.get_safe_text(el)))

        # Substitution
        for el in soup.find_all('span', class_=['critic', 'subst']):
            raise NotImplementedError("Substitution not implemented")

        # Highlight
        for el in soup.find_all('mark', class_=['critic']):
            self.render_inlines(el)
            el.replace_with(self.formatter.highlight(self.get_safe_text(el)))
        return soup

    def render_keystrokes(self, soup: Tag):
        for span in soup.find_all('span', class_='keys'):
            keys = []
            for key in span.find_all(['kbd']):
                key_class = get_class(key, re.compile(r'^key-(.*)$'))
                if key_class:
                    keys.append(key_class[4:])
                else:
                    keys.append(self.get_safe_text(key))
            span.replace_with(self.formatter.keystroke(keys))
        return soup

    def render_format(self, soup: Tag):
        mapper = {
            'del': self.formatter.strikethrough,
            'em': self.formatter.italic,
            'ins': self.formatter.underline,
            'mark': self.formatter.highlight,
            'strong': self.formatter.strong,
            'sub': self.formatter.subscript,
            'sup': self.formatter.superscript,
        }

        for el in soup.find_all(mapper.keys(), class_=False):
            if not el.parent:
                continue

            if el.name == 'sup' and el.get('id'):
                # This is a footnote, we will handle it later
                continue

            el = self.render_inlines(el)
            text = self.get_safe_text(el)
            el.replace_with(mapper[el.name](text))
        return soup

    def render_footnotes(self, soup: Tag):
        footnotes = {}
        for el in soup.find_all(['div'], class_='footnote'):
            for li in el.find_all('li'):
                footnote_id = re.sub(r'^fn:(\d+)', r'\1', li.get('id', ''))
                if not footnote_id:
                    raise ValueError(f"Missing id in footnote: {li}")
                self.render_inlines(li)
                footnotes[footnote_id] = self.get_safe_text(li)
            el.extract()

        for el in soup.find_all('sup', id=True):
            footnote_id = re.sub(r'^fnref:(\d+)', r'\1', el.get('id', ''))
            el.replace_with(self.formatter.footnote(footnotes[footnote_id]))
        return soup

    def render_list(self, soup: Tag):
        def is_checkbox(item):
            if item.startswith('[ ]'):
                return -1
            if item.startswith('[x]'):
                return 1
            return 0

        for el in find_all_dfs(soup, ['ol', 'ul']):
            items = []
            checkboxes = []
            for li in el.find_all('li'):
                self.render_inlines(li)
                text = self.get_safe_text(li)
                checkboxes.append(is_checkbox(text))
                items.append(text)

            has_checkbox = any(checkboxes)
            if has_checkbox:
                # Strip the checkbox litterals
                items = [item[4:] for item in items]

            match el.name:
                case 'ol':
                    el.replace_with(self.formatter.ordered_list(items=items))
                case 'ul':
                    if has_checkbox:
                        el.replace_with(self.formatter.choices(items=zip(checkboxes, items)))
                    else:
                        el.replace_with(self.formatter.unordered_list(items=items))
        return soup

    def render_description_list(self, soup: Tag):
        for dl in soup.find_all(['dl']):
            items = []
            title = None
            for el in soup.find_all(['dt', 'dd']):
                self.render_inlines(el)
                if el.name == 'dt':
                    title = self.get_safe_text(el)
                elif el.name == 'dd':
                    content = self.get_safe_text(el)
                    items.append((title, content))

            dl.replace_with(self.formatter.description_list(items=items))
        return soup

    def render_tabbed(self, soup: Tag):
        for div in soup.find_all(['div'], class_='tabbed-set'):
            # Get titles
            titles = []
            for label in div.find_all(['label']):
                self.render_inlines(label)
                titles.append(self.get_safe_text(label))

            # Get content
            tabbed_content = div.find('div', class_='tabbed-content')
            for i, tab in enumerate(tabbed_content.find_all(['div'], class_='tabbed-block')):
                self.render_inlines(tab)
                content = self.get_safe_text(tab)
                tab.replace_with(self.formatter.tabbed(content, title=titles[i]))
            tabbed_content.unwrap()

            for el in div.find_all(['input'], recursive=False):
                el.extract()
            for el in div.find_all(['div'], class_=['tabbed-labels']):
                el.extract()
            div.unwrap()
        return soup

    def render_figure(self, soup: Tag, file_path: Path):
        for figure in soup.find_all(['figure']):
            image = figure.find('img')
            if not image:
                raise ValueError(f"Missing image in figure {figure}")
            image_src = image.get('src')
            if not image_src:
                raise ValueError(f"Missing src in image {image}")
            if not image_src.startswith('http'):
                if file_path.name == 'index.md':
                    file_path = file_path.parent
                image_src = (file_path / image_src).resolve()
                if not image_src.exists():
                    raise ValueError(f"Image not found: {image_src}")
                filename = image2pdf(image_src, self.output_path)
            else:
                filename = fetch_image(image_src, self.output_path)

            caption = figure.find('figcaption')
            self.render_inlines(caption)
            caption_text = self.get_safe_text(caption) \
                if caption else image.get('alt', '')
            figure.replace_with(self.formatter.figure(
                caption=caption_text, path=filename))
        return soup

    def get_table_styles(self, cell):
        if not cell:
            return ''
        style = cell.get('style', '')
        if 'text-align: right' in style:
            return 'right'
        if 'text-align: center' in style:
            return 'center'
        return 'left'

    def render_table(self, soup: Tag):
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
        for table in soup.find_all(['table']):
            table_data = []
            styles = []
            for row in table.find_all('tr'):
                row_data = []
                row_styles = []
                cells = row.find_all(['td', 'th'])
                for cell in cells:
                    self.render_inlines(cell)
                    row_data.append(self.get_safe_text(cell).strip())
                    row_styles.append(self.get_table_styles(cell))
                table_data.append(row_data)
                styles.append(row_styles)

            table.replace_with(self.formatter.table(
                columns=styles[0],
                rows=table_data))

    def render_admonition(self, soup: Tag):
        # Admonitions with callout
        for admonition in soup.find_all(['div'], class_='admonition'):
            admonition = self.render_inlines(admonition)

            classes = admonition.get('class', [])
            filtered_classes = [cls for cls in classes if cls not in [
                'admonition', 'annotate', 'inline', 'end', 'left', 'right']]
            if len(filtered_classes) > 1:
                raise ValueError(
                    f"Multiple classes in admonition: {filtered_classes}")
            admonition_type = filtered_classes[0]
            if title_node := admonition.find('p', class_='admonition-title'):
                title = self.get_safe_text(title_node)
                title_node.extract()

            content = self.get_safe_text(admonition)

            admonition.replace_with(
                self.formatter.callout(content,
                                       title=title,
                                       type=admonition_type))

        # Foldable admonitions are implemented with details/summary
        for admonition in soup.find_all(['details']):
            self.render_inlines(admonition)
            classes = admonition.get('class', [])
            if len(classes) > 1:
                raise ValueError(f"Multiple classes in details: {classes}")
            admonition_type = classes[0]

            if summary := admonition.find('summary'):
                title = self.get_safe_text(summary)
                summary.extract()

            content = self.get_safe_text(admonition)

            admonition.replace_with(
                self.formatter.callout(content,
                                       title=title,
                                       type=admonition_type))
        return soup

    def render_links(self, soup: Tag):
        for a in soup.find_all('a'):
            self.render_inlines(a)
            text = self.get_safe_text(a)
            href = escape_latex_chars(quote(a.get('href')))
            if a.get('href', '').startswith('http'):
                a.replace_with(self.formatter.url(text, url=href))
            else:
                a.replace_with(f"\\href{{{href}}}{{{text}}}")
        return soup

    def render_inlines(self, soup: Tag):
        """Replace all inline elements."""

        self.render_critics(soup)
        self.render_format(soup)
        self.render_paragraph(soup)
        return soup

    def render_paragraph(self, soup: Tag):
        for p in soup.find_all('p', class_=False):
            self.render_inlines(p)
            text = self.get_safe_text(p)
            p.replace_with(text + '\n')

    def render(self, html, output_path, file_path, base_level=0):
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unwanted html elements such as headerlink and backrefs
        self.discard_unwanted(soup)

        # Contains a lot of tags, also spacing is important
        # Must be rendered first.
        self.render_codeblock(soup)

        # Mermaid diagrams are rendered front-end, they are not
        # they are inserted as <code> elements.
        self.render_mermaid(soup)

        # Formatted highlighted inline <code> can also contain
        # spans and special characters.
        self.render_codeinline(soup)

        # Math are just LaTeX strings, they are easy to render
        # but, they should not be escaped.
        self.render_math(soup)
        self.render_math_block(soup)

        # # YCR-Regex are inline regex that points to regex101
        # # The they need to be rendered before escaping.
        # self.render_regex(soup)

        # Emoji (Twemoji) are inline SVG or CDN links
        # They are converted to inline images.
        self.render_emoji(soup)

        ## Keystrokes
        self.render_keystrokes(soup)

        self.render_heading(soup, base_level)
        # self.render_autoref(soup)
        # self.render_footnotes(soup)
        # self.render_links(soup)

        # All navigables strings can safely be escaped
        # This render litterals as well (Smart Symbols)
        self.render_navigable_string(soup)

        self.render_abbreviation(soup)

        self.render_list(soup)
        self.render_description_list(soup)
        self.render_tabbed(soup)
        self.render_figure(soup, file_path)
        self.render_table(soup)
        self.render_admonition(soup)

        # Inlines are bold, italic, critics, etc.
        self.render_inlines(soup)
        self.render_format(soup)
        self.render_paragraph(soup)
        return unescape(str(soup))
