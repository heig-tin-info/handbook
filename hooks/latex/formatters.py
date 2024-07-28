import os
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from hashlib import sha256
import shutil
import urllib.parse
from typing import Union
import re

TEMPLATE_DIR = Path(__file__).parent / 'templates'


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


class LaTeXFormatter:
    def __init__(self, template_dir=TEMPLATE_DIR):
        # Easier to use LaTeX syntax for templates
        self.env = Environment(
            block_start_string=r'\BLOCK{',
            block_end_string=r'}',
            variable_start_string=r'\VAR{',
            variable_end_string=r'}',
            comment_start_string=r'\COMMENT{',
            comment_end_string=r'}',
            loader=FileSystemLoader(template_dir))

        # Load all templates
        self.templates = {
            Path(filename).stem: self.env.get_template(filename)
            for filename in os.listdir(template_dir)
        }

    def __getattr__(self, method):
        """Proxy method calls to the corresponding template
        that are note specifically defined in the class. """
        template = self.templates.get(method)
        mangled = f'handle_{method}'
        if mangled in self.__dict__:
            template = self.__dict__[mangled]
        if method in self.templates:
            template = self.templates[method]
        else:
            raise AttributeError(f"Object has no template for '{method}'")

        def render_template(*args, **kwargs):
            """Render the template with the given arguments.
            If a single argument is given, it is assumed to be the
            'text' argument. """
            if len(args) > 1:
                raise ValueError("Expected at most 1 argument, got "
                                 f"{len(args)}, use keyword arguments instead")
            if args:
                kwargs['text'] = args[0]
            return template.render(**kwargs)
        return render_template

    def handle_codeblock(self, code, language='text',
                         filename=None, lineno=False, highlight=None):
        """Handle codeblock with optional line numbers and
        highlighted lines. """

        if highlight is None:
            highlight = []

        return self.templates['codeblock'].render(
            code=code,
            language=language,
            linenos=lineno,
            filename=filename,
            highlight=optimize_list(highlight),  # e.g. 1,2,3 -> 1-3
        )

    def url(self, text, url):
        url = escape_latex_chars(urllib.parse.quote(url, safe=':/?&='))
        return self.templates['url'].render(text=text, url=url)

    def figure(self, caption: str, path: Path):
        extensions = ['.bmp', '.eps', '.gif', '.ico', '.jpg', '.jpeg', '.jp2',
                      '.msp', '.pcx', '.png', '.ppm', '.pgm', '.pbm', '.pnm',
                      '.sgi', '.rgb', '.rgba', '.bw', '.spi', '.tiff', '.tif',
                      '.webp', '.xbm', '.tga']

        if (str(path).startswith('http')):
            path = fetch_image(path, self.output_path)
        elif path.suffix == '.drawio':
            path = drawio2pdf(path, self.output_path)
        elif path.suffix == '.svg':
            path = svg2pdf(path, self.output_path)
        elif path.suffix in extensions:
            path = image2pdf(path, self.output_path)
        else:
            new_path = self.output_path / (sha256(path.read_bytes()).hexdigest() + path.suffix)
            shutil.copy(path, new_path)
            path = new_path

        return self.templates['figure'].render(caption=caption, path=path.name)

    def get_glossary(self):
        acronyms = [(tag, short, text) for tag, (short, text) in self.acronyms.items()]

        return self.templates['glossary'].render(glossary=acronyms)

    def svg(self, svg):
        pdfpath = svg2pdf(svg, self.output_path)
        return f"\\includegraphics[width=1em]{{{pdfpath }}}"
