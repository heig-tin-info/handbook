# LaTeX Renderer for MkDocs (Material)

## Order of Precedence

As the strategy is to use BeautifulSoup to iteratively parse the HTML and replace LaTeX code with images, the order of precedence is important.

The reason is some tags cannot be nested within others, and text must be escaped because LaTeX is capricious about chars such as `&` and `_`.

Take the following example:

```html
<strong><em>Foo&</em> bar&</strong>
<em>Foo& <strong>bar&</strong></em>
```

```markdown
*[**abc**](def)*
H^**2**^*O*
```

First pass:

```html
<strong><latex>\emph{Foo\&}</latex> bar&</strong>
<em>Foo& <latex>bar\&</latex></em>
```

Second pass:

```html
<strong><latex>\emph{Foo\&}</latex> bar&</strong>
<em>Foo& <latex>bar\&</latex></em>


## Strategy

- NavigableString are text nodes they are safe to be escaped
- Eventually, all NavigableString will be replaced with LaTeXString

```python
latekize(soup)
```

Will iterate over the soup, if all are either NavigableString or LaTeXString,
then the entire soup will be replaced with a LaTeXString.


## Features

- **bold** (strong)
- *italic* (emphasis)
- ***bold italic*** (strong emphasis)
- H^2^O (superscript)
- CO~2~ (subscript)
- Critics
  - {--deleted--} (red strikethrough)
  - {++inserted++} (green underline)
  - {~~highlighted~>none~~} (added/changed)
  - {==marked==} (highlighted)
  - {>>comment<<} (comment)
- `unformatted inline code` (minted inline)
- `#!python formatted inline block` (minted inline)
