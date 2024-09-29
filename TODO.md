# TO-DO And Bugs

## Content update

- [ ] Hand drawn flow diagram `https://i.sstatic.net/WdbInYwX.png`
- [ ] Show top-down approach `https://i.sstatic.net/wC9Tb8Y8.png`
- [ ] Part metaprogramming (Jinja/Python...)
- [ ] Compilation croisée
- [ ] Threading? SIMD
- [ ] Add section for courses with links to the only required stuff.

## Improvements

- [ ] Find a way to add crop cut on PDF as we don't use A4 format
- [ ] Better separation terms and definitions, acronyms, glossary
- [ ] Integrate bibliography (extra pages in backmatter)
- [ ] Chapter "Crédits des illustrations" in backmatter (ai generated?)
- [ ] Improve syntax for tags/index
- [ ] Make all figures compatible with both light/dark theme
  - [ ] Adapt SVG color when added in object
- [ ] Index table entry with many refs cuz ugly line break indent

## Bugs

- [ ] When `[](){#...}` before first title in a page it affects the title in toc
- [ ] Allow for code inline and markdown inline in table captions
- [ ] Code with title doesn't display well in LaTeX
- [ ] Image with width should be included with the correct size
- [ ] Implement local links to code, copy them in appencies
- [ ] Table des opérateurs, find a way
- [ ] Table size should be always slighly smaller than the normal text
- [ ] Autres tables, largeur, ajuster au contenu ? tabularx ?
- [ ] Find a way to have "short caption" on figures (maybe use alt text)
- [ ] Label for tables are cropped, should be placed above tables
- [ ] Exercises
  - [ ] Exercise plugin cause code to be renamed exercise
  - [ ] Exercises numbering (restart at each section)
  - [ ] Exercises Colors for fill-in-the-blank in slate theme
  - [ ] See solution of exercises without specific type.
  - [ ] Vertical alignment of multiple choices
  - [ ] Multicolumn for exercises (Validité des identificateurs)
  - [ ] Two/Three columns for exercises not working
  - [ ] Exercise in title Exercice 35 : Exercise : Promotion numérique
- [ ] Mkdocs Material Highlights tags by adding a space after the highlight.
- [ ] Mermaid width too wide
- [ ] [Albatros](/assets/src/albatros.txt) ref null
- [ ] Remove preambule… text introductif dans introductions ?
- [ ] Mal géré en LaTeX enuermate followed by itemize
- [ ] Size caption of tables and figures is different
- [ ] Carret position in "Opérateurs d'affectation" for XOR

## New Features (MkDocs, plugins)

- [ ] Split document in multiple volumes
- [ ] Reaveal js slides --> see on slides branch
- [ ] Allow to create nav with subsections (build only info1 chapters)
- [ ] Flexible tables parameter for adjusting width, fullwidth
- [ ] Embedded Interactive examples (linked-list)...
- [ ] Annotate code with circled number that can be used in text (see plug)
- [ ] Interactive exercices
  - [ ] Code execution
  - [ ] Fill the gap
- [ ] Flexible table
- [ ] Code execution (adapt dates, things...)

## Fix in mkdocs-material

- [ ] Allow for optional feedback title
- [ ] Translation for permalink title
- [.] Tags spacing in theme (search) (.md-tag margin-right: 0.5em;)
- [ ] Exercises are all checked
- [ ] Bug with examples
