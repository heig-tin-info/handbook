# Structures de contrôle

Les structures de contrôle appartiennent aux langages de programmation étant de [paradigme][paradigm] impératif et [structuré](https://fr.wikipedia.org/wiki/Programmation_structur%C3%A9e).

Elles permettent de modifier l'ordre des opérations lors de l'exécution du code. On peut citer les catégories suivantes:

- Les séquences

    - [Les séquences de code][sequence-code] (`;`)
    - [Les blocs de code][sequence-block] (`{}`)
    - [Les points de séquences][sequence-point]

- Les sauts (`jumps`)

    - [Conditionnels][conditional-jumps] (`if`, `switch`)
    - [Inconditionnels][jumps] (`break`, `continue`, `goto`, `return`)

- Les boucles (`loops`)

    - [Boucle itérative][loop-for] sur une valeur connue `for`
    - [Boucle sur condition][loop-while] `while`
    - [Boucle sur condition avec test à la fin][loop-do-while] `do`...`while`

Sans structure de contrôle, un programme se comportera toujours de la même manière et ne pourra pas être sensible à des évènements extérieurs puisque le flux d'exécution ne pourra pas être modifié conditionnellement.

L'intelligence d'un programme réside dans sa capacité à prendre des décisions en fonction de l'état du système et des données qu'il manipule. Les structures de contrôle permettent de définir ces décisions, un peu comme un livre dont vous êtes le héros où chaque choix vous mène à une page différente par un saut.

## Séquences

[](){#sequence-code}

### Séquences de code

En C, chaque instruction est séparée de la suivante par un point-virgule `;` U+003B. On appelle ce caractère le délimiteur d'instruction.

```c
k = 8; k *= 2;
```

Ceci permet d'écrire un programme sur une seule ligne (sauf concernant les directives préprocesseur), mais il est généralement préférable de séparer les instructions sur plusieurs lignes pour améliorer la lisibilité du code.

```c
#include <stdio.h>
int main() { char hello[] = "hello"; printf("%s, world", hello); return 42; }
```

Certaines instructions nécessitent un délimiteur pour être correctement interprétées par le compilateur. Par exemple le `do...while` doit être terminé par un point-virgule :

```c
do {
    printf("Hello, world\n");
} while (0); // <== point virgule obligatoire
```

!!! tip "Le point-virgule grec"

    N'allez pas confondre le point virgule `;` (U+003B) avec le `;` (U+037E), le point d'interrogation grec (ερωτηματικό). Certains farceurs aiment à le remplacer dans le code de camarades ce qui génère naturellement des erreurs de compilation.

[](){#sequence-block}

### Séquences de bloc

Une séquence bloc est une suite d'instructions regroupées en un bloc matérialisé par des accolades `{}`:

```c
{
    double pi = 3.14;
    area = pi * radius * radius;
}
```

Il est possible d'ajouter autant de blocs que vous voulez, mais il est recommandé de ne pas imbriquer les blocs de manière excessive. Un bloc est une unité de code qui peut être traitée comme une seule instruction. Il est possible de déclarer des variables locales dans un bloc, ces variables n'étant accessibles que dans le bloc où elles sont déclarées.

```c
{
    int a = 1;
    {
        int b = 2;
        {
            int c = 3;
        }
        // c n'est pas accessible ici
    }
    // b et c ne sont pas accessibles ici
}
// a, b et c ne sont pas accessibles ici
```

[](){#sequence-point}

### Point de séquence

    On appelle un point de séquence ou [sequence point](https://en.wikipedia.org/wiki/Sequence_point) décrite dans l'annexe du standard C que certains ordres d'évaluation sont garantis.

    Les règles sont les suivantes :

    1. l'appel d'une fonction est effectué après que tous ses arguments ont été évalués;
    2. la fin du premier opérande dans les opérations `&&`, `||`, `?` et `,` qui permet de court-circuiter le calcul dans `a() && b()`. La condition `b()` n'est jamais évaluée si la condition `a()` est valide;
    3. avant et après des actions associées à un formatage d'entrée sortie.

    L'opérateur d'assignation `=` n'est donc pas un point de séquence et l'exécution du code `(a = 2) + a + (a = 2)` est par conséquent indéterminée.

[](){#conditional-jumps}

## Les sauts conditionnels

Les embranchements sont des instructions de prise de décision. Une prise de décision est binaire lorsqu'il y a un choix *vrai* et un choix *faux*, ou multiple lorsque la condition est scalaire. En C il y en a deux types d'embranchements :

1. `if`, `if else`
2. `switch`

On peut représenter ces embranchements par des diagrammes de flux [BPMN](wiki:bpmn) (Business Process Modelling Notation) ou des [structogrammes](wiki:structogramme) NSD (Nassi-Shneiderman):

![Diagrammes BPMN]({assets}/images/branching-diagram.drawio)

Les embranchements s'appuient naturellement sur les séquences puisque chaque branche est composée d'une séquence.

[](){#if}

### `if`

L'instruction `if` traduite par *si* est la plus utilisée. L'exemple suivant illustre un embranchement binaire. Il affiche `odd` si le nombre est impair et `even` s'il est pair :

```c
if (value % 2)
{
    printf("odd\n");
}
else
{
    printf("even\n");
}
```

Notons que les blocs sont facultatifs. L'instruction `if` s'attend à une seule instruction, mais il est possible de regrouper plusieurs instructions dans un bloc `{}`. Il est recommandé de toujours utiliser les blocs pour éviter les erreurs de logique. Néanmoins le code suivant est valide :

```c
if (value % 2)
    printf("odd\n");
else
    printf("even\n");
```

De même que comme des `;` séparent les instructions, on peut aussi écrire:

```c
if (value % 2) printf("odd\n"); else printf("even\n");
```

!!! info

    Dans ce cas précis, l'instruction ternaire est plus élégante :

    ```c
    printf("%s\n", value % 2 ? "odd" : "even");
    ```

Le mot clé `else` est facultatif. Si l'on ne souhaite pas exécuter d'instruction lorsque la condition est fausse, il est possible de ne pas le spécifier.

```c
int a = 42;
int b = 0;

if (b == 0) {
    printf("Division par zéro impossible\n");
    exit(EXIT_FAILURE);
}

printf("a / b = %d\n", a / b);
```

En C il n'y a pas d'instruction `if..else if` comme on peut le trouver dans d'autres langages de programmation (p. ex. Python). Faire suivre une sous condition à `else` est néanmoins possible puisque `if` est une instruction comme une autre la preuve est donnée par la [grammaire][grammar] du langage:

```text
selection_statement
    : IF '(' expression ')' statement
    | IF '(' expression ')' statement ELSE statement
    | SWITCH '(' expression ')' statement
    ;
```

On voit que `if` peut être suivi d'un `statement` lequel peut être suivi d'un `ELSE` et d'un autre `statement`. Ces deux `statement` peuvent par conséquent être un `selection_statement` et donc être imbriqués.

Voici un exemple d'imbriquement de conditions :

```c
if (value < 0) {
    printf("La valeur est négative\n");
}
else {
    if (value == 0) {
        printf("La valeur est nulle\n");
    }
    else {
        printf("La valeur est positive\n");
    }
}
```

Néanmoins, comme il n'y a qu'une instruction `if` après le premier `else`, le bloc peut être omis. En outre, il est correct de faire figurer le `if` sur la même ligne que le `else` :

```c
if (value < 0) {
    printf("La valeur est négative\n");
}
else if (value == 0) {
    printf("La valeur est nulle\n");
}
else {
    printf("La valeur est positive\n");
}
```

Une condition n'est pas nécessairement unique, mais peut-être la concaténation logique de plusieurs conditions séparées :

```c
if((0 < x && x < 10) || (100 < x && x < 110) || (200 < x && x < 210))
{
    printf("La valeur %d est valide", x);
    is_valid = true;
}
else
{
    printf("La valeur %d n'est pas valide", x);
    is_valid = false;
}
```

Remarquons qu'au passage cet exemple peut être simplifié pour diminuer la [complexité cyclomatique](https://fr.wikipedia.org/wiki/Nombre_cyclomatique) :

```c
is_valid = (0 < x && x < 10) || (100 < x && x < 110) || (200 < x && x < 210);

if (is_valid)
{
    printf("La valeur %d est valide", x);
}
else
{
    printf("La valeur %d n'est pas valide", x);
}
```

### Point virgule en trop

Il est courant de placer un point virgule derrière un `if`. Le point virgule correspondant à une instruction vide, c'est cette instruction qui sera exécutée si la condition du test est vraie.

```c
if (z == 0);
printf("z est nul"); // ALWAYS executed
```

### Affectation dans un test

Le test de la valeur d'une variable s'écrit avec l'opérateur d'égalité `==` et non l'opérateur d'affectation `=`. Ici, l'évaluation de la condition vaut la valeur affectée à la variable.

```c
if (z = 0)               // set z to zero !!
    printf("z est nul"); // NEVER executed
```

### L'oubli des accolades

Dans le cas ou vous souhaitez exécuter plusieurs instructions, vous devez impérativement déclarer un bloc d'instructions. Si vous omettez les accolades, seule la première instruction sera exécutée puisque la séquence se termine par un point virgule ou un bloc.

```c
if (z == 0)
    printf("z est nul");
    is_valid = false;  // Ne fait par partie du bloc et s'exécute toujours
```

### Exemple

On peut utiliser des conditions multiples pour déterminer le comportement d'un programme. Par exemple, le programme suivant affiche un message différent en fonction de la valeur de `value` :

```c
if (value % 2)
{
    printf("La valeur est impaire.");
}
else if (value > 500)
{
    printf("La valeur est paire et supérieure à 500.");
}
else if (!(value % 5))
{
    printf("La valeur est paire, inférieur à 500 et divisible par 5.");
}
else
{
    printf("La valeur ne satisfait aucune condition établie.");
}
```

!!! exercise "Et si?"

    Comment se comporte l'exemple suivant :

    ```c
    if (!(i < 8) && !(i > 8))
        printf("i is %d\n", i);
    ```

!!! exercise "D'autres si ?"

    Compte tenu de la déclaration `int i = 8;`, indiquer pour chaque expression si elles impriment ou non `i vaut 8`:

    1. &#32;
       ```c
       if (!(i < 8) && !(i > 8)) then
           printf("i vaut 8\n");
       ```

    2. &#32;
       ```c
       if (!(i < 8) && !(i > 8))
           printf("i vaut 8");
           printf("\n");
       ```

    3. &#32;
       ```c
       if !(i < 8) && !(i > 8)
           printf("i vaut 8\n");
       ```
    4. &#32;
       ```c
       if (!(i < 8) && !(i > 8))
           printf("i vaut 8\n");
       ```

    5. &#32;
       ```c
       if (i = 8) printf("i vaut 8\n");
       ```

    6. &#32;
       ```c
       if (i & (1 << 3)) printf("i vaut 8\n");
       ```

    7. &#32;
       ```c
       if (i ^ 8) printf("i vaut 8\n");
       ```

    8. &#32;
       ```c
       if (i - 8) printf("i vaut 8\n");
       ```

    9. &#32;
       ```c
       if (i == 1 << 3) printf ("i vaut 8\n");
       ```

    10. &#32;
       ```c
       if (!((i < 8) || (i > 8)))
           printf("i vaut 8\n");
       ```

[](){#switch}

### `switch`

L'instruction `switch` n'est pas fondamentale et certains langages de programmation comme Python ne la connaissaient pas. Elle permet essentiellement de simplifier l'écriture pour minimiser les répétitions. On l'utilise lorsque les conditions multiples portent toujours sur la même variable. Par exemple, le code suivant peut être réécrit plus simplement en utilisant un `switch` :

```c
if (defcon == 1)
    printf("Guerre nucléaire imminente");
else if (defcon == 2)
    printf("Prochaine étape, guerre nucléaire");
else if (defcon == 3)
    printf("Accroissement de la préparation des forces");
else if (defcon == 4)
    printf("Mesures de sécurité renforcées et renseignements accrus");
else if (defcon == 5
    printf("Rien à signaler, temps de paix");
else
    printf("ERREUR: Niveau d'alerte DEFCON invalide");
```

Voici l'expression utilisant `switch`. Notez que chaque condition est plus claire :

```c
switch (defcon)
{
    case 1 :
        printf("Guerre nucléaire imminente");
        break;
    case 2 :
        printf("Prochaine étape, guerre nucléaire");
        break;
    case 3 :
        printf("Accroissement de la préparation des forces");
        break;
    case 4 :
        printf("Mesures de sécurité renforcées et renseignements accrus");
        break;
    case 5 :
        printf("Rien à signaler, temps de paix");
        break;
    default :
        printf("ERREUR: Niveau d'alerte DEFCON invalide");
}
```

La valeur par défaut `default` est optionnelle, mais recommandée pour traiter les cas d'erreurs possibles.

La structure d'un `switch` est composée d'une condition `switch (condition)` suivie d'une séquence `{}`. Les instructions de cas `case 42:` sont appelées *labels*. Notez la présence de l'instruction `break` qui est nécessaire pour terminer l'exécution de chaque condition. Par ailleurs, les labels peuvent être chaînés sans instructions intermédiaires ni `break`:

```c
switch (coffee)
{
    case IRISH_COFFEE :
        add_whisky();

    case CAPPUCCINO :
    case MACCHIATO :
        add_milk();

    case ESPRESSO :
    case AMERICANO :
        add_coffee();
        break;

    default :
        printf("ERREUR 418: Type de café inconnu");
}
```

Notons quelques observations :

- La structure `switch` bien qu'elle puisse toujours être remplacée par une structure `if..else if` est généralement plus élégante et plus lisible. Elle évite par ailleurs de répéter la condition plusieurs fois (c.f. {numref}`DRY`).
- Le compilateur est mieux à même d'optimiser un choix multiple lorsque les valeurs scalaires de la condition triées se suivent directement p. ex`{12, 13, 14, 15}`.
- L'ordre des cas d'un `switch` n'a pas d'importance, le compilateur peut même choisir de réordonner les cas pour optimiser l'exécution.

## Les boucles

![Bien choisir sa structure de contrôle]({assets}/images/road-runner.drawio)

Une boucle est une structure itérative permettant de répéter l'exécution d'une séquence. En C il existe trois types de boucles :

1. `#!c for`
2. `#!c while`
3. `#!c do` .. `#!c while`

Elles peuvent être représentées par les diagrammes de flux suivants :

![Aperçu des trois structures de boucles]({assets}/images/for.drawio)

On observe que quelque soit la structure de boucle, une condition de maintien est nécessaire. Cette condition est évaluée avant ou après l'exécution de la séquence. Si la condition est fausse, la séquence est interrompue et le programme continue son exécution.

[](){#loop-while}

### while

La structure `while` répète une séquence **tant que** la condition est vraie.

Dans l'exemple suivant tant que le poids d'un objet déposé sur une balance est inférieur à une valeur constante, une masse est ajoutée et le système patiente avant stabilisation.

```c
while (get_weight() < 420 /* newtons */) {
    add_one_kg();
    wait(5 /* seconds */);
}
```

Séquentiellement une boucle `while` teste la condition, puis exécute la séquence associée.

!!! exercise "Tant que..."

    Comment se comportent ces programmes :

    1. `size_t i=0;while(i<11){i+=2;printf("%i\n",i);}`
    2. `i=11;while(i--){printf("%i\n",i--);}`
    3. `i=12;while(i--){printf("%i\n",--i);}`
    4. `i = 1;while ( i <= 5 ){ printf ( "%i\n", 2 * i++ );}`
    5. `i = 1; while ( i != 9 ) { printf ( "%i\n", i = i + 2 ); }`
    6. `i = 1; while ( i < 9 ) { printf ( "%i\n", i += 2 ); break; }`
    7. `i = 0; while ( i < 10 ) { continue; printf ( "%i\n", i += 2 ); }`

[](){#loop-do-while}

### do..while

De temps en temps il est nécessaire de tester la condition à la sortie de la séquence et non à l'entrée. La boucle `do`...`while` permet justement ceci :

```c
size_t i = 10;

do {
    printf("Veuillez attendre encore %d seconde(s)\r\n", i);
    i -= 1;
} while (i);
```

Contrairement à la boucle `while`, la séquence est ici exécutée **au moins une fois**.

[](){#loop-for}

### for

La boucle `for` est un `while` amélioré qui permet en une ligne de résumer les conditions de la boucle :

```c
for (/* expression 1 */; /* expression 2 */; /* expression 3 */) {
    /* séquence */
}
```

Expression 1

: Exécutée une seule fois à l'entrée dans la boucle, c'est l'expression d'initialisation permettant par exemple de déclarer une variable et de l'initialiser à une valeur particulière.

Expression 2

: Condition de validité (ou de maintien de la boucle). Tant que la condition est vraie, la boucle est exécutée.

Expression 3

: Action de fin de tour. À la fin de l'exécution de la séquence, cette action est exécutée avant le tour suivant. Cette action permet par exemple d'incrémenter une variable.

Voici comment répéter 10x un bloc de code :

```c
for (size_t i = 0; i < 10; i++) {
    something();
}
```

Notons que les portions de `for` sont optionnels et que la structure suivante est strictement identique à la boucle `while`:

```c
for (; get_weight() < 420 ;) {
    /* ... */
}
```

!!! exercise "Pour quelques tours"

    Comment est-ce que ces expressions se comportent-elles ?

    ```c
    int i, k;
    ```

    1. `for (i = 'a'; i < 'd'; printf ("%i\n", ++i));`
    2. `for (i = 'a'; i < 'd'; printf ("%c\n", ++i));`
    3. `for (i = 'a'; i++ < 'd'; printf ("%c\n", i ));`
    4. `for (i = 'a'; i <= 'a' + 25; printf ("%c\n", i++ ));`
    5. `for (i = 1 / 3; i ; printf("%i\n", i++ ));`
    6. `for (i = 0; i != 1 ; printf("%i\n", i += 1 / 3 ));`
    7. `for (i = 12, k = 1; k++ < 5 ; printf("%i\n", i-- ));`
    8. `for (i = 12, k = 1; k++ < 5 ; k++, printf("%i\n", i-- ));`

!!! exercise "Erreur"

    Identifier les deux erreurs dans ce code suivant :

    ```c
    for (size_t = 100; i >= 0; --i)
        printf("%d\n", i);
    ```

!!! exercise "De un à cent"

    Écrivez un programme affichant les entiers de 1 à 100 en employant :

    1. Une boucle `for`
    2. Une boucle `while`
    3. Une boucle `do..while`

    Quelle est la structure de contrôle la plus adaptée à cette situation ?

!!! exercise "Opérateur virgule dans une boucle"

    Expliquez quelle est la fonctionnalité globale du programme ci-dessous :

    ```c
    int main(void) {
        for(size_t i = 0, j = 0; i * i < 1000; i++, j++, j %= 26, printf("\n"))
            printf("%c", 'a' + (char)j);
    }
    ```

    Proposer une meilleure implémentation de ce programme.

### Boucles infinies

Une boucle infinie n'est jamais terminée. On rencontre souvent ce type de boucle dans ce que l'on appelle à tort *La boucle principale* aussi nommée [run loop](https://en.wikipedia.org/wiki/Event_loop). Lorsqu'un programme est exécuté *bare-metal*, c'est à dire directement à même le microcontrôleur et sans système d'exploitation, il est fréquent d'y trouver une fonction `main` telle que :

```c
void main_loop() {
    // Boucle principale
}

int main(void) {
    for (;;)
    {
        main_loop();
    }
}
```

Il y a différentes variantes de boucles infinies :

```c
for (;;) { }

while (true) { }

do { } while (true);
```

Notions que l'expression `while (1)` que l'on rencontre fréquemment dans des exemples est fausse syntaxiquement. Une condition de validité devrait être un booléen, soit vrai, soit faux. Or, la valeur scalaire `1` devrait préalablement être transformée en une valeur booléenne. Il est donc plus juste d'écrire `while (1 == 1)` ou simplement `while (true)`.

On préférera néanmoins l'écriture `for (;;)` qui ne fait pas intervenir de conditions extérieures, car, avant **C99** définir la valeur `true` était à la charge du développeur et on pourrait s'imaginer cette plaisanterie de mauvais goût :

```c
_Bool true = 0;

while (true) { /* ... */ }
```

Lorsque l'on a besoin d'une boucle infinie, il est généralement préférable de permettre au programme de se terminer correctement lorsqu'il est interrompu par le signal **SIGINT** (c. f. {numref}`signals`). On rajoute alors une condition de sortie à la boucle principale :

```c
#include <stdlib.h>
#include <signal.h>
#include <stdbool.h>

static volatile bool is_running = true;

void sigint_handler(int dummy)
{
    is_running = false;
}

int main(void)
{
    signal(SIGINT, sigint_handler);

    while (is_running)
    {
       /* ... */
    }

    return EXIT_SUCCESS;
}
```

[](){#jumps}
## Les sauts

Il existe 4 instructions en C permettant de contrôler le déroulement de
l'exécution d'un programme. Elles déclenchent un saut inconditionnel vers un autre endroit du programme.

- `break` interrompt la structure de contrôle en cours. Elle est valide pour :

  - `while`
  - `do`...\`\`while\`\`
  - `switch`

- `continue`: saute un tour d'exécution dans une boucle
- `goto`: interrompt l'exécution et saute à un label situé ailleurs dans la fonction
- `return`

### `goto`

Il s'agit de l'instruction la plus controversée en C. Cherchez sur internet et les détracteurs sont nombreux, et ils ont partiellement raison, car dans la très vaste majorité des cas où vous pensez avoir besoin de `goto`, une autre solution plus élégante existe.

Néanmoins, il est important de comprendre que `goto` était dans certain langage de programmation comme BASIC, la seule structure de contrôle disponible permettant de faire des sauts. Elle est par ailleurs le reflet du langage machine, car la plupart des processeurs ne connaissent que cette instruction souvent appelée `JUMP`. Il est par conséquent possible d'imiter le comportement de n'importe quelle structure de contrôle si l'on dispose de `if` et de `goto`.

`goto` effectue un saut inconditionnel à un *label* défini en C par un identificateur [](){#identifiers} suivi d'un `:`.

L'un des seuls cas de figure autorisés est celui d'un traitement d'erreur centralisé lorsque de multiples points de retours existent dans une fonction ceci évitant de répéter du code :

```c
#include <time.h>

int parse_message(int message)
{
    struct tm *t = localtime(time(NULL));
    if (t->tm_hour < 7) {
        goto error;
    }

    if (message > 1000) {
        goto error;
    }

    /* ... */

    return 0;

    error:
        printf("ERROR: Une erreur a été commise\n");
        return -1;
}
```

### `continue`

Le mot clé `continue` ne peut exister qu'à l'intérieur d'une boucle. Il permet d'interrompre le cycle en cours et directement passer au cycle suivant.

```c
uint8_t airplane_seat = 100;

while (--airplane_seat)
{
    if (airplane_seat == 13) {
        continue;
    }

    printf("Dans cet avion il y a un siège numéro %d\n", airplane_seat);
}
```

Cette structure est équivalente à l'utilisation d'un goto avec un label placé à la fin de la séquence de boucle, mais promettez-moi que vous n'utiliserez jamais cet exemple :

```c
while (true)
{
    if (condition) {
        goto next;
    }

    /* ... */

    next:
}
```

### `break`

Le mot-clé `break` peut être utilisé dans une boucle ou dans un `switch`. Il permet d'interrompre l'exécution de la boucle ou de la structure `switch` la plus proche. Nous avions déjà évoqué l'utilisation dans un `switch` (c.f. {numref}`switch`).

### `return`

Le mot clé `return` suivi d'une valeur de retour ne peut apparaître que dans une fonction dont le type de retour n'est pas `void`. Ce mot-clé permet de stopper l'exécution d'une fonction et de retourner à son point d'appel.

```c
void unlock(int password)
{
    static tries = 0;

    if (password == 4710 /* MacGuyver: A Retrospective 1986 */) {
        open_door();
        tries = 0;
        return;
    }

    if (tries++ == 3)
    {
        alert_security_guards();
    }
}
```

## Exercices de révision

!!! exercise "Faute d'erreur"

    Considérons les déclarations suivantes :

    ```c
    long i = 0;
    double x = 100.0;
    ```

    Indiquer la nature de l'erreur dans les expressions suivantes :

    1.
        ```c
        do
            x = x / 2.0;
            i++;
        while (x > 1.0);
        ```
    2.
        ```c
        if (x = 0)
            printf("0 est interdit !\n");
        ```
    3.
        ```c
        switch(x) {
            case 100 :
                printf("Bravo.\n");
                break;
            default :
                printf("Pas encore.\n");

        }
        ```
    4.
        ```c
        for (i = 0 ; i < 10 ; i++);
            printf("%d\n", i);
        ```
    5.
        ```c
        while i < 100 {
            printf("%d", ++i);
        }
        ```

!!! exercise "Cas appropriés"

    Parmi les cas suivants, quelle structure de contrôle utiliser ?

    1. Test qu'une variable est dans un intervalle donné.
    2. Actions suivant un choix multiple de l'utilisateur
    3. Rechercher un caractère particulier dans une chaîne de caractère
    4. Itérer toutes les valeurs paires sur un intervalle donné
    5. Demander la ligne suivante du télégramme à l'utilisateur jusqu'à `STOP`

    ??? solution

        1. Le cas est circonscrit à un intervalle de valeur donnée, le `if` est approprié :

            ```c
            if (i > min && i < max) { /* ... */ }
            ```

        2. Dans ce cas un `switch` semble le plus approprié

            ```c
            switch(choice) {
                case 0 :
                    /* ... */
                    break;
                case 1 :
                    /* ... */
            }
            ```

        3. À reformuler *tant que le caractère n'est pas trouvé ou que la fin de la chaîne n'est pas atteinte*. On se retrouve donc avec une boucle à deux conditions de sorties.

            ```c
            size_t pos;
            while (pos < strlen(str) && str[pos] != c) {
                pos++;
            }
            if (pos == strlen(str)) {
                // Not found
            } else {
                // Found `c` in `str` at position `pos`
            }
            ```

        4. La boucle `for` semble ici la plus adaptée

            ```c
            for (size_t i = 100; i < 200; i += 2) {
                /* ... */
            }
            ```

        5. Il est nécessaire ici d'assurer au moins un tour de boucle :

            ```c
            const size_t max_line_length = 64;
            char format[32];
            snprintf(format, sizeof(format), "%%%zus", max_line_length - 1);
            unsigned int line = 0;
            char buffer[max_lines][max_line_length];
            do {
                printf("%d. ", line);
            } while (
                scanf(format, buffer[line]) == 1 &&
                strcmp(buffer[line], "STOP") &&
                ++line < max_lines
            );
            ```

!!! exercise "Comptons sur les caractères"

    Un texte est passé à un programme par `stdin`. Comptez le nombre de caractères transmis.

    ```console
    $ echo "hello world" | count-this
    11
    ```

!!! exercise "Esperluette conditionnelle"

    Quel est le problème avec cette ligne de code ?

    ```c
    if (x&mask==bits)
    ```

    ??? solution

        La priorité de l'opérateur unitaire `&` est plus élevée que `==` ce qui se traduit par :

        ```c
        if (x & (mask == bits))
        ```

        Le développeur voulait probablement appliquer le masque à `x` puis le comparer au motif `bits`. La bonne réponse devrait alors être :

        ```c
        if ((x & mask) == bits)
        ```
