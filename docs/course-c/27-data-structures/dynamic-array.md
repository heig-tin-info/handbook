
# Tableau dynamique

## Définition

Un tableau dynamique (aussi nommé vecteur en C++ ou liste en Python) est une structure de données qui transcende les limitations rigides du tableau classique en offrant une flexibilité d’utilisation accrue. Dans un tableau statique, la taille est déterminée dès l'initialisation et ne peut plus être modifiée, ce qui impose au développeur de prédire, parfois avec difficulté, la quantité exacte d'espace nécessaire. Un tableau dynamique, en revanche, s’ajuste à la croissance ou à la diminution des données qu’il contient, répondant ainsi aux besoins évolutifs du programme.

Le fonctionnement d’un tableau dynamique repose sur un mécanisme fondamental : la gestion dynamique de la mémoire. Initialement, un tableau dynamique est alloué avec une taille déterminée, souvent modeste, pour accueillir les premiers éléments. Cependant, lorsque le tableau atteint sa capacité maximale, une nouvelle allocation de mémoire plus vaste est effectuée. Ce processus implique la création d'un nouveau tableau plus grand, la copie des éléments du tableau original vers ce nouveau tableau, et enfin la libération de la mémoire allouée au tableau initial.

Cette flexibilité a un coût, celui de la performance, car la réallocation et la copie des éléments lors de l'agrandissement du tableau sont des opérations coûteuses en temps, surtout si elles sont fréquentes. Pour atténuer cet inconvénient, les tableaux dynamiques sont souvent conçus pour doubler leur capacité à chaque réallocation, réduisant ainsi la fréquence de ces opérations.

Outre la gestion de la capacité, un tableau dynamique offre également des opérations d'insertion et de suppression d'éléments plus souples que celles d'un tableau statique. Là où un tableau statique nécessiterait de déplacer manuellement les éléments pour insérer ou supprimer une valeur, le tableau dynamique gère ces opérations en interne, rendant son utilisation plus intuitive.

Néanmoins, cette puissance de flexibilité s'accompagne d'une exigence de gestion rigoureuse. Le développeur doit rester conscient de la manière dont la mémoire est utilisée, surtout dans des langages comme le C où le contrôle manuel de l'allocation et de la libération de la mémoire est requis. Une mauvaise gestion de ces aspects peut conduire à des fuites de mémoire ou à des inefficacités critiques.

## Exemple

Prenons un exemple simple pour illustrer le concept de tableau dynamique en C. Imaginons que nous souhaitons créer un buffer pour stocker une séquence de trois caractères :

```c
char *buffer = malloc(3);

buffer[0] = 'h';
buffer[1] = 'e';
buffer[2] = 'l'; // Le buffer est plein...
```

À ce stade, le buffer a atteint sa capacité maximale. Si nous souhaitons ajouter davantage de caractères, il nous faut augmenter la taille du buffer en réallouant dynamiquement de l'espace mémoire :

```c
// Augmente dynamiquement la taille du buffer à 5 caractères
char *tmp = realloc(buffer, 5);
assert(tmp != NULL);
buffer = tmp;

// Continue de remplir le buffer
buffer[3] = 'l';
buffer[4] = 'o'; // Le buffer est à nouveau plein...
```

Après avoir utilisé le buffer, il est crucial de libérer l'espace mémoire alloué pour éviter les fuites de mémoire :

```c
free(buffer);
```

Lors de la réallocation, la taille du nouvel espace mémoire est souvent augmentée selon un facteur de croissance prédéfini. Ce facteur varie généralement entre 1,5 et 2, selon le langage de programmation ou le compilateur utilisé. Ainsi, si l’on suit un facteur de 2, les tailles successives du tableau pourraient être 1, 2, 4, 8, 16, 32, et ainsi de suite.

Il est également possible de réduire la taille allouée lorsque le nombre d'éléments devient significativement inférieur à la taille effective du tableau. Toutefois, en pratique, cette opération est rarement mise en œuvre, car elle peut s’avérer inefficace et coûteuse en termes de performance, comme l’explique cette [réponse sur StackOverflow](https://stackoverflow.com/a/60827815/2612235).

Ainsi, la gestion dynamique de la mémoire à travers des opérations de réallocation permet une flexibilité précieuse, mais elle nécessite une gestion attentive pour éviter des inefficacités et des problèmes de performances.

## Anatomie

Un tableau dynamique est représenté en mémoire comme un contenu séquentiel qui possède un début et une fin. On appelle son début la **tête** (*head*) ou *front* et la fin du tableau, sa **queue** (*tail*) ou *back*. Selon que l'on souhaite ajouter des éléments au début ou à la fin du tableau, la complexité n'est pas la même.

Nous définirons par la suite les opérations suivantes :

![Opérations sur un tableau dynamique](/assets/images/dyn-array-operations.drawio)

Table: Vocabulaire des actions sur un tableau dynamique

