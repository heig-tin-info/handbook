import pandoc
import logging
import mkdocs
from pathlib import Path
import stopwatch as sw
log = logging.getLogger('mkdocs')
pages = []

stopwatch = sw.Stopwatch()

page_order = []

def on_nav(nav, config, files):
    for page in nav.pages:
        page_order.append(page.file.src_path)

    return nav

@mkdocs.plugins.event_priority(-100)
def on_page_markdown(markdown, page, config, files):
    stopwatch.start()
    doc = pandoc.read(markdown)
    pages.append({'file': page.file, 'doc': pandoc.write(doc, format='latex', options=[
        '--listings',
        # '-t markdown-simple_tables',
        '-r markdown-auto_identifiers'
    ])})
    stopwatch.stop()

def on_post_build(config):
    log.info(f"Hooks LaTeX done in {stopwatch.total:.2f} seconds.")

    project_dir = Path(config.config_file_path).parent
    output_dir = Path(project_dir / 'build' / 'latex')

    if output_dir.exists():
        for file in output_dir.glob('*'):
            file.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)

    log.error(page_order)

    for page in pages:
        # Add .tex extension to the file name
        with open((output_dir / page['file'].name).with_suffix('.tex'), 'w') as f:
            f.write(page['doc'])
