# Opérateurs

```{index} opérateur
```

```{index} arité
```

```{index} unaire
```

Le langage C est composé d'une multitude d'opérateurs permettant de modifier les valeurs de variables en mémoire. Un {index}`opérateur` prend habituellement deux opérandes et retourne un résultat. On dit alors que ces opérateurs ont une [arité](https://fr.wikipedia.org/wiki/Arit%C3%A9) de 2. Il existe également des opérateurs à arité de 1 dit [unaire](https://fr.wikipedia.org/wiki/Op%C3%A9ration_unaire) comme l'opposé d'un nombre réel : $-x$.

```{index} ALU
```

Dans un ordinateur c'est l'unité de calcul arithmétique [ALU](https://fr.wikipedia.org/wiki/Unit%C3%A9_arithm%C3%A9tique_et_logique) qui est en charge d'effectuer les opérations fondamentales. Un ordinateur à 2 GHz pourrait effectuer plus de 2'000'000'000 opérations par seconde. Cette unité de calcul est consensuellement représentée comme illustré à la figure {numref}`ual`.

(ual)=

:::{figure} ../../assets/figures/dist/processor/alu.*
:alt: ALU

Unité de calcul arithmétique ({index}`ALU`) composée de deux entrées `A` et `B`, d'une sortie `C` et d'un mode opératoire `O`.
:::

En admettant que l'opération est l'addition, le code C équivalent serait le suivant :

```c
c = a + b;
```

Notons qu'un opérateur possède plusieurs propriétés :

Une {index}`priorité`

: La multiplication `*` est plus prioritaire que l'addition `+`

Une {index}`associativité`

: L'opérateur d'affectation `=` possède une associativité à droite, c'est-à-dire que l'opérande à droite de l'opérateur sera évalué en premier

Un {index}`point de séquence`

: Certains opérateurs comme `&&`, `||`, `?` ou `,` possèdent un point de séquence garantissant que l'exécution séquentielle du programme sera respectée avant et après ce point. Par exemple si dans l'expression `i < 12 && j > 2` la valeur de `i` est plus grande que 12, le test `j > 2` ne sera jamais effectué. L'opérateur `&&` garanti l'ordre des choses ce qui n'est pas le cas avec l'affectation `=`.

## Opérateurs relationnels

```{index} opérateur relationnel
```

Les opérateurs relationnels permettent de comparer deux entités. Le résultat d'un opérateur relationnel est toujours un **boolean** c'est-à-dire que le résultat d'une comparaison est soit **vrai**, soit **faux**.

```{eval-rst}
.. table:: Opérateurs relationnels

    =========  =====================  ==================
    Opérateur  Description            Exemple vrai
    =========  =====================  ==================
    ``==``     Égal                   ``42 == 0x101010``
    ``>=``     Supérieur ou égal      ``9 >= 9``
    ``<=``     Inférieur ou égal      ``-8 <= 8``
    ``>``      Strictement supérieur  ``0x31 > '0'``
    ``<``      Inférieur              ``8 < 12.33``
    ``!=``     Différent              ``'a' != 'c'``
    =========  =====================  ==================
```

Un opérateur relationnel est plus prioritaire que l'opérateur d'affectation et donc l'écriture suivante applique le test d'égalité entre `a` et `b` et le résultat de ce test `1` ou `0` sera affecté à la variable `c` :

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

:::{note}
Programmer c'est être minimaliste, dès lors il serait possible de simplifier l'écriture ci-dessus de la façon suivante :

```c
printf("Les opérandes %s égaux.\n", a == b ? "sont" : "ne sont pas");
```

Dans se cas on utilise l'opérateur ternaire `? :` qui permet de s'affranchir d'une structure de contrôle explicite.
:::

## Opérateurs arithmétiques

```{index} modulo
```

Aux 4 opérations de base, le C ajoute l'opération [modulo](<https://fr.wikipedia.org/wiki/Modulo_(op%C3%A9ration)>), qui est le reste d'une division entière.

```{eval-rst}
.. table:: Opérateurs arithmétiques

    =========  =====================  ==================
    Opérateur  Description            Assertion vraie
    =========  =====================  ==================
    ``+``      Addition               ``5 == 2 + 3``
    ``-``      Soustraction           ``8 == 12 - 4``
    ``*``      Multiplication         ``42 == 21 * 2``
    ``/``      Division               ``2 == 5 / 2``
    ``%``      Modulo                 ``13 % 4 == 1``
    =========  =====================  ==================
```

Attention néanmoins aux types des variables impliquées. La division `5 / 2` donnera `2` et non `2.5` car les deux valeurs fournies sont entières.

Le modulo est le reste de la division entière. L'assertion suivante est donc vraie : `13 % 4 == 1`, car 13 divisé par 4 égal 3 et il reste 1.

Il est important de noter que les opérateurs arithmétiques sont tributaires des types sur lesquels ils s'appliquent. Par exemple, l'addition de deux entiers 8 bits `120 + 120` ne fera pas `240` car le type ne permet pas de stocker des valeurs plus grandes que `127` :

```c
int8_t too_small = 120 + 120;
assert(too_small != 120 + 120);
```

## Opérateurs bit à bit

Les opérations binaires agissent directement sur les bits d'une entrée, ils ont été vu en détail au chapitre sur la numération et ils sont listés sur la table {numref}`bitwise-operators`.

## Opérateurs d'affectation

```{index} sucre syntaxique
```

Les opérateurs d'affectation permettent d'assigner de nouvelles valeurs à une variable. En C il existe des sucres syntaxiques permettant de simplifier l'écriture lorsqu'une affectation est couplée à un autre opérateur.

```{eval-rst}
.. table:: Opérateurs d'affectation

    =========  ===============================  ===========  ==============
    Opérateur  Description                      Exemple      Équivalence
    =========  ===============================  ===========  ==============
    ``=``      Affectation simple               ``x = y``    ``x = y``
    ``+=``     Affectation par addition         ``x += y``   ``x = x + y``
    ``-=``     Affectation par soustraction     ``x -= y``   ``x = x - y``
    ``*=``     Affectation par multiplication   ``x *= y``   ``x = x * y``
    ``/=``     Affectation par division         ``x /= y``   ``x = x / y``
    ``%=``     Affectation par modulo           ``x %= y``   ``x = x % y``
    ``&=``     Affectation par conjonction      ``x &= y``   ``x = x & y``
    ``|=``     Affectation par disjonction      ``x |= y``   ``x = x | y``
    ``^=``     Affectation par XOR              ``x ^= y``   ``x = x ^ y``
    ``<<=``    Affectation par décalage gauche  ``x <<= y``  ``x = x << y``
    ``>>=``    Affectation par décalage droite  ``x >>= y``  ``x = x >> y``
    =========  ===============================  ===========  ==============
```

## Opérateurs logiques

Les opérateurs logiques sont au nombre de deux et ne doivent pas être confondus avec leur petits frères `&` et `|`.

- `&&` {index}`ET logique`
- `||` {index}`OU logique`

Le résultat d'une opération logique est toujours un {index}`booléen` (valeur 0 ou 1). Ainsi l'expression suivante affecte `1` à `x` : `x = 12 && 3 + 2`.

## Opérateurs d'incrémentation

Les opérateurs d'incrémentation sont régulièrement un motif d'arrachage de cheveux pour les étudiants. En effet, ces opérateurs sont très particuliers à ce sens qu'il se décomposent en deux étapes : l'affectation et l'obtention du résultat. Il existe 4 opérateurs d'incrémentation :

- `()++` Post-incrémentation
- `++()` Pré-incrémentation
- `()--` Post-décrémentation
- `--()` Pré-décrémentation

La pré-incrémentation ou pré-décrémentation effectue en premier la modification de la variable impliquée puis retourne le résultat de cette variable modifiée. Dans le cas de la post-incrémentation ou pré-décrémentation, la valeur actuelle de la variable est d'abord retournée, puis dans un second temps cette variable est incrémentée.

Notons qu'on peut toujours décomposer ces opérateurs en deux instructions explicites. Le code :

```c
y = x++;
```

est équivalent à :

```c
y = x;
x = x + 1;
```

De même :

```c
y = ++x;
```

est équivalent à :

```c
x = x + 1;
y = x;
```

## Opérateur ternaire

```{index} opérateur ternaire
```

L'opérateur ternaire aussi appelé {index}`opérateur conditionnel` permet de faire un test et de retourner soit le second opérande, soit le troisième opérande. C'est le seul opérateur du C avec une {index}`arité` de 3. Chacun des opérandes est symbolisé avec une paire de parenthèses :

```c
()?():()
```

Cet opérateur permet sur une seule ligne d'évaluer une expression et de renvoyer une valeur ou une autre selon que l'expression est vraie ou fausse. **valeur = (condition ? valeur si condition vraie : valeur si condition fausse);**

:::{note}
Seule la valeur utilisée pour le résultat est évaluée. Par exemple, dans le code `x > y ? ++y : ++x`, seulement `x` ou `y` sera incrémenté.
:::

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

## Opérateur de transtypage

```{index} cast
```

Le {index}`transtypage` ou *cast* permet de modifier explicitement le type apparent d'une variable. C'est un opérateur particulier car son premier opérande doit être un **type** et le second une **valeur**.

```c
(type)(valeur)
```

Dans l'exemple suivant, le résultat de la division est un entier car la promotion implicite de type reste un entier `int`. La valeur `c` vaudra donc le résultat de la division entière alors que dans le second cas, `b` est *casté* en un `double` ce qui force une division en virgule flottante.

```c
int a = 5, b = 2;
double c = a / b;
double d = a / (double)(b);
assert(c == 2.0 && d == 2.5);
```

## Opérateur séquentiel

L'opérateur séquentiel (*comma operator*) permet l'exécution ordonnée d'opérations, et retourne la dernière valeur. Son utilisation est couramment limitée soit aux déclarations de variables, soit au boucles `for`:

```c
for (size_t i = 0, j = 10; i != j; i++, j--) { /* ... */ }
```

Dans le cas ci-dessus, il n'est pas possible de séparer les instructions `i++` et `j--` par un point virgule, l'opérateur virgule permet alors de combiner plusieurs instructions en une seule.

Une particularité de cet opérateur est que seule la dernière valeur est retournée :

```c
assert(3 == (1, 2, 3))
```

L'opérateur agit également comme un {ref}`Point de séquence <sequence_point>`, c'est-à-dire que l'ordre des étapes est respecté.

```{eval-rst}
.. exercise:: Opérateur séquentiel

    Que sera-t-il affiché à l'écran ?

    .. code-block:: c

        int i = 0;
        printf("%d", (++i, i++, ++i));
```

## Opérateur sizeof

```{index} sizeof
```

Cet opérateur est *unaire* et retourne la taille en **byte** de la variable ou du type passé en argument. Il n'existe pas de symbole particulier et son usage est très similaire à l'appel d'une fonction :

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

:::{note}
Dans l'exemple ci-dessus, il est possible de s'affranchir de la taille effective du tableau en utilisant une sentinelle. Si le dernier élément du tableau à une valeur particulière et que le reste est initialisé à zéro, il suffit de parcourir le tableau jusqu'à cette valeur :

```c
int32_t array[128] = { [127]=-1 };
int i = 0;
while (array[i] != -1) {
    array[i++] = i * 10;
}
```

Cette écriture reste malgré tout très mauvaise car le tableau de 128 éléments doit être initialisé à priori ce qui mène aux mêmes performances. D'autre part l'histoire racontée par le développeur est moins claire que la première implémentation.
:::

(precedence)=

## Priorité des opérateurs

```{index} précédence
```

```{index} priorité des opérateurs
```

La **précédence** est un anglicisme de *precedence* (priorité) qui concerne la priorité des opérateurs, ou l'ordre dans lequel les opérateurs sont exécutés. Chacun connaît la priorité des quatre opérateurs de base (`+`, `-`, `*`, `/`), mais le C et ses nombreux opérateurs sont bien plus complexes.

La table suivante indique les règles à suivre pour les précédences des opérateurs en C.
La précédence

```{eval-rst}
.. table:: Priorité des opérateurs

    +----------+-----------------------+--------------------------------------------+-----------------+
    | Priorité | Opérateur             | Description                                | Associativité   |
    +==========+=======================+============================================+=================+
    | 1        | ``++``, ``--``        | Postfix incréments/décréments              | Gauche à Droite |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``()``                | Appel de fonction                          |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``[]``                | Indexage des tableaux                      |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``.``                 | Élément d'une structure                    |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``->``                | Élément d'une structure                    |                 |
    +----------+-----------------------+--------------------------------------------+-----------------+
    | 2        | ``++``, ``--``        | Préfixe incréments/décréments              | Droite à Gauche |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``+``, ``-``          | Signe                                      |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``!``, ``~``          | NON logique et NON binaire                 |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``(type)``            | Cast (Transtypage)                         |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``*``                 | Indirection, déréférencement               |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``&``                 | Adresse de...                              |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``sizeof``            | Taille de...                               |                 |
    +----------+-----------------------+--------------------------------------------+-----------------+
    | 3        | ``*``, ``/``, ``%``   | Multiplication, Division, Mod              | Gauche à Droite |
    +----------+-----------------------+--------------------------------------------+                 |
    | 4        | ``+``, ``-``          | Addition, soustraction                     |                 |
    +----------+-----------------------+--------------------------------------------+                 |
    | 5        | ``<<``, ``>>``        | Décalages binaires                         |                 |
    +----------+-----------------------+--------------------------------------------+                 |
    | 6        | ``<``, ``<=``         | Comparaison plus petit que                 |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``>``, ``>=``         | Comparaison plus grand que                 |                 |
    +----------+-----------------------+--------------------------------------------+                 |
    | 7        | ``==``, ``!=``        | Égalité, non égalité                       |                 |
    +----------+-----------------------+--------------------------------------------+                 |
    | 8        | ``&``                 | ET binaire                                 |                 |
    +----------+-----------------------+--------------------------------------------+                 |
    | 9        | ``^``                 | OU exclusif binaire                        |                 |
    +----------+-----------------------+--------------------------------------------+                 |
    | 10       | ``|``                 | OU inclusif binaire                        |                 |
    +----------+-----------------------+--------------------------------------------+                 |
    | 11       | ``&&``                | ET logique                                 |                 |
    +----------+-----------------------+--------------------------------------------+                 |
    | 12       | ``||``                | OU logique                                 |                 |
    +----------+-----------------------+--------------------------------------------+-----------------+
    | 13       | ``?:``                | Opérateur ternaire                         | Droite à Gauche |
    +----------+-----------------------+--------------------------------------------+                 |
    | 14       | ``=``                 | Assignation simple                         |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``+=``, ``-=``        | Assignation par somme/diff                 |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``*=``, ``/=``, ``%=``| Assignation par produit/quotient/modulo    |                 |
    |          +-----------------------+--------------------------------------------+                 |
    |          | ``<<=``, ``>>=``      | Assignation par décalage binaire           |                 |
    +----------+-----------------------+--------------------------------------------+-----------------+
    | 15       | ``,``                 | Virgule                                    | Gauche à Droite |
    +----------+-----------------------+--------------------------------------------+-----------------+
```

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

L'écriture en notation polonaise inversée donnerait alors

```text
34, i, 0, [], ++,  /, 5, 23, +, +, 0xFF, y, <<, &, x, =
```

### Associativité

```{index} associativité
```

L'associativité des opérateurs ([operator associativity](https://en.wikipedia.org/wiki/Operator_associativity)) décrit la manière dont sont évaluées les expressions.

Une associativité à gauche pour l'opérateur `~` signifie que l'expression `a ~ b ~ c` sera évaluée `((a) ~ b) ~ c` alors qu'une associativité à droite sera `a ~ (b ~ (c))`.

Note qu'il ne faut pas confondre l'associativité *évaluée de gauche à droite* qui est une associativité à *gauche*.

### Représentation mémoire des types de données

Nous avons vu au chapitre sur les types de données que les types C
définis par défaut sont représentés en mémoire sur 1, 2, 4 ou 8 octets.
On comprend aisément que plus cette taille est importante, plus on gagne
en précision ou en grandeur représentable. La promotion numérique régit
les conversions effectuées implicitement par le langage C lorsqu'on
convertit une donnée d'un type vers un autre. Cette promotion tend à
conserver le maximum de précision lorsqu'on effectue des calculs entre
types différents (ex : l'addition d'un `int` avec un `double` donne un
type `double`). Voici les règles de base :

- les opérateurs ne peuvent agir que sur des types identiques ;
- quand les types sont différents, il y a conversion automatique vers le type ayant le plus grand pouvoir de représentation ;
- les conversions ne sont faites qu'au fur et à mesure des besoins.

La **promotion** est l'action de promouvoir un type de donnée en un autre type de donnée plus général. On parle de promotion implicite des entiers lorsqu'un type est promu en un type plus grand automatiquement par le compilateur.

## Valeurs gauches

```{index} lvalue
```

Une {index}`valeur gauche` (`lvalue`) est une particularité de certains langages de programmation qui définissent ce qui peut se trouver à gauche d'une affectation. Ainsi dans `x = y`, `x` est une valeur gauche. Néanmoins, l'expression `x = y` est aussi une valeur gauche :

```c
int x, y, z;

x = y = z;    // (1)
(x = y) = z;  // (2)
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

## Optimisation

```{index} -O2
```

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

______________________________________________________________________

```{eval-rst}
.. exercise:: Masque binaire

    Soit les déclarations suivantes :

    .. code-block:: c

        char m, n = 2, d = 0x55, e = 0xAA;

    Représenter en binaire et en hexadécimal la valeur de tous les bits de la variable ``m`` après exécution de chacune des instructions suivantes :

    #. :code:`m = 1 << n;`
    #. :code:`m = ~1 << n;`
    #. :code:`m = ~(1 << n);`
    #. :code:`m = d | (1 << n);`
    #. :code:`m = e | (1 << n);`
    #. :code:`m = d ^ (1 << n);`
    #. :code:`m = e ^ (1 << n);`
    #. :code:`m = d & ~(1 << n);`
    #. :code:`m = e & ~(1 << n);`
```

```{eval-rst}
.. exercise:: Registre système

    Pour programmer les registres 16-bits d'un composant électronique chargé de gérer des sorties tout ou rien, on doit être capable d'effectuer les opérations suivantes :

    - mettre à 1 le bit numéro ``n``, ``n`` étant un entier entre 0 et 15;
    - mettre à 0 le bit numéro ``n``, ``n`` étant un entier entre 0 et 15;
    - inverser le bit numéro ``n``, ``n`` étant un entier entre 0 et 15;

    Pour des questions d'efficacité, ces opérations ne doivent utiliser que les opérateurs bit à bit ou décalage. On appelle ``r0`` la variable désignant le registre en mémoire et ``n`` la variable contenant le numéro du bit à modifier. Écrivez les expressions permettant d'effectuer les opérations demandées.
```

```{eval-rst}
.. exercise:: Recherche d'expressions

    Considérant les déclarations suivantes :

    .. code-block:: c

        float a, b;
        int m, n;

    Traduire en C les expressions mathématiques ci-dessous; pour chacune, proposer plusieurs écritures différentes lorsque c'est possible. Le symbole :math:`\leftarrow` signifie *assignation*

    #. :math:`n \leftarrow 8 \cdot n`
    #. :math:`a \leftarrow a + 2`
    #. :math:`n \leftarrow \left\{\begin{array}{lr}m & : m > 0\\ 0 & : \text{sinon}\end{array}\right.`
    #. :math:`a \leftarrow n`
    #. :math:`n \leftarrow \left\{\begin{array}{lr}0 & : m~\text{pair}\\ 1 & : m~\text{impair}\end{array}\right.`
    #. :math:`n \leftarrow \left\{\begin{array}{lr}1 & : m~\text{pair}\\ 0 & : m~\text{impair}\end{array}\right.`
    #. :math:`m \leftarrow 2\cdot m + 2\cdot n`
    #. :math:`n \leftarrow n + 1`
    #. :math:`a \leftarrow \left\{\begin{array}{lr}-a & : b < 0\\ a & : \text{sinon}\end{array}\right.`
    #. :math:`n \leftarrow \text{la valeur des 4 bits de poids faible de}~n`
```

```{eval-rst}
.. exercise:: Nombres narcissiques

    Un nombre narcissique ou `nombre d'Amstrong <https://fr.wikipedia.org/wiki/Nombre_narcissique>`__ est  un entier naturel ``n`` non nul qui est égal à la somme des puissances ``p``-ièmes de ses chiffres en base dix, où ``p`` désigne le nombre de chiffres de ``n``:

    .. math::

        n=\sum_{k=0}^{p-1}x_k10^k=\sum_{k=0}^{p-1}(x_k)^p\quad\text{avec}\quad x_k\in\{0,\ldots,9\}\quad\text{et}\quad x_{p-1}\ne 0

    Par exemple :

    - ``9`` est un nombre narcissique, car :math:`9 = 9^1 = 9`
    - ``153`` est un nombre narcissique, car :math:`153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153`
    - ``10`` n'est pas un nombre narcissique, car :math:`10 \ne 1^2 + 0^2 = 1`

    Implanter un programme permettant de vérifier si un nombre d'entrées est narcissique ou non. L'exécution est la suivante :

    .. code-block::

        $ ./armstrong 153
        1

        $ ./armstrong 154
        0
```
