# Algorithme de Rabin-Karp

Cet algorithme [Rabin-Karp](https://fr.wikipedia.org/wiki/Algorithme_de_Rabin-Karp) permet la recherche d'une sous-chaîne de caractère dans une chaîne plus grande. Sa complexité moyenne est $O(n + m)$.

L'algorithme se base sur le principe de la [fonction de hachage](https://fr.wikipedia.org/wiki/Fonction_de_hachage). Il consiste à calculer le hash de la chaîne à rechercher et de la chaîne dans laquelle on recherche. Si les deux hash sont égales, on compare les deux chaînes caractère par caractère.

L'algorithme fait glisser une fenêtre de la taille de la chaîne à rechercher sur la chaîne dans laquelle on recherche. À chaque itération, on calcule le hash de la fenêtre et on le compare au hash de la chaîne à rechercher. Si les deux hash sont égaux, on compare les deux chaînes caractère par caractère.

La performance de l'algorithme dépend de la fonction de hachage. Si la fonction de hachage est bien choisie, l'algorithme est très performant. Si la fonction de hachage est mal choisie, l'algorithme peut être lent.

Ici la fonction de hachage est très simple, on utilise un nombre premier.

```c title="rabin-karp.c"
--8<-- "docs/assets/src/rabin-karp.c"
```
