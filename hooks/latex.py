"""
- [ ] Footnotes
"""

import pandoc
import logging
import mkdocs
from pathlib import Path
import stopwatch as sw
from IPython import embed
from bs4 import BeautifulSoup

log = logging.getLogger('mkdocs')

stopwatch = sw.Stopwatch()

"""
    def convert_element(element):
        if element.name == 'h1':
            return f"\\section{{{element.get_text()}}}\n"
        elif element.name == 'h2':
            return f"\\subsection{{{element.get_text()}}}\n"
        elif element.name == 'h3':
            return f"\\subsubsection{{{element.get_text()}}}\n"
        elif element.name == 'p':
            return f"{element.get_text()}\n\n"
        elif element.name == 'ul':
            items = ''.join([f"\\item {convert_element(li)}" for li in element.find_all('li')])
            return f"\\begin{{itemize}}\n{items}\\end{{itemize}}\n"
        elif element.name == 'ol':
            items = ''.join([f"\\item {convert_element(li)}" for li in element.find_all('li')])
            return f"\\begin{{enumerate}}\n{items}\\end{{enumerate}}\n"
        elif element.name == 'li':
            return f"{element.get_text()}\n"
        elif element.name == 'code':
            return f"\\texttt{{{element.get_text()}}}"
        elif element.name == 'strong':
            return f"\\textbf{{{element.get_text()}}}"
        elif element.name == 'em':
            return f"\\emph{{{element.get_text()}}}"
        elif element.name == 'sup':
            return f"\\textsuperscript{{{element.get_text()}}}"
        elif element.name == 'sub':
            return f"\\textsubscript{{{element.get_text()}}}"
        elif element.name == 'blockquote':
            return f"\\begin{{quote}}\n{element.get_text()}\n\\end{{quote}}\n"
        elif element.name == 'a':
            return f"\\href{{{element.get('href')}}}{{{element.get_text()}}}"
        elif element.name == 'table':
            rows = element.find_all('tr')
            latex_table = "\\begin{tabular}{" + "l" * len(rows[0].find_all(['th', 'td'])) + "}\n"
            for row in rows:
                cols = row.find_all(['th', 'td'])
                latex_table += ' & '.join([col.get_text() for col in cols]) + " \\\\\n"
            latex_table += "\\end{tabular}\n"
            return latex_table
        elif element.name == 'img':
            return f"\\includegraphics[width=\\textwidth]{{{element.get('src')}}}"
        # Add more conversions as needed
        else:
            return element.get_text()

    latex_content = ''.join([convert_element(element) for element in soup.body.children])
    return latex_content
"""

def on_env(env, config, files):
    log.error(dir(files))

    for file in files:
        if file.src_path.endswith('.md'):
            html = file.page.content
            open('intermediate.html', 'w').write(html)
