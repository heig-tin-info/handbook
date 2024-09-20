# Programmation générique

La programmation générique est une technique de programmation qui permet de définir des algorithmes et des structures de données qui peuvent être utilisés avec différents types de données. En C, la programmation générique est réalisée à l'aide de macros, de types et de fonctions inline.

Écrire un code générique est le Graal de tout programmeur. Cela permet de réutiliser du code et de le rendre plus robuste. En effet, un code générique est un code qui peut être utilisé avec différents types de données et différentes configuration sans modification. Cela permet de réduire la duplication de code et d'améliorer la maintenabilité du code.

Néanmoins, la programmation générique en C est limitée par le fait que le langage n'est pas orienté objet et ne possède pas de couche de méta-programmation comme les *templates* en C++. Certains développeurs ont été jusqu'à inventer un nouveau langage comme le Vala pour palier à ces limitations. Vala est un meta-langage qui génère du code C à partir de code Vala. Il apporte le paradigme de la programmation orientée objet et de la programmation générique à C. Cependant, Vala n'est pas un langage très répandu en dehors de la communauté GNOME.

[](){#generickw}
## Fonctions génériques

Prenons l'exemple de la fonction d'addition suivante. Elle est écrite pour des entiers et ne fonctionnera donc pas pour des flottants. Il faudrait la réécrire pour les flottants mais cela implique une collision de nom de fonction. Il faudrait alors définir autant de fonctions que de types avec des suffixes différents (`add_int`, `add_float`, etc.).

```c
int add(int a, int b) { return a + b; }
```

Alternativement, on peut utiliser des macros pour définir des fonctions génériques. Par exemple, la macro suivante permet de définir une fonction d'addition pour n'importe quel type de données:

```c
#define add(a, b) ((a) + (b))
```

Néanmoins cette macro ne fonctionne que pour des fonctions simples. Pour des fonctions plus complexes, il est nécessaire de définir des fonctions séparées pour chaque type de données comme discuté précédemment :

```
int add_int(int a, int b) { return a + b; }
float add_float(float a, float b) { return a + b; }
```

Pour obtenir un comportement générique, on peut utiliser le mot-clé `_Generic` introduit dans C11. `_Generic` permet de définir une fonction en fonction du type de données passé en paramètre. Par exemple, la fonction suivante permet d'additionner des entiers ou des flottants :

```c
#define add(a, b) _Generic((a), \
    int: add_int, \
    float: add_float \
)(a, b)
```

Le fonctionnement de `_Generic` est le suivant : le premier argument est une expression qui est évaluée pour déterminer le type de données. Ensuite, `_Generic` compare le type de données avec les types définis dans la liste. Si le type de données correspond à un type défini, alors la fonction correspondante est appelée avec les arguments `a` et `b`. L'exemple donné n'est pas très pertinent car la solution simple avec une macro est plus simple et plus lisible. Néanmoins, `_Generic` est très utile pour des fonctions plus complexes. Prenons l'exemple de la fonction `print` qui affiche un entier ou un flottant :

```c
#include <stdio.h>

void print_int(int x) { printf("Entier : %d\n", x); }
void print_float(float x) { printf("Flottant : %.2f\n", x); }
void print_string(const char *x) { printf("Chaîne : %s\n", x); }

#define print(x) _Generic((x), \
    int: print_int, \
    float: print_float, \
    const char*: print_string \
)(x)

int main() {
    int a = 10;
    float b = 5.5;
    const char *c = "Bonjour";

    print(a);
    print(b);
    print(c);
}
```

Dans le standard C, l'en-tête `<tgmath.h>` fournit par exemple des fonctions génériques pour les fonctions mathématiques. Il n'y a donc plus à ce soucier du type de données passé en paramètre ce qui pourrait en théorie créer moins d'erreurs de programmation.

## Tableaux à taille variable

Nous avons vu qu'il est parfaitement correct d'écrire :

```c
int sum(int array[42]);
```

Cependant, cette fonction n'est valable que pour des tableaux de taille fixe à 42 éléments. Pour des tableaux de taille variable, il est nécessaire de passer la taille du tableau en paramètre.

```c
int sum(int *array, size_t size);
```

Notez que la notation est passée de `int array[]` à `int *array`. Cela met l'accent sur le fait que `array` est un pointeur et non un type tableau. L'avantage du pointeur est que l'on peut le parcourir avec une boucle `for` en utilisant l'arithmétique des pointeurs.

```c
int sum(int *array, size_t size) {
   int sum = 0, *end = array + size;
   while (array < end) sum += *(array++);
   return sum;
}
```

## Fonction de callback

Dans des algorithmes comme le tri d'un tableau. Il est possible de parcourir le tableau facilement si l'on connait sa taille et la taille du type de donnée. Cependant, pour comparer deux valeurs, il est nécessaire de connaître la méthode de comparaison car elle dépend du type. On peut utiliser `_Generic` mais cela fonctionnera que pour des types simples et connus.

Une fonction de tri générique ne peut pas connaître tous les types de données. Par exemple imaginons un type comme étant une structure contenant une personne :

```c
typedef struct {
    char *name;
    int age;
} Person;
```

Trier un tableau de personnes demande de savoir comment comparer deux personnes. On peut imaginer une fonction de comparaison qui compare deux personnes en fonction de leur âge ou de leur nom :

```c
int compare_age(Person a, Person b) { return a.age - b.age; }
int compare_name(Person a, Person b) { return strcmp(a.name, b.name); }
```

L'astuce consiste à passer une fonction de comparaison en paramètre de la fonction de tri. Cela permet de trier n'importe quel type de données. Par exemple, la fonction de tri suivante permet de trier un tableau de n'importe quel type de données :

```c
void swap(void *a, void *b, size_t size) {
    char tmp[size];
    memcpy(tmp, a, size);
    memcpy(a, b, size);
    memcpy(b, tmp, size);
}

void sort(void *array, size_t size, size_t count,
    int (*comp)(const void *, const void *))
{
    for (size_t i = 0; i < count; i++) {
        for (size_t j = i + 1; j < count; j++) {
            void *a = (char *)array + i * size;
            void *b = (char *)array + j * size;
            if (comp(a, b) > 0) swap(a, b, size);
        }
    }
}
```

L'utilisation de fonctions de *callback* est un concept fondamental en programmation générique. En C il implique le plus souvent de passer par un pointeur générique `void *` afin de pouvoir définir un prototype de fonction également générique.

La bibliothèque standard C fournit plusieurs fonctions génériques telles que :

```c
// Copie d'une région mémoire
void memcpy(void *dest, const void *src, size_t n);
// Tri rapide d'un tableau
void qsort(void *base, size_t nmemb, size_t size,
    int (*compar)(const void *, const void *));
// Recherche dichotomique
void bsearch(const void *key, const void *base, size_t nmemb, size_t size,
    int (*compar)(const void *, const void *));
```

## Types de données abstraits

Un [type de donnée abstrait](wiki:abstract-type) (**ADT** pour Abstract Data Type) cache généralement une structure dont le contenu n'est pas connu de l'utilisateur final. Ceci est rendu possible par le standard (C99 §6.2.5) par l'usage de types incomplets.

Pour mémoire, un type incomplet décrit un objet dont on ne connaît pas sa taille en mémoire. L'exemple suivant déclare un nouveau type structure qui n'est alors pas (encore) connu dans le fichier courant :

```c
typedef struct Unknown *Known;

int main() {
    Known foo; // Autorisé, le type est incomplet

    foo + 1; // Impossible car la taille de foo est inconnue.
    foo->key; // Impossible car le type est incomplet.
}
```

De façon générale, les types abstraits sont utilisés dans l'écriture de bibliothèques logicielles lorsqu'il est important que l'utilisateur final ne puisse pas compromettre le contenu du type et en forçant cet utilisateur à ne passer que par des fonctions d'accès.

Prenons le cas du fichier `foobar.c` lequel décrit une structure `struct Foo` et un type `Foo`. Notez que le type peut être déclaré avant la structure. `Foo` restera abstrait jusqu'à la déclaration complète de la structure `struct Foo` permettant de connaître sa taille. Ce fichier contient également trois fonctions :

- `init` permet d'initialiser la structure ;
- `get` permet de récupérer la valeur contenue dans `Foo` ;
- `set` permet d'assigner une valeur à `Foo`.

En plus, il existe un compteur d'accès `count` qui s'incrémente lorsque l'on assigne une valeur et se décrémente lorsque l'on récupère une valeur.

```c
#include <stdlib.h>

typedef struct Foo Foo;

struct Foo {
    int value;
    int count;
};

void init(Foo** foo) {
    *foo = malloc(sizeof(Foo)); // Allocation dynamique
    (*foo)->count = (*foo)->value = 0;
}

int get(Foo* foo) {
    foo->count--;
    return foo->value;
}

void set(Foo* foo, int value) {
    foo->count++;
    foo->value = value;
}
```

Évidemment, on ne souhaite pas qu'un petit malin compromette ce compteur en écrivant maladroitement :

```c
foo->count = 42; // Hacked this !
```

Pour s'en protéger, on a recours à la compilation séparée (voir chapitre sur la compilation séparée [TranslationUnits]) dans laquelle le programme est découpé en plusieurs fichiers. Le fichier `foobar.h` contiendra tout ce qui doit être connu du programme principal, à savoir les prototypes des fonctions, et le type abstrait :

```c
#pragma once

typedef struct Foo Foo;

void init(Foo** foo);
int get(Foo* foo);
void set(Foo* foo, int value);
```

Ce fichier sera inclus dans le programme principal `main.c` :

```c
#include "foobar.h"
#include <stdio.h>

int main() {
    Foo *foo;

    init(&foo);
    set(foo, 23);
    printf("%d\n", get(foo));
}
```

Un type abstrait peut être vu comme une boîte noire et est par conséquent une technique de programmation générique. Il est possible de définir des types abstraits pour des structures plus complexes comme des listes chaînées, des arbres, des graphes, mais que l'utilisateur final ne doit pas nécessairement connaître.