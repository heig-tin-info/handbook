# Chaînes de caractères

Une chaîne de caractères est représentée en mémoire comme une succession de bytes, chacun représentant un caractère ASCII spécifique. La chaîne de caractère `hello` contient donc 5 caractères et sera stockée en mémoire sur 5 bytes. Une chaîne de caractère est donc équivalente à un tableau de `char`.

En C, un artifice est utilisé pour faciliter les opérations sur les chaînes de caractères. Tous les caractères de 1 à 255 sont utilisables sauf le 0 qui est utilisé comme sentinelle. Lors de la déclaration d'une chaîne comme ceci :

```c
char str[] = "hello, world!";
```

Le compilateur ajoutera automatiquement un caractère de terminaison `'\0'` à la fin de la chaîne. Pour en comprendre l'utilité, imaginons une fonction qui permet de compter la longueur de la chaîne. Elle aurait comme prototype ceci :

```c
size_t strlen(const char str[]);
```

On peut donc lui passer un tableau dont la taille n'est pas définie et par conséquent, il n'est pas possible de connaître la taille de la chaîne passée sans le bénéfice d'une sentinelle.

```c
size_t strlen(const char str[]) {
    size_t len = 0,
    while (str[len++] != '\0') {}
    return len;
}
```

Une chaîne de caractère est donc strictement identique à un tableau de `char`.

Ainsi une chaîne de caractère est initialisée comme suit :

```c
char str[] = "Pulp Fiction";
```

La taille de ce tableau sera donc de 12 caractères plus une sentinelle `'\0'` insérée automatiquement. Cette écriture est donc identique à :

```c
char str[] = {'P', 'u', 'l', 'p', ' ', 'F', 'i', 'c', 't', 'i', 'o', 'n', '\0'};
```

## Tableaux de chaînes de caractères

Un tableau de chaîne de caractères est identique à un tableau multidimensionnel :

```c
char conjunctions[][10] = {"mais", "ou", "est", "donc", "or", "ni", "car"};
```

Il est ici nécessaire de définir la taille de la seconde dimension, comme pour les tableaux. C'est-à-dire que la variable `conjunctions` aura une taille de 7x10 caractères et le contenu mémoire de `conjunctions[1]` sera équivalent à :

```c
{'o', 'u', 0, 0, 0, 0, 0, 0, 0, 0}
```

D'ailleurs, ce tableau aurait pu être initialisé d'une tout autre façon :

```c
char conjunctions[][10] = {
    'm', 'a', 'i', 's', 0, 0, 0, 0, 0, 0, 'o', 'u', 0, 0, 0,
    0, 0, 0, 0, 0, 'e', 's', 't', 0, 0, 0, 0, 0, 0 , 0, 'd',
    'o', 'n', 'c', 0, 0, 0, 0, 0 , 0, 'o', 'r', 0, 0, 0, 0,
    0, 0, 0, 0, 'n', 'i', 0, 0, 0, 0, 0, 0, 0, 0, 'c', 'a',
    'r', 0, 0, 0, 0, 0, 0, 0,
};
```

Notons que la valeur `0` est strictement identique au caractère 0 de la table ASCII `'\0'`. La chaîne de caractère `"mais"` aura une taille de 5 caractères, ponctuée de la sentinelle `\0`.

## Wide-chars

Les chaînes de caractères larges sont des chaînes de caractères qui utilisent plus d'un byte pour représenter un caractère. En C, les chaînes de caractères larges sont représentées par le type `wchar_t`. Pour déclarer une chaîne de caractères larges, il est nécessaire d'utiliser le préfixe `L` :

```c
wchar_t wstr[] = L"Hello, 世界";
```

Ce type de chaîne de caractères est typiquement utilisé pour représenter des caractères Unicode. Comme nous l'avons vu au chapitre sur les [types de données](#unicode), les caractères qui ne sont pas dans la table ASCII sont représentés par plusieurs bytes. La fameuse émoji `👋` est représentée par 5 bytes U+1F44B.

L'en-tête `wchar.h` contient les fonctions pour manipuler les chaînes de caractères larges. Par exemple, pour obtenir la longueur d'une chaîne de caractères larges, on utilise la fonction `wcslen` :

```c
#include <wchar.h>

int main(void) {
    wchar_t wstr[] = L"Hello, 世界";
    size_t len = wcslen(wstr);
    assert(len == 9);

    char str[] = L"Hello, 世界";
    size_t len = strlen(str);
    assert(len == 13);
}
```

