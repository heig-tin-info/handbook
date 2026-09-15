# Handbook on Zensical + TeXSmith 0.7 — investigation and baseline

Branch `zensical` of `/home/ycr/handbook`, against `/home/ycr/texsmith` branch
`zensical` (0.7.1.dev4, tmark-core 0.1.0), Zensical 0.0.62. Nothing committed.
Logs and artefacts under
`/tmp/claude-1000/-home-ycr-texsmith/cd4a0f77-0da5-48d5-8a5b-d085fc6e155e/scratchpad/`.

## 1. Baseline as-is (TeXSmith 0.2.1, the existing lock)

`TEXSMITH_BUILD=1 uv run mkdocs build` **fails**.

| | |
| --- | --- |
| exit status | 1 (`Aborted with a BuildError!`) |
| wall time | 27.0 s |
| `WARNING` lines | 0 |
| `ERROR` lines | 2 |
| site | written, 142 HTML pages, 108 MB |
| books | **not produced** — no `book.tex`, no `tools.tex`, no PDF |

The site is built; the crash is in `on_post_build`, while rendering the book:

```
mkdocs_plugin_texsmith/plugin.py:665 _render_book
  texsmith/core/conversion/core.py:692 render_with_fallback
    texsmith/adapters/latex/renderer.py:199 render
      texsmith/adapters/plugins/material.py:159 render_epigraph
        bs4 ValueError: Cannot replace one element with another when the
        element to be replaced is not part of a tree
ERROR - LaTeX rendering failed for page 'Programmation'
```

The only artefact is `build/book/pages/course-c-00-preface-index-md.tex`.

**There is no working PDF baseline.** The handbook's two books are already
broken on the released pipeline, so the migration has nothing to regress
against; any PDF the new pipeline produces is a strict improvement.

Kept outside the tree at `scratchpad/handbook-baseline/` (`site/` HTML+JSON+XML
only, 22 MB; `build/`).

## 2. Switch to the local TeXSmith

`pyproject.toml`: `mkdocs-texsmith>=0.7.0` and `texsmith>=0.7.0` (the latter
added as a direct dependency so the source override applies), plus

```toml
[tool.uv.sources]
texsmith = { path = "/home/ycr/texsmith", editable = true }
mkdocs-texsmith = { path = "/home/ycr/texsmith/packages/mkdocs_texsmith", editable = true }
```

`uv lock && uv sync` clean: texsmith 0.7.1.dev4, mkdocs-texsmith 0.7.1.dev4,
`tmark-core` 0.1.0 added, `python-markdown-math` and `unicodeblocks` dropped.

| run | exit | wall | WARNING | ERROR |
| --- | --- | --- | --- | --- |
| `uv run mkdocs build` | 0 | 65.5 s (mkdocs: 57.7 s) | 1249 | 33 |
| `TEXSMITH_BUILD=1 uv run mkdocs build` | 1 | 44.3 s | — | LaTeX |

Both `.tex` bundles are written: `build/book/book.tex` (13.8 KB, 125 pages) and
`build/tools/tools.tex` (9.1 KB). `copy_files` works — `c-logo.pdf`,
`tool-hero.pdf`, `heiglogo.sty`, `titlepage.tex`, `imprint.tex` all land in the
bundles. The PDF step fails (§6).

### (a) Plugin options the current plugin no longer accepts

Exactly one, and it is not fatal:

```
WARNING - Config value 'plugins': Plugin 'texsmith' option 'save_html':
          Unrecognised configuration name: save_html
```

`save_html` has no equivalent: the HTML pipeline is gone, a book is built from
the Markdown source. The inspectable intermediate is now
`build/<folder>/sources/**.md`, written unconditionally.

Everything else the handbook sets is still accepted. Checked against
`site/book.py` (`load_book_settings`, `_read_book`, `BookExtras`) and
`core/config.py` (`BookConfig`):

* plugin level — `build_dir`, `clean_assets`, `template` ✅
* book level — `root`, `title`, `subtitle`, `folder`, `email`, `base_level`,
  `frontmatter`, `backmatter`, `copy_files`, `index_is_foreword`,
  `drop_title_index` ✅ (all fields of `BookConfig`)

