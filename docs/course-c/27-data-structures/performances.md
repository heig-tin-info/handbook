# Performances

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
