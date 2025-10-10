
# Tableau dynamique

## Définition

Un tableau dynamique (aussi nommé *vector* en C++ ou liste en Python) est une structure de données qui dépasse les limitations rigides du tableau classique en offrant une grande souplesse d’utilisation. Dans un tableau statique, la taille est déterminée dès l'initialisation et ne peut plus être modifiée, ce qui impose à la personne qui programme de prédire, souvent avec difficulté, la quantité exacte d'espace nécessaire. Un tableau dynamique, en revanche, s’ajuste à la croissance comme à la diminution des données qu’il contient et répond ainsi aux besoins évolutifs du programme.

Le fonctionnement d’un tableau dynamique repose sur un mécanisme essentiel : la gestion dynamique de la mémoire. Initialement, un tableau dynamique est alloué avec une taille déterminée, souvent modeste, pour accueillir les premiers éléments. Lorsque le tableau atteint sa capacité maximale, une nouvelle allocation de mémoire plus vaste est effectuée. Ce processus implique la création d'un tableau plus grand, la copie des éléments du tableau original vers ce nouvel espace, puis la libération de la mémoire utilisée par le tableau initial.

Cette flexibilité a un coût en matière de performances : réallouer la mémoire et copier les éléments lors de l'agrandissement du tableau sont des opérations coûteuses en temps, surtout si elles se répètent. Pour atténuer cet inconvénient, les tableaux dynamiques sont souvent conçus pour doubler leur capacité à chaque réallocation, ce qui réduit la fréquence des copies.

Outre la gestion de la capacité, un tableau dynamique offre aussi des opérations d'insertion et de suppression plus souples que celles d'un tableau statique. Là où un tableau statique impose de déplacer manuellement les éléments pour insérer ou supprimer une valeur, le tableau dynamique orchestre ces opérations, ce qui rend son utilisation plus intuitive.

Néanmoins, cette flexibilité exige une gestion rigoureuse. La personne qui développe doit rester consciente de la manière dont la mémoire est utilisée, surtout dans des langages comme le C où l'allocation et la libération demeurent manuelles. Une mauvaise gestion peut conduire à des fuites de mémoire ou à des inefficacités critiques.

## Exemple

Prenons un exemple simple pour illustrer le concept de tableau dynamique en C. Imaginons que nous souhaitons créer un buffer pour stocker une séquence de trois caractères :

```c
char *buffer = malloc(3);

buffer[0] = 'h';
buffer[1] = 'e';
buffer[2] = 'l'; // Le buffer est plein...
```

À ce stade, le tampon a atteint sa capacité maximale. Si nous souhaitons ajouter d'autres caractères, il faut augmenter la taille disponible en réallouant dynamiquement de la mémoire :

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

Il est également possible de réduire la taille allouée lorsque le nombre d'éléments devient nettement inférieur à la capacité effective. En pratique, cette opération est rarement appliquée, car elle se révèle souvent inefficace et coûteuse en performances, comme l’explique cette [réponse sur StackOverflow](https://stackoverflow.com/a/60827815/2612235).

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

Un espace mémoire est réservé dynamiquement sur le tas. Comme `malloc` ne retourne pas la taille de l'espace alloué mais seulement un pointeur, il est nécessaire de conserver la capacité du tableau dans une variable dédiée. Notons qu'un tableau de dix `int32_t` occupe 10 × 4 octets, soit 40 octets. La mémoire réservée par `malloc` n'est généralement pas vide : elle contient les vestiges d’anciennes allocations. Pour connaître le nombre d'éléments effectifs du tableau, il faut également stocker cette information. Enfin, le pointeur vers l'espace mémoire doit être mémorisé.

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

L'opération `shift` retire un élément depuis le début. Elle a une complexité en $O(n)$ puisqu'à chaque exécution il faut déplacer l'ensemble des éléments restants.

Figure: Suppression du premier élément dans un tableau dynamique

![Tableau dynamique: pop front](/assets/images/dyn-array-shift.drawio)

```c
if (elements <= 0) exit(EXIT_FAILURE);
int value = data[0];
for (int k = 0; k < elements - 1; k++)
    data[k] = data[k + 1];
```

Une optimisation consiste à déplacer le pointeur de données d'une position, ce qui réduit la complexité à $O(1)$ :

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

Dans le cas où le nombre d'éléments atteint la capacité maximale du tableau, il faut réallouer l'espace mémoire avec `realloc`. En pratique, on se contente souvent de doubler l'espace alloué.

