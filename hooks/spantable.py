"""Enhance HTML tables with additional classes for custom styling."""

from __future__ import annotations

from bs4 import BeautifulSoup, Tag
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

def add_class(element: Tag, classname: str) -> None:
    """Append a CSS class to a BeautifulSoup element."""

    element["class"] = [*element.get("class", []), classname]


def rowspan(soup: BeautifulSoup) -> BeautifulSoup:
    """Expand ``@span`` markers into actual ``rowspan`` attributes."""

    for table in soup.find_all("table"):
        cells_to_remove: list[Tag] = []
        apply = False
        for row in table.find_all("tr"):
            columns = row.find_all("td")

            spanned_cols = []
            for index, cell in enumerate(columns):
                has_span = "@span" in cell.text
                spanned_cols.append(has_span)
                if has_span:
                    cell.string = cell.text.replace("@span", "")
                    apply = True

            for index, cell in enumerate(columns):
                if not spanned_cols[index]:
                    continue
                span_rows = 1
                next_row = row.find_next_sibling("tr")
                while next_row is not None:
                    col = next_row.find_all("td")[index]
                    if col.text != "":
                        break
                    span_rows += 1
                    cells_to_remove.append(col)
                    next_row = next_row.find_next_sibling("tr")

                cell["rowspan"] = span_rows

                next_col_is_spanned = index + 1 < len(spanned_cols) and not spanned_cols[index + 1]
                prev_col_is_spanned = index - 1 >= 0 and not spanned_cols[index - 1]
                if next_col_is_spanned:
                    add_class(cell, "ycr-rowspan--right")
                if prev_col_is_spanned:
                    add_class(cell, "ycr-rowspan--left")
        if apply:
            for cell in cells_to_remove:
                cell.decompose()
    return soup


def auto_width(soup: BeautifulSoup) -> BeautifulSoup:
    """Mark tables that contain a ``@flex`` header for flexible width layouts."""

    for table in soup.find_all("table"):
        is_flex = False
        flexible_column: int | None = None
        for row in table.find_all("tr"):
            for index, col in enumerate(row.find_all("th")):
                if "@flex" in col.text:
                    flexible_column = index
                    col.string = col.text.replace("@flex", "")
                    break
        if flexible_column is not None:
            for row in table.find_all("tr"):
                for index, col in enumerate(row.find_all(["td", "th"])):
                    if index == flexible_column:
                        col["class"] = ["ycr-flex-column"]
                        is_flex = True

        if is_flex:
            add_class(table, "ycr-flex-table")
    return soup


def separators(soup: BeautifulSoup) -> BeautifulSoup:
    """Convert marker tokens (``@rb``/``@bb``) into CSS classes."""

    for table in soup.find_all("table"):
        cols_idx: list[int] = []
        for row in table.find_all("tr"):
            for index, col in enumerate(row.find_all(["th", "td"])):
                if "@rb" in col.text:
                    col.string = col.text.replace("@rb", "")
                    cols_idx.append(index)
                if "@bb" in col.text:
                    col.string = col.text.replace("@bb", "")
                    add_class(row, "ycr-bottom-border")

        if cols_idx:
            for row in table.find_all("tr"):
                for index, col in enumerate(row.find_all(["td", "th"])):
                    if index in cols_idx:
                        add_class(col, "ycr-right-border")
    return soup

# def on_page_markdown(markdown, page, config, files):
#     # Search for tables separators
#     lines = markdown.split('\n')
#     new_lines = []
#     for line in lines[1:]:
#         if match := re.match(r'^.*?\|:?\s*-{3,}\s*:?\|.*$', line):
#             sep = 0
#             seps = 0
#             for i in range(len(match)):
#                 if match[i] == '|':
#                     sep = sep + 1
#                     seps += 1
#                 else:
#                     sep = 0

#                 if sep == 2:
#                     match = match[:i] + ':' + match[i+1:]
#                     break

#                 if c == '-':
#                     match = match[:i] + ':' + match[i+1:]
#                     break
#         new_lines.append(line)

#     return markdown

def on_page_content(
    html: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Post-process rendered HTML tables for advanced layouts."""

    del page, config, files

    soup = BeautifulSoup(html, "html.parser")
    soup = auto_width(soup)
    soup = separators(soup)
    soup = rowspan(soup)
    return str(soup)
