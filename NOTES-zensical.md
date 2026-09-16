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

## 8. Wave 2 — the hooks leave (H5 … H9)

Branch `zensical`, on top of wave 1 (H1–H4, H10, H11). TeXSmith 0.7.1.dev5 of
`/home/ycr/texsmith` branch `zensical`, `tmark-core` 0.1.0, Zensical 0.0.62.

### What was done

| # | package | result |
| --- | --- | --- |
| H5 | `[[tag]]` → `#[term]` | **done**: 275 markers, 17 files, `utils/migrate_wiki_tags.py`; `hooks/tags.py` and `hooks/index.py` retired |
| H6 | `hooks/abbr.py` | **done**: 44 abbreviations carry their expansion; hook retired, `wikipedia` plugin kept for MkDocs |
| H7 | exercise numbering | **not applied**: two TeXSmith defects block it, the migration is committed unapplied as `utils/number_exercises.py` |
| H8 | `spantable` / `french` / `mermaid` | **done**: all three retired, `hooks/` deleted |
| H9 | the HEIG-VD cover | **done**: `press.titlepage` / `press.imprint` / `press.preamble` reach `tex/` from `mkdocs.yml` |
| (H4) | `--8<--` in a fence | **tried and reverted**: `include=` is spliced on the web now, but its path is not resolved the way the snippet extension resolves one |

`hooks:` is gone from `mkdocs.yml` and the `hooks/` directory with it.

### H5 — index entries

`hooks/tags.py` read four shapes, all of them a visible text plus an index
entry: `[[Zig]]`, `[[||void]]`, `[[|heraldique]]`, `[[Mayenne|Mayenne, Duc de]]`,
`[[Shadocks||Shadocks, les]]`, `[[bit|bit|bit, le]]`. The entry is the **last
non-empty field**, the visible text the first one — the hook's own rule (the
middle field kebab-cased into a `data-tag` for Lunr) disappears with it, since
`texsmith site search` keys the entry itself.

`utils/migrate_wiki_tags.py` (idempotent, `--check`) rewrites them to
`text #[term]`, or `#[term]` alone when nothing was visible: a TMark index
entry is **zero-width**, so the visible half has to be written out as ordinary
text. It skips fenced blocks and code spans, as the hook's inline processor
did. 275 markers, 17 files, distribution 142 `[[text]]`, 119 `[[||entry]]`,
6 `[[|tag]]`, 3 `[[text||entry]]`, 2+2 three-field, 1 `[[text|tag]]`.

`hooks/index.py` is **dropped, not migrated**: it wrapped every inline
`<code>` of three to fifteen characters in an index entry — an automatic index
of thousands of terms. The C keywords it mostly caught (`#[void]`, `#[while]`,
…) are already explicit entries in `syntax.md`, coming from the `[[||…]]` form.

Numbers: `compat-unsupported` 540 → **0**; Zensical's 45 `unresolved autoref`
→ **0**; `texsmith site search` reports **74 search entries gained the index
entries of their page** (it reported nothing before, the corpus declaring
none); the C book's `.tex` carries **270 `\tsindex{}`** calls and a
`\printindex`.

### H6 — abbreviations

`*[KEY]: https://…wikipedia.org/…` is not what `abbr` means anywhere but in
this repository: TMark reads the same definitions PHP-Markdown-Extra does and
gives them to `<abbr title>` on the web and to `glossaries` in the PDF. The 44
entries of `includes/abbreviations.md` therefore carry their **expansion**
(`*[POSIX]: Portable Operating System Interface`), which is what a reader
hovering an acronym wants; the click-through to the article is gone, and the
`wikipedia` plugin still decorates the article links written in the prose —
under MkDocs only, Zensical has no plugin hooks.

`K&R` left the list, see the lesson below.

**The acronym list does not reach the PDF**, and did not before either:
TeXSmith does not honour `pymdownx.snippets`' `auto_append`, so the file the
site appends to every page is invisible to the book builder
(`build/book/sources/**.md` has never contained it). Verified: an explicit
`{include}(includes/abbreviations.md)` on one page puts all 44
`\newacronym` in the preamble but substitutes `\tsacr{}` on that page only,
and `glossaries` prints only the entries that were used.

