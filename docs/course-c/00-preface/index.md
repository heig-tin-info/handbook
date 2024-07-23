# Préface

## Quel programmeur ?

Les cursus académiques en écoles d'ingénieurs sont souvent cloisonnées. Il existe une démarcation franche entre les facultés d'informatique et celle d'électronique. On observe en cotoyant ces profiles aux pédigrées différents, une culture du métier très différente. Les informaticiens disposent d'un excellent esprit d'abstraction, on connaissances du fonctionnement interne d'un système d'exploitation et possèdent de larges connaissances en programmation. Néanmoins, ils manquent d'une assise pratique avec le matériel électronique et les limites imposées par des architectures matérielles légères. Les électroniciens, quant à eux, ont une connaissance approfondie dans le bas niveau. Ils ont une vision pratique des systèmes et des contraintes matérielles. Cependant, ils manquent souvent de connaissances en programmation et en algorithmique.

Ces deux profiles bien que complémentaires ont souvent du mal à se comprendre. Les informaticiens trouvent les électroniciens trop terre-à-terre et les électroniciens trouvent les informaticiens trop abstraits. Des digergeances d'opinions peuvent naître de ces différences de culture, notament dans des notions communes dont les définitions varient. Par exemple, la notion de temps réel n'est pas la même pour un informaticien que pour un électronicien. Pour un informaticien, le temps réel est un système qui répond dans un délai déterminé pour un utilisateur ($\approx 100~ms$). Pour un électronicien, le temps réel est un système qui répond dans un délai déterminé et qui est déterministe ($\approx 100~\mu s$).
Un autre exemple est la complexité algorithmique. Pour un informaticien, la complexité algorithmique est une mesure de la performance d'un algorithme en termes généraux. Un accès à un dictionnaire est en $O(1)$, même s'il faut calculer un `sha256` qui est une formalité sur un ordinateur. Pour un électronicien, il lui est impossible de faire un `sha256` sur un microcontrôleur 8 bits et il s'intéressera à des optimisations profondes de l'algorithme, quitte à le rendre moins générique et modulaire.

Cet ouvrage a pour but de rapprocher ces deux cultures en donnant aux électroniciens les bases de la "vraie" informatique, de la programmation et de sa culture en rendant accessibles des concepts complexes tels que les arbres ou les graphes.

## À qui s'adresse cet ouvrage ?

Conçu comme un résumé du savoir nécessaire à l'ingénieur pour prendre en main le langage C, cet ouvrage n'est pas un manuel de référence. Il réfère à de nombreuses ressources internet et livres que le lecteur pourra consulter au besoin pour approfondir certains concepts.

Chaque chapitre est composé d'exercices, mais à des fins pédagogiques, toutes les solutions ne sont pas données. Certains exercices sont destinés à être faits en études.

Cet ouvrage est destiné à des étudiants ingénieurs de première année n'ayant aucune expérience en programmation.

Le contenu concerne les cours d'informatique 1 et 2 de l'enseignement de base du département des technologies industrielles (TIN) de la HEIG-VD.

## Cours d'informatique cursus bachelor

Ce cours d'informatique à la HEIG-VD est donné par le département TIN dans les cours du cursus Bachelor en Génie Électrique. Il concerne tout particulièrement les étudiants des cours suivants&nbsp;:

- Informatique 1 (INFO1) - 101 Première année
- Informatique 2 (INFO2) - 102 Première année
- Microinformatique (MICROINFO) - 101 Première année

## Organisation de l'ouvrage

### Raccourcis clavier

Pour améliorer votre navigation sur ce site, voici quelques raccourcis clavier que vous pouvez utiliser:

* ++f++ , ++s++ , ++slash++ : Ouvre la barre de recherche
* ++p++ , ++comma++ : Va à la page précédente
* ++n++ , ++period++ : Va à la page suivante
* ++b++ : Afficher/cacher les tables des matières
* ++m++ : Afficher/cacher le menu
* ++h++ : Afficher/cacher la table des matières

### Conventions d'écriture

#### Symbole d'égalité

Nous verrons que le signe d'égalité `=` peut aisément être confondu avec l'opérateur d'affectation (également) `=` utilisé en C. Dans certains exemples où l'on montre une égalité entre différentes écritures, le signe d'égalité triple U+2261 sera utilisé pour dissiper toute ambiguïté éventuelle:

```
'a' ≡ 0b1100001 ≡ 97 ≡ 0x61 ≡ 00141
```

#### Symbole de remplissage

Dans les exemples qui seront donnés, on pourra voir `#!c while (condition) { 〰 }` ou le caractère `〰` U+3030 indique une continuité logique d'opération. Le symbole exprime ainsi `...` ([points de suspension](https://fr.wikipedia.org/wiki/Points_de_suspension) ou *ellipsis*). Or, pour ne pas confondre avec le symbole C `...` utilisé dans les fonctions à arguments variables tels que `printf`.

#### Types de données

Les conventions C s'appliquent à la manière d'exprimer les grandeurs suivantes :

- `0xABCD` pour les valeurs hexadécimales `/0x[0-9a-f]+/i`
- `00217` pour les valeurs octales `/0[0-7]+/`
- `'c'` pour les caractères `/'([^']|\\[nrftvba'])'/`
- `123` pour les grandeurs entières `/-?[1-9][0-9]*/`
- `12.` pour les grandeurs réelles en virgule flottante

#### Encodage de caractère

Il sera souvent fait mention dans cet ouvrage la notation du type U+1F4A9, il s'agit d'une notation Unicode qui ne dépend pas d'un quelconque encodage. Parler du caractère ASCII 234 est incorrect, car cela dépend de la table d'encodage utilisée; en revanche, la notation Unicode est exacte.

#### Expressions régulières

Les expressions régulières sont utilisées pour décrire des motifs de texte. Elles sont utilisées pour rechercher, remplacer ou valider des chaînes de caractères. Les expressions régulières sont utilisées dans de nombreux langages de programmation, d'outils de recherche et de traitement de texte.

Aussi dans cet ouvrage, les expressions régulières sont mises en évidence avec `/regex/`. Le lien mène au site [regex101.com](https://regex101.com/) pour tester les expressions régulières. Il vous suffit d'ajouter du texte pour tester l'exemple donné.

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

!!! exercise inline

    Exercice de réflexion pour mettre en pratique les connaissances acquises.


///

## Copyright et références

Le contenu de ce livre est sous licence [Creative Commons](https://creativecommons.org/licenses/by-sa/4.0/). Vous êtes libre de partager et d'adapter ce contenu pour toute utilisation, même commerciale, à condition de citer l'auteur et de partager vos travaux dérivés sous la même licence.

De nombreuses références et sources de ce livre sont issues de Wikipedia, de la documentation officielle de la norme C, de StackOverflow, de forums de discussion et de blogs.

## Colophon

Ce livre est écrit en [Markdown](wiki:markdown) et généré en HTML par [MkDocs](https://www.mkdocs.org/). Le thème utilisé est [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). Les sources sont disponibles sur [GitHub](wiki:github) et l'hébergement est assuré par [GitHub Pages](https://pages.github.com/).

La plupart des illustrations sont réalisées avec [Draw.io](https://www.draw.io/), un outil de dessin vectoriel en ligne. Les schémas sont rendus dans le navigateur avec `GraphViewer`. Les diagrammes utilisent la technologie [Mermaid](https://mermaid-js.github.io/mermaid/#/). Les autres sources d'images sont issues en grande partie de [Wikimedia Commons](https://commons.wikimedia.org/) et [Wikipedia](https://www.wikipedia.org/).
