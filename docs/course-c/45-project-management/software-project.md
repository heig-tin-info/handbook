# Organisation d'un projet

## Introduction

Dans ce chapitre, nous allons voir comment organiser un projet logiciel. Nous allons voir comment structurer un projet, comment gérer les dépendances, comment gérer les tests unitaires et comment gérer les tests fonctionnels.

## Structure d'un projet

La structure d'un projet logiciel est un élément important pour sa maintenabilité. Une bonne structure permet de retrouver facilement les fichiers sources, les fichiers d'en-tête, les tests, etc.

Si votre projet est accessible par d'autres développeurs, il y a certaines conventions à respecter pour que tout le monde puisse s'y retrouver.

Tout commence avec un dossier racine. Ce dossier racine contient tous les fichiers sources, les fichiers d'en-tête, les tests, les dépendances, etc. Encore faut-il bien nommer ce projet. Un nom de projet doit être court, explicite et unique. Il est recommandé de ne pas utiliser d'espaces, de caractères spéciaux ou de majuscules.

!!! note "Les Majuscules"
    Les noms de fichiers et de dossiers sont sensibles à la casse sur les systèmes POSIX mais pas sous Windows. Cela crée certains problèmes de compatibilité entre les systèmes d'exploitation.

    D'autre part, l'usage des majuscules peut créer des ambiguïtés. Par exemple, `NomDuFichier` et `nomdufichier` sont deux noms différents. Comment allez-vous expliquer par téléphone à un collègue que le fichier s'écrit de cette manière ? L'ennui c'est les acronymes. Par exemple, `XMLParser`, `XmlParser` ou `XMLparser` ? Vous aurez tendance à choisir la troisième solution pour que `XML` ressort bien mais vous êtes incohérent puisque vous avez pas utilisé de majuscul pour `Parser`.

    Le problème est bien résolu avec l'utilisation d'underscores ou de tirets (notation kekbab-case ou snake_case). Par exemple, `xml_parser` est plus lisible et plus facile à expliquer.

    Une convention en voque est de nommer les fichiers en minuscules et d'utiliser des tirets pour séparer les mots. Par exemple, `xml-parser`. C'est la convention utilisée sur GitHub pour le nom des dépôts.

Voici une structure de projet classique :

```text
projet/
├── src/
│   ├── main.c
│   ├── foo.c
│   └── bar.c
├── include/
│   ├── foo.h
│   └── bar.h
├── tests/
│   ├── test_foo.c
│   └── test_bar.c
├── Makefile
└── README.md
```

Le point d'entrée pour le développeur c'est le fichier `README.md`. Ce fichier contient une description du projet, des instructions pour l'installation, des instructions pour la compilation, des instructions pour les tests, etc.

### README.md

Jadis, le fichier `README` était un fichier texte simple. Aujourd'hui, c'est un fichier `Markdown`. Le `Markdown` est un langage de balisage léger créé en 2004 par John Gruber et Aaron Swartz. Il est facile à lire et à écrire. Il est utilisé sur de très nombreux supports: GitHub, GitLab, Bitbucket, Reddit, Stack Overflow, etc. C'est d'ailleurs le format utilisé pour rédiger cet ouvrage.

Voici un exemple de fichier `README.md` :

