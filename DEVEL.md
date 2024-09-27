# Extensions/Hooks/Hacks

This document describes the custom extensions written for this project.

## Abbreviations (`hooks/abbr.py`)

![Example in MIT](docs/assets/snapshots/wiki-abbr.png)

MkDocs Material features support for PHP Markdown Extra syntax for abbreviations:

```markdown
*[ANSI]: American National Standards Institute
```

Which is rendered as the following everywhere in the document:

```html
<abbr title="American National Standards Institute">ANSI</abbr>
```

This feature is quite limited as it only supports a single line and hides the events on hyperlinks (popup). It is less interesting than a reference to Wikipedia.

The goal is to extend the PHP Markdown Extra syntax to replace abbreviations with links to Wikipedia if the abbreviation is a link to Wikipedia. This is done by adding a hook to the Markdown parser. Here a Wiki link

```markdown
*[ANSI]: https://en.wikipedia.org/wiki/American_National_Standards_Institute
```

This hook will be used with the wiki hook.

## Wikipedia (`hooks/wiki.py`)

This hook fetches from Wikipedia API a summary for each wiki link in the documentation. All summaries are saved in `links.yml`. Here the value for MIT:

```yaml
wikipedia:
  https://fr.wikipedia.org/wiki/Massachusetts_Institute_of_Technology:
    title: Massachusetts Institute of Technology
    thumbnail:
      source:
        https://upload.wikimedia.org/wikipedia/fr/thumb/4/44/MIT_Seal.svg/langfr-320px-MIT_Seal.svg.png
      width: 320
      height: 320
    tid: 9e2ca5e0-4b4f-11ef-ac93-7845222a8ccc
    timestamp: '2024-07-26T13:04:40Z'
    description: université américaine à Cambridge, Massachusetts
    extract: >
      Le Massachusetts Institute of Technology, en français Institut
      de technologie du Massachusetts, est un institut de recherche
      américain et une université, spécialisé dans les domaines de la
      science et de la technologie. Établissement privé situé à Cambridge,
      dans l'État du Massachusetts, à proximité immédiate de Boston,
      au Nord-Est des États-Unis, le MIT est considéré comme une des
      meilleures universités du monde.
    key: fr-massachusetts-institute-of-technology
    plainlink: https://fr.wikipedia.org/wiki/Massachusetts_Institute_of_Technology
```

The summary is served on the front-end and with a tooltip on hover, the thumbnail, title and summary is displayed.

![Example of Bjarne Stroupstrup](docs/assets/snapshots/bjarne-stroupstrup.png)

The involved files are:

- [`hooks/wiki.py`](hooks/wiki.py): The hook that fetches the data from Wikipedia
- [`docs/js/wiki-tips.js`](docs/js/wiki-tips.js): The JavaScript that displays the tooltip
- [`links.yml`](links.yml): The file that stores the summaries

## Unicode (`hooks/unicode.py`) and Regex (`hooks/regex.py`)

The goal is to enhance regexes and unicode chars code `U+...` and `s/abc/def` with a link to the Unicode website and a link to the regex101 website.

![Example of balloons for Regex and Unicode](docs/assets/snapshots/regex-unicode.png).

This hook is very specific, but we could imagine to integrate it in a more general hook in the MkDocs Material theme. The involved files are:

- [`hooks/unicode.py`](hooks/unicode.py): The hook for Unicode.
- [`hooks/regex.py`](hooks/regex.py): The hook for Regex.
- [`docs/css/extras.css`](docs/css/extras.css): The CSS that displays the balloons.

## Tags (`hooks/tags.py`)

MkDocs Material Tags feature is currently limited to insiders. Tags can be created per page in the metadata. Tags can increase searchability and categorization of the content, but it is limited to the page level.

![Example of tags](docs/assets/snapshots/tags.png)

This hook features a way to attach tags to any heading. This is particularly interesting for my use case where I write a programming course. Each topic or language keyword can be a tag.

Additionnaly, the general goal for this course is to generate both a static website and a printable PDF book. In a book, tags can become index entries.

The way of adding tags is the following:

```markdown
Here a [[tag]] in the text. Plurials are also possible [[tags|tag]].
For the specific case of printed version, index entry can be tweaked
[[The Matrix|Matrix|Matrix, The]]. Invisible tags are also possible [[|tag]] and only index entry can be inserted with [[||entry]].
```