```c
if (elements >= capacity) {
    data = realloc(data, capacity *= 2);
}
```

## Analyse de la complexité

Accès par index $O(1)$

: Cette opération est rapide et s'effectue en temps constant car les tableaux dynamiques, comme les tableaux statiques, permettent un accès direct à chaque élément via leur index.

Push $O(1)$ *amorti*

: En général, ajouter un élément à la fin d'un tableau dynamique prend un temps constant $O(1)$. Cependant, si la capacité est atteinte, le tableau doit être redimensionné, ce qui implique de copier tous les éléments existants vers un nouveau bloc de mémoire et coûte $O(n)$. Grâce à l'amortissement, la complexité moyenne reste $O(1)$ sur une série d'insertion.

Insertion au début (unshift) ou au milieu $O(n)$

: Insérer un élément au début ou au milieu du tableau nécessite de déplacer les éléments existants, ce qui implique un coût proportionnel au nombre d'éléments $O(n)$.

Pop $O(1)$

: La suppression du dernier élément est une opération constante, puisqu'il n'y a ni réarrangement des autres valeurs ni rallocation mémoire.

Suppression au début (shift) ou au milieu $O(n)$

: Comme pour l'insertion, la suppression d'un élément en début ou au milieu du tableau nécessite de décaler les éléments restants, ce qui entraîne une complexité de $O(n)$.

Lors d'un redimensionnement, il faut parfois copier les éléments dans un nouveau tableau si `realloc` ne parvient pas à agrandir l'espace existant, ce qui coûte $O(n)$. Toutefois, cette opération reste ponctuelle. On dit que le coût d'un redimensionnement est amorti sur les nombreuses opérations d'insertion. Prenons un exemple.

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

Si l'on insère 64 éléments, on doit redimensionner le tableau six fois et copier $64 + 32 + 16 + 8 + 4 + 2 = 126$ valeurs au total. En moyenne, chaque insertion revient donc à $126 / 64 \approx 2$, soit une constante notée $O(1)$. Ce coût étant amorti sur l'ensemble des opérations, la complexité d'insertion demeure $O(1)$ *amorti*.

## Pile

Une pile est une structure de données utilisée pour empiler des données de manière temporaire. C'est ce que l'on appelle un LIFO (*Last In, First Out*).

![Pile ou *stack*](/assets/images/dyn-array-stack.drawio)

Nous avons vu que certaines opérations sont plus coûteuses que d'autres. Les opérations `push-back` et `pop-back` sont les moins gourmandes. Puisque la pile ne repose que sur ces deux actions, on peut en tirer parti.

Une pile peut donc être implémentée sous forme d'un tableau dynamique dans lequel on ne conserve que ces deux opérations.

## Queue

Une queue est une structure de données utilisée comme file d'attente, ce que l'on appelle un FIFO (*First In, First Out*). Les éléments sont ajoutés à la fin et retirés au début. Pour éviter le déplacement constant des éléments en $O(n)$, on met généralement en place une file circulaire.

## Buffer circulaire

Un **tampon circulaire**, aussi appelé *buffer circulaire* ou *ring buffer* en anglais, est généralement de taille fixe et dispose de deux pointeurs : l'un vers le dernier élément (*tail*), l'autre vers le premier (*head*).

Lorsqu'un élément est supprimé du tampon, le pointeur de fin est incrémenté. Lorsqu'un élément est ajouté, c'est le pointeur de début qui avance.

Pour permettre la circulation, les indices sont calculés modulo la taille du buffer.

Il est possible de représenter schématiquement ce buffer comme un cercle et ses deux pointeurs :

![Exemple d'un tampon circulaire](/assets/images/ring.drawio)

Le nombre d'éléments dans le tampon est la différence entre le pointeur de tête et le pointeur de queue, modulo la taille du buffer. Néanmoins, l'opérateur `%` en C ne fonctionne que sur des nombres positifs et ne retourne pas toujours le résidu positif minimal. En somme, `-2 % 5` devrait donner `3`, ce qui est le cas en Python, mais en C, en C++ ou en PHP la valeur retournée est `-2`. Le modulo mathématiquement correct peut être calculé ainsi :

```c
((A % M) + M) % M
```

Les indices s'enroulent sur la taille du tampon ; l'élément suivant est donc défini par :

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
    return MOD(ring->head - ring->tail, SIZE);
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