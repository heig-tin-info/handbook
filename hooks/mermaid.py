"""
<figure id="_figure-1"><a class="glightbox" data-desc-position="bottom" data-height="auto" data-type="image"
data-width="auto" href="http://127.0.0.1:8000/handbook/assets/images/thompson-kernighan-ritchie.webp">

<img alt="Les pères fondateurs du C" src="http://127.0.0.1:8000/handbook/assets/images/thompson-kernighan-ritchie.webp"></a>

<figcaption> Les pères fondateurs du C</figcaption></figure>

<div class="mermaid"></div>

"""

import re

from bs4 import BeautifulSoup, Tag


def on_page_content(html, page, config, files):
    soup = BeautifulSoup(html, "html.parser")
    for el in soup.find_all("pre", class_="mermaid"):
        title = None
        if code := el.find("code"):
            if match := re.match(r"^%%\s*(.+)$", code.get_text(), re.MULTILINE):
                title = match.group(1)

        if not title:
            continue

        figure = Tag(name="figure", attrs={"class": "mermaid-figure"})
        figcaption = Tag(name="figcaption")
        figcaption.string = title

        el.wrap(figure)
        figure.append(figcaption)

    return str(soup)