### H7 — exercise numbering: what is missing

TMark numbers a callout through a counter item in its title, declared
site-wide under `plugins.texsmith.declare.counters`:

```yaml
ex: {name: Exercice, format: "Exercice {n}", scope: document}
```

`::: exercise {title="#(ex:mot-du-jour) : Mot du jour"}` renders
`Exercice 12 : Mot du jour` in both writers — verified on a standalone
document, web lowering and LaTeX. **Neither spelling survives the site path**:

1. `texsmith.site.index` parses a page's **body** and attaches a front-matter
   node afterwards (`SiteIndex.register` and `.lower`: `tmark.parse(padded)`
   where `padded` is the body, then `doc["front_matter"] = node`). The parser
   therefore never sees the page's own declarations, and
   `press.declare.admonitions` is invisible to it: `::: exercise` raises
   `container-unknown` and the lowering leaves the fence as **literal text on
   the page**. `tmark.parse` takes no declarations, so the fix is to parse the
   whole page text, or to re-parse once the site declarations are merged in.
   (The same page parsed whole — `tmark.parse(open(page).read())` — has no
   diagnostic and renders correctly.)
2. The `!!!` spelling needs no declaration, the PyMdownX profile taking any
   word as a callout kind, but it cannot carry the counter:
   `tmark.lower_web` splices a `#(ex:key)` written in a `!!!` title at the
   **start of the line** instead of at the marker, so
   `!!! exercise "#(ex:un) : T"` lowers to
   `<span class="ts-counter">Exercice 1</span>cise "#(ex:un) : T"`. The
   offsets of a node inside a `!!!` title look relative to the title rather
   than to the file.

Either one fixed is enough. `utils/number_exercises.py` is the finished
migration for (1) — 123 blocks, 25 files, the de-indentation and the
front-matter declaration included — committed **unapplied**: it reports by
default and writes only with `--apply`.

Also lost with the `exercises` plugin under Zensical, and not replaceable by
TMark: the multiple-choice quizzes it built from a `- [x]` list and the
fill-in-the-blank inputs it built from `{{word}}` (8 left in 3 files, reported
as `var-unresolved`). Numbering was **per page** there; the TMark counter is
continuous site-wide.

### H8 — the last three hooks

**`spantable.py`.** The operator-priority table repeats its priority and
associativity on every row instead of spanning them, and a `yaml table-config`
fence gives the description column the flexible width `@flex` asked for
(`clXl` in LaTeX). TMark's `yaml table` *can* express the row spans
(`{value: …, rows: 2}` with `~` below), but its **web lowering mangles a code
span inside a YAML cell** — `["`code`", "x"]` renders as ` ```yam ` — and that
table is made of `` `++` ``, `` `()` ``, `` `sizeof` ``. The `@rb` / `@bb`
markers of the addition table are dropped: CSS borders with no print meaning.
The dead rules go too, the global `white-space: nowrap` on every table cell
that hid behind `td:not(.ycr-flex-column)` included. 24 of the 25
`ref-unresolved` are gone with them.

**`french.py`.** Nothing localises a callout's default title: the LaTeX word
list (`ts_callout_words`) is the capitalised kind or tmark's English label
whatever `language:` says, and a declared kind's `name:` does not reach it
either — a declared `exercise: {name: Exercice}` still prints `Exercise`. The
eighteen untitled callouts of the four translated kinds (`tip`, `warning`,
`example`, `bug`) therefore carry their French title in the source, and
`extra.admonition_translations` is gone from `mkdocs.yml`. The typography pass
has **no equivalent**: `babel-french` spaces `;:!?` in the PDF, the web loses
the thin spaces and the `«…»`, and the ligature lint (`coeur` → `cœur`) with
them. `docs/css/french.css` is untouched — it styles the dash lists, not the
hook.

**`mermaid.py`.** The six fences whose first line was a `%% title` carry a
`Figure:` caption line after the fence instead, which is a numbered figure on
both media (`<figure><pre class="mermaid">…<figcaption>` on the web, a float in
the PDF).

### H9 — the cover

`press.titlepage`, `press.imprint` and `press.preamble` landed on the TeXSmith
side during this wave, so `mkdocs.yml` reaches `tex/titlepage.tex`,
`tex/imprint.tex` and `heiglogo.sty` without forking the template. The two
`.tex` files were written against the in-repo LaTeX class TeXSmith replaced and
were adapted: the template's macros (`\booktitle`, `\bookauthor`,
`\bookemail`, `\bookdate`) in place of bare `\title` / `\author` / `\email`,
and plain text where a Creative Commons *font* the class loaded used to draw a
glyph (`\creativecommon` is defined nowhere in this repository). The
`titlingpage` environment stays: the `book` template is `memoir`, which has it
and has no `titlepage`.

LaTeX stops nesting a bullet list at four levels and the Shunting-yard rules
nest six (`Too deeply nested`, the first content error after the cover). A
`tex/handbook.sty` loaded through `press.preamble` fixed it here; TeXSmith
then shipped `texsmith-lists.sty`, which does the same for `itemize` and
`enumerate` alike, so the handbook's copy went again and the preamble loads
the logo only.

Three anchors were renamed, `twos_complement` → `twos-complement` and
friends: an `_` in a label reaches `\hyperref[twos\_complement]{…}`, which
builds a csname and dies on `Missing \endcsname`. The stray second
`sequence_point` anchor became a link to the canonical one.

### The tail of H4, tried and put back

Wave 1 left `--8<-- "file"` inside a fence alone because the web lowering did
not splice `include="file"`. It does now — verified on
`docs/assets/src/hello.c` — so the 36 fences of 15 files were converted, and
put back: **the path is not resolved the same way**. The corpus writes it from
the project directory (`docs/assets/src/hello.c`), which is what
`pymdownx.snippets`' `base_path: .` means and what `--8<--` gets; the site
pre-pass reports `include-missing` for all 36 and leaves the fence **raw**, so
the listing becomes literal ```` ```c include="…" ```` text and swallows the
paragraph after it. Fifteen pages broken on the site; the book pass resolves
them fine. `utils/fix_tmark_deprecations.py` carries the finding where it says
why the corpus keeps the old spelling.

