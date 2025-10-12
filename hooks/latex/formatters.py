"""Utilities for rendering LaTeX templates."""

from __future__ import annotations

import glob
import urllib.parse
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Callable

from jinja2 import Environment, FileSystemLoader, Template

from .utils import escape_latex_chars

TEMPLATE_DIR = Path(__file__).parent / "templates"


def optimize_list(numbers: Iterable[int]) -> list[str]:
    """Merge consecutive integers into human-readable ranges.
    >>> optimize_list([1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16])
    ['1-6', '8-10', '12', '14-16']
    """

    values = sorted(numbers)
    if not values:
        return []

    optimized: list[str] = []
    start = end = values[0]

    for num in values[1:]:
        if num == end + 1:
            end = num
        else:
            optimized.append(f"{start}-{end}" if start != end else str(start))
            start = end = num

    optimized.append(f"{start}-{end}" if start != end else str(start))
    return optimized


class LaTeXFormatter:
    """Render LaTeX templates using Jinja2 with custom delimiters."""

    def __init__(self, template_dir: Path = TEMPLATE_DIR) -> None:
        self.env = Environment(
            block_start_string=r"\BLOCK{",
            block_end_string=r"}",
            variable_start_string=r"\VAR{",
            variable_end_string=r"}",
            comment_start_string=r"\COMMENT{",
            comment_end_string=r"}",
            loader=FileSystemLoader(template_dir),
        )

        template_paths: list[Path] = []
        for ext in (".tex", ".cls"):
            template_paths.extend(
                Path(path)
                for path in glob.glob(f"{template_dir}/**/*{ext}", recursive=True)
            )

        templates = [path.relative_to(template_dir) for path in template_paths]
        self.templates: dict[str, Template] = {
            str(filename.with_suffix("")).replace("/", "_"): self.env.get_template(
                str(filename)
            )
            for filename in templates
        }

    def __getattr__(self, method: str) -> Callable[..., str]:
        """Proxy calls to templates or custom handlers."""

        mangled = f"handle_{method}"
        try:
            handler = object.__getattribute__(self, mangled)
        except AttributeError:
            handler = None
        if handler is not None:
            return handler  # type: ignore[return-value]

        template = self.templates.get(method)
        if template is None:
            raise AttributeError(f"Object has no template for '{method}'") from None

        def render_template(*args: Any, **kwargs: Any) -> str:
            """Render the template with optional positional shorthand."""

            if len(args) > 1:
                msg = f"Expected at most 1 argument, got {len(args)}, use keyword arguments instead"
                raise ValueError(msg)
            if args:
                kwargs["text"] = args[0]
            return template.render(**kwargs)

        return render_template

    def __getitem__(self, key: str) -> Callable[..., str]:
        return self.templates[key].render

    def handle_codeblock(
        self,
        code: str,
        language: str = "text",
        filename: str | None = None,
        lineno: bool = False,
        highlight: Iterable[int] | None = None,
        **_: Any,
    ) -> str:
        """Render code blocks with optional line numbers and highlights."""

        highlight = list(highlight or [])
        return self.templates["codeblock"].render(
            code=code,
            language=language,
            linenos=lineno,
            filename=filename,
            highlight=optimize_list(highlight),
        )

    def url(self, text: str, url: str) -> str:
        """Render a URL, escaping special LaTeX characters."""

        safe_url = escape_latex_chars(urllib.parse.quote(url, safe=":/?&="))
        return self.templates["url"].render(text=text, url=safe_url)

    # def get_glossary(self) -> str:
    #     """Render the glossary of acronyms."""
    #     acronyms = [(tag, short, text) for tag, (short, text) in self.acronyms.items()]
    #     return self.templates["glossary"].render(glossary=acronyms)

    def svg(self, svg: str | Path) -> str:
        """Render an SVG image by converting it to PDF first."""
        from .transformers import svg2pdf

        pdfpath = svg2pdf(svg, self.output_path)
        return f"\\includegraphics[width=1em]{{{pdfpath}}}"

    def get_cover(self, name: str, **kwargs: Any) -> str:
        template = self.templates[f"cover/{name}"]
        return template.render(
            title=self.config.title,
            author=self.config.author,
            subtitle=self.config.subtitle,
            email=self.config.email,
            year=self.config.year,
            **self.config.cover.model_dump(),
            **kwargs,
        )
