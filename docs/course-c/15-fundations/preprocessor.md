# Préprocesseur

Figure: Illustration du mécanisme de pré-processing avant la compilation

![Mécanisme de pré-processing avant compilation](/assets/images/preprocessing-fun.drawio)

Comme nous l'avons vu en [introduction][structured-text-programming], le langage C est basé sur une double grammaire, c'est-à-dire qu'avant la compilation du code, un autre processus est appelé visant à préparer le code source avant la compilation.

Le cœur de cette opération est appelé **préprocesseur**. Les instructions du préprocesseur C sont faciles à reconnaître, car elles débutent toutes par le croisillon `#` U+0023, *hash* en anglais et utilisé récemment comme [hashtag](https://fr.wikipedia.org/wiki/Hashtag) sur les réseaux sociaux. Notons au passage que ce caractère était historiquement utilisé par les Anglais sous le dénominatif *pound* (livre). Lorsqu'il est apparu en Europe, il a été confondu avec le caractère dièse `♯` U+266F présent sur les pavés numériques de téléphone.

Le vocabulaire du préprocesseur est le suivant :

| Terme                                          | Description                                     |
| ---------------------------------------------- | ----------------------------------------------- |
| [`#include`][preprocessor-include]             | Inclus un fichier dans le fichier courant       |
| [`#define`][preprocessor-define]               | Crée une définition (Macro)                     |
| [`#undef`][preprocessor-undef]                 | Détruit une définition existante                |
| [`#if defined`][preprocessor-ifdef]            | Teste si une définition existe                  |
| [`#if` .. `#endif`][preprocessor-if]           | Test conditionnel                               |
| [`#`][preprocessor-hash]                       | Opérateur de conversion en chaîne de caractères |
| [`##`][preprocessor-hash-hash]                 | Opérateur de concaténation de chaînes           |
| [`#error "error message"`][preprocessor-error] | Génère une erreur                               |
| [`#pragma`][preprocessor-pragma]               | Directive spécifique au compilateur             |

Le préprocesseur C est indépendant du langage C, c'est-à-dire qu'il peut être exécuté sur n'importe quel type de fichier.

Prenons l'exemple d'une lettre générique d'un cabinet dentaire :

```text
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

Il est possible d'appeler le préprocesseur directement avec l'option `-E` de gcc. Des directives `define` peuvent être renseignées depuis la ligne de commande :

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

Notez que les instructions du préprocesseur (à l'exception des opérateurs de concaténation de conversion en chaîne de caractère) sont des instructions de ligne (*line-wise*), et doivent se terminer par un caractère de fin de ligne.

## Phases de traduction

Le standard décrit quatre phases de pré-processing :

1. Remplacement des caractères spéciaux, décodage des trigraphes, traitement des fin de lignes.
2. Fusionne les lignes utilisant un retour virtuel `\`.
3. Supprime les commentaires, décompose les symboles du préprocesseur
4. Exécute les directives du préprocesseur (`#define` et `#include`)

## Extensions des fichiers

Par convention, et selon le standard GNU, les extensions suivantes sont en vigueur :

`.h`

: Fichier d'en-tête ne comportant que des définitions préprocesseur, des déclarations (structures, unions ...) et des prototypes de fonction, mais aucun code exécutable. Ce fichier sera soumis au préprocesseur.

`.c`

: Fichier source C comportant les implémentations de fonction et les variables globales. Ce fichier sera soumis au préprocesseur.

`.i`

: Fichier source C qui ne sera pas soumis au préprocesseur: `gcc -E -o foo.i foo.c`

`.s`

: Fichier assembleur non soumis au préprocesseur.

`.S`

: Fichier assembleur soumis au préprocesseur. Notons toutefois que cette convention n'est pas  applicable sous Windows, car le système de fichier n'est pas sensible à la casse.

## Inclusion de fichiers

[](){ #preprocessor-include }

### #include

La directive include peut prendre deux formes, l'inclusion locale et l'inclusion globale. Il s'agit d'ailleurs de l'une des questions les plus posées (c.f. [cette question](https://stackoverflow.com/questions/21593/what-is-the-difference-between-include-filename-and-include-filename).).

`#include <filename>`

: Le préprocesseur va chercher le chemin du fichier à inclure dans les chemins de l'implémentation.

`#include "filename"`

: Le préprocesseur cherche le chemin du fichier à partir du chemin courant et les chemins donnés par les des directives `-I`.

L'inclusion de fichier est simplement du remplacement de chaînes :

```console
$ echo "Ce début de phrase est ici" > head.h
$ echo ", mais cette fin est là." > tail.h
$ echo -e '#include "head.h"\n#include "tail.h"\n' > main.c
$ gcc -E main.c -o-
# 1 "main.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 31 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 32 "<command-line>" 2
# 1 "main.c"
# 1 "head.h" 1
Ce début de phrase est ici
# 2 "main.c" 2
# 1 "tail.h" 1
, mais cette fin est là.
# 3 "main.c" 2
```

La directive `#include` est principalement utilisée pour inclure des fichiers d'en-tête (*header*), mais rarement (jamais), des fichiers C.

## Définitions

[](){ #preprocessor-define }

### #define

Les définitions sont des symboles généralement écrits en majuscule et qui sont remplacés par le préprocesseur. Ces définitions peuvent être utiles pour définir des constantes globales qui sont définies à la compilation :

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

Il est ainsi possible de définir la taille du tableau à la compilation avec :

```console
$ gcc main.c -DWINDOW_SIZE=42
```

Notons qu'au pré-processing, toute occurrence d'un symbole défini est remplacée par le contenu de sa définition. **C'est un remplacement de chaîne bête, idiot et naïf**. Il est par conséquent possible d'écrire :

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

On relèvera qu'il est aussi possible de commettre certaines erreurs :

```c
#define ADD a + b

int a = 12;
int b = 23;
int c = ADD * ADD
```

Après pré-processing on aura un comportement non désiré, car la multiplication est plus prioritaire que l'addition.

```c
#define ADD a + b

int a = 12;
int b = 23;
int c = a + b * a + b
```

Pour se prémunir contre ces éventuelles coquilles, on protègera toujours les définitions avec des parenthèses `#define ADD (a + b)`.

[](){ #preprocessor-ifdef }

### #if defined

[](){ #preprocessor-if }

### #if

[](){ #preprocessor-undef }

### #undef

Un symbole défini soit par la ligne de commande `-DFOO=1`, soit par la directive `#define FOO 1` ne peut pas être redéfini. C'est pourquoi il est possible d'utiliser `#undef` pour supprimer une directive préprocesseur :

```c
#ifdef FOO
#   undef FOO
#endif
#define FOO 1
```

Généralement on évitera de faire appel à `#undef` car le bon programmeur aura forcé la définition d'une directive en amont pour contraindre le développement en aval.

## Débogage

[](){ #preprocessor-error }

### #error

Cette directive génère une erreur avec le texte qui suit la directive :

```c
#if !(KERNEL_SIZE % 2)
#    error Le noyau du filtre est pair
#endif
```

### Directives spéciales

Le standard définit certains symboles utiles pour le débogage :

`__LINE__`

: Est remplacé par le numéro de la ligne sur laquelle est placé ce symbole

`__FILE__`

: Est remplacé par le nom du fichier sur lequel est placé ce symbole

`__func__`

: Est remplacé par le nom de la fonction du bloc dans lequel la directive se trouve

`__STDC__`

: Est remplacé par 1 pour indiquer que l'implémentation est compatible avec C90

`__DATE__`

: Est remplacé par la date sous la forme `"Mmm dd yyyy"`

`__TIME__`

: Est remplacé par l'heure au moment du pre-processing `"hh:mm:ss"`

## Caractère d'échappement

L'anti-slash (`backslash`) est interprété par le préprocesseur comme un saut de ligne virtuel. Il permet par exemple de casser les longues lignes :

```c
#define TRACE printf("Le programme est passé " \
    " dans le fichier %s" \
    " ligne %d\n", \
    __FILE__, __LINE__);
```

## Macros

Une macro est une définition qui prend des arguments en paramètre :

```c
#define MIN(x, y) ((x) < (y) ? (x) : (y))
```

De la même manière que pour les définitions simples, il s'agit d'un remplacement de chaîne :

```console
$ cat test.c
#define MIN(x, y) ((x) < (y) ? (x) : (y))

int main(void) {
    return MIN(23, 12);
}

$ gcc -E test.c -o-
int main(void) {
    return ((23) < (12) ? (23) : (12));
}
```

Notez que l'absence d'espace entre le nom de la macro et la parenthèse est importante. L'exemple suivant le démontre :

```console
$ cat test.c
#define ADD (x, y) ((x) + (y))

int main(void) {
    return ADD(23, 12);
}

$ gcc -E test.c -o-
int main(void) {
    return (x, y) ((x) + (y))(23, 12);
}
```

!!! warning "Macro avec paramètres"

    Le préprocesseur interprète une macro avec paramètres que si la parenthèse ouvrante suit directement et sans espace le nom de la macro. Ainsi, considérant cet exemple :

    ```c
    #define f (x) ((x) + 1)

    int u = f(1)
    ```

    Le préprocesseur génère ceci et le compilateur retournera une erreur du type `identification x non déclarés`.

    ```c
    int u = (x) ((x) + 1)(1)
    ```

    Observations :

    - Ne jamais mettre d'espace entre le nom d'une macro et ses paramètres.
    - Être toujours prêt à mettre en doute le code généré par une macro.

!!! warning "Paramètres de macro non protégés"

    On ne le répètera jamais assez: une macro est un remplacement de chaîne effectué par le préprocesseur. Donc écrire `#!c #define m(x) x * 2` et `m(2 + 5)` sera remplacé en `2 + 5 * 2`.

    Quel sera le problème dans le cas suivant ?

    ```c
    #define ABS(x) x >= 0 ? x: -x

    int foo(void) {
        return ABS(5 - 8);
    }
    ```

    Plus difficile, quel serait le problème ici :

    ```c
    #define ERROR(str) printf("Erreur: %s\r\n", str); log(str);

    if (y < 0)
        ERROR("Zero division");
    else
        x = x / y;
    ```

    Observations :

    - Toujours protéger les paramètres des macros avec des parenthèses

        ```c
        #define ABS(x) ((x) >= 0 ? (x): -(x))
        ```

    - Toujours protéger une macro à plusieurs instructions par une boucle vide :

        ```c
        #define ERROR(str) do { \
            printf("Erreur: %s\r\n", str); \
            log(str); \
        } while (0)
        ```

!!! warning "Pré/Post incrémentation avec une macro"

    On pourrait se dire qu'avec toutes les précautions prises, il n'y aura plus d'ennuis possibles. Or, les post/pré incréments peuvent encore poser problème.

    ```c
    #define ABS(x) ((x) >= 0 ? (x) : -(x))

    return ABS(x++)
    ```

    On peut constater que x sera post-incrémenté deux fois au lieu d'une :

    ```c
    #define ABS(x) ((x) >= 0 ? (x) : -(x))

    return ((x++) >= 0 ? (x++) : -(x++))
    ```

    Observations :

    - Éviter l'utilisation de la pre/post incrémentation/décrémentation dans l'appel de macros.

[](){ #preprocessor-hash-hash }

## Concaténation de chaînes

Parfois il est utile de vouloir concaténer deux symboles comme si ce n'était qu'un seul. Attention, il est nécessaire de passer par une macro pour que cela fonctionne :

```c
int foobar = 42;

#define CONCAT(a, b) a ## b
printf("%d", CONCAT(foo, bar));
```

En appelant seulement le préprocesseur, on constate ce résultat :

```sh
$ gcc -E ww.c
int foobar = 42;

printf("%d", foobar);
```

L'usage le plus courant est de définir le *mangling* des noms de fonctions :

```c
#define MANGLE(name) prefix_ ## name ## _suffix

void MANGLE(foo)(void) {
    printf("Hello");
}

int main() {
    MANGLE(foo)();
}
```

En effet le langage C ne permet pas de définir des fonctions avec le même nom, même si elles ont des signatures différentes et même si elles sont dans deux fichiers séparés. Le *mangling* permet de contourner cette limitation.

Par exemple si vous avez une bibliothèque qui permet de lire des fichiers XML, vous pourriez avoir une fonction `read` pour lire un fichier XML et une fonction `read` pour lire un fichier JSON. Si vous avez besoin des deux bibliothèques et que le nom des fonctions est le même, vous aurez un conflit.

Les développeurs autorisent l'utilisateur de la bibliothèque, pour autant que l'utilisateur ait accès au code source, à renommer les fonctions.

En utilisant le *mangling* vous pourriez définir `xml_read` et `json_read` pour éviter les conflits.

[](){ #preprocessor-hash }

## Conversion en chaîne

Il est possible de convertir un symbole en chaîne de caractères avec l'opérateur `#` :

```c
#define STR(x) #x
printf("%s", STR(42));
```

## Directives conditionnelles

Les directives `#if`, `#else`, `#elif` et `#endif` sont utiles pour rendre conditionnelle une section de code. Cela peut être utilisé pour définir une structure selon le boutisme de l'architecture cible :

```c
#ifdef BIG_ENDIAN
typedef struct {
    int header;
    int body;
    int tail;
} Dataframe;
#else
typedef struct {
    int tail;
    int body;
    int header;
} Dataframe;
#endif
```

### Désactivation de code

On voit souvent des développeurs commenter des sections de code pour le débogage. Cette pratique n'est pas recommandée, car les outils de [refactoring](https://en.wikipedia.org/wiki/Code_refactoring) (réusinage de code), ne parviendront pas à interpréter le code en commentaire jugeant qu'il ne s'agit pas de code, mais de texte insignifiant. Une méthode plus robuste et plus sure consiste à utiliser une directive conditionnelle :

```c
#if 0 // TODO: Check if this code is still required.
if (x < 0) {
    x = 0;
}
#endif
```

### Include guard

La protection des fichiers d'en-tête permet d'éviter d'inclure un fichier s'il a déjà été inclus.

Imaginons que la constante `M_PI` soit définie dans le header `<math.h>`:

```c
#define M_PI  3.14159265358979323846
```

Si ce fichier d'en-tête est inclus à nouveau, le préprocesseur générera une erreur, car le symbole est déjà défini. Pour éviter ce genre d'erreur, les fichiers d'en-tête sont protégés par un garde :

```c
#ifndef MATH_H
#define MATH_H

...

#endif
```

Si le fichier a déjà été inclus, la définition `MATH_H` sera déjà déclarée et le fichier d'en-tête ne sera pas ré-inclus.

On préfèrera utiliser la directive [#pragma once](https://en.wikipedia.org/wiki/Pragma_once) qui est plus simple à l'usage et évite une collision de nom. Néanmoins et bien que cette directive ne soit pas standardisée par l'ISO, elle est compatible avec la très grande majorité des compilateurs C.

```c
#pragma once

...
```

## Commentaires

Les commentaires C du type suivant sont aussi des directives du préprocesseur. Ils seront retirés par le préprocesseur :

```c
// Blabla

/**
 * Le corbeau et le renard.
 */
```

!!! exercise "Macro compromise ?"

    Que pensez-vous de cette définition ?

    ```c
    #define IS_OCTAL(c) ((c) >= '0' && (c) <= '8')
    ```

## Usages avancés

[](){ #preprocessor-pragma }

### #pragma

La directive `#pragma` est une directive spécifique à un compilateur. Elle permet de passer des options spécifiques au compilateur, elle n'est par conséquent pas standardisée. Par exemple, pour désactiver un warning :

```c
#pragma GCC diagnostic ignored "-Wformat"
```

On utilise également `#pragma` forcer l'alignement mémoire d'une structure :

```c
#pragma pack(push, 1)
typedef struct {
    char a;
    int b;
} MyStruct;
#pragma pack(pop)
```

### Simulation d'exceptions

Il est possible de simuler des exceptions en C en utilisant les directives du préprocesseur :

```c
#define TRY do { jmp_buf ex_buf__; if (setjmp(ex_buf__) == 0) {
#define CATCH } else {
#define ETRY } } while (0)
#define THROW longjmp(ex_buf__, 1)
```

### Débogage

Il est possible de définir des macros pour le débogage :

```c
#ifdef DEBUG
#    define TRACE printf("Trace: %s:%d\n", __FILE__, __LINE__)
#else
#    define TRACE
#endif
```
