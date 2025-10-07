import logging
from bs4 import BeautifulSoup

log = logging.getLogger('mkdocs')

def addclass(element, classname):
    if 'class' in element.attrs:
        element['class'].append(classname)
    else:
        element['class'] = [classname]

def rowspan(soup):
    for table in soup.find_all('table'):
        cells_to_remove = []
        apply = False
        for row in table.find_all('tr'):
            cols = row.find_all('td')

            # Identify columns with rowspan
            spanned_cols = []
            for i, cell in enumerate(cols):
                has_span = '@span' in cell.text
                spanned_cols.append(has_span)
                if has_span:
                    cell.string = cell.text.replace('@span', '')
                    apply = True

            # Process rowspan
            for i, cell in enumerate(cols):
                if not spanned_cols[i]:
                    continue
                span_rows = 1
                next_row = row.find_next_sibling('tr')
                while next_row is not None:
                    col = next_row.find_all('td')[i]
                    if col.text != '':
                        break
                    span_rows += 1
                    cells_to_remove.append(col)
                    next_row = next_row.find_next_sibling('tr')

                cell['rowspan'] = span_rows

                next_col_is_spanned = i + 1 < len(spanned_cols) and not spanned_cols[i + 1]
                prev_col_is_spanned = i - 1 >= 0 and not spanned_cols[i - 1]
                if next_col_is_spanned:
                    addclass(cell, 'ycr-rowspan--right')
                if prev_col_is_spanned:
                    addclass(cell, 'ycr-rowspan--left')
        if apply:
            for cell in cells_to_remove:
                cell.decompose()
    return soup


def auto_width(soup):
    for table in soup.find_all('table'):
        is_flex = False
        flexible_column = None
        for row in table.find_all('tr'):
            for i, col in enumerate(row.find_all('th')):
                if '@flex' in col.text:
                    flexible_column = i
                    col.string = col.text.replace('@flex', '')
                    break
        if flexible_column is not None:
            for row in table.find_all('tr'):
                for i, col in enumerate(row.find_all(['td', 'th'])):
                    if i == flexible_column:
                        col['class'] = ['ycr-flex-column']
                        is_flex = True

        if is_flex:
            addclass(table, 'ycr-flex-table')
    return soup


def separators(soup):
    for table in soup.find_all('table'):
        cols_idx = []
        for row in table.find_all('tr'):
            for i, col in enumerate(row.find_all(['th', 'td'])):
                if '@rb' in col.text:
                    col.string = col.text.replace('@rb', '')
                    cols_idx.append(i)
                if '@bb' in col.text:
                    col.string = col.text.replace('@bb', '')
                    addclass(row, 'ycr-bottom-border')

        if len(cols_idx) > 0:
            for row in table.find_all('tr'):
                for i, col in enumerate(row.find_all(['td', 'th'])):
                    if i in cols_idx:
                        addclass(col, 'ycr-right-border')
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

def on_page_content(html, page, config, files):
    soup = BeautifulSoup(html, 'html.parser')
    soup = auto_width(soup)
    soup = separators(soup)
    soup = rowspan(soup)
    return str(soup)
