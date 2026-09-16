# TO-DO And Bugs

## Zensical migration (2026-09-16)

Everything below this section predates the migration and a good part of it is
stale: it was written against MkDocs, Material and the plugin hooks, so the
exercise numbering, the figure captions and the checkbox bugs it lists are
TMark's business now, and "Fix in mkdocs-material" has no addressee any more.
What the move to Zensical + TeXSmith leaves open is here; `NOTES-zensical.md`
§§8–12 holds the evidence behind each item.

### Content

- [ ] Quizzes: the 129 `- [x]` lines of 11 files are plain checkboxes now, nothing checks an answer. TMark has no equivalent of what the `exercises` plugin built — either they become prose (a solution callout with the answer), or something has to render them. (`docs/`)
- [ ] Fill-in-the-blanks: 13 `{{word}}` markers in 3 files (8 `var-unresolved`), dead markup on both media. Same choice as the quizzes. (`docs/course-c/`)
- [ ] Exercise numbering is continuous site-wide (the `ex` counter of `plugins.texsmith.declare.counters`); the `exercises` plugin restarted it on every page. Decide whether per-page or per-section numbering is worth a counter scope. (`mkdocs.yml`, TeXSmith)
- [ ] Four abbreviations never reach the glossary: `EOF`, `FLOPS`, `SVG` and `W3C` are absent from `ts-glossary.sty` and `UTF-8` lands under the key `UTF8`, while the other forty are fine. Cause unknown. (`includes/abbreviations.md`, TeXSmith)
- [ ] `@Ry` in `docs/course-c/25-architecture-and-systems/cpu-zero.md` — a subscript in a formula the reference resolver reads as a counter reference, and the one warning the Zensical build still has. Either the formula or the resolver. (`docs/`, tmark)
- [ ] The `pie` mermaid fence of `docs/course-c/05-introduction/me-and-my-computer.md` is `asset-convert-failed` since the baseline. (TeXSmith asset conversion)
- [ ] `docs/tools/.nav.yml`'s `- "*"` matches nothing and both nav resolvers say so; it is the faithful conversion of the old `.pages` and was never cleaned up.

### Web rendering under Zensical

- [ ] A plain `![alt](img)` gets no numbered `Figure N` caption: `mkdocs-caption` was a plugin hook and Zensical has none. Only the web loses this — the PDF numbers its own figures. Either the images are marked up as TMark figures, or bare `<img>` is accepted. (`docs/`, TeXSmith)
- [ ] Markdown inside a rewritten callout title does not render: the title is emitted as `<p class="admonition-title">` with no `markdown` attribute, so a code span or an emphasis written in a title stays literal. (tmark web lowering)
- [ ] Nothing replaces `hooks/french.py`'s web typography: the thin spaces before `;:!?`, the `«…»` and the missing-ligature lint (`coeur` → `cœur`) are lost. `babel-french` still does it in the PDF. (TeXSmith, or a Zensical-side pass)
- [ ] The operator-priority table repeats its priority and associativity on every row instead of spanning them: `lower_web` mangles a code span inside a `yaml table` cell, and that table is made of `` `++` ``, `` `()` ``, `` `sizeof` ``. (tmark web lowering)

### The books

- [ ] Box-drawing glyphs in code blocks (`─ │ ┴`) have no coverage in the monospace font: ~7800 "Missing character" lines in the C book log. Pick a mono font covering U+2500…U+257F, or drop the glyphs from the listings. (TeXSmith fonts, `docs/`)

### Build, CI and dependencies

- [ ] Nothing in CI runs `make zensical`: `.github/workflows/ci.yml` still publishes with `uv run mkdocs gh-deploy --force`. Add a non-blocking `make zensical` job first, then switch the publish step — that switch is what decides when the MkDocs-only plugins can go.
- [ ] Decide what replaces `mike` before the CI switch, not after: Zensical has no versioning equivalent, `mike>=2.1.3` is still a dependency with its plugin commented out in `mkdocs.yml`, and nothing versions the site today. Either `mike` leaves `pyproject.toml`, or the versioning is done by another mechanism.
- [ ] Replace the `tmark-core` path override committed on this branch (`tmark-core = { path = "/home/ycr/tmark/crates/tmark-py" }` in `pyproject.toml`, with its `uv.lock`) by a released `tmark-core` carrying the core fixes this migration used: the site-wide declarations, the unresolved `include=` drop, the unescaped label names, the localised callout words, the front-matter epigraph. The two editable TeXSmith paths go the same way when 0.7.1 is released.
- [ ] Drop `mkdocs-autorefs`: it was the only thing resolving `[text][id]`, the corpus is written `[text](#id)` now, and TMark's lowering points a cross-page reference at the page holding the label on both generators. (`mkdocs.yml`, `pyproject.toml`)
- [ ] Drop `mkdocs-plugin-exercises` and `mkdocs-wikipedia` once CI stops running MkDocs: TMark numbers the exercises now, and the article summaries are the only thing `wikipedia` still adds. (`pyproject.toml`, `mkdocs.yml`)

### Zensical upstream

- [ ] Zensical's anchor check reads the source, not the lowered page: the 47 cross-page `[text](#id)` references of the corpus are each reported `anchor does not exist` although the built link is correct (`../datatype/#unicode`), because TMark splices the sibling's page into the link after that check has run. Ask upstream for a check that runs on what is rendered, or for a way to declare the site's anchors. (`zensical build`, TeXSmith hook order)
- [ ] Zensical ignores `exclude_docs`, so the include sources under `docs/` are built as orphan pages, reachable by URL though listed nowhere; their `search: {exclude: true}` front matter keeps them out of the index only. Ask upstream for `exclude_docs`, or move those sources out of `docs/`.
- [ ] `tags_allowed` is the knob if the 252 tags of the Filters facet ever prove too many: it restricts the facet to a declared list and warns on anything else. (`mkdocs.yml`)

## Content update

- [ ] Hand drawn flow diagram `https://i.sstatic.net/WdbInYwX.png`
- [ ] Show top-down approach `https://i.sstatic.net/wC9Tb8Y8.png`
- [ ] Part metaprogramming (Jinja/Python...)
- [ ] Compilation croisée
- [ ] Threading? SIMD
- [ ] Add section for courses with links to the only required stuff.

## Improvements

- [ ] Wrap table columns with syntax such as `>>>` or better a `yaml` table extension.
- [ ] Find a way to add crop cut on PDF as we don't use A4 format
- [ ] Improve deployment on gh-pages, reduce the number of changes
- [ ] Better separation terms and definitions, acronyms, glossary
- [ ] Integrate bibliography (extra pages in backmatter)
- [ ] Chapter "Crédits des illustrations" in backmatter (ai generated?)
- [ ] Improve syntax for tags/index
- [ ] Make all figures compatible with both light/dark theme
  - [ ] Adapt SVG color when added in object
- [ ] Index table entry with many refs cuz ugly line break indent

## Bugs

- [ ] Badge shows falling on README
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
