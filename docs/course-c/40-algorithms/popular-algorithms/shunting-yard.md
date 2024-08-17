# Algorithme de Shunting Yard

L'algorithme de [Shunting Yard](https://fr.wikipedia.org/wiki/Algorithme_de_Shunting-yard) est un algorithme de parsing d'expression mathématique. Il permet de transformer une expression mathématique en notation infixée en une expression postfixée. L'algorithme a été inventé par Edsger Dijkstra en 1961.

Imaginez que vous ayez une expression mathématique sous forme d'une chaîne de caractères :

```text
2 + 3 * 8 - 2 * ( 2 - 4 / ( 3 * 8 ) )
```

Comment calculer cette expression ? Si vous procédez de gauche à droite, vous allez rencontrer des parenthèses et des priorités d'opérations.

L'algorithme se compose de deux files d'attente (FIFO) et d'une pile (LIFO). La file d'attente de sortie contiendra l'expression postfixée. La pile contiendra les opérateurs.

![Algorithme de shunting yard](/assets/images/shunting-yard.drawio)

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
    --8<-- "docs/assets/src/shunting-yard/main.c"
    ```

=== "queue.h"

    ```c
    --8<-- "docs/assets/src/shunting-yard/queue.h"
    ```

=== "stack.h"

    ```c
    --8<-- "docs/assets/src/shunting-yard/stack.h"
    ```

=== "queue.c"

    ```c
    --8<-- "docs/assets/src/shunting-yard/queue.c"
    ```

=== "stack.c"

    ```c
    --8<-- "docs/assets/src/shunting-yard/stack.c"
    ```

!!! info "Notation polonaise inverse"

    La notation polonaise inverse (RPN) est une notation mathématique dans laquelle chaque opérateur suit ses opérandes. Par exemple, l'expression `3 + 4` s'écrira `3 4 +`. Cette notation a été inventée par le mathématicien polonais Jan Łukasiewicz.

    Elle a été longtemps utilisée par les calculatrices Hewlett-Packard et permet de s'affranchir des parenthèses. En effet, l'expression `3 + 4 * 5` s'écrira `3 4 5 * +`.

    La calculatrice mythique HP-42s apparue en 1988 était utilisée par beaucoup d'ingénieurs et de scientifiques. On y remarque l'absence de touche égale `=`. Pour calculer une expression, il suffisait de taper les opérandes et les opérateurs dans l'ordre. La calculatrice se chargeait de calculer le résultat.

    ![HP-42s](/assets/images/hp42s.jpg)

    La notation polonaise inverse est également très pratique pour les ordinateurs. En effet, il est plus facile de traiter une expression postfixée qu'une expression infixée. L'algorithme de Shunting Yard permet de transformer une expression infixée en une expression postfixée.
