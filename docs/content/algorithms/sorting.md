# Algorithmes de tris


## Heap Sort

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

## Quick Sort

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

## Counting Sort

Le [tri par dénombrement](https://fr.wikipedia.org/wiki/Tri_comptage) est un algorithme de tri particulier. Il est utilisé pour trier des éléments dont la valeur est connue à l'avance. Il est donc inutile pour trier des éléments dont la valeur est inconnue ou aléatoire.

## Stabilité

## Comparaison des performances
