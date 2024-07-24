import re
import logging
import colorlog
from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.rules_block import StateBlock
from markdown_it.renderer import RendererProtocol
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.attrs import attrs_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.footnote import footnote_plugin
from markdown_it.rules_core import StateCore
from markdown_it.common.utils import charCodeAt
import unicodedata
import subprocess
import os

def mermaid_to_svg(mermaid_text, output_path):
    # Write the Mermaid text to a temporary file
    temp_file = 'temp_mermaid.mmd'
    with open(temp_file, 'w') as file:
        file.write(mermaid_text)

    # Call the mermaid CLI to generate the SVG
    try:
        subprocess.run(['mmdc', '-i', temp_file, '-o', output_path], check=True)
        print(f'SVG successfully generated at {output_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error generating SVG: {e}')
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Create a handler
handler = logging.StreamHandler()

# Create a formatter with colorlog
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Add the formatter to the handler
handler.setFormatter(formatter)

# Add the handler to the logger
log.addHandler(handler)


# ASCII characters in Cc, Sc, Sm, Sk categories we should terminate on;
# you can check character classes here:
# http://www.unicode.org/Public/UNIDATA/UnicodeData.txt
OTHER_CHARS = ' \r\n$+<=>^`|~'

# Helper functions to get Unicode P and Z categories
UNICODE_PUNCT_RE = re.compile(r'[^\w\s]', re.UNICODE)
UNICODE_SPACE_RE = re.compile(r'\s', re.UNICODE)

def escapeRE(string):
    return re.escape(string)

def arrayReplaceAt(src, pos, newElements):
    # Create a new list by replacing elements at a specific position
    return src[:pos] + newElements + src[pos + 1:]

def abbr_def(state: StateBlock, startLine: int, endLine: int, silent: bool):
    labelEnd = -1
    pos = state.bMarks[startLine] + state.tShift[startLine]
    max_pos = state.eMarks[startLine]

    if pos + 2 >= max_pos:
        return False

    if charCodeAt(state.src, pos) != 0x2A:  # *
        return False
    pos += 1

    if charCodeAt(state.src, pos) != 0x5B:  # [
        return False
    pos += 1

    labelStart = pos

    while pos < max_pos:
        ch = charCodeAt(state.src, pos)
        if ch == 0x5B:  # [
            return False
        elif ch == 0x5D:  # ]
            labelEnd = pos
            break
        elif ch == 0x5C:  # \
            pos += 1
        pos += 1

    if labelEnd < 0 or charCodeAt(state.src, labelEnd + 1) != 0x3A:  # :
        return False

    if silent:
        return True

    label = state.src[labelStart:labelEnd].replace('\\', '')
    title = state.src[labelEnd + 2:max_pos].strip()
    if not label or not title:
        return False

    if 'abbreviations' not in state.env:
        state.env['abbreviations'] = {}

    if ':' + label not in state.env['abbreviations']:
        state.env['abbreviations'][':' + label] = title

    state.line = startLine + 1
    return True

def abbr_replace(state: StateCore):
    if 'abbreviations' not in state.env:
        return

    abbreviations = state.env['abbreviations']
    blockTokens = state.tokens

    regSimple = re.compile(
        '(?:' +
        '|'.join(
            [escapeRE(key[1:]) for key in sorted(abbreviations.keys(), key=len, reverse=True)]
        ) +
        ')'
    )

    regText = re.compile(
        '(^|{}|{}|[{}])'.format(
            UNICODE_PUNCT_RE.pattern,
            UNICODE_SPACE_RE.pattern,
            ''.join(map(escapeRE, OTHER_CHARS))
        ) +
        '(' +
        '|'.join(
            [escapeRE(key[1:]) for key in sorted(abbreviations.keys(), key=len, reverse=True)]
        ) +
        ')' +
        '($|{}|{}|[{}])'.format(
            UNICODE_PUNCT_RE.pattern,
            UNICODE_SPACE_RE.pattern,
            ''.join(map(escapeRE, OTHER_CHARS))
        )
    )

    for j in range(len(blockTokens)):
        if blockTokens[j].type != 'inline':
            continue

        tokens = blockTokens[j].children

        for i in range(len(tokens) - 1, -1, -1):
            currentToken = tokens[i]

            if currentToken.type != 'text':
                continue

            pos = 0
            text = currentToken.content
            nodes = []

            if not regSimple.search(text):
                continue

            for match in regText.finditer(text):
                if match.start() > 0 or match.group(1):
                    token = Token('text', '', 0)
                    token.content = text[pos:match.start() + len(match.group(1))]
                    nodes.append(token)

                token_o = Token('abbr_open', 'abbr', 1)
                token_o.attrs = [['title', abbreviations[':' + match.group(2)]]]
                nodes.append(token_o)

                token_t = Token('text', '', 0)
                token_t.content = match.group(2)
                nodes.append(token_t)

                token_c = Token('abbr_close', 'abbr', -1)
                nodes.append(token_c)

                pos = match.end() - len(match.group(3))

            if pos < len(text):
                token = Token('text', '', 0)
                token.content = text[pos:]
                nodes.append(token)

            if nodes:
                blockTokens[j].children = arrayReplaceAt(tokens, i, nodes)

