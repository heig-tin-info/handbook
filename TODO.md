# TO-DO And Bugs

## To-Do

- [ ] Content
  - [ ] Sécurité et bonnes pratiques (buffer overflow, vunérabilités, strcpy, gets, ... libfuzzer
  - [ ] Insérer un exemple de diagramme à la main https://i.sstatic.net/WdbInYwX.png
  - [ ] Ajouter des algorithmes de Numeriacl Recipes
    - [ ] Gauss Jordan 36
    - [ ] QR Decomposition 108
    - [ ] Chebyshev Approximation 190
    - [ ] Padé Appromants 200
    - [ ] Jacobi Transformation 463
    - [ ] FFT 12.2 504
    - [ ] Huffman Coding 903
  - [ ] Montrer un exemple top-down https://i.sstatic.net/wC9Tb8Y8.png
  - [ ]
  - [ ] Métaprogrammation avec Jinja/Python...
  - [ ] Errno, traitement des erreurs
  - [ ] Compilation croisée
  - [ ] Threading? SIMD
  - [ ] libuv, libevent, libev
  - [ ] valdrind, gdb, strace, ltrace
- [ ] Termes et définitions
  - [ ] Glossaire
  - [ ] Acronymes
- [ ] Index
- [ ] Crédits des illustrations
- [ ] Summary Wikipedia
- [ ] Bibliographie

- [ ] LaTeX
  - [x] Mint inline in titles cause weird behavior in the toc.
  - [x] Avoid breaking code block if contains boxchars or special chars (ascii art?)
  - [x] Do not use adjustbox on small tables
  - [ ] Code with title doesn't display well in LaTeX
  - [ ] Image with width should be included with the correct size
  - [ ] Implement local links to code, copy them in appencies
  - [ ] Table des opérateurs, find a way
  - [ ] Autres tables, largeur, ajuster au contenu ? tabularx ?
  - [ ] Find a way to have "short caption" on figures (maybe use alt text)
- [ ] Add tags anywhere (inline tags) to summary concepts
- [ ] Build another nav with only the required sections for INFO1, INFO2.
- [ ] Label for tables are cropped, should be placed above tables
- [ ] Exercise plugin cause code to be renamed exercise
- [ ] Make all figures compatible with both light/dark theme
- [ ] Tables
  - [x] Caption above table
  - [ ] Addfull parameter for adjusting width, fullwidth
- [ ] Slides for each course with inteactive examples
- [ ] Embedded Interactive examples (linked-list)...
- [ ] Interactive exercices
  - [ ] Multiple choice
  - [ ] Code execution
  - [ ] Fill the gap
- [ ] Two/Three columns for exercises ?
- [ ] Exercises style bullet is wrong



### Custom extensions

- [ ] Flexible table
  - [ ] Full Width
  - [ ] X column


## Bugs

- [ ] See solution of exercises without specific type.
- [ ] Gray colors for drawio. Use a smart way to convert gray in slate/default theme.
- [ ] Multicolumn for exercises (Validité des identificateurs)
- [ ] Exercise numbering (restart at each section)
- [ ] Colors for fill-in-the-blank in slate theme
- [ ] Mkdocs Material Highlights tags by adding a space after the highlight.
- [x] Add regexes with `#!re /pattern/replacement/flags`.
- [x] ⇧ 🠔 missing
- [ ] Mermaid width too wide
- [ ] Exercise in title Exercice 35 : Exercise : Promotion numérique
- [ ] Tentez de récupérer vous même le poème l'[Albatros](/assets/src/albatros.txt) ref null -> use web page from site, add link
- [ ] Weird position of ^ : | `^=`                 | Affectation par XOR             | `x ^= y`                 | `x = x ^ y`                 |

- [x] Author not in title page
- [ ] array.drawio p 252
- [ ] remove preambule… text introductif dans introductions ?
- [ ] Table un peu plus petite par défaut
- [ ] Mal géré en LaTeX enumate followed by itemize
- [x] Permanent link not translated : add config/markdown_extension/toc/permalink_title to translate
- [x] Remove feedback title : feedback_title: "" as the field is required
- [ ] Size caption of tables and figures is different

## Fix in mkdocs-material

- [ ] Allow for optional feedback title
- [ ] Translation for permalink title
- [ ] Tags spacing in theme (search) (.md-tag margin-right: 0.5em;)
- [ ] Exercises are all checked
- [ ] Resized tables make them sometime too large (resize but don't enlarge ?)
- [ ] Bug with examples
    ```latex
    \begin{enumerate}
    \item


    %\leavevmode % Required to avoid a bug in the tcolorbox package
    \begin{code}{c}{}{}
    unsigned short i = 32767;
    i++;
    \end{code}

    \item


    %\leavevmode % Required to avoid a bug in the tcolorbox package
    \begin{code}{c}{}{}
    short i = 32767;
    i++;
    \end{code}

    \item


    %\leavevmode % Required to avoid a bug in the tcolorbox package
    \begin{code}{c}{}{}
    short i = 0;
    i = i--;
    i = --i;
    i = i--;
    \end{code}


    \end{enumerate}
    ```

## Missing features

- [ ] Anotate code with circled number that can be used in text:

```c
int x = 42; // ((1))
```

Dans l'extrait de code ci-dessus, on constate ((1)) que la variable `x` est initialisée à 42.

Remplacement avec les circled numbers ①

## Changelog

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