En pratique les chaînes de caractères larges sont peu utilisées en C, car elles sont moins efficaces que les chaînes de caractères ASCII. En effet, les chaînes de caractères larges nécessitent plus de mémoire pour stocker les caractères et les opérations sur ces chaînes sont plus lentes.

De plus, elles ne sont pas portables, car la taille d'un `wchar_t` dépend de l'implémentation. Par exemple, sur Windows, un `wchar_t` est de 16 bits, alors que sur Linux, il est de 32 bits. Et comme nous l'avons les emojis peuvent être codés sur plus de 16 bits.

Pour ces raisons, on préfère utiliser l'UTF-8 pour représenter les caractères Unicode en C. L'UTF-8 est un encodage de caractères Unicode qui utilise un à quatre bytes pour représenter un caractère. Il est compatible avec l'ASCII et est plus efficace que les chaînes de caractères larges. Il fonctionne de la manière suivante :

- Les caractères U+0000 à U+007F sont codés sur un byte.
- Les caractères au delà de U+007F sont codés sur plusieurs bytes.

```text
0x00 - 0x7F         0b0xxxxxxx où x est le code ASCII sur 7-bits
0x80 - 0x7FF        0b110xxxxx 0b10xxxxxx
0x800 - 0xFFFF      0b1110xxxx 0b10xxxxxx 0b10xxxxxx
0x10000 - 0x10FFFF  0b11110xxx 0b10xxxxxx 0b10xxxxxx 0b10xxxxxx
```

Prenons l'exemple du caractère `👋`. Sa représentation binaire utilise 21 bits et nécessite donc une séquence de 4 octets.

```text
U+1F44B = 0b0001 1111 0100 0100 1011
```

En UTF-8, il sera représenté par la séquence de bytes suivante :

```text
0b11110xxx 0b10xxxxxx 0b10xxxxxx 0b10xxxxxx
       000     011111     010001     001011

0xF0       0x9F       0x91       0x8B
```

Donc la longueur de la chaîne de caractère avec `strlen` sera de 4 et non de 1.

```c
char str[] = "👋";
size_t len = strlen(str);
assert(len == 4);
```

Pour connaître la longueur d'une chaîne de caractères en UTF-8, il est nécessaire de la faire à la main:

```c
#include <stdio.h>

size_t utf8_strlen(const char *s) {
    size_t length = 0;

    while (*s) {
        // Si on trouve 0b10xxxxxx, c'est un byte de continuation
        // on l'ignore...
        if ((*s & 0xC0) != 0x80) length++;
        s++;
    }

    return length;
}

int main() {
    const char *str = "Hello, 👋 World!";
    size_t len = utf8_strlen(str);
    printf("The string length is: %zu characters\n", len);
}
```

## Buffer (tampon)

Bien souvent, les chaînes de caractères sont manipulées dans des buffers. Un buffer est un tableau de caractères d'une taille fixe utilisé pour stocker des données intermédiaires. Un cas typique est la lecture depuis l'entrée standard.

Admettons que l'on souhaite lire le nom d'un utilisateur depuis l'entrée standard. On peut définir un buffer de 256 caractères pour stocker le nom de l'utilisateur :

```c
#include <stdio.h>

int main(void) {
    char name[32];
    printf("Enter your name: ");
    scanf("%31s", name);
}
```

Dans cet exemple, `name` est un buffer de 32 caractères. La fonction `scanf` lit au maximum 31 caractères depuis l'entrée standard et les stocke dans `name`. La taille du buffer est de 32 caractères pour laisser de la place pour la sentinelle `\0`. Sans cette sécurité, il serait possible de déborder le buffer et d'écrire dans des zones mémoires qui ne nous appartiennent pas.

## Chaîne de caractères multi-lignes

En C, il n'est pas possible de déclarer une chaîne de caractères sur plusieurs lignes. Pour ce faire, il est nécessaire de concaténer plusieurs chaînes de caractères :

```c
char *str = "Hello, "
            "World!";
```

Dans cet exemple, `str` contiendra la chaîne de caractères `Hello, World!`.

## Chaîne de caractères constantes

Les chaînes de caractères constantes sont des chaînes de caractères qui ne peuvent pas être modifiées. Elles sont stockées dans la section `.rodata` de la mémoire. Pour déclarer une chaîne de caractères constante, il est nécessaire d'utiliser le mot-clé `const` :

```c
const char *str = "Hello, World!";
```

Notez que la déclaration est un peu différente de la déclaration d'une chaîne de caractères classique. Ici nous n'utilisons plus la notation `[]` mais un pointeur `*`.
