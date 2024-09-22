# Compilateur C/C++

Compiler un programme en C ou en C++ requiert un compilateur. Il s'agit d'un **programme** qui permet de traduire le code source en langage C ou C++ en un **fichier objet** (extension `.o` ou `.obj`), ou un **fichier exécutable** (extension `.exe` sous Windows ou sans extension dans un système POSIX).

Le compilateur le plus utilisé pour le C est `gcc` (GNU Compiler Collection) et pour le C++ est `g++`. Ces deux compilateurs sont inclus dans la suite logicielle `gcc`. Pour installer `gcc` sous Ubuntu, il suffit de taper la commande suivante dans un terminal :

```bash
sudo apt-get install build-essential
```

Sous Windows, c'est plus compliqué. GCC étant un logiciel prévu pour un système POSIX, il n'est pas directement compatible avec Windows. Il existe cependant des ports de GCC pour Windows, comme [MinGW](http://www.mingw.org/), [Cygwin](https://www.cygwin.com/) ou [MSYS2](https://www.msys2.org/). Ces ports permettent d'installer GCC sur Windows, mais il est plus élégant et plus pratique d'utiliser WSL si les applications que vous développez sont destinées à vos études et ne seront pas distribuées à des utilisateurs Windows.

Si vous souhaitez compiler sous Windows avec un compilateur Windows, vous pouvez utiliser [Visual Studio](https://visualstudio.microsoft.com/) qu'il ne faut pas confondre avec Visual Studio Code. Visual Studio est un IDE complet qui inclut un compilateur C/C++. Ce compilateur nommé `cl` est un compilateur propriétaire de Microsoft. Il est inclus dans Visual Studio et n'est pas disponible séparément. Ce compilateur ne respecte pas toujours le standard C (ISO/IEC 9899) mais couvre presque en totalité la norme C++ (ISO/IEC 14882).

## Cycle de compilation

La compilation requiert plusieurs étapes :

1. **Prétraitement** : Le préprocesseur remplace les macros par leur définition, inclut les fichiers d'en-tête, etc.
2. **Compilation** : La compilation converti le code source en assembleur.
3. **Assemblage** : L'assembleur converti le code assembleur en code objet, il lie les bibliothèques statiques et résoud les adresses des fonctions externes.
4. **Édition de liens** : Le lien édite les fichiers objets pour créer un fichier exécutable.

Chacune de ces étapes peut être réalisée séparément. Par exemple, pour compiler un programme en C, il est possible de générer le fichier objet sans l'éditer de liens. Cela permet de gagner du temps lors du développement, car seule la partie modifiée du code est recompilée:

```bash
# Génère un fichier C
$ cat > main.c <<EOF
#include <stdio.h>
int main() {
    printf("hello, world!\n");
}
EOF

# Étape de préprocesseur
$ gcc -E main.c -o main.i

# Étape de compilation
$ gcc -S main.i -o main.s

# Étape d'assemblage
$ gcc -c main.s -o main.o

# Étape d'édition de liens
$ gcc main.o -o main
```

## Compilation séparée

La compilation séparée est une technique de développement qui consiste à compiler chaque fichier source séparément. Cela permet de réduire le temps de compilation lors du développement, car seuls les fichiers modifiés sont recompilés. Cela permet également de réduire la taille des fichiers objets, car les fonctions non utilisées ne sont pas incluses dans le fichier objet.

```bash
# Génère un fichier C
$ cat > main.c <<EOF
#include "add.h"
#include <stdio.h>
int main() {
    const int a = 2, b = 3;
    printf("Somme de %d+%d = %d\n", a, b, add(a, b));
}
EOF

$ cat > add.h <<EOF
int add(int a, int b);
EOF

$ cat > add.c <<EOF
int add(int a, int b) {
    return a + b;
}
EOF

# Compilation séparée des objets
$ gcc -c main.c -o main.o
$ gcc -c add.c -o add.o

# Édition de liens
$ gcc main.o add.o -o main
```

Notez que si vous avez deux fichiers C mais que vous ne souhaitez pas les compiler séparément, vous pouvez les compiler en une seule commande :

```bash
$ gcc main.c add.c -o main
```

## Options de compilation

`gcc` et `g++` acceptent de nombreuses options de compilation. Les plus courantes sont :

| Option      | Description                                                        |
| ----------- | ------------------------------------------------------------------ |
| `-c`        | Compile le code source en un fichier objet sans l'éditer de liens. |
| `-o`        | Spécifie le nom du fichier de sortie.                              |
| `-I`        | Spécifie un répertoire où chercher les fichiers d'en-tête.         |
| `-L`        | Spécifie un répertoire où chercher les bibliothèques.              |
| `-l`        | Spécifie une bibliothèque à lier.                                  |
| `-Wall`     | Active tous les avertissements.                                    |
| `-Werror`   | Traite les avertissements comme des erreurs.                       |
| `-g`        | Inclut des informations de débogage dans le fichier objet.         |
| `-O`        | Optimise le code.                                                  |
| `-std`      | Spécifie la norme du langage.                                      |
| `-pedantic` | Respecte strictement la norme.                                     |
| `-D`        | Définit une macro.                                                 |
| `-U`        | Undefine une macro.                                                |
| `-E`        | Arrête après l'étape de préprocesseur.                             |
| `-S`        | Arrête après l'étape de compilation.                               |
| `-v`        | Affiche les commandes exécutées par le compilateur.                |

Pour compiler un programme avec les optimisations maximales, dans la norme C17, avec tous les avertissements activés et traités comme des erreurs, vous pouvez utiliser la commande suivante :

```bash
$ gcc -std=c17 -O3 -Wall -Werror -pedantic main.c -o main
```
## Optimisation

L'optimisation est une technique qui vise à améliorer les performances d'un programme en réduisant le temps d'exécution et/ou la consommation de mémoire. Les compilateurs `gcc` et `g++` offrent plusieurs niveaux d'optimisation, chacun ayant des caractéristiques propres.

`-O0`

: Aucune optimisation. C'est le niveau par défaut. Le code C est traduit en langage assembleur sans tentative d'amélioration des performances. Cela facilite le débogage, car le code généré reste très proche du code source. Toutefois, les performances peuvent être deux à trois fois inférieures à celles du code optimisé.

`-O1`

: Optimisation légère. Le compilateur applique des optimisations locales comme la suppression des instructions inutiles, la propagation des constantes, et la simplification des expressions constantes. Ce niveau d'optimisation équilibre le gain de performances avec la vitesse de compilation.

`-O2`

: Optimisation standard. À ce niveau, le compilateur applique des optimisations plus agressives, telles que la réduction des boucles, la suppression des appels de fonctions inutiles et l'amélioration de la gestion des expressions. Cela peut allonger le temps de compilation et augmenter la taille du code, mais les performances générées sont significativement améliorées.

`-O3`

: Optimisation maximale. Le compilateur applique toutes les optimisations du niveau `-O2` ainsi que des optimisations supplémentaires comme l'optimisation des boucles (loop unrolling), l'inlining de fonctions plus importantes, et l'amélioration de la gestion des appels de fonctions. Ce niveau maximise les performances, mais peut également accroître la taille du code et le temps de compilation.

`-Os`

: Optimisation pour la taille. Le compilateur se concentre sur la réduction de la taille du fichier exécutable. Cela peut réduire les performances, mais est souvent utile pour les environnements à ressources limitées, comme les systèmes embarqués, ou pour les applications devant être distribuées via des réseaux à faible bande passante.

`-Ofast`

: Optimisation rapide. Le compilateur applique les optimisations du niveau `-O3`, mais avec des assouplissements sur le respect des normes du langage C. Certaines vérifications sont désactivées pour améliorer encore les performances, ce qui peut entraîner des comportements non conformes à la norme dans certains cas. Ce niveau peut être très performant, mais il doit être utilisé avec précaution.

`-ffast-math`

: Optimisation agressive des calculs mathématiques. Le compilateur effectue des optimisations poussées sur les opérations mathématiques en ignorant certaines précautions sur la précision et les exceptions. Cela peut considérablement accélérer les calculs, mais augmente également le risque de résultats incorrects ou inattendus. Cette option est à utiliser uniquement si la précision des calculs n'est pas critique.

`-flto`

: Optimisation intermodulaire (Link-Time Optimization). Le compilateur fusionne les fichiers objets avant l'édition de liens, permettant ainsi des optimisations globales à l'échelle du programme. Cela inclut l'inlining entre fichiers, la suppression des fonctions inutilisées, la propagation des constantes et la fusion des boucles. Cette optimisation est particulièrement efficace sur les gros projets avec plusieurs fichiers source, permettant d'améliorer les performances globales du programme.


## Bibliothèques

Les bibliothèques sont des fichiers contenant des fonctions et des variables prédéfinies. Il existe deux types de bibliothèques : les bibliothèques **statiques** et les bibliothèques **partagées**. Les bibliothèques statiques ont l'extension `.a` sous POSIX et `.lib` sous Windows. Les bibliothèques partagées ont l'extension `.so` sous POSIX et `.dll` sous Windows.

La bibliothèque standard du langage C est `libc`. Elle est incluse par défaut dans tous les programmes C. Pour inclure une bibliothèque, il suffit de spécifier son nom avec l'option `-l`. Par exmple la bibliothèque `m` contient des fonctions mathématiques. Elle s'appelle `libm` sous Unix/Linux.

Aussi si vous souhaitez calculer le sinus de 3.14, vous pouvez utiliser la fonction `sin` de la bibliothèque `m`, et par conséquent vous devez lier cette bibliothèque à votre programme :

```bash
$ gcc main.c -o main -lm
```

Notez que l'option `-lm` doit être placée après le nom du fichier source. En effet, `gcc` traite les options dans l'ordre où elles apparaissent sur la ligne de commande. Si l'option `-lm` est placée avant le nom du fichier source, `gcc` ne trouvera pas la fonction `sin` et échouera.

Voici quelques bibliothèques couramment utilisées :

| Bibliothèque | Description                         |
| ------------ | ----------------------------------- |
| `libc`       | Bibliothèque standard du langage C. |
| `libm`       | Fonctions mathématiques.            |
| `libpthread` | Fonctions de threads POSIX.         |
| `libcurl`    | Client HTTP.                        |
| `libssl`     | Bibliothèque de chiffrement SSL.    |
| `libcrypto`  | Bibliothèque de chiffrement.        |
| `libz`       | Compression de données.             |
| `libpng`     | Traitement d'images PNG.            |
| `libsqlite3` | Base de données SQLite.             |
