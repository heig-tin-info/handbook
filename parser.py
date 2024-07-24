import re
import logging
from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.rules_block import StateBlock
from markdown_it.renderer import RendererProtocol
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.attrs import attrs_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.tasklists import tasklists_plugin


log = logging.getLogger(__name__)

PLUGINS = [
    dollarmath_plugin,
    admon_plugin,
    attrs_plugin,
    deflist_plugin,
    tasklists_plugin
]

ENABLES = [
    'table',
    'strikethrough'
]


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
        self.token_handlers = {
            'heading_open': self.heading_open,
            'heading_close': self.heading_close,
            'paragraph_open': self.paragraph_open,
            'paragraph_close': self.paragraph_close,
            'inline': self.inline,
            'text': self.text,
            'strong_open': self.strong_open,
            'strong_close': self.strong_close,
            'em_open': self.em_open,
            'em_close': self.em_close,
            'code_inline': self.code_inline,
            'image': self.image,
            'admonition_open': self.admonition_open,
            'admonition_close': self.admonition_close,
            'admonition_title_open': self.admonition_title_open,
            'admonition_title_close': self.admonition_title_close,
            'math_block': self.math_block,
            'html_block': self.html_block,
            'fence': self.fence
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
        for child in token.children:
            result = self.render_token(child, walker)
            if result:
                output.append(result)
        return ''.join(output)

    def inline(self, token, walker):
        pass

    def text(self, token, walker):
        return token.content

    def paragraph_open(self, token, walker):
        return '\n'

    def paragraph_close(self, token, walker):
        return '\n'

    def heading_open(self, token, walker):
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

    def heading_close(self, token, walker):
        return '}\n'

    def strong_open(self, token, walker):
        return "\\textbf{"

    def strong_close(self, token, walker):
        return "}"

    def em_open(self, token, walker):
        return "\\emph{"

    def em_close(self, token, walker):
        return "}"

    def code_inline(self, token, walker):
        return f"\\lstinline{{{token.content}}}"

    def image(self, token, walker):
        output = []
        output.append("\\begin{figure}[H]\n")
        output.append("   \\centering\n")
        output.append(f"   \\includegraphics{{{token.attrs['src']}}}\n")
        if token.children:
            output.append(f"   \\caption{{{self.render_children(token, walker)}}}\n")
        output.append("\\end{figure}")
        return ''.join(output)

    def admonition_open(self, token, walker):
        output = "\\begin{{admonition}}{{{token.meta['tag']}}}"
        assert walker.next.type == 'admonition_title_open'

        return output

    def admonition_close(self, token, walker):
        return "\\end{admonition}\n"

    def admonition_title_open(self, token, walker):
        return None

    def admonition_title_close(self, token, walker):
        return None

    def math_block(self, token, walker):
        return f"\\[{token.content}\\]\n"

    def html_block(self, token, walker):
        if token.content.startswith('<!--'):
            return f"\\begin{{verbatim}}\n{token.content[4:-4]}\n\\end{{verbatim}}\n"
        return None

    def fence(self, token, walker):
        return "\\begin{lstlisting}" + \
            f"{{language={token.info}}}\n" + \
            f"{token.content}" + \
            "\\end{lstlisting}\n"

    def render_default(self, token, walker):
        self.output.append(f"\\begin{{verbatim}}\n   {token}\n\\end{{verbatim}}\n")


class Parser:
    def __init__(self, plugins=PLUGINS, enables=ENABLES):
        self.md = MarkdownIt()
        for enable in enables:
            self.md = self.md.enable(enable)
        for plugin in plugins:
            self.md = self.md.use(plugin)
        self.md = self.md
        self.md.renderer = LaTeXRenderer()

    def render(self, text):
        return self.md.render(text)

p = Parser()
print(p.render(open('test.md').read()))
