# Préprocesseur

Figure: Illustration du mécanisme de pré-processing avant la compilation

![Mécanisme de pré-processing avant compilation](/assets/images/preprocessing-fun.drawio)

Comme nous l'avons vu en [introduction][structured-text-programming], le langage C est basé sur une double grammaire, c'est-à-dire qu'avant la compilation du code, un autre processus est appelé visant à préparer le code source avant la compilation. Le cœur de cette opération est appelé **préprocesseur**. Les instructions du préprocesseur C sont faciles à reconnaître, car elles débutent toutes par le croisillon `#` U+0023, *hash* (ou *she*) en anglais et utilisées récemment comme [hashtag](https://fr.wikipedia.org/wiki/Hashtag) sur les réseaux sociaux. Notons au passage que ce caractère était historiquement utilisé par les Anglais sous le dénominatif *pound* (livre). Lorsqu'il est apparu en Europe, il a été confondu avec le caractère dièse (*sharp*) `♯` U+266F présent sur les pavés numériques de téléphone.

Le vocabulaire du préprocesseur se compose de directives démarrant par un croisillon. Notons que ces directives (à l'exception des opérateurs de concaténation de conversion en chaîne de caractère) sont des instructions de ligne (*line-wise*), c'est-à-dire qu'elles doivent se terminer par un caractère de fin de ligne. Le point-virgule n'a pas d'effet sur le préprocesseur. En outre, il est possible d'insérer des espaces et des tabulations entre le croisillon et la directive. Il est communément admis d'utiliser cette fonctionnalité pour gérer l'indentation des directives préprocesseur, car certaines conventions imposent que le croisillon soit en première colonne. La table suivante résume les directives du préprocesseur.

Table: Vocabulaire du préprocesseur

| Terme                                          | Description                                     |
| ---------------------------------------------- | ----------------------------------------------- |
| [`#include`][preprocessor-include]             | Inclus un fichier dans le fichier courant       |
| [`#define`][preprocessor-define]               | Crée une définition (Macro)                     |
| [`#undef`][preprocessor-undef]                 | Détruit une définition existante                |
| [`#if defined`][preprocessor-ifdef]            | Teste si une définition existe                  |
| [`#if` .. `#endif`][preprocessor-if]           | Test conditionnel                               |
| [`#`][preprocessor-hash]                       | Opérateur de conversion en chaîne de caractères |
| [`##`][preprocessor-hash-hash]                 | Opérateur de concaténation de chaînes           |
| [`#line`][preprocessor-line]                   | Directive de ligne                              |
| [`#error "error message"`][preprocessor-error] | Génère une erreur                               |
| [`#pragma`][preprocessor-pragma]               | Directive spécifique au compilateur             |

Le préprocesseur C est indépendant du langage C, c'est-à-dire qu'il peut être exécuté sur n'importe quel type de fichier. Pour le prouver, prenons l'exemple d'une lettre générique d'un cabinet dentaire :

```c
#ifdef FEMALE
#    define NAME Madame
#else
#    define NAME Monsieur
#endif
Bonjour NAME,

Veuillez noter votre prochain rendez-vous le DATE, à HOUR heure.

Veuillez agréer, NAME, nos meilleures salutations,

#ifdef IS_BOSS
Le directeur
#elif defined IS_ASSISTANT
La secrétaire du directeur
#elif defined OWNER_NAME
OWNER_NAME
#else
#    error "Lettre sans signature"
#endif
```

Il est possible d'appeler le préprocesseur directement avec l'option `-E` de `gcc`. Des directives `define` additionnelles peuvent être renseignées depuis la ligne de commande avec le drapeau `-D`. Voici un exemple d'utilisation :

```console
$ gcc -xc -E test.txt \
    -DDATE=22 -DHOUR=9:00 \
    -DFEMALE \
    -DOWNER_NAME="Adam" -DPOSITION=employee
# 1 "test.txt"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "test.txt"
Bonjour Madame,

Veuillez noter votre prochain rendez-vous le 22, à 9:00 heure.

Veuillez agréer, Madame, nos meilleures salutations,

Adam
```

En sortie il reste des directives `#` nommées *linemarkers* ou marqueurs de lignes qui sont des commentaires utilisés pour le déverminage. Ces directives de lignes contiennent en première position le numéro de la ligne du fichier originel suivi d'informations sont utiles pour le débogage, car elles permettent de retrouver la source des erreurs. Le format est spécifique à GCC. Un marqueur de ligne à le format suivant :

```c
# linenum filename flags
```

Les drapeaux peuvent être : `1` pour indiquer le début d'un nouveau fichier inclus, `2` pour indiquer la fin d'un fichier inclus, `3` pour indiquer que le texte suivant provient d'un fichier système et `4` pour indiquer que le texte doit être traité comme un bloc implicite.

!!! note "Suppression des marqueurs de lignes"

    Il est possible de supprimer les directives de lignes générées par le préprocesseur avec l'option `-P` de `gcc`. Le `-xc` indique que le fichier est un fichier C ce qui évite un message d'erreur su l'extension du fichier d'entrée n'est pas `.c`.

    ```console
    $ gcc -xc -E test.txt -P
    ```

## Phases de traduction

Le standard C99 §5.1.1.2 alinéa 1 définit 8 phases de traductions dont les 4 premières concernent le préprocesseur :

1.  Remplacement des multicaractères: les caractères Unicode et autres caractères spéciaux sont remplacés par des caractères ASCII. Les trigraphes sont également interprétés.

2.  Remplacement des *backslash* de fin de ligne. Lorsqu'un *backslash* est suivi d'un saut de ligne, le saut de ligne est supprimé. Cela permet d'écrire des lignes longues sur plusieurs lignes.

3.  Suppression des commentaires. Chaque commentaire est remplacé par une espace. Les commentaires de type `//` et `/* */` sont par conséquent supprimés.

4.  Les directives de prétraitement sont exécutées, les invocations de macros sont étendues et les expressions avec l'opérateur unaire `_Pragma` sont exécutées ainsi que les directives `#include` appliquées récursivement.

Voici un exemple de code C avec des directives de prétraitement :

```c
int noël[] = ??< 23, 42 ??> ; // Array of integers
char *💩 = /* WTF */ "Pile of Poo";
```

Après prétraitement avec `gcc -std=c99 -E -P` on obtient le code suivant:

```c
int no\U000000ebl[] = { 23, 42 } ;
char *\U0001f4a9 = "Pile of Poo";
```

Notons que dans le standard C23, les trigraphes ont été supprimés c'est pourquoi l'exemple ci-dessus ne fonctionne que si le flag `-std=c99` est utilisé.

## Extensions des fichiers

Pour s'y retrouver, une convention existe sur les extensions des fichiers. Rappelons que selon POSIX un fichier n'a pas nécessairement d'extension, c'est une convention libre à l'utilisateur néanmoins GCC utilise les extensions pour déterminer le type de fichier. Selon le standard GNU, les extensions suivantes sont en vigueur :

`.h`

: Fichier d'en-tête ne comportant que des définitions du préprocesseur, des déclarations (structures, unions ...) et des prototypes de fonction, mais aucun code exécutable. Ce fichier sera soumis au préprocesseur s'il est inclus dans un fichier source.

`.c`

: Fichier source C comportant les implémentations de fonctions et les variables globales. Ce fichier sera soumis au préprocesseur.

`.i`

: Fichier source C qui a déjà été prétraité qui ne sera pas soumis au préprocesseur: `gcc -E -o foo.i foo.c`

`.s`

: Fichier assembleur non soumis au préprocesseur.

`.S`

: Fichier assembleur soumis au préprocesseur. Notons toutefois que cette convention n'est pas applicable sous Windows, car le système de fichier n'est pas sensible à la casse et un programme ne peut pas savoir si le fichier est `.s` ou `.S` (merci Windows pour toutes ces frustrations que tu me crées).

`.o`

: Fichier objet généré par le compilateur après compilation

`.a`

: Bibliothèque statique. Similaire à un fichier `.o` mais peut contenir plusieurs fichiers objets.

`.so`

: Bibliothèque dynamique. Fichier objet partagé.

[]{#preprocessor-include}

## Inclusion (`#include`)

La directive `#include` permet d'incorporer le contenu d’un fichier dans un autre de manière récursive, facilitant ainsi la modularisation et la lisibilité du code. Cette approche permet de structurer un programme en plusieurs fichiers, favorisant une meilleure organisation et maintenabilité.

Deux formes d'inclusion existent : locale et globale. C'est d’ailleurs une question récurrente sur [StackOverflow](https://stackoverflow.com/a/21594/2612235).

Inclusion globale : `#include <filename>`

: Dans ce cas, le préprocesseur recherche le fichier à inclure dans les chemins système prédéfinis (`/usr/include`, etc.), ainsi que dans ceux spécifiés par les options `-I` du compilateur ou la variable d'environnement `C_INCLUDE_PATH`.

Inclusion locale : `#include "filename"`

: Ici, la recherche débute dans le répertoire courant, puis se poursuit dans les chemins définis par les options `-I` et la variable `C_INCLUDE_PATH`.

L’inclusion de fichiers est un processus simple de concaténation : le contenu du fichier inclus est copié à l’emplacement de la directive `#include`. Toutefois, cela peut mener à des dépendances cycliques, provoquant des inclusions infinies. Par exemple, si un fichier `foo.h` s'inclut lui-même, le préprocesseur entrera dans une boucle sans fin, aboutissant à une erreur après un certain seuil :

```bash
$ echo '#include "foo.h"' > foo.h
$ gcc -E foo.h
head.h:1:18: error: #include nested depth 200 exceeds maximum of 200 (use
-fmax-include-depth=DEPTH to increase the maximum)
    1 | #include "foo.h"
```

### Prévenir les inclusions multiples

Pour éviter ce genre de problème, il est courant d’utiliser des *include guards* (ou *header guards*). Ce mécanisme consiste à encapsuler le contenu d’un fichier d’en-tête avec une macro unique, garantissant ainsi que le fichier ne sera inclus qu'une seule fois au cours de la compilation. Ce procédé est détaillé [plus loin][preprocessor-include-guard].

### Chevrons ou guillemets ?

Une question souvent posée est de savoir si l'inclusion doit se faire avec des guillemets ou des chevrons. La réponse dépend du contexte du projet. Pour les projets de petite envergure, les bibliothèques standard sont incluses avec des chevrons, tandis que les fichiers locaux, souvent situés dans le même répertoire que les fichiers sources, sont inclus via des chemins relatifs avec des guillemets. Dans le cas de projets plus conséquents, où les fichiers sources et les en-têtes sont souvent séparés, il peut être inapproprié d’utiliser des chemins relatifs tels que `#include "../include/foo.h"`. Une meilleure pratique consiste à utiliser l’option GCC `-Iinclude/`, qui permet d’indiquer au compilateur où trouver les fichiers d’en-tête. Bien qu'il soit techniquement possible d’utiliser des chevrons dans ce cas, cela peut prêter à confusion pour les lecteurs du code, qui pourraient penser qu’il s’agit d’une bibliothèque standard.

### Ordre des inclusions

Il est recommandé de respecter un ordre précis lors de l'inclusion des fichiers d'en-tête, pour éviter des dépendances implicites et des conflits potentiels :

1. Les fichiers d'en-tête propres au projet.
2. Les en-têtes des bibliothèques externes.
3. Les en-têtes de la bibliothèque standard.

Ainsi, on pourrait avoir le code suivant :

```c
#include "foo.h"

#include <SDL2/SDL.h>

#include <stdio.h>
#include <stdlib.h>
```

Cet ordre garantit que les dépendances des bibliothèques externes ou standard ne soient pas résolues par inadvertance grâce à une inclusion locale. Pour mieux illustrer, considérons un fichier `stack.h` qui définit une structure de pile :

```c
#pragma once

bool stack_push(int_least32_t value);
bool stack_pop(int_least32_t *value);
```

Ici, les types `bool` et `int_least32_t` ne sont pas définis dans ce fichier, car les inclusions de `<stdbool.h>` et `<stdint.h>` sont absentes. Si le fichier `main.c` les inclut avant `stack.h` :

```c
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include "stack.h"
```

Aucune erreur ne sera générée. Cependant, `stack.h` dépend d'inclusions externes, ce qui est généralement à éviter. En incluant les fichiers locaux en premier, on s'assure de leur autonomie.

[]{#preprocessor-define}

## Macros (`#define`)

Les macros sont des symboles généralement écrits en majuscule et qui sont remplacés par le préprocesseur. Ces définitions peuvent être utiles pour définir des constantes globales qui sont définies à la compilation et qui peuvent être utilisées comme des options de compilation. Par exemple, pour définir la taille d'une fenêtre de filtrage :

```c
#ifndef WINDOW_SIZE
#    define WINDOW_SIZE 10
#endif

int tab[WINDOW_SIZE];

void init(void) {
    for(size_t i = 0; i < WINDOW_SIZE; i++)
        tab[i] = i;
}
```

L'ajout de la directive conditionnelle `#ifndef` permet d'autoriser la définition de la taille du tableau à la compilation directement depuis GCC:

```console
$ gcc main.c -DWINDOW_SIZE=42
```

Notons que durant le préprocessing toute occurrence d'un symbole défini est remplacée par le contenu de sa définition. **C'est un remplacement de chaîne bête, idiot et naïf**. Il est par conséquent possible d'écrire :

```c
#define MAIN int main(
#define BEGIN ) {
#define END return 0; }
#define EOF "\n"

MAIN
BEGIN
    printf("Hello" EOF);
END
```

Par ailleurs, on relèvera qu'il est aussi possible de commettre certaines erreurs en utilisant les définitions. Prenons l'exemple d'une macro déclarée sans parenthèses :

```c
#define ADD a + b

int a = 12;
int b = 23;
int c = ADD * ADD
```

Après prétraitement le comportement ne sera pas celui attendu, car la multiplication devrait être plus prioritaire que l'addition :

```c
int a = 12;
int b = 23;
int c = a + b * a + b
```

Pour se prémunir contre ces éventuelles coquilles, on protègera toujours les définitions avec des parenthèses

```c
#define ADD (a + b)
#define PI (3.14159265358979323846)
```

!!! warning "Espace nécessaire"

    Il est important de noter que l'espace entre le nom de la macro et les parenthèses est **strictement nécessaire**. En effet, si on écrit `#!c #define ADD(a + b)`, le préprocesseur générera une erreur car il considère que `ADD` est une macro.

### Linéarisation

Le processus d'expansion des macros est une étape clé dans la façon dont le préprocesseur C interprète et remplace les macros définies avec `#define`. Ce processus est appelé **linéarisation**, car les macros sont substituées avant la compilation en suivant une logique linéaire et récursive. Prenons l'exemple de macros imbriquées :

```c
#define DOUBLE(x) (2 * (x))
#define SQUARE(x) ((x) * (x))

int main() {
    int result = SQUARE(DOUBLE(3));
}
```

### Macros avec arguments

Une **macro** peut prendre des paramètres et permettre de générer du code à la compilation par simple substitution de texte. Les macros sont souvent employées pour définir des fonctions simples qui ne nécessitent pas de typage explicite. Par exemple, pour implémenter une macro `MIN` qui retourne la valeur minimale entre deux arguments :

```c
#define MIN(x, y) ((x) < (y) ? (x) : (y))
```

Le mécanisme de la macro repose uniquement sur un remplacement textuel :

```console
$ cat test.c
#define MIN(x, y) ((x) < (y) ? (x) : (y))
int main(void) { return MIN(23, 12); }

$ gcc -E -P test.c -o-
int main(void) { return ((23) < (12) ? (23) : (12)); }
```

Notez que l'absence d'espace entre le nom de la macro et la parenthèse qui suit est cruciale. Une macro incorrectement définie, comme dans l'exemple ci-dessous, entraîne un comportement inattendu :

```console
$ cat test.c
#define ADD (x, y) ((x) + (y))
int main(void) { return ADD(23, 12); }

$ gcc -E -P test.c -o-
int main(void) { return (x, y) ((x) + (y))(23, 12); }
```

Une macro peut contenir plusieurs instructions, comme dans l'exemple suivant :

```c
#define ERROR(str) printf("Erreur: %s\r\n", str); log(str);

if (y < 0)
    ERROR("Zero division");
else
    x = x / y;
```

Dans cet exemple, l'absence d'accolades dans l'instruction `if` fait que seule la première instruction est exécutée lorsque la condition `y < 0` est vraie. Or, la macro `ERROR` contient deux instructions distinctes, ce qui conduit à un comportement incorrect.

Une solution triviale consisterait à encapsuler les instructions de la macro dans des accolades :

```c
#define ERROR(str) { printf("Erreur: %s\r\n", str); log(str); }
```

Cependant, cette approche présente des problèmes lorsqu’elle est utilisée dans des structures conditionnelles, comme un `if-else`. En effet, l'appel à la macro est suivi d'un point-virgule, et un bloc délimité par des accolades constitue une **instruction composée** (*compound statement*). L'ajout du point-virgule après la macro provoque alors une terminaison anticipée de l'instruction `if`, laissant le `else` sans correspondance :

```c
if (y < 0)
    ERROR("Zero division");
else
    x = x / y;
```

Pour contourner ce problème, il est préférable d'envelopper la macro dans une structure `do { ... } while (0)` afin de la transformer en une seule instruction indivisible, quel que soit le contexte d'utilisation :

```c
#define ERROR(str) do { \
    printf("Erreur: %s\r\n", str); \
    log(str); \
} while (0)
```

Cette construction crée une boucle vide qui s'exécute une seule fois, garantissant que la macro se comporte comme une instruction unique, même si elle contient plusieurs lignes. De plus, l'utilisation de `\` permet d'échapper le retour à la ligne pour conserver une lisibilité optimale tout en faisant comprendre au préprocesseur que tout le bloc est une seule ligne logique.

Même avec une bonne encapsulation des macros, certains pièges subsistent, notamment l'utilisation des post/pré-incréments dans les arguments. Par exemple, considérons la macro `ABS` qui calcule la valeur absolue d’un nombre :

```c
#define ABS(x) ((x) >= 0 ? (x) : -(x))

return ABS(x++);
```

Dans cet exemple, la variable `x` est post-incrémentée plusieurs fois, car l'argument de la macro est réévalué à chaque usage :

```c
return ((x++) >= 0 ? (x++) : -(x++));
```

Ici, `x` est incrémenté trois fois au lieu d'une seule, ce qui peut entraîner des comportements indésirables.

**Rappel des règles de bonnes pratiques:**

1. **Protéger les paramètres de macro avec des parenthèses** pour garantir une évaluation correcte de l'expression.
2. **Encapsuler les macros à plusieurs instructions dans une boucle vide** pour éviter des erreurs dans les structures de contrôle comme `if-else`.
3. **Éviter les post/pré-incréments dans les macros**, car ils peuvent provoquer des réévaluations imprévues et des erreurs difficiles à détecter.

::: exercise {title="#(ex:macro-compromise) : Macro compromise ?"}
Que retourne la fonction `foo` lors de son exécution avec le code suivant ?

```c
#define ABS(x) x >= 0 ? x: -x
int foo(void) { return ABS(5 - 8); }
```

- [ ] 3
- [ ] -3
- [x] -13
- [ ] 5 - 8
- [ ] 0
:::

[]{#preprocessor-if}
[]{#preprocessor-ifdef}

### _Static_assert

Le mot-clé `_Static_assert` est une directive de préprocesseur introduite dans le standard C11. Elle permet de vérifier des conditions à la compilation. Contrairement à `#if`, `_Static_assert` génère une erreur de compilation si la condition n'est pas vérifiée. Par exemple, pour vérifier que la taille d'un tableau est supérieure à 10 :

```c
_Static_assert(sizeof(tab) > 10, "La taille du tableau est inférieure à 10");
```

[]{#preprocessor-va-args}

### Varadiques

Les macros varadiques permettent de définir des macros qui prennent un nombre variable d'arguments. Par exemple, pour définir une macro qui affiche un message avec un nombre variable d'arguments. Il s'agit d'une extension du standard C99. Pour cela on utilise l'opérateur `...` suivi de `__VA_ARGS__` qui représente les arguments passés à la macro.

C'est utilisé par exemple pour créer des fonctions de débogage :

```c
#define DEBUG_LOG(level, fmt, ...) \
    printf("[%s] " fmt "\n", level, __VA_ARGS__)

int main() {
    DEBUG_LOG("\033[32mINFO\033[0m", "User %s logged in", "Alice");
    DEBUG_LOG("\033[31mERROR\033[0m", "Failed to open file %s", "data.txt");
}
```

### Terminologie

Que ce soit en anglais ou en français il n'est pas très clair de comment nommer :

1. `#define FOO 42`
2. `#define FOO(x) (x * x)`

Formellement les deux sont des **définitions de préprocesseur** mais également des **macros**. En informatique une macro est un modif de substitution de texte pouvant prendre des arguments.

Dans un sens plus large la première définition est souvent qualifiée de **constante symbolique** bien que ce ne soit pas une vraie constante (`const`) elle rempli un rôle similaire.

## Directive conditionnelle (`#if`)

La directive conditionnelle `#if` permet de tester des expressions à la compilation. Elle est souvent utilisée pour définir des options de compilation en fonction des besoins.

Prenons l'exemple d'un programme qui gère une grosse masse de messages. Ces derniers sont triés selon un critère spécifique et pour ce faire une fonction de tri est utilisée. Nous verrons plus tard que le tri est un sujet complexe et qu'un critère du choix d'un algorithme de tri est la stabilité. Un tri stable préserve l'ordre relatif des éléments qui ne sont pas distingués par le critère de tri. Par exemple, si on trie des personnes par leur âge, un tri stable préservera l'ordre des personnes de même âge. Si la stabilité n'est pas un critère, un tri instable peut être plus rapide. Pour cette raison, selon la nécessité d'utilisation du programme, il peut être pertinent de définir lors de la compilation s'il faut être très performant mais instable ou plus lent mais stable. Cela pourrait se faire avec :

```c
#ifdef STABLE_SORT
#    define SORT merge_sort
#else
#    define SORT quick_sort
#endif
```

La configuration peut se faire soit directement dans le code source avec une directive préprocesseur :

```c
#define STABLE_SORT
```

soit depuis la ligne de commande :

```console
$ gcc main.c -DSTABLE_SORT
```

L'instruction `#ifdef` est un sucre syntaxique pour `#if defined`, autrement dit : *si la définition est déclarée et quelle que soit sa valeur*. En effet, une déclaration sans valeur est tout à fait possible. Néanmoins cela peut créer de la confusion. Prenons l'exemple suivant pour lequel le message `Dynamic allocation is allowed` sera affiché bien que la valeur de `ALLOW_DYNAMIC_ALLOCATION` soit `0` :

```c
#define ALLOW_DYNAMIC_ALLOCATION 0

#if defined ALLOW_DYNAMIC_ALLOCATION
printf("Dynamic allocation is allowed");
#else
printf("Dynamic allocation is not allowed");
#endif
```

Pour se prémunir de ce genre de problème, il est recommandé de toujours définir une valeur à une déclaration et de tester si cette valeur est vraie :

```c
#define ALLOW_DYNAMIC_ALLOCATION 0

#if ALLOW_DYNAMIC_ALLOCATION
〜
```

Une bonne pratique est soit de lever une erreur si la valeur n'est pas définie, soit de définir une valeur par défaut :

```c
#define YES 1
#define NO 0

#define STRICT YES
#define ALLOW_DYNAMIC_ALLOCATION YES

#ifndef ALLOW_DYNAMIC_ALLOCATION
#    if defined STRICT && STRICT == YES
#        error "ALLOW_DYNAMIC_ALLOCATION is not defined"
#    else
#        define ALLOW_DYNAMIC_ALLOCATION NO
#    endif
#endif
```

Par analogie à l'instruction `if`, il est possible d'utiliser `#else` (`else`) et `#elif` (`else if`) pour définir des alternatives :

```c
#define MODE_UPPERCASE 0
#define MODE_LOWERCASE 1
#define MODE_ARABIC 2

#ifndef DISPLAY_MODE
#   define DISPLAY_MODE MODE_UPPERCASE
#endif

void display(char value) {
#if DISPLAY_MODE == MODE_UPPERCASE
    printf("%c", 'A' + (value % 26));
#elif DISPLAY_MODE == MODE_LOWERCASE
    printf("%c", 'a' + (value % 26));
#elif DISPLAY_MODE == MODE_ARABIC
    printf("%d", value);
#else
#   error "DISPLAY_MODE is not defined"
#endif
}
```

[]{#preprocessor-undef}

## Suppression (`#undef`)

Un symbole défini soit par la ligne de commande `-DFOO=1`, soit par la directive `#define FOO 1` ne peut pas être redéfini:

```console
$ cat test.c
#define ANSWER 42
#define ANSWER 23
$ gcc -E test.c
test.c:2: warning: "ANSWER" redefined
    2 | #define ANSWER 23
      |
test.c:1: note: this is the location of the previous definition
    1 | #define ANSWER 42
      |
```

C'est pourquoi il peut être utile d'utiliser `#undef` pour supprimer une directive préprocesseur :

```c
#ifdef FOO
#   undef FOO
#endif
#define FOO 1
```

L'utilisation de `#undef` dans un programme est tout à fait légitime dans certains cas, mais elle doit être manipulée avec précaution.

On peut citer par exemple la fameuse constante `M_PI` qui n'est pas définie par le standard C mais que la plupart des compilateurs définissent. Si vous avez besoin d'utiliser la valeur $\pi$ dans votre programme, vous pouvez soit utiliser par défaut la valeur définie par la bibliothèque si elle existe sinon la vôtre:

```c
#ifndef M_PI
#    define M_PI 3.14159265358979323846
#endif
```

Ou alors, vous pourriez forcer la valeur de $\pi$ à celle que vous souhaitez :

```c
#undef M_PI
#define M_PI 3.14159265358979323846
```

[]{#preprocessor-error}

## Erreur (`#error`)

La directive `#error` génère une erreur avec le texte qui suit la directive et arrête la compilation. Elle est souvent utilisée pour s'assurer que certaines conditions sont remplies avant de compiler le code. Par exemple, pour s'assurer que la taille du noyau d'un filtre est impair :

```c
#if !(KERNEL_SIZE % 2)
#    error Le noyau du filtre est pair
#endif
```

On peut l'utiliser également pour s'assurer que le compilateur est compatible avec une version spécifique du standard C :

```c
#if __STDC_VERSION__ < 201112L
    #error "C11 support required"
#endif
```

!!! note "Warning"

    Certains compilateurs comme GCC ou Clang permettent d'utiliser `#warning` pour générer un avertissement, bien que cette directive ne soit pas standard.

    ```c
    #warning "This is a warning"
    ```

## Macros prédéfinies

Le standard définit certains symboles utiles pour le débogage :

`__LINE__`

: Est remplacé par le numéro de la ligne sur laquelle est placé ce symbole

`__FILE__`

: Est remplacé par le nom du fichier sur lequel est placé ce symbole

`__func__`

: Est remplacé par le nom de la fonction du bloc dans lequel la directive se trouve

`__STDC__`

: Est remplacé par 1 pour indiquer que l'implémentation est compatible avec C90

`__STDC_VERSION__`

: Est remplacé par la version du standard C utilisée par le compilateur, il s'agit d'un entier de la forme `AAAAMM` où `AAAA` est l'année et `MM` le mois. Par exemple pour C11, la valeur est `201112L`

`__DATE__`

: Est remplacé par la date sous la forme `"Mmm dd yyyy"`

`__TIME__`

: Est remplacé par l'heure au moment du pre-processing `"hh:mm:ss"`

`__COUNTER__`

: Est remplacé par un entier qui s'incrémente à chaque fois qu'il est utilisé. C'est une directive non standard mais disponible dans GCC et Clang.

On peut par exemple créer une macro pour afficher des messages de d'erreur avec le nom du fichier le numéro de ligne et la date de compilation :

```c
#define ERROR(msg) fprintf(stderr, "%s:%d %s %s\n", \
    __FILE__, __LINE__, __DATE__, msg)
```

## Caractère d'échappement

La plupart des instructions préprocesseur sont des instructions de ligne, c'est-à-dire qu'elles se terminent par un saut de ligne or parfois (notamment pour les macros), on souhaiterait écrire une instruction sur plusieurs lignes.

L'anti-slash (`backslash`) suivi directement d'un retour à la ligne est interprété par le préprocesseur comme un saut de ligne virtuel. Il permet par exemple de casser les longues lignes :

```c
#define TRACE printf("Le programme est passé " \
    " dans le fichier %s" \
    " ligne %d\n", \
    __FILE__, __LINE__);
```

[]{#preprocessor-line}

## Directive de ligne

La directive `#line` permet de modifier le numéro de ligne et le nom du fichier pour les directives de débogage. En pratique elle est peu utilisée, car les compilateurs modernes gèrent correctement les numéros de ligne et les noms de fichiers.

```c
#line 42 "foo.c"
```

[]{#preprocessor-hash-hash}

## Concaténation de chaînes

Parfois il est utile de vouloir concaténer deux symboles comme si ce n'était qu'un seul. L'opérateur de concaténation `##` permet de concaténer deux arguments dans une macro et de les combiner en un seul *token*. Cet opérateur est particulièrement utilisé dans des macros avancées pour générer du code automatiquement à partir d'une combinaison d'arguments.

Un cas d'usage typique est la création de noms dynamiques.

```c
#define CONCAT(a, b) a##b

int main() {
    int var1 = 10, var2 = 20;

    CONCAT(var, 1) = 30;  // devient var1 = 30
    CONCAT(var, 2) = 40;  // devient var2 = 40

    printf("%d, %d\n", var1, var2);  // 30, 40
}
```

Cela peut être utile par exemple pour gérer des traductions :

```c
#define LANGUAGE FR

#define CONCAT(a, b) a##b

void greet_FR(void) { printf("Bonjour\n"); }
void greet_EN(void) { printf("Hello\n"); }

#define GREET CONCAT(greet_, LANGUAGE)

int main() {
    GREET();
}
```

Un autre usage courant est de définir le *mangling* des noms de fonctions pour une bibliothèque. Par exemple, si vous avez une bibliothèque qui définit une fonction `foo` et que vous voulez éviter les conflits de noms, vous pourriez définir une macro pour ajouter un préfixe et un suffixe :

```c
#define MANGLE(name) prefix_ ## name ## _suffix

void MANGLE(foo)(void) {
    printf("Hello");
}

int main() {
    MANGLE(foo)();
}
```

Rappelez-vous que le langage C ne permet pas de définir des fonctions avec le même nom même si elles ont des signatures différentes et même si elles sont dans deux fichiers séparés. Un paramètre de configuration `MANGLE` permettrait de spécifier à la compilation d'une bibliothèque le préfixe à ajouter à toutes les fonctions de la bibliothèque.

[]{#preprocessor-hash}

## Conversion en chaîne

Il est possible de convertir un symbole en chaîne de caractères avec l'opérateur `#` :

```c
#define STRINGIFY(x) #x
printf(STRINGIFY(42));
```

Le plus souvent cet opérateur est utilisé pour traiter des messages d'erreurs:

```c
#define WARN_IF_NEGATIVE(x) \
    if (x < 0) { \
        printf("Warning: the value of " #x " is negative (%d)\n", x); \
    }

int main() {
    int value = -5;
    WARN_IF_NEGATIVE(value);
}
```

Ou par exemple pour afficher la valeur d'une variable :

```c
#define PRINT_VAR(var) printf(#var " = %d\n", var)

int main() {
    int a = 10;
    PRINT_VAR(a);
}
```

## Désactivation de code

Je vois trop souvent des développeurs commenter des sections de code pour le débogage. Cette pratique n'est pas recommandée, car les outils de [refactoring](https://en.wikipedia.org/wiki/Code_refactoring) (réusinage de code), ne parviendront pas à interpréter le code en commentaire jugeant qu'il ne s'agit pas de code, mais de texte insignifiant. Une méthode plus robuste et plus sure consiste à utiliser une directive conditionnelle :

```c
#if 0 // TODO: Check if this code is still required.
if (x < 0) {
    x = 0;
}
#endif
```

[]{#preprocessor-include-guard}

## Include guard

Comme évoqué plus haut, les fichiers d'en-tête peuvent être inclus plusieurs fois dans un programme ce qui peut poser des problèmes de redéfinition de symboles ou d'erreurs de dépendences cycliques. En informatique on parle volontiers d'**idempotence** pour désigner une opération qui peut être appliquée plusieurs fois sans changer le résultat au-delà de la première application. Inclure une ou plusieurs fois un même fichier d'en-tête ne doit pas changer le résultat de la compilation.

Pour ce faire, on utilise des garde-fous (*guards*) pour protéger les fichiers d'en-tête. Imaginons que la constante `M_PI` soit définie dans le header `<math.h>`:

```c
#define M_PI  3.14159265358979323846
```

Si ce fichier d'en-tête est inclus à nouveau, le préprocesseur générera une erreur, car le symbole est déjà défini. Pour éviter ce genre d'erreur, les fichiers d'en-tête sont protégés par un garde :

```c
#ifndef MATH_H
#define MATH_H

...

#endif // MATH_H
```

Si le fichier a déjà été inclus, la définition `MATH_H` sera déjà déclarée et le fichier d'en-tête ne sera pas ré-inclus.

Le consensus veut que le nom du garde soit le nom du fichier en majuscule avec des underscores à la place des points et des tirets. Par exemple, pour le fichier `foo/bar.h` on utilisera `FOO_BAR_H`. On ajoutera également un commentaire pour indiquer la fin du garde. J'ai personnellement un avis assez défavorable sur cette pratique, car elle engeandre un problème de source de vérité. En effet, si le nom du fichier change, il faudra également changer le nom du garde et je peux vous garantir que bien souvent l'un est réalisé sans l'autre. Cela pose également un problème de suivi de modifications sous Git.

Alternativement une solution est d'avoir une chaîne de caractère unique pour chaque fichier d'en-tête. Cela peut être réalisé en s'énervant sur le clavier. Il y a peu de chance de retrouver une telle chaîne dans un autre fichier. Néanmoins, il est aussi possible de générer une telle chaîne de manière automatique avec un outil comme `uuidgen` ou `openssl rand -hex 16`.

```c
#ifndef FJHJFDKLHSKIOUZEZEUWEHDLKSH
#define FJHJFDKLHSKIOUZEZEUWEHDLKSH

#endif // FJHJFDKLHSKIOUZEZEUWEHDLKSH
```

On préfèrera utiliser la directive [#pragma once](https://en.wikipedia.org/wiki/Pragma_once) qui est plus simple à l'usage et évite une collision de nom. Néanmoins et bien que cette directive ne soit pas standardisée par l'ISO, elle est compatible avec la très grande majorité des compilateurs C.

```c
#pragma once

...
```


[]{#preprocessor-pragma}

## Pragmas (`#pragma`)

Le terme *pragma* est une abréviation de *pragmatic information* (information pragmatique). Les pragmas sont des instructions spécifiques à un compilateur qui permettent de contrôler le comportement du compilateur. Ils sont souvent utilisés pour désactiver des avertissements, spécifier l'alignement mémoire ou encore pour optimiser le code. La directive `#pragma` permet donc de passer des options spécifiques au compilateur, elle n'est par conséquent pas standardisée.

Une utilisation possible avec GCC serait forcer la désactivation d'un avertissement :

```c
#pragma GCC diagnostic ignored "-Wformat"
```

On utilise également un `#pragma` pour forcer l'alignement mémoire d'une structure :

```c
#pragma pack(push, 1)
typedef struct {
    char a;
    int b;
} MyStruct;
#pragma pack(pop)
```

Comme les pragmas ne sont pas standardisées, il est recommandé de les utiliser avec parcimonie et de les documenter correctement.

Notons que si l'on souhaite définir un pragma au sein d'une directive préprocesseur tel qu'une macro, il faudra utiliser l'opérateur unaire `_Pragma` :

```c
#define PRAGMA(x) _Pragma(#x)
```

[]{#preprocessor-exceptions}
## Simulation d'exceptions

Dans des langages de plus haut niveau comme le C++, le Python ou le Java, il existe un mécanisme nommé exception qui permet de gérer des erreurs plus efficacement. Au lieu de retourner une valeur d'erreur, on lève une exception qui sera attrapée plus haut dans la chaîne d'appel.

En C il n'existe pas de mécanisme d'exception, mais il est possible de simuler ce comportement avec des macros et l'instruction `setjmp` et `longjmp` de la librairie standard. `setjmp` permet de sauvegarder l'état du programme à un endroit donné et `longjmp` permet de revenir à cet endroit en sautant les appels de fonctions intermédiaires. Il faut voir `longjmp` comme un `goto` encore plus dangereux.

Cette utilisation n'est pas recommendée car elle peut rendre le code plus obscure et plus difficile à maintenir. Néanmoins dans certains cas de figure, notament pour des programmes embarqués, cette technique peut se révéler très utile.

On définit tout d'abord les macros suivantes dans un fichier `exception.h` :

```c
#pragma once
#include <setjmp.h>

#define TRY do { jmp_buf ex_buf__; if (setjmp(ex_buf__) == 0) {
#define CATCH } else {
#define ETRY } } while (0)
#define THROW longjmp(ex_buf__, 1)
```

On peut ensuite utiliser ces macros pour gérer des erreurs :

```c
#include "exception.h"

void qux(void) {
    printf("qux\n");
    THROW; // Simulate an error !
}

void bar(void) { printf("bar\n"); qux(); }
void foo(void) { printf("foo\n"); bar(); }

int main(void) {
    TRY {
        foo();
    } CATCH {
        printf("An error occured\n");
    } ETRY;
}
```

Dans cet exemple, si la fonction `qux` lève une exception, le programme sautera à la ligne `CATCH` et affichera `An error occured` en court-circuitant les appels de fonctions intermédiaires.

Notez que cette technique est très dangereuse dans le cas de programmes utilisant l'allocation dynamique de mémoire. En effet, si une exception est levée alors que de la mémoire a été allouée, il y aura des fuites mémoires.
