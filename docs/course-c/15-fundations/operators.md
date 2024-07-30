# Opérateurs

En programmation, un opérateur est une **fonction** qui effectue une opération. sur des valeurs. Les opérateurs utilisent des identificateurs spécifiques propres à chaque langage de programmation, ce qui permet de simplifier l'écriture des expressions. Par exemple, l'opérateur d'addition `+` permet d'additionner deux valeurs.

L'unité de calcul arithmétique du processeur est responsable d'effectuer les opérations fondamentales. Un ordinateur à 2 GHz pourrait par exemple effectuer plus de 2'000'000'000 opérations par seconde.

Un **opérateur** prend habituellement deux opérandes et retourne un résultat. On dit alors que cette classe d'opérateurs a une [arité](https://fr.wikipedia.org/wiki/Arit%C3%A9) de 2. Il existe également des opérateurs à arité de 1, aussi appelés opérateurs [unaires](https://fr.wikipedia.org/wiki/Op%C3%A9ration_unaire) comme pour obtenir l'opposé d'un nombre ($-x$). Connaissant le complément à deux, on sait que pour obtenir l'opposé d'un nombre, il suffit d'inverser tous les bits et d'ajouter 1. C'est-à-dire de faire l'opération de négation `~` puis de faire une addition `+1`.

Un opérateur possède plusieurs propriétés :

Une **priorité**

: La multiplication `*` est plus prioritaire que l'addition `+`

Une **associativité**

: L'opérateur d'affectation `=` possède une associativité à droite, c'est-à-dire que l'opérande à droite de l'opérateur sera évalué en premier

Un **point de séquence**

: Certains opérateurs comme `&&`, `||`, `?` ou `,` possèdent un point de séquence garantissant que l'exécution séquentielle du programme sera respectée avant et après ce point. Par exemple si dans l'expression `i < 12 && j > 2` la valeur de `i` est plus grande que 12, le test `j > 2` ne sera jamais effectué. L'opérateur `&&` garantit l'ordre des choses, ce qui n'est pas le cas avec l'affectation `=`.

## ALU (Arithmetic Logic Unit)

