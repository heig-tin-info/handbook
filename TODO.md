# TO-DO And Bugs

## Content update

- [ ] Complete Algorithmes utilitaires (split, slurp, join, trim)
- [ ] Complete part quality and security (buffer overflow... libfuzzer)
- [ ] Hand drawn flow diagram https://i.sstatic.net/WdbInYwX.png
- [ ] Add some algorithms from Numeriacl Recipes
  - [ ] Gauss Jordan 36
  - [ ] QR Decomposition 108
  - [ ] Chebyshev Approximation 190
  - [ ] Padé Appromants 200
  - [ ] Jacobi Transformation 463
  - [ ] FFT 12.2 504
  - [ ] Huffman Coding 903
- [ ] Show top-down approach https://i.sstatic.net/wC9Tb8Y8.png
- [ ] Part metaprogramming (Jinja/Python...)
- [ ] Compilation croisée
- [ ] Threading? SIMD
- [ ] libuv, libevent, libev
- [ ] valdrind, gdb, strace, ltrace
- [ ] Add section for courses with links to the only required stuff.

## Improvements

- [ ] Better separation terms and definitions, acronyms, glossary
- [ ] Include Wikipedia links in addition to `wiki:`
- [ ] Update index
- [ ] Integrate bibliography (extra pages in backmatter)
- [ ] Chapter "Crédits des illustrations" in backmatter
  - [ ] Can I ask chat-gpt/openAI to generate it?
- [ ] Improve syntax for tags/index
- [ ] Make all figures compatible with both light/dark theme
- [ ] Index table entry with many refs cuz ugly line break indent
- [ ] On LaTeX description list, add more space between item and desc.

## Bugs

- [ ] Allow for code inline and markdown inline in table captions
- [ ] Include regular SVG in objects to be automatically adapted to the theme
- [ ] Code with title doesn't display well in LaTeX
- [ ] Image with width should be included with the correct size
- [ ] Implement local links to code, copy them in appencies
- [ ] Table des opérateurs, find a way
- [ ] Table size should be always slighly smaller than the normal text
- [ ] Autres tables, largeur, ajuster au contenu ? tabularx ?
- [ ] Find a way to have "short caption" on figures (maybe use alt text)
- [ ] Label for tables are cropped, should be placed above tables
- [ ] Exercise plugin cause code to be renamed exercise
- [ ] Two/Three columns for exercises ?
- [ ] See solution of exercises without specific type.
- [ ] Multicolumn for exercises (Validité des identificateurs)
- [ ] Exercises numbering (restart at each section)
- [ ] Exercises Colors for fill-in-the-blank in slate theme
- [ ] Mkdocs Material Highlights tags by adding a space after the highlight.
- [ ] Mermaid width too wide
- [ ] Exercise in title Exercice 35 : Exercise : Promotion numérique
- [ ] [Albatros](/assets/src/albatros.txt) ref null
- [ ] Remove preambule… text introductif dans introductions ?
- [ ] Mal géré en LaTeX enumate followed by itemize
- [ ] Size caption of tables and figures is different
- [ ] Carret position in "Opérateurs d'affectation" for XOR

## New Features (MkDocs, plugins)

These features are sorted by priority.

- [ ] Split document in multiple volumes
- [ ] Autoindex of C keywords and functions
- [ ] Reaveal js slides --> see on slides branch
- [ ] Allow to create nav with subsections (build only info1 chapters)
- [ ] Flexible tables parameter for adjusting width, fullwidth
- [ ] Embedded Interactive examples (linked-list)...
- [ ] Anotate code with circled number that can be used in text:
- [ ] Interactive exercices
  - [ ] Code execution
  - [ ] Fill the gap
- [ ] Flexible table

## Fix in mkdocs-material

- [ ] Allow for optional feedback title
- [ ] Translation for permalink title
- [ ] Tags spacing in theme (search) (.md-tag margin-right: 0.5em;)
- [ ] Exercises are all checked
- [ ] Resized tables make them sometime too large (resize but don't enlarge ?)
- [ ] Bug with examples

## Changelog

- [x] Slighly reduce the size of the tables
- [x] Do not enlarge tables in LaTeX, only reduce when too large
- [x] Reduce tables by default
- [x] Add index entries for single inline keywords (printf, ...)

## 0.1.10

#### Content

- [x] Errno, traitement des erreurs
- [x] Redraw ASCII tables in drawio, support for transparency

#### New features

- [x] New feature : add tags anywhere (inline tags) to summary concepts
- [x] Add regexes with `#!re /pattern/replacement/flags`.
- [x] Multiple choice exercises

#### Improvements

- [x] Caption above table
- [x] Remove feedback title : feedback_title: "" as the field is required
- [x] Do not use adjustbox on small tables
- [x] Gray colors for drawio
- [x] Permanent link not translated, now in french

#### Bugs

- [x] Mint inline in titles cause weird behavior in the toc.
- [x] Avoid breaking code block if contains boxchars or special chars
- [x] Exercises style bullet is wrong
- [x] ⇧ 🠔 missing
- [x] Weird position of carret in code in tables
- [x] Author not in title page

### 0.1.9

- [x] LaTeX
  - [x] Generate PDF with LaTeX
  - [x] Only generate LaTeX on build
  - [x] Replace weavydash with 〜 ?
  - [x] Fetch solution to exercises and display them later in document
  - [x] Number exercises with a counter
  - [x] Support unicode chars in LaTeX (Use lualatex?)
  - [x] Auto number tables?
  - [x] \leavevmode only if item is right before code block
- [x] Find a way to add unbreakable space before semi-colon in paragraphs
- [x] Center mermaid diagrams
- [x] Center tables
- [x] Two columns for itemize ?
- [x] Drawio
  - [x] Allow to click on drawio image to see it full screen
  - [x] Drawio and SVG size is not correct
  - [x] Update drawio plugin to use theme colors.
  - [x] Drawio export doesn't accept attributes {width=100%}
  - Fixed by rendering the drawio frontend with a mygraph parser
- [x] When I enable navigation.tabs, I dont see the fold/unfold
  - Fixed by not enabling the navigation.sections
- [x] CI cannot get insiders version of mkdocs.
  - Fixed by adding git config --global url."https://${GH_TOKEN}@github.com/".insteadOf "git@github.com:"
- [x] Tables
  - [x] Rowspan