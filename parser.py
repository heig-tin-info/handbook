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

PLUGINS = [
    dollarmath_plugin,
    admon_plugin,
    attrs_plugin,
    deflist_plugin,
    tasklists_plugin,
    footnote_plugin
]

ENABLES = [
    'table',
    'strikethrough'
]


UNESCAPE_RE = re.compile(r'\\([ \\!"#$%&\'()*+,./:;<=>?@[\]^_`{|}~-])')

def superscript(state, silent):
    max_pos = state.posMax
    start = state.pos

    if state.srcCharCode[start] != 0x5E:  # ^
        return False
    if silent:
        return False
    if start + 2 >= max_pos:
        return False

    state.pos = start + 1
    found = False

    while state.pos < max_pos:
        if state.srcCharCode[state.pos] == 0x5E:  # ^
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

    if state.srcCharCode[start] != 0x7E:  # ~
        return False
    if silent:
        return False
    if start + 2 >= max_pos:
        return False

    state.pos = start + 1
    found = False

    while state.pos < max_pos:
        if state.srcCharCode[state.pos] == 0x7E:  # ~
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
            while token := next(walker):
                output = self.render_token(token, walker)
                if output:
                    self.output.append(output)
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

    def handle_inline(self, token, walker):
        return self.render_children(token, walker)

    def handle_text(self, token, walker):
        return token.content

    def handle_paragraph_open(self, token, walker):
        return '\n'

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
        output = [f"\\{headings[int(token.tag[1:])]}{{"]
        assert walker.next.type == 'inline'
        output.append(self.render_children(next(walker), walker))
        output.append("}\n")
        return ''.join(output)

    def handle_heading_close(self, token, walker):
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

    def handle_bullet_list_open(self, token, walker):
        output = "\\begin{itemize}\n"
        output = self.render_until(walker, 'bullet_list_close')
        return output

    def handle_bullet_list_close(self, token, walker):
        return "\\end{itemize}\n"

    def handle_list_item_open(self, token, walker):
        return "   \\item "

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

    def render_default(self, token, walker):
        log.error("Unhandled token: %s", token)
        self.output.append(f"\\begin{{verbatim}}\n   {token}\n\\end{{verbatim}}\n")


class Parser:
    def __init__(self, plugins=PLUGINS, enables=ENABLES):
        self.md = MarkdownIt()
        for enable in enables:
            self.md = self.md.enable(enable)
        for plugin in plugins:
            self.md = self.md.use(plugin)
        sub_plugin(self.md)
        self.md.renderer = LaTeXRenderer()

    def render(self, text):
        return self.md.render(text)

p = Parser()
print(p.render(open('test.md').read()))
