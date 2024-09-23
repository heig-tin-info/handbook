# CMake

## Introduction

CMake, créature singulière dans l’univers du développement logiciel, est un outil de compilation destiné à automatiser et simplifier la génération des fichiers de configuration nécessaires à la compilation d’un projet. Né à la fin des années 1990, à l’époque où la prolifération des systèmes d’exploitation et des plateformes matérielles complexifiait le processus de construction des logiciels, CMake s’inscrit dans une quête pragmatique : rendre le développement multi-plateformes plus fluide et plus unifié.

À une époque où les systèmes de build comme Make étaient omniprésents, ces outils étaient souvent très spécifiques à un système particulier, et les développeurs devaient écrire des fichiers de configuration différents pour chaque environnement. CMake a donc été conçu par Kitware, avec pour objectif de générer des fichiers de build qui pourraient s’adapter à différents compilateurs et plateformes sans avoir à réécrire manuellement de nombreuses configurations. Ce besoin est apparu principalement dans le cadre de projets de grande envergure, tels que les logiciels scientifiques ou industriels, qui devaient tourner aussi bien sur des systèmes Unix que sur Windows ou encore macOS.

Dès ses débuts, CMake s’est imposé comme une solution de configuration multi-plateforme flexible. Son avantage par rapport à ses concurrents réside dans sa capacité à générer des fichiers de construction adaptés aux environnements variés, que ce soit pour Make, Ninja, ou encore des outils spécifiques à Visual Studio. Cette abstraction permet de s’affranchir de l'écriture manuelle de fichiers de build complexes pour chaque plateforme.

Comparé à ses concurrents directs comme **Autotools**, CMake brille par sa relative simplicité à prendre en main et à configurer des projets multi-systèmes, tout en restant assez puissant pour s’adapter à des projets de grande envergure. Contrairement à des outils plus anciens, il se concentre sur l'abstraction du processus de construction et permet de gérer plus facilement les dépendances externes et internes d'un projet. En cela, CMake surpasse souvent les systèmes de build traditionnels par sa flexibilité.

Cependant, s’il possède un net avantage pour un projet complexe et multi-plateforme, il souffre aussi de certains travers. Et c’est ici que les développeurs grimacent souvent.

## Une syntaxe austère et rebutante

L’un des reproches les plus fréquents adressés à CMake est sa syntaxe. Elle est souvent décrite comme austère, voire "immonde", pour reprendre l’expression que beaucoup lui prêtent dans des cercles de développeurs chevronnés. La langue de CMake est une sorte de dialecte dérivé d’une forme rudimentaire de script, mais dont la lisibilité et la clarté laissent à désirer.

Prenons par exemple un fichier typique de configuration, appelé `CMakeLists.txt`. Ce fichier est une séquence de directives qui sont interprétées pour générer les fichiers de build. Voici un exemple minimaliste :

```cmake
cmake_minimum_required(VERSION 3.15)
project(MonProjet LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(SOURCES main.cpp util.cpp)

add_executable(MonExecutable ${SOURCES})
```

À première vue, il peut sembler relativement simple. Mais lorsqu’on plonge dans un projet plus conséquent, la syntaxe devient rapidement verbeuse et dénuée de la concision ou de l’élégance syntaxique qu’on pourrait espérer dans un langage de configuration moderne. Les fonctions sont souvent longues et les macros omniprésentes, rendant difficile le débogage et la maintenance d’un script CMake complexe.

Comparé à des outils modernes comme **Meson**, qui se veut plus concis et plus explicite, CMake trahit son origine dans les années 1990. Il conserve un certain bagage historique, une sorte de legacy syntaxique qui, à défaut d’être intuitive, a tout de même l’avantage d’être éprouvée et très bien documentée.

## Exemple

L'utilisation de CMake, bien que légèrement déroutante au départ, suit des principes relativement simples. Voici comment se déroule typiquement le processus :

1. **Écrire le fichier `CMakeLists.txt`** : Ce fichier contient les instructions qui décrivent les sources, les dépendances, les bibliothèques, et d’autres options de configuration.

2. **Générer les fichiers de build** :

    Depuis la ligne de commande, vous exécutez une commande comme :

    ```bash
    cmake -S . -B build
    ```

    Cela crée un répertoire `build` où sont placés les fichiers de configuration pour l’outil de construction choisi (Make, Ninja, etc.).

3. **Compiler le projet** :

    Vous pouvez alors exécuter :

    ```bash
    cmake --build build
    ```

    Et CMake utilisera les fichiers générés pour compiler votre projet.

4. **Facilité de gestion des dépendances** :

    L’un des atouts majeurs de CMake réside dans sa gestion des dépendances via `find_package()`, qui permet de détecter et lier automatiquement les bibliothèques externes.

Par exemple, si vous voulez lier votre projet à **Boost**, vous pouvez simplement ajouter ceci dans votre `CMakeLists.txt` :

```cmake
find_package(Boost 1.75 REQUIRED)
target_link_libraries(MonExecutable Boost::Boost)
```

C’est cette capacité à manipuler aisément des dépendances complexes qui a permis à CMake de supplanter d’autres systèmes.

## Conclusion

En définitive, CMake incarne un compromis délicat entre flexibilité et simplicité. Né d’un besoin impérieux de rationaliser la compilation multi-plateforme, il a su s’imposer comme une référence malgré ses imperfections syntaxiques. Si sa syntaxe déplait à beaucoup et peut rebuter au premier abord, il n’en reste pas moins que ses capacités à gérer des projets d’envergure, à s’adapter à une multitude de systèmes et à orchestrer la compilation de manière automatisée en font un outil indispensable dans le paysage actuel du développement logiciel.

Un outil imparfait, certes, mais indéniablement efficace dans sa mission.