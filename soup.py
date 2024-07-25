"""
TO-DO

- [ ] Remove [^1] and footnotes support
- [ ] Nested items in lists
- [ ] Admonitions (with callouts types)
- [ ] Unicode 1/4... not supported, replacing with math? (usepackage{units} and (nicefrac)?
  - [ ] +/-
  - [ ] -->
  - [ ] <--
  - [ ] <-->
- [ ] Checkbox support, use \item[\correctchoice] or \item[\choice]
- [ ] Abbreviations
- [ ] Use pygments instead of listings? begin{minted}[linenos, frame=lines, framesep=2mm]{python}
- [ ] Tables
- [ ] Record images to be converted
- [ ] Find a way to make Mermaid work

Once it works

- [ ] Generate latex for all markdown files
- [ ] Convert drawio into svg. Use library using frontend with node?
- [ ] Convert all images
- [ ] Copy all images to the output folder
- [ ] Generate nav document with all imports
- [ ] Generate the PDF
"""

import re
from bs4 import BeautifulSoup
import textwrap
html = open('doc.html').read()
soup = BeautifulSoup(html, 'html.parser')
from IPython import embed
from hashlib import sha256
from jinja2 import Environment

jinja_env = Environment(
    block_start_string=r'\BLOCK{',
    block_end_string=r'}',
    variable_start_string=r'\VAR{',
    variable_end_string=r'}',
    comment_start_string=r'\COMMENT{',
    comment_end_string=r'}'
)

acronyms = []

def Template(template):
    return jinja_env.from_string(template)

def render_heading(title, level):
    tag = [
        'section',
        'subsection',
        'subsubsection',
        'paragraph',
        'subparagraph'
        'textbf'][level]

    return Template(r"\\VAR{tag}{\VAR{title}}").render(tag=tag, title=title)


def render_minted(code, language, **kwargs):
    options = []
    if kwargs.get('filename'):
        options.append(f"caption={kwargs['filename'].get_text()}")
    if kwargs.get('lineno'):
        options.append("linenos")
    if kwargs.get('highlighted_lines'):
        options.append(f"highlightlines={{{','.join(optimize_list(kwargs['highlighted_lines']))}}}")

    options = ', '.join(options)
    return Template(textwrap.dedent(r"""\begin{minted}[\VAR{options}]{\VAR{language}}
        \VAR{code}
        \end{minted}""")).render(code=code, language=language, options=options)

def render_codeinline(code, language, options):
    return Template(r"""\mintinline\BLOCK{if language}{\VAR{language}}\BLOCK{endif}{\VAR{code}}
    """).render(code=code, language=language, options=options)

def optimize_list(numbers):
    if not numbers:
        return []

    numbers = sorted(numbers)
    optimized = []
    start = numbers[0]
    end = numbers[0]

    for num in numbers[1:]:
        if num == end + 1:
            end = num
        else:
            if start == end:
                optimized.append(str(start))
            else:
                optimized.append(f"{start}-{end}")
            start = num
            end = num

    if start == end:
        optimized.append(str(start))
    else:
        optimized.append(f"{start}-{end}")

    return optimized

def get_table_styles(cell):
    if not cell:
        return ''
    style = cell.get('style', '')
    if 'text-align: right' in style:
        return 'r'
    if 'text-align: center' in style:
        return 'c'
    return 'l'


def extract_table(table):
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
            row_styles.append(get_table_styles(cell))
        table_data.append(row_data)
        styles.append(row_styles)

    print(table_data)
    print(styles)
    return table_data, styles

def get_code_language(element):
    classes = element.get('class', [])
    if 'highlight' not in classes:
        return None
    classlist = [c for c in classes if c.startswith('language-')]
    if classlist:
        lang = classlist[0][9:]
        if lang == 'latex':
            return 'tex'
    return 'text'

def convert_ul_to_latex(ul):
    items = []
    checkboxes = False
    for li in ul.find_all('li', recursive=False):
        sub_ul = li.find('ul')
        text = li.get_text().strip()
        print(text)
        head = f"\\item {text}"
        if text.startswith('[ ]'):
            head = f"\\item[\\choice] {text[4:]}"
            checkboxes = True
        elif text.startswith('[x]'):
            head = f"\\item[\\correctchoice] {text[4:]}"
            checkboxes = True

        if sub_ul:
            sub_ul.extract()
            items.append(f"{head}\n{convert_ul_to_latex(sub_ul)}")
        else:
            items.append(f"{head}")
    if checkboxes:
        return "\n\\begin{description}\n" + '\n'.join(items) + "\n\\end{description}\n"
    return "\\begin{itemize}\n" + '\n'.join(items) + "\n\\end{itemize}"