| Action                                         | Terme technique         |
| ---------------------------------------------- | ----------------------- |
| Ajout d'un élément à la tête du tableau        | `push-front`, `unshift` |
| Ajout d'un élément à la queue du tableau       | `push-back`, `push`     |
| Suppression d'un élément à la tête du tableau  | `pop-front`, `shift`    |
| Suppression d'un élément à la queue du tableau | `pop-back`, `pop`       |
| Insertion d'un élément à la position n         | `insert`                |
| Suppression d'un élément à la position n       | `delete`                |

Nous comprenons rapidement qu'il est plus compliqué d'ajouter ou de supprimer un élément depuis la tête du tableau, car il est nécessaire ensuite de déplacer chaque élément (l'élément 0 devient l'élément 1, l'élément 1 devient l'élément 2...).

Un tableau dynamique peut être représenté par la figure suivante :

![Tableau dynamique](/assets/images/dyn-array.drawio)

Un espace mémoire est réservé dynamiquement sur le tas. Comme `malloc` ne retourne pas la taille de l'espace mémoire alloué, mais juste un pointeur sur cet espace, il est nécessaire de conserver dans une variable la capacité du tableau. Notons qu'un tableau de 10 `int32_t` représentera un espace mémoire de 4x10 bytes, soit 40 bytes. La mémoire ainsi réservée par `malloc` n'est généralement pas vide, mais elle contient des valeurs, vestige d'une ancienne allocation mémoire d'un autre programme depuis que l'ordinateur a été allumé. Pour connaître le nombre d'éléments effectifs du tableau, il faut également le mémoriser. Enfin, le pointeur sur l'espace mémoire est aussi mémorisé.

Les composants de cette structure de données sont donc :

La capacité

: Un entier non signé `size_t` représentant la capacité de stockage totale du tableau dynamique à un instant T lorsqu'il est plein.

Le nombre d'éléments

: Un entier non signé `size_t` représentant le nombre d'éléments effectifs dans le tableau.

Un pointeur de données

: Un pointeur sur un entier `int *` contenant l'adresse mémoire de l'espace alloué par `malloc`.

Les données

: Un espace mémoire alloué par `malloc` et contenant les données.

Il peut être déclaré sous forme de structure :

```c
typedef struct vector {
    size_t capacity;
    size_t size;
    int* data;
} Vector;
```

### Pop (*pop_back*)

L'opération `pop` retire l'élément de la fin du tableau. Le nombre d'éléments est donc ajusté en conséquence.