Other 0.2.1 options the handbook does not use and that are gone: `parser`,
`embed_fragments` (now `embed_documents`), `register_material`. New options
worth adopting: `declare` (site-wide counters), `web`, `css`,
`inject_markdown_extensions`.

### (b) Hooks

**No hook imports `texsmith`** (`grep -rn texsmith hooks/` is empty), so none of
them fails on a missing API. The breakage is structural and comes in two waves.

Wave 1, already true under MkDocs 0.7: the five `on_page_content` hooks act on
rendered HTML, and the book is no longer rendered from HTML. Whatever they did
for the PDF is silently lost today.

Wave 2, under Zensical: `hooks:` is unsupported, so they do nothing for the site
either.

| hook | what it does for the site | for the PDF (0.2.1) | 0.7 / `texsmith.site` | replacement |
| --- | --- | --- | --- | --- |
| `index.py` | wraps `<code>kw</code>` in `<span class="ycr-hashtag" data-index-entry>` | fed `\index{}` | lost | TMark `#[term]` index entries + `texsmith site search`; or a small Python-Markdown extension |
| `tags.py` | `[[tag]]`/`[[text|tag]]`/`[[t|tag|entry]]` inline processor, plus `search_index.json` injection in `on_post_build` | index entries | **not lost, refused**: TMark reports `compat-unsupported: wiki link [[…]] is not implemented yet` (540 occurrences, 17 files) and leaves them literal | TMark index syntax; the `search_index.json` half is exactly what `texsmith site search` does |
| `spantable.py` | `@span`/`@flex`/`@rb`/`@bb` markers in cells → `rowspan` + CSS classes | rowspans in LaTeX tables | lost; TMark sees the markers as text and reports `ref-unresolved` on `@rb`, `@bb`, `@flex` | TMark table attributes, or drop the feature (1 file uses it) |
| `french.py` | translates untitled admonition titles from `extra.admonition_translations`; thin spaces and « » in HTML; warns on missing ligatures | translated titles reached the PDF | lost | callout titles in the source, or `declare` + template; the typography pass has no TMark equivalent |
| `mermaid.py` | wraps a `%% title` mermaid fence in `<figure><figcaption>` | — | lost | TMark figure caption on the fence |
| `abbr.py` | `*[ABBR]: https://…wikipedia.org/…` renders as `<a class="ycr-abbr">` (73 pages) | glossary | lost | TMark `abbr` + `glossary.wikipedia` feature |

Dead code, **not** in `hooks:` and therefore already inert:
`hooks/book.py` (imports `latex.config` / `latex.renderer`, i.e. `hooks/latex/`,
the in-repo ancestor of TeXSmith), `hooks/drawio.py`, `hooks/latex/**`
(a whole LaTeX renderer with 40 `.tex` templates and `mkbook.cls`).

### (c) Page-level TMark diagnostics

There is no `tmark lint` on the CLI; the diagnostics come from the build and
from `texsmith site build --diagnostics-json`. Totals of one
`uv run mkdocs build` (site pass **plus** the two book passes):

| code | severity | count |
| --- | --- | --- |
| `compat-unsupported` | warning | 540 |
| `deprecated` | warning | 330 |
| `asset-missing` | warning | 183 |
| `frontmatter-yaml` | **error** | 33 |
| `include-missing` | warning | 32 |
| `ref-unresolved` | warning | 25 |
| `attr-no-host` | warning | 24 |
| `var-unresolved` | warning | 8 |
| `asset-convert-failed` | warning | 1 |

A single pass over the corpus (the Zensical run, §4) gives 270
`compat-unsupported`, 168 `deprecated`, 17 `frontmatter-yaml`, 13
`ref-unresolved`, 12 `attr-no-host`.

