# Algorithmes utilitaires

## Slurp

Souvent on a besoin de lire l'entrée standard en entier dans une chaîne de caractère. Il faut convertir le flux d'entrée en une chaîne de caractère. Cependant, comme l'entrée standard n'est pas *seekable*, il faut lire le flux caractère par caractère. Une implémentation possible se repose sur le concept des tableaux dynamiques.

```c title="slurp.h"
--8<-- "docs/assets/src/slurp/slurp.h"
```

```c title="slurp.c"
--8<-- "docs/assets/src/slurp/slurp.c"
```

## Split

## Join

## Trim

## Reverse

## Gestion des arguments