![Suppression d'un élément dans un tableau dynamique](/assets/images/dyn-array-pop.drawio)

```c
if (elements <= 0) exit(EXIT_FAILURE);
int value = data[--elements];
```

### Push (*push_back*)

L'opération `push` ajoute un élément à la fin du tableau.

![Ajout d'un élément dans un tableau dynamique](/assets/images/dyn-array-push.drawio)

```c
if (elements >= capacity) exit(EXIT_FAILURE);
data[elements++] = value;
```

### Shift (*pop_front*)

L'opération `shift` retire un élément depuis le début. L'opération à une complexité de O(n) puisqu'à chaque opération il est nécessaire de déplacer chaque élément qu'il contient.

Figure: Suppression du premier élément dans un tableau dynamique

![Tableau dynamique: pop front](/assets/images/dyn-array-shift.drawio)

```c
if (elements <= 0) exit(EXIT_FAILURE);
int value = data[0];
for (int k = 0; k < elements - 1; k++)
    data[k] = data[k + 1];
```

Une optimisation peut être faite en déplaçant le pointeur de données de 1 permettant de réduire la complexité à O(1) :

```c
if (elements <= 0) exit(EXIT_FAILURE);
if (capacity <= 0) exit(EXIT_FAILURE);
int value = data[0];
data++;
capacity--;
```

Il est toutefois indispensable de conserver séparément un pointeur vers le bloc initial pour pouvoir le libérer correctement avec `free`.

### Unshift (*push_front*)

Enfin, l'opération `unshift` ajoute un élément depuis le début du tableau :

![Ajout d'un élément en début d'un tableau dynamique](/assets/images/dyn-array-unshift.drawio)

```c
for (int k = elements; k >= 1; k--)
    data[k] = data[k - 1];
data[0] = value;
```

Dans le cas ou le nombre d'éléments atteint la capacité maximum du tableau, il est nécessaire de réallouer l'espace mémoire avec `realloc`. Généralement on se contente de doubler l'espace alloué.

```c
if (elements >= capacity) {
    data = realloc(data, capacity *= 2);
}
```

## Analyse de la complexité

Accès par index $O(1)$

: Cette opération est rapide et s'effectue en temps constant car les tableaux dynamiques, comme les tableaux statiques, permettent un accès direct à chaque élément via leur index.

Push $O(1)$ *amorti*

: En général, ajouter un élément à la fin d'un tableau dynamique prend un temps constant $O(1)$. Cependant, si la capacité du tableau est atteinte, le tableau doit être redimensionné, ce qui implique de copier tous les éléments existants vers un nouveau tableau, ce qui a un coût $O(n)$. Grâce à l'amortissement, la complexité moyenne reste $O(1)$ sur une série d'opérations d'insertion.

Insertion au début (unshift) ou au milieu $O(n)$

: Insérer un élément au début ou au milieu du tableau nécessite de déplacer les éléments existants, ce qui implique un coût proportionnel au nombre d'éléments $O(n)$.

Pop $O(1)$

: La suppression du dernier élément est une opération constante, puisqu'il n'y a pas besoin de réarranger les autres éléments, ou bien réserver davantage d'espace mémoire.

Suppression au début (shift) ou au milieu $O(n)$

: Comme pour l'insertion, la suppression d'un élément en début ou au milieu du tableau nécessite de décaler les éléments restants, ce qui entraîne une complexité de $O(n)$.

Lors d'un redimensionnement il faut parfois copier les éléments dans un nouveau tableau si `realloc` ne parviens pas à agrandir l'espace existant, ce qui a un coût de $O(n)$. Toutefois, cette opération ne se produit que de temps en temps. On dit que le coût d'un redimensionnement est est amorti sur les nombreuses opérations d'insertion. Prenons un exemple.

```
Élements, Capacité, Redimensionnements

1         1
2         2         1 (2)
3         4         2 (4)
4         4
5         8         3 (8)
6         8
7         8
8         8
9..16     16        4 (16)
17..32    32        5 (32)
33..64    64        6 (64)
```

Si on insert 64 éléments on a du redimensionner le tableau 6 fois et on à du copier $64 + 32 + 16 + 8 + 4 + 2 = 126$ éléments en totalité. En moyenne c'est comme si chaque insertion avait coûté $126 / 64 \approx 2$, soit une constante que l'on écrit $O(1)$. Comme ce coût est amorti sur l'ensemble des éléments, on dit que la complexité d'insertion est de $O(1)$ *amorti*.

## Pile

Une pile est une structure de données utilisée pour empiler des données de manière temporaire. C'est ce que l'on appelle un LIFO (*Last In, First Out*).

![Pile ou *stack*](/assets/images/dyn-array-stack.drawio)

Nous avons vu que certaines opérations sont plus onéreuses que d'autres. Les opérations `push-back` et `pop-back` sont les moins gourmandes. Puisque la pile n'a que deux opérations, on peut en tirer parti.

Une pile peut donc être implémentée sous forme d'un tableau dynamique dans lequel on ne conserverai que deux opérations.

## Queue

Une queue est une structure de données utilisée comme file d'attente. C'est ce que l'on nomme un FIFO (*First In, First Out*). Les éléments sont ajoutés à la fin et retirés au début. Néanmoins, afin d'éviter le déplacement constant des éléments en $O(n)$, une file circulaire est souvent utilisée.

## Buffer circulaire

Un **tampon circulaire** aussi appelé *buffer circulaire* ou *ring buffer* en anglais est généralement d'une taille fixe et possède deux pointeurs. L'un pointant sur le dernier élément (*tail*) et l'un sur le premier élément (*head*).

Lorsqu'un élément est supprimé du buffer, le pointeur de fin est incrémenté. Lorsqu'un élément est ajouté, le pointeur de début est incrémenté.

Pour permettre la circulation, les indices sont calculés modulo la taille du buffer.

Il est possible de représenter schématiquement ce buffer comme un cercle et ses deux pointeurs :

![Exemple d'un tampon circulaire](/assets/images/ring.drawio)

Le nombre d'éléments dans le buffer est la différence entre le pointeur de tête et le pointeur de queue, modulo la taille du buffer. Néanmoins, l'opérateur `%` en C ne fonctionne que sur des nombres positifs et ne retourne pas le résidu positif le plus petit. En sommes, `-2 % 5` devrait donner `3`, ce qui est le cas en Python, mais en C, en C++ ou en PHP la valeur retournée est `-2`. Le modulo vrai, mathématiquement correct, peut être calculé ainsi :

```c
((A % M) + M) % M
```

Les indices sont bouclés sur la taille du buffer, l'élément suivant est donc défini par :

```c
(i + 1) % SIZE
```

Voici une implémentation possible du buffer circulaire :

```c
#define SIZE 16
#define MOD(A, M) (((A % M) + M) % M)
#define NEXT(A) (((A) + 1) % SIZE)

typedef struct Ring {
    int buffer[SIZE];
    int head;
    int tail;
} Ring;

void init(Ring *ring) {
    ring->head = ring->tail = 0;
}

int count(Ring *ring) {
    return MOD(ring->head - ring->tail, size);
}

bool is_full(Ring *ring) {
    return count(ring) == SIZE - 1;
}

bool is_empty(Ring *ring) {
    return ring->tail == ring->head;
}

int* enqueue(Ring *ring, int value) {
    if (is_full(ring)) return NULL;
    ring->buffer[ring->head] = value;
    int *el = &ring->buffer[ring->head];
    ring->head = NEXT(ring->head);
    return el;
}

int* dequeue(Ring *ring) {
    if (is_empty(ring)) return NULL;
    int *el = &ring->buffer[ring->tail];
    ring->tail = NEXT(ring->tail);
    return el;
}
```