def convert_ol_to_latex(ol):
    items = []
    for li in ol.find_all('li', recursive=False):
        sub_ol = li.find('ol')
        text = li.get_text().strip()
        print(text)
        if sub_ol:
            sub_ol.extract()
            items.append(f"\\item {text}\n{convert_ol_to_latex(sub_ol)}")
        else:
            items.append(f"\\item {text}")
    return "\\begin{enumerate}\n" + '\n'.join(items) + "\n\\end{enumerate}"

for element in soup.find_all('div', class_='highlight'):
    for span in element.find_all('span'):
        pan.replace_with(span.get_text())

        # cat = span.get('class', [])
        # if len(cat) == 1:
        #     match cat[0]:
        #         case 'p':
        #             span.replace_with(span.get_text()+"\n")
        #         case _:
        #             span.replace_with(span.get_text())
    # text = ''.join(element.stripped_strings)
    # element.replace_with(f":::{text}:::")
    # filename = element.find('span', class_='filename')
    # lang = get_code_language(element)
    # lineno = False
    # highlighted_lines = []

    # # Has line numbers
    # if (table := element.find('table', class_='highlighttable')):
    #     code = '\n'.join([row.get_text()
    #                       for row in table.find_all('td', class_='code')])
    #     lineno = True
    # else:
    #     code = element.get_text()

    # # Has highlighted lines
    # if element.find('span', class_='hll'):
    #     span_elements = soup.find_all('span', id=re.compile(r'^__span-'))
    #     for i, line in enumerate(span_elements):
    #         if line.find('span', class_='hll'):
    #             highlighted_lines.append(i + 1)
    # element.replace_with(render_codeblock(code, lang, filename=filename,
    #                                       lineno=lineno,
    #                                       highlighted_lines=highlighted_lines))

# for inline in soup.find_all(['abbr', 'span','sub', 'ins', 'del', 'kbd', 'mark', 'span', 'strong', 'em', 'code', 'a', 'sup']):
#     text = inline.get_text()
#     match inline.name:
#         case 'abbr':
#             tag = inline.get('title', '')
#             text = inline.get_text()
#             inline.replace_with(f"\\gls{{{tag}}}")
#             acronyms.append((text, tag))
#         case 'a':
#             # Remove Permanent link
#             if 'headerlink' in inline.get('class', []):
#                 inline.extract()
#         case 'sub':
#             inline.replace_with(f"\\textsubscript{{{text}}}")
#         case 'strong':
#             inline.replace_with(f"\\textbf{{{text}}}")
#         case 'em':
#             inline.replace_with(f"\\emph{{{text}}}")
#         case 'sup':
#             inline.replace_with(f"\\textsuperscript{{{text}}}")
#         case 'mark':
#             inline.replace_with(f"\\hl{{{text}}}")
#         case 'del':
#             inline.replace_with(f"\\sout{{{text}}}")
#         case 'ins':
#             inline.replace_with(f"\\uline{{{text}}}")
#         case 'kbd':
#             inline.replace_with(f"\\kbd{{{text}}}")
#         case 'code':
#             text = inline.get_text()
#             if language := get_code_language(inline):
#                 inline.replace_with(render_codeinline(text, language, {}))
#             else:
#                 inline.replace_with(f"\\texttt{{{text}}}")
#         case 'span':
#             classes = inline.get('class', [])
#             if 'twemoji' in classes:
#                 if inline.children:
#                     svg = next(inline.children)
#                     if svg and svg.name == 'svg':
#                         svg_code = svg.prettify()
#                         filename = sha256(svg_code.encode()).hexdigest() + '.svg'
#                         open(filename, 'w').write(svg_code)

#                         # Should convert to pdf: inkscape *.svg --export-area-drawing --export-type=pdf
#                         inline.replace_with(f"\\includegraphics[width=1em]{{{filename.replace('.svg', '.pdf')}}}")
#             elif 'arithmatex' in classes:
#                 text = inline.get_text()
#                 inline.replace_with(f"${text[2:-2]}$")

