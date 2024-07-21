"""
Mkdocs doesn't handle absolute links well, especially when combined
with certain plugins. By default, Mkdocs validates links with the
following configuration:

validation:
  links:
    absolute_links: info

This configuration raises a warning for every absolute link found in the
documentation. To avoid these warnings and ensure compatibility, this hook
replaces absolute links with relative ones. It assumes that the assets folder
is located in the docs/assets directory.

The hook uses a regular expression to find links in the markdown content
and replaces any absolute link pointing to the assets directory with a
relative link based on the page's location.

It allows links to be written as follows:

```markdown
![Image]({assets}/image.png)
```
"""

import re
import mkdocs
import os
import logging
from pathlib import Path

log = logging.getLogger('mkdocs')

RE = re.compile(r"(\[[^\]]+\]\(){assets}([^\)]+\))")

@mkdocs.plugins.event_priority(100)
def on_page_markdown(markdown, page, config, files):
    project = Path() / 'docs'
    page_url = (project / Path(page.file.url)).resolve().parent
    assets_dir = (project / 'assets').resolve()
    relpath = os.path.relpath(assets_dir, page_url)

    def replace(match):
        return f"{match.group(1)}{relpath}{match.group(2)}"

    return RE.sub(replace, markdown)
