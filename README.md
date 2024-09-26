# Handbook

![.github/workflows/ci.yml](https://github.com/heig-tin-info/handbook/workflows/.github/workflows/ci.yml/badge.svg)

![version](https://img.shields.io/github/v/release/heig-tin-info/handbook)
![downloads](https://img.shields.io/github/downloads/heig-tin-info/handbook/latest/total)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/heig-tin-info/handbook)

Ce référentiel contient un livre sur l'informatique. Il est destiné à être utilisé comme support de cours pour les étudiants de la [HEIG-VD](http://www.heig-vd.ch), département TIN. Il couvre les bases de l'informatique, de l'architecture des ordinateurs à la programmation en C. Il est prévu de l'étendre à C++ et Python.

La version web est disponible sur cette [page](https://heig-tin-info.github.io/handbook/).

## Technologie

Le livre est écrit en Markdown en utilisant [MkDocs](https://www.mkdocs.org/) et le thème [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) accompagné de nombreuses extensions et plugins personnels. Les graphiques sont générés avec [Mermaid](https://mermaid.js.org/) et [Draw.io](https://www.drawio.com/).

La valeur ajoutée est la génération d'un livre PDF à partir du site web en respectant une mise en page stricte et soignée. Ceci est rendu possible à l'aide du moteur [LaTeX](https://www.latex-project.org/) (LuA)TeX. Un générateur LaTeX a totalement été écrit pour permettre la génération du livre en PDF car les outils existants ne répondaient pas à nos besoins.

## Contribuer

### Différences livre web et PDF

Le contenu Markdown est la seule source de données pour la génération du site web static et le livre PDF. Aussi, il est important de respecter quelques  règles pour éviter des problèmes lors de la génération.

La présentation d'un imprimé est différente de celle d'un site web. On peut identifier les différences suivantes :

- Un site utilise des liens hypertextes pour naviguer entre les pages, un livre utilise des références croisées basées sur des identifiants de section ou d'élément (figure, table).
- Les sections web n'ont pas besoin d'être numérotées alors que les sections d'un livre doivent l'être pour permettre les références croisées.
- Les figures, les tableaux et les équations peuvent être des flottants, c'est à dire qu'elles peuvent être déplacées par le moteur de composition pour une meilleure harmonie de la page alors que sur un site internet elles sont insérées à l'endroit où elles sont déclarées puisque la page n'a pas de bornes fixes.
- Une référence un flottant peut être relatif à sa position dans le texte (en-dessous, en-dessus) alors que dans un livre, elle doit être absolue (page, section).
- Dans un site web, des liens hypertextes externes peuvent être utilisés pour référencer à des ressources en provenance d'autres sites (Wikipédia, etc.) alors que dans un livre, il est préférable de citer la source directement dans le texte par exemple avec une note de base de page ou une référence bibliographique.
- Il est courant de voir des reférences externes informatives sur un site web, c'est à dire des liens hypertextes vers des ressources externes pour approfondir un sujet mais qui ne servent pas le propos du document. Ces liens informatifs ne sont généralement pas présents dans un livre qui ne ferait que gonfler la bibliographie sans valeur ajoutée aucune.
- La hiérarchie des titres à une importance moindre sur un site web, il n'est pas rare de faire figurer du texte après un titre de premier niveau alors que dans un livre, les parties et les chapitres influencent la mise en page et aucun texte n'est généralement permis après un titre de premier (partie) ou de second niveau (chapitre).
- Un livre contient généralement une table des matières, un index, une bibliography, un glossaire, une liste des figures et des tableaux ainsi qu'une liste des acronymes, termes et définitions. Ces éléments sont généralement absents d'un site web.

### Limites de la technologie

Le langage Markdown dans sa forme la plus simple ne permet pas de définir des éléments de structure complexes. Heureusement des extensions existent pour combler ces lacunes. Cependant, ces extensions s'efforcent de ne pas casser le parseur Markdown de base. Cela signifie que certaines constructions ne sont pas possibles ou sont très difficiles à réaliser. Par exemple, il est difficile de définir des environnements flottants ou d'associer à des liens des attributs supplémentaires. Il a fallu alors développer quelques extensions très spécifiques au besoin pour combler ces lacunes.

### Règles et conventions

#### Liens hypertextes

Un lien hyper texte Markdown est défini par `[texte](url)`. Pour les liens externes et `[texte][identifiant]` (plugin [autorefs](https://mkdocstrings.github.io/autorefs/)) pour les liens internes. Un lien externe peut être *informatif* ou *cité*. Les liens informatifs superposés à un texte sont laissés dans le documents PDF mais inaccessibles dans l'imprimé. S'il s'agit d'un lien cité, il doit figurer dans la bibliographie. Voici quelques exemples:

> Le site [Stack Overflow](https://stackoverflow.com) est une ressource incontournable pour les développeurs. (informatif)

Ce dernier peut être résolu par

1. une note de bas de page
2. une référence bibliographique en fin d'ouvrage
3. aucun des deux.

```markdown
Karl Tombre dans son ouvrage [Introduction à la programmation](https://members.loria.fr/KTombre/DepInfo/PolyTC/tcinfo.pdf){ .cite .page=45 } introduit la programmation objet par l'école de programmation Algol (cité)
```

Le propos de l'ouvrage s'appuie sur une référence bibliographique comme élément vérifiable et vérifié. Le lien peut être résolu par :

1. une note de bas de page (`[1]`)
2. une référence bibliographique en fin d'ouvrage (`[tombre2003]`)

Dans les deux cas et pour ne pas encombrer le texte, le lien, ainsi que le texte associé est déplacé, on obtient alors :

```markdown
Karl Tombre dans son ouvrage [tombre2023] introduit la programmation objet par l'école de programmation Algol.
```

Par défaut le texte du lien est conservé, mais il peut être caché avec `{ .hide }`

#### Références à des flottants

Le plugin [caption](https://tobiasah.github.io/mkdocs-caption/) permet de définir des flottants comme des figures ou des tables avec un titre et une légende. Les flottants sont référencés par un identifiant unique :

```markdown
Table: Exemple de tableau {#table-example}

| Colonne 1 | Colonne 2 |
| --------- | --------- |
| Ligne 1   | Ligne 1   |
```

Dans le texte d'une page web on trouvera volontiers :

```markdown
En Markdown on peut insérer des tabeaux comme le montre la table [#table-exemple].
```

Cette référence peut être résolue par :

1. Le numéro de table si la table est numérotée.
2. Le titre de la table si la table n'est pas numérotée.
3. Le texte `ci-dessus`, `supra` ou `ci-dessous`, `infra`.

En outre, un flottant est référencé dans un imprimé dans une liste des tables/figures par un descriptif court. En LaTeX on utilise `\caption[court]{long}` pour définir le descriptif destiné à la liste des tables ou figures, et la légende du flottant. En Markdown, il n'y a pas de syntaxe pour définir un descriptif court. On peut utiliser `{ .short="descriptif court" }` pour définir un descriptif court.

Pour les figures, on peut profiter de la syntaxe Markdown pour le descriptif court :

```markdown
Figure: Descriptif **long** de la figure {#figure-example}

![Descriptif court](images/figure.png)
```

#### Index

Dans un imprimé, il n'y a pas de champ de recherche, le lecteur se réfère généralement à la table des matières ou à l'index pour retrouver des informations. L'index est généré automatiquement à partir d'entrées choisies dans le texte. Le hook `index` permet de définir des entrées d'index dans le texte avec la syntaxe:

```markdown
L'informaticien [[Brian Kernighan]] est connu pour avoir co-écrit le livre *The C Programming Language* avec [[Dennis Ritchie]].
```

Parfois, il existe des entrées d'index qui doivent être écrites différement dans le texte et dans l'index. Le film `[[The Matrix|Matrix|Matrix, the]]` est un exemple de ce cas. Dans le texte, on verra `The Matrix`, un tag MkDocs sera associé à cette section `Matrix` et l'entrée d'index sera `Matrix, the`. Une entrée supplémentaire `[[||Matrix]]` permet de n'insérer aucun texte mais d'avoir une référence `Matrix` dans l'index pointant vers la section dans laquelle elle est déclarée.

#### Glossaire

En LaTeX, il est possible de définir un glossaire avec le package `glossaries` qui permet d'associer une définition à un terme. En Markdown, il n'y a pas de syntaxe pour cela. [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/tooltips/#adding-abbreviations) défini une syntaxe pour ajouter des abbréviations (acronymes) qui peuvent être utilisées comme entrées de glossaire. Par exemple, `OS` est défini comme `Système d'exploitation`. Lorsque le lecteur survole `OS`, il verra la définition `Système d'exploitation`. La syntaxe proposée par Material for MkDocs est transparente, il suffit de définir quelque part dans le document :

```markdown
*[OS]: Système d'exploitation
```

#### Liens Wikipedia

Il est courant de faire référence à des articles Wikipedia pour approfondir un sujet. Dans un imprimé, ces liens n'étant pas accessibles, il est possible d'extraire de Wikipedia le résumé de la page ainsi que son titre qui peut faire office de référence bibliographique et de glossaire.

## Développement

La version utilisée est Ubuntu 24.04 LTS. Commencez par installer les paquets suivants :

```bash
sudo apt install -y fonts-noto
sudo apt install -y texlive-full
sudo apt install -y pipx
sudo fc-cache -fv
```

L'image Docker `Dockerfile` permet alternativement de compiler le livre en PDF.

Initialisez le dépôt  avec :

```bash
git clone https://github.com/heig-tin-info/handbook.git
cd handbook
pipx install poetry
```

Puis pour lancer le développement :

```bash
poetry install
poetry run mkdocs serve
```

## Références

- [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions)
- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Mermaid](https://mermaid.js.org/)
- [Draw.io](https://www.draw.io/)