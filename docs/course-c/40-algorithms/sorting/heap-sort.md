# Heap Sort

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
