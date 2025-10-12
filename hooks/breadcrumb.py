"""Emulate MkDocs Insiders breadcrumbs for the public edition."""

from __future__ import annotations

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

CARET = """
<svg class="breadcrumb-CARET" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512">
    <path d="M246.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-9.2-9.2-22.9-11.9-34.9-6.9s-19.8 16.6-19.8 29.6l0 256c0 12.9 7.8 24.6 19.8 29.6s25.7 2.2 34.9-6.9l128-128z"/>
</svg>"""


def on_page_content(
    html: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Inject a breadcrumb trail at the top of each page."""

    del config, files  # MkDocs requires this signature even if unused.

    elements: list[Page] = [page]
    while elements[-1].parent:
        elements.append(elements[-1].parent)

    def render_link(element: Page) -> str:
        if getattr(element, "url", None):
            return f'<a href="{element.url}">{element.title}</a>'
        return f"<span>{element.title}</span>"

    breadcrumb = CARET.join(render_link(el) for el in reversed(elements))
    return f'<div class="breadcrumb">{breadcrumb}</div>{html}'
