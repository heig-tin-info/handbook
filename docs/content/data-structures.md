# Structures de données

## Types de données abstraits

Un [type de donnée abstrait](https://fr.wikipedia.org/wiki/Type_abstrait) (**ADT** pour Abstract Data Type) cache généralement une structure dont le contenu n'est pas connu de l'utilisateur final. Ceci est rendu possible par le standard (C99 §6.2.5) par l'usage de types incomplets.

Pour mémoire, un type incomplet décrit un objet dont on ne connaît pas sa taille en mémoire.

L'exemple suivant déclare un nouveau type structure qui n'est alors pas (encore) connu dans le fichier courant :

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

Pour s'en protéger, on a recours à la compilation séparée (voir chapitre {ref}`TranslationUnits`) dans laquelle le programme est découpé en plusieurs fichiers. Le fichier `foobar.h` contiendra tout ce qui doit être connu du programme principal, à savoir les prototypes des fonctions, et le type abstrait :

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

En résumé, un type abstrait impose l'utilisation de fonctions intermédiaires pour modifier le type. Dans la grande majorité des cas, ces types représentent des structures qui contiennent des informations internes qui ne sont pas destinées à être modifiées par l'utilisateur final.

## Tableau dynamique

Un tableau dynamique aussi appelé *vecteur* est, comme son nom l'indique, alloué dynamiquement dans le *heap* en fonction des besoins. Vous vous rappelez que le *heap* grossit à chaque appel de `malloc` et diminue à chaque appel de `free`.

Un tableau dynamique est souvent spécifié par un facteur de croissance (rien à voir avec les hormones). Lorsque le tableau est plein et que l'on souhaite rajouter un nouvel élément, le tableau est réalloué dans un autre espace mémoire plus grand avec la fonction `realloc`. Cette dernière n'est rien d'autre qu'un `malloc` suivi d'un `memcopy` suivi d'un `free`. Un nouvel espace mémoire est réservé, les données sont copiées du premier espace vers le nouveau, et enfin le premier espace est libéré. Voici un exemple :

```c
// Alloue un espace de trois chars
char *buffer = malloc(3);

// Rempli le buffer
buffer[0] = 'h';
buffer[1] = 'e';
buffer[2] = 'l'; // Le buffer est plein...

// Augmente dynamiquement la taille du buffer à 5 chars
char *tmp = realloc(buffer, 5);
assert(tmp != NULL);
buffer = tmp;

// Continue de remplir le buffer
buffer[3] = 'l';
buffer[4] = 'o'; // Le buffer est à nouveau plein...

// Libère l'espace mémoire utilisé
free(buffer);
```

La taille du nouvel espace mémoire est plus grande d'un facteur donné que l'ancien espace. Selon les langages de programmation et les compilateurs, ces facteurs sont compris entre 3/2 et 2. C'est-à-dire que la taille du tableau prendra les tailles de 1, 2, 4, 8, 16, 32, etc.

Lorsque le nombre d'éléments du tableau devient inférieur du facteur de croissance à la taille effective du tableau, il est possible de faire l'opération inverse, c'est-à-dire réduire la taille allouée. En pratique cette opération est rarement implémentée, car peu efficace (c.f. [cette](https://stackoverflow.com/a/60827815/2612235) réponse sur stackoverflow).

### Anatomie

Un tableau dynamique est représenté en mémoire comme un contenu séquentiel qui possède un début et une fin. On appelle son début la **tête** ou *head* et la fin du tableau, sa **queue** ou *tail*. Selon que l'on souhaite ajouter des éléments au début ou à la fin du tableau, la complexité n'est pas la même.

Nous définirons par la suite le vocabulaire suivant:

Table: Vocabulaire des actions sur un tableau dynamique

| Action                                         | Terme technique |
| ---------------------------------------------- | --------------- |
| Ajout d'un élément à la tête du tableau        | `unshift`       |
| Ajout d'un élément à la queue du tableau       | `push`          |
| Suppression d'un élément à la tête du tableau  | `shift`         |
| Suppression d'un élément à la queue du tableau | `pop`           |

Nous comprenons rapidement qu'il est plus compliqué d'ajouter ou de supprimer un élément depuis la tête du tableau, car il est nécessaire ensuite de déplacer chaque élément (l'élément 0 devient l'élément 1, l'élément 1 devient l'élément 2...).

Un tableau dynamique peut être représenté par la figure suivante :

![Tableau dynamique](../assets/images/dyn-array.drawio)

Un espace mémoire est réservé dynamiquement sur le tas. Comme `malloc` ne retourne pas la taille de l'espace mémoire alloué, mais juste un pointeur sur cet espace, il est nécessaire de conserver dans une variable la capacité du tableau. Notons qu'un tableau de 10 `int32_t` représentera un espace mémoire de 4x10 bytes, soit 40 bytes. La mémoire ainsi réservée par `malloc` n'est généralement pas vide, mais elle contient des valeurs, vestige d'une ancienne allocation mémoire d'un autre programme depuis que l'ordinateur a été allumé. Pour connaître le nombre d'éléments effectifs du tableau, il faut également le mémoriser. Enfin, le pointeur sur l'espace mémoire est aussi mémorisé.

Les composants de cette structure de donnée sont donc :

- Un entier non signé `size_t` représentant la capacité totale du tableau dynamique à un instant T.
- Un entier non signé `size_t` représentant le nombre d'éléments effectivement dans le tableau.
- Un pointeur sur un entier `int *` contenant l'adresse mémoire de l'espace alloué par `malloc`.
- Un espace mémoire alloué par `malloc` et contenant des données.

L'opération `pop` retire l'élément de la fin du tableau. Le nombre d'éléments est donc ajusté en conséquence.

![Suppression d'un élément dans un tableau dynamique](../assets/images/dyn-array-pop.drawio)

```c
if (elements <= 0) exit(EXIT_FAILURE);
int value = data[--elements];
```

L'opération `push` ajoute un élément à la fin du tableau.

![Ajout d'un élément dans un tableau dynamique](../assets/images/dyn-array-push.drawio)

```c
if (elements >= capacity) exit(EXIT_FAILURE);
data[elements++] = value;
```

L'opération `shift` retire un élément depuis le début. L'opération à une complexité de O(n) puisqu'à chaque opération il est nécessaire de déplacer chaque élément qu'il contient.

![Suppression du premier élément dans un tableau dynamique](../assets/images/dyn-array-shift.drawio)


```c
if (elements <= 0) exit(EXIT_FAILURE);
int value = data[0];
for (int k = 0; k < capacity; k++)
    data[k] = data[k+1];
```

Une optimisation peut être faite en déplaçant le pointeur de donnée de 1 permettant de réduite la complexité à O(1) :

```c
if (elements <= 0) exit(EXIT_FAILURE);
if (capacity <= 0) exit(EXIT_FAILURE);
int value = data[0];
data++;
capacity--;
```

Enfin, l'opération `unshift` ajoute un élément depuis le début du tableau :

![Ajout d'un élément en début d'un tableau dynamique](../assets/images/dyn-array-unshift.drawio)

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

## Buffer circulaire

Un **tampon circulaire** aussi appelé *buffer circulaire* ou *ring buffer* en anglais est généralement d'une taille fixe et possède deux pointeurs. L'un pointant sur le dernier élément (*tail*) et l'un sur le premier élément (*head*).

Lorsqu'un élément est supprimé du buffer, le pointeur de fin est incrémenté. Lorsqu'un élément est ajouté, le pointeur de début est incrémenté.

Pour permettre la circulation, les indices sont calculés modulo la taille du buffer.

Il est possible de représenter schématiquement ce buffer comme un cercle et ses deux pointeurs :

![Exemple d'un tampon circulaire](../assets/images/ring.drawio)

Le nombre d'éléments dans le buffer est la différence entre le pointeur de tête et le pointeur de queue, modulo la taille du buffer. Néanmoins, l'opérateur `%` en C ne fonctionne que sur des nombres positifs et ne retourne pas le résidu positif le plus petit. En sommes, `-2 % 5` devrait donner `3`, ce qui est le cas en Python, mais en C, en C++ ou en PHP la valeur retournée est `-2`. Le modulo vrai, mathématiquement correct peut être calculé ainsi :

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

## Listes chaînées

On s'aperçoit vite avec les tableaux que certaines opérations sont plus coûteuses que d'autres. Ajouter ou supprimer un élément à la fin du tableau coûte $O(1)$ amorti, mais ajouter ou supprimer un élément à l'intérieur du tableau coûte $O(n)$ du fait qu'il est nécessaire de déplacer tous les éléments qui suivent l'élément concerné.

Une possible solution à ce problème serait de pouvoir s'affranchir du lien entre les éléments et leurs positions en mémoire relative les uns aux autres.

Pour illustrer cette idée, imaginons un tableau statique dans lequel chaque élément est décrit par la structure suivante :

```c
struct Element {
    int value;
    int index_next_element;
};

struct Element elements[100];
```

Considérons les dix premiers éléments de la séquence de nombre [A130826](https://oeis.org/A130826) dans un tableau statique. Ensuite, répartissons ces valeurs aléatoirement dans notre tableau `elements` déclaré plus haut entre les indices 0 et 19.

![Construction d'une liste chainée à l'aide d'un tableau](../assets/images/static-linked-list.drawio)

On observe sur la figure ci-dessus que les éléments n'ont plus besoin de se suivre en mémoire, car il est possible facilement de chercher l'élément suivant de la liste avec cette relation :

```c
struct Element current = elements[4];
struct Element next = elements[current.index_next_element]
```

De même, insérer une nouvelle valeur `13` après la valeur `42` est très facile:

```c
// Recherche de l'élément contenant la valeur 42
struct Element el = elements[0];
while (el.value != 42 && el.index_next_element != -1) {
    el = elements[el.index_next_element];
}
if (el.value != 42) abort();

// Recherche d'un élément libre
const int length = sizeof(elements) / sizeof(elements[0]);
int k;
for (k = 0; k < length; k++)
    if (elements[k].index_next_element == -1)
        break;
assert(k < length && elements[k].index_next_element == -1);

// Création d'un nouvel élément
struct Element new = (Element){
    .value = 13,
    .index_next_element = -1
};

// Insertion de l'élément quelque part dans le tableau
el.index_next_element = k;
elements[el.index_next_element] = new;
```

Cette solution d'utiliser un lien vers l'élément suivant et s'appelle liste chaînée. Chaque élément dispose d'un lien vers l'élément suivant situé quelque part en mémoire. Les opérations d'insertion et de suppression au milieu de la chaîne sont maintenant effectuées en $O(1)$ contre $O(n)$ pour un tableau standard. En revanche l'espace nécessaire pour stocker ce tableau est doublé puisqu'il faut associer à chaque valeur le lien vers l'élément suivant.

D'autre part, la solution proposée n'est pas optimale :

- L'élément 0 est un cas particulier qu'il faut traiter différemment. Le premier élément de la liste doit toujours être positionné à l'indice 0 du tableau. Insérer un nouvel élément en début de tableau demande de déplacer cet élément ailleurs en mémoire.
- Rechercher un élément libre prend du temps.
- Supprimer un élément dans le tableau laisse une place mémoire vide. Il devient alors difficile de savoir où sont les emplacements mémoires disponibles.

Une liste chaînée est une structure de données permettant de lier des éléments structurés entre eux. La liste est caractérisée par :

- un élément de tête (*head*),
- un élément de queue (*tail*).

Un élément est caractérisé par :

- un contenu (*payload*),
- une référence vers l'élément suivant et/ou précédent dans la liste.

Les listes chaînées réduisent la complexité liée à la manipulation d'éléments dans une liste. L'empreinte mémoire d'une liste chaînée est plus grande qu'avec un tableau, car à chaque élément de donnée est associé un pointeur vers l'élément suivant ou précédent.

Ce surcoût est souvent part du compromis entre la complexité d'exécution du code et la mémoire utilisée par ce programme.

Table: Coût des opérations dans des structures de données récursives

| Structure de donnée      | Pire cas   |                 |                    |                      |
| ------------------------ | ---------- | --------------- | ------------------ | -------------------- |
|                          | **Insertion**  | **Suppression**     | **Recherche (Trié)**   | **Recherche (Non trié)** |
| Tableau, pile, queue     | $O(n)$     | $O(n)$          | $O(\log(n))$       | $O(n)$               |
| Liste chaînée simple     | $O(1)$     | $O(1)$          | $O(n)$             | $O(n)$               |

### Liste simplement chaînée (*linked-list*)

La figure suivante illustre un set d'éléments liés entre eux à l'aide d'un pointeur rattaché à chaque élément. On peut s'imaginer que chaque élément peut se situer n'importe où en mémoire et
qu'il n'est alors pas indispensable que les éléments se suivent dans l'ordre.

Il est indispensable de bien identifier le dernier élément de la liste grâce à son pointeur associé
à la valeur `NULL`.

![Liste chaînée simple](../assets/images/list.drawio)

```c
#include <stdio.h>
#include <stdlib.h>

struct Point
{
    double x;
    double y;
    double z;
};

struct Element
{
    struct Point point;
    struct Element* next;
};

int main(void)
{
    struct Element a = {.point = {1,2,3}, .next = NULL};
    struct Element b = {.point = {4,5,6}, .next = &a};
    struct Element c = {.point = {7,8,9}, .next = &b};

    a.next = &c;

    struct Element* walk = &a;

    for (size_t i = 0; i < 10; i++)
    {
        printf("%d. P(x, y, z) = %0.2f, %0.2f, %0.2f\n",
            i,
            walk->point.x,
            walk->point.y,
            walk->point.z
        );

        walk = walk->next;
    }
}
```

### Opérations sur une liste chaînée

- Création
- Nombre d'éléments
- Recherche
- Insertion
- Suppression
- Concaténation
- Destruction

Lors de la création d'un élément, on utilise principalement le mécanisme
de l'allocation dynamique ce qui permet de récupérer l'adresse de
l'élément et de faciliter sa manipulation au travers de la liste.  Ne
pas oublier de libérer la mémoire allouée pour les éléments lors de leur
suppression…

#### Calcul du nombre d'éléments dans la liste

Pour évaluer le nombre d'éléments dans une liste, on effectue le
parcours de la liste à partir de la tête, et on passe d'élément en
élément grâce au champ *next* de la structure `Element`. On incrément
le nombre d'éléments jusqu'à ce que le pointeur *next* soit égal à `NULL`.

```c
size_t count = 0;

for (Element *e = &head; e != NULL; e = e->next)
    count++;
```

#### Détection des boucles

Attention, la technique précédente ne fonctionne pas dans tous les cas, spécialement lorsqu'il y a des boucles dans la liste chaînée. Prenons l'exemple suivant :

![Boucle dans une liste chaînée](../assets/images/loop.drawio)

La liste se terminant par une boucle, il n'y aura jamais d'élément de fin et le nombre d'éléments
calculé sera infini. Or, cette liste a un nombre fixe d'éléments. Comment donc les compter ?

Il existe un algorithme nommé détection de cycle de Robert W. Floyd aussi appelé *algorithme du lièvre et de la tortue*. Il consiste à avoir deux pointeurs qui parcourent la liste chaînée. L'un avance deux fois plus vite que le second.

![Algorithme de détection de cycle de Robert W. Floyd](../assets/images/floyd.drawio)

```c
size_t compute_length(Element* head)
{
    size_t count = 0;

    Element* slow = head;
    Element* fast = head;

    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;

        count++;

        if (slow == fast) {
            // Collision
            break;
        }
    }

    // Case when no loops detected
    if (fast == NULL || fast->next == NULL) {
        return count;
    }

    // Move slow to head, keep fast at meeting point.
    slow = head;
    while (slow != fast) {
        slow = slow->next;
        fast = fast->next;

        count--;
    }

    return count;
}
```

!!! tip

    Une bonne idée pour se simplifier la vie est simplement d'éviter la création de boucles.

#### Insertion

L'insertion d'un élément dans une liste chaînée peut-être implémentée de la façon suivante :

```c
Element* insert_after(Element* e, void* payload)
{
    Element* new = malloc(sizeof(Element));

    memcpy(new->payload, payload, sizeof(new->payload));

    new->next = e->next;
    e->next = new;

    return new;
}
```

#### Suppression

La suppression implique d'accéder à l'élément parent, il n'est donc pas possible à partir d'un élément donné de le supprimer de la liste.

```c
void delete_after(Element* e)
{
    e->next = e->next->next;
    free(e);
}
```

#### Recherche

Rechercher dans une liste chaînée est une question qui peut-être complexe et il est nécessaire de ce poser un certain nombre de questions :

- Est-ce que la liste est triée?
- Combien d'espace mémoire puis-je utiliser?

On sait qu'une recherche idéale s'effectue en $O(log(n))$, mais que la solution triviale en $O(n)$ est la suivante :

## Liste doublement chaînée

### Liste chaînée XOR

L'inconvénient d'une liste doublement chaînée est le surcoût nécessaire au stockage d'un élément. Chaque élément contient en effet deux pointeurs sur l'élément précédent (*prev*) et suivant (*next*).

```text
...  A       B         C         D         E  ...
        –>  next –>  next  –>  next  –>
        <–  prev <–  prev  <–  prev  <–
```

Cette liste chaînée particulière compresse les deux pointeurs en un seul en utilisant l'opération XOR (dénotée ⊕).

```text
...  A        B         C         D         E  ...
        <–>  A⊕C  <->  B⊕D  <->  C⊕E  <->
```

Lorsque la liste est traversée de gauche à droite, il est possible de facilement reconstruire le pointeur de l'élément suivant à partir de l'adresse de l'élément précédent.

Les inconvénients de cette structure sont :

- Difficultés de débogage
- Complexité de mise en œuvre

L'avantage principal étant le gain de place en mémoire.

## Liste chaînée déroulée (Unrolled linked list)

Une liste chaînée déroulée rassemble les avantages d'un tableau et d'une liste chaînée. Elle permet d'accroître les performances en réduisant l'overhead de réservation mémoire avec `malloc`.

![Liste chaînée déroulée](../assets/images/unrolled-linked-list.drawio)

```c
typedef struct Node {
    struct Node *next;
    size_t count;  // Nombre d'éléments
    int elements[]; // Membre flexible contenant les éléments
} Node;
```

## Arbres

![Arbre binaire IRL](../assets/images/binary-tree.jpg)

### Arbre binaire de recherche

L'objectif de cette section n'est pas d'entrer dans les détails des [arbres binaires](https://fr.wikipedia.org/wiki/Arbre_binaire_de_recherche) dont la théorie requiert un ouvrage dédié, mais de vous sensibiliser à l'existence de ces structures de données qui sont à la base de beaucoup de langage de haut niveau comme C++, Python ou C#.

L'arbre binaire, n'est rien d'autre qu'une liste chaînée comportant deux enfants un `left` et un `right`:

![Arbre binaire équilibré](../assets/images/binary-tree.drawio)

Lorsqu'il est équilibré, un arbre binaire comporte autant d'éléments à gauche qu'à droite et lorsqu'il est correctement rempli, la valeur d'un élément est toujours :

- La valeur de l'enfant de gauche est inférieure à celle de son parent
- La valeur de l'enfant de droite est supérieure à celle de son parent

Cette propriété est très appréciée pour rechercher et insérer des données complexes. Admettons que l'on a un registre patient du type :

```c
struct patient {
    size_t id;
    char firstname[64];
    char lastname[64];
    uint8_t age;
}

typedef struct node {
    struct patient data;
    struct node* left;
    struct node* right;
} Node;
```

Si l'on cherche le patient numéro `612`, il suffit de parcourir l'arbre de façon dichotomique :

```c
Node* search(Node* node, size_t id)
{
    if (node == NULL)
        return NULL;

    if (node->data.id == id)
        return node;

    return search(node->data.id > id ? node->left : node->right, id);
}
```

L'insertion et la suppression d'éléments dans un arbre binaire font appel à des [rotations](https://fr.wikipedia.org/wiki/Rotation_d%27un_arbre_binaire_de_recherche), puisque les éléments doivent être insérés dans le correct ordre et que l'arbre, pour être performant, doit toujours être équilibré. Ces rotations sont donc des mécanismes de rééquilibrage de l'arbre ne sont pas triviaux, mais dont la complexité d'exécution reste simple, et donc performante.

### Heap

La structure de donnée `heap` aussi nommée tas ne doit pas être confondue avec le tas utilisé en allocation dynamique. Il s'agit d'une forme particulière de l'arbre binaire dit "presque complet", dans lequel la différence de niveau entre les feuilles n'excède pas 1. C'est-à-dire que toutes les feuilles sont à une distance identique de la racine plus ou moins 1.

Un tas peut aisément être représenté sous forme de tableau en utilisant la règle suivante :

Table: Opération d'accès à un élément d'un heap

| Cible            | Début à 0        | Début à 1      |
| ---------------- | ---------------- | -------------- |
| Enfant de gauche | $2*k  + 1$       | $2 * k$        |
| Enfant de droite | $2*k  + 2$       | $2 * k + 1$    |
| Parent           | $floor(k-1) / 2$ | $floor(k) / 2$ |

![Représentation d'un *heap*](../assets/images/heap.drawio)

## Queue prioritaire

Une queue prioritaire ou *priority queue*, est une queue dans laquelle les éléments sont traités par ordre de priorité. Imaginons des personnalités, toutes atteintes d'une rage de dents et qui font la queue chez un dentiste aux mœurs discutables. Ce dernier ne prendra pas ses patients par ordre d'arrivée, mais, par importance aristocratique.

```c
typedef struct Person {
   char *name;
   enum SocialStatus {
       PEON;
       WORKER;
       ENGINEER;
       DOCTOR;
       PROFESSOR;
       PRESIDENT;
       SUPERHERO;
   } status;
} Person;

int main() {
    ProrityQueue queue;
    queue_init(queue);

    for(int i = 0; i < 100; i++) {
       queue_enqueue(queue, (Person) {
          .name = random_name(),
          .status = random_status()
       });

       Person person;
       queue_dequeue(queue, &person);
       dentist_heal(person);
    }
}
```

La queue prioritaire dispose donc aussi des méthodes `enqueue` et `dequeue` mais le `dequeue` retournera l'élément le plus prioritaire de la liste. Ceci se traduit par trier la file d'attente à chaque opération `enqueue` ou `dequeue`. L'une de ces deux opérations pourrait donc avoir une complexité de $O(n log n)$. Heureusement, il existe des méthodes de tris performantes si un tableau est déjà trié et qu'un seul nouvel élément y est ajouté.

L'implémentation de ce type de structure de donnée s'appuie le plus souvent sur un *heap*, soit construite à partir d'un tableau statique, soit un tableau dynamique.

## Tableau de Hachage

Les tableaux de hachage (*Hash Table*) sont une structure particulière dans laquelle une fonction dite de *hachage* est utilisée pour transformer les entrées en des indices d'un tableau.

L'objectif est de stocker des chaînes de caractères correspondant a des noms simples ici utilisés pour l'exemple. Une possible répartition serait la suivante :

![Tableau de hachage simple](../assets/images/hash-linear.drawio)

Si l'on cherche l'indice correspondant à `Ada`, il convient de pouvoir calculer la valeur de l'indice correspondant à partir de la valeur de la chaîne de caractère. Pour calculer cet indice aussi appelé *hash*, il existe une infinité de méthodes. Dans cet exemple, considérons une méthode simple. Chaque lettre est identifiée par sa valeur ASCII et la somme de toutes les valeurs ASCII est calculée. Le modulo 10 est ensuite calculé sur cette somme pour obtenir une valeur entre 0 et 9. Ainsi nous avons les calculs suivants :

```console
Nom    Valeurs ASCII     Somme  Modulo 10
---    --------------    -----  ---------
Mia -> {77, 105, 97}  -> 279 -> 4
Tim -> {84, 105, 109} -> 298 -> 1
Bea -> {66, 101, 97}  -> 264 -> 0
Zoe -> {90, 111, 101} -> 302 -> 5
Jan -> {74, 97, 110}  -> 281 -> 6
Ada -> {65, 100, 97}  -> 262 -> 9
Leo -> {76, 101, 111} -> 288 -> 2
Sam -> {83, 97, 109}  -> 289 -> 3
Lou -> {76, 111, 117} -> 304 -> 7
Max -> {77, 97, 120}  -> 294 -> 8
Ted -> {84, 101, 100} -> 285 -> 10
```

Pour trouver l'indice de `"Mia"` il suffit donc d'appeler la fonction suivante :

```c
int hash_str(char *s) {
    int sum = 0;
    while (*s != '\0') sum += s++;
    return sum % 10;
}
```

L'assertion suivante est donc vraie :

```c
assert(strcmp(table[hash_str("Mia")], "Mia") == 0);
```

Rechercher `"Mia"` et obtenir `"Mia"` n'est certainement pas l'exemple le plus utile. Néanmoins il est possible d'encoder plus qu'une chaîne de caractère et utiliser plutôt une structure de donnée :

```c
struct Person {
    char name[3 + 1 /* '\0' */];
    struct {
        int month;
        int day;
        int year;
    } born;
    enum {
        JOB_ASTRONOMER,
        JOB_INVENTOR,
        JOB_ACTRESS,
        JOB_LOGICIAN,
        JOB_BIOLOGIST
    } job;
    char country_code; // For example 41 for Switzerland
};
```

Dans ce cas, le calcul du hash se ferait sur la première clé d'un élément :

```c
int hash_person(struct Person person) {
    int sum = 0;
    while (*person.name != '\0') sum += s++;
    return sum % 10;
}
```

L'accès à une personne à partir de la clé se résout donc en `O(1)` car il n'y a aucune itération ou recherche à effectuer.

Cette [vidéo](https://www.youtube.com/watch?v=KyUTuwz_b7Q) YouTube explique bien le fonctionnement des tableaux de hachage.

### Collisions

Lorsque la **fonction de hachage** est mal choisie, un certain nombre de collisions peuvent apparaître. Si l'on souhaite par exemple ajouter les personnes suivantes :

```text
Sue -> {83, 117, 101} -> 301 -> 4
Len -> {76, 101, 110} -> 287 -> 1
```

On voit que les positions `4` et `1` sont déjà occupées par Mia et Tim.

Une stratégie de résolution s'appelle [Open adressing](https://en.wikipedia.org/wiki/Open_addressing). Parmi les possibilités de cette stratégie, le *linear probing* consiste à vérifier si la position du tableau est déjà occupée et en cas de collision, chercher la prochaine place disponible dans le tableau :

```c
Person people[10] = {0}

// Add Mia
Person mia = {.name="Mia", .born={.day=1,.month=4,.year=1991}};
int hash = hash_person(mia);
while (people[hash].name[0] != '\0') hash++;
people[hash] = mia;
```

Récupérer une valeur dans le tableau demande une comparaison supplémentaire :

```c
char key[] = "Mia";
int hash = hash_str(key)
while (strcmp(people[hash], key) != 0) hash++;
Person person = people[hash];
```

Lorsque le nombre de collisions est négligeable par rapport à la table de hachage, la recherche d'un élément est toujours en moyenne égale à $O(1)$, mais lorsque le nombre de collisions est prépondérant, la complexité se rapproche de celle de la recherche linéaire $O(n)$ et on perd tout avantage à cette structure de donnée.

Dans le cas extrême, pour garantir un accès unitaire pour tous les noms de trois lettres, il faudrait un tableau de hachage d'une taille $26^3 = 17576$ personnes. L'empreinte mémoire peut être considérablement réduite en stockant non pas une structure `struct Person` mais plutôt l'adresse vers cette structure :

```c
struct Person *people[26 * 26 * 26] = { NULL };
```

Dans ce cas exagéré, la fonction de hachage pourrait être la suivante :

```c
int hash_name(char name[4]) {
    int base = 26;
    return
        (name[0] - 'A') * 1 +
        (name[1] - 'a') * 26 +
        (name[2] - 'a') * 26 * 26;
}
```

### Facteur de charge

Le facteur de charge d'une table de hachage est donné par la relation :

$$
\text{Facteur de charge} = \frac{\text{Nombre total d'éléments}}{\text{Taille de la table}}
$$

Plus ce facteur de charge est élevé, dans le cas du *linear probing*, moins bon sera la performance de la table de hachage.

Certains algorithmes permettent de redimensionner dynamiquement la table de hachage pour conserver un facteur de charge le plus faible possible.

### Chaînage

Le chaînage ou *chaining* est une autre méthode pour mieux gérer les collisions. La table de hachage est couplée à une liste chaînée.

![Chaînage d'une table de hachage](../assets/images/hash-table.drawio)

### Fonction de hachage

Nous avons vu plus haut une fonction de hachage calculant le modulo sur la somme des caractères ASCII d'une chaîne de caractères. Nous avons également vu que cette fonction de hachage est source de nombreuses collisions. Les chaînes `"Rea"` ou `"Rae"` auront les même *hash* puisqu'ils contiennent les mêmes lettres. De même une fonction de hachage qui ne répartit pas bien les éléments dans la table de hachage sera mauvaise. On sait par exemple que les voyelles sont nombreuses dans les mots et qu'il n'y en a que six et que la probabilité que nos noms de trois lettres contiennent une voyelle en leur milieu est très élevée.

L'idée générale des fonctions de hachage est de répartir **uniformément** les clés sur les indices de la table de hachage. L'approche la plus courante est de mélanger les bits de notre clé dans un processus reproductible.

Une idée **mauvaise** et **à ne pas retenir** pourrait être d'utiliser le caractère pseudo-aléatoire de `rand` pour hacher nos noms :

```c
#include <stdlib.h>
#include <stdio.h>

int hash(char *str, int mod) {
    int h = 0;
    while(*str != '\0') {
        srand(h + *str++);
        h = rand();
    }
    return h % mod;
}

int main() {
    char *names[] = {
        "Bea", "Tim", "Len", "Sam", "Ada", "Mia",
        "Sue", "Zoe", "Rae", "Lou", "Max", "Tod"
    };
    for (int i = 0; i < sizeof(names) / sizeof(*names); i++)
        printf("%s : %d\n", names[i], hash(names[i], 10));
}
```

Cette approche nous donne une assez bonne répartition :

```console
$ ./a.out
Bea : 2
Tim : 3
Len : 0
Sam : 3
Ada : 4
Mia : 3
Sue : 6
Zoe : 5
Rae : 8
Lou : 0
Max : 3
Tod : 1
```

Dans la pratique, on utilisera volontiers des fonctions de hachage utilisées en cryptographies tels que [MD5](https://en.wikipedia.org/wiki/MD5) ou `SHA`. Considérons par exemple la première partie du poème Chanson de Pierre Corneille :

```console
$ cat chanson.txt
Si je perds bien des maîtresses,
J'en fais encor plus souvent,
Et mes voeux et mes promesses
Ne sont que feintes caresses,
Et mes voeux et mes promesses
Ne sont jamais que du vent.

$ md5sum chanson.txt
699bfc5c3fd42a06e99797bfa635f410  chanson.txt
```

Le *hash* de ce texte est exprimé en hexadécimal ( `0x699bfc5c3fd42a06e99797bfa635f410`). Converti en décimal `140378864046454182829995736237591622672` il peut être réduit en utilisant le modulo. Voici un exemple en C :

```c
#include <stdlib.h>
#include <stdio.h>
#include <openssl/md5.h>
#include <string.h>

int hash(char* str, int mod) {
    // Compute MD5
    unsigned int output[4];
    MD5_CTX md5;
    MD5_Init(&md5);
    MD5_Update(&md5, str, strlen(str));
    MD5_Final((char*)output, &md5);

    // 128-bits --> 32-bits
    unsigned int h = 0;
    for (int i = 0; i < sizeof(output)/sizeof(*output); i++) {
        h ^= output[i];
    }

    // 32-bits --> mod
    return h % mod;
}

int main() {
    char *text[] = {
        "La poule ou l'oeuf?",
        "Les pommes sont cuites!",
        "Aussi lentement que possible",
        "La poule ou l'oeuf.",
        "La poule ou l'oeuf!",
        "Aussi vite que nécessaire",
        "Il ne faut pas lâcher la proie pour l’ombre.",
        "Le mieux est l'ennemi du bien",
    };

    for (int i = 0; i < sizeof(text) / sizeof(*text); i++)
        printf("% 2d. %s\n", hash(text[i], 10), text[i]);
}
```

```console
$ gcc hash.c -lcrypto
$ ./a.out
1. La poule ou l'oeuf?
2. Les pommes sont cuites!
3. Aussi lentement que possible
4. La poule ou l'oeuf.
5. La poule ou l'oeuf!
6. Aussi vite que nécessaire
8. Il ne faut pas lâcher la proie pour l’ombre.
9. Le mieux est l'ennemi du bien
```

On peut constater qu'ici les indices sont bien répartis et que la fonction de hachage choisie semble uniforme.

## Piles ou LIFO (*Last In First Out*)

Une pile est une structure de donnée très similaire à un tableau dynamique, mais dans laquelle les opérations sont limitées. Par exemple, il n'est possible que :

- d'ajouter un élément (*push*) ;
- retirer un élément (*pop*) ;
- obtenir le dernier élément ajouté (*peek*) ;
- tester si la pile est vide (*is_empty*) ;
- tester si la pile est pleine avec (*is_full*).

Une utilisation possible de pile sur des entiers serait la suivante :

```c
#include "stack.h"

int main() {
    Stack stack;
    stack_init(&stack);

    stack_push(42);
    assert(stack_peek() == 42);

    stack_push(23);
    assert(!stack_is_empty());

    assert(stack_pop() == 23);
    assert(stack_pop() == 42);

    assert(stack_is_empty());
}
```

Les piles peuvent être implémentées avec des tableaux dynamiques ou des listes chaînées (voir plus bas).

## Queues ou FIFO (*First In First Out*)

Les queues sont aussi des structures très similaires à des tableaux dynamiques, mais elles ne permettent que les opérations suivantes :

- ajouter un élément à la queue (*push*) aussi nommé *enqueue* ;
- supprimer un élément au début de la queue (*shift*) aussi nommé *dequeue* ;
- tester si la queue est vide (*is_empty*) ;
- tester si la queue est pleine avec (*is_full*).

Les queues sont souvent utilisées lorsque des processus séquentiels ou parallèles s'échangent des tâches à traiter :

```c
#include "queue.h"
#include <stdio.h>

void get_work(Queue *queue) {
    while (!feof(stdin)) {
        int n;
        if (scanf("%d", &n) == 1)
            queue_enqueue(n);
        scanf("%*[^\n]%[\n]");
    }
}

void process_work(Queue *queue) {
    while (!is_empty(queue)) {
        int n = queue_dequeue(queue);
        printf("%d est %s\n", n, n % 2 ? "impair" : "pair";
    }
}

int main() {
    Queue* queue;

    queue_init(&queue);
    get_work(queue);
    process_work(queue);
    queue_free(queue);
}
```

## Performances

Les différentes structures de données ne sont pas toutes équivalentes en termes de performances. Il convient, selon l'application, d'opter pour la structure la plus adaptée, et par conséquent il est important de pouvoir comparer les différentes structures de données pour choisir la plus appropriée. Est-ce que les données doivent être maintenues triées ? Est-ce que la structure de donnée est utilisée comme une pile ou un tas ? Quelle est la structure de donnée avec le moins d'*overhead* pour les opérations de `push` ou `unshift` ?

L'indexation (*indexing*) est l'accès à une certaine valeur du tableau par exemple avec `a[k]`. Dans un tableau statique et dynamique l'accès se fait par pointeur depuis le début du tableau soit : `*((char*)a + sizeof(a[0]) * k)` qui est équivalant à `*(a + k)`. L'indexation par arithmétique de pointeur n'est pas possible avec les listes chaînées dont il faut parcourir chaque élément pour découvrir l'adresse du prochain élément :

```c
int get(List *list) {
    List *el = list->head;
    for(int i = 0; i < k; i++)
        el = el.next;
    return el.value;
}
```

L'indexation d'une liste chaînée prend dans le cas le plus défavorable $O(n)$.

Les arbres binaires ont une structure qui permet naturellement la dichotomique. Chercher l'élément 5 prend 4 opérations : `12 -> 4 -> 6 -> 5`. L'indexation est ainsi possible en $O(log~n)$.

```text
            12
             |
         ----+----
       /           \
      4            12
     --            --
   /    \        /    \
  2      6      10    14
 / \    / \    / \   /  \
1   3  5   7  9  11 13  15
```

Le tableau suivant résume les performances obtenues pour les différentes structures de données que nous avons vues dans ce chapitre :

Table: Comparaison des performances des structures récursives

| Action            | Tableau    | Liste               | Buffer    | Arbre        | Hash Map  |
| ----------------- | ---------- | ------------------- | --------- | ------------ | --------- |
|                   | Statique   | Dynamique           | chaînée   | circulaire   | binaire   | linéaire    |
| **Indexing**      | 1          | 1                   | n         | 1            | log n     | 1           |
| **Unshift/Shift** | n          | n                   | 1         | 1            | log n     | n           |
| **Push/Pop**      | 1          | 1 amorti            | 1         | 1            | log n     | 1           |
| **Insert/Delete** | n          | n                   | 1         | n            | log n     | n           |
| **Search**        | n          | n                   | n         | n            | log n     | 1           |
| **Sort**          | n log n    | n log n             | n log n   | n log n      | 1         | *n/a*       |