```markdown
# Nom du Projet

Description du projet.

## Installation

Comment installer le projet :

```bash
git clone http://...
cd projet
make
```

## Utilisation

Comment utiliser le projet :

```bash
./projet
```

Le fichier `README.md` est un fichier important. Il doit être à jour et bien rédigé car c'est la première chose que l'on voit lorsqu'on arrive sur le dépôt du projet. Il doit permettre à l'utilisateur rapidement :

1. Que fait le projet et quelle est son utilité ?
2. Est-ce que ce projet est fait pour moi ?
3. Comment l'installer ?
4. Comment l'utiliser ?
5. Comment contribuer ?

### Dotfiles

Dans un système POSIX, les fichiers commençant par un point sont des fichiers cachés. C'est une convention utilisée pour les fichiers de configuration. Ces fichiers sont appelés `dotfiles`.

On va trouver toute une panoplie de fichiers de configuration dans un projet logiciel tel que :

- `.gitignore` : liste des fichiers à ignorer par Git.
- `.editorconfig` : conventions de codage pour les éditeurs de texte.
- `.github/` : dossier contenant l'intégration continue, les actions GitHub, etc.
- `.env` : variables d'environnement pour le projet.

### Makefile

Le `Makefile` est un fichier de configuration pour le programme `make`. C'est généralement le point d'entrée pour construire un projet. Si vous trouvez un `Makefile`, vous savez que vous pourrez très probablement simplement utiliser la commande `make` pour construire le projet.

Néanmoins, parfois le `Makefile` n'est pas suffisant car votre projet est plus complexe et dépend de plusieurs bibliothèques tierces qui peuvent être fastidieuses à installer. C'est là qu'interviennent les gestionnaires de dépendances que nous verrons plus tard.

Alternativement, on peut trouver simplement un script `build.sh` ou `build.bat` pour construire le projet que vous appelerer avec `./build.sh` ou `.\build.bat`.

### Organisation des fichiers sources

Lorsque le projet dépasse 5 à 10 fichiers, il est habituel de les déplacer dans un dossier pour ne pas encombrer la racine du projet. On crée un dossier `src` pour les fichiers sources qui va contenir tous les fichiers `.c`.

Faut-il séparer les fichiers sources des fichiers d'en-tête ? C'est une question de goût. Certains développeurs préfèrent tout mettre dans un seul dossier `src` pour simplifier la navigation. D'autres préfèrent séparer les fichiers sources des fichiers d'en-tête. Cela permet de mieux organiser le projet et de mieux gérer les dépendances. Il n'y a pas de consensus établi mais on peut noter plusieurs points.

Lorsqu'un projet est destiné à devenir une bibliothèque partagée, vous devez fournir les fichiers d'en-tête pour que les autres développeurs puissent utiliser votre bibliothèque. S'ils sont séparés, c'est plus facile de les extraire et les distribuer.

Néanmoins, séplacer les fichiers d'en-tête dans un dossier `include` nécessite d'informer le compilateur de l'emplacement des fichiers d'en-tête. C'est généralement fait avec l'option `-I` de GCC :

```bash
gcc -Iinclude -c src/*.c
```

### Répertoire de construction

Lorsque vous compilez un projet, vous allez générer des fichiers intermédiaires (fichiers objets) et des fichiers finaux (exécutables, bibliothèques). Selon le projet il peut y avoir beaucoup de fichiers. Afin d'éviter de ne voir ces fichiers dans votre explorateur de fichiers, on crée un dossier `build` pour les stocker.

Ceci est une convention. Vous pouvez choisir un autre nom pour ce dossier. Par exemple, `bin`, `out`, `dist`, etc.

Néanmoins, il faut d'une part penser à ajouter ce dossier dans le `.gitignore` pour ne pas le versionner, mais également modifier la configuration de votre compilateur pour qu'il place les fichiers objets dans ce dossier :

```bash
mkdir -p build
gcc -Iinclude -c src/*.c -o build/*.o
```

## En-têtes de fichiers

Historiquement, les développeurs C utilisait l'outil [Doxygen](wiki:doxygen) pour générer de la documentation à partir des commentaires dans le code source. Cela a donné naissance à une convention pour les commentaires de documentation qui est souvent utilisée de manière abusive.

Aujourd'hui, avec les éditeurs modernes, il est plus facile de naviguer dans le code source et de trouver des informations sur les fonctions et les structures. Les commentaires de documentation sont souvent redondants et inutiles, ils polluent plus qu'ils n'aident. Néanmoins, je peux vous donner un exemple de commentaires de documentation pour un fichier d'en-tête :

```c
/**
 * @brief Définition des fonctions pour manipuler des nombres
 * @file numbers.h
 * @date 2024-09-01
 * @author John Doe
 * @version 1.0
 * @copyright Copyright (c) 2021
 *
 * Description détaillée.
 */

/*********************************************************/
/*                       INCLUDES                        */
/*********************************************************/
#include <stdio.h>

/*********************************************************/
/*                       STRUCTURES                      */
/*********************************************************/
typedef struct point {
    int x; //!< Abscisse du point.
    int y; //!< Ordonnée du point.
} Point; //!< Structure point.

/*********************************************************/
/*                       FONCTIONS                       */
/*********************************************************/

/**
 * @brief Fonction d'addition de deux entiers.
 * @param a Premier entier.
 * @param b Deuxième entier.
 * @return La somme des deux entiers.
 *
 * Cette fonction permet d'additionner deux entiers.
 */
int add(int a, int b) {
    return a + b;
}

