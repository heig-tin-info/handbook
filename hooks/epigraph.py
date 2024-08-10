from mkdocs.utils import log
from IPython import embed

def on_page_content(html, page, config, files):
    if 'epigraph' not in page.meta:
        return html
    text = page.meta['epigraph']['text']
    source = page.meta['epigraph']['source']
    lines = html.split('\n')
    # Find first header tag
    for i, line in enumerate(lines):
        if '<h' in line:
            lines.insert(i + 1, (
                f'<blockquote class="epigraph">{text}'
                f'<footer>{source}</footer></blockquote>'))
            break
    else:
        log.warning('No header found in %s', page.file.src_path)

    return '\n'.join(lines)
