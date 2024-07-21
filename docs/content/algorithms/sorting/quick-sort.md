# Quick Sort

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

![Représentation du tableau à trier avec son pivot.]({assets}/images/quicksort.drawio)

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

Voici comment `partition(a, 0, 10, 10)` modifie le tableau (voir [code source](../../../assets/src/partition.c)) :

```text
2 9 4 1 b 5 a 7 3 8 6
2 4 9 1 b 5 a 7 3 8 6
2 4 1 9 b 5 a 7 3 8 6
2 4 1 5 b 9 a 7 3 8 6
2 4 1 5 3 9 a 7 b 8 6
2 4 1 5 3 6 a 7 b 8 9
```

On constate que la valeur `6` choisie comme pivot est maintenant à sa bonne place. L'algorithme est donc appelé récursivement pour les éléments `0` à `4` et \`\` 6\`\`  à `a`.

![Tri rapide après le premier partitionnement.]({assets}/images/quicksort-2.drawio)

Voici une autre représentation (voir [code source](../../../assets/src/quicksort.c)) :

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
