from bs4 import BeautifulSoup, NavigableString

html = r"""
<strong><em>Foo&</em> bar&</strong>
<em>Foo& <strong>bar&</strong></em>
"""

soup = BeautifulSoup(html, 'html.parser')

class LaTeXString(NavigableString):
    def __init__(self, value, escape=False):
        if escape:
            value = self._escape_latex(value)
        super().__init__(value)

class Tag:
    def __init__(self, soup):
        self.soup = soup

    def append(self, tag):
        self.children.append(tag)

    def __repr__(self):
        return f'<{self.name}>'
def walk(soup):
    for tag in soup.children:
        if tag.name:
            yield tag
            yield from walk(tag)
