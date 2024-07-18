# Algorithmes et conception

L'algorithmique est le domaine scientifique qui étudie les algorithmes, une suite finie et non ambiguë d'opérations ou d'instructions permettant de résoudre un problème ou de traiter des données.

Un algorithme peut être également considéré comme étant n'importe quelle séquence d'opérations pouvant être simulées par un système [Turing-complet](https://fr.wikipedia.org/wiki/Turing-complet). Un système est déclaré Turing-complet s'il peut simuler n'importe quelle [machine de Turing](https://fr.wikipedia.org/wiki/Machine_de_Turing). For heureusement, le langage C est Turing-complet puisqu'il possède tous les ingrédients nécessaires à la simulation de ces machines, soit compter, comparer, lire, écrire...

Dans le cas qui concerne cet ouvrage, un algorithme est une recette exprimée en une liste d'instructions et permettant de résoudre un problème informatique. Cette recette contient à peu de choses près les éléments programmatiques que nous avons déjà entre aperçus: des structures de contrôle, des variables, etc.

Généralement un algorithme peut être exprimé graphiquement en utilisant un organigramme (*flowchart*) ou un structogramme (*Nassi-Shneiderman diagram*) afin de s'affranchir du langage de programmation cible.

La **conception** aussi appelée [Architecture logicielle](https://fr.wikipedia.org/wiki/Architecture_logicielle) est l'art de penser un programme avant son implémentation. La phase de conception fait bien souvent appel à des algorithmes.

Pour être qualifiées d'algorithmes, certaines propriétés doivent être respectées :

1. **Entrées**, un algorithme doit posséder 0 ou plus d'entrées en provenance de l'extérieur de l'algorithme.
2. **Sorties**, un algorithme doit posséder au moins une sortie.
3. **Rigueur**, chaque étape d'un algorithme doit être claire et bien définie.
4. **Finitude**, un algorithme doit comporter un nombre fini d'étapes.
5. **Répétable**, un algorithme doit fournir un résultat répétable.

## Complexité d'un algorithme

Il est souvent utile de savoir quelle est la performance d'un algorithme afin de le comparer à un autre algorithme équivalent. Il existe deux indicateurs :

- La complexité en temps : combien de temps CPU consomme un algorithme pour s'exécuter.
- La complexité en mémoire : combien de mémoire tampon consomme un algorithme pour s'exécuter.

Bien évidemment, la complexité d'un algorithme dépend des données en entrée. Par exemple si on vous donne à corriger un examen de 100 copies, et le protocol de correction associé, votre temps de travail dépendra du nombre de copies à corriger, je sais de quoi je parle...

La complexité en temps et en mémoire d'un algorithme est souvent exprimée en utilisant la notation en O (*big O notation*). Cette notation a été ontroduite par le mathématicien et informaticien allemand Paul Bachmann en 1984 dans son ouvrage *Analytische Zahlentheorie*. Cependant, c'est le mathématicien austro-hongrois Edmund Landau qui a popularisé cette notation dans le contexte de la théorie des nombres.

En substance, la complexité en temps d'un algorithme qui demanderait 10 étapes pour être résolu s'écrirait :

$$
O(10)
$$

Un algorithme qui ferait une recherche dichotomique sur un tableau de $n$ éléments à une complexité $O(log(n))$. La recherche dichotomique c'est comme chercher un mot dans un dictionnaire. Vous ouvrez le dictionnaire à la moitié, si le mot est avant, vous répétez l'opération sur la première moitié, sinon sur la seconde. Vous répétez l'opération jusqu'à trouver le mot. À chaque étape vous éliminez la moitié restante des mots du dictionnaire. Si le dictionnaire contient 100'000 mots, vous aurez trouvé le mot en :

$$
\log_2(100'000) = 16.6
$$

étapes. C'est bien plus rapide que de parcourir le dictionnaire de manière linéaire, en tournant les pages une à une.

Prenons un algoritme qui prend un certain temps pour s'exécuter. L'algorithme $A$ prend $f(n)$ unités de temps pour une entrée de taille $n$. On peut dire que $A$ est en $O(g(n))$ si $f(n) \leq c \cdot g(n)$ pour tout $n \geq n_0$, où $c$ est une constante et $n_0$ est un entier.

Il existe différents indicateurs de Landau :

**Notation Big O (O)** :

: Utilisée pour décrire une borne supérieure asymptotique. Cela signifie qu'une fonction \( f(n) \) est en \( O(g(n)) \) s'il existe des constantes \( c > 0 \) et \( n_0 \) telles que \( f(n) \leq c \cdot g(n) \) pour tout \( n \geq n_0 \). En d'autres termes, \( g(n) \) est une limite supérieure sur le comportement de \( f(n) \) pour de grandes valeurs de \( n \).

: Big O est souvent utilisée pour décrire le pire cas.

**Notation Big Omega (Ω)** :

: Utilisée pour décrire une borne inférieure asymptotique. Cela signifie qu'une fonction \( f(n) \) est en \( \Omega(g(n)) \) s'il existe des constantes \( c > 0 \) et \( n_0 \) telles que \( f(n) \geq c \cdot g(n) \) pour tout \( n \geq n_0 \). En d'autres termes, \( g(n) \) est une limite inférieure sur le comportement de \( f(n) \) pour de grandes valeurs de \( n \).

: Big Omega est souvent utilisée pour décrire le meilleur cas.

**Notation Big Theta (Θ)** :

: Utilisée pour décrire une borne asymptotique stricte. Cela signifie qu'une fonction \( f(n) \) est en \( \Theta(g(n)) \) s'il existe des constantes \( c_1, c_2 > 0 \) et \( n_0 \) telles que \( c_1 \cdot g(n) \leq f(n) \leq c_2 \cdot g(n) \) pour tout \( n \geq n_0 \). En d'autres termes, \( g(n) \) est une approximation asymptotique exacte de \( f(n) \).

: Big Theta est utilisée pour décrire un comportement asymptotique précis, souvent interprété comme le cas moyen.

!!! example "Identifier les valeurs paires et impaires"

    À titre d'exemple, le programme suivant qui se charge de remplacer les valeurs paires d'un tableau par un $0$ et les valeurs impaires par un $1$ à une complexité en temps de $O(n)$ où `n` est le nombre d'éléments du tableau.

    ```c
    void discriminate(int* array, size_t length)
    {
        for (size_t i = 0; i < length; i++)
        {
            array[i] %= 2;
        }
    }
    ```

!!! example "Somme des entiers"

    Si on vous demande d'écrire un algorithme permettant de connaître la somme des entiers de $1$ à $n$, vous pourriez écrire un algorithme en $O(n)$ :

    === "C"

        ```c
        int sum(int n) {
            int sum = 0;
            for (int i = 1; i <= n; i++) {
                sum += i;
            }
            return sum;
        }
        ```

    === "Python"

        ```python
        def sum(n):
            return [i for i in range(1, n + 1)]
        ```

    Ensuite vous vous posez la question de savoir si vous pouvez faire mieux. En effet, il existe une formule mathématique permettant de calculer la somme des entiers de $1$ à $n$ :

    $$
    \sum_{i=1}^{n} i = \frac{n \cdot (n + 1)}{2}
    $$

    Cette formule est en $O(1)$.

    === "C"

        ```c
        int sum(int n) {
            return n * (n + 1) / 2;
        }
        ```

    === "Python"

        ```python
        def sum(n):
            return n * (n + 1) // 2
        ```

D'une manière générale, la plupart des algorithmes que l'ingénieur écrira appartiendront à ces catégories exprimées du meilleur au plus mauvais :

Table: Temps pour différentes complexités d'algorithmes

| Complexité    | $n = 100000$    | i7 (100'000 MIPS)                     |
| ------------- | --------------- | ------------------------------------- |
| $O(log(n))$   | 11              | 0.11 ns                               |
| $O(n)$        | 100'000         | 1 us                                  |
| $O(n log(n))$ | 1'100'000       | 11 us                                 |
| $O(n^2)$      | 10'000'000'000  | 100 ms (un battement de cil)          |
| $O(2^n)$      | très très grand | Le soleil devenu géante rouge         |
|               |                 | aura ingurgité la terre               |
| $O(n!)`       | trop trop grand | La galaxie ne sera plus que poussière |

Les différentes complexités peuvent être résumées sur la figure suivante :

![Différentes complexités d'algorithmes](../../assets/images/complexity.drawio)

Un algorithme en $O(n^2)$, doit éveiller chez le développeur la volonté de voir s'il n'y a pas moyen d'optimiser l'algorithme en réduisant sa complexité, souvent on s'aperçoit qu'un algorithme peut être optimisé et s'intéresser à sa complexité est un excellent point d'entrée.

Attention toutefois à ne pas mal évaluer la complexité d'un algorithme. Voyons par exemple les deux algorithmes suivants :

```c
int min = MAX_INT;
int max = MIN_INT;

for (size_t i = 0; i < sizeof(array) / sizeof(array[0]); i++) {
    if (array[i] < min) {
        min = array[i];
    }
    if (array[i] > min) {
        max = array[i];
    }
}
```

```c
int min = MAX_INT;
int max = MIN_INT;

for (size_t i = 0; i < sizeof(array) / sizeof(array[0]); i++)
{
    if (array[i] < min) {
        min = array[i];
    }
}

for (size_t i = 0; i < sizeof(array) / sizeof(array[0]); i++)
{
    if (array[i] > min) {
        max = array[i];
    }
}
```

!!! exercise "Triangle évanescent"

    Quel serait l'algorithme permettant d'afficher :

    ```c
    *****
    ****
    ***
    **
    *
    ```

    et dont la taille peut varier ?

!!! exercise "L'entier manquant"

    On vous donne un gros fichier de 3'000'000'000 entiers positifs 32-bits, il vous faut générer un entier qui n'est pas dans la liste. Le hic, c'est que vous n'avez que 500 MiB de mémoire de travail. Quel algorithme proposez-vous ?

    Une fois le travail terminé, votre manager vient vous voir pour vous annoncer que le cahier des charges a été modifié. Le client dit qu'il n'a que 10 MiB. Pensez-vous pouvoir résoudre le problème quand même ?

## Machines d'états

## Diagrammes visuels

- Diagrammes en flux
- Structogrammes
- Diagramme d'activités
- Machines d'états ([UML state machine](https://en.wikipedia.org/wiki/UML_state_machine))
- [BPMN](https://en.wikipedia.org/wiki/Business_Process_Model_and_Notation) (*Business Process Model and Notation*)

## Récursivité

La [récursivité](https://fr.wikipedia.org/wiki/R%C3%A9cursivit%C3%A9) est une autoréférence. Il peut s'agit en C d'une fonction qui s'appelle elle-même.

!!! exercise "La plus petite différence"

    Soit deux tableaux d'entiers, trouver la paire de valeurs (une dans chaque tableau) ayant la plus petite différence (positive).

    Exemple :

    ```c
    int a[] = {5, 3, 14, 11, 2};
    int b[] = {24, 128, 236, 20, 8};

    int diff = 3 // pair 11, 8
    ```

    1. Proposer une implémentation
    2. Quelle est la complexité de votre algorithme ?

## Programmation dynamique

La programmation dynamique est une méthode algorithmique datant des années 1950, mais devenue populaire ces dernières années. Elle permet de coupler des algorithmes récursifs avec le concept de mémoïsation.

Prenons par exemple l'algorithme de Fibonacci récursif :

```c
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

Le problème de cet algorithme est sa performance. Appeler `fibonacci(50)` demandera de calculer `fibonacci(49)` et `fibonacci(48)` mais pour calculer `fibonacci(49)` il faudra recalculer `fibonacci(48)`. On voit qu'on effectue du travail à double. En réalité c'est bien pire que ça. La complexité est de $O(2^n)$. Donc pour calculer la valeur `50` il faudra effectuer $1 125 899 906 842 624$ opérations. Avec un ordinateur capable de calculer 1 milliard d'opérations par seconde, il faudra tout de même plus d'un million de secondes. Cet algorithme est donc très mauvais !

En revanche, si l'on est capable de mémoriser dans une table les résultats précédents des appels de Fibonacci, les performances seront bien meilleures.

Voici l'algorithme modifié :

```c
int fibonacci(int n) {
    static int memo[1000] = {0};
    if (memo[n]) return memo[n];
    if (n <= 1) return n;
    return memo[n] = fibonacci(n - 1) + fibonacci(n - 2);
}
```

Sa complexité est ainsi réduite à $O(2\cdot n)$ et donc $O(n)$. En revanche, l'approche dynamique demande un espace mémoire supplémentaire. On n'a rien sans rien et l'éternel dilemme mémoire versus performance s'applique toujours.

## Algorithmes utilitaires

### Slurp

Souvent on a besoin de lire l'entrée standard en entier dans une chaîne de caractère. Il faut convertir le flux d'entrée en une chaîne de caractère. Cependant, comme l'entrée standard n'est pas *seekable*, il faut lire le flux caractère par caractère. Une implémentation possible se repose sur le concept des tableaux dynamiques.

```c title="slurp.h"
--8<-- "../../assets/src/slutp/slurp.h"
```

```c title="slurp.c"
--8<-- "../../assets/src/slutp/slurp.c"
```

## Algorithmes célèbres

### Exponentiation rapide

Cet algorithme permet de calculer rapidement des puissances entières ($a^n$). La méthode naïve consiste à calculer les puissances avec une boucle :

```c
long long pow(long long a, long long n) {
    for (int i = 0; i < n - 1; i++) {
        a *= a;
    }
}
```

La complexité de cet algorithme est $O(n)$. Il est possible de faire mieux en $O(n log n)$.

```c
long long bin_pow(long long a, long long b) {
    if (b == 0) return 1;
    long long res = bin_pow(a, b / 2);
    return res * res * (b % 2 ? a : 1);
}
```

Comme évoqué plus haut, un algorithme récursif est souvent moins performant que sa variante itérative. Voici l'implémentation itérative :

```c
long long bin_pow(long long a, long long b) {
    long long res = 1;
    while (b > 0) {
        if (b & 1) res = res * a;
        a *= a;
        b /= 2;
    }
    return res;
}
```

### Racine carrée inverse rapide

Cet algorithme a été développé chez Silicon Graphics au début des années 90. Il a été utilisé dans des jeux vidéos comme [Quake III Arena](https://fr.wikipedia.org/wiki/Quake_III_Arena) pour améliorer la performance du calcul des angles d'incidence dans la réflexion des lumières.

```c
float Q_rsqrt(float number)
{
    const float threehalfs = 1.5F;

    float x2 = number * 0.5F;
    float y = number;
    long i = *(long *) &y; // Evil floating point bit level hacking
    i = 0x5f3759df - (i >> 1); // What the fuck?
    y = *(float *) &i;
    y = y * (threehalfs - (x2 * y * y)); // 1st iteration
#if BETTER
    y = y * (threehalfs - (x2 * y * y)); // 2nd iteration
#endif
    return y;
}
```

Cet algorithme de [racine carrée inverse rapide](https://fr.wikipedia.org/wiki/Racine_carr%C3%A9e_inverse_rapide) utilise une constante magique `0x5f3759df`. L'implémentation proposée ci-dessus est extraite du code source du jeu Quake III arena ([q_math.c](https://github.com/id-Software/Quake-III-Arena/blob/dbe4ddb10315479fc00086f08e25d968b4b43c49/code/game/q_math.c#L552)) disponible sur GitHub.

Ce n'est pas un algorithme très académique, il s'agit d'un [kludge](https://fr.wikipedia.org/wiki/Kludge), une solution irrespectueuse des règles de l'art de la programmation, car la valeur `y` est transtypée en un `long` (`i = *(long *)&y`. C'est cette astuce qui permet de tirer avantage que les valeurs en virgule flottantes sont exprimées en puissances de 2.

### Algorithme de Rabin-Karp

Cet algorithme [Rabin-Karp](https://fr.wikipedia.org/wiki/Algorithme_de_Rabin-Karp) permet la recherche d'une sous-chaîne de caractère. Sa complexité moyenne est $O(n + m)$.

```c title="rabin-karp.c"
--8<-- "docs../../assets/src/rabin-karp.c"
```

### Algorithme de Shunting Yard

L'algorithme de [Shunting Yard](https://fr.wikipedia.org/wiki/Algorithme_de_Shunting-yard) est un algorithme de parsing d'expression mathématique. Il permet de transformer une expression mathématique en notation infixée en une expression postfixée. L'algorithme a été inventé par Edsger Dijkstra en 1961.

Imaginez que vous ayez une expression mathématique sous forme d'une chaîne de caractères :

```text
2 + 3 * 8 - 2 * ( 2 - 4 / ( 3 * 8 ) )
```

Comment calculer cette expression ? Si vous procédez de gauche à droite, vous allez rencontrer des parenthèses et des priorités d'opérations.

L'algorithme se compose de deux files d'attente (FIFO) et d'une pile (LIFO). La file d'attente de sortie contiendra l'expression postfixée. La pile contiendra les opérateurs.

![Algorithme de shunting yard](../../assets/images/shunting-yard.drawio)

Commençons par quelques définitions :

**TOKEN**

: Un token est un élément de l'expression mathématique. Il peut s'agir d'un nombre, d'un opérateur ou d'une parenthèse.

**INPUT**

: Une file d'attente contenant les **TOKENS** de l'expression mathématique à traiter.

**OUTPUT**

: Une file d'attente qui contiendra les **TOKENS** de l'expression postfixée.

**STACK**

: Une pile qui contiendra les opérateurs.

Voici le pseudo code de l'algorithme :

- **Tant qu'il** y a des *TOKEN* à lire:
  - Lire le *TOKEN*
    **Si** le *TOKEN* est:
    - Un nombre:
      - Le déplacer sur *OUTPUT*.
    - Un opérateur $O_1$
      - **Tant que**:
        - Il y a un opérateur $O_2$ sur le dessus *STACK*,
          - **et** que ce n'est pas une parenthèse gauche,
          - **et** que $O_2$ a une plus grande priorité que $O_1$,
        - **ou** que $O_2$ a la même priorité que $O_1$,
          - **et** que $O_1$ est associatif à gauche.
        - **Alors**:
          - Déplacer $O_2$ de *STACK* sur *OUTPUT*.
          - Déplacer $O_1$ sur le *STACK*.
    - Une parenthèse gauche (`(`):
      - Déplacer sur le *STACK*.
    - Une parenthèse droite (`)`):
      - **Tant que** l'opérateur sur le dessus du *STACK* **n'est pas** une parenthèse gauche.
        - **Alors**, déplacer le dernier opérateur du *STACK* sur *OUTPUT*.
        - Supprimer la parenthèse gauche du *STACK*.
- **Tant qu'il** y a des *TOKEN* sur le *STACK*:
  - Déplacer le *TOKEN* de *STACK* sur *OUTPUT*

On observe que si on dispose de fonctions pour ajouter/supprimer des éléments d'une file d'attente et d'une pile, l'algorithme est relativement simple à implémenter. Voici l'implémentation en C :

=== "main.c"

    ```c
    --8<-- "docs../../assets/src/shunting-yard/main.c"
    ```

=== "queue.h"

    ```c
    --8<-- "docs../../assets/src/shunting-yard/queue.h"
    ```

=== "stack.h"

    ```c
    --8<-- "docs../../assets/src/shunting-yard/stack.h"
    ```

=== "queue.c"

    ```c
    --8<-- "docs../../assets/src/shunting-yard/queue.c"
    ```

=== "stack.c"

    ```c
    --8<-- "docs../../assets/src/shunting-yard/stack.c"
    ```

!!! info "Notation polonaise inverse"

    La notation polonaise inverse (RPN) est une notation mathématique dans laquelle chaque opérateur suit ses opérandes. Par exemple, l'expression `3 + 4` s'écrira `3 4 +`. Cette notation a été inventée par le mathématicien polonais Jan Łukasiewicz.

    Elle a été longtemps utilisée par les calculatrices Hewlett-Packard et permet de s'affranchir des parenthèses. En effet, l'expression `3 + 4 * 5` s'écrira `3 4 5 * +`.

    La calculatrice mythique HP-42s apparue en 1988 était utilisée par beaucoup d'ingénieurs et de scientifiques. On y remarque l'absence de touche égale `=`. Pour calculer une expression, il suffisait de taper les opérandes et les opérateurs dans l'ordre. La calculatrice se chargeait de calculer le résultat.

    ![HP-42s](../../assets/images/hp42s.jpg)

    La notation polonaise inverse est également très pratique pour les ordinateurs. En effet, il est plus facile de traiter une expression postfixée qu'une expression infixée. L'algorithme de Shunting Yard permet de transformer une expression infixée en une expression postfixée.

### Codage de Huffman

Le codage de Huffman est un algorithme de compression de données sans perte. Il a été inventé par

## Algorithmes de tris

### Heap Sort

L'algorithme [Heap Sort](https://fr.wikipedia.org/wiki/Tri_par_tas) aussi appelé "Tri par tas" est l'un des algorithmes de tri les plus performants offrant une complexité en temps de $O(n\cdot log(n))$ et une complexité en espace de $O(1)$. Il s'appuie sur le concept d'arbre binaire.

Prenons l'exemple du tableau ci-dessous et deux règles suivantes :

- l'enfant de gauche est donné par `2 * k + 1` ;
- l'enfant de droite est donné par `2 * k + 2`.

```text
  1   2       3                  4
┞──╀──┬──╀──┬──┬──┬──╀──┬──┬──┬──┬──┬──┬──┬──┦
│08│04│12│20│06│42│14│11│03│35│07│09│11│50│16│
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  (indice)
```

La première valeur du tableau est appelée la racine *root*. C'est le premier élément de l'arbre. Puisqu'il s'agit d'un arbre binaire, chaque nœud peut comporter jusqu'à 2 enfants. L'enfant de gauche est calculé à partir de l'indice `k` de l'élément courant. Ainsi les deux enfants de l'élément `4` seront `2 * 4 + 1 = 9` et `2 * 4 + 2 == a`.

Ce tableau linéaire en mémoire pourra être représenté visuellement comme un arbre binaire :

```text
             8
             |
         ----+----
       /           \
      4            12
   /    \        /    \
  20     6      42    14
 / \    / \    / \   /  \
11  3  35  7  9  11 50  16
```

Le cœur de cet algorithme est le sous-algorithme nommé *heapify*. Ce dernier à pour objectif de satisfaire une exigence supplémentaire de notre arbre : **chaque enfant doit être plus petit que son parent**. Le principe est donc simple. On part du dernier élément de l'arbre qui possède au moins un enfant : la valeur `14` (indice `6`). Le plus grand des enfants est échangé avec la valeur du parent. Ici `50` sera échangé avec `14`. Ensuite on applique récursivement ce même algorithme pour tous les enfants qui ont été échangés. Comme `14` (anciennement `50`) n'a pas d'enfant, on s'arrête là.

L'algorithme continue en remontant jusqu'à la racine de l'arbre. La valeur suivante analysée est donc `42`, comme les deux enfants sont petits on continue avec la valeur `6`. Cette fois-ci `35` qui est plus grand est alors échangé. Comme `6` n'a plus d'enfant, on continue avec `20`, puis `12`. À cette étape, notre arbre ressemble à ceci :

```text
             8
             |
         ----+----
       /           \
      4            12
   /    \        /    \
  20    35      42    50
 / \    / \    / \   /  \
11  3  6   7  9  11 14  16
```

La valeur `12` est plus petite que `50` et est donc échangée. Mais puisque `12` contient deux enfants (`14` et `16`), l'algorithme continue. `16` est échangé avec `12`. L'algorithme se poursuit avec `4` et se terminera avec la racine `8`. Finalement l'arbre ressemblera à ceci :

```text
            35
             |
         ----+----
       /           \
     20            50
   /    \        /    \
  11     7      42    16
 / \    / \    / \   /  \
8   3  6   4  9  11 14  12
```

On peut observer que chaque nœud de l'arbre satisfait à l'exigence susmentionnée : tous les enfants sont inférieurs à leurs parents.

Une fois que cette propriété est respectée, on a l'assurance que la racine de l'arbre est maintenant le plus grand élément du tableau. Il est alors échangé avec le dernier élément du tableau `12`, qui devient à son tour la racine.

Le dernier élément est sorti du tableau et notre arbre ressemble maintenant à ceci :

```text
1   2       3                  4
┞──╀──┬──╀──┬──┬──┬──╀──┬──┬──┬──┬──┬──┬──┦──┦
│12│20│50│11│ 7│42│16│ 8│ 3│ 6│ 4│ 9│11│14│35│
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
  0  1  2  3  4  5  6  7  8  9  a  b  c  d     (indice)

            12
             |
         ----+----
       /           \
     20            50
   /    \        /    \
  11     7      42    16
 / \    / \    / \   /
8   3  6   4  9  11 14
```

À ce moment on recommence :

1. `heapify`
2. Échange du premier élément avec le dernier.
3. Sortie du dernier élément de l'arbre.
4. Retour à (1) jusqu'à ce que tous les éléments soient sortis de l'arbre.

### Quick Sort

Le [tri rapide](https://fr.wikipedia.org/wiki/Tri_rapide) est l'algorithme de tri par référence dans la plupart des langage de programmation. Selon le compilateur C que vous utilisez, la fonction `qsort` implémente cette méthode de tri en $O(n log n)$.

Quick sort est théoriquement plus lent que le Heap sort avec dans le pire des cas en $O(n^2)$. Néanmoins, en s'appuyant que cette [réponse](https://stackoverflow.com/a/1853219/2612235) StackOverflow, quick sort reste meilleur pour de grands tableaux car les embranchements sont moins fréquents, et le cache processeur est donc mieux utilisé.

Cet algorithme utilise la notion de **pivot**. Le pivot est un élément qui est choisi pour être le point autour duquel sont agencé les éléments. La méthode de tri est la suivante :

1. Choix d'un pivot
2. Paritionnement : tous les éléments plus petit que le pivot sont déplacé à gauche et tous les éléments plus grands sont à droite. L'élément pivot est ainsi positionné à sa bonne place dans le tableau.
3. Appel récursif pour la partie gauche et droite.

Considérons le tableau suivant. Les valeurs ne sont pas triées. La première étape consiste à choisir un pivot. Il existe plusieurs technique :

- Choisir le premier élément comme pivot
- Choisir le dernier élément comme pivot
- Choisir l'élément médian comme pivot

Dans cet exemple, le dernier élément `6` sera arbitrairement choisi comme pivot.

![Représentation du tableau à trier avec son pivot.](../../assets/images/quicksort.drawio)

L'étape de paritionnement utilise l'algorithme suivant :

```c
int partition (int a[], int low, int high, int pivot)
{
    int i = low;
    for (int j = low; j < high; j++)
        if (a[j] < a[pivot])
            swap(&a[i++], &a[j]);
    swap(&a[i], &a[pivot]);
    return i;
}
```

Voici comment `partition(a, 0, 10, 10)` modifie le tableau (voir [code source](../../assets/src/partition.c)) :

```text
2 9 4 1 b 5 a 7 3 8 6
2 4 9 1 b 5 a 7 3 8 6
2 4 1 9 b 5 a 7 3 8 6
2 4 1 5 b 9 a 7 3 8 6
2 4 1 5 3 9 a 7 b 8 6
2 4 1 5 3 6 a 7 b 8 9
```

On constate que la valeur `6` choisie comme pivot est maintenant à sa bonne place. L'algorithme est donc appelé récursivement pour les éléments `0` à `4` et \`\` 6\`\`  à `a`.

![Tri rapide après le premier partitionnement.](../../assets/images/quicksort-2.drawio)

Voici une autre représentation (voir [code source](../../assets/src/quicksort.c)) :

```c
1  9  5  2  b  4  a  7  3  8 [6]
1  5  2  4  3 [6] a  7  b  8  9
1  5  2  4 [3]
1  2 [3] 4  5
1 [2]
1 [2]
        4 [5]
        4 [5]
                a  7  b  8 [9]
                7  8 [9] a  b
                7 [8]
                7 [8]
                        a [b]
                        a [b]
```

## Type d'algorithmes

### Algorithmes en ligne (incrémental)

Un algorithme incrémental ou [online](https://fr.wikipedia.org/wiki/Algorithme_online) est un algorithme qui peut s'exécuter sur un flux de données continu en entrée. C'est-à-dire qu'il est en mesure de prendre des décisions sans avoir besoin d'une visibilité complète sur le set de données.

Un exemple typique est le [problème de la secrétaire](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_secr%C3%A9taire). On souhaite recruter une nouvelle secrétaire et le recruteur voit défiler les candidats. Il doit décider à chaque entretien s'il engage ou non le candidat et ne peut pas attendre la fin du processus d'entretiens pour obtenir le score attribué à chaque candidat. Il ne peut comparer la performance de l'un qu'à celle de deux déjà entrevus. L'objectif est de trouver la meilleure stratégie.

La solution à ce problème est de laisser passer 37% des candidats sans les engager. Ceci correspond à une proportion de $1/e$. Ensuite il suffit d'attendre un ou une candidate meilleure que tous ceux/celles du premier échantillon.

## Exercices de révision

!!! exercise "Intégrateur de Kahan"

    L'intégrateur de Kahan (`Kahan summation algorithm <https://en.wikipedia.org/wiki/Kahan_summation_algorithm>`__) est une solution élégante pour pallier à la limite de résolution des types de données.

    L'algorithme pseudo-code peut être exprimé comme :

    ```text
    function kahan_sum(input)
        var sum = 0.0
        var c = 0.0
        for i = 1 to input.length do
            var y = input[i] - c
            var t = sum + y
            c = (t - sum) - y
            sum = t
        next i
        return sum
    ```

    1. Implémenter cet algorithme en C compte tenu du prototype :

        ```c
        float kahan_sum(float value, float sum, float c);
        ```

    2. Expliquer comment fonctionne cet algorithme.
    3. Donner un exemple montrant l'avantage de cet algorithme sur une simple somme.

!!! exercise "Robot aspirateur affamé"

    Un robot aspirateur souhaite se rassasier et cherche le frigo, le problème c'est qu'il ne sait pas où il est. Elle serait la stratégie de recherche du robot pour se rendre à la cuisine ?

    Le robot dispose de plusieurs fonctionnalités :

    - Avancer
    - Tourner à droite de 90°
    - Détection de sa position absolue p. ex. `P5`

    Élaborer un algorithme de recherche.

    ```text
        │ A │ B │ C │ D │ E │ F │ G │ H │ I │ J │ K │ L │ M │ O │ P │ Q │
    ──┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
    1 ┃                     x ┃       ┃               ┃               ┃
    ──┃             F1: Frigo ┃       ┃               ┃               ┃
    2 ┃       ┃               ┃       ┃               ┃               ┃
    ──┃       ┃               ┃       ┃               ┃               ┃
    3 ┃       ┃               ┃       ┃               ┃               ┃
    ──┃       ┃               ┃       ┃               ┃               ┃
    4 ┃       ┃               ┃       ┃               ┃               ┃
    ──┃       ┃               ┃       ┃               ┃               ┃
    5 ┃       ┃               ┃       ┃               ┃      <--o     ┃
    ──┃       ┣━━━━━━━   ━━━━━┫       ┃               ┃     P5: Robot ┃
    6 ┃       ┃               ┃       ┃               ┃               ┃
    ──┃       ┃               ┃       ┃               ┃               ┃
    7 ┃                       ┃       ┃               ┃               ┃
    ──┃                       ┃       ┃               ┃               ┃
    8 ┃       ┃               ┃       ┃               ┃               ┃
    ──┣━━━━━━━┻━━━━━━━    ━━━━┛   ━━━━┛   ━━━━━━━━━━━━┛   ━━━━┳━━━━━━━┫
    9 ┃                                                       ┃       ┃
    ──┃                                                       ┃       ┃
    10┃                                                               ┃
    ──┃                                                               ┃
    11┃                                                       ┃       ┃
    ──┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━┛
    ```
