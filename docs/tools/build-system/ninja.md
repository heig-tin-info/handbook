# Ninja

Ninja est un outil de build système conçu pour être rapide. Il est souvent utilisé pour compiler de gros projets C/C++ comme LLVM, Chromium ou Android. Ninja est écrit en C++ et est distribué sous licence Apache 2.0. Il a été conçu pour gérer efficacement de très gros projets, tels que **Chromium**, **LLVM** ou **Android**, où des milliers de fichiers peuvent être compilés et liés. Il a été créé en tant qu'alternative à **Make**, pour résoudre des problèmes de performance dans des scénarios de compilation à grande échelle. Ninja est particulièrement optimisé pour la **vitesse d'exécution**, en évitant de faire plus de travail que nécessaire.

L'objectif de Ninja est simple : minimiser le temps nécessaire à la **compilation incrémentale**, c'est-à-dire le temps requis pour recompiler uniquement les fichiers qui ont été modifiés ou leurs dépendances, sans avoir à recompiler tout le projet.

## Principe de fonctionnement

Ninja fonctionne avec des fichiers de build appelés `build.ninja`, qui contiennent les règles de compilation. Ces fichiers sont semblables aux `Makefile`, mais beaucoup plus simples et compacts. Voici comment fonctionne Ninja :

1. **Fichiers d'entrée simplifiés** : Ninja ne génère pas ses fichiers de configuration de manière manuelle, contrairement à Make, où les développeurs doivent souvent écrire de longs et complexes `Makefile`. Les fichiers `build.ninja` sont généralement générés par un **outil de configuration** externe (comme **CMake**, **GN** ou **Meson**).

2. **Graphes de dépendance** : Ninja crée un graphe des dépendances pour déterminer quelles parties du projet doivent être reconstruites en fonction des changements dans les fichiers source.

3. **Compilation incrémentale rapide** : Ninja détecte les fichiers modifiés et ne recompile que ce qui est nécessaire. Il optimise également le **parallélisme** en construisant plusieurs fichiers simultanément, en fonction des cœurs CPU disponibles.

4. **Pas de fonctionnalités inutiles** : Ninja se concentre uniquement sur le build. Il n’inclut pas de fonctionnalités additionnelles comme l'installation, le nettoyage (clean), etc., qui sont souvent présentes dans d'autres systèmes comme Make. Il délègue ces tâches à des outils externes.

### Avantages par rapport à Make

1. **Vitesse** : Ninja est conçu pour être **plus rapide** que Make, particulièrement pour les builds incrémentaux. Il minimise le temps de reconfiguration et de relance des builds en évitant des vérifications inutiles.

2. **Optimisation du parallélisme** : Ninja est plus efficace que Make pour tirer parti des systèmes multi-cœurs. Il calcule mieux les dépendances et s'assure que le maximum de tâches est lancé en parallèle.

3. **Simplicité des fichiers de build** : Les fichiers `build.ninja` sont simples, épurés et plus rapides à lire pour l'outil. Cela contraste avec les `Makefile`, souvent longs et difficiles à maintenir.

4. **Moins d'ambiguïté** : Ninja évite certains pièges de Make, comme la nécessité de suivre des conventions implicites. Ninja est explicite et ne laisse pas de place à des comportements ambigus.

5. **Aucun overhead de fonctionnalités inutiles** : Ninja se concentre exclusivement sur la compilation et ne se charge pas d'autres tâches comme l'installation ou le nettoyage. Cela réduit la complexité du processus de build.

6. **Build déterministe** : Ninja est conçu pour être **déterministe**, c'est-à-dire que si l'état du système est identique, le build produit sera identique, ce qui n'est pas toujours le cas avec Make.

Ci-dessous un tableau comparatif entre **Make** et **Ninja**.

Table: Comparaison entre Make et Ninja

| **Caractéristiques**        | **Make**                                            | **Ninja**                                             |
| --------------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| **Performance**             | Plus lent pour les gros projets                     | Conçu pour être extrêmement rapide                    |
| **Configuration**           | Fichiers `Makefile` manuellement écrits             | Fichiers `build.ninja` souvent générés par des outils |
| **Parallélisme**            | Support, mais moins optimisé                        | Très performant avec des builds parallèles            |
| **Complexité des fichiers** | Peut être très complexe et verbeux                  | Fichiers simples et explicites                        |
| **Objectif**                | Outil généraliste                                   | Conçu uniquement pour la compilation rapide           |
| **Gestion des dépendances** | Manuelle, souvent avec des outils externes          | Détection automatique des dépendances                 |
| **Fonctionnalités**         | Supporte des tâches additionnelles (install, clean) | Focus uniquement sur la compilation                   |

### Installation

Pour installer Ninja, il suffit de télécharger l'exécutable ou d'utiliser un gestionnaire de paquets. Par exemple :

=== "Ubuntu"

    ```bash
    sudo apt-get install ninja-build
    ```

=== "macOS"

    ```bash
    brew install ninja
    ```

=== "Windows"

    Aucune idée... À vous de chercher.

### Exemple de fichier `build.ninja`

Un fichier simple `build.ninja` pourrait ressembler à ceci :

```ninja
rule cc
  command = gcc -c $in -o $out
  description = Compiling $in

rule link
  command = gcc $in -o $out
  description = Linking $out

build foo.o: cc foo.c
build bar.o: cc bar.c
build my_program: link foo.o bar.o
```

Dans cet exemple, Ninja exécute deux étapes principales :

- **Compilation** (`cc`), qui compile les fichiers `.c` en `.o`.
- **Linkage** (`link`), qui prend les fichiers objets `.o` et les lie pour produire l'exécutable final `my_program`.

Une fois que le fichier `build.ninja` est généré, vous pouvez compiler votre projet en exécutant simplement la commande :

```bash
ninja
```

Cela lancera la compilation en fonction des règles définies dans le fichier `build.ninja`, avec des optimisations pour la compilation incrémentale et le parallélisme.