def abbr_plugin(md: MarkdownIt):
    md.block.ruler.before('reference', 'abbr_def', abbr_def, {'alt': ['paragraph', 'reference']})
    md.core.ruler.after('linkify', 'abbr_replace', abbr_replace)


UNESCAPE_RE = re.compile(r'\\([ \\!"#$%&\'()*+,./:;<=>?@[\]^_`{|}~-])')

def superscript(state, silent):
    max_pos = state.posMax
    start = state.pos

    if state.src[start] != 0x5E:  # ^
        return False
    if silent:
        return False
    if start + 2 >= max_pos:
        return False

    state.pos = start + 1
    found = False

    while state.pos < max_pos:
        if state.src[state.pos] == 0x5E:  # ^
            found = True
            break
        state.md.inline.skipToken(state)

    if not found or start + 1 == state.pos:
        state.pos = start
        return False

    content = state.src[start + 1:state.pos]

    # don't allow unescaped spaces/newlines inside
    if re.search(r'(^|[^\\])(\\\\)*\s', content):
        state.pos = start
        return False

    # found!
    state.posMax = state.pos
    state.pos = start + 1

    token_so = Token('sup_open', 'sup', 1)
    token_so.markup = '^'
    state.tokens.append(token_so)

    token_t = Token('text', '', 0)
    token_t.content = UNESCAPE_RE.sub(r'\1', content)
    state.tokens.append(token_t)

    token_sc = Token('sup_close', 'sup', -1)
    token_sc.markup = '^'
    state.tokens.append(token_sc)

    state.pos = state.posMax + 1
    state.posMax = max_pos
    return True

def subscript(state, silent):
    max_pos = state.posMax
    start = state.pos

    if state.src[start] != 0x7E:  # ~
        return False
    if silent:
        return False
    if start + 2 >= max_pos:
        return False

    state.pos = start + 1
    found = False

    while state.pos < max_pos:
        if state.src[state.pos] == 0x7E:  # ~
            found = True
            break
        state.md.inline.skipToken(state)

    if not found or start + 1 == state.pos:
        state.pos = start
        return False

    content = state.src[start + 1:state.pos]

    # don't allow unescaped spaces/newlines inside
    if re.search(r'(^|[^\\])(\\\\)*\s', content):
        state.pos = start
        return False

    # found!
    state.posMax = state.pos
    state.pos = start + 1

    token_so = Token('sub_open', 'sub', 1)
    token_so.markup = '~'
    state.tokens.append(token_so)

    token_t = Token('text', '', 0)
    token_t.content = UNESCAPE_RE.sub(r'\1', content)
    state.tokens.append(token_t)

    token_sc = Token('sub_close', 'sub', -1)
    token_sc.markup = '~'
    state.tokens.append(token_sc)

    state.pos = state.posMax + 1
    state.posMax = max_pos
    return True

def sub_plugin(md):
    md.inline.ruler.after('emphasis', 'sub', subscript)
    md.inline.ruler.after('emphasis', 'sup', superscript)




class Walker(list):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.index = 0

    @property
    def current(self):
        return self[0]

    @property
    def next(self):
        if self.index + 1 < len(self):
            return self[1]
        return None

    def pop_next(self):
        if self.index + 1 < len(self):
            return self.pop(self.index + 1)
        return None

    def __next__(self):
        self.index += 1
        if self.index < len(self):
            return self[0]
        raise StopIteration()

    def __getitem__(self, s):
        if isinstance(s, slice):
            start = s.start + self.index if s.start is not None else self.index
            return super().__getitem__(slice(start, s.stop, s.step))
        elif isinstance(s, int):
            return super().__getitem__(s + self.index)
        else:
            raise TypeError

    def __repr__(self):
        return repr(self[:])


