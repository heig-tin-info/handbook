---
frontmatter: true
---
# Préface

## À qui s'adresse cet ouvrage ?

Conçu comme un résumé du savoir nécessaire à l'ingénieur pour s'initier à la programmation et prendre en main le langage C, cet ouvrage n'est pas un manuel de référence. Il se réfère à de nombreuses ressources internet et livres que le lecteur pourra consulter au besoin pour approfondir certains concepts.

Chaque chapitre est composé d'exercices, mais à des fins pédagogiques, l'intégralité des solutions ne sont pas fournies; certains exercices sont destinés à être faits en études.

Cet ouvrage est destiné à des étudiants ingénieurs de première année n'ayant aucune expérience en programmation.

Le contenu concerne principalement les cours d'informatique 1 et 2 de l'enseignement de base du département des technologies industrielles (TIN) de la HEIG-VD.

## Cours d'informatique cursus bachelor

Ce cours d'informatique à la HEIG-VD est donné par le département TIN dans les cours du cursus Bachelor en Génie électrique. Il concerne tout particulièrement les étudiants des cours suivants&nbsp;:

- Informatique 1 (INFO1) - 101 Première année
- Informatique 2 (INFO2) - 102 Première année
- Microinformatique (MICROINFO) - 101 Première année

## Quel programmeur êtes-vous ?

Les études en écoles d'ingénieurs sont souvent cloisonnées. On observe, entre les différentes facultés (électronique, informatique, etc.), que l'enseignement de l'informatique s'inscrit dans une culture distincte avec un langage spécifique. Les informaticiens, dotés d'un esprit d'abstraction remarquable, acquièrent des connaissances approfondies du fonctionnement interne des systèmes d'exploitation et possèdent une expertise étendue en programmation. Néanmoins, ils manquent parfois d'une expérience pratique avec le matériel électronique et les contraintes imposées par des architectures matérielles légères (systèmes embarqués, microcontrôleurs, etc.). Les électroniciens, quant à eux, disposent d'une compréhension approfondie des systèmes à bas niveau. Ils ont une vision pragmatique des systèmes et des contraintes matérielles. Cependant, ils manquent souvent de connaissances poussées en programmation et en algorithmique.

Ces deux profils, bien que complémentaires, ont souvent du mal à se comprendre. Les informaticiens perçoivent les électroniciens comme trop terre-à-terre, tandis que les électroniciens jugent les informaticiens trop abstraits. Des divergences d'opinions peuvent émerger de ces différences culturelles, notamment dans des notions communes dont les définitions varient. Par exemple, la notion de temps réel diffère pour un informaticien et un électronicien. Pour un informaticien, le temps réel désigne un système qui répond dans un délai déterminé pour un utilisateur (environ 100 ms). Pour un électronicien, le temps réel désigne un système qui répond dans un délai déterminé et qui est déterministe (environ 100 µs).

Un autre exemple est la complexité algorithmique. Pour un informaticien, la complexité algorithmique mesure la performance d'un algorithme en termes généraux. Un accès à un dictionnaire est en $O(1)$, même s'il implique le calcul d'un `sha256`, une opération triviale sur un ordinateur. Pour un électronicien, il est impossible de réaliser un `sha256` sur un microcontrôleur 8 bits, ce qui l'incite à rechercher des optimisations profondes de l'algorithme, quitte à le rendre moins générique et modulaire.

Cet ouvrage a pour objectif de rapprocher ces deux cultures en fournissant aux électroniciens les bases de la véritable informatique, de la programmation et de sa culture, en rendant accessibles des concepts complexes tels que les arbres et les graphes.

## Organisation de l'ouvrage

/// html | div[class="latex-ignore"]

### Raccourcis clavier

Pour améliorer votre navigation sur ce site, voici quelques raccourcis clavier que vous pouvez utiliser:

++f++, ++s++, ++slash++

: Ouvre la barre de recherche

++p++, ++comma++

: Va à la page précédente

++n++, ++period++

: Va à la page suivante

++b++

: Afficher/cacher les tables des matières

++m++

: Afficher/cacher le menu

++h++

: Afficher/cacher la table des matières

///

### Conventions d'écriture

#### Encodage de caractère

Il sera souvent fait mention dans cet ouvrage la notation du type U+1F4A9, il s'agit d'une notation Unicode qui ne dépend pas d'un quelconque encodage. Parler du caractère ASCII 234 est incorrect, car cela dépend de la table d'encodage utilisée; en revanche, la notation Unicode est plus précise.

