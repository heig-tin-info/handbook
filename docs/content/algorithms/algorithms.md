[](){#algorithms-and-design}
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

![Différentes complexités d'algorithmes]({assets}/images/complexity.drawio)

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


## Algorithmes utilitaires

### Slurp

Souvent on a besoin de lire l'entrée standard en entier dans une chaîne de caractère. Il faut convertir le flux d'entrée en une chaîne de caractère. Cependant, comme l'entrée standard n'est pas *seekable*, il faut lire le flux caractère par caractère. Une implémentation possible se repose sur le concept des tableaux dynamiques.

```c title="slurp.h"
--8<-- "docs/assets/src/slurp/slurp.h"
```

```c title="slurp.c"
--8<-- "docs/assets/src/slurp/slurp.c"
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