# for inline in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
#     title = inline.get_text()
#     level = int(inline.name[1:]) - 1
#     inline.replace_with(render_heading(title, level))

# All p without a class
# for inline in soup.find_all('p', class_=False):
#     inline.replace_with(f"{inline.get_text()}\n")

# for inline in soup.find_all(['div'], class_='arithmatex'):
#     inline.replace_with(f"\n{inline.get_text()}\n")

# ul_elements = soup.find_all('ul')
# for ul in reversed(ul_elements):
#     ul.replace_with(BeautifulSoup(convert_ul_to_latex(ul), 'html.parser'))

# ol_elements = soup.find_all('ol')
# for ol in reversed(ol_elements):
#     ol.replace_with(BeautifulSoup(convert_ol_to_latex(ol), 'html.parser'))

# for inline in soup.find_all(['dl']):
#     for dt in inline.find_all('dt'):
#         dt.replace_with(f"\\item[{dt.get_text()}]")
#     for dd in inline.find_all('dd'):
#         dd.replace_with(f"{dd.get_text()}\n")
#     inline.replace_with(f"\\begin{{description}}\n{inline.get_text()}\\end{{description}}\n")

# for table in soup.find_all(['table']):
#     table_data, styles = extract_table(table)
#     if table_data:
#         latex_table = "\\begin{tabular}{" + "l" * len(table_data[0]) + "}\n"
#         for row in table_data:
#             latex_table += ' & '.join(row) + " \\\\\n"
#         latex_table += "\\end{tabular}\n"
#         table.replace_with(latex_table)

# # Admonitions with callout
# for admonition in soup.find_all(['div'], class_='admonition'):
#     classes = admonition.get('class', [])
#     filtered_classes = [cls for cls in classes if cls not in ['admonition', 'annotate', 'inline', 'end', 'left', 'right']]
#     if len(filtered_classes) > 1:
#         raise(f"Multiple classes in admonition: {filtered_classes}")
#     admonition_type = filtered_classes[0]
#     admonition_title = admonition.find('p', class_='admonition-title')
#     if title:
#         title = admonition_title.get_text()
#         admonition_title.extract()
#     # elif summary := admonition.find('summary'):
#     #     title = summary.get_text()
#     #     summary.extract()
#     content = admonition.get_text()
#     admonition.replace_with(f"\\begin{{callout}}{{{title}}}{{{admonition_type}}}\n{content}\n\\end{{callout}}\n")

# for admonition in soup.find_all(['details']):
#     classes = admonition.get('class', [])
#     if len(classes) > 1:
#         raise(f"Multiple classes in admonition: {classes}")
#     admonition_type = classes[0]
#     admonition_title = admonition.find('summary')
#     if title:
#         title = admonition_title.get_text()
#         admonition_title.extract()
#     content = admonition.get_text()
#     admonition.replace_with(f"\\begin{{callout}}{{{title}}}{{{admonition_type}}}\n{content}\n\\end{{callout}}\n")

# for tabbed_set in soup.find_all('div', class_='tabbed-set'):
#     labels = []
#     for tabbed_labels in tabbed_set.find_all('label'):
#         labels.append(f"\\textbf{{{tabbed_labels.get_text()}}}")
#     for i, tabbed_block in enumerate(tabbed_set.find_all('div', class_='tabbed-block')):
#         content = tabbed_block.get_text()
#         tabbed_block.replace_with(f"{labels[i]}:\n{content}\n")
#     tabbed_set.replace_with(tabbed_set.get_text())


# # Mermaid
# for mermaid in soup.find_all('pre', class_='mermaid'):
#     code = mermaid.get_text()
#     mermaid.replace_with(render_codeblock(code, 'text'))

latex = str(soup)

# # Add acronyms
# for tag, acronym in acronyms:
#     latex += f"\\newacronym{{{tag}}}{{{tag}}}{{{acronym}}}\n"

# # Replace all html
# latex = latex.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')

# # Replace all multiple empty lines with a single empty line ? How to avoid code ?
# latex = latex.replace(' ', '~')

# Use latexindent -w output.tex to format the output
open('output.tex', 'w').write(latex)
