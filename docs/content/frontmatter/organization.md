# Introduction

## À qui s'adresse cet ouvrage ?

## Organisation de l'ouvrage

Conçu comme un résumé du savoir nécessaire à l'ingénieur pour prendre en main le langage C, cet ouvrage n'est pas un manuel de référence. Il réfère à de nombreuses ressources internet et livres que le lecteur pourra consulter au besoin pour approfondir certains concepts.

Chaque chapitre est composé d'exercices, mais à des fins pédagogiques, toutes les solutions ne sont pas données. Certains exercices sont destinés à être faits en études.

Cet ouvrage est destiné à des étudiants ingénieurs de première année n'ayant aucune expérience en programmation.

Le contenu concerne les cours d'informatique 1 et 2 de l'enseignement de base du département des technologies industrielles (TIN) de la HEIG-VD.

## Raccourcis clavier

Pour améliorer votre navigation sur ce site, voici quelques raccourcis clavier que vous pouvez utiliser :

* ++f++ , ++s++ , ++slash++ : Ouvre la barre de recherche
* ++p++ , ++comma++ : Va à la page précédente
* ++n++ , ++period++ : Va à la page suivante
* ++b++ : Afficher/cacher les tables des matières
* ++m++ : Afficher/cacher le menu
* ++h++ : Afficher/cacher la table des matières

## Conventions d'écriture

### Symbole d'égalité

Nous verrons que le signe d'égalité `=` peut aisément être confondu avec l'opérateur d'affectation (également) `=` utilisé en C. Dans certains exemples où l'on montre une égalité entre différentes écritures, le signe d'égalité triple  (`U+2261`) sera utilisé pour dissiper toute ambiguïté éventuelle :

```
'a' ≡ 0b1100001 ≡ 97 ≡ 0x61 ≡ 00141
```

### Symbole de remplissage

Dans les exemples qui seront donnés, on pourra voir `while (condition) { 〰 }` ou `〰` (`U+3030`) indique une continuité logique d'opération. Le symbole exprime ainsi `...` ([points de suspension](https://fr.wikipedia.org/wiki/Points_de_suspension) ou *ellipsis*). Or, pour ne pas confondre avec le symbole C `...` utilisé dans les fonctions à arguments variables tels que `printf`.

### Types de données

Les conventions C s'appliquent à la manière d'exprimer les grandeurs suivantes :

- `0xABCD` pour les valeurs hexadécimales (`/0x[0-9a-f]+/i`)
- `00217` pour les valeurs octales (`/0[0-7]+/`)
- `'c'` pour les caractères (`/'([^']|\\[nrftvba'])'/`)
- `123` pour les grandeurs entières (`/-?[1-9][0-9]*/`)
- `12.` pour les grandeurs réelles en virgule flottante

### Encodage de caractère

Il sera souvent fait mention dans cet ouvrage la notation du type `U+01AE`, il s'agit d'une notation Unicode qui ne dépend pas d'un quelconque encodage. Parler du caractère ASCII 234 est incorrect, car cela dépend de la table d'encodage utilisée; en revanche, la notation Unicode est exacte.

### Encadrés

Des encadrés sont utilisés pour mettre en avant des informations complémentaires ou des astuces. Ils sont également utilisés pour donner des informations sur des concepts avancés ou des détails techniques.

!!! info

    Ceci est un encadré d'information.

!!! warning

    Point important à retenir.

!!! danger

      Attention

!!! example

    Exemple à suivre.

!!! note

    Corollaire à retenir.

!!! tip

    Astuce pour faciliter la compréhension.

!!! exercise

    Exercice à faire.