The involved files are:

- [`hooks/tags.py`](hooks/tags.py): The hook

## Mermaid

Mermaid diagrams can be rendered directly in the browser. However they cannot be displayed with a figcaption. This hook extracts the first comment in the mermaid code and displays it as a caption.

![Example of Mermaid with caption](docs/assets/snapshots/mermaid-title.png)

The involved files are:

- [`hooks/mermaid.py`](hooks/mermaid.py): The hook

## French

MkDocs Material isn't very good with French. French has a lot of special rules for typography. This hook is more a durty hack because it is complicated to respect all the rules. Currenlty it adds some French typography rules to your MkDocs project:

- Add a thin space before `!`, `?`, `:` and `;` punctuation marks.
- Use french quote (« and ») around quoted text.
- Use long dash (—) lists.
- Translate admonition titles (MkDocs Material doesn't support native translation of admonition titles).

## Epigraph

Epigraphs are quotes at the beginning of a chapter. They are usually displayed in italic and with a right alignment. This hook adds a new syntax for epigraphs. It is used in the metadata of the markdown file:

```text
---
epigraph:
    text: "C is quirky, flawed, and an enormous success."
    source: Dennis Ritchie
---
```

![Epigraph example](docs/assets/snapshots/epigraph.png)


## Drawio

Drawio is a great tool for creating diagrams, but MkDocs Material does not support it. This hook allows to display drawio diagrams in the documentation. The drawio diagrams are rendered in the browser and can be clicked to see them in full screen.

A fix is also applied to make it compatible with the GLightbox plugin.

On the frontend, colors are updated to match the theme colors :

![Example of Drawio diagram](docs/assets/snapshots/drawio-light.png)

![Example of Drawio diagram](docs/assets/snapshots/drawio-slate.png)


The involved files are:

- [`hooks/drawio.py`](hooks/drawio.py): The hook
- [`docs/js/drawio.js`](docs/js/drawio.js): The JavaScript that displays the drawio diagrams
- [`docs/js/viewer.min.js`](docs/js/viewer.min.js): Drawio viewer from the drawio website
- [`docs/css/drawio.css`](docs/css/drawio.css): The CSS that displays the drawio diagrams

## LaTeX

MkDocs misses one huge feature: Beautiful PDF generation. I've tried pandoc and several plugins, but generating a book has tons of tricky parts. I eventually decided to write my own MkDocs Material to PDF converter using LaTeX. This is a huge work in progress because despite it is working pretty well, it is still far from production ready.

I initially wanted to start conversion from the Markdown content, but I quickly realized that parsing Markdown with all the extensions and hooks is too complicated. Moreover, a lot of plugins are not applied in the Markdown content, but in the HTML rendererd content. It is though easier to parse XML than Markdown.

Also, a lots of plugins make changes in the HTML in such way that numerous little tricks are needed to convert it to LaTeX. That's why I implemented my own LaTeX renderer.

To start with this plugins, you have to add a `latex` section in your `mkdocs.yml` file to declare your books. Here an example:

```yml
extra:
  latex:
    build_dir: build
    mermaid_config: tex/mermaid-config.json
    books:
      - root: Cours C
        title: L'informatique pour l'ingénieur
        subtitle: Cours de programmation en C
        output_folder: book
        email: yves.chevallier@heig-vd.ch
        frontmatter:
          - Préface
        backmatter:
          - colophon
        copy_files:
          docs/assets/c-logo.pdf: assets/
          tex/*.sty: .
```

This configuration uses custom `mermaid-config` to set the printed colors, the book entry section is set with the `root` key. Some sections can be moved to the frontmatter or backmatter. Some files can be copied to the output folder depending on the theme...

![Example of LaTeX book](docs/assets/snapshots/book.png)

Mermaid diagrams, drawio, images must be converted to PDF. The transformers are in charge of converting the images to PDF.

The formatter uses Jinja templates to convert html to LaTeX.

The involved files are:

- [`hooks/latex.py`](hooks/latex.py): The hook
- `hooks/latex/`: LaTeX Renderer, formatter and transformer
- `hooks/latex/templates`: Jinja templates
