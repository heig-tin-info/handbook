## Bibliothèques standard

Les bibliothèques standard ([C standard library](https://fr.wikipedia.org/wiki/Biblioth%C3%A8que_standard_du_C)) sont une collection normalisée d'en-têtes portables. C'est à dire que quelque soit le compilateur et l'architecture cible, cette collection sera accessible.

Le standard **C99** définit un certain nombre d'en-têtes dont les plus utilisés (et ceux utilisés dans ce cours) sont :

`<assert.h>`

: Contient la macro `assert` pour valider certains prérequis.

`<complex.h>`

: Pour manipuler les nombres complexes

`<float.h>`

: Contient les constantes qui définissent la précision des types flottants sur l'architecture cible. `float` et `double` n'ont pas besoin de cet en-tête pour être utilisés.

`<limits.h>`

: Contient les constantes qui définissent les limites des types entiers.

`<math.h>`

: Fonctions mathématiques `sin`, `cos`, ...

`<stdbool.h>`

: Défini le type booléen et les constantes `true` et `false`.

`<stddef.h>`

: Défini certaines macros comme `NULL`

`<stdint.h>`

: Défini les types standard d'entiers (`int32_t`, `int_fast64_t`, ...).

`<stdio.h>`

: Permet l'accès aux entrées sorties standard (`stdin`, `stdout`, `stderr`). Définis entre autres la fonction `printf`.

`<stdlib.h>`

: Permet l'allocation dynamique et défini `malloc`

`<string.h>`

: Manipulation des chaînes de caractères

`<time.h>`

: Accès au fonctions lecture et de conversion de date et d'heure.

!!! exercise "Arc-cosinus"

    La fonction Arc-Cosinus `acos` est-elle définie par le standard et dans quel fichier d'en-tête est-elle déclarée? Un fichier d'en-tête se termine avec l'extension `.h`.

    ??? solution

        En cherchant `man acos header` dans Google, on trouve que la fonction `acos` est définie dans le header `<math.h>`.

        Une autre solution est d'utiliser sous Linux la commande `apropos`:

        ```bash
        $ apropos acos
        acos (3)     - arc cosine function
        acosf (3)    - arc cosine function
        acosh (3)    - inverse hyperbolic cosine function
        acoshf (3)   - inverse hyperbolic cosine function
        acoshl (3)   - inverse hyperbolic cosine function
        acosl (3)    - arc cosine function
        cacos (3)    - complex arc cosine
        cacosf (3)   - complex arc cosine
        cacosh (3)   - complex arc hyperbolic cosine
        cacoshf (3)  - complex arc hyperbolic cosine
        cacoshl (3)  - complex arc hyperbolic cosine
        cacosl (3)   - complex arc cosine
        ```

        Le premier résultat permet ensuite de voir :

        ```bash
        $ man acos | head -10
        ACOS(3)    Linux Programmer's Manual         ACOS(3)

        NAME
            acos, acosf, acosl - arc cosine function

        SYNOPSIS
            #include <math.h>

            double acos(double x);
            float acosf(float x);
        ```

        La réponse est donc `<math.h>`.

        Sous Windows avec Visual Studio, il suffit d'écrire `acos` dans un fichier source et d'appuyer sur `F1`. L'IDE redirige l'utilisateur sur l'aide Microsoft [acos-acosf-acosl](https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/acos-acosf-acosl) qui indique que le header source est `<math.h>`.

!!! exercise "Date"

    Lors du formatage d'une date, on y peut y lire `%w`, par quoi sera remplacé ce *token* ?

### Fonctions d'intérêt

Il serait inutile ici de lister toutes les fonctions, les bibliothèques standard étant largement documentées sur internet. Il ne fait aucun doute que le développeur sera trouver comment calculer un sinus avec la fonction `sin`. Néanmoins l'existence de certaines fonctions peut passer inaperçues et c'est de celles-ci don't j'aimerais parler.

#### Math

Table: Constantes mathématiques

| Constantes  | Description                  |
| ----------- | ---------------------------- |
| `M_PI`      | Valeur de :math:`\pi`        |
| `M_E`       | Valeur de :math:`e`          |
| `M_SQRT1_2` | Valeur de :math:`1/\sqrt(2)` |

Table: Fonctions mathématiques

| Fonction     | Description                                     |
| ------------ | ----------------------------------------------- |
| `exp(x)`     | Exponentielle :math:`e^x`                       |
| `ldexp(x,n)` | Exposant d'un nombre flottant :math:`x\cdot2^n` |
| `log(x)`     | Logarithme binaire :math:`\log_{2}(x)`          |
| `log10(x)`   | Logarithme décimal :math:`\log_{10}(x)`         |
| `pow(x,y)`   | Puissance :math:`x^y`                           |
| `sqrt(x)`    | Racine carrée :math:`\sqrt(x)`                  |
| `cbrt(x)`    | Racine cubique :math:`\sqrt[3](x)`              |
| `hypot(x,y)` | Hypoténuse optimisé :math:`\sqrt(x^2 + y^2)`    |
| `ceil`       | Arrondi à l'entier supérieur                    |
| `floor`      | Arrondi à l'entier inférieur                    |

Notons par exemple que la fonction `hypot` peut très bien être émulée facilement en utilisant la fonction `sqrt`. Néanmoins elle existe pour deux raisons élémentaires :

1. Éviter les dépassements (*overflow*).
2. Une meilleure optimisation du code.

Souvent, les processeurs sont équipés de coprocesseurs arithmétiques capables de calculer certaines fonctions plus rapidement.

#### Chaînes de caractères

`strcopy(dst, src)`

: Identique à `memcpy` mais sans nécessité de donner
  la taille de la chaîne puisqu'elle se termine par `\0`

`memmove(dst, src, n)`

: Identique à `memcpy` mais traite les cas particuliers lorsque
  les deux régions mémoire se superposent.

#### Types de données

Test d'une propriété d'un caractère passé en paramètre

Table: Fonctions de test de caractères

| Fonction     | Description                            |
| ------------ | -------------------------------------- |
| `isalnum`  | une lettre ou un chiffre               |
| `isalpha`  | une lettre                             |
| `iscntrl`  | un caractère de commande               |
| `isdigit`  | un chiffre décimal                     |
| `isgraph`  | un caractère imprimable ou le blanc    |
| `islower`  | une lettre minuscule                   |
| `isprint`  | un caractère imprimable (pas le blanc) |
| `ispunct`  | un caractère imprimable pas isalnum    |
| `isspace`  | un caractère d'espace blanc            |
| `isupper`  | une lettre majuscule                   |
| `isxdigit` | un chiffre hexadécimal                 |

#### Limites

Table: Valeurs limites pour les entiers signés et non signés

| Constante       | Valeur        |
| --------------- | ------------- |
| `SCHAR_MIN`   | -128          |
| `SCHAR_MAX`   | +127          |
| `CHAR_MIN`    | 0             |
| `CHAR_MAX`    | 255           |
| `SHRT_MIN`    | -32768        |
| `SHRT_MAX`    | +32767        |
| `USHRT_MAX`   | 65535         |
| `LONG_MIN`    | -2147483648   |
| `LONG_MAX`    | +2147483647   |
| `ULONG_MAX`   | +4294967295   |
| `DBL_MAX`     | 1E+37 ou plus |
| `DBL_EPSILON` | 1E-9 ou moins |