`deprecated` breaks down as 238 `[](){…}` → `[]{…}`, 68 `--8<-- "file"` in a
fence → `include="file"`, 24 `/// html` → ```` ```html ```` raw fence.

Examples:

* `compat-unsupported` — `course-c/05-introduction/c-lang.md:10:28`,
  `:12:230`, `course-c/15-fundations/syntax.md:…`: wiki link `[[…]]` not
  implemented, stays literal text (this is `hooks/tags.py` syntax).
* `frontmatter-yaml` — `course-c/15-fundations/syntax.md:1:1`,
  `course-c/05-introduction/programming.md:1:1`,
  `course-cpp/cpp.md:1:1`: *invalid front matter: missing field `quote`*.
  The handbook writes `mkdocs-epigraph`'s shape, TMark wants its own:

  ```yaml
  epigraph:          # handbook            epigraph:      # tmark.ir.Epigraph
    text: "…"                                quote: "…"
    source: Einstein                         source: Einstein
  ```

  17 files.
* `asset-missing` — `build/book/sources/course-c/05-introduction/programming.md:22:1`
  image `/assets/images/eniac.jpg` not found; same for `…/pgcd.drawio`,
  `…/bubblesort.drawio`. **All 183 are root-relative paths** (`/assets/…`),
  by extension: 112 `.drawio`, 42 `.png`, 17 `.jpg`, 4 `.webp`, 4 `.gif`,
  2 `.svg`, 2 `.avif`. None is a genuinely missing file — see §6.
* `include-missing` — `build/book/sources/course-c/05-introduction/c-lang.md:293:1`
  `docs/assets/src/hello.c`; `…/15-fundations/stdio.md:105:1` `docs/assets/src/iota.c`.
* `ref-unresolved` — `course-c/15-fundations/operators.md:120:15` `@rb`,
  `:120:35` `@bb`, `:995:57` `@flex`: the `spantable.py` markers read as
  TMark references.
* `attr-no-host` — `course-c/00-preface/index.md:35:1`, `:87:1`, `:123:1`:
  malformed attribute list on the fence (the `/// html` blocks).
* `var-unresolved` — `…/programming.md:553:209` `{{sorties}}`,
  `…/me-and-my-computer.md:188:5` `{{posix}}`, `…/10-numeration/data.md:136:25`
  `{{pair}}`; 8 in total, 3 files, left as written.

### (d) Constructs outside TMark