class LaTeXRenderer(RendererProtocol):
    def __init__(self):
        self.output = []
        self.level = 0
        super().__init__()
        prefix = 'handle_'
        self.token_handlers = {
            name[len(prefix):]: getattr(self, name)
            for name in dir(self) if name.startswith('handle_')
        }

    def render(self, tokens: Token, options, env):
        self.output = []
        walker = Walker(tokens)
        try:
            token = walker.current
            while True:
                output = self.render_token(token, walker)
                if output:
                    self.output.append(output)
                token = next(walker)
        except StopIteration:
            pass

        return ''.join(self.output)

    def render_token(self, token, walker):
        self.level += token.nesting
        if token.type in self.token_handlers:
            return self.token_handlers[token.type](token, walker)
        return self.render_default(token, walker)

    def render_children(self, token, walker):
        output = []
        if not token.children:
            return None
        for child in token.children:
            result = self.render_token(child, walker)
            if result:
                output.append(result)
        return ''.join(output)

    def render_until(self, walker, stop):
        output = []
        try:
            while token := next(walker):
                s = self.render_token(token, walker)
                if s:
                    output.append(s)
                if token.type == stop:
                    break
        except StopIteration:
            pass
        return ''.join(output)

    @property
    def padding(self):
        return '  ' * self.level

    def handle_inline(self, token, walker):
        return self.render_children(token, walker)

    def handle_text(self, token, walker):
        return token.content

    def handle_paragraph_open(self, token, walker):
        return None

    def handle_paragraph_close(self, token, walker):
        return '\n'

    def handle_heading_open(self, token, walker):
        headings = [
            'section',
            'subsection',
            'subsubsection',
            'paragraph',
            'subparagraph',
            'textbf'  # No direct equivalent in LaTeX for h6
        ]
        output = [f"\n\\{headings[int(token.tag[1:]) - 1]}{{"]
        assert walker.next.type == 'inline'
        output.append(self.render_children(next(walker), walker))
        output.append("}\n")

        self.level -= 1  # No nesting for headings
        return ''.join(output)

    def handle_heading_close(self, token, walker):

        self.level += 1 # No nesting for headings
        return '\n'

    def handle_strong_open(self, token, walker):
        return "\\textbf{"

    def handle_strong_close(self, token, walker):
        return "}"

    def handle_em_open(self, token, walker):
        return "\\emph{"

    def handle_em_close(self, token, walker):
        return "}"

    def handle_code_inline(self, token, walker):
        if m := re.match(r'^#\!(\w+)(.*)$', token.content):
            return f"\\lstinline[language={m.group(1)}]{{{m.group(2)}}}"
        return f"\\lstinline{{{token.content}}}"

    def handle_image(self, token, walker):
        output = []
        output.append("\\begin{figure}[H]\n")
        output.append("   \\centering\n")
        output.append(f"   \\includegraphics{{{token.attrs['src']}}}\n")
        if token.children:
            output.append(f"   \\caption{{{self.render_children(token, walker)}}}\n")
        output.append("\\end{figure}")
        return ''.join(output)

    def handle_admonition_open(self, token, walker):
        output = f"\\begin{{admonition}}{{{token.meta['tag']}}}"
        assert walker.next.type == 'admonition_title_open'

        return output

    def handle_admonition_close(self, token, walker):
        return "\\end{admonition}\n"

    def handle_admonition_title_open(self, token, walker):
        return None

    def handle_admonition_title_close(self, token, walker):
        return None

    def handle_math_block(self, token, walker):
        return f"\\[\n{token.content}\n\\]\n"

    def handle_html_block(self, token, walker):
        if token.content.startswith('<!--'):
            return f"\\begin{{verbatim}}\n{token.content[4:-4]}\n\\end{{verbatim}}\n"
        return None

    def handle_fence(self, token, walker):
        return "\\begin{lstlisting}" + \
            f"{{language={token.info}}}\n" + \
            f"{token.content}" + \
            "\\end{lstlisting}\n"

    def handle_ordered_list_open(self, token, walker):
        output = self.padding
        output += "\\begin{enumerate}\n"
        output += self.render_until(walker, 'ordered_list_close')
        return output

    def handle_ordered_list_close(self, token, walker):
        return f"{self.padding}\\end{{enumerate}}\n"

    def handle_bullet_list_open(self, token, walker):
        output = self.padding
        output += "\\begin{itemize}\n"
        output += self.render_until(walker, 'bullet_list_close')
        return output

    def handle_bullet_list_close(self, token, walker):
        return "\\end{itemize}\n"

    def handle_list_item_open(self, token, walker):

        if walker.next.type == 'paragraph_open' and walker[2].type == 'inline' and walker[2].children[0].type == 'html_inline':
            html_inline = walker[2].children[0]
            if 'checked="checked"' in html_inline.content:
                return f"{self.padding}\\CorrectChoice "
            else:
                return f"{self.padding}\\Choice "
        return f"{self.padding}\\item "

    def handle_list_item_close(self, token, walker):
        return "\n"

    def handle_link_open(self, token, walker):
        return f"\\href{{{token.attrs['href']}}}{{"

    def handle_link_close(self, token, walker):
        return "}"

    def handle_softbreak(self, token, walker):
        return "\\par"

    def handle_s_open(self, token, walker):
        return "\\sout{"

    def handle_s_close(self, token, walker):
        return "}"

    def handle_html_inline(self, token, walker):
        if 'task-list-item-checkbox"' in token.content:
            return None # Handled by list item
        return f"%% HTML\n{self.render_children(token, walker)}\n%% END HTML\n"

    def handle_sub_open(self, token, walker):
        return "\\textsubscript{"

    def handle_sub_close(self, token, walker):
        return "}"

    def handle_footnote_ref(self, token, walker):
        return f"\\footnote{{{token.meta['id']}}}"

    def handle_footnote_block_open(self, token, walker):
        return "\\begin{footnotes}\n"

    def handle_footnote_block_close(self, token, walker):
        return "\\end{footnotes}\n"

    def handle_footnote_open(self, token, walker):
        return "\\footnote{{"

    def handle_footnote_close(self, token, walker):
        return "}"

    def handle_footnote_anchor(self, token, walker):
        return f"\\footnotemark[{token.meta['id']}]"

    def handle_sup_open(self, token, walker):
        return "\\textsuperscript{"

    def handle_sup_close(self, token, walker):
        return "}"

    def handle_table_open(self, token, walker):
        # Determine the number of columns
        columns = []
        for sibling in walker:
            if sibling.type == 'tr_close':
                break
            if sibling.type == 'th_open':
                style = sibling.attrs.get('style', None)
                if 'text-align:left' in style:
                    columns.append('l')
                elif 'text-align:right' in style:
                    columns.append('r')
                elif 'text-align:center' in style:
                    columns.append('c')
                else:
                    columns.append('l')
        coldef = ''.join(columns)
        return f"\\begin{{table}}[H]\n\\centering\n\\begin{{tabular}}{{{coldef}}}\n"

    def handle_table_close(self, token, walker):
        return "\\end{table}\n"

    def handle_tr_open(self, token, walker):
        return "   "

    def handle_tr_close(self, token, walker):
        return "\n"

    def handle_td_open(self, token, walker):
        return "   "

    def handle_td_close(self, token, walker):
        return " & " if not walker.next.type == 'tr_close' else " \\\\\n"

    def handle_th_open(self, token, walker):
        return "\\textbf{"

    def handle_th_close(self, token, walker):
        return "}" + (" & " if not walker.next.type == 'tr_close' else " \\\\\n")


    def handle_thead_open(self, token, walker):
        return "\\toprule\n"

    def handle_thead_close(self, token, walker):
        return "\\midrule\n"

    def handle_tbody_open(self, token, walker):
        return None

    def handle_tbody_close(self, token, walker):
        return "\\bottomrule\n"

    def render_default(self, token, walker):
        log.error("Unhandled token: %s", token)
        self.output.append(f"\\begin{{verbatim}}\n   {token}\n\\end{{verbatim}}\n")

PLUGINS = [
    dollarmath_plugin,
    admon_plugin,
    attrs_plugin,
    deflist_plugin,
    tasklists_plugin,
    footnote_plugin,
    sub_plugin,
    abbr_plugin
]

ENABLES = [
    'table',
    'strikethrough'
]

class Parser:
    def __init__(self, plugins=PLUGINS, enables=ENABLES):
        self.md = MarkdownIt()
        for enable in enables:
            self.md = self.md.enable(enable)
        for plugin in plugins:
            self.md = self.md.use(plugin)

        self.md.renderer = LaTeXRenderer()

    def render(self, text):
        return self.md.render(text)

p = Parser()
print(p.render(open('test.md').read()))
