"""
- [ ] Footnotes
"""
import logging
import mkdocs
from pathlib import Path
from IPython import embed

from processor import LaTeXRenderer
log = logging.getLogger('mkdocs')

files_to_process = []
latex_dir = Path('build')

renderer = LaTeXRenderer(latex_dir)

def on_nav(nav, config, files):
    book = 'Chapter'
    for section in nav:
        if section.title == book:
            for page in section.children:
                files_to_process.append(page.file)

def on_env(env, config, files):
    # Create output directory
    latex_dir.mkdir(exist_ok=True)

    for file in files:
        if file.src_path.endswith('.md'):
            path = latex_dir / file.src_path.replace('.md', '.tex')
            path.parent.mkdir(parents=True, exist_ok=True)

            html = file.page.content
            latex = renderer.render(html, latex_dir)
            with open(path, 'w') as f:
                f.write(latex)
