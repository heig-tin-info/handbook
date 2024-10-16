# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Update MkDocs Material, remove fix for tags in search
- Split template LaTeX in imprint and titlepage
- Add content MCU, CPU and some figures
- Adds some information about processors
- Adds DEVEL.md for documentation
- Adds a new hook for linking abbreviations to wikipedia
- Move LaTeX class definition in a separate file mkbook.cls
- Add wikipedia links in glossary
- Update project readme
- Create devcontainer for development with VSCode
- Include Wikipedia links in addition to `wiki:`
- Remove `wiki:` replace with urls
- Add wiki url in latex glossary
- Update index
- Save wiki links on_env
- Update Dockerfile to freeze version based on TexLive 2023
- Add support for Xindy in Dockerfile (works for glossary)
- On LaTeX description list, add more space between item and desc.
- valdrind, gdb, strace, ltrace
- More content on quality and security
- Multibook build
- Specify hero logo
- Specify coverpage theme
- Specify coverpage color from mkdocs.yml
- Generate Tools book
- Autoindex of C keywords and functions
- libuv
- Complete Algorithmes utilitaires (split, slurp, join, trim)

## 0.1.12

### Fix

- Slighly reduce the size of the tables
- Do not enlarge tables in LaTeX, only reduce when too large
- Reduce tables by default
- Add index entries for single inline keywords (printf, ...)

## 0.1.10

### Content

- Errno, traitement des erreurs
- Redraw ASCII tables in drawio, support for transparency

### Added

- New feature : add tags anywhere (inline tags) to summary concepts
- Add regexes with `#!re /pattern/replacement/flags`.
- Multiple choice exercises

### Improvements

- Caption above table
- Remove feedback title : feedback_title: "" as the field is required
- Do not use adjustbox on small tables
- Gray colors for drawio
- Permanent link not translated, now in french

### Fixes

- Mint inline in titles cause weird behavior in the toc.
- Avoid breaking code block if contains boxchars or special chars
- Exercises style bullet is wrong
- ⇧ 🠔 missing
- Weird position of carret in code in tables
- Author not in title page

## 0.1.9

- LaTeX
  - Generate PDF with LaTeX
  - Only generate LaTeX on build
  - Replace weavydash with 〜 ?
  - Fetch solution to exercises and display them later in document
  - Number exercises with a counter
  - Support unicode chars in LaTeX (Use lualatex?)
  - Auto number tables?
  - \leavevmode only if item is right before code block
- Find a way to add unbreakable space before semi-colon in paragraphs
- Center mermaid diagrams
- Center tables
- Two columns for itemize ?
- Drawio
  - Allow to click on drawio image to see it full screen
  - Drawio and SVG size is not correct
  - Update drawio plugin to use theme colors.
  - Drawio export doesn't accept attributes {width=100%}
  - Fixed by rendering the drawio frontend with a mygraph parser
- When I enable navigation.tabs, I dont see the fold/unfold
  - Fixed by not enabling the navigation.sections
- CI cannot get insiders version of mkdocs.
  - Fixed by adding git config --global url."https://${GH_TOKEN}@github.com/".insteadOf `git@github.com:`
- Tables
  - Rowspan
