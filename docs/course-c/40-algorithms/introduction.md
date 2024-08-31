---
epigraph:
  text: ... conduire par ordre mes pensées, en commençant par les objets les plus simples et les plus aisés à connaître, pour monter peu à peu, comme par degrés, jusques à la connaissance des plus composés; et supposant même de l'ordre entre ceux qui ne se précèdent point naturellement les uns les autres.
  source: René Descartes, Discours de la méthode
---

[](){#algorithmsanddesign}

# Introduction

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

## Complexité Algorithmique

Il est souvent utile de savoir quelle est la performance d'un algorithme afin de le comparer à un autre algorithme équivalent. On peut s'intéresser à deux indicateurs :

- **La complexité en temps** : combien de temps CPU consomme un algorithme pour s'exécuter.
- **La complexité en mémoire** : combien de mémoire tampon consomme un algorithme pour s'exécuter.

Bien évidemment, la complexité d'un algorithme dépend des données en entrée. Par exemple si on vous donne à corriger un examen de 100 copies, et le protocol de correction associé, votre temps de travail dépendra du nombre de copies à corriger, je sais de quoi je parle...

La complexité en temps et en mémoire d'un algorithme est souvent exprimée en utilisant la notation en O (*Big O notation*). Cette notation a été introduite par le mathématicien et informaticien allemand Paul Bachmann en 1984 dans son ouvrage *Analytische Zahlentheorie*. Cependant, c'est le mathématicien austro-hongrois Edmund Landau qui a popularisé cette notation dans le contexte de la théorie des nombres.

En substance, la complexité en temps d'un algorithme qui demanderait 10 étapes pour être résolu s'écrirait :

$$
O(10)
$$

Un algorithme qui ferait une recherche dichotomique sur un tableau de $n$ éléments à une complexité $O(log(n))$. La recherche dichotomique c'est comme chercher un mot dans un dictionnaire. Vous ouvrez le dictionnaire à la moitié, si le mot est avant, vous répétez l'opération sur la première moitié, sinon sur la seconde. Vous répétez l'opération jusqu'à trouver le mot. À chaque étape vous éliminez la moitié restante des mots du dictionnaire. Si le dictionnaire contient 100'000 mots, vous aurez trouvé le mot en un nombre d'étapes équivalent à :

$$
\log_2(100'000) = 16.6
$$

C'est bien plus rapide que de parcourir le dictionnaire de manière linéaire, en tournant les pages une à une.

Prenons un algoritme qui prend un certain temps pour s'exécuter. L'algorithme $A$ prend $f(n)$ unités de temps pour une entrée de taille $n$. On peut dire que $A$ est en $O(g(n))$ si $f(n) \leq c \cdot g(n)$ pour tout $n \geq n_0$, où $c$ est une constante et $n_0$ est un entier.

On pourrait faire le raccourcis que la complexité algorithmique mesure le nombre d'opérations élémentaires nécessaires pour résoudre un problème. Cepender, la complexité algorithmique ne mesure ni le temps en secondes ni le nombre d'opérations élémentaires. Elle mesure la croissance du nombre d'opérations élémentaires en fonction de la taille de l'entrée. C'est très différent. Prenons l'exemple suivant :

```c
for (int i, i < n, i++) {
    printf("%d ", a[i]);
}

for (int i, i < m, i++) {
    printf("%d ", b[i]);
}
```

On itère sur deux tableaux `a` et `b` respectivement de taille `n` et `m`. La complexité de cet algorithme est $O(n + m)$. Maintenant considérons l'exemple suivant :

```c
for (int i, i < n, i++) {
    for (int j, j < m, j++) {
        printf("%d ", a[i] + b[j]);
    }
}
```

Cette fois-ci on observe une imbrication de deux boucles `for`. La complexité de cet algorithme est $O(n \cdot m)$. On peut dire que la complexité de cet algorithme est quadratique.

Enfin, imaginons que nous devons appliquer 10 opérations sur chaque élément avant l'affichage:

```c
for (int i, i < n, i++) {
    for (int j, j < m, j++) {
        for (int k, k < 10, k++) {
            printf("%d ", a[i] + b[j]);
        }
    }
}
```

Naïvement on pourrait penser que la complexité de cet algorithme est $O(10 \cdot n \cdot m) = O(n \cdot m)$. Cependant, la complexité de cet algorithme est $O(10 \cdot n \cdot m) = O(n \cdot m)$. En effet, la constante 10 n'a pas d'impact sur la croissance de la complexité de l'algorithme. On peut dire que la complexité de cet algorithme est quadratique.

### Suppression des constantes

Dans la notation Big O, les constantes sont ignorées. Par exemple, si un algorithme prend $5n^2 + 3n + 2$ unités de temps pour une entrée de taille $n$, on dira que cet algorithme est en $O(n^2)$. En effet, pour de grandes valeurs de $n$, la croissance de $5n^2 + 3n + 2$ est dominée par $n^2$.

Table: Suppression des constantes

| Complexité         | Complexité sans les constantes |
| ------------------ | ------------------------------ |
| $O(5n^2)$          | $O(n^2)$                       |
| $O(3n)$            | $O(n)$                         |
| $O(2)$             | $O(1)$                         |
| $O(n^2 + n)$       | $O(n^2)$                       |
| $O(5n^2 + 3n + 2)$ | $O(n^2)$                       |
| $O(n + \log(n))$   | $O(n)$                         |

Cette règle est valable our l'addition, mais pour la multiplication, les constantes ne sont pas ignorées. Dans le cas de $O(n\cdot\log(n))$ la valeur de $\log(n)$ est importante.

### Indicateurs de Landau

Il existe différents indicateurs de Landau :

**Notation Big O (O)**

: Utilisée pour décrire une borne supérieure asymptotique. Cela signifie qu'une fonction \( f(n) \) est en \( O(g(n)) \) s'il existe des constantes \( c > 0 \) et \( n_0 \) telles que \( f(n) \leq c \cdot g(n) \) pour tout \( n \geq n_0 \). En d'autres termes, \( g(n) \) est une limite supérieure sur le comportement de \( f(n) \) pour de grandes valeurs de \( n \).

: Big O est souvent utilisée pour décrire le pire cas.

**Notation Big Omega (Ω)**

: Utilisée pour décrire une borne inférieure asymptotique. Cela signifie qu'une fonction \( f(n) \) est en \( \Omega(g(n)) \) s'il existe des constantes \( c > 0 \) et \( n_0 \) telles que \( f(n) \geq c \cdot g(n) \) pour tout \( n \geq n_0 \). En d'autres termes, \( g(n) \) est une limite inférieure sur le comportement de \( f(n) \) pour de grandes valeurs de \( n \).

: Big Omega est souvent utilisée pour décrire le meilleur cas.

**Notation Big Theta (Θ)**

: Utilisée pour décrire une borne asymptotique stricte. Cela signifie qu'une fonction \( f(n) \) est en \( \Theta(g(n)) \) s'il existe des constantes \( c_1, c_2 > 0 \) et \( n_0 \) telles que \( c_1 \cdot g(n) \leq f(n) \leq c_2 \cdot g(n) \) pour tout \( n \geq n_0 \). En d'autres termes, \( g(n) \) est une approximation asymptotique exacte de \( f(n) \).

: Big Theta est utilisée pour décrire un comportement asymptotique précis, souvent interprété comme le cas moyen.

!!! exercise "Quelle Complexité ?"

    Quelle est la complexité en temps de cet algorithme ?
    ```c
    void foo(int a[], int n) {
        int sum = 0, product = 1;
        for (int i = 0; i < n; i++) {
            sum += a[i];
        }
        for (int i = 0; i < n; i++) {
            product *= a[i];
        }
        printf("Sum: %d, Product: %d\n", sum, product);
    }
    ```

    - [ ] $O(2n)$
    - [x] $O(n)$
    - [ ] $O(n^2)$
    - [ ] $O(n \log(n))$

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

![Différentes complexités d'algorithmes](/assets/images/complexity.drawio)

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

## Diagrammes visuels

- Diagrammes en flux
- Structogrammes
- Diagramme d'activités
- Machines d'états ([UML state machine](https://en.wikipedia.org/wiki/UML_state_machine))
- [BPMN](https://en.wikipedia.org/wiki/Business_Process_Model_and_Notation) (*Business Process Model and Notation*)


## Type d'algorithmes

### Algorithmes en ligne (incrémental)

Un algorithme incrémental ou [online](https://fr.wikipedia.org/wiki/Algorithme_online) est un algorithme qui peut s'exécuter sur un flux de données continu en entrée. C'est-à-dire qu'il est en mesure de prendre des décisions sans avoir besoin d'une visibilité complète sur le set de données.

Un exemple typique est le [problème de la secrétaire](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_secr%C3%A9taire). On souhaite recruter une nouvelle secrétaire et le recruteur voit défiler les candidats. Il doit décider à chaque entretien s'il engage ou non le candidat et ne peut pas attendre la fin du processus d'entretiens pour obtenir le score attribué à chaque candidat. Il ne peut comparer la performance de l'un qu'à celle de deux déjà entrevus. L'objectif est de trouver la meilleure stratégie.

La solution à ce problème est de laisser passer 37% des candidats sans les engager. Ceci correspond à une proportion de $1/e$. Ensuite il suffit d'attendre un ou une candidate meilleure que tous ceux/celles du premier échantillon.

## Méthodes de résolution

Il existe deux méthodes quasiment infaillibles pour résoudre un problème complexe :

1. La réduction du problème en sous-problèmes plus simples.
2. Le raisonnement par l'inverse.

La rédiction aussi appelée [Divide and Conquer](https://fr.wikipedia.org/wiki/Diviser_pour_r%C3%A9gner) consiste à diviser un problème en sous-problèmes plus simples, les résoudre et combiner les solutions pour obtenir la solution du problème initial. C'est une méthode très utilisée en informatique pour résoudre des problèmes complexes. Par exemple, le tri fusion, le tri rapide, la recherche dichotomique sont des méthodes de résolution de problèmes basées sur la réduction.

Le raisonnement par l'inverse consiste à partir de la solution pour remonter au problème en posant des hypothèses. Par exemple, si vous avez un problème de recherche de chemin, vous pouvez partir de la destination pour remonter au point de départ. C'est une méthode très utilisée en mathématiques pour résoudre des problèmes complexes. Par exemple, la méthode de Newton pour trouver les racines d'une fonction est basée sur le raisonnement par l'inverse.

## Les Problèmes NP et NP-Complet

La théorie de la complexité computationnelle est une branche fascinante de l'informatique théorique qui s'intéresse à la classification des problèmes en fonction de la difficulté à les résoudre. Au cœur de cette théorie se trouvent les classes de problèmes NP et NP-complet, concepts essentiels pour comprendre pourquoi certains problèmes sont si difficiles à résoudre. Pour les néophytes, ces termes peuvent sembler abstraits, mais leur compréhension révèle des enjeux fondamentaux pour la science et l'ingénierie modernes.

### Qu'est-ce qu'un problème NP ?

Pour saisir ce qu'est un problème NP, il faut d'abord comprendre la notion de temps de calcul. Le temps de calcul d'un algorithme correspond au nombre d'étapes nécessaires pour résoudre un problème, en fonction de la taille de l'entrée. Par exemple, trier une liste de mille éléments prend généralement plus de temps que trier une liste de dix éléments.

Un problème est dit "en P" (pour "Polynomial") si une solution peut être trouvée par un algorithme en un temps raisonnable, c'est-à-dire en un temps qui croît de manière polynomiale avec la taille de l'entrée. Par exemple, l'algorithme qui permet de trier une liste en utilisant un tri par insertion appartient à la classe P car son temps de calcul est proportionnel au carré de la taille de la liste.

Cependant, certains problèmes semblent beaucoup plus complexes à résoudre. Un problème est dit "en NP" (pour "Nondeterministic Polynomial time") si, bien qu'il puisse être difficile de trouver une solution, il est relativement facile de vérifier la validité d'une solution donnée. Autrement dit, si on vous fournit une solution supposée correcte à un problème en NP, vous pouvez vérifier cette solution en temps polynomial. Le terme "nondeterministic" fait référence à l'idée théorique d'une machine qui pourrait essayer simultanément toutes les solutions possibles et choisir la bonne.

Un exemple classique de problème en NP est le problème du *Knapsack* (ou problème du sac à dos). Ce problème consiste à déterminer quels objets, parmi une collection donnée, doivent être placés dans un sac à dos de capacité limitée de manière à maximiser la valeur totale des objets. Trouver la meilleure combinaison d'objets à mettre dans le sac peut être très difficile car le nombre de combinaisons possibles croît de manière exponentielle avec le nombre d'objets. En revanche, si quelqu'un vous donne une combinaison prétendument optimale, vous pouvez rapidement vérifier si elle respecte la capacité du sac et si sa valeur est maximale.

### Les Problèmes NP-Complet

Parmi les problèmes en NP, certains sont particulièrement redoutables : ce sont les problèmes NP-complet. Un problème est dit NP-complet s'il est à la fois en NP et au moins aussi difficile que tous les autres problèmes en NP. En d'autres termes, si vous pouviez trouver une méthode efficace pour résoudre un problème NP-complet, alors vous pourriez utiliser cette méthode pour résoudre tous les autres problèmes en NP.

Le problème du *Knapsack* que nous avons mentionné plus tôt est un exemple de problème NP-complet. D'autres exemples bien connus incluent le problème du voyageur de commerce (TSP), où il s'agit de trouver le chemin le plus court pour visiter un ensemble de villes une fois et revenir au point de départ, ou encore le problème de la coloration de graphe, qui consiste à déterminer le nombre minimum de couleurs nécessaires pour colorier les sommets d'un graphe de manière que deux sommets adjacents n'aient pas la même couleur.

### Le Problème P = NP

Le problème millénaire P = NP, formulé par Stephen Cook en 1971, est l'une des questions les plus célèbres et les plus importantes de la science informatique. Il se demande si tous les problèmes qui peuvent être vérifiés rapidement (c'est-à-dire en temps polynomial) peuvent également être résolus rapidement. En d'autres termes, P est-il égal à NP ?

Si P = NP, cela signifierait qu'il existe un algorithme rapide pour résoudre chaque problème dont la solution peut être rapidement vérifiée. Cela bouleverserait notre compréhension de la complexité computationnelle et aurait des implications énormes dans de nombreux domaines, de la cryptographie à la logistique. À ce jour, personne n'a réussi à prouver ou à réfuter cette conjecture, et elle reste l'un des grands mystères non résolus de la science.

### Pourquoi les Problèmes NP-Complet sont-ils Importants ?

Les problèmes NP-complet sont essentiels car ils nous montrent les limites de ce que nous pouvons résoudre efficacement avec des ordinateurs. Ils nous forcent à accepter qu'il existe des problèmes pour lesquels, en l'état actuel de nos connaissances, il n'existe pas de solution rapide, ce qui a des conséquences pratiques. Par exemple, en cryptographie, la sécurité des systèmes repose souvent sur l'hypothèse que certains problèmes sont difficiles à résoudre, ce qui les rend résistants aux attaques.

En outre, comprendre ces problèmes nous pousse à développer de nouvelles techniques pour les résoudre ou les contourner. Parfois, cela signifie trouver des algorithmes approximatifs, qui fournissent des solutions proches de l'optimum en un temps raisonnable. D'autres fois, cela peut conduire à l'innovation en matière de matériel informatique, comme l'exploration des ordinateurs quantiques, qui pourraient potentiellement résoudre certains de ces problèmes beaucoup plus rapidement que les ordinateurs classiques.

### Conclusion

La classification des problèmes en P, NP, et NP-complet est une pierre angulaire de l'informatique théorique. Les problèmes NP-complet, en particulier, représentent certains des défis les plus redoutables auxquels nous sommes confrontés dans le domaine. Ils ne sont pas seulement des énigmes abstraites pour les théoriciens ; ils ont des implications profondes et très concrètes pour la science, la technologie, et même notre vie quotidienne. Comprendre ces concepts, c'est plonger au cœur de ce que signifie la complexité et la difficulté dans le monde des algorithmes, et reconnaître les limites actuelles de ce que nous pouvons accomplir avec des machines de calcul.

## Exercices de révision

!!! exercise "Intégrateur de Kahan"

    L'intégrateur de Kahan ([Kahan summation algorithm](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)) est une solution élégante pour pallier à la limite de résolution des types de données.

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
