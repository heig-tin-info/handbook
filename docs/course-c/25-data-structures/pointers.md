[](){#pointers}
# Pointeurs

[Attention les vélos](https://fr.wikiquote.org/wiki/Le_Jour_de_gloire), on s'attaque à un sujet délicat, difficile, scabreux, mais nécessaire. Un sujet essentiel, indispensable et fantastique: les [pointeurs](https://fr.wikipedia.org/wiki/Pointeur_(programmation)).

Les pointeurs sont des **variables** qui, au lieu de stocker une valeur, stockent une **adresse mémoire**. Dans quel but me direz-vous ? Pour créer des indirections, simplifier l'exécution du code.

Prenons un exemple concret. Le [Vicomte de Valmont](https://fr.wikipedia.org/wiki/Vicomte_de_Valmont) décide d'écrire à la marquise de Merteuil et il rédige une lettre. Il cachette sa lettre et la dépose dans sa boîte aux lettres pour enlèvement par le facteur moyennant quelques sous. En des termes programmatiques, on a :

```c
char lettre[] = "Chère Marquise, ...";
```

Cette variable `lettre` est dès lors enregistrée en mémoire à l'adresse `0x12345abc` qui pourrait correspondre à l'emplacement de la boîte aux lettres du Vicomte.

Le facteur qui ne craint pas la besogne prend connaissance du courrier à livrer, mais constate avec effroi que le cachet de cire a fondu sous l'effet du réchauffement climatique. La lettre est collée au fond de la boîte et il ne parvient pas à la détacher. Pire encore, et ajoutant à la situation déjà cocasse un dramatisme sans équivoque, à forcer de ses maigres doigts le papier de l'enveloppe se déchire et le contenu de lettre indécollable lui est révélée.

Je l'admets volontiers, il me faut bien faire quelques pirouettes pour justifier qu'une valeur en mémoire ne peut être transportée d'un lieu à un autre à simple dos de facteur. Aussi, notre facteur qui est si bon, mais qui n'a plus la mémoire de sa jeunesse, ni papier d'ailleurs, décide de mémoriser la lettre et de la retranscrire chez madame la Marquise qu'il connaît bien. Or comme il est atteint de la maladie de *64-bits* il n'arrive à mémoriser que 8 caractères `Chère Ma`. Sur son bolide, il arrive à destination et retranscrit dans le fond de la boîte de madame de Merteuil les huit caractères fidèlement retranscrits. Comme il est bonnet, mais assidu, il consacre le restant de sa journée en des allers-retours usant la gomme de son [tout nickelé](https://www.paroles.net/georges-brassens/paroles-pour-me-rendre-a-mon-bureau) jusqu'à ce que toute la lettre ait été retranscrite.

On se retrouve avec une **copie** de la lettre chez madame de Merteuil :

```c
char valmont_mailbox[] = "Chère Maquise, ...";
char merteil_mailbox[] = "Chère Maquise, ...";
```

La canicule n'étant pas finie, et cette physique discutable ne pouvant être déjouées, la marquise décide de résoudre le problème et se rend à [Tarente](https://fr.wikipedia.org/wiki/Pierre_Choderlos_de_Laclos) (un très mauvais choix par jour de canicule) et formule sa réponse sur le mur sud du Castello Aragonese ayant préalablement pris soin de noter la position GPS du mur avec exactitude (`0x30313233`):

```c
char castello_wall[] = "Cher Vicomte ...";
char (*gps_position)[] = &castello_wall;
```

De retour chez elle, elle prie le facteur de transmettre au vicomte de Valmont ce simple mot: `0x30313233`. Le facteur parvient sans mal à mémoriser les 4 octets du message.

La variable `gps_position` ne contient donc pas le message, mais seulement l'adresse mémoire de ce message. Il s'agit ici d'un **pointeur sur un tableau de caractères**.

Entre-temps, le vicomte qui est paresseux s'est équipé d'un téléscripteur capable d'exécuter du code C et il parvient à lire le message de sa complice la marquise.

```c
printf("%s", *gps_position);
```

S'il avait oublié l'astérisque (`*`, U+002A) dans cette dernière ligne, il n'aurait pas vu le message espéré, mais simplement `0123` qui correspond au contenu à l'adresse mémoire ou se trouve l'adresse du message (et non le message).

L'astérisque agit donc comme un **déréférencement**, autrement dit, la demande expresse faite au dévoué facteur d'aller à l'adresse donnée récupérer le contenu du message.

Oui, mais, on utilise un astérisque pour déréférencer, mais dans l'exemple précédant on a utilisé l'esperluette (`&`, U+0026): `&castello_wall`, pourquoi ? L'esperluette quand elle préfixe une variable peut être traduite par **l'adresse de**. Cela revient à l'étape pendant laquelle la marquise a mesuré la position GPS du mur sur à Tarente.

Il manque encore une chose, il y a aussi une astérisque sur `(*gps_position)[]`. Cela vaudrait-il dire qu’on déréférence la position GPS pour affecter l'adresse du mur ? Non, pas du tout... Et c'est d'ailleurs à cette étape que les novices perdent le fil. Où en étais-je ?

Notons qu'il y a plusieurs interprétations de l'astérisque en C :

- Opérateur de multiplication: `a * b`
- Déréférencement d'un pointeur: `*ptr`
- Déclaration d'un pointeur: `int * ptr`

Donc ici, on déclare un pointeur. En appliquant la règle gauche-droite que l'on verra plus bas :

```c
char (*gps_position)[]
       ^^^^^^^^^^^^        1. gps_position est
                   ^       2. ...
      ^                    3. un pointeur sur
                    ^^     4. un tableau de
^^^^                       5. caractères
                           6. PROFIT...
```

Résumons :

- Un pointeur est une **variable**
- Il contient une **adresse mémoire**
- Il peut être **déréférencé** pour en obtenir la valeur de l'élément qu'il pointe
- **L'adresse d'une variable** peut être obtenue avec une esperluette

## Pointeur simple

Le format le plus simple d'un pointeur sur un entier s'écrit avec l'astérisque `*`:

```c
int* ptr = NULL;
```

La valeur `NULL` correspond à l'adresse nulle `0x00000000`. On utilise cette convention pour bien indiquer qu'il s'agit d'une adresse et non d'une valeur scalaire.

!!! warning "nul, null, nulll"

    Attention à l'écriture de `NULL`:

    - `nul` est le caractère de fin de chaîne de caractères `'\0'` ;
    - `null` est une adresse qui pointe nulle part ;
    - `nulll` veut dire que vous avez fait une faute de frappe.

À tout moment, la valeur du pointeur peut être assignée à l'adresse d'un entier puisque nous avons déclaré un pointeur sur un entier :

```c
int boiling = 100;
int freezing = 0;

for (char i = 0; i < 10; i++) {
    ptr = i % 2 ? &boiling : &freezing;
    printf("%d", *ptr);
}
```

Lorsque nous avions vu les tableaux, nous écrivions :

```c
int array[10] = {0,1,2,3,4,5,6,7,8,9};
```

Vous ne le saviez pas, mais 𝄽 *plot twist* 𝄽 la variable `array` est un pointeur, et la preuve est que `array` peut être déréférencé:

```c
printf("%d", *array); // Affiche 0
```

La différence entre un **tableau** et un **pointeur** est la suivante :

- Il n'est pas possible d'assigner une adresse à un tableau
- Il n'est pas possible d'assigner des valeurs à un pointeur

D'ailleurs, l'opérateur crochet `[]` n'est rien d'autre qu'un [sucre syntaxique](https://fr.wikipedia.org/wiki/Sucre_syntaxique):

```c
a[b] == *(a + b);
```

Bien que ce soit une très mauvaise idée, il est tout à fait possible d'écrire le code suivant puisque l'addition est commutative :

```c
assert(4[a] == a[4]);
```

## Arithmétique de pointeurs

Fondamentalement un pointeur est une variable qui contient un [ordinal](https://fr.wikipedia.org/wiki/Nombre_ordinal), c'est-à-dire qu'il peut être imaginé l'ajout à un pointeur une grandeur finie :

```c
char str[] = "Le vif zéphyr jubile sur les kumquats du clown gracieux";

for (char* ptr = str; *ptr; ptr++) {
    putchar(*ptr);
}
```

Imaginons que l'on souhaite représenter le carré magique suivant :

```
┌───┬───┬───┐
│ 4 │ 9 │ 2 │
├───┼───┼───┤
│ 3 │ 5 │ 7 │
├───┼───┼───┤
│ 8 │ 1 │ 6 │
└───┴───┴───┘
```

On peut le représenter en mémoire linéairement et utiliser de l'arithmétique de pointeur pour le dessiner :

```c
char magic[] = "492" "357" "816";

char* ptr = magic;

for (size_t row = 0; row < 3; row++) {
    for (size_t col = 0; col < 3; col++)
        putchar(*(ptr + row * 3 + col));
    putchar('\n');
}
```

Mais ? N'est-ce pas là ce que fait le compilateur lorsque l'adresse les éléments d'un tableau multidimensionnel ?

```c
char magic[][3] = {"792", "357", "816"};

for (size_t row = 0; row < 3; row++) {
    for (size_t col = 0; col < 3; col++)
        putchar(magic[row][col]);
    putchar('\n');
}
```

Oui très exactement, les deux codes sont similaires, mais l'un est plus élégant que l'autre, lequel d'après vous ?

L'arithmétique de pointeur est donc chose courante avec les tableaux. À vrai dire, les deux concepts sont interchangeables :

Table: Arithmétique sur tableau unidimensionnel

| Élément        | Premier  | Deuxième     | Troisième    | n ième |
|----------------|----------|--------------|--------------|--------|
| Accès tableau  | `a[0]` | `a[1]`     | `a[2]`     | `a[n - 1]` |
| Accès pointeur | `*a`   | `*(a + 1)` | `*(a + 2)` | `*(a + n - 1)` |


De même, l'exercice peut être répété avec des tableaux à deux dimensions :

Table: Arithmétique sur tableau bidimensionnel

| Élément        | Premier         | Deuxième        | n ligne m colonne|
|----------------|-----------------|-----------------|------------------|
| Accès tableau  | `a[0][0]`     | `a[1][1]`     | `a[n - 1][m - 1]`|
| Accès pointeur | `*(*(a+0)+0)` | `*(*(a+1)+1)` | `*(*(a+i-1)+j-1)`|


## Pointeur et chaînes de caractères

```c
static const char* conjonctions[] = {
    "mais", "ou", "est", "donc", "or", "ni", "car"
};
```

![Pointeur sur une chaîne de caractère]({assets}/images/ptrstr.drawio)

Cette structure est très exactement la même que pour les arguments transmis à la fonction `main`: la définition `char *argv[]`.

## Structures et pointeurs

### Initialisation d'un pointeur sur une structure

De la même manière qu'avec les types standards, on peut définir un
pointeur sur une structure de données.

```c
typedef struct Date {
    unsigned char day;
    unsigned char month;
    unsigned int  year;
} Date;
```

L'exemple précédent définit un type de donnée *Date*. On pourrait donc
initialiser un pointeur sur cette structure de la façon suivante :

```c
Date date;
Date *p;  // Pointeur sur un type Date

p = &date;  // Initialisation du pointeur sur un type structuré
```

Le pointeur reste un pointeur, soit un espace mémoire qui contient une adresse vers la structure `Date`. En conséquence, la taille de ce pointeur est de 8 bytes sur une machine 64 bits :

```c
Date *p;
assert(sizeof(p) == 8);
```

### Utilisation d'un pointeur sur une structure

On a vu que les champs d'une structure sont accessibles au travers du
`.` faisant la liaison entre la variable et le champ. Cela est
valable si la variable est du type structuré. Si la variable est du type
pointeur sur une structure, on remplacera le `.` par `->`.

```c
Date date;
Date *p;

p = &date;

p->day = 29;
p->month = 12;
p->year = 1964;
```

La syntaxe `->` est un sucre syntaxique. Les deux écritures suivantes sont par conséquent équivalentes :

```c
p->year
(*p).year
```

### Utilisation d'un pointeur récursif sur une structure

Lorsqu'on utilise des listes chaînées, on a besoin de créer une
structure contenant des données ainsi qu'un pointeur sur un élément
précédent et un autre sur l'élément suivant. Ces pointeurs sont du même
type que la structure dans laquelle ils sont déclarés et cela impose un
style d'écriture spécifique :

```c
typedef struct Element {
  struct Element *prev;  // Pointeur sur l'élément précédent
  struct Element *next;  // Pointeur sur l'élément suivant
  unsigned long data;  // Donnée d'une liste chaînée
} Element;
```

Exemple d'utilisation :

```c
Element e[3];

// Premier élément de la liste
e[0].prev = NULL;
e[0].next = &e[1];

// Second élément de la liste
e[1].prev = &e[0];
e[1].next = &e[2];

// troisième élément de la liste
e[2].prev = &e[1];
e[2].next = NULL;
```

## Pointeurs et paramètres de fonctions

Les fonctions comportent une liste de paramètres permettant de retourner
une information au programme appelant. Il est souvent indispensable de
pouvoir fournir à une fonction des paramètres qu'elle peut modifier lors
de son exécution. Pour ce faire, on passera par l'utilisation de
pointeurs.

### Paramètres sous la forme de pointeurs

Le prototype d'une fonction recevant un (ou plusieurs) pointeur s'écrit
de la manière suivante :

```c
type fonction(Type *param);
```

Cette fonction reçoit un paramètre (*param*) qui est un pointeur sur le type `Type`.

Exemple de prototype :

```c
int compute(double x, double *pres);
```

La fonction *calcul* prend 2 paramètres. Le premier (*x*) est du type
double. Le second (*pres*) est un pointeur sur un double. Il sera donc
possible, lors de l'appel de la fonction, de lui donner l'adresse d'une
variable dans laquelle la fonction placera le résultat du calcul.

```c
int calcul(double x, double * pres) {
    *pres = x * 2.;  // calcul du double de x
                     // place le resultat à l'adresse pres
    return 0;  // code retour = 0 (int)
}

int main() {
    double value = 7.;
    double r = 0.;
    int res = 0;

    res = compute(value, &r);
    // res vaut maintenant 14.
}
```

Lors de l'appel d'une fonction recevant un pointeur comme paramètre, on
placera le symbole `&` pour lui donner l'adresse de la variable.

## Transtypage de pointeurs (cast)

Le `cast` de pointeur s'avère nécessaire lorsqu'un pointeur du type `void` est déclaré, comme c'est le cas pour la fonction de copie mémoire `memcpy`. En effet, cette fonction accepte en entrée un pointeur vers une région mémoire source, et un pointeur vers une région mémoire de destination. D'un cas d'utilisation à un autre, le format de ces régions mémoires peut être de nature très différente :

```c
char message[] = "Mind the gap, please!";
int array[128];
struct { int a; char b; float c[3] } elements[128];
```

Il faudrait donc autant de fonctions `memcpy` que de type possible, ce qui n'est ni raisonnable, ni même imaginable. Face à ce dilemme, on utilise un pointeur neutre, celui qui n'envie personne et que personne n'envie `void` et qui permet sans autre :

```c
void *ptr;

ptr = message;
ptr = array;
ptr = elements;
```

Que pensez-vous que `sizeof(void)` devrait retourner ? Formellement ceci devrait mener à une erreur de compilation, car `void` n'a pas de substance, et donc aucune taille associée. Néanmoins `gcc` est très permissif de base et (à ma [grande surprise](https://stackoverflow.com/questions/1666224/what-is-the-size-of-void)), il ne génère par défaut ni *warning*, ni erreurs sans l'option `-Wpointer-arith` sur laquelle nous aurons tout le loisir de revenir.

L'intérêt d'un pointeur, c'est justement de pointer une région mémoire et le plus souvent, de la balayer grâce à l'arithmétique de pointeurs. Notre fonction de copie mémoire doit en somme pouvoir parcourir toute la région mémoire de source et de destination et de ce fait incrémenter le pointeur. Mais, n'ayant aucune taille l'arithmétique de pointeur n'est pas autorisée avec le pointeur `void` et nous voilà bien avancés, notre pointeur ne nous est guère d'usage que son utilité éponyme: rien.

Or, le titre de cette section étant le transtypage, il doit donc y avoir moyen de s'en sortir par une pirouette programmatique dans laquelle je déclare un nouveau pointeur du type char auquel j'associe la valeur de ptr par un **cast explicite**.

```c
char *iptr = (char*)ptr;
```

Dès lors, l'arithmétique est redevient possible `iptr++`. Pourquoi ne pas avoir utilisé ce subterfuge plus tôt me direz-vous ? En effet, il m'aurait été possible d'écrire `char *ptr = (char*)elements;` directement et sans détour, mais ceci aurait alors mené à ce prototype-ci :

```c
void *memcpy(char* dest, const char* src, size_t n);
```

La clé est dans le standard ISO/IEC 9899:2011 section 6.3.2.3 page 55 :

> A pointer to void may be converted to or from a pointer to any object type. A pointer to any object type may be converted to a pointer to void and back again; the result shall compare equal to the original pointer.

Autrement dit, il n'est pas nécessaire ni recommandé de faire un transtypage explicite pour convertir vers et en provenance d'un pointeur sur `void`. Et donc, l'astuce de memcpy est que la fonction accepte n'importe quel type de pointeur et c'est le message auto documenté du code.

Et quant à l'implémentation de cette fonction me direz-vous ? Une possibilité serait :

```c
void memcpy(void *dest, void *src, size_t n)
{
    char* csrc = src;
    char* cdest = dest;

    for (size_t i = 0; i < n; i++)
        cdest[i] = csrc[i];
}
```

Où plus concis :

```c
void memcpy(void *dest, void *src, size_t n)
{
    for (size_t i = 0; i < n; i++)
        ((char*)dst)[i] = ((char*)src)[i];
}
```

Or, rien de tout ceci n'est juste. `memcpy` est une fonction fondamentale en C, ce pourquoi nous nous y attardons temps. Elle est constamment utilisée et doit être extrêmement performante. Aussi, si le compilateur cible une architecture 64-bits pourquoi diable copier les éléments par paquet de 8-bits. C'est un peu comme si notre facteur, au début de ce chapitre, aurait fait ses allers-retours avec en tête qu'un octet par trajet. L'implémentation dépend donc de l'architecture cible et doit tenir compte des éventuels effets de bords. Par exemple s'il faut copier un tableau de 9 x 32 bits. Une architecture 64-bits aura une grande facilité à copier les 8 premiers octets, mais quant au dernier, il s'agit d'un cas particulier et selon la taille de la copie et l'architecture du processeur, l'implémentation devra être ajustée. C'est pourquoi ce type très bas niveau de fonction est l'affaire d'une cuisine interne du compilateur et dont le développeur ne doit pas se soucier. Vous êtes comme [Thomas l'apôtre](https://fr.wikipedia.org/wiki/Thomas_(ap%C3%B4tre)), et ne me croyez pas ? Alors, digressons et essayons :

```c
#include <string.h>
#include <stdio.h>

int main(void)
{
    char a[] = "La Broye c'est fantastique!";
    char b[sizeof(a)];

    memcpy(a, b, sizeof(a));

    printf("%s %s", a, b);
}
```

On observe qu'il n'y a aucun appel de fonction à `memcpy` comme c'est le cas pour `printf` (`bl printf`). La copie tient place en 6 instructions.

```
main :
    // Entry
    str     lr, [sp, #-4]!
    sub     sp, sp, #60

    // Inline memcpy
    mov     ip, sp      // Destination address
    add     lr, sp, #28 // Source address (char b located 28 octets after a)

    ldmia   lr!, {r0, r1, r2, r3}   // Load 4 x 32-bits
    stmia   ip!, {r0, r1, r2, r3}   // Store 4 x 32-bits

    ldm     lr, {r0, r1, r2}        // Load 3 x 32-bits
    stm     ip, {r0, r1, r2}        // Store 3 x 32-bits

    // Display (printf)
    add     r2, sp, #28
    mov     r1, sp
    ldr     r0, .L4
    bl      printf

    // Exit
    mov     r0, #0
    add     sp, sp, #60
    ldr     pc, [sp], #4
.L4 :
    .word   .LC0
.LC0 :
    .ascii  "La Broye c'est fantastique!\000"
```

Vous pouvez jouer avec cet exemple sur le site [godbolt](https://godbolt.org).

## Pointeurs de fonctions

Un pointeur peut pointer n'importe où en mémoire, et donc il peut également pointer non pas sur une variable, mais sur une fonction. Les pointeurs de fonctions sont très utiles pour des fonctions de rappel ([callback](https://fr.wikipedia.org/wiki/Fonction_de_rappel)).

Par exemple on veut appliquer une transformation sur tous les éléments d'un tableau, mais la transformation n'est pas connue à l'avance. On pourrait écrire :

```c
int is_odd(int n)
{
    return !(n % 2);
}

void map(int array[], int (*callback)(int), size_t length)
{
    for (size_t i = 0; i < length; i++) {
        array[i] = callback(array[i]);
    }
}

void main(void)
{
    int array[] = {1,2,3,4,5};

    map(array, is_odd);
}
```

Avec la règle gauche droite, on parvient à décortiquer la déclaration :

```c
int (*callback)(int)
      ^^^^^^^^        callback is
              ^
     ^                a pointer on
               ^^^^^  a function taking an int
^^^                   and returning an int
```

## La règle gauche-droite

Cette [règle](http://cseweb.ucsd.edu/~ricko/rt_lt.rule.html) est une recette magique permettant de correctement décortiquer une déclaration C contenant des pointeurs. Il faut tout d'abord lire :

Table: Règles gauche droite

| Symbole | Traduction              | Direction         |
|---------|-------------------------|-------------------|
| `*`   | `pointeur sur`        | Toujours à gauche |
| `[]`  | `tableau de`          | Toujours à droite |
| `()`  | `fonction retournant` | Toujours à droite |

Première étape

: Trouver l'identifiant et se dire `L'identifiant est`.

Deuxième étape

: Chercher le symbole à droite de l'identifiant. Si vous trouvez un `()`, vous savez que cet identifiant est une fonction et vous avez *L'identifiant est une fonction retournant*. Si vous trouvez un `[]` vous dites alors *L'identifiant est un tableau de*. Continuez à droite jusqu'à ce que vous êtes à court de symboles, **OU** que vous trouvez une parenthèse fermante `)`.

Troisième étape

: Regardez le symbole à gauche de l'identifiant. S’il n'est aucun des symboles précédents, dites quelque chose comme `int`. Sinon, convertissez le symbole en utilisant la table de correspondance. Continuez d'aller à **gauche** jusqu'à ce que vous êtes à court de symboles **OU** que vous rencontrez une parenthèse ouvrante `(`.

Ensuite...

: Continuez les étapes 2 et 3 jusqu'à ce que vous avez une déclaration complète.

Voici quelques exemples :

```c
int *p[];
```

1. Trouver l'identifiant: `p`: `p est`

    ```c
    int *p[];
         ^
    ```

2. Se déplacer à **droite**: `p est un tableau de`

    ```c
    int *p[];
          ^^
    ```

3. Se déplacer à **gauche**: `p est un tableau de pointeurs sur`

    ```c
    int *p[];
        ^
    ```

4. Continuer à **gauche**: `p est un tableau de pointeurs sur un int`

    ```c
    int *p[];
    ^^^
    ```

### cdecl

Il existe un programme nommé [cdecl](https://github.com/paul-j-lucas/cdecl) qui permet de décoder de complexes déclaration c :

```console
$ cdecl 'char (*(*x[3])())[5]'
declare x as array 3 of pointer to function returning pointer to array 5 of char
```

Une version en ligne est également [disponible](https://cdecl.org/).

## Initialisation par transtypage

L'utilisation de structure peut être utile pour initialiser un type de donnée en utilisant un autre type de donnée. Nous citons ici deux exemples.

```c
int i = *(int*)(struct { char a; char b; char c; char d; }){'a', 'b', 'c', 'd'};
```

```c
union {
    int matrix[10][10];
    int vector[100];
} data;
```

## Enchevêtrement ou *Aliasing*

Travailler avec les pointeurs demande une attention particulière à tous
les problèmes d'*alisasing* dans lesquels différents pointeurs pointent sur
une même région mémoire.

Mettons que l'on souhaite simplement déplacer une région mémoire vers une nouvelle région mémoire. On pourrait implémenter le code suivant :

```c
void memory_move(char *dst, char*src, size_t size) {
    for (int i = 0; i < size; i++)
        *dst++ = *src++;
}
```

Ce code est très simple mais il peut poser problème selon les cas. Imaginons que l'on dispose d'un tableau simple de dix éléments et de deux pointeurs `*src` et `*dst`. Pour déplacer la région du tableau de 4 éléments vers la droite. On se dirait que le code suivant pourrait fonctionner :

```text
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│2│3│4│5│6│7│8│9│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
 ^*src ^*dst
      ┌─┬─┬─┬─┬─┬─┬─┐
      │0│1│2│3│4│5│6│
      └─┴─┴─┴─┴─┴─┴─┘
       ↓ ↓ ↓ ↓ ↓ ↓ ↓
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│2│0│1│2│3│4│5│6│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
```

Naïvement l'exécution suivante devrait fonctionner, mais les deux pointeurs source et destination s'enchevêtrent et le résultat n'est pas celui escompté.

```c
char array[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
char *src = &array[0];
char *dst = &array[3];

memory_move(b, a, 7);
```

```text
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│2│3│4│5│6│7│8│9│ Tableau d'origine
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│2│0│1│2│0│1│2│0│ Opération avec `memory_move`
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│2│0│1│2│3│4│5│6│ Opération avec `memmove` (fonction standard)
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
```

Notre simple fonction de déplacement mémoire ne fonctionne pas avec des régions mémoires qui s'enchevêtrent. En revanche, la fonction standard `memmove` de `<stdlib.h>` fonctionne, car elle autorise, au détriment d'une plus grande complexité, de gérer ce type de situation.

Notons que sa fonction voisine `memcpy` ne dois **jamais** être utilisée en cas d'*aliasing*. Cette fonction se veut performante, c'est-à-dire qu'elle peut être implémentée en suivant le même principe que notre exemple `memory_move`. Le standard **C99** ne définit pas le comportement de `memcpy` pour des pointeurs qui se chevauchent.

## Exercices de révision

!!! exercise "Esperluettes cascadées"

    Quel est le type de :

    ```c
    *&*&*&*&*&*&(int)x;
    ```

!!! exercise "Passage par adresse"

    Donnez les valeurs affichées par ce programme pour les variables `a` à `e`.

    ```c
    #include <stdio.h>
    #include <stdlib.h>

    int test(int a, int * b, int * c, int * d) {
        a = *b;
        *b = *b + 5;
        *c = a + 2;
        d = c;
        return *d;
    }

    int main(void) {
        int a = 0, b = 100, c = 200, d = 300, e = 400;
        e = test(a, &b, &c, &d);
        printf("a:%d, b:%d, c:%d, d:%d, e:%d\n", a, b, c, d, e);
    }
    ```

    ??? solution

        ```text
        a:0, b:105, c:102, d:300, e:102
        ```
