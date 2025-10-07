
[](){#linkedlist}

# Listes chaînées

## Définition

Les listes chaînées, en informatique, représentent une structure de données d'une élégance discrète, dont la simplicité apparente dissimule une puissance d'adaptation remarquable. Contrairement aux tableaux dynamiques, qui dépendent d'une allocation contiguë en mémoire et nécessitent des réallocations coûteuses lorsque leur capacité est dépassée, les listes chaînées se distinguent par leur nature flexible et décentralisée.

Une liste chaînée se compose d'une série de nœuds, chacun contenant un élément de données ainsi qu'un pointeur vers le nœud suivant. Cette architecture singulière permet à la liste de croître et de se contracter sans nécessiter de réallocation massive de mémoire : il suffit d'ajouter ou de retirer des nœuds au gré des besoins, sans déplacer les éléments existants. En d'autres termes, la mémoire n'est allouée que lorsque cela est nécessaire, éliminant ainsi les gâchis d'espace que peuvent entraîner les tableaux dynamiques lorsque ceux-ci sont sous-utilisés.

L’avantage principal de cette structure réside dans sa capacité à insérer ou supprimer des éléments avec une efficacité redoutable. Là où un tableau dynamique doit parfois déplacer de grandes portions de données pour insérer ou retirer un élément, une liste chaînée ne demande que la modification des quelques pointeurs concernés. Cette opération, d'une légèreté exemplaire, confère à la liste chaînée une fluidité dans la manipulation des données que les tableaux, même dynamiques, ne sauraient égaler.

Cependant, cette flexibilité n'est pas sans contrepartie. L'accès direct à un élément particulier est plus lent dans une liste chaînée que dans un tableau, car il faut parcourir les nœuds un à un, en suivant les pointeurs. Cette absence d'accès indexé, qui fait la force du tableau, devient ici une faiblesse relative, surtout pour les opérations qui nécessitent de fréquentes consultations des données.

## Exemple

Pour illustrer cette idée, imaginons un tableau statique dans lequel chaque élément est décrit par la structure suivante :

```c
struct Element {
    int value;
    int index_next_element;
};

struct Element elements[100];
```

Considérons les dix premiers éléments de la séquence de nombre [A130826](https://oeis.org/A130826) dans un tableau statique. Ensuite, répartissons ces valeurs aléatoirement dans notre tableau `elements` déclaré plus haut entre les indices 0 et 19.

![Construction d'une liste chainée à l'aide d'un tableau](/assets/images/static-linked-list.drawio)

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

Cette solution, qui consiste à utiliser un lien vers l'élément suivant, s'appelle une liste chaînée. Chaque élément dispose d'un lien vers l'élément suivant situé quelque part en mémoire. Les opérations d'insertion et de suppression au milieu de la chaîne sont maintenant effectuées en $O(1)$ contre $O(n)$ pour un tableau standard. En revanche l'espace nécessaire pour stocker ce tableau est doublé puisqu'il faut associer à chaque valeur le lien vers l'élément suivant.

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

Ce surcoût fait souvent partie du compromis entre la complexité d'exécution du code et la mémoire utilisée par ce programme.

Table: Coût des opérations dans des structures de données récursives

| Structure de donnée  | Pire cas      |                 |                      |                          |
| -------------------- | ------------- | --------------- | -------------------- | ------------------------ |
|                      | **Insertion** | **Suppression** | **Recherche (Trié)** | **Recherche (Non trié)** |
| Tableau, pile, queue | $O(n)$        | $O(n)$          | $O(\log(n))$         | $O(n)$                   |
| Liste chaînée simple | $O(1)$        | $O(1)$          | $O(n)$               | $O(n)$                   |

## Liste simplement chaînée (*linked-list*)

La figure suivante illustre un set d'éléments liés entre eux à l'aide d'un pointeur rattaché à chaque élément. On peut s'imaginer que chaque élément peut se situer n'importe où en mémoire et
qu'il n'est alors pas indispensable que les éléments se suivent dans l'ordre.

Il est indispensable de bien identifier le dernier élément de la liste grâce à son pointeur associé
à la valeur `NULL`.

![Liste chaînée simple](/assets/images/list.drawio)

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

### Calcul du nombre d'éléments dans la liste

Pour évaluer le nombre d'éléments dans une liste, on effectue le
parcours de la liste à partir de la tête, et on passe d'élément en
élément grâce au champ *next* de la structure `Element`. On incrément
le nombre d'éléments jusqu'à ce que le pointeur *next* soit égal à `NULL`.

```c
size_t count = 0;

for (Element *e = &head; e != NULL; e = e->next)
    count++;
```

### Détection des boucles

Attention, la technique précédente ne fonctionne pas dans tous les cas, spécialement lorsqu'il y a des boucles dans la liste chaînée. Prenons l'exemple suivant :

![Boucle dans une liste chaînée](/assets/images/loop.drawio)

La liste se terminant par une boucle, il n'y aura jamais d'élément de fin et le nombre d'éléments
calculé sera infini. Or, cette liste a un nombre fixe d'éléments. Comment donc les compter ?

Il existe un algorithme nommé détection de cycle de Robert W. Floyd aussi appelé *algorithme du lièvre et de la tortue*. Il consiste à avoir deux pointeurs qui parcourent la liste chaînée. L'un avance deux fois plus vite que le second.

![Algorithme de détection de cycle de Robert W. Floyd](/assets/images/floyd.drawio)

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

### Insertion

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

### Suppression

La suppression implique d'accéder à l'élément parent, il n'est donc pas possible à partir d'un élément donné de le supprimer de la liste.

```c
void delete_after(Element* e)
{
    e->next = e->next->next;
    free(e);
}
```

### Recherche

Rechercher dans une liste chaînée est une question qui peut-être complexe et il est nécessaire de ce poser un certain nombre de questions :

- Est-ce que la liste est triée?
- Combien d'espace mémoire puis-je utiliser?

On sait qu'une recherche idéale s'effectue en $O(log(n))$, mais que la solution triviale en $O(n)$ est la suivante :

## Liste doublement chaînée

La liste doublement chaînée n'est qu'une extension de la liste chaînée simple dans laquelle on rajoute un pointeur vers l'élément précédent. Cela augmente l'emprunte mémoire de chaque élément mais permet de parcourir la liste dans les deux sens.

![Liste chaînée simple](/assets/images/list-double.drawio)

## Liste chaînée XOR

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

![Liste chaînée déroulée](/assets/images/unrolled-linked-list.drawio)

```c
typedef struct Node {
    struct Node *next;
    size_t count;  // Nombre d'éléments
    int elements[]; // Membre flexible contenant les éléments
} Node;
```


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