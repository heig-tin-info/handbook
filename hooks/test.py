from bs4 import BeautifulSoup
import os
from jinja2 import Environment, FileSystemLoader
import textwrap


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




class LaTeXRenderer:
    def __init__(self):
        template_dir = 'templates/'
        self.env = Environment(
            block_start_string=r'\BLOCK{',
            block_end_string=r'}',
            variable_start_string=r'\VAR{',
            variable_end_string=r'}',
            comment_start_string=r'\COMMENT{',
            comment_end_string=r'}',
            loader=FileSystemLoader(template_dir))

        self.templates = {
            os.path.basename(filename): self.env.get_template(filename)
            for filename in os.listdir(template_dir)
        }

    def render_heading(self, title, level):
        return self.templates['heading'].render(title=title, level=level)

    def render_minted(self, code, language='text', filename=None, lineno=False,
                      highlight=[]):
        options = []
        if filename:
            options.append(f"caption={filename}")

        if highlight:
            options.append(f"highlightlines={{{','.join(optimize_list(highlight))}}}")
        options = ', '.join(options)

        return self.templates['minted'].render(
            code=code,
            language=language,
            linenos=lineno,
            highlight=optimize_list(highlight),
            caption=filename,
            filename=filename
        )

    def extract_code_block(soup):
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
            'listing': '\n'.join(listing)
        }

    def render(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for el in soup.find_all('div', class_=['highlight']):
            if code := self.extract_code_block(el):
                el.replace_with(self.render_minted(**code))

        return str(soup)