**TeXSmith lesson**: the site pipeline should resolve a fence's `include=`
against the snippet base paths, as it resolves `--8<--`; and an unresolved
include should not leave a fence raw enough to eat the next paragraph.

### Verification

`uv run mkdocs build` (site **and** both `.tex` bundles, 37.8 s, exit 0):

| | wave 1 | wave 2 |
| --- | --- | --- |
| `WARNING` lines | 643 | **79** |
| `ERROR` lines | 0 | **0** |

| code | count | what is left |
| --- | --- | --- |
| `deprecated` | 68 | 36 `--8<--` in a fence, counted twice (site + book); see above |
| `var-unresolved` | 8 | the `{{word}}` fill-in-the-blanks of three exercises |
| `ref-unresolved` | 1 | `@Ry` in a formula of `cpu-zero.md` |
| `asset-convert-failed` | 1 | the `pie` mermaid fence of `me-and-my-computer.md`, already failing in the baseline |

`rm -rf .cache && make zensical`:

* `texsmith site assets` — 122 diagrams, 115 exported, unchanged.
* `zensical build` — **No issues found** (45 before wave 1, 146 with
  `texsmith.site.web`), 8.98 s, 145 pages.
* `texsmith site search` — **74 search entries gained the index entries of
  their page**.
* `texsmith site build` — both PDFs, on a machine to itself:

  | book | bundle | PDF | pages |
  | --- | --- | --- | --- |
  | *L'informatique pour l'ingénieur* | `book.tex` 16.5 KB + 87 page files | 37.8 MB | **640** |
  | *Outils de développement* | `tools.tex` 9.1 KB + 21 page files | 4.5 MB | **64** |

  The C book opens on the HEIG-VD cover (`pdftotext -f 1`: the title, the
  author, the TIN address, the date) and page 3 is the imprint. About six
  minutes end to end — the forty-minute runs of this session were two agents
  compiling the same `build/book/book.tex` at once, which is worth knowing:
  pass `--build-dir` when the tree is shared.