/// html | div[class="latex-ignore"]
La notation est cliquable et vous redirigera vers le site [symbl.cc](https://www.symbl.cc/).
///

#### Expressions régulières

Les expressions régulières sont utilisées pour décrire des motifs de texte. Elles sont utilisées pour rechercher, remplacer ou valider des chaînes de caractères. Les expressions régulières sont utilisées dans de nombreux langages de programmation, d'outils de recherche et de traitement de texte.

Aussi dans cet ouvrage, les expressions régulières sont mises en évidence avec `/regex/`. Le lien mène au site [regex101.com](https://regex101.com/). Pour tester les expressions régulières, il vous suffit alors d'ajouter votre propre texte pour tester l'exemple donné.

#### Symbole d'égalité

Nous verrons que le signe d'égalité `=` peut aisément être confondu avec l'opérateur d'affectation du langage C qui s'écrit de la même manière. Dans certains exemples où l'on montre une égalité entre différentes écritures, le signe d'égalité triple U+2261 sera utilisé pour dissiper toute ambiguïté éventuelle:

```
'a' ≡ 0b1100001 ≡ 97 ≡ 0x61 ≡ 00141
```

#### Symbole de remplissage

Dans les exemples qui seront donnés, on pourra voir `#!c while (condition) { 〜 }` ou le caractère `〜` U+3030 indique une continuité logique d'opération. Le symbole exprime ainsi `...` ([points de suspension](https://fr.wikipedia.org/wiki/Points_de_suspension) ou *ellipsis*). Or, pour ne pas confondre avec le symbole C `...` utilisé dans les fonctions à arguments variables tels que `printf`.

#### Types de données

Les conventions C s'appliquent à la manière d'exprimer les grandeurs suivantes :

- `0xABCD` pour les valeurs hexadécimales `/0x[0-9a-f]+/i`
- `00217` pour les valeurs octales `/0[0-7]+/`
- `'c'` pour les caractères `/'([^']|\\[nrftvba'])'/`
- `123` pour les grandeurs entières `/-?[1-9][0-9]*/`
- `12.` pour les grandeurs réelles en virgule flottante

#### Encadrés

Des encadrés sont utilisés pour mettre en avant des informations complémentaires ou des astuces. Ils sont également utilisés pour donner des informations sur des concepts avancés ou des détails techniques.

/// html | div[style='display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-evenly;']

!!! info inline

    Fait historique où information complémentaire pour ceux qui voudraient en savoir plus.

!!! warning inline

    Point important à faire attention qui source d'erreur fréquente.

!!! danger inline

    Note importante qui comporte des risques à considérer.

!!! example inline

    Exemple pratique pour illustrer un concept.

!!! note inline

    Corollaire à retenir.

!!! tip inline

    Truc ou Astuce pour faciliter la compréhension.

!!! bug inline

    Limitations ou bugs possibles d'une méthode proposée.

!!! exercise inline "Quelle icône ?"

    Quelle icône est utilisée pour les exercices ?

///

## Anglicismes

Parler l'informatique ou de technologies sans utiliser d'anglicismes est un exercice difficile. Il est parfois moins lourd de parler de *hardware* que de *matériel informatique*. Certains termes n'ont pas de traduction en français. Par exemple, le terme *set* appliqué à un ensemble de données n'a pas de traduction crédible en français. La table [][anglisismes] quelques termes qui seront utilisés dans cet ouvrage:

Table: Anglicismes


| Anglais | Français | Préférence |
|---------|----------|------------|
| *hardware* | matériel informatique | *hardware* |
| *software* | logiciel informatique | *software* |
| *byte* | octet | *byte* |
| *set* | ensemble | *set* |
| *pipe* | tube | *pipe* |
| *stream* | flux de données | *stream* |
| *listing* | extrait de code | *listing* |
| *process* | processus | processus |
| *seekable* | positionnable | *seekable* |

[](){#anglisismes}

Notons que *byte* et *octet* ne sont pas exactement synonymes. Un *byte* est un ensemble généralement admis de 8 bits mais dont la taille a pu varier selon les années, alors qu'un *octet* est un ensemble de 8 bits sans exception. En pratique, les deux termes sont souvent utilisés de manière interchangeable. En anglais il n'existe pas de mot pour *octet*.

Les termes anglais sont généralement indiqués en italique.

## Copyright et références

Le contenu de ce livre est sous licence [Creative Commons](https://creativecommons.org/licenses/by-sa/4.0/). Vous êtes libre de partager et d'adapter ce contenu pour toute utilisation, même commerciale, à condition de citer l'auteur et de partager vos travaux dérivés sous la même licence.

De nombreuses références et sources de ce livre sont issues de Wikipedia, de la documentation officielle de la norme C, de StackOverflow, de forums de discussion et de blogs.

## Comment contribuer ?

Vous avez remarqué une erreur, une faute de frappe ou une information manquante ? Vous auriez désiré une explication plus détaillée sur un sujet ? Vous pouvez contribuer à l'amélioration de ce livre en soumettant une [issue](https://github.com/heig-tin-info/handbook/issues). Alternativement, vous pouvez faire un *fork* du projet et proposer une *pull request*.

## Colophon

Ce livre est écrit en [Markdown](wiki:markdown) et généré en HTML par [MkDocs](https://www.mkdocs.org/). Le thème utilisé est [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). Les sources sont disponibles sur [GitHub](wiki:github) et l'hébergement est assuré par [GitHub Pages](https://pages.github.com/).

La plupart des illustrations sont réalisées avec [Draw.io](https://www.draw.io/), un outil de dessin vectoriel en ligne. Les schémas sont rendus dans le navigateur avec `GraphViewer`. Les diagrammes utilisent la technologie [Mermaid](https://mermaid-js.github.io/mermaid/#/). Les autres sources d'images sont issues en grande partie de [Wikimedia Commons](https://commons.wikimedia.org/) et [Wikipedia](https://www.wikipedia.org/).

La génération de l'ouvrage en PDF est utilise son propre convertisseur vers LaTeX. Les extraits de code sources sont colorés avec [Pygments](https://pygments.org/) en utilisant le paquet [minted](https://ctan.org/pkg/minted).

L'orthographe et la grammaire ont été revues avec [Antidote](https://www.antidote.info/).