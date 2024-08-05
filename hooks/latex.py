"""
- [ ] Footnotes
"""
import logging
import mkdocs
from pathlib import Path, PosixPath
from IPython import embed
from mkdocs.structure.nav import Section
from latex.renderer import LaTeXRenderer
import yaml
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
enabled = False
renderer = None

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

def on_startup(command, dirty):
    global enabled
    global renderer
    enabled = command != 'serve'

    if enabled:
        renderer = LaTeXRenderer(latex_dir)

def on_nav(nav, config, files):
    global files_to_process
    global book_nav
    global saved_nav
    if not enabled:
        return
    book = 'Cours C'
    for section in nav:
        if section.title == book:
            break

    level = -1
    latex = []

    def get_nav(section: Section, level):
        for child in section.children:
            if child.is_page:
                files_to_process.append((child.file, level))
                # Replace md with tex
                tex_path = child.file.src_path.replace('.md', '.tex')
                latex.append(f'\\input{{{tex_path}}}')
            else:
                latex.append('\n')
                latex.append(renderer.formatter.heading(child.title, level=level))
                get_nav(child, level + 1)

    get_nav(section, level)
    book_nav = '\n'.join(latex)

def on_env(env, config, files):
    if not enabled:
        return

    # Create output directory
    latex_dir.mkdir(exist_ok=True)
    project_dir = Path(config.config_file_path).parent / config['docs_dir']

    for file, level in files_to_process:
        log.info(f'Processing LaTeX {file.src_path} (level {level})...')
        if file.src_path.endswith('.md'):
            path = latex_dir / file.src_path.replace('.md', '.tex')
            path.parent.mkdir(parents=True, exist_ok=True)

            html = file.page.content

            with open(path.with_suffix('.html'), 'w', encoding='utf-8') as f:
                f.write(html)

            latex = renderer.render(
                html,
                latex_dir, project_dir / file.src_path,
                level)

            path.write_text(latex)


    # Save assets map and clean unused assets
    def path_representer(dumper, data):
        # Path relative to the project directory
        data = data.resolve().relative_to(Path(config.config_file_path).parent)
        return dumper.represent_scalar('tag:yaml.org,2002:str', str(data))
    yaml.add_representer(PosixPath, path_representer)

    assets_map = renderer.get_assets_map()

    # Remove unused objets (list build/assets directors and remove those that are not in assets_map keys)
    for file in (latex_dir / 'assets').iterdir():
        if file not in assets_map:
            log.info(f'Removing unused asset {file}')
            #file.unlink()

    with(open(latex_dir / 'assets_map.yml', 'w')) as f:
        assets_map = yaml.dump(assets_map, default_flow_style=False, allow_unicode=True)
        f.write(assets_map)

    # Build index page
    index = renderer.formatter.template(content=book_nav)
    (latex_dir / 'index.tex').write_text(index)

    Path('build/acronyms.tex').write_text(renderer.get_list_acronyms())
    Path('build/glossary.tex').write_text(renderer.get_list_glossary())
    Path('build/solutions.tex').write_text(renderer.get_list_solutions())
