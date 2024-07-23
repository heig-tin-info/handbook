from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.rules_block import StateBlock
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.attrs import attrs_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
import re
import logging

log = logging.getLogger(__name__)

plugins = [
    dollarmath_plugin,
    admon_plugin,
    attrs_plugin,
    deflist_plugin,
    tasklists_plugin
]
md = MarkdownIt().enable('table').enable('strikethrough')
for plugin in plugins:
    md = md.use(plugin)
md = md
tokens = md.parse(open('test.md', 'r').read())

next_text_is_special = False
latex_output = []
for token in tokens:
    if token.hidden:
        log.warning(f"Hidden token: {token}")
        continue;

    if token.type == 'heading_open':
        if token.tag == 'h1':
            latex_output.append("\\section{")
        elif token.tag == 'h2':
            latex_output.append("\\subsection{")
        elif token.tag == 'h3':
            latex_output.append("\\subsubsection{")
        elif token.tag == 'h4':
            latex_output.append("\\paragraph{")
        elif token.tag == 'h5':
            latex_output.append("\\subparagraph{")
        elif token.tag == 'h6':
            latex_output.append("\\textbf{")  # No direct equivalent in LaTeX for h6
    elif token.type == 'heading_close':
        latex_output.append("}\n")
    elif token.type == 'paragraph_open':
        latex_output.append("\n")
    elif token.type == 'paragraph_close':
        latex_output.append("\n")
    elif token.type == 'inline':
        for child in token.children:
            if child.type == 'text':
                if next_text_is_special == 'admonition-title':
                    latex_output.append(f"{{{child.content[1:-1]}}}")
                    next_text_is_special = False
                    continue
                latex_output.append(child.content)
            elif child.type == 'strong_open':
                latex_output.append("\\textbf{")
            elif child.type == 'strong_close':
                latex_output.append("}")
            elif child.type == 'em_open':
                latex_output.append("\\emph{")
            elif child.type == 'em_close':
                latex_output.append("}")
            elif child.type == 'code_inline':
                latex_output.append("\\texttt{" + child.content + "}")
            elif child.type == 'image':
                latex_output.append("\\begin{figure}[H]\n   \\centering\n")

                latex_output.append(f"   \\includegraphics{{{child.attrs['src']}}}\n")
                if child.children:
                    if child.children[0].type == 'text':
                        latex_output.append(f"   \\caption{{{child.children[0].content}}}\n")

                latex_output.append("\\end{figure}")

    elif token.type == 'admonition_open':
        latex_output.append(f"\\begin{{admonition}}{{{token.meta['tag']}}}")
    elif token.type == 'admonition_close':
        latex_output.append(f"\\end{{{token.info}}}\n")
    elif token.type == 'admonition_title_open':
        next_text_is_special = 'admonition-title'
    elif token.type == 'admonition_title_close':
        continue
    elif token.type == 'math_block':
        latex_output.append(f"\\[{token.content}\\]\n")
    elif token.type == 'html_block':
        if token.content.startswith('<!--'):
            latex_output.append(f"\\begin{{verbatim}}\n{token.content[4:-4]}\n\\end{{verbatim}}\n")
    elif token.type == 'fence':
        latex_output.append("\\begin{lstlisting}")
        latex_output.append(f"{{language={token.info}}}\n")
        latex_output.append(f"{token.content}")
        latex_output.append("\\end{lstlisting}\n")
    else:
        latex_output.append(f"\\begin{{verbatim}}\n   {token}\n\\end{{verbatim}}\n")
print(''.join(latex_output))





def admonition_plugin(md: MarkdownIt):
    def admonition(state: StateBlock, startLine: int, endLine: int, silent: bool):
        pos = state.bMarks[startLine] + state.tShift[startLine]
        max_pos = state.eMarks[startLine]

        if state.src[pos:pos + 3] != "!!!":
            return False

        start_pos = pos
        pos += 3
        while pos < max_pos and state.src[pos].isspace():
            pos += 1

        if pos >= max_pos:
            return False

        title = state.src[pos:max_pos].strip()

        # Create the opening token
        token = state.push('admonition_open', 'div', 1)
        token.attrs = {"class": f"admonition {title}"}
        token.markup = "!!!"
        token.block = True
        token.map = [startLine, 0]

        # Advance the line
        nextLine = startLine + 1

        while nextLine < endLine:
            if state.sCount[nextLine] < state.blkIndent:
                break

            nextLine += 1

        # Create the body tokens
        state.md.block.tokenize(state, startLine + 1, nextLine)

        # Create the closing token
        token = state.push('admonition_close', 'div', -1)
        token.block = True

        state.line = nextLine
        return True

    md.block.ruler.before('paragraph', 'admonition', admonition)
