# Bugs

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

## Missing features

- [ ] Anotate code with circled number that can be used in text:

```c
int x = 42; // ((1))
```

Dans l'extrait de code ci-dessus, on constate ((1)) que la variable `x` est initialisée à 42.

Remplacement avec les circled numbers ①