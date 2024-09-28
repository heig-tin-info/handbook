# Deployement

## Semantic Versioning

La version d'un logiciel est un numéro qui permet d'identifier une version spécifique d'un logiciel. La version est généralement composée de trois nombres séparés par des points, par exemple `1.2.3`. La première partie est le numéro de version majeure, la deuxième partie est le numéro de version mineure et la troisième partie est le numéro de version de correctif.

Le site [semver.org](https://semver.org/) propose des recommandations pour la numérotation des versions de logiciels.

## Changelog

Un *changelog* prend souvent la forme d'un fichier texte ou Markdown qui liste les modifications apportées à un projet. Il est généralement inclus dans le dépôt du projet et est utilisé pour informer les utilisateurs des mises à jour et des nouvelles fonctionnalités. L'objectif est de pouvoir informer les utilisateurs des changements lié à une nouvelle version du logiciel.

L'excellent site [Keep a Changelog](https://keepachangelog.com/) propose des recommandations pour la rédaction de *changelog*. On peut notament y lire :

- Un changelog est un fichier qui contient une liste épurée, chronologique des changements apportés à chaque version d'un projet.
- Il facilite la vie des utilisateurs et contributeurs en permettant de voir les changements notables entre chaque version.

### Catégories

Les catégories recommandées pour un *changelog* sont les suivantes :

- `Added` pour les nouvelles fonctionnalités.
- `Changed` pour les modifications de fonctionnalités existantes.
- `Deprecated` pour les fonctionnalités obsolètes qui seront supprimées dans les prochaines versions.
- `Removed` pour les fonctionnalités supprimées.
- `Fixed` pour les corrections de bugs.
- `Security` pour les correctifs de sécurité.

### Nom du fichier

La recommandation est de nommer votre fichier `CHANGELOG.md` ou `CHANGELOG.txt` et de le placer à la racine de votre dépôt, certains le nomment également `HISTORY`, `NEWS` ou `RELEASES`.

### Exemple

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- v1.1 German Translation

### Changed

- Internal socket connection now use `libuv` instead of native bindings.
- Use extended precision for matrix calculations (#358).

### Removed

- SSOT attribute in `User` model, `age` can be calculated from birthdate.

## [1.1.1] - 2023-03-05

### Added

- Arabic translation (#444).
- Centralize all links into `/data/links.json` so they can be updated easily.

### Fixed

- Rounding error in algorithm for `tan()` function (#442).
- Typo in the French translation (#443).

### Changed

- Upgrade dependencies to use `sdl2` for better performance.

### Removed

...

## [1.1.0] - 2019-02-15

...
```
