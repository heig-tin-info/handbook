# Avancé

Ce chapitre regroupe les sujets avancés dont la compréhension n'est pas requise pour le contrôle de connaissance.

## Points de séquences

On appelle un point de séquence ou [sequence point](https://en.wikipedia.org/wiki/Sequence_point) exprimé dans l'annexe C du standard C99 chaque élément de code dont l'exécution est garantie avant la séquence suivante. Ce qu'il est important de retenir c'est :

- L'appel d'une fonction est effectué après que tous ses arguments ont été évalués

- La fin du premier opérande dans les opérations `&&`, `||`, `?` et `,`.

    - Ceci permet de court-circuiter le calcul dans ``` a() && b() ``. La condition ``b() ``` n'est jamais évaluée si la condition `a()` est valide.

- Avant et après des actions associées à un formatage d'entrée sortie

L'opérateur d'assignation `=` n'est donc pas un point de séquence et l'exécution du code `(a = 2) + a + (a = 2)` est par conséquent indéterminée.

## Complément sur les variables initialisées

Le fait de déclarer des variables dans en langage C implique que le
logiciel doit réaliser l'initialisation de ces variables au tout début
de son exécution. De fait, on peut remarquer deux choses. Il y a les
variables initialisées à la valeur zéro et les variables initialisées à
des valeurs différentes de zéro. Le compilateur regroupe en mémoire ces
variables en deux catégories et ajoute un bout de code au début de votre
application (qui est exécuté avant le *main*).

Ce code (que l'on n'a pas à écrire) effectue les opérations suivantes :

- mise à zéro du bloc mémoire contenant les variables ayant été
  déclarées avec une valeur d'initialisation à zéro
- recopie d'une zone mémoire contenant les valeurs initiales des
  variables ayant été déclarées avec une valeur d'initialisation
  différente de zéro vers la zone de ces mêmes variables.

Par ce fait, dès que l'exécution du logiciel est effectuée, on a, lors
de l'exécution du *main*, des variables correctement initialisées.

## Binutils

Les outils binaires ([binutils](https://en.wikipedia.org/wiki/GNU_Binutils)) sont une collection de programmes installés avec un compilateur et permettant d'aider au développement et au débogage. Certains de ces outils sont très pratiques, mais nombreux sont les développeurs qui ne les connaissent pas.

`nm`

: Liste tous les symboles dans un fichier objet (binaire). Ce programme appliqué sur le programme hello world de l'introduction donne :

  ```console
  $ nm a.out
  0000000000200dc8 d _DYNAMIC
  0000000000200fb8 d _GLOBAL_OFFSET_TABLE_
  00000000000006f0 R _IO_stdin_used
                  w _ITM_deregisterTMCloneTable
                  w _ITM_registerTMCloneTable

  ...

                  U __libc_start_main@@GLIBC_2.2.5
  0000000000201010 D _edata
  0000000000201018 B _end
  00000000000006e4 T _fini
  00000000000004f0 T _init
  0000000000000540 T _start

  ...

  000000000000064a T main
                   U printf@@GLIBC_2.2.5
  00000000000005b0 t register_tm_clones
  ```

  On observe notamment que la fonction `printf` est en provenance de la bibliothèque GLIBC 2.2.5, et qu'il y a une fonction `main`.

`strings`

: Liste toutes les chaînes de caractères imprimables dans un fichier binaire. On observe tous les symboles de débogue qui sont par défaut intégrés au fichier exécutable. On lit également la chaîne de caractère `hello, world`. Attention donc à ne pas laisser les éventuels mots de passes ou numéro de licence en clair dans un fichier binaire.

  ```console
  $ strings a.out
  /lib64/ld-linux-x86-64.so.2
  libc.so.6
  printf

  ...

  AUATL
  []A\A]A^A_
  hello, world
  ;*3$"
  GCC: (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0

  ...

  _IO_stdin_used
  __libc_csu_init
  __bss_start
  main
  __TMC_END__
  _ITM_registerTMCloneTable
  __cxa_finalize@@GLIBC_2.2.5
  .symtab
  .strtab

  ...

  .data
  .bss
  .comment
  ```

`size`

: Lister la taille des segments mémoires utilisés. Ici le programme représente 1517 bytes, les données initialisées 8 bytes, les données variables 600 bytes, soit une somme décimale de 2125 bytes ou `84d` bytes.

  ```console
  $ size a.out
  text    data     bss     dec     hex filename
  1517     600       8    2125     84d a.out
  ```

## Format Q

Le format [Q](<https://en.wikipedia.org/wiki/Q_(number_format)>) est une notation en virgule fixe dans laquelle le format d'un nombre est représenté par la lettre **Q** suivie de deux nombres :

1. Le nombre de bits entiers
2. Le nombre de bits fractionnaires

Ainsi, un registre 16 bits contenant un nombre allant de +0.999 à -1.0 s'exprimera **Q1.15** soit 1 + 15 valant 16 bits.

Pour exprimer la valeur pi (3.1415...) il faudra au minimum 3 bits pour représenter la partie entière, car le bit de signe doit rester à zéro. Le format sur 16 bits sera ainsi **Q4.12**.

La construction de ce nombre est facile :

1. Prendre le nombre réel
2. Le multiplier par 2 à la puissance du nombre de bits
3. Prendre la partie entière

```text
1.    3.1415926535
2.    2**12 * 3.1415926535 = 12867.963508736
3.    12867
```

Pour convertir un nombre **Q4.12** en sa valeur réelle il faut :

1. Prendre le nombre encodé en **Q4.12**
2. Diviser sa valeur 2 à la puissance du nombre de bits

```text
1.    12867
2.    12867 / 2**12 = 3.141357421875
```

On note une perte de précision puisqu'il n'est pas possible d'encoder un tel nombre dans seulement 16 bits. L'incrément positif minimal serait : $1 / 2^12 = 0.00024$. Il convient alors d'arrondir le nombre à la troisième décimale soit 3.141.

Les opérations arithmétiques sont possibles facilement entre des nombres de mêmes types.

### Addition

L'addition peut se faire avec ou sans saturation :

```c
typedef int16_t Q;
typedef Q Q12;

Q q_add(Q a, Q b) {
    return a + b;
}

Q q_add_sat(Q a, Q b) {
    int32_t res = (int32_t)a + (int32_t)b;
    res = res > 0x7FFF ? 0x7FFF : res
    res = res < -1 * 0x8000 ? -1 * 0x8000 : res;
    return (Q)res;
}
```

### Multiplication

Soit deux nombres 0.9 et 3.141 :

```text
┌─┬─┬─┬─╀─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│0│0│1│1│1│0││0│1│1│0│0│1│1│0│ Q4.12 (0.9) 3686
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘

┌─┬─┬─┬─╀─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│1│1│0│0│1│0││0│1│0│0│0│0│1│1│ Q4.12 (3.141) 12867
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘
```

Multiplier ces deux valeurs revient à une multiplication sur 2 fois la taille. Le résultat doit être obtenu sur 32-bits sachant que les nombre **Q** s'additionnent comme **Q4.12** x **Q4.12** donnera **Q8.24**.

On voit immédiatement que la partie entière vaut 2, donc 90% de 3.14 donnera une valeur en dessous de 3. Pour reconstruire une valeur **Q8.8** il convient de supprimer les 16-bits de poids faible.

```text
3686 * 12867 = 47227762

┌─┬─┬─┬─┬─┬─┬─┬─┦┌─┬─┬─┬─┬─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│0│0│0│0│1│0││1│1│0│1│0│0│0│0││1│0│1│0│0│0│1│1││0│1│1│1│0│0│1│0│ Q8.24
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘

┌─┬─┬─┬─┬─┬─┬─┬─┦┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│0│0│0│0│1│0││1│1│0│1│0│0│0│0│ Q8.8
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘
```

```c
inline Q q_sat(int32_t x) {
    x = x > 0x7FFF ? 0x7FFF : x
    x = x < -1 * 0x8000 ? -1 * 0x8000 : x;
    return (Q)x;
}

inline int16_t q_mul(int16_t a, int16_t b, char q)
{
    int32_t c = (int32_t)a * (int32_t)b;
    c += 1 << (q - 1);
    return sat(c >> q);
}

inline int16_t q12_mul(int16_t a, int16_t b)
{
    return q_mul(a, b, 12);
}
```

## Mémoire partagée

Nous le verrons plus loin au chapitre sur la MMU, mais la mémoire d'un processus mémoire (programme) ne peut pas être accédée par un autre programme. Le système d'exploitation l'en empêche.

Lorsque l'on souhaite communiquer entre plusieurs programmes, il est possible d'utiliser différentes méthodes :

- les flux (fichiers, stdin, stdout...)
- la mémoire partagée
- les sockets

Vous avez déjà vu les flux au chapitre précédent, et les sockets ne font pas partie de ce cours d'introduction.

Notons que la mémoire partagée est un mécanisme propre à chaque système d'exploitation. Sous POSIX elle est normalisée et donc un programme compatible POSIX et utilisant la mémoire partagée pourra fonctionner sous Linux, WSL ou macOS, mais pas sous Windows.

C'est principalement l'appel système `mmap` qui est utilisé. Il permet de mapper ou démapper des fichiers ou des périphériques dans la mémoire.

```c
void *mmap(
    void *addr,
    size_t length, // Size in bytes
    int prot,      // Access protection (read/write/execute)
    int flags,     // Attributs (shared/private/anonymous...)
    int fd,
    int offset
);
```

Voici un exemple permettant de réserver un espace partagé en écriture et en lecture entre deux processus :

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

void* create_shared_memory(size_t size) {
    // Accessible en lecture et écriture
    int protection = PROT_READ | PROT_WRITE;

    // D'autres processus peuvent accéder à cet espace
    // lequel est anonyme
    // so only this process and its children will be able to use it:
    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    // The remaining parameters to `mmap()` are not important for this use case,
    // but the manpage for `mmap` explains their purpose.
    return mmap(NULL, size, protection, visibility, -1, 0);
}
```

### File memory mapping

Traditionnellement lorsque l'on souhaite travailler sur un fichier, il convient de l'ouvrir avec `fopen` et de lire son contenu. Lorsque cela est nécessaire, ce fichier est copié en mémoire :

```c
FILE *fp = fopen("foo", "r");
fseek(fp, 0, SEEK_END);
int filesize = ftell(fp);
fseek(fp, 0, SEEK_SET);
char *file = malloc(filesize);
fread(file, filesize, sizeof(char), fp);
fclose(fp);
```

Cette copie n'est pas nécessairement nécessaire. Une approche **POSIX**, qui n'est donc pas couverte par le standard **C99** consiste à lier le fichier dans un espace mémoire partagé.

Ceci nécessite l'utilisation de fonctions bas niveau.

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

int main() {
    int fd = open("foo.txt", O_RDWR, 0600);
    char *addr = mmap(NULL, 100, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    printf("Espace mappé à %p\n", addr);
    printf("Premiers caractères du fichiers : %.*s...\n", 20, addr);
}
```

Les avantages de cette méthode sont :

- pas nécessaire de copier l'intégralité du fichier en mémoire ;
- possibilité de partager le même fichier ouvert entre plusieurs processus ;
- possibilité laissée au système d'exploitation d'utiliser la RAM ou non si les ressources mémoires deviennent tendues.

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

En revanche en C, il n'existe aucun mécanisme aussi sophistiqué alors prenez garde à bien libérer les ressources utilisées et à éviter d'écrire des fonctions qui allouent du contenu mémoire dynamiquement.
