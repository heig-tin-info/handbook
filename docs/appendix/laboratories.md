# Laboratoires

Les laboratoires sont des travaux pratiques permettant à l'étudiant d'attaquer des problèmes de programmation plus difficiles que les exercices faits en classe.

## Protocole

1. Récupérer le référentiel du laboratoire en utilisant GitHub Classroom.
2. Prendre connaissance du cahier des charges.
3. Rédiger le code.
4. Le tester.
5. Rédiger votre rapport de test si demandé.
6. Le soumettre avant la date butoir.

## Évaluation

Une grille d'évaluation est intégrée à tous les laboratoires. Elle prend la forme d'un fichier `criteria.yml` que l'étudiant peut consulter en tout temps.

## Directives

- La recherche sur internet est autorisée et conseillée.
- Le plagiat n'est pas autorisé, et sanctionné si découvert par la note de 1.0.
- Le rendu passé la date butoir est sanctionné à raison de 1 point puis 1/24 de point par heure de retard.

## Format de rendu

- Fin de lignes: `LF` (`'\n'`).
- Encodage: UTF-8 sans BOM.
- Code source respectueux de ISO/IEC 9899:1999.
- Le code doit comporter un exemple d'utilisation et une documentation mise à jour dans `README.md`.
- Lorsqu'un rapport est demandé, vous le placerez dans `REPORT.md`.

## Anatomie d'un travail pratique

Un certain nombre de fichiers vous sont donnés, il est utile de les connaître. Un référentiel sera généralement composé des éléments suivants :

```text
$ tree
.
├── .clang-format
├── .devcontainer
│   ├── Dockerfile
│   └── devcontainer.json
├── .editorconfig
├── .gitattributes
├── .gitignore
├── .vscode
│   ├── launch.json
│   └── tasks.json
├── Makefile
├── README.md
├── assets
│   └── test.txt
├── foo.c
├── foo.h
├── main.c
├── criteria.yml
└── tests
    ├── Makefile
    └── test_foo.c
```

### README.md

Il s'agit de la documentation principale de votre référentiel. Elle contient la donnée du travail pratique en format Markdown. Ce fichier est également utilisé par défaut dans GitHub. Il contient notamment le titre du laboratoire, la durée, le délai de rendu et le format individuel ou de groupe :

```markdown
# Laboratoire <!-- omit in toc -->
- **Durée**: 2 périodes + environ 3h à la maison
- **Date de rendu**: dimanche avant minuit
- **Format**: travail individuel
...
```

### criteria.yml

Ce fichier contient les directives d'évaluation du travail pratique. Il est au format YAML. Pour chaque point évalué une description est donnée avec la clé `description` et un nombre de points est spécifié. Une exigence peut avoir soit un nombre de points positifs soit négatifs. Les points négatifs agissent comme une pénalité. Ce choix d'avoir des points et des pénalités permet de ne pas diluer les exigences au travers d'autres critères importants, mais normalement respectés des étudiants.

Des points bonus sont donnés si le programme dispose d'une aide et d'une version et si la fonctionnalité du programme est étendue.

```yaml
# Critères d'évaluation du travail pratique
%YAML 1.2
---
tests:
    build:
        description: Le programme compile sans erreurs ni warning
        points: 0/-4
        test: test_build
    unit-testing:
        function_foo:
        points: 0/10
        test: test_foo
        function_bar:
        points: 0/10
        test: test_bar
    functional-testing:
        arguments:
        description: La lecture des arguments fonctionne comme demandé
        points: 0/7
        test: test_arguments
        output-display:
        description: Affichage sur stdout/stderr comme spécifié
        points: 0/3
        test: test_output
        errors:
        description: Le programme affiche des erreurs si rencontrées
        points: 0/2
        test: test_errors
report:
    introduction:
        description: Le rapport de test contient une introduction
        points: 0/2
    conclusion:
        description: Le rapport de test contient une conclusion
        points: 0/2
    analysis:
        description: Le rapport de test contient une analyse du comportement
        points: 0/3
code:
    specifications:
        prototypes:
            description: Les prototypes des fonctions demandées sont respectés
            points: 0/3
        main:
            description: Le programme principal est minimaliste
            points: 0/3
        algorithm:
            description: L'algorithme de encode/decode est bien pensé
            points: 0/5
    comments:
        header:
        description: Un en-tête programme est clairement défini
        points: 0/2
        purpose:
        description: Les commentaires sont pertinents
        points: 0/-2
        commented-code:
        description: Du code est commenté
        points: 0/-2
    variables:
        naming:
        description: Le noms des variables est minimaliste et explicite
        points: 0/2
        scope:
        description: La portée des variables est réduite au minimum
        points: 0/2
        type:
        description: Le type des variables est approprié
        points: 0/2
    functions:
        length:
        description: La longueur des fonctions est raisonnable
        points: 0/-4
    control-flow:
        description: Les structures de contrôle sont appropriées
        points: 0/4
    overall:
        dry:
        description: Pas de répétition dans le code
        points: 0/-5
        kiss:
        description: Le code est minimaliste et simple
        points: 0/-5
        ssot:
        description: Pas de répétition d'information
        points: 0/-5
        indentation:
        description: L'indentation du code est cohérente
        points: 0/-5
bonus:
    help:
        description: Le programme dispose d'une aide
        bonus: 0/1
        test: test_help
    version:
        description: La version du programme peut être affichée
        bonus: 0/1
        test: test_version
    extension:
        description: La fonctionnalité du programme est étendue
        bonus: 0/3
    english:
        description: Usage de l'anglais
        bonus: 0/1
```

Ce fichier est utilisé par des tests automatique pour faciliter la correction du travail pratique.
