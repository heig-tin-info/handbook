import logging
import re
from hashlib import sha256
from html import unescape
from pathlib import Path
from typing import Union
from urllib.parse import quote, urlparse, urlunparse

import yaml
from bs4 import BeautifulSoup, NavigableString, PageElement, ProcessingInstruction, Tag
from IPython import embed

from .formatters import LaTeXFormatter
from .transformers import (
    drawio2pdf,
    fetch_image,
    get_pdf_page_sizes,
    image2pdf,
    mermaid2pdf,
    svg2pdf,
)

log = logging.getLogger("mkdocs")


def resolve_asset_path(file_path, path):
    if Path(file_path).name == "index.md":
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
    return urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            encoded_path,
            parsed_url.params,
            encoded_query,
            encoded_fragment,
        )
    )


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_class(element, pattern: Union[str, re.Pattern]):
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    return next((c for c in element.get("class", []) if pattern.match(c)), None)


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
        ("&", r"\&"),
        ("%", r"\%"),
        ("#", r"\#"),
        ("$", r"\$"),
        ("_", r"\_"),
        ("^", r"\^"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("\\", r"\textbackslash{}"),
    ]
    return "".join([c if c not in dict(mapping) else dict(mapping)[c] for c in text])


class LaTeXRenderer:
    def __init__(self, output_path=Path("build"), config={}):
        self.config = config
        self.formatter = LaTeXFormatter()
        self.output_path = Path(output_path) / "assets"
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Rendering order
        self.renderering_order = [
            # AST Simplification
            self.discard_unwanted,
            self.render_hr,
            self.render_br,
            # Prior escaping LaTeX special characters
            self.render_regex,
            self.render_codeblock,
            self.render_codeinline,
            self.render_math,
            self.render_math_block,
            self.render_unicode,
            self.render_navigable_string,
            self.render_emoji,
            self.render_keystrokes,
            self.render_tabbed,
            self.render_heading,
            self.render_epigraph,
            self.render_autoref,
            self.render_footnotes,
            self.render_links,
            # After escaping LaTeX special characters
            self.render_abbreviation,
            self.render_list,
            self.render_description_list,
            self.render_quote,
            self.render_admonition,
            self.render_mermaid,
            self.render_figure,
            self.render_table,
            self.render_inlines,
            self.render_format,
            # At last
            self.render_columns,
            self.render_paragraph,
        ]

        # Wiki links
        with open("links.yml") as f:
            self.links = yaml.load(f, Loader=yaml.FullLoader)
        self.wikimap = {
            value["url"]: {"key": key, **value}
            for key, value in self.links.get("wikipedia", {}).items()
        }

        # Metadata
        self.abbreviations = {}
        self.acronyms = {}
        self.glossary = {}
        self.snippets = {}
        self.solutions = []
        self.exercise_counter = 0

        self.assets_map = {}

        self.level = 0

    def discard_unwanted(self, soup: Tag, **kwargs):
        unwanted = [
            ("a", ["headerlink", "footnote-backref"], "extract"),
            ("a", ["glightbox"], "unwrap"),
            ("div", ["latex-ignore"], "extract"),
            ("span", ["exercise-title"], "unwrap"),
            ("div", ["exercise-checkbox"], "extract"),
            ("figure", ["mermaid-figure"], "extract"),
        ]

        for tag, classes, mode in unwanted:
            for el in soup.find_all(tag, class_=classes):
                if mode == "unwrap":
                    el.unwrap()
                elif mode == "extract":
                    el.extract()

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
        prefix = "language-"
        if "highlight" not in soup.get("class", []):
            return None
        return (
            next(
                (
                    c[len(prefix) :]
                    for c in soup.get("class", [])
                    if c.startswith(prefix)
                ),
                "text",
            )
            or "text"
        )

    def apply(self, element: PageElement, template, *args, **kwargs):
        latex = getattr(self.formatter, template)(*args, **kwargs)
        node = NavigableString(latex)
        node.processed = True
        element.replace_with(node)
        return node

    def render_litterals(self, s: str):
        """Markdown SmartSymbols extension offers support
        for litteral, they are not all supported in LaTeX. So they
        need to be replaced accordingly.
        """
        mapping = {
            "½": "\\nicefrac{1}{2}",
            "¼": "\\nicefrac{1}{4}",
            "¾": "\\nicefrac{3}{4}",
            "⅓": "\\nicefrac{1}{3}",
            "⅔": "\\nicefrac{2}{3}",
            "⅛": "\\nicefrac{1}{8}",
            "⅜": "\\nicefrac{3}{8}",
            "⅝": "\\nicefrac{5}{8}",
            "⅞": "\\nicefrac{7}{8}",
            "⅕": "\\nicefrac{1}{5}",
            "⅖": "\\nicefrac{2}{5}",
            "⅗": "\\nicefrac{3}{5}",
            "⅘": "\\nicefrac{4}{5}",
            "⅙": "\\nicefrac{1}{6}",
            "⅚": "\\nicefrac{5}{6}",
        }
        # Litteral chars
        for key, value in mapping.items():
            s = s.replace(key, value)

        # Litteral fractions e.g. 23/43 -> \nicefrac{23}{43}
        s = re.sub(r"\b(\d+)\/(\d+)\b", r"\\nicefrac{\1}{\2}", s)

        return s

    def render_navigable_string(self, soup: Tag, **kwargs):
        """Replace all NavigableString to escape LaTeX special characters.
        This should not be on code blocks, only on text elements.
        """
        for el in soup.find_all(string=True):
            if el.find_parent("code"):
                continue  # Skip

            if getattr(el, "processed", False):
                continue  # Skip

            # Escape LaTeX string only once
            text = el.get_text()
            text = escape_latex_chars(text)

            text = self.monkeypatch_hyphenation(text)

            el.replace_with(text)
        return soup

    def render_unicode(self, soup: Tag, **kwargs):
        """Display a unicode char code."""
        for a in soup.find_all("a", class_=["ycr-unicode"]):
            code = f"U+{self.get_safe_text(a)}"
            self.apply(a, "href", code, url=safe_quote(a.get("href", "")))
        return soup

    def render_regex(self, soup: Tag, **kwargs):
        """Replace all regex elements with LaTeX formatted strings.
        This is not markdown standard, YCR uses the syntax `:regex:...`
        plugin will replace with:

        <a href="https://regex101.com/?regex='...'&flags=...&flavor=pcre2"
            class="ycr-regex" target="_blank">/.../</a>
        """
        for a in soup.find_all("a", class_=["ycr-regex"]):
            if code_tag := a.find("code"):
                code = self.get_safe_text(code_tag)
            else:  # Fallback to text
                code = self.get_safe_text(a)

            code = code.replace("&", "\\&").replace("#", "\\#")
            self.apply(a, "regex", code, url=safe_quote(a.get("href", "")))
        return soup

    def render_codeinline(self, soup: Tag, **kwargs):
        """Extract code from a <code> object."""
        for el in soup.find_all("code"):
            # Skip mermaid
            if el.find_parent("pre", class_="mermaid"):
                continue

            if get_class(el, "highlight"):
                code = "".join([e.get_text() for e in el.find_all("span")])
            else:
                code = self.get_safe_text(el)
            language = self.get_code_language(el)

            code = escape_latex_chars(code).replace(" ", "~")

            self.apply(el, "codeinlinett", code)
        return soup

    def render_codeinline_old(self, soup: Tag, **kwargs):
        """Extract code from a <code> object.
        TeX doesn't like verb command inside arguments, so we cannot
        use mintinline anywhere. It limits the use, or conditionnaly replace it with
        textt where it is allowed... but it is not a good solution.
        """

        def find_safe_delimiter(text):
            delimiters = ["|", "@", "?", "~", "*", "£", "§"]
            for delimiter in delimiters:
                if delimiter not in text:
                    return delimiter
            raise ValueError("No safe delimiter found")

        for el in soup.find_all("code"):
            # Skip mermaid
            if el.find_parent("pre", class_="mermaid"):
                continue

            if get_class(el, "highlight"):
                code = "".join([e.get_text() for e in el.find_all("span")])
            else:
                code = self.get_safe_text(el)
            language = self.get_code_language(el)

            # code = code.replace('&', '\\&').replace('%', '\\%')
            # .replace('#', '\\#')

            self.apply(
                el,
                "codeinline",
                code,
                language=language,
                delimiter=find_safe_delimiter(code),
            )
        return soup

    def render_mermaid(self, soup: Tag, **kwargs):
        """Extract mermaid diagrams from a <code> object
        to be rendered as images."""
        for el in soup.find_all("pre", class_=["mermaid"]):
            code = el.find("code")
            if not code:
                code = el

            diagram = self.get_safe_text(code)

            caption = None
            if match := re.search(r"^%%\s*(.*?)\n", diagram):
                caption = match.group(1)

            kwargs = {}
            if mermaid_config := self.config.mermaid_config:
                kwargs["config_filename"] = self.config.project_dir / mermaid_config

            filename = mermaid2pdf(diagram, self.output_path, **kwargs)
            if not filename:
                raise ValueError("Mermaid diagram not rendered")

            self.assets_map[filename] = {
                "type": "mermaid",
                "inline": True,  # Inline content
            }
            template = (
                "figure_tcolorbox" if kwargs.get("tcolorbox", False) else "figure"
            )

            width, height = get_pdf_page_sizes(filename)

            # Naive scaling. Assume PDF page is 210mm x 297mm
            # With 30 + 40 mm margins, linewidth is 140 mm.
            if width > 140:
                # ratio = round(140 / width, 2)
                ratio = 1.0
                width = f"{ratio*100}%"
            else:
                width = f"{width}mm"

            self.apply(el, template, path=filename.name, caption=caption, width=width)

        return soup

    def render_epigraph(self, soup: Tag, **kwargs):
        for el in soup.find_all("blockquote", class_=["epigraph"]):
            if footer := el.find("footer"):
                self.render_inlines(footer)
                source = self.get_safe_text(footer)
                footer.extract()

            text = el.get_text()
            self.apply(el, "epigraph", text, source=source)
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
        for el in soup.find_all("div", class_=["highlight"]):
            language = self.get_code_language(el)
            lineno = bool(el.find(class_="linenos"))

            filename = None
            if el_filename := el.find(class_="filename"):
                self.render_inlines(el_filename)
                filename = el_filename.get_text()

            code = el.find("code")

            if not code:
                raise ValueError("No code block found in codeblock")

            listing = []
            highlight = []
            spans = code.find_all("span", id=lambda x: x and x.startswith("__"))
            for i, span_line in enumerate(spans):
                if hl := span_line.find("span", class_="hll"):
                    highlight.append(i + 1)
                    span_line = hl
                # tokens = span_line.find_all('span')
                listing.append(span_line.get_text())

            code = "".join(listing)

            def is_ascii_art(s):
                chars = "┌┬─┐"
                for c in chars:
                    if c in s:
                        return True
                return False

            baselinestretch = 0.5 if is_ascii_art(code) else None

            self.apply(
                el,
                "codeblock",
                code=code,
                language=language,
                lineno=lineno,
                filename=filename,
                highlight=highlight,
                baselinestretch=baselinestretch,
            )
        return soup

    def render_quote(self, soup: Tag, **kwargs):
        for el in soup.find_all(["blockquote"]):
            self.render_inlines(el)
            text = self.get_safe_text(el)
            self.apply(el, "blockquote", text)
        return soup

    def render_heading(self, soup: Tag, **kwargs):
        base_level = kwargs.get("base_level", 0)
        for el in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            self.render_inlines(el)
            title = self.get_safe_text(el)
            level = int(el.name[1:]) + base_level - 1
            ref = el.get("id", None)
            self.apply(
                el,
                "heading",
                title,
                level=level,
                ref=ref,
                numbered=kwargs.get("numbered", True),
            )
        return soup

    def render_autoref(self, soup: Tag, **kwargs):

        for el in soup.find_all("autoref", attrs={"identifier": True}):
            tag = el.get("identifier")
            text = self.get_safe_text(el)
            self.apply(el, "ref", text, ref=tag)

        for el in soup.find_all("span", attrs={"data-autorefs-identifier": True}):
            identifier = el.get("data-autorefs-identifier")
            self.render_inlines(el)
            text = self.get_safe_text(el)
            self.apply(el, "ref", text, ref=identifier)
        return soup

    def render_math(self, soup: Tag, **kwargs):
        """Replace all math elements.

        <span class="arithmatex">...</span>
        """
        for el in soup.find_all("span", class_=["arithmatex"]):
            text = self.get_safe_text(el)
            node = NavigableString(text)
            node.processed = True
            el.replace_with(node)
        return soup

    def render_math_block(self, soup: Tag, **kwargs):
        for math_block in soup.find_all(["div"], class_="arithmatex"):
            text = self.get_safe_text(math_block)
            node = NavigableString(f"\n{text}\n")
            node.processed = True
            math_block.replace_with(node)
        return soup

    def render_abbreviation(self, soup: Tag, **kwargs):
        for abbr in soup.find_all("abbr"):
            text = escape_latex_chars(abbr.get("title"))
            short = self.get_safe_text(abbr)

            # Discard any special characters not allowed in glossary references
            tag = "acr:" + re.sub(r"[^a-zA-Z0-9]", "", short).lower()

            self.acronyms[tag] = (short, text)
            self.apply(abbr, "acronym", tag)
        return soup

    def render_emoji(self, soup: Tag, **kwargs):
        """Twemoji can be rendered as inline SVG or CDN link.

        <img alt="🙋‍♂️" class="twemoji" src="img.svg" title=":man_raising_hand:"/>

        <span class="twemoji">
            <svg viewbox="0 0 24 24">
                <path></path>
            </svg>
        </span>
        """
        for img in soup.find_all("img", class_=["twemoji"]):
            src = img.get("src")
            if not src.startswith("http"):
                raise ValueError(f"Expected URL, got {src}")
            filename = fetch_image(src, self.output_path)
            self.assets_map[filename] = {"type": "twemoji", "url": src}
            self.apply(img, "icon", filename)

        for span in soup.find_all("span", class_=["twemoji"]):
            svg = span.find("svg")
            if not svg:
                raise ValueError("Expected SVG element in twemoji")
            svgdata = str(svg)
            filename = svg2pdf(svgdata, self.output_path)
            self.assets_map[filename] = {"type": "twemoji", "inline": True}
            self.apply(span, "icon", filename)
        return soup

    def render_critics(self, soup: Tag, **kwargs):
        """Critics from CriticMarkup are rendered as follows"""

        # Strikethrough with red background
        for el in soup.find_all("del", class_=["critic"]):
            self.render_inlines(el)
            self.apply(el, "deletion", self.get_safe_text(el))

        # Underline with green background
        for el in soup.find_all("ins", class_=["critic"]):
            self.render_inlines(el)
            self.apply(el, "addition", self.get_safe_text(el))

        # Gray with /* */ comment
        for el in soup.find_all("span", class_=["critic", "comment"]):
            self.render_inlines(el)
            self.apply(el, "comment", self.get_safe_text(el))

        # Substitution
        for el in soup.find_all("span", class_=["critic", "subst"]):
            raise NotImplementedError("Substitution not implemented")

        # Highlight
        for el in soup.find_all("mark", class_=["critic"]):
            self.render_inlines(el)
            self.apply(el, "highlight", self.get_safe_text(el))
        return soup

    def render_keystrokes(self, soup: Tag, **kwargs):
        for span in soup.find_all("span", class_="keys"):
            keys = []
            for key in span.find_all(["kbd"]):
                key_class = get_class(key, re.compile(r"^key-(.*)$"))
                if key_class:
                    keys.append(key_class[4:])
                else:
                    keys.append(self.get_safe_text(key))
            self.apply(span, "keystroke", keys)
        return soup

    def render_format(self, soup: Tag, **kwargs):
        mapper = {
            "del": "strikethrough",
            "em": "italic",
            "ins": "underline",
            "mark": "highlight",
            "strong": "strong",
            "sub": "subscript",
            "sup": "superscript",
        }

        for el in soup.find_all(mapper.keys(), class_=False):
            if not el.parent:
                continue

            if el.name == "sup" and el.get("id"):
                # This is a footnote, we will handle it later
                continue

            el = self.render_inlines(el)
            text = self.get_safe_text(el)
            self.apply(el, mapper[el.name], text)
        return soup

    def render_footnotes(self, soup: Tag, **kwargs):
        footnotes = {}
        for el in soup.find_all(["div"], class_="footnote"):
            for li in el.find_all("li"):
                footnote_id = re.sub(r"^fn:(\d+)", r"\1", li.get("id", ""))
                if not footnote_id:
                    raise ValueError(f"Missing id in footnote: {li}")
                self.render_inlines(li)
                footnotes[footnote_id] = self.get_safe_text(li)
            el.extract()

        for el in soup.find_all("sup", id=True):
            footnote_id = re.sub(r"^fnref:(\d+)", r"\1", el.get("id", ""))
            self.apply(el, "footnote", footnotes[footnote_id])
        return soup

    def render_list(self, soup: Tag, **kwargs):
        def is_checkbox(item):
            if item.startswith("[ ]"):
                return -1
            if item.startswith("[x]"):
                return 1
            return 0

        for el in find_all_dfs(soup, ["ol", "ul"]):
            items = []
            checkboxes = []
            for li in el.find_all("li"):
                self.render_inlines(li)
                text = self.get_safe_text(li)
                checkboxes.append(is_checkbox(text))
                items.append(text)

            has_checkbox = any(checkboxes)
            if has_checkbox:
                # Strip the checkbox litterals
                items = [item[4:] for item in items]

            checkboxes = [c > 0 for c in checkboxes]

            match el.name:
                case "ol":
                    self.apply(el, "ordered_list", items=items)
                case "ul":
                    if has_checkbox:
                        self.apply(el, "choices", items=zip(checkboxes, items))
                    else:
                        self.apply(el, "unordered_list", items=items)
        return soup

    def render_description_list(self, soup: Tag, **kwargs):
        for dl in soup.find_all(["dl"]):
            items = []
            title = None
            for el in dl.find_all(["dt", "dd"]):
                self.render_inlines(el)
                if el.name == "dt":
                    title = self.get_safe_text(el)
                elif el.name == "dd":
                    content = self.get_safe_text(el)
                    items.append((title, content))

            self.apply(dl, "description_list", items=items)
        return soup

    def get_heading_level(self, soup: Tag):
        """Iterate parents and ancestors to get current <h> level."""
        current = soup
        while current is not None:
            # Check current element
            if current.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                return int(current.name[1:])

            # Check previous siblings
            sibling = current.previous_sibling
            while sibling is not None:
                if sibling.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                    return int(sibling.name[1:])
                sibling = sibling.previous_sibling

            # Move to parent
            current = current.parent

        return None

    def render_tabbed(self, soup: Tag, **kwargs):
        for div in soup.find_all(["div"], class_="tabbed-set"):
            level = self.get_heading_level(div)
            # Get titles
            titles = []
            if tabbed_labels := div.find("div", class_="tabbed-labels"):
                for label in tabbed_labels.find_all(["label"]):
                    self.render_inlines(label)
                    titles.append(self.get_safe_text(label))
                tabbed_labels.extract()
            else:
                raise ValueError("Missing tabbed-labels")

            # Remove checkbox
            for el in div.find_all(["input"], recursive=False):
                el.extract()

            # Get content
            tabbed_content = div.find("div", class_="tabbed-content")
            for i, tab in enumerate(
                tabbed_content.find_all(["div"], class_="tabbed-block")
            ):
                heading = soup.new_tag(f"h{min(level + 1, 6)}")
                heading.string = titles[i]
                tab.insert_before(f"\n\\textbf{{{titles[i]}}}\\par\n")
                tab.unwrap()

            tabbed_content.unwrap()
            div.unwrap()
        return soup

    def render_figure(self, soup: Tag, **kwargs):
        for figure in soup.find_all(["figure"]):
            if get_class(figure, "mermaid-figure"):
                continue
            image = figure.find("img")
            if not image:
                raise ValueError(f"Missing image in figure {figure}")
            image_src = image.get("src")
            if not image_src:
                raise ValueError(f"Missing src in image {image}")
            if is_valid_url(image_src):
                filename = fetch_image(image_src, self.output_path)
                self.assets_map[filename] = {
                    "type": "image",
                    "source": image_src,
                }
            else:
                filepath = resolve_asset_path(
                    kwargs.get("file_path", Path()), image_src
                )
                if not filepath:
                    raise ValueError(f"Image not found: {image_src}")
                match filepath.suffix:
                    case ".svg":
                        filename = svg2pdf(filepath, self.output_path)
                        self.assets_map[filename] = {"type": "svg", "source": filepath}
                    case ".drawio":
                        filename = drawio2pdf(filepath, self.output_path)
                        self.assets_map[filename] = {
                            "type": "drawio",
                            "source": filepath,
                        }
                    case _:
                        filename = image2pdf(filepath, self.output_path)
                        self.assets_map[filename] = {
                            "type": "image",
                            "source": filepath,
                        }
            caption = figure.find("figcaption")
            short_caption = image.get("alt", "")
            self.render_inlines(caption)
            caption_text = self.get_safe_text(caption) if caption else short_caption

            if short_caption and len(caption) > len(short_caption):
                short_caption = None

            width = image.get("width", None)

            label = None
            if label_id := figure.get("id"):
                label = f"{label_id}"

            template = (
                "figure_tcolorbox" if kwargs.get("tcolorbox", False) else "figure"
            )
            self.apply(
                figure,
                template,
                caption=caption_text,
                shortcaption=short_caption,
                path=filename.name,
                label=label,
                width=width,
            )
        return soup

    def get_table_styles(self, cell):
        if not cell:
            return ""
        style = cell.get("style", "")
        if "text-align: right" in style:
            return "right"
        if "text-align: center" in style:
            return "center"
        return "left"

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
        for table in soup.find_all(["table"]):
            if caption_element := table.find("caption"):
                caption_element = self.render_inlines(caption_element, **kwargs)
                caption = self.get_safe_text(caption_element)
                caption_element.extract()
            else:
                caption = None

            label = None
            if label_id := table.get("id"):
                label = f"{label_id}"

            table_data = []
            styles = []
            is_large = False
            for row in table.find_all("tr"):
                row_data = []
                row_styles = []
                cells = row.find_all(["td", "th"])
                for cell in cells:
                    self.render_inlines(cell)
                    row_data.append(self.get_safe_text(cell).strip())
                    row_styles.append(self.get_table_styles(cell))

                # We already have rendered some LaTeX, so to have an idea of the table width
                # we simply strip the LaTeX commands and count the characters...
                # Ugly? yes.
                is_large |= (
                    len(
                        "".join(
                            [
                                re.sub(r"\\href\{[^\}]+?\}|\\\w{3,}|[\{\}|]", "", col)
                                for col in row_data
                            ]
                        )
                    )
                    > 50
                )

                table_data.append(row_data)
                styles.append(row_styles)

            self.apply(
                table,
                "table",
                columns=styles[0],
                rows=table_data,
                caption=caption,
                label=label,
                is_large=is_large,
            )

    def process_exercise(self, soup: Tag, title, **kwargs):
        """Extract solution from exercise if found, to render later as a solution."""
        if not get_class(soup, "exercise"):
            return soup, title
        self.exercise_counter += 1

        # Capture multiple choices
        # The content should have been already rendered
        answer = False
        for el in soup.find_all(string=True):
            if m := re.findall(r"\\item\[\\(correct)?choice]", el):
                answers = [bool(c) for c in m]
                # Replace True with the position in the list rendered at the letter in the alphabet
                keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                answers = [keys[i] for i, a in enumerate(answers) if a]
                answer = (
                    f"Réponse{'' if len(answers) == 1 else 's'}: {', '.join(answers)}"
                )
                el.replace_with(el.get_text().replace("\\correctchoice", "\\choice"))

        # Fill in the blank
        if gaps := soup.find_all("input", class_="text-with-gap"):
            answers = []
            for el in gaps:
                correct_value = el.get("answer")
                answers.append(correct_value)
                el.replace_with(f"\\rule{{{len(correct_value)}ex}}{{0.4pt}}")
            answer = f"Réponse{'' if len(answers) == 1 else 's'}: {', '.join(answers)}"
        if el := soup.find("p", "align--right"):
            el.extract()

        # Extract solution if found
        solution_label = f"sol:{self.exercise_counter}"
        label = f"ex:{self.exercise_counter}"

        solution = ""
        if solution_el := soup.find("details", class_=["solution"]):
            if solution_el.find("summary"):
                solution_el.find("summary").extract()
            solution_el = self.render_inlines(solution_el)
            solution += self.get_safe_text(solution_el)
            self.apply(solution_el, "label", label)

        # Add answer if found
        if answer:
            solution += answer

        if solution:
            solution = f"\\label{{{solution_label}}}\n{solution}"
            self.solutions.append((self.exercise_counter, title, label, solution))
            title = f"\\hyperref[{solution_label}]{{{title}}}"

        return soup, title

    def render_admonition(self, soup: Tag, **kwargs):
        # Admonitions with callout
        for admonition in soup.find_all(["div"], class_="admonition"):
            if not admonition.parent:
                continue

            classes = admonition.get("class", [])
            filtered_classes = [
                cls
                for cls in classes
                if cls
                not in [
                    "admonition",
                    "annotate",
                    "inline",
                    "end",
                    "left",
                    "right",
                    "checkbox",
                    "fill-in-the-blank",
                ]
            ]
            if len(filtered_classes) > 1:
                raise ValueError(f"Multiple classes in admonition: {filtered_classes}")
            admonition_type = filtered_classes[0]
            if title_node := admonition.find("p", class_="admonition-title"):
                if label := title_node.find("span", class_="exercise-label"):
                    # label_text = self.get_safe_text(label)
                    label.extract()

                title = self.get_safe_text(title_node)
                title_node.extract()

            # Treat figures in admonitions differently
            # Tcolorbox does not support figure environments
            admonition = self.render_figure(admonition, tcolorbox=True, **kwargs)
            admonition = self.render_mermaid(admonition, tcolorbox=True, **kwargs)

            admonition, title = self.process_exercise(admonition, title, **kwargs)

            admonition = self.render_after(self.render_admonition, admonition, **kwargs)
            content = self.get_safe_text(admonition)

            self.apply(
                admonition, "callout", content, title=title, type=admonition_type
            )

        # Foldable admonitions are implemented with details/summary
        for admonition in soup.find_all(["details"]):
            if not admonition.parent:
                continue
            classes = admonition.get("class", [])
            if len(classes) > 1:
                raise ValueError(f"Multiple classes in details: {classes}")
            admonition_type = classes[0]

            if summary := admonition.find("summary"):
                title = self.get_safe_text(summary)
                summary.extract()

            # Treat figures in admonitions differently
            # Tcolorbox does not support figure environments
            admonition = self.render_figure(admonition, tcolorbox=True, **kwargs)
            admonition = self.render_mermaid(admonition, tcolorbox=True, **kwargs)

            admonition = self.render_after(self.render_admonition, admonition, **kwargs)
            content = self.get_safe_text(admonition)

            self.apply(
                admonition, "callout", content, title=title, type=admonition_type
            )
        return soup

    def render_links(self, soup: Tag, **kwargs):
        for el in soup.find_all("a"):
            self.render_inlines(el)
            self.render_abbreviation(el)
            text = self.get_safe_text(el)
            href = el.get("href", "")
            if href.startswith("http"):
                if href in self.wikimap:
                    data = self.wikimap[href]
                    self.glossary[data["key"]] = {
                        "name": escape_latex_chars(data["title"]),
                        "description": escape_latex_chars(data["extract"]),
                    }
                    self.apply(el, "glossary", key=data["key"])
                    continue

                href = escape_latex_chars(safe_quote(el.get("href")))
                self.apply(el, "href", text=text, url=href)
            elif href.startswith("#"):
                self.apply(el, "ref", text, ref=href[1:])
            elif href == "" and el.get("id"):
                self.apply(el, "label", el.get("id"))
            elif path := resolve_asset_path(kwargs.get("file_path", Path()), href):
                with open(path, "rb") as f:
                    content = f.read()
                    digest = sha256().hexdigest()
                reference = f"snippet:{digest}"
                self.snippets[reference] = {
                    "path": path,
                    "content": content,
                    "format": path.suffix[1:],
                }
                self.apply(el, "ref", text="extrait", ref=reference)
            else:
                raise NotImplementedError("Local links not implemented")
        return soup

    def render_columns(self, soup: Tag, **kwargs):
        for div in soup.find_all(["div"], class_="two-column-list"):
            self.apply(div, "multicolumn", self.get_safe_text(div), columns=2)

        for div in soup.find_all(["div"], class_="three-column-list"):
            self.apply(div, "multicolumn", self.get_safe_text(div), columns=3)

    def render_inlines(self, soup: Tag, **kwargs):
        """Replace all inline elements."""

        self.render_autoref(soup)
        self.render_index(soup)
        self.render_columns(soup)
        self.render_table(soup)
        self.render_abbreviation(soup)
        self.render_critics(soup)
        self.render_format(soup)
        self.render_paragraph(soup)
        return soup

    def render_index(self, soup: Tag, **kwargs):
        """Render index entries"""
        for el in soup.find_all("span", class_="ycr-hashtag"):
            text = self.get_safe_text(el)
            tag = el.get("data-tag")
            entry = el.get("data-index-entry", text if text else tag)
            self.apply(el, "index", text, tag=tag, entry=entry)
        return soup

    def render_paragraph(self, soup: Tag, **kwargs):
        for p in soup.find_all("p", class_=False):
            p = self.render_inlines(p)
            text = self.get_safe_text(p)
            p.replace_with(text + "\n")

    def render_grid_cards(self, soup: Tag, **kwargs):
        for div in soup.find_all(["div"], class_="grid-cards"):
            div.unwrap()

    def render_hr(self, soup: Tag, **kwargs):
        for el in soup.find_all("hr"):
            el.extract()
        return soup

    def render_br(self, soup: Tag, **kwargs):
        for el in soup.find_all("br"):
            node = NavigableString("\\")
            node.processed = True
            el.replace_with(node)
        return soup

    def render_after(self, function, soup: Tag, **kwargs):
        index = self.renderering_order.index(function)
        for render in self.renderering_order[index:]:
            render(soup, **kwargs)
        return soup

    def get_list_acronyms(self):
        acronyms = [(tag, short, text) for tag, (short, text) in self.acronyms.items()]
        return self.formatter.list_acronyms(acronyms)

    def get_list_glossary(self):
        return self.formatter.list_glossary(self.glossary)

    def get_list_solutions(self):
        return self.formatter.exercises_solutions(self.solutions)

    def get_assets_map(self):
        return self.assets_map

    def get_snippets(self):
        tex = ""
        for key, data in self.snippets.items():
            tex += self.formatter.heading(key.name, level=1)
            tex += self.formatter.codeblock(data["content"], language=data["format"])
        return tex

    def monkeypatch_item(self, latex: str):
        """Verbatim material should not go in the argument to other commands.
        In some cases mintinline works, but you cannot expect it always does.

        Solution: reduce to a case where mintinline works inside arguments,
        because the code has already been absorbed verbatim.
        """
        latex = re.sub(
            r"(\\item\[\\mintinline)(\{[^\}]+\}|.*?|)(\])", r"\\minteditem\2", latex
        )
        return latex

    def monkeypatch_caption(self, latex: str):
        """Caption plugin defines labels for each figures, they are note
        meant to be cross-documents and we don't really use them in LaTeX.
        """
        return re.sub(r"\\label\{_(?:figure|table)-\d+\}", "", latex)

    def monkeypatch_hyphenation(self, latex: str):
        """TeX will not hyphenate past an explicit hyphen, unless you
        explicitly tell it to.

        This has to be applied only in plain text and not in code blocks.

        https://tex.stackexchange.com/a/723596/85416

        This patch is very naive and will not work in all cases.
        """
        if len(latex) < 50:
            return latex

        return re.sub(
            r"(\b[^\W\d_]{2,}-)([^\W\d_]{7,})\b", r"\1\\allowhyphens \2", latex
        )

    def render(self, html, output_path, file_path, base_level=0, numbered=True):
        soup = BeautifulSoup(html, "html.parser")

        kwargs = {
            "file_path": file_path,
            "output_path": output_path,
            "base_level": base_level,
            "numbered": numbered,
        }

        for render in self.renderering_order:
            render(soup, **kwargs)

        # Unwrap remaining div
        for div in soup.find_all(["div"]):
            div.unwrap()

        latex = unescape(str(soup).replace(" ", "~"))

        latex = self.monkeypatch_item(latex)
        latex = self.monkeypatch_caption(latex)
        return latex