| construct | census | web (MkDocs 0.7) | web (Zensical) | PDF |
| --- | --- | --- | --- | --- |
| `{{ macro }}` | 8 in 3 files | literal | literal | literal + `var-unresolved` |
| `/// html` block | 3 in `course-c/00-preface/index.md` | rendered by `pymdownx.blocks.html` | same | `attr-no-host` + `deprecated`, content emitted as text |
| `!!! exercise` | 123 blocks | `exercises` plugin numbers them: `<span class="exercise-label">Exercice 1 : </span>` | plain admonition, **no number, no "Exercice"** | TMark callout, no numbering |
| spantables `@span/@flex/@rb/@bb` | 1 file | `spantable.py` builds the rowspans | markers visible as text | markers visible + `ref-unresolved` |
| `.pages` | 32 files | awesome-pages | **ignored** (§5) | ignored (§5) |
| epigraph front matter | 17 files | `epigraph` plugin, 140 pages carry the markup | **absent** | `frontmatter-yaml` error, epigraph dropped |
| wikipedia links / `*[ABBR]: https://…wikipedia.org/…` | 73 pages | `abbr.py` + `wikipedia` plugin | **absent** | absent |
| `[[tag]]` index tags | 540 in 17 files | `tags.py` → `ycr-hashtag` (98 pages) | literal, and Zensical's autorefs warns on each | literal |
| vegalite | **0 uses** | — | — | — |
| markdown-exec python fences | **0 uses** (2 plain ```` ```python ````) | — | — | — |
| drawio | 123 files, 122 referenced | `drawio` plugin | `texsmith site assets` exports SVG, `texsmith.site.web` rewrites `<img>` ✅ | converted to vector PDF ✅ |
| `[text][label]` + `[](){#id}` | 104 anchors, 207 links, 103 of them to an anchor, 30 files | **broken**: left literal | broken, 101 extra "unresolved autoref" | broken, left literal |

Two of the fourteen (vegalite, markdown-exec) are dead configuration and can be
deleted from `mkdocs.yml` outright.

## 3. First Zensical attempt

`cp mkdocs.yml zensical-trial.yml` and **nothing else**:

```console
$ uv run --with zensical zensical build -f zensical-trial.yml
45 issues found
Build finished in 5.75s    (exit 0)
```

No YAML adaptation was needed, contrary to `specs/zensical.md`. Zensical 0.0.62
loads the config with `yaml.Loader` (the full loader), so `!!python/name:` for
the superfences validators and for `pymdownx.emoji` works; it registers its own
`!ENV` constructor, so `docs_dir: !ENV [DOCS, docs]` and the `group` plugin's
`enabled: !ENV CI` parse; and it rewrites `material.extensions` →
`zensical.extensions` on the way in. `theme.custom_dir: overrides`, `hooks:`,
`watch:` and `exclude_docs:` are accepted and ignored. The handbook does not use
`!relative`, and `autorefs.resolve_closest` is a listed ignorable option.

Plugins: **supported natively** — `autorefs`, `tags`, `glightbox`,
`markdown-exec`, `search`. **Silently ignored** — `group`, `caption`,
`awesome-pages`, `epigraph`, `pills`, `texsmith`, `wikipedia`, `drawio`,
`exercises`. (`zensical/config.py:115 _PLUGIN_UNSUPPORTED_OPTIONS` lists
`awesome-nav` but has no entry for `awesome-pages`.)

All 45 issues are `unresolved autoref [[…]]`: Zensical's native autorefs sees
`hooks/tags.py`'s syntax and cannot resolve it.

Site comparison, marker by marker (`grep -rl` over the HTML of each build):

| marker | MkDocs | Zensical |
| --- | --- | --- |
| HTML pages | 142 | 145 |
| `<figcaption>` (caption plugin) | 72 | 36 |
| `ycr-hashtag` (tags hook) | 98 | 0 |
| `ycr-abbr` (abbr hook) | 73 | 0 |
| `epigraph` | 140 | 0 |
| `admonition exercise` | 25 | 25 (unnumbered) |
| `glightbox` | 139 | 64 |

Navigation is alphabetical and untitled: `Advanced`, `Appendix`, `Assets`,
`Course c`, `05 introduction`, `Src`, `Summaries` instead of `Cours C`,
`Introduction`, `Annexes`. Three pages MkDocs kept out of the navigation
(`advanced/`, `assets/summaries/`) become pages of their own. The theme
`overrides/` and Material features (`md-tabs`, `md-header`) are honoured; French
typography, index keywords, the tags page and the exercise numbering are not.

### With `texsmith.site.web`

```console
$ uv run texsmith site assets zensical-trial.yml
0 snippet previews under docs/assets/snippets: 0 rendered.
122 draw.io diagrams under docs/assets/drawio: 115 exported. 0 pruned, 0 failed.
Stylesheet at docs/assets/texsmith/texsmith.css.                  (130.5 s)

$ uv run --with zensical zensical build -f zensical-trial.yml
146 issues found
Build finished in 8.36s     (exit 0)
```

**No crash**, +2.6 s on 142 pages. The extension emits the TeXSmith diagnostics
with page paths (270 `compat-unsupported`, 168 `deprecated`, 17
`frontmatter-yaml`, 13 `ref-unresolved`, 12 `attr-no-host`), lowers every page,
and rewrites the draw.io images to their SVG export:

```html
<img src="../../../assets/drawio/assets/images/gtk-stack.svg">
```

Two defects found on this corpus, both on the TeXSmith side:

1. **glightbox `href` is not rewritten.** The `<img src>` becomes the SVG but
   the anchor Zensical's glightbox wraps it in still points at the diagram:
   `<a class="glightbox" href="/assets/images/program.drawio"><img src="…/program.svg"></a>`.
   Clicking a figure downloads a `.drawio` file.
2. **+101 `unresolved autoref`** (45 → 146). `[](){#opengl-coordinates}` is
   lowered to `<span id="opengl-coordinates"></span>`, which is raw HTML and
   therefore invisible to autorefs' tree scanner, and `[Plus haut][opengl-coordinates]`
   survives as literal text in the page. Verified identical under
   **MkDocs** with the same TeXSmith — it is not a Zensical problem:

   ```
   <p>[Plus haut][opengl-coordinates], nous avions défini…</p>
   ```

`texsmith site search` was not exercised (the corpus declares no `#[term]`
entries yet; it becomes relevant once `hooks/index.py` and `hooks/tags.py` are
migrated).

## 4. Navigation: `.pages` vs `.nav.yml`

32 `.pages` files. Keys actually used, in full:

| key | files | awesome-nav equivalent |
| --- | --- | --- |
| `title` | 29 | `title`, identical |
| `nav` | 20 | `nav`, identical |
| `arrange` | 2 (`docs/tools`, `docs/appendix`) | `nav` — an **exact alias**: `mkdocs_awesome_pages_plugin/meta.py:137` does `if nav is None and arrange is not None: nav = [...]` |
| `titles` | 1 (`docs/tools/analysis/.pages`) | a typo for `title`, currently silently ignored |
| `hide` | 1 (`docs/assets`) | `hide`, identical |

No `collapse`, no `order`, no `sort_type`, no `...` rest marker, no
`ignore_no_matches`, no inline `Title: [items]` groups. Item values are plain
strings plus one `Title: path` mapping
(`docs/course-c/10-numeration/.pages`: `- L'information: data.md`), which both
plugins spell the same way.

**The handbook should convert to `.nav.yml`, not TeXSmith teach `.pages`.**
Zensical implements awesome-nav natively and ignores awesome-pages, so a
`.pages`-reading resolver in TeXSmith would fix the PDF and leave the site's
navigation wrong. The conversion is mechanical — `arrange` → `nav`,
`titles` → `title`, rename the file — and I ran it as a check:

```python
data = yaml.safe_load(p.read_text()) or {}
if "arrange" in data and "nav" not in data: data["nav"] = data.pop("arrange")
if "titles" in data and "title" not in data: data["title"] = data.pop("titles")
p.with_name(".nav.yml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
```

Before (`texsmith.site.nav.resolve_navigation(Path("docs"))`), the resolver falls
back to MkDocs' default navigation: sections named `Tools`, `Course c`,
`Analysis`, `C cpp`, alphabetical, 142 pages, and

```
$ uv run texsmith site build mkdocs.yml --book "Outils de développement"
error: Root section 'Cours C' not found in navigation.        (1.1 s, exit 1)
```

After: `index.md`, `Cours C`, `Cours C++`, `Concurrence`, `Outils`, `Annexes`;
125 pages in navigation, 17 unlisted; and

```
$ uv run texsmith site build mkdocs.yml --book "Outils de développement" --no-pdf
Outils de développement: …/tools/tools.tex     (3.6 s, exit 0, 7 diagnostics)
```

The 32 `.nav.yml` are left in the working tree, untracked, beside the `.pages`.
The two sets are consistent duplicates; keep both until MkDocs is retired.

## 5. The books

### What the current builder already does

`BookConfig` has a field for every key the handbook uses — `root`, `title`,
`subtitle`, `author`, `year`, `email`, `folder`, `frontmatter`, `backmatter`,
`base_level`, `copy_files`, `index_is_foreword`, `drop_title_index`, `cover` —
and `_copy_extra_files` honours `copy_files`, globs included. Both `.tex`
bundles are written with all five override files in place. So the *option*
surface is not the crux; the crux is that nothing includes the overrides and
that LaTeX refuses the result.

### Gap 1: nothing consumes `tex/titlepage.tex`, `tex/imprint.tex`, `tex/heiglogo.sty`

`copy_files` copies them into `build/book/` but `book.tex` never `\input`s or
`\usepackage`s them: `\maketitle` uses the template's own title page and the
imprint comes from the `imprint_thanks` / `imprint_license` /
`imprint_copyright` Markdown attributes. `src/texsmith/templates/book/template/manifest.toml`
offers slots `frontmatter`, `dedication`, `mainmatter`, `preface`, `backmatter`,
`appendix`, `colophon` — all content slots, none a preamble or a cover hook —
and `extra_packages` is computed from the fragments, not author-settable.

Two ways out: scaffold a `handbook` template
(`texsmith --template-scaffold`, then `template: handbook`) whose
`template.tex` inputs those files; or TeXSmith grows a `preamble` /
`titlepage` / `imprint` file-valued attribute. The first needs no TeXSmith
change and is the smaller step.

### Gap 2: the `book` template does not compile in French

Minimal reproduction, nine lines, no handbook content:

```yaml
---
title: Essai
press:
  template: book
  language: fr
---
# Chapitre
Bonjour le monde.
```

```console
$ uv run texsmith doc.md --build
error: book.tex:248: Missing number, treated as zero
```

The same document with `language: en` produces a PDF. The trace:

```
\__hook begindocument … \computemaxpartnumberwidth
  \@settodim  {\cftpartfont \cftpartpresnum \int_to_Roman:n {1}}
    \cftpartpresnum -> \partname~
      \FB@partname … \value{part} … \partnameord
        \ordinal -> \form@tnumber -> \numdigits -> \setcounter{workm@mctr}{#1}
          \calc@assign@generic … (#4!      ← "!" where a number is expected
```

`src/texsmith/templates/book/template/fixtoc.sty` measures the part-number
column at `\AtBeginDocument` with `\settowidth`, expanding `\cftpartpresnum`;
under `babel-french` that is `\partname` → `\FB@partname`, which formats an
ordinal through `calc` and needs a `part` counter that does not exist yet.
**This is the single blocker for both handbook PDFs**, and it blocks every
French book TeXSmith produces.

### Gap 3: four content-triggered LaTeX failures behind it

Neutralising `\cftpartpresnum` inside the `AtBeginDocument` hook lets `book.tex`
run into the pages. Compiling with `tectonic -Z continue-on-errors` gives at
least **114 errors** before the run wedges on `stdio.md`:

| errors | message | cause |
| --- | --- | --- |
| 104 | `Extra alignment tab has been changed to \cr` | a `|` inside a code span in a table row |
| 2 | `Something's wrong--perhaps a missing \item` | idem |
| 2 | `Extra \endgroup` | idem |
| 1 | `Missing \endcsname inserted` | `\tskeys{Alt,\(\leftarrow\)}` |
| 1 each | `\begin{document} ended by \end{tscode}` / `\end{Verbatim}`, `Paragraph ended before \environment tscode was complete`, `Illegal unit of measure` | fallout |

The table bug is precise. Source
(`docs/course-c/15-fundations/operators.md:442`):

```
| `         | `                                | [Disjonction (OU)][operator-or] | `(0b1101 | 0b1010) == 0b1111` |
```

TMark splits the row on every `|`, code spans included, and emits four cells
into a three-column `tabularx`, leaving the backticks unconverted:

```latex
` & ` & [Disjonction (OU)][operator-or] & `(0b1101 & 0b1010) == 0b1111` \\
```

Python-Markdown's `tables` extension honours the code span, which is why the
site is fine. **337 such rows in 13 files**, worst offenders
`course-c/35-libraries/standard-library.md` (145),
`course-c/15-fundations/stdio.md` (50), `operators.md` (32),
`tools/arch/filesystem.md` (28).

The keystroke bug: `\tskeys{Alt,\(\leftarrow\)}` builds `\csname ts@key@\(…`
and dies on `Missing \endcsname` — `ts_key:n` assumes a csname-safe key name.

### Gap 4: root-relative image paths

Every one of the 183 `asset-missing` is a `/assets/…` path. The book builder
resolves an image against the persisted source
(`build/<folder>/sources/<page>.md`) and treats `/assets/…` as
filesystem-absolute. `texsmith/site/assets.py:145` already does the right thing
for the same corpus (`if clean.startswith("/"): target = clean.lstrip("/")`,
resolved under `docs_dir`) — which is how `texsmith site assets` found and
exported 122 of 123 draw.io diagrams. The book path needs the same rule, i.e.
MkDocs' `validation.absolute_links: relative_to_docs`.

### Gap 5: `--8<--` includes

32 `include-missing` for `docs/assets/src/*.c`.
`snippet_base_paths_from_extensions` returns `[]` when
`pymdownx.snippets` declares no `base_path` (the handbook declares
`check_paths`, `url_max_size`, `url_timeout`, `auto_append` only), so the
include resolves against the source directory. Setting `base_path: .` in
`mkdocs.yml` is the cheap fix on the handbook side and is what
`docs/guide/mkdocs.md` asks for anyway; defaulting to the project directory
when the option is absent is the fix on the TeXSmith side.

## 6. Plan

### TeXSmith must add or fix

| # | work package | where | size | unblocks |
| --- | --- | --- | --- | --- |
| T1 | `fixtoc.sty`: measure the part/chapter/section number widths without expanding `\cftpartpresnum` (or expand it in a group with `\partname` neutralised), so the `book` template compiles under `babel-french`. Add a French book to the parity corpus. | `src/texsmith/templates/book/template/fixtoc.sty` | **S** | every French PDF, including both handbook books |
| T2 | Table rows: honour code spans (and `\|`) when splitting a GFM row. | `tmark` core parser | **M** | 104+ LaTeX errors, 337 rows, 13 files |
| T3 | Book builder: resolve root-relative image paths against `docs_dir`, reusing the rule at `site/assets.py:145`. | `src/texsmith/site/book.py` | **S** | 183 `asset-missing`, all figures of the C book |
| T4 | `[text][label]` reference links pointing at a TMark label: resolve them to a real cross-reference in both writers, and register the lowered anchor where autorefs can see it (a real `<a id>` element, not a stashed raw-HTML span). | `tmark` + `site/web.py` | **M** | 207 links / 104 anchors, broken today on MkDocs, Zensical **and** the PDF |
| T5 | `texsmith.site.web`: rewrite the enclosing `<a href>` as well as `<img src>` when redirecting a `.drawio` to its export. | `src/texsmith/site/web.py` | **S** | glightbox on 64 pages |
| T6 | `\tskeys` / `ts_key:n`: accept a key name that is not csname-safe. | `ts-keystrokes` fragment | **S** | `++alt+←++` and friends |
| T7 | `snippet_base_paths_from_extensions`: default to the project directory when `pymdownx.snippets` declares no `base_path`. | `src/texsmith/site/config.py:173` | **S** | 32 `include-missing` |
| T8 | Book template: an author-settable preamble / title-page / imprint hook (file-valued attribute or a `preamble` slot), so `copy_files` overrides are actually reachable. | `templates/book`, `core/templates` | **M** | the handbook's HEIG-VD cover without forking the template |
| T9 | `save_html`: document its removal in `docs/guide/migration.md` and keep the warning. | docs | **S** | migration clarity |
| T10 | Record in `specs/zensical.md` that Zensical 0.0.62 needs **no** config adaptation (full `yaml.Loader`, `!ENV` constructor, `material.extensions` remap); the three adaptations listed there are stale. | `specs/zensical.md` | **S** | accuracy |

T1 first, alone, is what turns "no PDF" into "a PDF with bad tables". T1 + T2 +
T3 is the minimum for a readable book.

### The handbook must migrate

| # | work package | where | size | unblocks |
| --- | --- | --- | --- | --- |
| H1 | Convert the 32 `.pages` to `.nav.yml` (`arrange` → `nav`, `titles` → `title`), keep both until MkDocs is retired. **Done in this branch, untracked.** | `docs/**/.nav.yml` | **S** | `texsmith site build` at all; Zensical navigation |
| H2 | `epigraph: {text:}` → `epigraph: {quote:}` in 17 files; drop the `epigraph` plugin. | `docs/**/*.md`, `mkdocs.yml` | **S** | 33 `frontmatter-yaml` errors; epigraphs in the PDF and on Zensical |
| H3 | Escape the pipes: `` `|` `` → `` `\|` `` in 337 table rows / 13 files (or wait for T2 and leave the source as it is — T2 makes H3 unnecessary). | `docs/**/*.md` | **M** | 104 LaTeX errors |
| H4 | Run the deprecation fixes: 238 `[](){#id}` → `[]{#id}`, 68 `--8<--`-in-fence → `include="…"`, 24 `/// html` → ```` ```html ```` raw fences. | `docs/**/*.md` | **M** | 330 `deprecated`, 24 `attr-no-host` |
| H5 | Migrate `hooks/tags.py`'s `[[tag]]` (540 uses, 17 files) to TMark index entries, then wire `texsmith site search` into the Zensical build. Retire `hooks/index.py` the same way. | `docs/`, `Makefile` | **L** | 540 `compat-unsupported`; the index of both books; site search parity |
| H6 | Replace `hooks/abbr.py` + the `wikipedia` plugin with TMark `abbr` / `glossary.wikipedia` (73 pages). | `docs/`, `includes/abbreviations.md` | **M** | abbreviations on Zensical and in the PDF |
| H7 | Decide the fate of `!!! exercise` numbering (123 blocks): TMark counters via `plugins.texsmith.declare.counters`, or keep the `exercises` plugin and accept unnumbered exercises on Zensical. | `docs/`, `mkdocs.yml` | **M** | exercise numbering parity |
| H8 | Retire `hooks/spantable.py` (1 file), `hooks/french.py` (fold the admonition titles into the sources), `hooks/mermaid.py` (caption on the fence). | `hooks/`, `docs/` | **M** | 25 `ref-unresolved`; hookless build |
| H9 | Either scaffold a `handbook` book template that inputs `tex/titlepage.tex`, `tex/imprint.tex` and `heiglogo.sty`, or wait for T8. | `templates/handbook/`, `mkdocs.yml` | **M** | the HEIG-VD cover |
| H10 | Housekeeping: delete `save_html`, the `vegalite` custom fence (0 uses) and the `python`/markdown-exec fence (0 uses) from `mkdocs.yml`; add `pymdownx.snippets.base_path: .`; gitignore `docs/assets/drawio/`, `docs/assets/snippets/`, `docs/assets/texsmith/`; delete the dead `hooks/book.py`, `hooks/drawio.py`, `hooks/latex/`. | `mkdocs.yml`, `.gitignore`, `hooks/` | **S** | a clean config; no `save_html` warning |
| H11 | A `Makefile` target chaining `texsmith site assets` → `zensical build` → `texsmith site search` → `texsmith site build`, and a CI job running it non-blocking. | `Makefile`, CI | **S** | the two-command Zensical workflow becomes one |

### Suggested order

1. **T1** (unblocks any PDF at all), then **H1** + **H2** + **H10** (a morning's
   work on the handbook, no TeXSmith dependency).
2. **T2**, **T3**, **T6**, **T7** — after these, `texsmith site build` should
   produce two compiling PDFs; measure again.
3. **T4** + **T5**, then **H4** — the web and the PDF stop losing
   cross-references and diagram links.
4. **H5** … **H9** and **T8** — feature parity; the long tail.
5. **T9**, **T10**, **H11** — documentation and workflow.

## 7. Working-tree state of this branch

Modified: `pyproject.toml` (dependency bump + `[tool.uv.sources]`), `uv.lock`.
Untracked: this file, `zensical-trial.yml` (the trial copy of `mkdocs.yml` with
`texsmith.site.web` and the stylesheet added), 32 `docs/**/.nav.yml`,
`docs/assets/drawio/` (115 SVG exports), `docs/assets/texsmith/texsmith.css`,
`docs/assets/snippets/` (empty). The last three are generated and belong in
`.gitignore` (H10).