/*********************************************************/
/*                       FIN                             */
/*********************************************************/
```

Nous pouvons maintenant discuter de la pertinence de ces commentaires. Intéressons-nous tout d'abord à l'en-tête du fichier :

`@file`

: Le nom du fichier est en redondance avec le vrai nom du fichier. Si vous renommez le fichier, vous devrez également changer ce commentaire. C'est d'une part une source d'erreur mais surtout pour Git, cela implique que le fichier n'est pas simplement renommé mais supprimé et recréé. Cela peut poser des problèmes de fusion et d'accès à l'historique. Aussi, si vous utilisez Git, cette information est parfaitement inutile.

`@date`

: La date est inutile car si vous avez besoin de la date, vous pouvez utiliser Git pour voir la date de la dernière modification du fichier. D'autre part, il est courant qu'un fichier soit modifié sans que la date soit mise à jour. Cela peut être une source de confusion.

`@author`

: Si vous utilisez Git, vous possédez déjà cette information et de manière beaucoup plus fine. Vous pouvez voir qui a modifié chaque ligne du fichier. Gérer cette information dans le fichier c'est également s'astreindre à ajouter son nom, même si vous n'avez ajouté qu'une ligne. Et puis, si vous aimez tant le fichier que vous venez tant à le modifier que vous avez changé toutes les lignes, devez-vous supprimer le nom du vrai auteur pour mettre le vôtre ? C'est une source de conflit, est c'est beaucoup plus simple de laisser Git gérer cette information.

`@version`

: Même rengaine et même punition. Si vous utilisez Git, vous avez déjà cette information. Git gère les version avec les tags et les branches. Vous pouvez voir l'historique des modifications et les différences entre les versions. D'autre part, pour les même raisons qu'évoquées, à chaque nouvelle version de votre projet, vous devez modifier ce commentaire dans tous les fichiers. Cela implique que tous ces fichiers vont changer et vous allez vous perdre dans l'historique.

`@brief`

: Enfin une information utile. C'est une excellente pratique que d'avoir une description courte du fichier. Néanmoins avec Doxygen il existe l'option `JAVADOC_AUTOBRIEF` qui permet de générer automatiquement le `@brief` à partir de la première phrase du commentaire si elle se termine par un point. C'est une option à activer pour éviter de répéter la même chose.

`@copyright`

: C'est une information importante. Elle permet de savoir comment le fichier peut être utilisé. Néanmoins, il est rare que pour un projet donné, le copyright et la licence changent d'un fichier à l'autre, il est donc plus judicieux de mettre cette information dans le `README` ou mieux dans un fichier `LICENSE`.

Maintenant que nous avons balayé l'en-tête, concentrons-nous sur la fonction `add`. Cette fonction fait 3 lignes et le commentaire 8 lignes. Est-ce réellement nécessaire de documenter une fonction que tout le monde peut comprendre ?

La réponse n'est pas si simple. Si vous publier le code source avec votre bibliothèque, la réponse est non car n'importe qui pourra la comprendre. Néanmoins votre bibliothèque est publiée sans le code source, la seule chose que votre utlisateur aura c'est le fichier d'en-tête (`.h`) :

```c
int add(int a, int a);
```

C'est peut-être un peu court et un complément d'information pourrait être utile. Mais faut-il documenter tous les paramètres ? Si le *brief* dit que la fonction additionne deux entiers, et que vous avez accès aux types des paramètres, est-ce vraiment nécessaire de documenter les paramètres ? La réponse est non. Je le répète souvent, un commentaire est fait pour expliquer le pourquoi, pas le comment. Si vous avez besoin de documenter le comment, c'est que votre code n'est pas assez clair. On pourrait par exemple réécrire la fonction de la manière suivante :

```c
int add_two_integers_together(int first, int second) {
    return first + second;
}
```

Je vous l'accorde, c'est un peu long, mais ça à le mérire d'être parfaitement clair.

Questionnons maintenant les séparateurs de contenu. Lorsque vous débutez en programmation, vous avez tendance à vous faire mousser un peu en écrivant plus que le nécessaire, écrire des commentaires c'est sans risque et cela rallonge votre beau programme. Alors pour bien structurer votre code, vous avez mis des séparateurs de contenu. Néanmoins ils n'apportent pas grand chose. En Python par exemple, la norme propose d'ajouter deux retour à la ligne entre chaque fonction. C'est une convention qui est largement suffisante pour séparer les différents éléments du code.

Enfin, la dernière question est de savoir si le commentaire de la structure `Point` est utile. Pour cette structure qui est très simple, on pourrait se passer de commentaires, mais dans le cas ou les éléments nécessitent d'être expliqués, c'est la notation Doxygen qui peut être discutée.

Doxygen utilise la notation `#!c //!` pour les commentaires de documentation. C'est une notation spéciale qui a la facheuse tendance s'afficher en rouge vif dans certains éditeurs de texte. Si vous n'utilisez pas Doxygen, il est préférable de ne pas utiliser cette notation. Il est préférable de rester sur la notation `#!c //` qui est plus universelle.

Après ces longues explications, je vous propose de vous redonner l'exemple simplifié :

```c
/**
 * Définition des fonctions pour manipuler des nombres
 *
 * Description détaillée.
 */
#include <stdio.h>

typedef struct point {
    int x; //!< Abscisse du point.
    int y; //!< Ordonnée du point.
} Point; //!< Structure point.

int add_two_integers(int a, int b) {
    return a + b;
}
```

