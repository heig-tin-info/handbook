# Counting Sort

Le [tri par dénombrement](https://fr.wikipedia.org/wiki/Tri_comptage) est un algorithme de tri particulier. Il est utilisé pour trier des éléments dont la valeur est connue à l'avance. Il est donc inutile pour trier des éléments dont la valeur est inconnue ou aléatoire.

Nous l'avons vu précédemment, il n'est pas possible de trier un tableau mieux qu'en **O(n~log~n)**. En revanche cette assertion n'est pas tout à fait juste dans le cas ou les données brutes possèdent des propriétés remarquables.

Pour que cet algorithme soit utilisable, imaginons un contexte où les données d'entrées possèdent des propriétés remarquables.

Ici, les données d'entrées seront générées entre 0 et 51 ; chaque valeur représentera une carte à jouer selon la règle suivante :

![cards]({assets}/images/playing-cards.svg){ width=600px }

Cette série de valeurs dispose de plusieurs propriétés intéressantes :

1. La valeur d'une carte est identifiée par `n % 13`.
2. La couleur est identifiée par `n / 13`.
3. Il n'y a donc que **13** valeurs par couleur et **4** couleurs.
4. Bien qu'un entier soit stocké sur 4 bytes, il suffit en réalité de 6 bits pour encoder la valeur d'une carte.

L'algorithme `counting-sort` est intéressant, car il ne fait pas appel à des comparaisons de valeurs.

L'algorithme itératif est le suivant :

1. On crée un tableau statique de 13 positions correspondant au nombre de valeurs possibles dans notre set de donnée. Ce tableau peut être nommé `counts`
2. On parcourt le tableau à trier linéairement et on compte le nombre d'occurrences de chaque valeur dans `counts`. On aura donc à la position `0` le nombre d'as contenus dans le tableau à trier et à la positon `10` le nombre de valets dans le jeu de cartes fourni.
3. Une fois ces comptes terminés, une opération de somme cumulée est faite sur ce tableau (p.ex. le tableau `{1, 2, 2, 0, 8, 1}` sera sommé comme suit `{1, 3, 5, 5, 13, 14}`).
4. Le tableau à trier est parcouru linéairement de la fin vers le début et on copie la valeur à la bonne position dans le tableau des valeurs triées. Si votre tableau d'entrée non trié est nommé `a` et votre tableau de sortie trié `b` vous aurez pour chaque élément `i` : `b[c[a[i]--] - 1] = a[i]`

À l'issue de cet algorithme, vous aurez dans `b` un tableau trié par valeurs.

**Notez qu'ici les couleurs ne sont pas triées**.

Voici un exemple de tri sur des entiers entre 0 et 9 :

```text
1 0 9 3 8 1 4 8 7 5  Tableau d'entrée `a` non trié et contenant que des chiffres
                     Il y a 10 valeurs possibles par chiffre, donc le tableau
                     `counts` aura 10 positions:

1 2 0 1 1 1 0 1 2 1  Tableau `counts` calculé, il faut lire : une occurrence
                     de 0, deux occurrences de 2, zero occurrences de 3...

1 3 3 4 5 6 6 1 9 B  Somme cumulée (affiché en hexadécimal)

Pour trouver la position triée d'une valeur, par exemple le 3 :

1 0 9 3 8 1 4 8 7 5  a[i] == 3 (on part du tableau a)
      ↧
1 3 3 4 5 6 6 1 9 B  counts[a[i]] == 4 (on consulte la somme cumulée)
      ↧
_ _ _ 3 _ _ _ _ _ _  b[counts[a[i]]-- - 1] == 3 (on insert la valeur triée)

0 1 1 3 4 5 7 8 8 9  Et ainsi de suite jusqu'à tri complet du tableau
```

On constate en effet que `3` est à la bonne position dans `b` et qu'il y aura `0 1 1` devant.

Tel quel, cet algorithme ne permet pas de modifier directement le tableau d'origine puisqu'il ne fait pas intervenir de permutations (`swap`). Il requiert donc un buffer supplémentaire et donc à une complexité en espace de **O(n)**.

Concernant les cartes à jouer, voici un exemple de tri :

```text
41 23 00 15 26 39 13 02 28  Tableau d'entrée
00 26 39 13 41 15 02 28 23  Tableau trié
À♣ À♥ A♠ A♦ 3♠ 3♦ 3♣ 3♥ V♦  Valeurs interprétées des cartes
```

Un avantage de cet algorithme est qu'il est stable, c'est-à-dire que l'ordre des éléments égaux est conservé. Donc on peut ensuite retrier les cartes par couleur.
