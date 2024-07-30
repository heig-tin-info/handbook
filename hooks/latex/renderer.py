from bs4 import BeautifulSoup, NavigableString, ProcessingInstruction, Tag, PageElement
from .formatters import LaTeXFormatter
from pathlib import Path
from typing import Union
import re
from urllib.parse import quote
from hashlib import sha256
from html import unescape
from IPython import embed
from .transformers import fetch_image, image2pdf, svg2pdf, mermaid2pdf, drawio2pdf
import logging
from urllib.parse import quote, urlparse, urlunparse

log = logging.getLogger('mkdocs')

def resolve_asset_path(file_path, path):
    if file_path.name == 'index.md':
        file_path = file_path.parent
    path = (file_path / path).resolve()
    if not path.exists():
        return None
    return path

def safe_quote(url):
    parsed_url = urlparse(url)
    encoded_path = quote(parsed_url.path)
    encoded_query = quote(parsed_url.query)
    encoded_fragment = quote(parsed_url.fragment)
    return urlunparse((parsed_url.scheme, parsed_url.netloc, encoded_path, parsed_url.params, encoded_query, encoded_fragment))


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

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


class LaTeXRenderer:
    def __init__(self, output_path=Path('build')):
        self.formatter = LaTeXFormatter()
        self.output_path = Path(output_path) / 'assets'
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Rendering order
        self.renderering_order = [
            # AST Simplification
            self.discard_unwanted,
            self.render_hr,
            self.render_br,

            # Prior escaping LaTeX special characters
            self.render_codeblock,

            self.render_codeinline,
            self.render_math,
            self.render_math_block,
            self.render_regex,
            self.render_unicode,

            self.render_navigable_string,

            self.render_emoji,
            self.render_keystrokes,
            self.render_heading,
            self.render_autoref,
            self.render_footnotes,
            self.render_links,

            # After escaping LaTeX special characters
            self.render_abbreviation,
            self.render_list,
            self.render_description_list,

            self.render_admonition,
            self.render_mermaid,
            self.render_figure,
            self.render_table,
            self.render_inlines,
            self.render_format,

            # At last
            self.render_tabbed,
            self.render_columns,
            self.render_paragraph
        ]

        # Metadata
        self.abbreviations = {}
        self.acronyms = {}
        self.glossary = {}
        self.snippets = {}
        self.solutions = []
        self.exercise_counter = 0

        self.level = 0

    def get_filename_from_content(self, content: str):
        """Generate a filename from content.
        This renderer, store assets with files sometime
        generated from content. This function will generate
        a unique filename based on the content.
        """
        digest = sha256(content.encode()).hexdigest()
        return self.output_path / digest

    def discard_unwanted(self, soup: Tag, **kwargs):
        # Headerlink and Footnote-backref only useful on HTML
        for el in soup.find_all('a', class_=['headerlink', 'footnote-backref']):
            el.extract()

        # Glighbox plugin wraps images in a span, we don't need it
        for el in soup.find_all('a', class_=['glightbox']):
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

    def apply(self, element: PageElement, template, *args, **kwargs):
        latex = getattr(self.formatter, template)(*args, **kwargs)
        node = NavigableString(latex)
        node.processed = True
        element.replace_with(node)
        return node

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

    def render_navigable_string(self, soup: Tag, **kwargs):
        """Replace all NavigableString to escape LaTeX special characters.
        This should not be on code blocks, only on text elements.
        """
        for el in soup.find_all(string=True):
            if el.find_parent('code'):
                continue  # Skip

            if getattr(el, 'processed', False):
                continue  # Skip

            # Escape LaTeX string only once
            text = el.get_text()
            text = escape_latex_chars(text)
            el.replace_with(text)
        return soup

    def render_unicode(self, soup: Tag, **kwargs):
        """Display a unicode char code."""
        for a in soup.find_all('a', class_=['ycr-unicode']):
            code = f"U+{self.get_safe_text(a)}"
            self.apply(a, 'href',
                       code,
                       url=safe_quote(a.get('href', '')))
        return soup

    def render_regex(self, soup: Tag, **kwargs):
        """Replace all regex elements with LaTeX formatted strings.
        This is not markdown standard, YCR uses the syntax `:regex:...`
        plugin will replace with:

        <a href="https://regex101.com/?regex='...'&flags=...&flavor=pcre2"
            class="ycr-regex" target="_blank">/.../</a>
        """
        for a in soup.find_all('a', class_=['ycr-regex']):
            code = self.get_safe_text(a)
            code = code.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')
            self.apply(a, 'regex',
                       code,
                       url=safe_quote(a.get('href', '')))
        return soup

    def render_codeinline(self, soup: Tag, **kwargs):
        """Extract code from a <code> object."""

        def find_safe_delimiter(text):
            delimiters = ['|', '@', '?', '~']
            for delimiter in delimiters:
                if text.count(delimiter) % 2 == 0:
                    return delimiter
            raise ValueError("No safe delimiter found")

        for el in soup.find_all('code'):
            # Skip mermaid
            if el.find_parent('pre', class_='mermaid'):
                continue

            if get_class(el, 'highlight'):
                code = ''.join([e.get_text() for e in el.find_all('span')])
            else:
                code = self.get_safe_text(el)
            language = self.get_code_language(el)

            code = code.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')

            self.apply(el, 'codeinline', code, language=language,
                       delimiter=find_safe_delimiter(code))
        return soup

    def render_mermaid(self, soup: Tag, **kwargs):
        """Extract mermaid diagrams from a <code> object
        to be rendered as images."""
        for el in soup.find_all('pre', class_=['mermaid']):
            code = el.find('code')
            if not code:
                raise ValueError("No code block found in mermaid")

            diagram = self.get_safe_text(code)
            filename = mermaid2pdf(diagram, self.output_path)

            template = 'figure_tcolorbox' if \
                kwargs.get('tcolorbox', False) else 'figure'
            self.apply(el, template,
                       path=filename.name)
        return soup

    def render_codeblock(self, soup: Tag, **kwargs):
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

            code = el.find("code")

            if not code:
                raise ValueError("No code block found in codeblock")

            listing = []
            highlight = []
            spans = code.find_all('span', id=lambda x: x and x.startswith('__'))
            for i, span_line in enumerate(spans):
                if hl := span_line.find('span', class_='hll'):
                    highlight.append(i + 1)
                    span_line = hl
                #tokens = span_line.find_all('span')
                listing.append(span_line.get_text())

            self.apply(el, 'codeblock', code=''.join(listing),
                       language=language, lineno=lineno, filename=filename,
                       highlight=highlight)
        return soup

    def render_heading(self, soup: Tag, **kwargs):
        base_level = kwargs.get('base_level', 0)
        for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            self.render_inlines(el)
            title = self.get_safe_text(el)
            level = int(el.name[1:]) + base_level - 1
            ref = el.get('id', None)
            self.apply(el, 'heading', title, level=level, ref=ref)
        return soup

    def render_autoref(self, soup: Tag, **kwargs):
        for el in soup.find_all('span', attrs={'data-autorefs-identifier': True}):
            identifier = el.get('data-autorefs-identifier')
            self.render_inlines(el)
            text = self.get_safe_text(el)
            self.apply(el, 'ref', text, ref=identifier)
        return soup

    def render_math(self, soup: Tag, **kwargs):
        """Replace all math elements.

        <span class="arithmatex">...</span>
        """
        for el in soup.find_all('span', class_=['arithmatex']):
            text = self.get_safe_text(el)
            node = NavigableString(text)
            node.processed = True
            el.replace_with(node)
        return soup

    def render_math_block(self, soup: Tag, **kwargs):
        for math_block in soup.find_all(['div'], class_='arithmatex'):
            text = self.get_safe_text(math_block)
            node = NavigableString(f"\n{text}\n")
            node.processed = True
            math_block.replace_with(node)
        return soup

    def render_abbreviation(self, soup: Tag, **kwargs):
        for abbr in soup.find_all('abbr'):
            text = escape_latex_chars(abbr.get('title'))
            short = self.get_safe_text(abbr)
            short = escape_latex_chars(short)

            # Discard any special characters not allowed in glossary references
            tag = 'acr:' + re.sub(r'[^a-zA-Z0-9]', '', short).lower()

            self.acronyms[tag] = (short, text)
            self.apply(abbr, 'acronym', tag)
        return soup

    def render_emoji(self, soup: Tag, **kwargs):
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
            self.apply(img, 'icon', filename)

        for span in soup.find_all('span', class_=['twemoji']):
            svg = span.find('svg')
            if not svg:
                raise ValueError("Expected SVG element in twemoji")
            svgdata = str(svg)
            filename = svg2pdf(svgdata, self.output_path)
            self.apply(span, 'icon', filename)
        return soup

    def render_critics(self, soup: Tag, **kwargs):
        """Critics from CriticMarkup are rendered as follows"""

        # Strikethrough with red background
        for el in soup.find_all('del', class_=['critic']):
            self.render_inlines(el)
            self.apply(el, 'deletion', self.get_safe_text(el))

        # Underline with green background
        for el in soup.find_all('ins', class_=['critic']):
            self.render_inlines(el)
            self.apply(el, 'addition', self.get_safe_text(el))

        # Gray with /* */ comment
        for el in soup.find_all('span', class_=['critic', 'comment']):
            self.render_inlines(el)
            self.apply(el, 'comment', self.get_safe_text(el))

        # Substitution
        for el in soup.find_all('span', class_=['critic', 'subst']):
            raise NotImplementedError("Substitution not implemented")

        # Highlight
        for el in soup.find_all('mark', class_=['critic']):
            self.render_inlines(el)
            self.apply(el, 'highlight', self.get_safe_text(el))
        return soup

    def render_keystrokes(self, soup: Tag, **kwargs):
        for span in soup.find_all('span', class_='keys'):
            keys = []
            for key in span.find_all(['kbd']):
                key_class = get_class(key, re.compile(r'^key-(.*)$'))
                if key_class:
                    keys.append(key_class[4:])
                else:
                    keys.append(self.get_safe_text(key))
            self.apply(span, 'keystroke', keys)
        return soup

    def render_format(self, soup: Tag, **kwargs):
        mapper = {
            'del': 'strikethrough',
            'em': 'italic',
            'ins': 'underline',
            'mark': 'highlight',
            'strong': 'strong',
            'sub': 'subscript',
            'sup': 'superscript',
        }

        for el in soup.find_all(mapper.keys(), class_=False):
            if not el.parent:
                continue

            if el.name == 'sup' and el.get('id'):
                # This is a footnote, we will handle it later
                continue

            el = self.render_inlines(el)
            text = self.get_safe_text(el)
            self.apply(el, mapper[el.name], text)
        return soup

    def render_footnotes(self, soup: Tag, **kwargs):
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
            self.apply(el, 'footnote', footnotes[footnote_id])
        return soup

    def render_list(self, soup: Tag, **kwargs):
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
                    self.apply(el, 'ordered_list', items=items)
                case 'ul':
                    if has_checkbox:
                        self.apply(el, 'choices', items=zip(checkboxes, items))
                    else:
                        self.apply(el, 'unordered_list', items=items)
        return soup

    def render_description_list(self, soup: Tag, **kwargs):
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

            self.apply(dl, 'description_list', items=items)
        return soup

    def render_tabbed(self, soup: Tag, **kwargs):
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
                self.apply(tab, 'tabbed', content, title=titles[i])
            tabbed_content.unwrap()

            for el in div.find_all(['input'], recursive=False):
                el.extract()
            for el in div.find_all(['div'], class_=['tabbed-labels']):
                el.extract()
            div.unwrap()
        return soup

    def render_figure(self, soup: Tag, **kwargs):
        for figure in soup.find_all(['figure']):
            image = figure.find('img')
            if not image:
                raise ValueError(f"Missing image in figure {figure}")
            image_src = image.get('src')
            if not image_src:
                raise ValueError(f"Missing src in image {image}")
            if is_valid_url(image_src):
                filename = fetch_image(image_src, self.output_path)
            else:
                filepath = resolve_asset_path(kwargs.get('file_path', Path()), image_src)
                if not filepath:
                    raise ValueError(f"Image not found: {image_src}")
                match filepath.suffix:
                    case '.svg':
                        filename = svg2pdf(filepath, self.output_path)
                    case '.drawio':
                        filename = drawio2pdf(filepath, self.output_path)
                    case _:
                        filename = image2pdf(filepath, self.output_path)

            caption = figure.find('figcaption')
            self.render_inlines(caption)
            caption_text = self.get_safe_text(caption) \
                if caption else image.get('alt', '')

            label = None
            if label_id := figure.get('id'):
                label = f"{label_id}"

            template = 'figure_tcolorbox' if \
                kwargs.get('tcolorbox', False) else 'figure'
            self.apply(figure, template,
                       caption=caption_text, path=filename.name, label=label)
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

    def render_table(self, soup: Tag, **kwargs):
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
            if caption_element := table.find('caption'):
                caption_element = self.render_inlines(caption_element, **kwargs)
                caption = self.get_safe_text(caption_element)
                caption_element.extract()
            else:
                caption = None

            label = None
            if label_id := table.get('id'):
                label = f"{label_id}"

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

            self.apply(table, 'table', columns=styles[0], rows=table_data, caption=caption, label=label)

    def render_admonition(self, soup: Tag, **kwargs):
        # Admonitions with callout
        for admonition in soup.find_all(['div'], class_='admonition'):
            if not admonition.parent:
                continue

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


            # Exercise solution
            # if solution_el := admonition.find('div', class_=['details', 'solution']):
            #     if solution_el.find('summary'):
            #         solution_el.find('summary').extract()
            #     solution = self.get_safe_text(solution_el)
            #     self.solutions.append((title, solution))
            #     admonition_type = 'solution'

            # Treat figures in admonitions differently
            # Tcolorbox does not support figure environments
            admonition = self.render_figure(admonition,
                                            tcolorbox=True, **kwargs)
            admonition = self.render_mermaid(admonition, tcolorbox=True, **kwargs)


            admonition = self.render_after(self.render_admonition,
                                           admonition, **kwargs)
            content = self.get_safe_text(admonition)

            self.apply(admonition, 'callout', content,
                       title=title, type=admonition_type)

        # Foldable admonitions are implemented with details/summary
        for admonition in soup.find_all(['details']):
            if not admonition.parent:
                continue
            classes = admonition.get('class', [])
            if len(classes) > 1:
                raise ValueError(f"Multiple classes in details: {classes}")
            admonition_type = classes[0]

            if summary := admonition.find('summary'):
                title = self.get_safe_text(summary)
                summary.extract()

            # Treat figures in admonitions differently
            # Tcolorbox does not support figure environments
            admonition = self.render_figure(admonition,
                                            tcolorbox=True, **kwargs)
            admonition = self.render_mermaid(admonition, tcolorbox=True, **kwargs)

            admonition = self.render_after(self.render_admonition, admonition, **kwargs)
            content = self.get_safe_text(admonition)

            self.apply(admonition, 'callout', content,
                       title=title, type=admonition_type)
        return soup

    def render_autoref(self, soup: Tag, **kwargs):
        for el in soup.find_all('autoref', attrs={'identifier': True}):
            tag = el.get('identifier')
            text = self.get_safe_text(el)
            self.apply(el, 'ref', text, ref=tag)

    def render_links(self, soup: Tag, **kwargs):
        for el in soup.find_all('a'):
            self.render_inlines(el)
            self.render_abbreviation(el)
            text = self.get_safe_text(el)
            href = el.get('href', '')
            if href.startswith('http'):
                href = escape_latex_chars(safe_quote(el.get('href')))
                self.apply(el, 'href', text=text, url=href)
            elif href.startswith('#'):
                self.apply(el, 'ref', text, ref=href[1:])
            elif href == '' and el.get('id'):
                self.apply(el, 'label', el.get('id'))
            elif path := resolve_asset_path(kwargs.get('file_path', Path()), href):
                digest = sha256(href.encode()).hexdigest()
                self.snippets[digest] = path
                self.apply(el, 'ref', text='extrait', path=digest)
            else:
                raise NotImplementedError("Local links not implemented")
        return soup

    def render_columns(self, soup: Tag, **kwargs):
        for div in soup.find_all(['div'], class_='two-column-list'):
            self.apply(div, 'multicolumn', self.get_safe_text(div), columns=2)

        for div in soup.find_all(['div'], class_='three-column-list'):
            self.apply(div, 'multicolumn', self.get_safe_text(div), columns=3)

    def render_inlines(self, soup: Tag, **kwargs):
        """Replace all inline elements."""

        self.render_abbreviation(soup)
        self.render_critics(soup)
        self.render_format(soup)
        self.render_paragraph(soup)
        return soup

    def render_paragraph(self, soup: Tag, **kwargs):
        for p in soup.find_all('p', class_=False):
            self.render_inlines(p)
            text = self.get_safe_text(p)
            p.replace_with(text + '\n')

    def render_grid_cards(self, soup: Tag, **kwargs):
        for div in soup.find_all(['div'], class_='grid-cards'):
            div.unwrap()

    def render_hr(self, soup: Tag, **kwargs):
        for el in soup.find_all('hr'):
            el.extract()
        return soup

    def render_br(self, soup: Tag, **kwargs):
        for el in soup.find_all('br'):
            node = NavigableString('\\newline\n')
            node.processed = True
            el.replace_with(node)
        return soup

    def render_after(self, function, soup: Tag, **kwargs):
        index = self.renderering_order.index(function)
        for render in self.renderering_order[index:]:
            render(soup, **kwargs)
        return soup

    def get_list_acronyms(self):
        acronyms = [(tag, short, text)
                    for tag, (short, text) in self.acronyms.items()]
        return self.formatter.list_acronyms(acronyms)

    def render(self, html, output_path, file_path, base_level=0):
        soup = BeautifulSoup(html, 'html.parser')

        kwargs = {
            'file_path': file_path,
            'output_path': output_path,
            'base_level': base_level
        }

        for render in self.renderering_order:
            render(soup, **kwargs)

        # Unwrap remaining div
        for div in soup.find_all(['div']):
            div.unwrap()

        return unescape(str(soup).replace(' ', '~'))
