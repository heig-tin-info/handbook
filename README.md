# Handbook

Cours d'informatique pour les étudiants de la HEIG-VD, département TIN.

Ce cours couvre les bases de l'informatique, de l'architecture des ordinateurs à la programmation en C.

La version web est disponible sur cette [page](https://heig-tin-info.github.io/handbook/).

## Développement

```bash
poetry install
poetry run mkdocs serve
```

### Docker

Alternativement, vous pouvez utiliser Docker pour lancer le serveur de développement :

```bash
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

### Vscode

Installer l'extension `vscode-yaml` pour une meilleure coloration syntaxique des fichiers `.yml`.

## To-Do

- [ ] Fix drawio generation on GitHub Actions
- [ ] Make figures compatible with both light/dark theme
- [ ] Tables
  - [ ] Caption above table
  - [ ] Addfull parameter for adjusting width, fullwidth
  - [ ] Alternate colors for table entries
  - [ ] Number table from section number
- [ ] Slides for each course with inteactive examples
- [ ] Embedded Interactive examples (linked-list)...
- [ ] Interactive exercices
  - [ ] Multiple choice
  - [ ] Code execution
  - [ ] Fill the gap
- [ ] Generate PDF with LaTeX
- [x] Center tables
- [x] Two columns for itemize ?

### Content

- [ ] Architecture de l'ordinateur, alu...

## Guideline

Inline code, use the following to specify the language in inline code:

```
`#!py3 code`
```

Tabbed

```markdown
=== "Fruit List"
    - :apple: Apple
    - :banana: Banana
    - :kiwi: Kiwi

=== "Fruit Table"
    Fruit           | Color
    --------------- | -----
    :apple:  Apple  | Red
    :banana: Banana | Yellow
    :kiwi:   Kiwi   | Green
```

Pages:

Create a `.pages` file in the `docs` folder with the following content:

```yaml
title: "Title"
arrange:
    - page1.md
hide: true
collapse : true
```

## Extensions to be implemented

### Drawio

Currently drawio conversion occurs at each build (very slow) and does not support dark mode. It would be nice to have a way to convert the drawio files to svg and include them in the markdown files.

One solution for simple graphics is to include svg directly and twick the svg to map colors with the theme colors.

One possiblity is to integrate the svg as `<object>` and use css to style the svg.

### Exercices

- Add "Exercise:" before admonition Exercice
- Number exercises with section number
- Multiple choice questions, letting user to choose the answer and show the correct one
- Regroup all exercices in one page

#### Multiple choice

Could improve the design of the checkbox with these https://getcssscan.com/css-checkboxes-examples :

```html
<div class="checkbox-wrapper-32">
  <input type="checkbox" name="checkbox-32" id="checkbox-32">
  <label for="checkbox-32">
    Checkbox
  </label>
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M 10 10 L 90 90" stroke="#000" stroke-dasharray="113" stroke-dashoffset="113"></path>
    <path d="M 90 10 L 10 90" stroke="#000" stroke-dasharray="113" stroke-dashoffset="113"></path>
  </svg>
</div>

<style>
  .checkbox-wrapper-32 {
    --size: 20px;
    --border-size: 2px;

    position: relative;
  }

  .checkbox-wrapper-32 *,
  .checkbox-wrapper-32 *::after,
  .checkbox-wrapper-32 *::before {
    box-sizing: border-box;
  }

  .checkbox-wrapper-32 input[type="checkbox"] {
    display: inline-block;
    vertical-align: middle;
    opacity: 0;
  }

  .checkbox-wrapper-32 input[type="checkbox"],
  .checkbox-wrapper-32 label::before {
    width: var(--size);
    height: var(--size);
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
  }

  .checkbox-wrapper-32 label {
    display: inline-block;
    position: relative;
    padding: 0 0 0 calc(var(--size) + 7px);
  }

  .checkbox-wrapper-32 label::before {
    content: '';
    border: var(--border-size) solid #000;
    opacity: 0.7;
    transition: opacity 0.3s;
  }

  .checkbox-wrapper-32 input[type="checkbox"]:checked + label::before {
    opacity: 1;
  }

  .checkbox-wrapper-32 svg {
    position: absolute;
    top: calc(50% + var(--border-size));
    left: var(--border-size);
    width: calc(var(--size) - (var(--border-size) * 2));
    height: calc(var(--size) - (var(--border-size) * 2));
    margin-top: calc(var(--size) / -2);
    pointer-events: none;
  }

  .checkbox-wrapper-32 svg path {
    stroke-width: 0;
    fill: none;
    transition: stroke-dashoffset 0.2s ease-in 0s;
  }

  .checkbox-wrapper-32 svg path + path {
    transition: stroke-dashoffset 0.2s ease-out 0.2s;
  }

  .checkbox-wrapper-32 input[type="checkbox"]:checked ~ svg path {
    stroke-dashoffset: 0;
    stroke-width: calc(var(--size) / 2);
  }
</style>
```

### References to figures

In figure [](fig:label), we can see that...

```markdown
![Caption](url){label="fig:label"}
```

### Table caption ?

How to add a caption to a table ? The plugin `mkdocs-caption` is straightforward, but does not support:

- Table above the caption
- Number from section numbers section.number
- No alt text for the caption
- No markdown in the caption (Table: *italic*) not supported

```markdown

Table: Caption

| Header 1 | Header 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |
```

We could use superfences to add a caption and caption alt to the table:

```markdown

Table: Caption {#my_id alt="Short Caption"}

| Header 1 | Header 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |

```

### Preview Wikipedia links in modal

When highlight a wiki link, show a modal with the content of the page.


## My extensions

### Numbering

The plugin `mkdocs-numbering` has several goals:

- Add section numbering
- Numbering can be configured to appear in the title, in the TOC, in the sidebar
- Add table, figure and equation numbering, based on the section numbers
- Configure admonition numbering

```yaml
plugins:
  numbering:
    toc: true
    sidebar: true
    admonition:
      - exercise