"""
- [ ] Footnotes
"""
import logging
import mkdocs
from pathlib import Path
from IPython import embed
from mkdocs.structure.nav import Section
from processor import LaTeXRenderer
import ipdb
import sys
def excepthook(type, value, traceback):
    ipdb.post_mortem(traceback)

sys.excepthook = excepthook

log = logging.getLogger('mkdocs')

files_to_process = []
book_nav = []
saved_nav = []
latex_dir = Path('build')

renderer = LaTeXRenderer(latex_dir)

def fetch_files(section: Section):
    files = []
    for child in section.children:
        if child.is_page:
            files.append(child.file)
        else:
            files.extend(fetch_files(child))
    return files

def build_nav(section: Section, node):
    for child in section.children:
        if child.is_page:
            node.append(child.file.src_path)
        else:
            new_node = []
            node.append([child.title, new_node])
            build_nav(child, new_node)

def on_nav(nav, config, files):
    global files_to_process
    global book_nav
    global saved_nav
    book = 'Cours C'
    for section in nav:
        if section.title == book:
            break

    level = 0
    latex = []

    def get_nav(section: Section, level):
        for child in section.children:
            if child.is_page:
                files_to_process.append((child.file, level))
                # Replace md with tex
                tex_path = child.file.src_path.replace('.md', '.tex')
                latex.append(f'\input{{{tex_path}}}')
            else:
                latex.append('\n')
                latex.append(renderer.formatter.heading(child.title, level=level))
                get_nav(child, level + 1)

    get_nav(section, level)
    book_nav = '\n'.join(latex)

def on_env(env, config, files):

    # Create output directory
    latex_dir.mkdir(exist_ok=True)
    project_dir = Path(config.config_file_path).parent / config['docs_dir']

    for file, level in files_to_process:
        log.info(f'Processing LaTeX {file.src_path}...')
        if file.src_path.endswith('.md'):
            path = latex_dir / file.src_path.replace('.md', '.tex')
            path.parent.mkdir(parents=True, exist_ok=True)

            html = file.page.content
            latex = renderer.render(html, latex_dir, project_dir / file.src_path, level)
            with open(path, 'w') as f:
                f.write(latex)

            with open(path.with_suffix('.html'), 'w') as f:
                f.write(html)

    # Build index
    index = renderer.formatter.template(content=book_nav,
                                        glossary=renderer.formatter.get_glossary())
    with open(latex_dir / 'index.tex', 'w') as f:
        f.write(index)
