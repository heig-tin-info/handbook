"""
- [ ] Footnotes
"""
import logging
import mkdocs
from pathlib import Path
from IPython import embed
from mkdocs.structure.nav import Section
from processor import LaTeXRenderer
log = logging.getLogger('mkdocs')

files_to_process = []
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

def on_nav(nav, config, files):
    global files_to_process
    book = 'Cours C'
    for section in nav:
        if section.title == book:
            files_to_process = fetch_files(section)


def on_env(env, config, files):
    # Create output directory
    latex_dir.mkdir(exist_ok=True)

    for file in files_to_process:
        log.info(f'Processing LaTeX {file.src_path}...')
        if file.src_path.endswith('.md'):
            path = latex_dir / file.src_path.replace('.md', '.tex')
            path.parent.mkdir(parents=True, exist_ok=True)

            html = file.page.content
            latex = renderer.render(html, latex_dir)
            with open(path, 'w') as f:
                f.write(latex)