**The printed index is empty.** The 270 `\tsindex` calls all reach
`book.idx` — `makeindex book.idx` turns it into a correct 334-line `book.ind`
(`<complex.h>, 66`, `=, 80`, …) — but `ts-index.sty` is
`\RequirePackage[xindy]{imakeidx}` and `imakeidx` runs the index program
through shell-escape, which the `tectonic` invocation does not enable. So
`\printindex` prints nothing and the book has no index page, silently.
**TeXSmith lesson**: run the index program from the build driver (it already
picks one, `core/templates/base.py:_detect_index_engine`) and re-run the
engine, or enable shell-escape for that pass.

### Still open

* **H7**, waiting on either TeXSmith defect above.
* `mkdocs-plugin-exercises` and `mkdocs-wikipedia` stay in `pyproject.toml`:
  the first still numbers the exercises under MkDocs, the second still fetches
  the article summaries there. `pyproject.toml` is not touched at all in this
  wave.
* `tools/.nav.yml`'s `- "*"` matches nothing and both nav resolvers say so;
  it is the faithful conversion of the `.pages` and was left alone.

### The TeXSmith lessons of this wave

| # | what | where |
| --- | --- | --- |
| 1 | A page's own `press.declare` never reaches the **parser**: `texsmith.site.index` parses the body and attaches the front matter afterwards, so a declared container is `container-unknown` and lowers to literal text. | `site/index.py` `register` / `lower` |
| 2 | `lower_web` splices a `#(prefix:key)` written in a `!!!` callout title at the start of the line instead of at the marker. | `tmark` web lowering |
| 3 | A callout's default title is English whatever `language:` says, and a declared kind's `name:` does not reach the LaTeX word list either. | `fragments/callouts/__init__.py:_callout_words` |
| 4 | `lower_web` mangles a **code span inside a `yaml table` cell**: a cell holding a backticked word renders as a slice of the fence line itself. | `tmark` web lowering |
| 5 | A fence's `include=` is spliced on the web now but its path is not resolved against the snippet base paths, and an unresolved include leaves the fence raw enough to swallow the next paragraph. | `site/` include resolution |
| 6 | `pymdownx.snippets`' `auto_append` is not honoured anywhere, so a site-wide abbreviation list never reaches a book. | `site/config.py`, `site/book.py` |
| 7 | An acronym key that is not csname-safe emits a second `\newacronym` with the **unsanitised** lowercased key: `\newacronym{k&r}` is a LaTeX syntax error. | glossary writer |
| 8 | An `_` in a label reaches `\hyperref[a\_b]{…}`, which builds a csname and dies on `Missing \endcsname`. | LaTeX writer |
| 9 | The index program is never run: `imakeidx` needs shell-escape, `tectonic` is called without it, and `\printindex` prints nothing. | build driver |

#### The half of lesson 5 that stays with the core

The path half is fixed TeXSmith-side: the site hands `lower_web` a loader that
searches the page's directory, then the `--include-path` entries, then the
snippet base paths — the order and the code `resolve_include` uses for the PDF
(`readers/loader.py:SearchPathLoader`). The 36 converted fences go from 36
`include-missing` to 0, and none is left carrying the attribute.

The *unresolved* half is the core's. Evidence, from this repository's own
`pymdownx.superfences`:

```python
>>> markdown.Markdown(extensions=["pymdownx.superfences"]).convert(
...     '```c include="missing.c"\n```\n')
'<p><code>c include="missing.c"</code></p>'
```

`include=` in an info string is not something superfences parses, so the fence
is not a fence at all: it becomes an inline code span, the listing disappears
and the block runs into what follows. When the include cannot be resolved,
`lower_web` keeps the bytes and reports `include-missing` — correct for the
diagnostic, wrong for the page. It should **drop the `include=` option from
the lowered info string** (the fence then renders as a plain, empty `c` block)
and keep reporting `include-missing`; a fence a reader can see is better than
a paragraph a reader loses.

The typography `french.py` did on the web — thin spaces before `;:!?`, `«…»`,
the missing-ligature lint — has no TMark equivalent and is simply lost under
Zensical. `babel-french` still spaces the punctuation in the PDF.

## 9. Wave 3 — what the seven fixed lessons unblocked

Branch `zensical`, on top of wave 2. TeXSmith 0.7.1.dev5 of `/home/ycr/texsmith`
branch `zensical`, `mkdocs-texsmith` 0.7.1.dev4, `tmark-core` 0.1.0 of
`/home/ycr/tmark` branch `autorefs-anchors`, Zensical 0.0.62, MkDocs 1.6.1.

