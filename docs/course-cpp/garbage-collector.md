## Collecteur de déchets (*garbage collector*)

Le C est un langage primitif qui ne gère pas automatiquement la libération des ressources allouées dynamiquement. L'exemple suivant est évocateur :

```c
int* get_number() {
    int *num = malloc(sizeof(int));
    *num = rand();
}

int main() {
    for (int i = 0; i < 100; i++) {
        printf("%d\n", *get_number());
    }
}
```

La fonction `get_number` alloue dynamiquement un espace de la taille d'un entier et lui assigne une valeur aléatoire. Dans le programme principal, l'adresse retournée est déréférencée pour être affichée sur la sortie standard.

A la fin de l'exécution de la boucle for, une centaine d'espaces mémoire sont maintenant dans les [limbes](https://fr.wikipedia.org/wiki/Limbes). Comme le pointeur retourné n'a jamais été mémorisé, il n'est plus possible de libérer cet espace mémoire avec `free`.

On dit que le programme à une [fuite mémoire](https://fr.wikipedia.org/wiki/Fuite_de_m%C3%A9moire). En admettant que ce programme reste résidant en mémoire, il peut arriver un moment où le programme peut aller jusqu'à utiliser toute la RAM disponible. Dans ce cas, il est probable que `malloc` retourne `NULL` et qu'une erreur de segmentation apparaisse lors du `printf`.

Allons plus loin dans notre exemple et considérons le code suivant :

```c
#include <stdio.h>
#include <stdlib.h>

int foo(int *new_value) {
    static int *values[10] = { NULL };
    static int count = 0;

    if (rand() % 5 && count < sizeof(values) / sizeof(*values) - 1) {
        values[count++] = new_value;
    }

    if (count > 0)
        printf("Foo aime %d\n", *values[rand() % count]);
}

int bar(int *new_value) {
    static int *values[10] = { NULL };
    static int count = 0;

    if (rand() % 5 && count < sizeof(values) / sizeof(*values) - 1) {
        values[count++] = new_value;
    }

    if (count > 0)
        printf("Bar aime %d\n", *values[rand() % count]);
}

int* get_number() {
    int *number = malloc(sizeof(int));
    *number = rand() % 1000;
    return number;
}

int main() {
    int experiment_iterations = 10;
    for (int i = 0; i < experiment_iterations; i++) {
        int *num = get_number();
        foo(num);
        bar(num);
        #if 0 // ...
            free(num) ??
        #endif
    };
}
```

La fonction `get_number` alloue dynamiquement un espace mémoire et assigne un nombre aléatoire. Les fonctions `foo` et `bar` reçoivent en paramètre un pointeur sur un entier. Chacune à le choix de mémoriser ce pointeur et de clamer sur `stdout` qu'elle aime un des nombres mémorisés.

Au niveau du `#if 0` dans la fonction `main`, il est impossible de savoir si l'adresse pointée par `num` est encore utilisée ou non. Il se peut que `foo` et `bar` utilisent cet espace mémoire, comme il se peut qu'aucun des deux ne l'utilise.

Comment peut-on savoir si il est possible de libérer ou non `num` ?

Une solution couramment utilisée en C++ s'appelle un *smart pointer*. Il s'agit d'un pointeur qui contient en plus de l'adresse de la valeur, le nombre de références utilisées. De cette manière il est possible en tout temps de savoir si le pointeur est référencé quelque part. Dans le cas où le nombre de référence tombe à zéro, il est possible de libérer la ressource.

Dans un certain nombre de langage de programmation comme Python ou Java, il existe un mécanisme automatique nommé *Garbage Collector* et qui, périodiquement, fait un tour de toutes les allocations dynamique pour savoir si elle sont encore référencées ou non. Le cas échéant, le *gc* décide libérer la ressource mémoire. De cette manière il n'est plus nécessaire de faire la chasse aux ressources allouées.

En revanche, en C, il n'existe aucun mécanisme aussi sophistiqué alors prenez garde à bien libérer les ressources utilisées et à éviter d'écrire des fonctions qui allouent du contenu mémoire dynamiquement.
