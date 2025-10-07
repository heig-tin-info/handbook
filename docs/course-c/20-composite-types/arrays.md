# Tableaux

Les [tableaux](https://fr.wikipedia.org/wiki/Tableau_(structure_de_donn%C3%A9es)) (*arrays*) représentent une séquence finie d'éléments d'un type donné que l'on peut accéder par leur position (indice) dans la séquence. Un tableau est par conséquent une liste indexée de variables du même type.

Un exemple typique d'utilisation d'un tableau est le [Crible d'Ératosthène](https://fr.wikipedia.org/wiki/Crible_d%27%C3%89ratosth%C3%A8ne) qui permet de trouver tous les nombres premiers inférieurs à un entier donné. Dans cet algorithme, un tableau de booléens est utilisé pour marquer les nombres qui ne sont pas premiers. Le code est en 4 parties. D'abord la capture d'une valeur donnée par l'utilisateur stockée dans `n`, puis l'initialisation des valeurs du tableau à `true` avec une boucle, suivi de l'algorithme du crible qui contient deux boucles imbriquées et enfin l'affichage du résultat. Notons que la plus ancienne référence connue au crible (en grec ancien : κόσκινον Ἐρατοσθένους, kóskinon Eratosthénous) se trouve dans l'Introduction à l'arithmétique de Nicomachus de Gérasa, un ouvrage du début du IIᵉ siècle de notre ère, qui l'attribue à Ératosthène de Cyrène, un mathématicien grec du IIIᵉ siècle avant J.-C., bien qu'il décrive le criblage par les nombres impairs plutôt que par les nombres premiers.

```c
#define MAX 1000

int main(int argc, char *argv[]) {
   if (argc != 2) return -1;
   int n = atoi(argv[1]);
   if (n > MAX) return -2;

   // At start, all numbers are prime numbers
   bool primes[MAX];
   for (int i = 0; i <= n; i++) primes[i] = true;

   // Ératosthène sieve algorithm
   primes[0] = primes[1] = false;  // 0 et 1 are not prime numbers
   for (int p = 2; p <= sqrt(n); p++)
      if (primes[p])
         for (int i = p * p; i <= n; i += p) primes[i] = false;

   // Display prime numbers
   for (int i = 2; i <= n; i++)
      if (primes[i]) printf("%d ", i);
   printf("\n");
}
```

L'opérateur crochet `[]` est utilisé à la fois pour le déréférencement (accès à un indice du tableau) et pour l'assignation d'une taille à un tableau :

La déclaration d'un tableau d'entiers de dix éléments s'écrit de la façon suivante :

```c
int array[10];
```

Par la suite il est possible d'accéder aux différents éléments ici l'élément 1 et 3 (deuxième et quatrième position du tableau) :

```c
array[1];
array[5 - 2];
```

Imaginons un tableau de `int16_t` de 5 éléments. En mémoire ce tableau est une succession de 10 bytes (5 éléments de 2 bytes chacun).

![Tableau en mémoire](/assets/images/array.drawio)

```c
int16_t array[5] = {0x0201, 0x0403, 0x0605, 0x0807, 0x0A09};
```

Rappelez-vous que les entiers sont stockés en mémoire en *little-endian*, c'est-à-dire que l'octet de poids faible est stocké en premier. Ainsi, l'entier `0x0201` est stocké en mémoire `0x01` puis `0x02`. Lorsque vous accédez à un élément du tableau, chaque élément en mémoire possède une adresse qui lui est propre. Néanmoins lorsque l'on se réfère au tableau dans son ensemble (ici `array`), c'est l'adresse du premier élément qui est retournée, soit `0xffacb10`.

Comme le tableau est de type `int16_t`, chaque élément est de taille 2 bytes, donc lorsque l'on accède à l'élément 3, une arithmétique sur les adresse est effectuée:

$$
\begin{aligned}
\text{array} & = 0xffacb10 \\
\text{array[3]} & = 0xffacb10 + 3 \times 2 = 0xffacb16
\end{aligned}
$$

L'opérateur `sizeof` qui permet de retourner la taille d'une structure de donnée en mémoire est très utile pour les tableaux. Cependant, cet opérateur retourne la taille du tableau en bytes, et non le nombre d'éléments qui le compose. Dans l'exemple suivant `sizeof(array)` retourne $5\cdot2 = 10$ bytes tandis que `sizeof(array[0])` retourne la taille d'un seul élément $2$; et donc, `sizeof(array) / sizeof(array[0])` est le nombre d'éléments de ce tableau, soit 5.

```c
size_t length = sizeof(array) / sizeof(array[0]);
assert (length == 5);
```

!!! warning "L'indice zéro"

    L'index d'un tableau commence toujours à **zéro** et par conséquent l'index maximum d'un tableau de 5 éléments sera 4. Il est donc fréquent dans une boucle d'utiliser `<` et non `<=`:

    ```c
    for(size_t i = 0; i < sizeof(array) / sizeof(array[0]); i++) {
    /* ... */
    }
    ```

Nous le verrons plus tard lorsque nous parlerons des [pointeurs][pointers], mais un tableau **n'est pas** un pointeur : il s'agit d'un type distinct dont la taille est connue du compilateur. En revanche, dans la plupart des expressions, un tableau « se transforme » en pointeur vers son premier élément. C'est cette conversion implicite qui donne l'impression que les deux notions se confondent. Ce qu'il est important de retenir, c'est que lorsqu'un tableau est passé à une fonction comme dans l'exemple suivant, ce n'est pas l'intégralité des données du tableau qui sont copiées sur la pile, mais seulement l'adresse du premier élément.

Une preuve est que le contenu du tableau peut être modifié à distance :

```c
void function(int i[5]) {
   i[2] = 12;
}

int main(void) {
   int array[5] = {0};
   function(array);
   assert(array[2] == 12);
}
```

Un fait remarquable est que l'opérateur `[]` est commutatif. En effet, l'opérateur *crochet* est un sucre syntaxique défini comme :

```c
a[b] == *(a + b)
```

Et cela fonctionne de la même manière avec les tableaux à plusieurs dimensions :

```c
a[1][2] == *(*(a + 1) + 2)
```

Pour résumer, un tableau permet de regrouper dans un même conteneur une liste d'éléments du même type. Il est possible d'accéder à ces éléments par leur indice, et il est possible de passer un tableau à une fonction par référence.

!!! warning "La taille est une constante littérale"

    La taille d'un tableau doit être une constante littérale. Il n'est pas possible de déclarer un tableau avec une taille variable. Par exemple, l'écriture suivante est incorrecte :

    ```c
    size_t size = 10;
    int array[size];
    ```

    En pratique, cet exemple va compiler mais en utilisant une fonctionnalité nommée [VLA][vla] (*Variable Length Array*) qui n'est pas recommandée. Les tableaux de taille variable sont une source de bugs potentiels et ne sont pas supportés par tous les compilateurs.

!!! bug "Limites"

    En C il n'y a pas de vérification de limites lors de l'accès à un tableau. Il est donc possible d'accéder à un élément qui n'existe pas. Par exemple, si un tableau de 5 éléments est déclaré, il est possible d'accéder à l'élément 6 sans générer d'erreur. Cela peut être source de bugs très difficiles à détecter.

    ```c
    int array[5] = {0};
    array[6] = 42; // Pas d'erreur !
    ```

    C'est au programmeur de s'assurer que les indices utilisés sont valides. Le plus souvent, ce type d'erreur ne mène pas à un crash immédiat, mais à un comportement indéterminé car l'accès mémoire est en dehors de la zone allouée au tableau et correspond à une zone mémoire qui peut être utilisée par une autre variable. C'est ce que l'on appelle un [buffer overflow](https://fr.wikipedia.org/wiki/D%C3%A9bordement_de_tampon). Dans l'exemple suivant, les tableaux `a` et `b` sont déclarés l'un après l'autre sur la pile, et l'écriture en dehors de `a` modifie la valeur de `b` :

    ```c
    int main() {
        int a[4] = {0};
        int b[4] = {0};
        a[4] = 42;
        printf("%d\n", b[0]); // Affiche 42 !
    }
    ```

## Initialisation

Lors de la déclaration d'un tableau, le compilateur réserve un espace mémoire de la taille suffisante pour contenir tous les éléments du tableau. La déclaration suivante réserve un espace pour 6 entiers, chacun d'une taille de 32-bits (4 bytes). L'espace mémoire réservé est donc de 24 bytes.

```c
int32_t even[6];
```

Compte tenu de cette déclaration, il n'est pas possible de connaître la valeur des différents éléments car ce tableau n'a pas été initialisé et le contenu mémoire est non prédictible puisqu'il peut contenir les vestiges d'un ancien programme ayant tantôt résidé dans cette région mémoire.

Pour définir un contenu, il est nécessaire d'initialiser le tableau en affectant une valeur à chaque élément comme suit :

```c
int32_t sequence[6];
sequence[0] = 4;
sequence[1] = 8;
sequence[2] = 15;
sequence[3] = 16;
sequence[4] = 23;
sequence[5] = 42;
```

Cette écriture n'est certainement pas la plus optimisée, car l'initialisation du tableau n'est pas réalisée à la compilation, mais à l'exécution du programme ; et ce sera pas moins de six opérations qui seront nécessaires à l'initialiser. En pratique on utilise la notation par accolades `{}` pour initialiser un tableau :

```c
int32_t sequence[6] = {4, 8, 15, 16, 23, 42};
```

Ici, les accolades ne forment pas un bloc de code, mais une liste d'éléments, chacun séparé par une virgule.

Dans cette dernière écriture, on notera une redondance d'information. La liste  d'initialisation `{4, 8, 15, 16, 23, 42}` comporte six éléments et le tableau est déclaré avec six éléments `[6]`. Pour éviter une double source de vérité, il est ici possible d'omettre la taille du tableau :

```c
int32_t sequence[] = {4, 8, 15, 16, 23, 42};
```

Le compilateur peut inférer la taille du tableau en fonction du nombre d'éléments de la liste d'initialisation. Néanmoins, une liste d'initialisation n'initialise pas nécessairement tous les éléments du tableau. Il est possible par exemple de déclarer un tableau de 100 éléments où seul les premiers sont initialisés :

```c
int32_t sequence[100] = {4, 8, 15, 16, 23, 42 /* le reste vaudra zéro */ };
```

Dans ce cas, les éléments 6 à 99 seront initialisés à zéro. Pour s'en donner la preuve, observons le code assembleur généré par le compilateur :

```
mov     rbp, rsp
sub     rsp, 280
lea     rdx, [rbp-400]    ; adresse du tableau
mov     eax, 0            ; valeur à initialiser
mov     ecx, 50           ; nombre de mots de 8 bytes à initialiser
mov     rdi, rdx          ; destination
rep stosq                 ; répète l'opération de stockage 50 fois

; Tous les éléments du tableau sont maintenant initialisés à zéro.
; Ensuite, les éléments 0 à 5 sont initialisés explicitement.

mov     DWORD PTR [rbp-400], 4
mov     DWORD PTR [rbp-396], 8
mov     DWORD PTR [rbp-392], 15
mov     DWORD PTR [rbp-388], 16
mov     DWORD PTR [rbp-384], 23
mov     DWORD PTR [rbp-380], 42
```

Donc, lors de l'initialisation d'un tableau de 100 éléments dans une fonction on peut noter:

1. Le tableau est déclaré sur la pile.
2. Tous les éléments sont initialisés à zéro.
3. Puis, les éléments 0 à 5 sont initialisés explicitement.

Le langage C permet également d'initialiser un tableau de façon partielle. Dans l'exemple suivant, les éléments 0 à 5 sont initialisés, les autres éléments sont initialisés à zéro :

```c
int32_t sequence[100] = {[0]=4, [2]=8, [4]=15, [6]=16, [8]=23, [10]=42};
```

Notons que lorsque la notation `[]=` est utilisée, les valeurs qui suivent seront positionnées aux indices suivants. On peut donc écrire :

```c
int32_t sequence[6] = {[0]=4, 8, [3]=16, 23, 42};
```

Dans l'exemple ci-dessus `sequence[2]` vaudra zéro.

!!! bug "Initialisation tardive"

    Il n'est pas possible d'initialiser un tableau après sa déclaration. L'initialisation doit être réalisée lors de la déclaration du tableau. L'écriture suivante est donc incorrecte :

    ```c
    int array[10];

    // Erreur: l'initialisation tardive n'est pas autorisée.
    array = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    ```

## Initialisation à zéro

Pour initialiser un tableau à zéro, on devrait être autorisé à écrire le code suivant puisque tous les éléments non explicitement initialisés sont initialisés à zéro :

```c
int32_t sequence[6] = {};
```

Cependant cette écriture n'est pas autorisée selon la norme car **au moins un élément** doit être initialisé. Il est donc nécessaire d'initialiser au moins un élément à zéro :

```c
int32_t sequence[6] = {0};
```

!!! bug "Initialisation à 42"

    L'écriture ci-dessus ne veut pas dire que tout le tableau est initialisé à zéro de la même manière l'écriture suivante ne veut pas dire que tout le tableau est initialisé à 42 :

    ```c
    int32_t sequence[6] = {42};
    ```

    Seul le premier élément est initialisé à 42, les autres éléments sont initialisés à zéro.

## Initialisation à une valeur particulière

Cette écriture n'est pas normalisée **C99**, mais est généralement compatible avec la majorité des compilateurs.

```c
int array[1024] = { [ 0 ... 1023 ] = -1 };
```

En **C99**, il n'est pas possible d'initialiser un type composé à une valeur unique. La manière traditionnelle reste la boucle itérative :

```c
for (size_t i = 0; i < sizeof(array)/sizeof(array[0]); ++i)
    array[i] = -1;
```

## Tableaux non modifiables

Maintenant que nous savons initialiser un tableau, il peut être utile de définir un tableau avec un contenu qui n'est pas modifiable. Le mot clé `const` est utilisé à cette fin.

```c
const int32_t sequence[6] = {4, 8, 15, 16, 23, 42};
sequence[2] = 12; // Interdit !
```

Dans l'exemple ci-dessus, la seconde ligne génèrera l'erreur suivante :

```text
error: assignment of read-only location ‘sequence[2]’
```

Notons que lors de l'utilisation de pointeurs, il serait possible, de façon détournée, de modifier ce tableau malgré tout :

```c
int *p = sequence;
p[2] = 12;
```

Dans ce cas, ce n'est pas une erreur, mais une alerte du compilateur qui survient :

```text
warning: initialization discards ‘const’ qualifier from pointer
target type [-Wdiscarded-qualifiers]
```

## Tableaux multidimensionnels


Il est possible de déclarer un tableau à plusieurs dimensions. Si par exemple on souhaite définir une grille de jeu du *tic-tac-toe* ou morpion, il faudra une grille de 3x3.

Pour ce faire, il est possible de définir un tableau de 6 éléments comme vu auparavant, et utiliser un artifice pour adresser les lignes et les colonnes :

```c
char game[6] = {0};
int row = 1;
int col = 2;
game[row * 3 + col] = 'x';
```

Néanmoins, cette écriture n'est pas pratique et le langage C dispose heureusement de la syntaxe idoine pour alléger l'écriture. La grille de jeu sera simplement initialisée comme suit :

```c
char game[3][3] = {0};
```

Jouer `x` au centre équivaut à écrire :

```c
game[1][1] = 'x';
```

De la même façon, il est possible de définir une structure tridimensionnelle :

```c
int volume[10][4][8];
```

L'initialisation des tableaux multidimensionnelle est très similaire aux tableaux standards, mais il est possible d'utiliser plusieurs niveaux d'accolades.

Ainsi le jeu de morpion suivant :

```text
 o | x | x
---+---+---
 x | o | o
---+---+---
 x | o | x
```

Peut s'initialiser comme suit :

```c
char game[][3] = {{'o', 'x', 'x'}, {'x', 'o', 'o'}, {'x', 'o', 'x'}};
```

Notons que l'écriture suivante est aussi acceptée car un tableau multidimensionnel est toujours représenté en mémoire de façon linéaire : comme un tableau à une dimension :

```c
char game[][3] = {'o', 'x', 'x', 'x', 'o', 'o', 'x', 'o', 'x'};
```

Nous l'avons vu plus haut, il n'est pas nécessaire de fournir toutes les informations de taille du tableau lors de l'initialisation. Dans l'exemple du tic-tac-toe, la valeur de la première dimension est omise car elle peut être inférée du nombre d'éléments de la liste d'initialisation.

Prenons l'exemple du tableau suivant:

```c
int array[2][3][4];
```

On peut le représenter graphiquement comme suit :

![Tableau multidimensionnel 2x3x4](/assets/images/multidimensional-array.drawio)

Néanmoins en mémoire, ce tableau est toujours représenté de façon linéaire. L'association des coordonnées `x`, `y` et `z` est subjective et dépend de la manière dont le tableau est utilisé. Néanmoins, on pourrait s'accorder sur une représentation en mémoire logique. Dans le cas de cette figure, l'axe horizontal est l'axe des `x`, l'axe vertical est l'axe des `y` et la profondeur est l'axe des `z`. L'accès se fera avec `[z][y][x]`:

```c
int array[][3][4] = {
    {{1,2,3,4}, {5,6,7,8}, {9,10,11,12}},
    {{13,14,15,16}, {17,18,19,20}, {21,22,23,24}}
};

int x = 0, y = 0, z = 0;
assert(array[z][y][x] == 1);
```

Si on décide l'agencement `[x][y][z]` qui peut sembler plus naturel, il sera déclaré comme suit :

```c
int array[4][3][2] = {
    {{1,13}, {5,17}, {9,21}},
    {{2,14}, {6,18}, {10,22}},
    {{3,15}, {7,19}, {11,23}},
    {{4,16}, {8,20}, {12,24}}
};
```

Pour cette raison, il est plus courant d'inverser les dimensions pour les tableaux multidimensionnels. Un tableau x-y à deux dimensions est souvent déclaré `array[y][x]` pour faciliter l'initialisation.

## Tableaux et fonctions

Le passage d'un tableau à une fonction est un peu particulier. Lorsqu'on fournit le nom d'un tableau en argument, le langage C le transforme automatiquement en pointeur vers son premier élément. Cette conversion, souvent appelée *array-to-pointer decay*, donne parfois l'impression qu'un tableau **est** un pointeur alors qu'il s'agit bien de deux types différents. Un tableau possède une taille fixe connue du compilateur, tandis qu'un pointeur ne transporte que l'adresse qu'il contient.

Pour le cas le plus simple, lorsqu'une fonction reçoit un tableau, il est utile de passer la taille du tableau en paramètre, ceci permet de ne pas déborder du tableau. La fonction suivante reçoit un tableau de 5 entiers :

```c
void function(int array[5]);
```

En paramètre de fonction, cette syntaxe est immédiatement ajustée en `int *array`. Autrement dit, le compilateur ne conserve pas l'information de taille du tableau formel et ne connaît plus que l'adresse du premier élément et le type des éléments suivants. On parle donc de passage de l'adresse du tableau. La fonction suivante est strictement identique à la précédente :

```c
void function(int array[]);
```

Pour un tableau multidimensionnel, seul le premier niveau est converti en pointeur : `int array[3][4][5]` devient ainsi un pointeur vers un tableau de `4x5` entiers. Il reste donc nécessaire de connaître les dimensions suivantes afin de pouvoir calculer les adresses. En effet pour un tableau de 3x4x5 déclaré `int array[3][4][5]`, si l'on a besoin d'obtenir l'adresse de `array[2][3][4]`, le compilateur calcule l'offset en multipliant successivement les dimensions internes :

```c
int (*slice)[4][5] = array;                 // type après conversion du premier niveau
int *flat = &slice[0][0][0];                // pointeur sur le tout premier élément
size_t offset = ((2 * 4) + 3) * 5 + 4;      // nombre d'éléments à sauter
int value = flat[offset];                   // équivalent à array[2][3][4]
```

Autrement dit, la première dimension n'intervient pas dans l'arithmétique réalisée une fois la conversion en pointeur effectuée, mais les tailles des dimensions restantes sont indispensables.

## Allocation mémoire

Jusqu'ici lorsque l'on déclarait un tableau, au sein d'une fonction, il est déclaré sur la pile. Cette dernière est limitée en taille et il est possible de déborder et d'obtenir l'erreur tant redoutée `stack smashing detected` aussi appelée `stack overflow`.

En pratique lorsque l'on a besoin de grands espaces mémoire, il est préférable de déclarer le tableau sur le tas (allocation dynamique) ou en variable globale.

```c

char a[1024];           // Déclaration globale dans le segment de données

int main() {
    char b[1024];           // Déclaration sur la pile
    char* c = malloc(1024); // Déclaration sur le tas
    free(c);                // Libération de la mémoire
}
```

Ces trois déclarations sont équivalentes en termes de taille et d'utilisation du tableau. Néanmoins, leur utilisation est différente.

Déclaration globale

:  La mémoire est allouée lors de la compilation et est disponible tout au long de l'exécution du programme. Il est possible de modifier le contenu de la mémoire à tout moment. La visibilité de la variable est globale, c'est-à-dire que la variable est accessible depuis n'importe quelle fonction du programme ce qui peut être source de bogues.

Déclaration sur la pile

:  La mémoire est allouée lors de l'appel de la fonction et est libérée à la fin de la fonction. C'est une excellente méthode pour de petits tableaux mais comme la pile (*stack*) à une taille limitée, cette méthode ne doit pas être utilisée pour de grands tableaux.

Déclaration sur le tas

:  La mémoire est allouée dynamiquement lors de l'exécution du programme. La mémoire est disponible jusqu'à ce que le programme libère l'espace mémoire. C'est la méthode la plus flexible mais elle n'est pas utilisable sur des architectures embarquées car l'allocation dynamique de mémoire peut être source de fragmentation de la mémoire et de risque de fuite mémoire.

[](){#vla}

## Tableau de longueur variable (VLA)

Un [VLA](https://en.wikipedia.org/wiki/Variable-length_array) (*Variable Length Array*) est un tableau dont la taille est déterminée à l'exécution du programme. Cette fonctionnalité est disponible depuis le standard **C99**.

```c
void foo(unsigned int n) {
    int array[n];
    ...
}
```

C'est une fonctionnalité qui peut être très utile, mais elle n'est pas sans risque. En effet, la taille du tableau est déterminée à l'exécution du programme et il est possible de déborder la pile si les précautions nécessaires ne sont pas prises.

!!! bug "Débordement de pile"

    L'exemple suivant illustre un débordement de pile. La fonction `foo` alloue un tableau de `n` éléments. Si `n` est très grand, il est possible de déborder la pile et de provoquer un crash du programme.

    ```c
    void foo(unsigned int n) {
        int array[n];
        ...
    }

    int main() {
        foo(1000000);
    }
    ```

    Dans cet exemple, la fonction `foo` alloue un tableau de 4 millions d'octets (4 Mo) sur la pile. Si la taille de la pile est de 1 Mo, le programme crashera.

    À priori l'utilisateur ne sait pas ce que fait la fonction `foo` et il ne sait donc pas qu'un VLA est alloué sur la pile.

    Pire, on pourrait imaginer le programme suivant:

    ```c
    void foo(unsigned int n) {
        int array[n];
        ...
    }

    int main() {
        unsigned int n;
        scanf("%u", &n);
        foo(n);
    }
    ```

    Cette fois, l'utilisateur peut choisir la taille du tableau alloué sur la pile. Vous voyez le problème ?

Pour les raisons évoquées, les VLA sont très controversés et il est recommandé de ne pas les utiliser. Il est préférable d'utiliser l'allocation dynamique de mémoire pour allouer des tableaux de taille variable. Du reste, avec C11, le support des VLA sont devenus optionnels, c'est-à-dire qu'un compilateur peut être compatible C11 sans supporter les VLA.

## Copie d'un tableau

Imagions le code suivant :

```c
char a[5] = {1, 2, 3, 4, 5};
char b[5] = {0};
```

Pour copier le contenu du tableau `a` dans le tableau `b`, il est nécessaire de copier chaque élément un par un. Il n'existe pas d'affectation directe entre deux tableaux.

```c
void copy(char dest[], char src[], size_t size) {
    for (size_t i = 0; i < size; i++)
        dest[i] = src[i];
}
```

Notez ici que la déclaration de la fonction utilise la notation `[]` pour les tableaux car la taille des données à copier n'est pas connue à la compilation. C'est pour cette raison qu'on utilise un paramètre `size` pour indiquer la taille des tableaux. Ainsi pour copier `a` dans `b`, il suffit d'appeler la fonction `copy` :

```c
copy(b, a, 5);
```

En pratique on utilisera la fonction `memcpy` de la bibliothèque standard qui est plus rapide et plus sûre que la fonction `copy` que nous avons écrite.

```c
#include <string.h>

memcpy(b, a, 5);
```

## Exercices


!!! exercise "Assignation"

    Écrire un programme qui lit la taille d'un tableau de cinquante entiers de 8 bytes et assigne à chaque élément la valeur de son indice.

    ??? solution

        ```c
        int64_t a[50];
        for (size_t i = 0; i < sizeof(a) / sizeof(a[0]); i++) {
            a[i] = i;
        }
        ```

!!! exercise "Première position"

    Soit un tableau d'entiers, écrire une fonction retournant la position de la première occurrence d'une valeur dans le tableau.

    Traitez les cas particuliers.

    ```c
    int index_of(int *array, size_t size, int search);
    ```

    ??? solution

        ```c
        int index_of(int *array, size_t size, int search) {
            int i = 0;
            while (i < size && array[i++] != search);
            return i == size ? -1 : i;
        }
        ```

!!! exercise "Déclarations de tableaux"

    Considérant les déclarations suivantes :

    ```c
    #define LIMIT 10
    const int twelve = 12;
    int i = 3;
    ```

    Indiquez si les déclarations suivantes (qui n'ont aucun lien entre elles), sont correctes ou non.

    ```c
    int t(3);
    int k, t[3], l;
    int i[3], l = 2;
    int t[LIMITE];
    int t[i];
    int t[douze];
    int t[LIMITE + 3];
    float t[3, /* five */ 5];
    float t[3]        [5];
    ```

!!! exercise "Comparaisons"

    Soit deux tableaux `char u[]` et `char v[]`, écrire une fonction comparant leur contenu et retournant :

    `0`
        La somme des deux tableaux est égale.

    `-1`
        La somme du tableau de gauche est plus petite que le tableau de droite

    `1`
        La somme du tableau de droite est plus grande que le tableau de gauche

    Le prototype de la fonction à écrire est :

    ```c
    int comp(char a[], char b[], size_t length);
    ```

    ??? solution

        ```c
        int comp(char a[], char b[], size_t length) {
            int sum_a = 0, sum_b = 0;

            for (size_t i = 0; i < length; i++) {
                sum_a += a[i];
                sum_b += b[i];
            }

            return sum_b - sum_a;
        }
        ```

!!! exercise "Le plus grand et le plus petit"

    Dans le canton de Genève, il existe une tradition ancestrale: l'[Escalade](https://fr.wikipedia.org/wiki/Escalade_(Gen%C3%A8ve)). En commémoration de la victoire de la république protestante sur les troupes du duc de Savoie suite à l'attaque lancée contre Genève dans la nuit du 11 au 12 décembre 1602 (selon le calendrier julien), une traditionnelle marmite en chocolat est brisée par l'ainé et le cadet après la récitation de la phrase rituelle "Ainsi périrent les ennemis de la République !".

    Pour gagner du temps et puisque l'assemblée est grande, il vous est demandé d'écrire un programme pour identifier le doyen et le benjamin de l'assistance.

    Un fichier contenant les années de naissance de chacun vous est donné, il ressemble à ceci :

    ```c
    1931
    1986
    1996
    1981
    1979
    1999
    2004
    1978
    1964
    ```

    Votre programme sera exécuté comme suit :

    ```bash
    $ cat years.txt | marmite
    2004
    1931
    ```

!!! exercise "L'index magique"

    Un indice magique d'un tableau `A[0..n-1]` est défini tel que la valeur `A[i] == i`. Étant donné que le tableau est trié avec des entiers distincts (sans répétition), écrire une méthode pour trouver un indice magique s'il existe.

    Exemple :

    ```text
        0   1   2   3   4   5   6   7   8   9   10
    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
    │-90│-33│ -5│ 1 │ 2 │ 4 │ 5 │ 7 │ 10│ 12│ 14│
    └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
                                    ^
    ```

    ??? solution

        Une solution triviale consiste à itérer tous les éléments jusqu'à trouver l'indice magique :

        ```c
        int magic_index(const int array[], size_t size) {
            size_t i = 0;

            while (i < size && array[i] != (int)i) i++;

            return i == size ? -1 : (int)i;
        }
        ```

        La complexité de cet algorithme est :math:`O(n)` or, la donnée du problème indique que le tableau est trié. Cela veut dire que probablement, cette information n'est pas donnée par hasard.

        Pour mieux se représenter le problème, prenons l'exemple d'un tableau :

        ```text
            0   1   2   3   4   5   6   7   8   9   10
        ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
        │-90│-33│ -5│ 1 │ 2 │ 4 │ 5 │ 7 │ 10│ 12│ 14│
        └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
                                        ^
        ```

        La première valeur magique est `7`. Est-ce qu'une approche dichotomique est possible ?

        Prenons le milieu du tableau `A[5] = 4`. Est-ce qu'une valeur magique peut se trouver à gauche du tableau ? Dans le cas le plus favorable qui serait :

        ```text
            0   1   2   3   4
        ┌───┬───┬───┬───┬───┐
        │ -1│ 0 │ 1 │ 2 │ 3 │
        └───┴───┴───┴───┴───┘
        ```

        On voit qu'il est impossible que la valeur se trouve à gauche, car les valeurs dans le tableau sont distinctes et il n'y a pas de répétitions. La règle que l'on peut poser est `A[mid] < mid` où `mid` est la valeur médiane.

        Il est possible de répéter cette approche de façon dichotomique :

        ```c
        static int _magic_index(const int array[], int start, int end) {
            if (end < start) return -1;
            int mid = start + (end - start) / 2;
            if (array[mid] == mid) {
                return mid;
            } else if (array[mid] > mid) {
                return _magic_index(array, start, mid - 1);
            } else {
                return _magic_index(array, mid + 1, end);
            }
        }

        int magic_index(const int array[], size_t size) {
            if (size == 0) return -1;
            return _magic_index(array, 0, (int)size - 1);
        }
        ```

!!! exercise "Détectives privés"

    Voici les dépenses de service annuelles d'un célèbre bureau de détectives privés :


    | Mois      | Bosley | Sabrina | Jill   | Kelly  |
    | --------- | ------ | ------- | ------ | ------ |
    | Janvier   | 414.38 | 222.72  | 99.17  | 153.81 |
    | Février   | 403.41 | 390.61  | 174.39 | 18.11  |
    | Mars      | 227.55 | 73.86   | 291.08 | 416.55 |
    | Avril     | 220.20 | 342.25  | 139.45 | 86.98  |
    | Mai       | 13.46  | 172.66  | 252.33 | 265.32 |
    | Juin      | 259.37 | 378.72  | 173.02 | 208.43 |
    | Juillet   | 327.06 | 16.53   | 391.05 | 266.84 |
    | Août      | 50.82  | 3.37    | 201.71 | 170.84 |
    | Septembre | 450.78 | 9.33    | 111.63 | 337.07 |
    | Octobre   | 434.45 | 77.80   | 459.46 | 479.17 |
    | Novembre  | 420.13 | 474.69  | 343.64 | 273.28 |
    | Décembre  | 147.76 | 250.73  | 201.47 | 9.75   |

    Afin de laisser plus de temps aux détectives à résoudre des affaires, vous êtes mandaté pour écrire une fonction qui reçoit en paramètre le tableau de réels ci-dessus formaté comme suit :

    ```c
    double accounts[][] = {
        {414.38, 222.72,  99.17, 153.81, 0},
        {403.41, 390.61, 174.39, 18.11,  0},
        {227.55,  73.86, 291.08, 416.55, 0},
        {220.20, 342.25, 139.45, 86.98,  0},
        {13.46 , 172.66, 252.33, 265.32, 0},
        {259.37, 378.72, 173.02, 208.43, 0},
        {327.06,  16.53, 391.05, 266.84, 0},
        {50.82 ,   3.37, 201.71, 170.84, 0},
        {450.78,   9.33, 111.63, 337.07, 0},
        {434.45,  77.80, 459.46, 479.17, 0},
        {420.13, 474.69, 343.64, 273.28, 0},
        {147.76, 250.73, 201.47, 9.75,   0},
        {  0,      0,      0,    0,      0}
    };
    ```

    Et laquelle complète les valeurs manquantes.

!!! exercise "Pot de peinture"

    À l'instar de l'outil *pot de peinture* des éditeurs d'image, il vous est demandé d'implémenter une fonctionnalité similaire.

    L'image est représentée par un tableau bidimensionnel contenant des couleurs indexées :

    ```c
    #include <stdbool.h>

    typedef enum { BLACK, RED, PURPLE, BLUE, GREEN, YELLOW, WHITE } Color;

    #if 0 // Image declaration example
    Color image[100][100];
    #endif

    bool paint(size_t rows, size_t cols, Color image[rows][cols], Color fill_color);
    ```

    !!! hint

        Deux approches intéressantes sont possibles: **DFS** (Depth-First-Search) ou **BFS** (Breadth-First-Search), toutes deux récursives.