Wave 2 ended on nine TeXSmith lessons. Seven came back fixed — 1, 2, 3, 5, 6, 8
and 9 — and this wave is what the handbook could do once they were. Lessons 4
(a code span inside a `yaml table` cell) and 7 (a csname-unsafe acronym key) are
still open, and neither blocks anything here: the operator table went to a plain
GFM table in wave 2 and `K&R` left the abbreviation list.

### What was done

| # | package | result |
| --- | --- | --- |
| H7 | exercise numbering | **done**: 123 callouts, 25 files, `Exercice 1` … `Exercice 123` on the site, 1 … 118 in the C book |
| (H4) | `--8<--` in a fence | **done**: the 36 fences of 15 files carry `include=`; `deprecated` 68 → 0 |
| — | the 18 French callout titles | **reverted to untitled** |
| — | `tools/.nav.yml`'s `- "*"` | **kept**, in the spelling that says it may match nothing |
| — | the three hyphenated anchors | **kept hyphenated** |

### H7 — the exercises are numbered again

Wave 2's blocker was lesson 1: `texsmith.site.index` parsed a page's body and
attached the front matter afterwards, so `press.declare.admonitions` never
reached the parser and `::: exercise` lowered to literal text. TeXSmith merges
the declarations before parsing now, **and reads them site-wide**, which is
better than what `utils/number_exercises.py` was written against:

```yaml
plugins:
  - texsmith:
      declare:
        counters:
          ex: {name: Exercice, format: "Exercice {n}", scope: document}
        admonitions:
          exercise: {name: Exercice}
```

One place, both parsers — the site's and each book's — so the 25 pages carry
nothing but the rewrite itself and the script lost the front-matter step it
used to need, along with the warning that held it back.

```md
!!! exercise "Mot du jour"    ->  ::: exercise {title="#(ex:mot-du-jour) : Mot du jour"}
```

123 blocks, 25 files. On the site: 123 `<span class="ts-counter" data-counter="ex">`,
numbered **1 … 123 with no gap and no repeat**, continuous in nav order — the
`exercises` plugin restarted at 1 on every page. In the C book's `.tex`, 118
`\begin{tscallout}[kind=exercise, title={…\label{ex:key}Exercice N : …}]`,
numbered 1 … 118: the book is its own document and its own registry. The five
missing ones are `darkside.md`, which no `.nav.yml` lists, so Zensical builds
the page but no book takes it.

**One source bug surfaced.** `darkside.md` had an unclosed ```` ```c ```` fence
that had been there all along: under `!!!` the admonition ended where its
indentation did and took the runaway fence with it, under `:::` the fence ran
on and swallowed the exercise after it (120 was missing from the site's
sequence, which is how it was found). Closed.

**What stays lost with the `exercises` plugin**, and is not TMark's to replace:
the multiple-choice quizzes it built from a `- [x]` list — 129 such lines in 11
files, which render as literal `[x]` list items — and the fill-in-the-blanks it
built from `{{word}}`, 13 markers in 3 files, reported as `var-unresolved`.

### The tail of H4, this time for good

Lesson 5 had two halves and both are fixed. TeXSmith hands the web lowering a
loader that searches the page's directory, the `--include-path` entries and the
snippet base paths, in the order `resolve_include` uses for the PDF, so
`docs/assets/src/hello.c` — written from the project directory, as
`pymdownx.snippets`' `base_path: .` means it — resolves; and the core drops an
`include=` it could not resolve from the lowered info string, so the worst case
is an empty code block instead of the lost paragraph wave 2 measured.

`utils/fix_tmark_deprecations.py` grew the listing rewrite its docstring used
to argue against. It reads fences at **any** indentation — five of the 36 sit
inside a tabbed block or an admonition, which the ≤ 3-space fence regex of the
other two rewrites does not see — and rewrites one only when its whole body is
the include line. 36 listings, 15 files, idempotent.

The 15 pages keep their `<pre>` count to the block (2, 3, 13, 46, 83, 22, 20,
20, 1, 6, 17, 8, 3, 7, 5 before and after), the listings carry their code, and
a `title="slurp.h"` in the info string still reaches the filename bar.
`pymdownx.snippets` stays in `markdown_extensions`: `auto_append` and the
block-level `--8<--` still go through it.

### The 18 callout titles go back

Wave 2 titled eighteen untitled `tip` / `warning` / `example` / `bug` callouts
in French because the LaTeX word list was English whatever `language:` said.
`fragments/callouts/words.py` keys the words by the document's language now, so
`build/book/ts-callouts.sty` defines `ts@callout@word@tip` as *Astuce*,
`@warning` as *Avertissement*, `@bug` as *Bogue* and `@example` as *Exemple*,
and the eighteen titles carried no content the kind does not carry itself.
Reverted. In the finished PDF: 9 *Avertissement*, 6 *Astuce*, 39 *Exemple*, 2
*Bogue*, and the three remaining English words are prose and code, not titles.

### `tools/.nav.yml`

`arrange:` in a `.pages` orders the entries it names and leaves the rest where
they are; `nav:` in a `.nav.yml` is exhaustive, so the faithful conversion ends
on `- "*"`. `docs/tools/` holds exactly the seven directories listed above it,
so the glob matches nothing and awesome-nav says so once per build. Dropping it
would silently drop a page added later, so it keeps the long spelling instead:

```yaml
- glob: "*"
  ignore_no_matches: true