!!! info "Le commentaire de trop"

    ```c
    /*********************************************************/
    /*                    FIN DU FICHIER                     */
    /*********************************************************/
    ```

    Diable ! Pourquoi trouve-t-on toujours un commentaire `FIN` à la fin des fichiers ? C'est une pratique qui remonte à l'époque des cartes perforées. Les cartes perforées étaient utilisées pour stocker les programmes. Chaque carte avait un numéro de ligne et un numéro de colonne. Pour éviter de mélanger les cartes, on mettait un commentaire `FIN` à la fin de chaque carte. C'est une pratique ancestrale qui a perduré jusqu'à aujourd'hui. Les développeurs répètent inlassablement ces habitudes sans toutefois les remettre en question.

    Aujourd'hui, un fichier est fini au sens que lorsqu'on en atteint la fin, on le sait. Il n'est alors pas pertinent de le préciser.

    C'est un peu la même chose que ces pages dans les livres laissées blanches, ou presque, avec un commentaire *"Cette page a été intentionnellement laissée blanche"* qui remontait à l'époque de l'impression en offset. Lorsqu'on imprimait un livre, on imprimait les pages par feuille de 16 pages. Si le livre faisait 200 pages, il fallait ajouter 4 pages blanches à la fin pour que l'impression soit correcte. Aujourd'hui, les livres sont imprimés en numérique et il n'y a plus besoin de ces pages blanches.

## Gestion de configuration

La gestion de configuration est un élément important pour un projet logiciel. Elle permet de stocker des informations qui peuvent varier d'un environnement à un autre. Par exemple, les informations de connexion à une base de données, les clés d'API, les adresses IP, etc.

Il existe plusieurs solutions pour gérer la configuration d'un projet :

- Les variables d'environnement.
- Les fichiers de configuration.

### Variables d'environnement

Les variables d'environnement sont des variables stockées dans l'environnement d'exécution d'un programme. Elles sont accessibles par le programme et peuvent être modifiées par l'utilisateur. Ces variables sont propagées à tous les processus enfants pour autant qu'elles ait été exportées. Elles peuvent être utile dans un projet pour stocker des informations sensibles qui ne devraient pas être versionnées.

Prenons l'exemple d'une clé d'API. Cette clé vous permet d'accéder à un service tiers depuis votre programme. Chaque utilisateur de votre programme doit avoir sa propre clé d'API. Si vous stockez cette clé dans le code source, vous risquez de la versionner et de la rendre publique. Si vous stockez cette clé dans un fichier de configuration, vous risquez de le versionner et de le rendre public également. Une bonne solution est de stocker cette clé dans une variable d'environnement.

Il se peut d'ailleurs que votre projet nécessite plusieurs variables d'environnement. On utilise couramment un fichier `.env.example` pour lister les variables d'environnement nécessaires au projet. Ce fichier est versionné et contient des valeurs par défaut. L'utilisateur doit copier ce fichier en `.env` et renseigner les valeurs.

```bash title=".env.example"
API_KEY=your_api_key
DATABASE_URL=your_database_url
```

```bash title=".env"
API_KEY=1234567890
DATABASE_URL=postgres://user:password@localhost:5432/database
```

Pour déployer votre environnement de développement, vous devez exporter ces variables d'environnement. Vous pouvez le faire dans votre terminal ou dans un fichier de configuration de votre terminal (`.bashrc`, `.zshrc`, etc.).

```bash
export $(cat .env | xargs)
```

Sous Windows vous pouvez utiliser la commande `set` :

```cmd
for /f "delims== tokens=1,2" %i in (.env) do set %i=%j
```

Ces commandes sont généralement intégrées dans un script `start.sh` ou `start.bat` pour démarrer votre projet, ou alors directement dans le `Makefile`.

### Fichier d'en-tête

On trouve très souvent dans un projet C un fichier d'en-tête `.h` qui contient des définitions de configuration. Par exemple, un fichier `config.h` qui contient des constantes, des macros, des structures, etc.

```c
#ifndef CONFIG_H
#define CONFIG_H

#define VERSION "1.0.0"
#define AUTHOR "John Doe"

#define USE_FEATURE_A
#define USE_FEATURE_B

#define API_KEY "your_api_key"
#define DATABASE_URL "your_database_url"
```

Ce fichier est inclus dans les fichiers sources qui ont besoin de ces informations. Il est versionné et donc ne devrait pas contenir d'informations sensibles. Si vous avez des informations sensibles, vous pouvez les stocker dans un fichier `.env` et les exporter dans les variables d'environnement. Ces variables peuvent être utilisée dans votre Makefile pour déclarer des variables de compilation.

```makefile
include .env

CFLAGS += -DAPI_KEY=\"$(API_KEY)\"
CFLAGS += -DDATABASE_URL=\"$(DATABASE_URL)\"
```
