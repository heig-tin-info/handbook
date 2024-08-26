# Le côté obscure

## Shadowy escape


!!! exercise "Shadowy escape"

    Que retourne la fonction `f` ?

    ```c
    #include <stdio.h>

    int x = 42;
    int f() {
        int x = 23;
        {
            extern int x;
            return x;
        }
    }

    - [x] 42
    - [ ] 23
    - [ ] 0
    - [ ] 1

!!! exercise "Curieux entier"

    Que vaut `x`

    ```c
    int32_t x = '0123';
    ```

    - [ ] Erreur de compilation
    - [ ] 123
    - [x] 0x30313233
    - [ ] 4817243
    - [x] Warning `multi-character character constant`

!!! exercise "Vilains crochets"

    Que vaut `x`

    ```c
    char x = "hello"[4];
    ```

    - [ ] Erreur de compilation
    - [x] 'o'
    - [ ] 'h'
    - [ ] 0

!!! exercise "La règle gourmande"

    Que vaut `x`

    ```c
    int x = 0;
    x = x+++x++;
    ```

    - [ ] 0
    - [x] 1
    - [ ] 2
    - [ ] 3

    ??? solution

        L'expression `x+++x++` est équivalente à `x++ + x++`. L'opérateur `++` est associatif à droite, donc `x++` est évalué en premier, puis `x++` est évalué. `x` est incrémenté deux fois, donc `x` vaut 2. On parle de *greedy lexer rule*. Le parseur est gourmand et prend le plus grand nombre de caractères possible pour former un jeton.

        Cela ne fonctionne pas à tous les coups. L'expression `x+++++y` est invalide car l'opérateur `++` ne peut pas être suivi d'un autre opérateur `++`. Il est nécessaire dans ce cas de séparer les opérateurs par des espaces pour que le code soit valide: `x+++ ++y`.

!!! exercise "Collision globale"

    Qu'affiche le programme ?

    ```c title="a.c"
    int x = 42;
    ```

    ```c title="b.c"
    int x;
    {
        printf("%d\n", x);
    }
    ```

    ```bash
    $ gcc a.c b.c && ./a.out
    ```

    - [x] 42
    - [ ] 0
    - [ ] Indéfini
    - [ ] Erreur de compilation