Dans un ordinateur, ou sur un microcontrôleur, c'est l'unité de calcul arithmétique [ALU](https://fr.wikipedia.org/wiki/Unit%C3%A9_arithm%C3%A9tique_et_logique) qui est en charge d'effectuer les opérations fondamentales. Cette unité de calcul est consensuellement représentée comme illustrée à la figure suivante :

![ALU]({assets}/images/alu.drawio)

L'unité de calcul arithmétique (**ALU**) représentée est composée de deux entrées `A` et `B`, d'une sortie `C` et d'un mode opératoire `O`. Sur de petites architectures matérielles, l'ALU peut être limité aux opérations d'addition `+`, d'inversion bit à bit `~`, de décalage vers la gauche `<<` et vers la droite `>>` et de l'opération bit à bit logique `&` pour la conjonction ainsi que `|` pour la disjonction.

Si l'on souhaite faire une addition, on peut écrire en C :

```c
c = a + b;
```

[](){#operator-arithmetic}

### Types d'opérateurs

Le langage C définit un certain nombre d'opérateurs qui peuvent être classés en plusieurs catégories :

- Les opérateurs arithmétiques
- Les opérateurs relationnels
- Les opérateurs logiques
- Les opérateurs bit à bit
- Les opérateurs d'affectation
- Les opérateurs de pointeurs
- Les opérateurs de taille
- Les opérateurs de séquence
- Les opérateurs de pré/post-incrémentation
- Les opérateurs de condition

Nous allons tous les voir un par un ; ce chapitre est long...

### Opérateurs arithmétiques

Aux 4 opérations de base (+, -, ×, ÷) le C ajoute l'opération [modulo](<https://fr.wikipedia.org/wiki/Modulo_(op%C3%A9ration)>), qui est le reste d'une division entière.

Table: Opérateurs arithmétiques

| Opérateur | Abréviation | Description    | Assertion vraie  |
| --------- | ------------ | -------------- | ---------------- |
| `+`     | *add*        | Addition       | `5 == 2 + 3`   |
| `-`     | *sub*        | Soustraction   | `8 == 12 - 4`  |
| `*`     | *mul*        | Multiplication | `42 == 21 * 2` |
| `/`     | *div*        | Division       | `2 == 5 / 2`   |
| `%`     | *mod*        | Modulo         | `13 % 4 == 1`  |

Lors d'opérations il faut faire attention aux types des variables impliquées. La division `5 / 2` donnera `2` et non, `2.5` car les deux valeurs fournies sont entières et le résultat est donc un entier. Pour obtenir un résultat flottant, il faut que l'une des valeurs soit un flottant, ici le `5` est exprimé en `double`, la propagation de type fera que le résultat sera aussi un `double` :

```c
int a = 5 / 2;      // 2
double b = 5.0 / 2; // 2.5
```

Le modulo (*mod*, `%`) est le reste de la division entière. L'assertion suivante est donc vraie, car 13 divisé par 4 égal 3 et il reste 1 :

```c
assert(13 % 4 == 1)
```

$$
\begin{array}{rr|l}
  1 & 3 & 4 \\
\hline
 - & 8   & \textbf{2} \\
  & \textbf{5}   & \\
  & &
\end{array}
$$

Il est important de noter aussi que les opérateurs arithmétiques sont tributaires des types sur lesquels ils s'appliquent. Par exemple, l'addition de deux entiers 8 bits `120 + 120` ne fera pas, `240` car le type ne permet pas de stocker des valeurs plus grandes que `127` :

```c
int8_t too_small = 120 + 120;
assert(too_small != 120 + 120);
```

Nous l'avons tous appris dans les petites écoles, les opérations arithmétiques s'effectuent de **droite à gauche** et **chiffre à chiffre**.
Lorsque le résultat de l'opération dépasse la capacité d'un chiffre, on retient une unité et on la reporte à la colonne suivante. L'addition de $123$ et $89$ en base $10$ donne $212$.

$$
\begin{array}{lrrr}
\phantom{1}& _1 & _1 &  \\
           & 1           & 2 & 3_{~10} \\
         + & \phantom{0} & 8 & 9_{~10} \\
\hline
           &           2 & 1 & 2_{~10} \\
\end{array}
$$

L'exemple reste valable quelque soit la base, en binaire par exemple, on commence par additionner les bits de poids faible et on reporte les retenues. Ainsi en premier lieu on aura $1_2 + 1_2 = 10_2$. Donc le résultat est $0$ et la retenue (*carry*) est $1$ :

$$
\begin{array}{lrrrrrrrr}
  & _1 & _1 & _1 & _1 &  & _1 & _1 &  \\
    & & 1 & 1 & 1 & 1 & 0 & 1 & 1_{~2} \\
 +  & & 1 & 0 & 1 & 1 & 0 & 0 & 1_{~2} \\
\hline
  &1 & 1 & 0 & 1 & 0 & 1 & 0 & 0_{~2} \\
\end{array}
$$

En algèbre de Boole, l'addition de deux chiffres n'a que $2^2 = 4$ cas de figure (contre $10^2=100$ en base $10$).

L'addition de deux bits $A$ et $B$ est donnée par la table suivante où `C` est la retenue engendrée par l'addition :

Table: Addition binaire

|   A   | B  @rb | A + B @rb | C @bb |
| :---: | :----: | :-------: | :---: |
|   0   |   0    |     0     |   0   |
|   0   |   1    |     1     |   0   |
|   1   |   0    |     1     |   0   |
|   1   |   1    |     0     |   1   |

!!! tip "Le cas de la soustraction"

    La soustraction reste une addition mais elle s'effectue sur les nombres représentés en complément à deux. On pourrait s'amuser à soustraire deux nombres en base $10$ en les représentant en complément à neuf plus 1. Par exemple, pour soustraire $23$ de $12$ il faut représenter $12$ en complément à neuf plus un.

    La méthode est la même, on effectue le complément à $9$ de $12$, soit $87$ et on ajoute $1$ pour obtenir $88$. Ensuite on peut faire l'addition en éliminant le chiffre supplémentaire qui dépasse :

    $$
    \begin{array}{lrrr}
    & _1 & _1 &  \\
    & 0 & 2 & 3_{~10} \\
    +  & 0 & 8 & 8_{~10} \\
    \hline
    & 1 & 1 & 1_{~10} \\
    \end{array}
    $$

    L'intérêt de cette méthode c'est qu'il s'agisse d'une addition ou d'une soustraction, c'est la même opération calculée par l'unité arithmétique et logique.

!!! exercise "Additions binaires"

    Une unité de calcul arithmétique (ALU) est capable d'effectuer les 4 opérations de bases comprenant additions et soustractions.

    Traduisez les opérandes ci-dessous en binaire, puis poser l'addition en binaire.

    1. $1 + 51$
    2. $51 - 7$
    3. $204 + 51$
    4. $204 + 204$ (sur 8-bits)

    ??? solution

        Voici la solution du calcul en binaire :

        1. $1 + 51$

            ```text
                    ¹¹
                     1₂
            +   110011₂  (2⁵ + 2⁴ + 2¹+ 2⁰ ≡ 51)
            ----------
                110100₂
            ```

        2. $51 - 7$

            ```text
              …¹¹¹  ¹¹
              …000110011₂  (2⁵ + 2⁴ + 2¹ + 2⁰ ≡ 51)
            + …111111001₂  (complément à deux, 2³ + 2¹ + 2⁰ ≡ 111₂ → !7 + 1 ≡ …111001₂)
              -----------
              …000101100₂  (2⁵ + 2³ + 2₂ ≡ 44)
            ```

        3. $204 + 51$

            ```text
                11001100₂
            +     110011₂
              -----------
              …011111111₂  (2⁸ - 1 ≡ 255)
            ```

        4. $204 + 204$ (sur 8-bits)

            ```text
                ¹|¹  ¹¹
                 |11001100₂
             +   |11001100₂
              ---+--------
                1|10011000₂  (152, le résultat complet devrait être 2⁸ + 152 ≡ 408)
            ```

### Opérateurs relationnels

Les opérateurs relationnels permettent de comparer deux valeurs. Le résultat d'un opérateur relationnel est toujours un **booléen** c'est-à-dire que le résultat d'une comparaison est soit **vrai**, soit **faux**.

Rappelons qu'en C et dans la plupart des langages de programmation, une valeur vraie est représentée par `1` et une valeur fausse par `0`.

Les opérateurs relationnels sont les suivants :

Table: Opérateurs relationnels

| Opérateur | Abréviation | Description           | Exemple vrai     |
| --------- | ------------ | --------------------- | ---------------- |
| `==`      | *eq*         | Égal                  | `42 == 0x101010` |
| `!=`      | *ne*         | Différent             | `'a' != 'c'`     |
| `>=`      | *ge*         | Supérieur ou égal     | `9 >= 9`         |
| `<=`      | *le*         | Inférieur ou égal     | `-8 <= 8`        |
| `>`       | *gt*         | Strictement supérieur | `0x31 > '0'`     |
| `<`       | *lg*         | Strictement inférieur | `8 < 12.33`      |

Un opérateur relationnel est plus prioritaire qu'un opérateur d'affectation et donc l'écriture suivante applique le test d'égalité entre `a` et `b` et le résultat de ce test `1` ou `0` sera affecté à la variable `c` :

```c
int a = 2, b = 3;
int c = a == b;
```

Les opérateurs relationnels sont le plus souvent utilisés dans des structures de contrôles :

```c
if (a == b) {
    printf("Les opérandes sont égaux.\n");
} else {
    printf("Les opérandes ne sont pas égaux.\n");
}
```

!!! tip

    Programmer c'est être minimaliste, dès lors il serait possible de simplifier l'écriture ci-dessus de la façon suivante :

    ```c
    printf("Les opérandes %s égaux.\n", a == b ? "sont" : "ne sont pas");
    ```

    Dans se cas on utilise l'opérateur ternaire `? :` qui permet de s'affranchir d'une structure de contrôle explicite.



Attention lors de l'utilisation du test d'égalité avec des valeurs flottantes, ces dernières sont des approximations et il est possible que deux valeurs qui devraient être égales ne le soient pas.

Par exemple, cette assertion est fausse :

```c
assert(0.1 + 0.2 == 0.3) // false
```

Pour comparer des valeurs flottantes, il est recommandé d'utiliser une fonction de comparaison qui prend en compte une marge d'erreur. Par exemple, on pourrait écrire une fonction `float_eq` qui compare deux valeurs flottantes avec une marge d'erreur de `0.0001` :

```c
bool float_eq(float a, float b) {
    return fabs(a - b) < 0.0001;
}
```

Alternativement on peut utiliser la définition `FLT_EPSILON` qui est la plus petite valeur positive telle que `1.0 + FLT_EPSILON != 1.0` :

```c
assert(fabs(0.1 + 0.2 - 0.3) < FLT_EPSILON);
```

Voici une démonstration :

```c
#include <stdio.h>
#include <float.h>
#include <math.h>
int main() {
    double u1 = 0.3, u2 = 0.1 + 0.2;
    long long int i1 = *(long int*)&u1;
    long long int i2 = *(long int*)&u2;
    printf("Hex value of 0.3:\t\t0x%x\n", i1);
    printf("Hex value of 0.3:\t\t0x%x\n", i2);

    printf("Float value of 0.3:\t\t%.20f\n", u1);
    printf("Float value of 0.1 + 0.2:\t%.20f\n", u2);

    printf("0.1 + 0.2 == 0.3: %d\n", u1 == u2);
    printf("0.1 + 0.2 == 0.3: %d\n", fabs(u1 - u2) < DBL_EPSILON );
}
```

Le résultat de ce programme est le suivant :

```text
Hex value of 0.3:               0x33333333
Hex value of 0.3:               0x33333334
Float value of 0.3:             0.29999999999999998890
Float value of 0.1 + 0.2:       0.30000000000000004441
0.1 + 0.2 == 0.3: 0
0.1 + 0.2 == 0.3: 1
```

!!! warning "Confusion = et =="

    L'erreur est si vite commise, mais souvent fatale :

    ```c
    if (c = 'o') {

    }
    ```

    L'effet contre-intuitif est que le test retourne toujours VRAI, car `'o' > 0`. Ajoutons que la valeur de `c` est modifié au passage.

    Observations :

    - Pour éviter toute ambiguïté, éviter les affectations dans les structures conditionnelles.

!!! info "Triple égalité ?"

    Dans certains langages comme le [JavaScript](https://fr.wikipedia.org/wiki/JavaScript), il existe un opérateur de comparaison `===` qui compare non seulement les valeurs mais aussi les types.

    En C, il n'existe pas d'opérateur de comparaison de type, il faut donc faire attention à ce que les types des opérandes soient compatibles.

    Voici une différence entre C et JavaScript:

    === "C"

        ```c
        assert('4' == 4); // false
        assert(4 == 4.0); // true
        ```

    === "JavaScript"

        ```javascript
        assert('4' == 4); // true
        assert('4' === 4); // false
        ```

### Opérateurs bit à bit

Les **opérations bit à bit** (*bitwise*) agissent sur chaque bit d'une valeur. Les disponibles en C sont les suivantes :

Table: Opérateurs bit à bit

| Opérateur | Description                                | Exemple                          |
| --------- | ------------------------------------------ | -------------------------------- |
| `&`     | [Conjonction (ET)][operator-and]          | `(0b1101 & 0b1010) == 0b1000`  |
| `        | `                                         | [Disjonction (OU)][operator-or] | `(0b1101 | 0b1010) == 0b1111` |
| `^`     | [XOR binaire][operator-xor]               | `(0b1101 ^ 0b1010) == 0b0111`  |
| `~`     | [Complément à un][operator-not]           | `~0b11011010 == 0b00100101`    |
| `<<`    | [Décalage à gauche][operator-shift-left]  | `(0b1101 << 3) == 0b1101000`   |
| `>>`    | [Décalage à droite][operator-shift-right] | `(0b1101 >> 2) == 0b11`        |


!!! important

    Ne pas confondre l'opérateur `!` et l'opérateur `~`. Le premier est la négation d'un nombre tandis que l'autre est l'inversion bit à bit. La négation d'un nombre différent de zéro donnera toujours `0` et la négation de zéro donnera toujours `1`.

[](){#operator-and}

#### Conjonction

La conjonction ou **ET logique** ($\wedge$) est identique à la multiplication appliquée bit à bit et ne génère pas de retenue.

Table: Conjonction bit à bit

| $A ∧ B$ @rb @bb | $A=0$ | $A=1$ |
| --------------- | ----- | ----- |
| $B=0$           | 0     | 0     |
| $B=1$           | 0     | 1     |

Avec cette opération l'état dominant est le `0` et l'état récessif est le `1`. Il suffit qu'une seule valeur soit à zéro pour forcer le résultat à zéro :

```c
assert(0b1100 & 0b0011 == 0b0000)
```

Cet opérateur est d'ailleurs souvent utilisé pour imposer une valeur nulle suivant une condition. Dans l'exemple suivant, le [Balrog](https://fr.wikipedia.org/wiki/Balrog) est réduit à néant par [Gandalf](https://fr.wikipedia.org/wiki/Gandalf) le gris :

```c
balrog = 0b1100110101;
gandalf = 0;

balrog = balrog & gandalf; // You shall not pass!
```

[](){#operator-or}

#### Disjonction

La disjonction ou **OU logique** ($\lor$) s'apparente à l'opération `+`.

Table: Disjonction bit à bit

| $A ∨ B$ | $A=0$ | $A=1$ |
| ------- | ----- | ----- |
| $B=0$   | 0     | 1     |
| $B=1$   | 1     | 1     |

Ici l'état dominant est le `1` car il force n'importe quel `0` à changer d'état :

```c
bool student = false; // Veut pas faire ses devoirs ?
bool teacher = true;

student = student | teacher; // Tes devoirs tu feras...
```

[](){#operator-xor}

#### Disjonction exclusive

Le **OU exclusif** ($\oplus$ ou $\veebar$) est une opération curieuse, mais extrêmement puissante et utilisée massivement en cryptographie.

En électronique sur les symboles CEI, l'opération logique est nommée, `=1` car si le résultat de l'addition des deux opérandes est différent de `1`, la sortie sera nulle. Lorsque `A` et `B` valent `1` la somme vaut `2` et donc la sortie est nulle.

Table: Disjonction exclusive

| $A \veebar B$ | $A=0$ | $A=1$ |
| ------------- | ----- | ----- |
| $B=0$         | 0     | 1     |
| $B=1$         | 1     | 0     |

L'opération présente une propriété très intéressante : elle est réversible.

```c
assert(1542 ^ 42 ^ 42 == 1542)
```

Par exemple il est possible d'inverser la valeur de deux variables simplement :

```c
int a = 123;
int b = 651;

a ^= b;
b ^= a;
a ^= b;

assert(a == 651);
assert(b == 123);
```

!!! warning "Attention"

    Attention avec cet exemple, il ne fonctionne que si les deux valeurs `a` et `b` ont des adresses mémoires différentes. Si les deux variables pointent vers la même adresse mémoire, le résultat sera `0`.

    ```c
    int a = 123;
    int *b = &a;

    a ^= *b;
    *b ^= a;
    a ^= *b;

    assert(a == 0);
    assert(*b == 0);
    ```

[](){#operator-not}
#### Complément à un

Le complément à un ($\lnot$) est simplement la valeur qui permet d'inverser bit à bit une valeur :

Table: Complément à un

| $A$ | $\lnot~A$ |
| --- | --------- |
| 0   | 1         |
| 1   | 0         |

!!! info

    Pourquoi l'opération s'appelle le complément à un ? Complémenter à $N$ signifie trouver la valeur telle que $A + \lnot A = N$. Par exemple, en base 10, pour complémenter à $A = 9$ il suffit de faire $9 - A$.

    En base 10, le symbole le plus grand est `9`. En binaire le symbole le plus grand est `1`. Donc pour inverser un nombre on complémente chaque bit à un.

[](){#operator-shift-left}
[](){#operator-shift-right}
#### Décalages

Les opérations de décalage permettent de déplacer les bits d'une valeur vers la gauche ou vers la droite. Les bits décalés sont perdus et remplacés par des zéros dans le cas d'une valeur non signée et par le bit de signe dans le cas d'une valeur signée.

```c
assert(0b0000'1101 << 2 == 0b0011'0100)
assert(0b0001'0000 >> 4 == 0b0000'0001)

char a = 0b1000'0000;
char b = a << 1;
assert(b == 0x0000'0000);

assert(-8 >> 1 == -4) // 0b1111'1000 >> 1 == 0b1111'1100
```

!!! warning

    Le standard ne définit pas le comportement des décalages pour des valeurs de décalage négatives (`a >> -2`). Néanmoins il n'y aura pas d'erreur de compilation, le comportement est simplement indéfini et le résultat dépend donc du compilateur utlisé.

#### Tester un bit

En micro-informatique, il est fréquent de tester l'état d'un bit. Pour cela on utilise l'opération ET logique `&` avec un masque. Par exemple, pour tester le bit de poids faible d'une valeur, `a` on peut écrire :

```c
int a = 0b1101'1010;
int mask = 0b0000'0001;

if (a & mask) {
    printf("Le bit de poids faible est à 1.\n");
} else {
    printf("Le bit de poids faible est à 0.\n");
}
```

En pratique il est préférable de numéroter le bit que l'on souhaite tester pour plus de clarté. On peut positionner un bit à la position souhaitée avec l'opération de décalage `<<` :

```c
int a = 0b1101'1010;
int bit = 1;
printf("Le bit %d à %d.\n", bit, a & (1 << bit));
```

#### Inverser un bit

Pour inverser un bit, on utilise l'opération XOR `^` avec un masque. Par exemple, pour inverser le bit de poids faible d'une valeur `a` on peut écrire :

```c
int a = 0b1101'1010;
int bit = 3;
int b = a ^ (1 << bit);
```

#### Forcer un bit à un

Pour forcer un bit à un, on utilise l'opération OU `|` avec un masque. Par exemple, pour forcer le bit de poids faible d'une valeur `a` à un on peut écrire :

```c
int a = 0b1101'1010;
int bit = 2;
int b = a | (1 << bit);
```

#### Forcer un bit à zéro

Pour forcer un bit à zéro, on utilise l'opération ET `&` avec un masque inversé. Par exemple, pour forcer le bit de poids faible d'une valeur `a` à zéro on peut écrire :

```c
int a = 0b1101'1010;
int bit = 4;
int b = a & ~(1 << bit);
```

### Opérations logiques

Les opérations logiques sont introduites par l'[algèbre de Boole](<https://fr.wikipedia.org/wiki/Alg%C3%A8bre_de_Boole_(logique)>) et permettent de combiner plusieurs grandeurs binaires en utilisant des opérations. Les opérateurs logiques sont au nombre de deux et ne doivent pas être confondus avec leur petits frères `&` et `|`.

Table: Opérateurs arithmétiques

| Opérateur                 | ISO646 | Description | Assertion vraie                              |
| ------------------------- | ------ | ----------- | -------------------------------------------- |
| `&&`                      | *and*  | ET logique  | `true && false == false`                     |
| <code>&#124;&#124;</code> | *or*   | OU logique  | <code>true &#124;&#124; false == true</code> |

Le résultat d'une opération logique est toujours un `booléen` (valeur 0 ou 1). Ainsi l'expression suivante affecte `1` à `x` : `x = 12 && 3 + 2`.

La priorité des opérateurs logiques est plus faible que celle des opérateurs de comparaison et plus forte que celle des opérateurs d'affectation. Ainsi l'expression `a == b && c == d` est équivalente à `(a == b) && (c == d)`. Les parenthèses sont facultatives, mais permettent de clarifier l'expression.

!!! warning

    La priorité de l'opérateur `&&` est plus forte que celle de l'opérateur `||`. Ainsi l'expression `a || b && c` est équivalente à `a || (b && c)`. C'est un piège classique en programmation, pour l'éviter il est recommandé d'utiliser des parenthèses.

!!! warning "Confusion `&` et `&&`"

    Confondre le ET logique et le ET binaire est courant. Dans l'exemple suivant, le `if` n'est jamais exécuté:

    ```c
    int a = 0xA;
    int b = 0x5;

    if(a & b) {

    }
    ```

### Opérateurs d'affectation

Les opérateurs d'affectation permettent d'assigner de nouvelles valeurs à une variable. En C il existe des sucres syntaxiques permettant de simplifier l'écriture lorsqu'une affectation est couplée à un autre opérateur.

Table: Opérateurs d'affectation

| Opérateur            | Description                     | Exemple                  | Équivalence                 |
| -------------------- | ------------------------------- | ------------------------ | --------------------------- |
| `=`                  | Affectation simple              | `x = y`                  | `x = y`                     |
| `+=`                 | Affectation par addition        | `x += y`                 | `x = x + y`                 |
| `-=`                 | Affectation par soustraction    | `x -= y`                 | `x = x - y`                 |
| `*=`                 | Affectation par multiplication  | `x *= y`                 | `x = x * y`                 |
| `/=`                 | Affectation par division        | `x /= y`                 | `x = x / y`                 |
| `%=`                 | Affectation par modulo          | `x %= y`                 | `x = x % y`                 |
| `&=`                 | Affectation par conjonction     | `x &= y`                 | `x = x & y`                 |
| <code>&#124;=</code> | Affectation par disjonction     | <code>x &#124;= y</code> | <code>x = x &#124; y</code> |
| `^=`                 | Affectation par XOR             | `x ^= y`                 | `x = x ^ y`                 |
| `<<=`                | Affectation par décalage gauche | `x <<= y`                | `x = x << y`                |
| `>>=`                | Affectation par décalage droite | `x >>= y`                | `x = x >> y`                |

Un opérateur d'affectation implique que la valeur à gauche de l'égalité soit modifiable ([lvalue][lvalue]). Ainsi l'expression `3 += 2` est incorrecte, car `3` est une constante et ne peut être modifiée.

!!! exercise "R-value"

    Est-ce que l'expression suivante est valide ?

    ```c
    int a, b, c = 42;
    a + b = c;
    ```

    - [ ] Oui car la destination est une *lvalue*
    - [x] Non car la destination est une *rvalue*

    ??? solution

        L'opération `+` entre deux nombre retourne une *rvalue* et ne peut donc pas être affecté. L'expression est donc invalide.

### Opérateurs d'incrémentation

Les opérateurs d'incrémentation sont régulièrement un motif primaire d'arrachage de cheveux pour les étudiants. En effet, ces opérateurs sont très particuliers à ce sens qu'il se décomposent en deux étapes : l'affectation et l'obtention du résultat. Il existe 4 opérateurs d'incrémentation :

Table: Opérateurs arithmétiques

| Opérateur | Description         | Assertion vraie |
| --------- | ------------------- | --------------- |
| `()++`    | Post-incrémentation | `i++`           |
| `++()`    | Pré-incrémentation  | `++i`           |
| `()--`    | Post-décrémentation | `i--`           |
| `--()`    | Pré-décrémentation  | `--i`           |

La pré-incrémentation ou pré-décrémentation effectue en premier la modification de la variable impliquée puis retourne le résultat de cette variable modifiée. Dans le cas de la post-incrémentation ou pré-décrémentation, la valeur actuelle de la variable est d'abord retournée, puis dans un second temps cette variable est incrémentée.

Notons qu'on peut toujours décomposer ces opérateurs en deux instructions explicites. Le code :

=== "Forme réduite"

    ```c
    y = x++;

    y = ++x;
    ```

=== "Forme étendue"

    ```c
    y = x;
    x = x + 1;

    x = x + 1;
    y = x;
    ```

!!! tip

    Pour résoudre les ambiguïtés, on procède par étape. Par exemple l'expression suivante n'est pas très claire :

    ```c
    k = i++ * 4 + --j * 2
    ```

    1. On commence par résoudre les pré-incrémentation et pré-décrémentation :

        ```c
        j = j - 1;
        k = i++ * 4 + j * 2
        ```
    2. Ensuite on résout les post-incrémentation :

        ```c
        j = j - 1;
        k = i * 4 + j * 2
        i = i + 1;
        ```
    3. On peut utiliser les sucres syntaxiques pour simplifier l'écriture :

        ```c
        j -= 1;
        k = i * 4 + j * 2
        i += 1;
        ```

!!! warning "Écriture déroutante"

    Selon la table de précédences on aura `i--` calculé en premier suivi de `- -j`:

    ```c
    k = i----j;
    ```

    Observations :

    - Éviter les formes ambigües d'écriture
    - Favoriser la précédence explicite en utilisant des parenthèses
    - Séparez vos opérations par des espaces pour plus de lisibilité: `#!c k = i-- - -j`

!!! tip

    Il est généralement préférable d'utiliser la pré-incrémentation ou la pré-décrémentation car elles sont plus efficaces. En effet, la post-incrémentation ou la post-décrémentation nécessitent de stocker la valeur actuelle de la variable pour la retourner après l'incrémentation ou la décrémentation.

    C'est particulièrement le cas en C++ où la post-incrémentation ou la post-décrémentation nécessitent de créer une copie de la variable avant de l'incrémenter ou de la décrémenter.

    En C++ on utilise la surcharge d'opérateur pour définir le comportement de l'opérateur `++` et `--` pour les classes personnalisées. Ajouter à une classe ce type de surcharge se fait comme ceci :

    ```cpp
    class MyClass {
    public:
        // Pré-incrémentation
        auto operator++() {
            return *this;
        }

        // Post-incrémentation
        auto operator++(int) {
            MyClass tmp(*this);
            operator++();
            return tmp;
        }
    };
    ```

    On voit que la post-incrémentation crée une copie de l'objet avant de l'incrémenter, elle est donc moins efficace.

    Donc dans une boucle `for` on préférera :

    ```c
    for (int i = 0; i < 10; ++i) { }
    ```

    Plutôt que

    ```c
    for (int i = 0; i < 10; i++) { }
    ```

[](){#operator-ternary}
### Opérateur ternaire

L'opérateur ternaire aussi appelé **opérateur conditionnel** permet de faire un test et de retourner soit le second opérande, soit le troisième opérande. C'est le seul opérateur du C avec une `arité` de 3. Chacun des opérandes est symbolisé avec une paire de parenthèses :

```c
()?():()
```

Cet opérateur permet sur une seule ligne d'évaluer une expression et de renvoyer une valeur ou une autre selon que l'expression est vraie ou fausse.

```text
valeur = (condition ? valeur si condition vraie : valeur si condition fausse);
```

!!! note
    Seule la valeur utilisée pour le résultat est évaluée. Par exemple, dans le code `x > y ? ++y : ++x`, seulement `x` ou `y` sera incrémenté.

On utilise volontiers cet opérateur lorsque dans les deux cas d'un embranchement, la même valeur est modifiée :

```c
if (a > b)
    max = a;
else
    min = b;
```

On remarque dans cet exemple une répétition `max =`. Une façon plus élégante et permettant de réduire l'écriture est d'utiliser l'opérateur ternaire :

```c
max = a > b ? a : b;
```

!!! warning

    Ne pas utiliser l'opérateur ternaire si vous ne modifiez pas une valeur. L'opérateur ternaire est un opérateur de **sélection** et non de **modification**.

    === "Bon exemple"

        ```c
        int max = a > b ? a : b;
        ```

    === "Mauvais exemple"

        ```c
        a > b ? max = a : min = b;
        ```

    Cela va de même pour afficher une valeur :

    === "Bon exemple"

        ```c
        printf("Le maximum est %d\n", a > b ? a : b);
        ```

    === "Mauvais exemple"

        ```c
        a > b ? printf("Le maximum est %d\n", a) : printf("Le maximum est %d\n", b);
        ```

Enfin, on notera que le résultat de l'opérateur ternaire est une *rvalue* et ne peut donc pas être modifiée.

[](){#operator-cast}
### Opérateur de transtypage

Le `transtypage` ou *cast* permet de modifier explicitement le type apparent d'une variable. C'est un opérateur particulier, car son premier opérande doit être un **type** et le second une **valeur**.

```c
(type)(valeur)
```

Dans l'exemple suivant, le résultat de la division est un entier, car la promotion implicite de type reste un entier `int`. La valeur `c` vaudra donc le résultat de la division entière alors que dans le second cas, `b` est *casté* en un `double` ce qui force une division en virgule flottante.

```c
int a = 5, b = 2;
double c = a / b;
double d = a / (double)(b);
assert(c == 2.0 && d == 2.5);
```

[](){#operator-comma}
### Opérateur séquentiel

L'opérateur séquentiel (*comma operator*) permet l'exécution ordonnée d'opérations, et retourne la dernière valeur. Son utilisation est couramment limitée, soit aux déclarations de variables, soit au boucles `for`:

```c
for (size_t i = 0, j = 10; i != j; i++, j--) { /* ... */ }
```

Dans le cas ci-dessus, il n'est pas possible de séparer les instructions `i++` et `j--` par un point-virgule, l'opérateur virgule permet alors de combiner plusieurs instructions en une seule.

Une particularité de cet opérateur est que seule la dernière valeur est retournée :

```c
assert(3 == (1, 2, 3))
```

L'opérateur agit également comme un Point de séquence [](){#sequence_point}, c'est-à-dire que l'ordre des étapes est respecté.

!!! exercise "Opérateur séquentiel"

    Que sera-t-il affiché à l'écran ?

    ```c
    int i = 0;
    printf("%d", (++i, i++, ++i));
    ```

### Opérateur sizeof

Cet opérateur est *unaire* et retourne la taille en **byte** de la variable ou du type passé en argument. Il n'existe pas de symbole particulier et son usage est très similaire à l'appel d'une fonction:

```c
int32_t foo = 42;
assert(sizeof(foo) == 4);
assert(sizeof(int64_t) == 64 / 8);
```

L'opérateur `sizeof` est très utile durant le débogage pour connaître la taille en mémoire d'une variable ou celle d'un type. On l'utilise en pratique pour connaître la taille d'un tableau lors d'une boucle itérative :

```c
int32_t array[128];
for (int i = 0; i < sizeof(array) / sizeof(array[0]); i++) {
   array[i] = i * 10;
}
```

Dans l'exemple ci-dessus, `sizeof(array)` retourne la taille de l'espace mémoire occupé par le tableau `array`, soit $128 \cdot 4$ bytes. Pour obtenir le nombre d'éléments dans le tableau, il faut alors diviser ce résultat par la taille effective de chaque élément du tableau. L'élément `array[0]` est donc un `int32_t` et sa taille vaut donc 4 bytes.

!!! note

    Dans l'exemple ci-dessus, il est possible de s'affranchir de la taille effective du tableau en utilisant une sentinelle. Si le dernier élément du tableau à une valeur particulière et que le reste est initialisé à zéro, il suffit de parcourir le tableau jusqu'à cette valeur :

```c
int32_t array[128] = { [127]=-1 };
int i = 0;
while (array[i] != -1) {
    array[i++] = i * 10;
}
```

Cette écriture reste malgré tout très mauvaise, car le tableau de 128 éléments doit être initialisé à priori ce qui mène aux mêmes performances. D'autre part l'histoire racontée par le développeur est moins claire que la première implémentation.

## Priorité des opérateurs

La **précédence** est un anglicisme de *precedence* (priorité) qui concerne la priorité des opérateurs, ou l'ordre dans lequel les opérateurs sont exécutés.

Chacun connaît la priorité des quatre opérateurs de base (`+`, `-`, `*`, `/`), mais le C et ses nombreux opérateurs sont bien plus complexes.

La table suivante indique les règles à suivre pour les précédences des opérateurs en C.

Table: Priorité des opérateurs

| Priorité | Opérateur                 | Description @flex                       | Associativité   |
| -------- | ------------------------- | --------------------------------------- | --------------- |
| 1 @span  | `++`, `--`                | Postfix incréments/décréments           | Gauche à Droite @span |
|          | `()`                      | Appel de fonction                       |                 |
|          | `[]`                      | Indexage des tableaux                   |                 |
|          | `.`                       | Élément d'une structure                 |                 |
|          | `->`                      | Élément d'une structure                 |                 |
| 2 @span  | `++`, `--`                | Préfixe incréments/décréments           | Droite à Gauche @span |
|          | `+`, `-`                  | Signe                                   |                 |
|          | `!`, `~`                  | NON logique et NON binaire              |                 |
|          | `(type)`                  | [Cast (Transtypage)][operator-cast]{ data-preview }    |                 |
|          | `*`                       | Indirection, déréférencement            |                 |
|          | `&`                       | Adresse de...                           |                 |
|          | `sizeof`                  | Taille de...                            |                 |
| 3        | `*`, `/`, `%`             | Multiplication, Division, Mod           | Gauche à Droite @span |
| 4        | `+`, `-`                  | Addition, soustraction                  |                 |
| 5        | `<<`, `>>`                | Décalages binaires                      |                 |
| 6 @span  | `<`, `<=`                 | Comparaison plus petit que              |                 |
|          | `>`, `>=`                 | Comparaison plus grand que              |                 |
| 7        | `==`, `!=`                | Égalité, non égalité                    |                 |
| 8        | `&`                       | ET binaire                              |                 |
| 9        | `^`                       | OU exclusif binaire                     |                 |
| 10       | <code>&#124;</code>       | OU inclusif binaire                     |                 |
| 11       | `&&`                      | ET logique                              |                 |
| 12       | <code>&#124;&#124;</code> | OU logique                              |                 |
| 13       | `?:`                      | [Opérateur ternaire][operator-ternary]{ data-preview } | Droite à Gauche @span |
| 14 @span | `=`                       | Assignation simple                      |                 |
|          | `+=`, `-=`                | Assignation par somme/diff              |                 |
|          | `*=`, `/=`, `%=`          | Assignation par produit/quotient/modulo |                 |
|          | `<<=`, `>>=`              | Assignation par décalage binaire        |                 |
| 15       | `,`                       | [Virgule][operator-comma]{ data-preview }              | Gauche à Droite |


Considérons l'exemple suivant :

```c
int i[2] = {10, 20};
int y = 3;

x = 5 + 23 + 34 / ++i[0] & 0xFF << y;
```

Selon la précédence de chaque opérateur ainsi que son associativité on a :

```text
[]  1
++  2
/   3
+   4
+   4
<<  5
&   8
=   14
```

!!! info "Notation polonaise inversée"

    La notation polonaise inversée (*Reverse Polish Notation*) est une notation mathématique où les opérateurs sont placés après leurs opérandes.

    L'écriture en notation polonaise inversée donnerait alors :

    ```text
    34, i, 0, [], ++,  /, 5, 23, +, +, 0xFF, y, <<, &, x, =
    ```

    C'est une notation très utilisée en informatique pour les calculatrices et les compilateurs car elle permet de simplifier l'écriture des expressions mathématiques, et surtout s'affranchir du problème des priorités d'opérateurs.

    L'algorithme de [Shunting Yard](https://en.wikipedia.org/wiki/Shunting-yard_algorithm) permet de convertir une expression en notation infixée en une expression en notation polonaise inversée.

### Associativité

L'associativité des opérateurs ([operator associativity](https://en.wikipedia.org/wiki/Operator_associativity)) décrit la manière dont sont évaluées les expressions.

Une associativité à gauche pour l'opérateur `~` signifie que l'expression `a ~ b ~ c` sera évaluée `((a) ~ b) ~ c` alors qu'une associativité à droite sera `a ~ (b ~ (c))`.

Note qu'il ne faut pas confondre l'associativité *évaluée de gauche à droite* qui est une associativité à *gauche*.


## Promotion de type

Nous avons vu au chapitre sur les types de données que les types C
définis par défaut sont représentés en mémoire sur 1, 2, 4 ou 8 octets.
On comprend aisément que plus cette taille est importante, plus on gagne
en précision ou en grandeur représentable. La promotion numérique régit
les conversions effectuées implicitement par le langage C lorsqu'on
convertit une donnée d'un type vers un autre. Cette promotion tend à
conserver le maximum de précision lorsqu'on effectue des calculs entre
types différents (p.ex : l'addition d'un `int` avec un `double` donne un
type `double`). Voici les règles de base :

- les opérateurs ne peuvent agir que sur des types identiques ;
- quand les types sont différents, il y a conversion automatique vers le type ayant le plus grand pouvoir de représentation ;
- les conversions ne sont faites qu'au fur et à mesure des besoins.

La **promotion** est l'action de promouvoir un type de donnée en un autre type de donnée plus général. On parle de promotion implicite des entiers lorsqu'un type est promu en un type plus grand automatiquement par le compilateur.

## Lois de De Morgan

Les [lois de De Morgan](https://fr.wikipedia.org/wiki/Lois_de_De_Morgan) sont des identités logiques formulées il y a près de deux siècles par Augustus De Morgan (1806-1871). À noter que l'on peut prononcer *də mɔʁ.gɑ̃* (de Mort Gant) ou *də mɔʁ.ɡan* (de Morgane).

En logique classique, la négation d'une conjonction implique la disjonction des négations et la conjonction de négations implique la négation d'une disjonction. On peut donc écrire les relations suivantes :

$$
\begin{aligned}
& \overline{P \land Q} &\Rightarrow~& \overline{P} \lor \overline{Q} \\
& \overline{P} \land \overline{Q} &\Rightarrow~& \overline{P \lor Q}
\end{aligned}
$$

Ces opérations logiques sont très utiles en programmation où elles permettent de simplifier certains algorithmes.

À titre d'exemple, les opérations suivantes sont équivalentes :

```c
int a = 0b110010011;
int b = 0b001110101;

assert(a | b == ~a & ~b);
assert(~a & ~b == ~(a | b));
```

En logique booléenne on exprime la négation par une barre p.ex. $\overline{P}$.

!!! exercise "De Morgan"

    Utiliser les relations de De Morgan pour simplifier l'expression suivante

    $$
    D \cdot E + \overline{D} + \overline{E}
    $$

    ??? solution

        Si l'on applique De Morgan ($\overline{XY} = \overline{X} + \overline{Y}$):

        $$
        D \cdot E + \overline{D} + \overline{E}
        $$

## Arrondis

En programmation, la notion d'arrondi ([rounding](https://en.wikipedia.org/wiki/Rounding)) est beaucoup plus délicate que l'on peut l'imaginer de prime abord.

Un nombre réel dans $\mathbb{R}$ peut être converti en un nombre entier de plusieurs manières dont voici une liste non exhaustive :

- tronqué (*truncate*) lorsque la partie fractionnaire est simplement enlevée ;
- arrondi à l'entier supérieur (*rounding up*) ;
- arrondi à l'entier inférieur (*rounding down*) ;
- arrondi en direction du zéro (*rounding towards zero*) ;
- arrondi loin du zéro (*rounding away from zero*) ;
- arrondi au plus proche entier (*rounding to the nearest integer*) ;
- arrondi la moitié en direction de l'infini (*rounding half up*).

Selon le langage de programmation et la méthode utilisée, le mécanisme d'arrondi sera différent. En C, la bibliothèque mathématique offre les fonctions `ceil` pour l'arrondi au plafond (entier supérieur), `floor` pour arrondi au plancher (entier inférieur) et `round` pour l'arrondi au plus proche (*nearest*). Il existe également une fonction `trunc` qui tronque la valeur en supprimant la partie fractionnaire.

Le fonctionnement de la fonction `round` n'est pas unanime entre les mathématiciens et les programmeurs. C utilise l'arrondi au plus proche, c'est-à-dire que -23.5 donne -24 et 23.5 donnent 24.

En Python ou en Java, c'est la méthode du *commercial rounding* qui a été choisie. Elle peut paraître contre-intuitive, car `round(3.5)` donne 4, mais `round(4.5)` donne 4 aussi.

Pourquoi faire cela ? Il y a deux raisons principales :

1. **Réduction du biais cumulatif** : Lorsque vous arrondissez toujours vers le haut ou vers le bas en cas de valeur à mi-chemin (comme 0.5), cela introduit un biais systématique dans vos données. Par exemple, si vous arrondissez toujours 0.5 vers le haut, la somme des valeurs arrondies sera systématiquement plus grande que la somme des valeurs originales.

2. **Statistiques plus précises** : En arrondissant les valeurs à la paire la plus proche, vous distribuez les erreurs d'arrondissement de manière plus équitable, ce qui donne des statistiques globales plus précises.

Supposons que nous avons les montants suivants:

```text
3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5
```

En utilisant l'arrondi classique (toujours vers le haut à 0.5), nous obtenons :

```text
4 + 5 + 6 + 7 + 8 + 9 + 10 = 49
```

En utilisant l'arrondi commercial, nous obtenons :

```text
4 + 4 + 6 + 6 + 8 + 8 + 10 = 46
```

Si on compare à la somme réelle des valeurs, on obtient :

```text
3.5 + 4.5 + 5.5 + 6.5 + 7.5 + 8.5 + 9.5 = 45.5
```

La méthode *round half to even* donne une somme arrondie (46) qui est plus proche de la somme réelle (45.5) que la méthode classique (49).

L'utilisation cette méthode est particulièrement utile dans les domaines où l'exactitude statistique est cruciale et où les erreurs d'arrondissement peuvent s'accumuler sur de grands ensembles de données, comme en finance, en analyse de données, et en statistiques.

[](){#lvalue}
[](){#rvalue}

## Valeurs gauches

Une `valeur gauche` (`lvalue`) est une particularité de certains langages de programmation qui définissent ce qui peut se trouver à gauche d'une affectation. Ainsi dans `x = y`, `x` est une valeur gauche. Néanmoins, l'expression `x = y` est aussi une valeur gauche :

```c
int x, y, z;

x = y = z;    // 1
(x = y) = z;  // 2
```

1. L'associativité de `=` est à droite donc cette expression est équivalente à `x = (y = (z))` qui évite toute ambiguïté.

2. En forçant l'associativité à gauche, on essaie d'assigner `z` à une *lvalue* et le compilateur s'en plaint :

   ```text
   4:8: error: lvalue required as left operand of assignment
     (x = y) = z;
             ^
   ```

Voici quelques exemples de valeurs gauches :

- `x /= y`
- `++x`
- `(x ? y : z)`

Par analogie une *rvalue* est une valeur qui ne peut se trouver à gauche d'une affectation. Ainsi `x + y` est une *rvalue* car elle ne peut être affectée. De même que `x++` est une *rvalue* car elle ne peut être affectée.

## Optimisation

Le compilateur est en règle général plus malin que le développeur. L'optimiseur de code (lorsque compilé avec `-O2` sous `gcc`), va regrouper certaines instructions, modifier l'ordre de certaines déclarations pour réduire soit l'empreinte mémoire du code, soit accélérer son exécution.

Ainsi l'expression suivante, ne sera pas calculée à l'exécution, mais à la compilation :

```c
int num = (4 + 7 * 10) >> 2;
```

De même que ce test n'effectuera pas une division, mais testera simplement le dernier bit de `a`:

```c
if (a % 2) {
    puts("Pair");
} else {
    puts("Impair");
}
```

## ISO/IEC 646

La bibliothèque standard `<iso646.h>` appartient à la norme C90 et définit des macros pour les opérateurs logiques. Ces macros sont les suivantes :

Table: Macros de l'ISO/IEC 646

| Opérateur |  Macro   | Description         |
| :-------: | :------: | :------------------ |
|   `&&`    |  `and`   | ET logique          |
|  `\|\|`   |   `or`   | OU logique          |
|    `!`    |  `not`   | NON logique         |
|   `!=`    | `not_eq` | Différent de        |
|   `&=`    | `and_eq` | ET binaire          |
|   `\|=`   | `or_eq`  | OU binaire          |
|   `^=`    | `xor_eq` | OU exclusif binaire |
|    `^`    |  `xor`   | OU exclusif binaire |
|    `~`    | `compl`  | Complément binaire  |

Ces macros sont utiles pour les personnes qui ne peuvent pas taper certains caractères spéciaux sur leur clavier. Elles sont également utiles pour les personnes qui veulent rendre leur code plus lisible. Néanmoins, elles ne sont pas très utilisées en pratique.

```c
#include <iso646.h>

int foo(int a, int b, int c) {
    return a and b or not c;
}
```

## Exercices de révision

!!! exercise "Quelle priorité"

    Quel est l'opérateur qui a la priorité la plus basse ?

    - [ ] `+`
    - [ ] `*`
    - [ ] <code>&#124;&#124;</code>
    - [x] `&&`

!!! exercise "Masque binaire"

    Soit les déclarations suivantes :

    ```c
    char m, n = 2, d = 0x55, e = 0xAA;
    ```

    Représenter en binaire et en hexadécimal la valeur de tous les bits de la variable `m` après exécution de chacune des instructions suivantes :

    1. `m = 1 << n;`
    2. `m = ~1 << n;`
    3. `m = ~(1 << n);`
    4. `m = d | (1 << n);`
    5. `m = e | (1 << n);`
    6. `m = d ^ (1 << n);`
    7. `m = e ^ (1 << n);`
    8. `m = d & ~(1 << n);`
    9. `m = e & ~(1 << n);`


!!! exercise "Registre système"

    Pour programmer les registres 16-bits d'un composant électronique chargé de gérer des sorties tout ou rien, on doit être capable d'effectuer les opérations suivantes :

    - mettre à 1 le bit numéro `n`, `n` étant un entier entre 0 et 15;
    - mettre à 0 le bit numéro `n`, `n` étant un entier entre 0 et 15;
    - inverser le bit numéro `n`, `n` étant un entier entre 0 et 15;

    Pour des questions d'efficacité, ces opérations ne doivent utiliser que les opérateurs bit à bit ou décalage. On appelle `r0` la variable désignant le registre en mémoire et `n` la variable contenant le numéro du bit à modifier. Écrivez les expressions permettant d'effectuer les opérations demandées.

!!! exercise "Recherche d'expressions"

    Considérant les déclarations suivantes :

    ```c
    float a, b;
    int m, n;
    ```

    Traduire en C les expressions mathématiques ci-dessous; pour chacune, proposer plusieurs écritures différentes lorsque c'est possible. Le symbole $\leftarrow$ signifie *assignation*

    1. $n \leftarrow 8 \cdot n$
    2. $a \leftarrow a + 2$
    3. $n \leftarrow \left\{\begin{array}{lr}m & : m > 0\\ 0 & : \text{sinon}\end{array}\right.$
    4. $a \leftarrow n$
    5. $n \leftarrow \left\{\begin{array}{lr}0 & : m~\text{pair}\\ 1 & : m~\text{impair}\end{array}\right.$
    6. $n \leftarrow \left\{\begin{array}{lr}1 & : m~\text{pair}\\ 0 & : m~\text{impair}\end{array}\right.$
    7. $m \leftarrow 2\cdot m + 2\cdot n$
    8. $n \leftarrow n + 1$
    9. $a \leftarrow \left\{\begin{array}{lr}-a & : b < 0\\ a & : \text{sinon}\end{array}\right.$
    10. $n \leftarrow \text{la valeur des 4 bits de poids faible de}~n$


!!! exercise "Nombres narcissiques"

    Un nombre narcissique ou [nombre d'Amstrong](https://fr.wikipedia.org/wiki/Nombre_narcissique) est
    un entier naturel `n` non nul qui est égal à la somme des puissances `p`-ièmes de ses
    chiffres en base dix, où `p` désigne le nombre de chiffres de `n`:

    $$
    n=\sum_{k=0}^{p-1}x_k10^k=\sum_{k=0}^{p-1}(x_k)^p\quad\text{avec}\quad x_k\in\{0,\ldots,9\}\quad\text{et}\quad x_{p-1}\ne 0
    $$

    Par exemple :

    - `9` est un nombre narcissique, car $9 = 9^1 = 9$
    - `153` est un nombre narcissique, car $153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153$
    - `10` n'est pas un nombre narcissique, car $10 \ne 1^2 + 0^2 = 1$

    Implanter un programme permettant de vérifier si un nombre d'entrées est narcissique ou non. L'exécution est la suivante :

    ```bash
    $ ./armstrong 153
    1

    $ ./armstrong 154
    0
    ```

!!! exercise "Swap sans valeur intermédiaire"

    Soit deux variables entières `a` et `b`, chacune contenant une valeur différente. Écrivez les instructions permettant d'échanger les valeurs de a et de b sans utiliser de valeurs intermédiaires. Indice: utilisez l'opérateur XOR `^`.

    Testez votre solution...

    ??? solution

        ```c
        a ^= b;
        b ^= a;
        a ^= b;
        ```
