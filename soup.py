"""
TO-DO

- [ ] Remove [^1] and footnotes support
- [ ] Nested items in lists
- [ ] Admonitions (with callouts types)
- [ ] Unicode 1/4... not supported, replacing with math? (\usepackage{units} and (\nicefrac)?
  - [ ] +/-
  - [ ] -->
  - [ ] <--
  - [ ] <-->
- [ ] Checkbox support, use \item[\correctchoice] or \item[\choice]
- [ ] Abbreviations
- [ ] Use pygments instead of listings? \begin{minted}[linenos, frame=lines, framesep=2mm]{python}
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

def Template(template):
    return jinja_env.from_string(textwrap.dedent(template))

def render_heading(title, level):
    tag = [
        'section',
        'subsection',
        'subsubsection',
        'paragraph',
        'subparagraph'
        'textbf'][level]

    return Template(r"\\VAR{tag}{\VAR{title}}").render(tag=tag, title=title)

def render_codeblock(code, language, options):
    return Template(r"""\begin{lstlisting}[language=\VAR{language}]
        \VAR{code}
        \end{lstlisting}
    """).render(code=code, language=language, options=options)

def render_codeinline(code, language, options):
    return Template(r"""\lstinline\BLOCK{if language}[language=\VAR{language}]\BLOCK{endif}|\VAR{code}|
    """).render(code=code, language=language, options=options)

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
    return None

for element in soup.find_all('div', class_='highlight'):
    if lang := get_code_language(element):
        code = element.get_text()
        element.replace_with(render_codeblock(code, lang, {}))

for inline in soup.find_all(['span','sub', 'ins', 'del', 'kbd', 'mark', 'span', 'strong', 'em', 'code', 'a', 'sup']):
    text = inline.get_text()
    match inline.name:
        case 'a':
            # Remove Permanent link
            if 'headerlink' in inline.get('class', []):
                inline.extract()
        case 'sub':
            inline.replace_with(f"\\textsubscript{{{text}}}")
        case 'strong':
            inline.replace_with(f"\\textbf{{{text}}}")
        case 'em':
            inline.replace_with(f"\\emph{{{text}}}")
        case 'sup':
            inline.replace_with(f"\\textsuperscript{{{text}}}")
        case 'mark':
            inline.replace_with(f"\\hl{{{text}}}")
        case 'del':
            inline.replace_with(f"\\sout{{{text}}}")
        case 'ins':
            inline.replace_with(f"\\uline{{{text}}}")
        case 'kbd':
            inline.replace_with(f"\\kbd{{{text}}}")
        case 'code':
            text = inline.get_text()
            if language := get_code_language(inline):
                inline.replace_with(render_codeinline(text, language, {}))
            else:
                inline.replace_with(f"\\texttt{{{text}}}")
        case 'span':
            classes = inline.get('class', [])
            if 'twemoji' in classes:
                if inline.children:
                    svg = next(inline.children)
                    if svg and svg.name == 'svg':
                        svg_code = svg.prettify()
                        filename = sha256(svg_code.encode()).hexdigest() + '.svg'
                        open(filename, 'w').write(svg_code)
                        # Should convert to pdf: inkscape *.svg --export-area-drawing --export-type=pdf
                        inline.replace_with(f"\\includegraphics[width=1em]{{{filename}}}")
            elif 'arithmatex' in classes:
                text = inline.get_text()
                inline.replace_with(f"${text[2:-2]}$")

for inline in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
    title = inline.get_text()
    level = int(inline.name[1:]) - 1
    inline.replace_with(render_heading(title, level))

for inline in soup.find_all(['p']):
    inline.replace_with(f"{inline.get_text()}\n")

for inline in soup.find_all(['div'], class_='arithmatex'):
    inline.replace_with(f"\n{inline.get_text()}\n")

for inline in soup.find_all(['ul']):
    items = ''.join([f"\\item {li.get_text()}\n" for li in inline.find_all('li')])
    inline.replace_with(f"\\begin{{itemize}}\n{items}\\end{{itemize}}\n")

for inline in soup.find_all(['ol']):
    items = ''.join([f"\\item {li.get_text()}\n" for li in inline.find_all('li')])
    inline.replace_with(f"\\begin{{enumerate}}\n{items}\\end{{enumerate}}\n")

for inline in soup.find_all(['dl']):
    for dt in inline.find_all('dt'):
        dt.replace_with(f"\\item[{dt.get_text()}]")
    for dd in inline.find_all('dd'):
        dd.replace_with(f"{dd.get_text()}\n")
    inline.replace_with(f"\\begin{{description}}\n{inline.get_text()}\\end{{description}}\n")

for table in soup.find_all(['table']):
    table_data, styles = extract_table(table)
    if table_data:
        latex_table = "\\begin{tabular}{" + "l" * len(table_data[0]) + "}\n"
        for row in table_data:
            latex_table += ' & '.join(row) + " \\\\\n"
        latex_table += "\\end{tabular}\n"
        table.replace_with(latex_table)

# Admonitions with callout
# for admonition in soup.find_all(['div'], class_='admonition'):
#     title = admonition.find('p').get_text()
#     content = admonition.find('div').get_text()
#     admonition.replace_with(f"\\begin{{admonition}}{{{title}}}\n{content}\n\\end{{admonition}}")

# Tabbed-set with inline code ?
latex = str(soup)

# Replace all multiple empty lines with a single empty line ? How to avoid code ?
latex.replace(' ', '~')

# Use latexindent -w output.tex to format the output
open('output.tex', 'w').write(latex)