```

Same nav — the "Outils" section still carries its seven children in order — one
warning fewer.

### The three anchors keep their hyphens

`twos-complement`, `calling-conventions` and `sequence-point` were renamed in
wave 2 because an `_` in a label reached `\hyperref[twos\_complement]{…}` and
died on `Missing \endcsname`. Lesson 8 is fixed (`latex: a label name is not
escaped as prose`), so the rename is no longer forced — and they keep the
hyphens anyway: **all 119 `[]{#…}` anchors of the corpus are hyphenated, none
has an underscore**, and the only in-repo links to these three are the ones
wave 2 updated. A deep link from outside to `#twos_complement` on the published
site would break, but these are prose anchors, never surfaced in a table of
contents or a permalink, so consistency wins.

### Verification

`uv run mkdocs build` (site **and** both `.tex` bundles, exit 0):

| | wave 1 | wave 2 | wave 3 |
| --- | --- | --- | --- |
| `WARNING` lines | 643 | 79 | **10** |
| `ERROR` lines | 0 | 0 | **0** |

| code | count | what is left |
| --- | --- | --- |
| `deprecated` | **0** | — |
| `var-unresolved` | 8 | the `{{word}}` fill-in-the-blanks of three exercises |
| `ref-unresolved` | 1 | `@Ry` in a formula of `cpu-zero.md` |
| `asset-convert-failed` | 1 | the `pie` mermaid fence of `me-and-my-computer.md`, failing since the baseline |

The nineteenth line of wave 2, awesome-nav's `'*' doesn't match any files`, is
gone with the `.nav.yml` change.

`rm -rf .cache && make zensical`, about six minutes end to end:

* `texsmith site assets` — 122 draw.io diagrams, all up to date.
* `zensical build` — **No issues found**, 8.9 s, 145 HTML pages.
* `texsmith site search` — **74 search entries gained the index entries of
  their page**.
* `texsmith site build` — both PDFs, on a machine to itself:

  | book | bundle | PDF | pages |
  | --- | --- | --- | --- |
  | *L'informatique pour l'ingénieur* | `book.tex` 16.6 KB + 87 page files | 37.8 MB | **647** |
  | *Outils de développement* | `tools.tex` 9.2 KB + 21 page files | 4.5 MB | **65** (64 in wave 2) |

**The index prints, and so do the acronyms.** Lesson 9 is fixed: the build
driver runs the index program itself instead of leaving it to `imakeidx` and a
shell escape `tectonic` never got. The C book's 270 `\tsindex` calls reach
`book.idx`, `makeindex-py` turns them into a 325-line `book.ind`, and pages
645–647 are the printed *Index* (`0b, 79`, `=, 80`, `while, 72`). Lesson 6 is
fixed too — `pymdownx.snippets`' `auto_append` is honoured — so
`includes/abbreviations.md` reaches both books: `makeglossaries-py` and `xindy`
build `book.acr` and pages 641–644 are the *Acronymes* list. The tools book
gained its own acronym page, which is its 64th → 65th page. 40 of the 44
abbreviations reach the preamble; `UTF-8` lands under the key `UTF8`, and
`EOF`, `FLOPS`, `SVG` and `W3C` do not appear — worth one look next wave.

The cover and the imprint are unchanged: page 1 is the HEIG-VD title page, page
3 the imprint with the Creative Commons text.

Browse check, `uv run zensical serve -f mkdocs.yml -a 127.0.0.1:8123`:

* `/course-c/10-numeration/bases/` — 6 `<div class="admonition exercise">`,
  each opening on `<span class="ts-counter" data-counter="ex">Exercice 22…24…</span>`.
* `/course-c/40-algorithms/utilities/` — 8 `<pre>`, two of them titled
  `slurp.h` and `slurp.c`, and no `include=&quot;` anywhere in the page.
* `/course-c/05-introduction/programming/` — every `.drawio` rewritten to its
  `assets/drawio/**.svg` export, no `.drawio` left in a `src`.

### Still open

**TeXSmith / tmark owe**

* Lesson 4: `lower_web` mangles a code span inside a `yaml table` cell, which
  is why the operator-priority table is a plain GFM table with its priority
  repeated on every row instead of the row spans `yaml table` can express.
* Lesson 7: an acronym key that is not csname-safe emits a second
  `\newacronym` with the unsanitised key. `K&R` left `includes/abbreviations.md`
  because of it.
* Four abbreviations (`EOF`, `FLOPS`, `SVG`, `W3C`) never reach `ts-glossary.sty`
  although the other forty do; cause unknown.
* `@Ry` in `cpu-zero.md` — a subscript in a formula the reference resolver reads
  as a counter reference. Either the formula or the resolver.
* The `pie` mermaid fence of `me-and-my-computer.md` — `asset-convert-failed`
  since the baseline.
* Nothing replaces `french.py`'s web typography: thin spaces before `;:!?`,
  `«…»`, the missing-ligature lint. `babel-french` still does it in the PDF.

**The handbook owes**

* **CI still publishes with MkDocs.** `.github/workflows/ci.yml` runs
  `mkdocs gh-deploy --force`; the Zensical chain is `make zensical` and nothing
  runs it. Switching the workflow is the last step of the migration, and it is
  what decides when the MkDocs-only plugins can go.
* **`mike` is dead weight.** It is a dependency (`mike>=2.1.3`) but its plugin
  is commented out in `mkdocs.yml` and the workflow deploys with `gh-deploy`
  directly, so nothing versions the site today. Zensical has no `mike`: if the
  handbook wants versioned docs, that is a question to answer before the CI
  switch, not after — and if it does not, `mike` should simply leave
  `pyproject.toml`.
* **The plugins that only run under MkDocs.** Zensical has no plugin hooks, so
  `exercises`, `wikipedia`, `caption`, `glightbox`, `drawio`, `tags`, `pills`
  and `autorefs` are inert there. Most have been replaced; two have not:
  `caption` numbered every plain `![alt](img)` into a `<figure>` with a
  `Figure N` caption, and on Zensical those images are bare `<img>` (the PDF
  numbers its figures itself, so only the web loses this); and `search` is
  replaced by `texsmith site search` in the chain.
* **`mkdocs-plugin-exercises` and `mkdocs-wikipedia` can go** once CI stops
  running MkDocs — the exercises are numbered by TMark now, and the article
  summaries are the only thing `wikipedia` still adds.
* `pyproject.toml` still carries the `tmark-core` path override
  (`/home/ycr/tmark/crates/tmark-py`) alongside the two editable TeXSmith
  paths. The TeXSmith ones go when 0.7.1 is released; the `tmark-core` one waits
  on a `tmark-core` release carrying the fixes this wave used — the site-wide
  declarations, the unresolved-`include=` drop, the unescaped label names and
  the localised callout words. **Never commit it.**
* The 13 `{{word}}` fill-in-the-blanks (8 `var-unresolved` lines, one per
  distinct marker position the writers report) and the 129 `- [x]` quiz
  lines are dead
  markup on both media. Either they become prose (a solution callout with the
  answer) or something has to render them.
