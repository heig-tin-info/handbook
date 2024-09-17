---
epigraph:
    text: "Tout problème informatique peut être résolu en introduisant un niveau d'indirection supplémentaire."
    source: David J. Wheeler / Butler Lampson
---

# Structures de contrôle

Les structures de contrôle appartiennent aux langages de programmation impératifs et [structuré](https://fr.wikipedia.org/wiki/Programmation_structur%C3%A9e). Elles permettent de modifier l'ordre des opérations lors de l'exécution du code. On peut citer les catégories suivantes:

Les séquences

: On défini par séquences les instructions qui s'exécutent les unes après les autres. Celles-ci peuvent être jalonnées explicitement par une instruction de fin d'instruction, implicitement par un point de séquence ou regroupé dans un bloc. On peut distinguer trois types de séquences :

    - [les séquences de code][sequence-code] (`;`);
    - [les blocs de code][sequence-block] (`{}`);
    - [les points de séquences][sequence-point].

Les sélections ou sauts

: Il existe des instructions qui permettent de modifier le flux d'exécution du programme, c'est-à-dire de sauter à une autre partie du code. Les sauts conditionnels dépendent d'une condition, tandis que les sauts inconditionnels sont toujours exécutés. On peut distinguer les sauts d’instructions suivantes :

    - [sauts conditionnels][conditional-jumps] (`if`, `switch`);
    - [sauts inconditionnels][jumps] (`break`, `continue`, `goto`, `return`).

Les itérations ou boucles

: Une boucle est une structure de contrôle qui permet de répéter une instruction ou un bloc d'instructions tant qu'une condition est vraie. On peut distinguer les boucles suivantes :

    - [boucles itératives][loop-for] sur une valeur connue `for`;
    - [boucles sur condition][loop-while] `while`;
    - [boucles sur condition avec test à la fin][loop-do-while] `do`...`while`.

Sans structure de contrôle, un programme se comportera toujours de la même manière et ne pourra pas être sensible à des évènements extérieurs puisque le flux d'exécution ne pourra pas être modifié conditionnellement. L'intelligence d'un programme réside donc dans sa capacité à prendre des décisions en fonction de l'état du système et des données qu'il manipule. Les structures de contrôle permettent de définir ces décisions, un peu comme un livre dont vous êtes le héros où chaque choix vous mène à une page différente par un saut.

Historiquement, les premiers langages de programmation ne disposaient pas de structures de contrôle évoluées. Au niveau assembleur on il est possible d'être Turing complet avec deux types de sauts : inconditionnel (`jmp`) et conditionnel `jz` (*jump if zero*: saut si la valeur de la condition est nulle). Avec plus de 100 ans de recul, et des milliers de langages de programmation, la programmation impérative n'a pas beaucoup évoluée. Les structures de contrôle sont restées les mêmes, seules les syntaxes ont évolué. Certains langages comme le Python on même décidé de simplifier certaines structures de contrôle comme le `do...while` qui n'existe pas.

On peut néanmoins citer certaines fonctions d'ordre supérieur en programmation fonctionnelle (p. ex. `map`, `filter`, `reduce`) qui permettent de manipuler des séquences de données sans utiliser de boucles explicites. Ces fonctions sont souvent plus expressives et plus sûres que les boucles traditionnelles, mais elles ne remplacent pas les structures de contrôle classiques et elles n'existent pas en C. Les monades en Haskell sont un autre exemple de structures de contrôle avancées qui permettent de gérer des effets de bord de manière sûre et contrôlée. Des langages comme Kotlin ou JavaScript ont introduit des concepts similaires comme les coroutines ou les promesses pour gérer de manière asynchrone des tâches longues, mais une fois de plus ce sont des concepts qui n'existent pas en C.

## Séquences

En informatique, une **séquence** représente la forme la plus fondamentale de structure de contrôle dans les langages de programmation impératifs. Elle définit un ordre d'exécution linéaire où les instructions sont exécutées les unes après les autres, suivant l'ordre dans lequel elles apparaissent dans le code source. Cette exécution séquentielle est essentielle pour garantir la prévisibilité et la cohérence du comportement d'un programme.

Formellement, une séquence peut être vue comme une composition de plusieurs instructions élémentaires \(S_1; S_2; \dots; S_n\), où chaque instruction \(S_i\) est exécutée après la précédente. Dans ce modèle, le flux de contrôle passe implicitement d'une instruction à la suivante sans interruption, sauf si une structure de contrôle (comme une boucle ou une condition) modifie ce flux.

La notion de séquence est au cœur de la **programmation structurée**, qui préconise l'utilisation de structures de contrôle bien définies (séquences, sélections, itérations) pour améliorer la lisibilité, la maintenabilité et la fiabilité du code. En évitant les sauts non structurés comme le `goto`, les programmes deviennent plus faciles à comprendre et à vérifier formellement.

En pratique, les séquences en code source sont souvent délimitées par des symboles spécifiques ou des conventions syntaxiques du langage utilisé. Par exemple : en C, les instructions sont terminées par un point-virgule `;`, et les blocs de code sont délimités par des accolades `{}`, en Python,  l'indentation définit les blocs de code, et chaque instruction est généralement écrite sur une nouvelle ligne.

Il est important de noter que même si les séquences représentent l'exécution linéaire de code, elles peuvent contenir des appels à des fonctions ou des procédures qui encapsulent elles-mêmes des structures de contrôle plus complexes. Ainsi, la séquence constitue le fondement sur lequel sont bâties les constructions plus élaborées d'un programme.

Au sein d'une même fonction (ou d'un même bloc de code) on retrouve l'ordre séquentiel des instructions :

```c
int main() {
    /* 1 */ int a = 5;
    /* 2 */ int b = 10;
    /* 3 */ int sum = a + b;
    /* 4 */ printf("%d\n", sum);
}
```

[](){#sequence-code}

### Séquences de code

En C, chaque instruction est séparée de la suivante par un point-virgule `;` U+003B. On appelle ce caractère le délimiteur d'instruction. Nous noterons que le retour à la ligne n'est pas un délimiteur d'instruction, mais un séparateur visuel qui permet de rendre le code plus lisible. Il est donc possible d'écrire plusieurs instructions sur une seule ligne :

```c
#include <stdio.h> // doit être sur une seule ligne
int main() { char hello[] = "hello"; printf("%s, world", hello); return 42; }
```

Seuls les directives du préprocesseur (qui commencent par `#`) et les commentaires de lignes (`//`) dépendent du retour à la ligne.

!!! tip "Le point-virgule grec"

    N'allez pas confondre le point virgule `;` (U+003B) avec le `;` (U+037E), le point d'interrogation grec (ερωτηματικό). Certains farceurs aiment à le remplacer dans le code de camarades ce qui génère naturellement des erreurs de compilation.

[](){#sequence-block}

### Séquence bloc

Une séquence bloc ou instruction composée (*compound statement*) est une suite d'instructions regroupées en un bloc matérialisé par des accolades `{}`:

```c
{
    double pi = 3.14;
    area = pi * radius * radius;
}
```

Il est possible d'ajouter autant de blocs que vous voulez, mais il est recommandé de ne pas imbriquer les blocs de manière excessive. Un bloc est une unité de code qui peut être traité comme une seule instruction, mais qui n'est pas terminé par un point-virgule.

Il est possible de déclarer des variables locales dans un bloc, ces variables n'étant accessibles que dans le bloc où elles sont déclarées. L'exemple suivant montre plusieurs variables locales dont la visibilité est limitée à leur bloc respectif :

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

!!! info "Limites de profondeur"

    Le standard C99 §5.2.4.1 impose qu'un compilateur C doit supporter au moins 127 niveaux d'imbrication de blocs, ce qui est emplement suffisant. Cette valeur n'a pas été introduite par hasard, 127 est la valeur maximale d'un entier signé sur 8 bits (`char`) et les ordinateurs ne savent pas manipuler efficacement des types de données plus petits.

    Ceci étant, le nombre d'imbrication de structures conditionnelles est limité à 63, ce qui est déjà beaucoup trop. Si vous avez besoin de plus de 63 niveaux d'imbrication, il est temps de revoir votre conception !

    Notons néanmoins que les compilateurs modernes ne limitent pas le nombre d'imbrication de blocs et de structures conditionnelles.

[](){#sequence-point}

### Point de séquence

### Points de séquence

Un point de séquence, ou [sequence point](https://en.wikipedia.org/wiki/Sequence_point), est une notion définie dans l'annexe du standard C, qui garantit que certains ordres d'évaluation sont respectés lors de l'exécution d'instructions. En d'autres termes, un point de séquence marque un moment où tous les effets secondaires d'expressions précédentes doivent être achevés avant d'entamer l'évaluation d'expressions suivantes.

Les règles relatives aux points de séquence sont les suivantes :

Appel de fonction

: L'évaluation des arguments d'une fonction est entièrement terminée avant l'exécution de cette fonction elle-même. Autrement dit, l'ordre d'évaluation des arguments peut être indéterminé, mais tous les arguments doivent être évalués avant l'appel de la fonction.

Opérateurs conditionnels et logiques

: Les opérateurs `&&`, `||`, `? :`, et `,` introduisent des points de séquence entre leurs opérandes. Par exemple, dans l'expression `a() && b()`, si `a()` retourne `false`, `b()` ne sera jamais évaluée, car le résultat global de l'expression est déterminé sans avoir besoin de calculer `b()`. Ce mécanisme, appelé "court-circuit", optimise le traitement logique.

Entrées-sorties

: Un point de séquence est présent avant et après toute opération d'entrée/sortie (I/O). Cela garantit que les effets liés à ces opérations, comme l'écriture sur un fichier ou l'affichage à l'écran, se produisent dans un ordre prévisible.

Il est essentiel de noter que l'opérateur d'affectation `=` **n'est pas** un point de séquence. Par conséquent, l'évaluation d'une expression telle que `(a = 2) + a + (a = 2)` est indéterminée. Selon l'ordre d'évaluation des sous-expressions, le résultat peut varier, car les modifications de la variable `a` peuvent intervenir de manière imprévisible.

Pour mieux saisir la notion de point de séquence, il est essentiel de comprendre que, lorsqu'un programme en C est compilé, il est traduit en instructions assembleur qui seront ensuite exécutées par le processeur. Le compilateur, afin d'optimiser les performances, peut réordonner certaines instructions ou les paralléliser dans l'unité arithmétique et logique (ALU). Toutefois, ces optimisations peuvent entraîner des comportements indéterminés si elles interfèrent avec l'ordre d'exécution attendu par le programmeur.

Les points de séquence jouent un rôle crucial en imposant des barrières explicites dans le flux d'instructions, garantissant qu'à ces points précis, tous les effets des calculs précédents sont achevés avant de passer à l'évaluation des instructions suivantes. En d'autres termes, ils empêchent le réordonnancement des instructions au-delà d'un point donné, assurant ainsi un comportement prévisible et conforme aux attentes du programmeur.

[](){#loops}

[](){#jumps}

[](){#conditional-jumps}

## Les sauts conditionnels

Les embranchements sont des instructions de contrôle permettant au programme de prendre des décisions en fonction de conditions spécifiques. Une prise de décision est dite **binaire** lorsqu'elle repose sur un choix entre deux alternatives : *vrai* ou *faux*. Elle est dite **multiple** lorsque la condition évalue une variable scalaire, conduisant à plusieurs chemins possibles. En langage C, il existe deux types principaux d'instructions d'embranchement :

1. `if` et `if else` pour les décisions binaires,
2. `switch` pour la sélection parmi plusieurs cas possibles.

Ces types d'embranchements peuvent être représentés visuellement à l'aide de diagrammes de flux, comme les diagrammes BPMN ([Business Process Model and Notation](wiki:bpmn)) ou les [structogrammes NSD](wiki:structogramme) (Nassi-Shneiderman Diagrams). Ces représentations graphiques permettent de modéliser les choix conditionnels de manière intuitive.

Voici un exemple de diagrammes BPMN et NSD illustrant un embranchement binaire :

![Diagrammes BPMN](/assets/images/branching-diagram.drawio)

Les embranchements reposent sur des séquences d'instructions, car chaque branche, qu'elle soit choisie ou non, est elle-même une séquence de commandes à exécuter selon l'évaluation de la condition.

[](){#if}

### `if`

L'instruction `if` traduite par *si* est de loin la plus utilisée. L'exemple suivant illustre un embranchement binaire. Il affiche `odd` si le nombre est impair et `even` s'il est pair :

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

Notons que les blocs sont facultatifs. L'instruction `if` s'attend à une instruction ou une instruction composée. Il est recommandé de toujours utiliser les blocs pour éviter les erreurs de logique. Néanmoins le code suivant est parfaitement valide :

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

Dans certaines normes pour le médical ou l'aéronautique, comme [MISRA](wiki:misra), l'absence d'accollades est interdite pour éviter les erreurs de logique. C'est généralement une bonne pratique à suivre sauf lorsque la lisibilité du code est améliorée par l'absence d'accollades.

!!! info

    Dans l'exemple ci-dessus, l'instruction ternaire est plus élégante :

    ```c
    printf("%s\n", value % 2 ? "odd" : "even");
    ```

Le mot clé `else` est facultatif. Si l'on ne souhaite pas exécuter d'instruction lorsque la condition est fausse, il est possible de ne pas la spécifier.

```c
int a = 42;
int b = 0;

if (b == 0) {
    printf("Division par zéro impossible\n");
    exit(EXIT_FAILURE);
}

printf("a / b = %d\n", a / b);
```

En C il n'y a pas d'instruction `if..else if` comme on peut le trouver dans d'autres langages de programmation (p. ex. Python avec `elif`). Faire suivre une sous condition à `else` est néanmoins possible puisque `if` est une instruction comme une autre la preuve est donnée par la [grammaire][grammar] du langage qui détermine qu'une instruction de sélection (`selection_statement`), qui est une instruction (`statement`), peut être suivie d'une autre instruction, et donc d'une autre instruction de sélection.

```text
selection_statement
    : IF '(' expression ')' statement
    | IF '(' expression ')' statement ELSE statement
    | SWITCH '(' expression ')' statement
    ;
```

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

Une condition n'est pas nécessairement unique, elle peut-être la concaténation logique de plusieurs conditions séparées :

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

Remarquons que cet exemple peut être simplifié pour diminuer la [complexité cyclomatique](https://fr.wikipedia.org/wiki/Nombre_cyclomatique) :

```c
bool is_valid = (0 < x && x < 10) ||
                (100 < x && x < 110) ||
                (200 < x && x < 210);

if (is_valid) {
    printf("La valeur %d est valide", x);
}
else {
    printf("La valeur %d n'est pas valide", x);
}
```

!!! info "Allman, Stroustrup ou K&R ?"

    Il existe plusieurs conventions de style pour écrire les blocs de code. Les plus connues sont les styles Allman, Stroustrup et K&R. Le style Allman place les accolades sur des lignes séparées, le style Stroustrup les place sur la même ligne que l'instruction de contrôle, et le style K&R les place sur la même ligne que l'instruction de contrôle mais avec un décalage.

    Chacun de ces styles a ses partisans et ses détracteurs, et il est important de choisir un style cohérent pour un projet donné.

    Le style de codage est prisé par les managers qui ne savent pas programmer, ils ont appris à repérer les incohérences de style et pense qu'il s'agit d'un indicateur de qualité du code. C'est un peu comme si un chef cuisinier jugeait la qualité d'un plat à la couleur de l'assiette. Peu importe la couleur de l'assiette, ce qui compte c'est le goût du plat. Néanmoins un restaurant qui n'aurait pas de cohérence dans la couleur de ses assiettes pourrait être perçu comme négligé.

!!! bug "Point virgule en trop"

    Il peut arriver par reflexe d'ajouter un point virgule derrière un `if` qui a pour effet de terminer prématurément le bloc. Par exemple :

    ```c
    if (z == 0);
    printf("z est nul"); // ALWAYS executed
    ```

    C'est une erreur classique qui peut être difficile à repérer.

!!! bug "Affectation dans un test"

    Le test de la valeur d'une variable s'écrit avec l'opérateur d'égalité `==` et non l'opérateur d'affectation `=`. Ici, l'évaluation de la condition vaut la valeur affectée à la variable.

    ```c
    if (z = 0)               // set z to zero !!
        printf("z est nul"); // NEVER executed
    ```

!!! bug "L'oubli des accolades"

    Dans le cas ou vous souhaitez exécuter plusieurs instructions, vous devez impérativement déclarer un bloc d'instructions. Si vous omettez les accolades, seule la première instruction sera exécutée puisque la séquence se termine par un point virgule ou un bloc.

    ```c
    if (z == 0)
        printf("z est nul");
        is_valid = false;  // Ne fait par partie du bloc et s'exécute toujours
    ```

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

L'instruction `switch` n'est pas fondamentale et certains langages de programmation ne la définissent pas. Elle permet essentiellement de simplifier l'écriture pour minimiser les répétitions. On l'utilise lorsque les conditions multiples portent toujours sur la même variable. Par exemple, le code suivant peut être réécrit plus simplement en utilisant un `switch` :

![Switch Case BPMN](/assets/images/switch-case.drawio)

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

Voici la même séquence utilisant `switch`. Notez que chaque condition est plus claire :

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

La structure d'un `switch` est composée d'une condition `switch (condition)` suivie d'une séquence `{}`. Les instructions de cas `case 42:` sont appelées étiquettes (*labels*). Notez la présence de l'instruction `break` qui est nécessaire pour terminer l'exécution de chaque condition. Par ailleurs, les labels peuvent être chaînés sans instructions intermédiaires ni `break`:

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

Notons que le compilateur est capable d'optimiser les `switch` en fonction des valeurs des étiquettes. Il n'est pas nécessaire que les étiquettes soient triées, car le compilateur peut réordonner les cas pour optimiser l'exécution. Néanmoins des étiquettes à progression logique p. ex. `{12, 13, 14, 15}` sont plus efficaces que des étiquettes aléatoires p. ex. `{1, 109, 9, 42}`.

La construction d'une étiquette `case` implique une constante littérale. Il n'est pas possible d'utiliser une expression ou une variable. En outre, il ne peut y avoir qu'une seule étiquette par ligne, car cette dernière doit être située après un retour à la ligne. Voici un exemple permettant de déterminer le nombre de jours dans un mois :

```c
int ndays = -1;
switch (month) {
    case 1:  // JAN
    case 3:  // MAR
    case 5:  // MAY
    case 7:  // JUL
    case 8:  // AUG
    case 10: // OCT
    case 12: // DEC
        ndays = 31;
        break;
    case 4:  // APR
    case 6:  // JUN
    case 9:  // SEP
    case 11: // NOV
        ndays = 30;
        break;
    case 2:  // FEB
        if (year % 400 == 0)
            ndays = 29;
        else if (year % 100 == 0)
            ndays = 28;
        else if (year % 4 == 0)
            ndays = 29;
        else
            ndays = 28;
        break;
    default:
        // Erreur : mois invalide
}
```

#### Déclaration de variables

Il faut comprendre que la structure `switch` est un peu particulière. Le `switch` agit comme un bloc, la déclaration de variable est possible à n'importe quel endroit du bloc, mais toutes les lignes de ce bloc ne seront pas exécutées puisque le `switch` utilisera les labels pour sauter à la bonne instruction. Considérons l'exemple suivant :

```c
int main(int argc) {
   switch (argc) {
      int i = 23;
      case 1:
         int j = 42;
         printf("0. %d\n", i + j);
         break;
      case 2:
         int j = 23;
         printf("1. %d\n", i + j);
         break;
   }
}
```

À la compilation on notera l'erreur suivante:

```text
test.c: In function ‘main’:
test.c:5:11: warning: statement will never be executed [-Wswitch-unreachable]
    5 |       int i = 23;
      |           ^
```

En effet, cette instruction se trouve avant le premier label `case` et ne sera donc jamais exécuté. La variable est belle et bien déclarée, mais elle ne sera pas initialisée.

En outre, la déclaration de `j = 23` pose également problème, l'erreur de compilation suivante apparaît:

```text
test.c: In function ‘main’:
test.c:11:14: error: redefinition of ‘j’
   11 |          int j = 23;
      |              ^
test.c:7:14: note: previous definition of ‘j’ with type ‘int’
    7 |          int j = 42;
      |            ^
```

Vous savez qu'il n'est pas possible de redéclarer une variable déjà existante dans le même bloc. La solution à ce problème est de déclarer les variables propres à un cas dans un bloc séparé. Notez que la variable `k` n'étant utilisée qu'une fois, elle peut être dans le contexte global du `switch` mais situé après le premier label `case`. En pratique, n'essayez pas de jouer avec les limites de la syntaxe, cela ne fera que rendre votre code plus difficile à lire et à maintenir.

```c
#include <stdio.h>

int main(int argc) {
   switch (argc) {
      case 1:
         int k = 10;
         {
            int i = 23;
            int j = 42;
            printf("0. %d\n", i + j + k);
            break;
         }
      case 2: {
         int i = 23;
         int j = 23;
         printf("1. %d\n", i + j);
         break;
      }
   }
}
```

#### Imbrication

Il est possible d'imbriquer différents niveaux dans un switch :

```c
switch(a) {
    case 100:
        switch(b) {
            case 200:
                printf("a=100, b=200\n");
                break;
            case 300:
                printf("a=100, b=300\n");
                break;
        }
        break;
}
```

#### Appareil de Duff

Le [Duff's device](https://en.wikipedia.org/wiki/Duff%27s_device) est une technique d'optimisation assez originale en langage C, qui permet de dérouler une boucle de manière partiellement manuelle, dans le but de gagner en performance, notamment sur des architectures matérielles plus anciennes. Il a été inventé par Tom Duff en 1983 lorsqu'il travaillait chez Lucasfilm.

L'objectif du Duff's device est de dérouler manuellement une boucle afin de réduire le nombre d'itérations et d'optimiser l'exécution, notamment dans les situations où le coût d'un saut conditionnel dans une boucle pouvait être élevé. Cette optimisation est souvent appelée unrolling, où plusieurs itérations de la boucle sont "fusionnées" en une seule.

La particularité du Duff's device est qu'il combine à la fois une structure de boucle `while` et un `switch` de manière surprenante et astucieuse. Voici à quoi ressemble le code original :

```c
register int count = (n + 7) / 8;  // Nombre d'itérations par paquet de 8
register short *to = dest;
register short *from = src;

switch (n % 8) {  // Détermine le point d'entrée initial dans la boucle
    case 0: do { *to = *from++;
    case 7:      *to = *from++;
    case 6:      *to = *from++;
    case 5:      *to = *from++;
    case 4:      *to = *from++;
    case 3:      *to = *from++;
    case 2:      *to = *from++;
    case 1:      *to = *from++;
            } while (--count > 0);
}
```

#### Résumé des points clés

- La structure `switch` bien qu'elle puisse toujours être remplacée par une structure `if..else if` est généralement plus élégante et plus lisible. Elle évite par ailleurs de répéter la condition plusieurs fois (c.f. [DRY][dry]).
- Le compilateur est mieux à même d'optimiser un choix multiple lorsque les valeurs scalaires de la condition triées se suivent directement p. ex. `{12, 13, 14, 15}`.
- L'ordre des cas d'un `switch` n'a pas d'importance, le compilateur peut même choisir de réordonner les cas pour optimiser l'exécution.
- Les étiquettes `case` ne peuvent être que des constantes littérales, il n'est pas possible d'utiliser des expressions ou des variables.
- Les étiquettes `case` doivent être séparées par un retour à la ligne, il n'est pas possible d'avoir plusieurs étiquettes sur une même ligne.
- Il est possible de chaîner les étiquettes sans `break` pour exécuter plusieurs instructions.


[](){#loops}
## Les boucles

![Bien choisir sa structure de contrôle](/assets/images/road-runner.drawio)

Une boucle est une structure itérative permettant de répéter l'exécution d'une séquence. En C il existe trois types de boucles :

1. `#!c for`
2. `#!c while`
3. `#!c do` .. `#!c while`

Elles peuvent être représentées par les diagrammes de flux suivants :

![Aperçu des trois structures de boucles](/assets/images/for.drawio)

On observe que quelque soit la structure de boucle, une **condition de maintien** est nécessaire. Cette condition est évaluée avant ou après l'exécution de la séquence. Si la condition est fausse, la séquence est interrompue et le programme continue son exécution.

[](){#loop-while}

### while

La structure `while` répète une séquence **tant que** la condition est vraie. Dans l'exemple suivant, tant que le poids d'un objet déposé sur une balance est inférieur à une valeur constante, une masse est ajoutée et le système patiente avant stabilisation.

```c
while (get_weight() < 420 /* newtons */) {
    add_one_kg();
    wait(5 /* seconds */);
}
```

Séquentiellement une boucle `while` teste la condition, puis exécute la séquence associée.

!!! exercise "Tant que..."

    Comment se comportent ces programmes ?

    1. `#!c size_t i=0; while(i<11) { i+=2; printf("%i\n",i); }`
    2. `#!c i = 11; while(i--){ printf("%i\n",i--); }`
    3. `#!c i = 12; while(i--){ printf("%i\n",--i); }`
    4. `#!c i = 1; while ( i <= 5 ){ printf ( "%i\n", 2 * i++ );}`
    5. `#!c i = 1; while ( i != 9 ) { printf ( "%i\n", i = i + 2 ); }`
    6. `#!c i = 1; while ( i < 9 ) { printf ( "%i\n", i += 2 ); break; }`
    7. `#!c i = 0; while ( i < 10 ) { continue; printf ( "%i\n", i += 2 ); }`

[](){#loop-do-while}

On utilise une boucle `while` lorsque le nombre d'itérations n'est pas connu à l'avance. Si la séquence doit être exécutée au moins une fois, on utilise une boucle `do`...`while`.

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

Notez ci-dessus la présence d'un `;` après le `while`. La structure `do`...`while` est un peu particulière, car elle est la seule structure de contrôle à se terminer par un point-virgule.

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

    1. `#!c for (i = 'a'; i < 'd'; printf ("%i\n", ++i));`
    2. `#!c for (i = 'a'; i < 'd'; printf ("%c\n", ++i));`
    3. `#!c for (i = 'a'; i++ < 'd'; printf ("%c\n", i ));`
    4. `#!c for (i = 'a'; i <= 'a' + 25; printf ("%c\n", i++ ));`
    5. `#!c for (i = 1 / 3; i ; printf("%i\n", i++ ));`
    6. `#!c for (i = 0; i != 1 ; printf("%i\n", i += 1 / 3 ));`
    7. `#!c for (i = 12, k = 1; k++ < 5 ; printf("%i\n", i-- ));`
    8. `#!c for (i = 12, k = 1; k++ < 5 ; k++, printf("%i\n", i-- ));`

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

L'opérateur `,` est un opérateur de séquence qui permet de séparer des expressions. Il est souvent utilisé dans les boucles `for` pour exécuter plusieurs instructions dans les différentes parties de la boucle. Par exemple pour définir deux variables `i` et `j` dans la partie d'initialisation de la boucle. Voici par exemple comment afficher les lettres de l'alphabet en alternance `z-a y-b x-c`... :

```c
for (char i = 'z', j = 'a'; i > j; i--, j++) {
    printf("%c-%c ", i, j);
}
```

Le programme affiche :

```text
z-a y-b x-c w-d v-e u-f t-g s-h r-i q-j p-k o-l n-m
```

!!! bug "Variable d'induction non signée"

    Il est recommandé d'utiliser des variables d'induction signées pour les boucles `for` afin d'éviter des erreurs de logique. En effet, si vous utilisez une variable d'induction non signée et que vous la décrémentez, vous risquez de créer une boucle infinie :

    ```c
    for (size_t i = 10; i >= 0; i--) {
        printf("%d\n", i);
    }
    ```

    Dans cet exemple, `i` est une variable non signée de type `size_t`. Lorsque `i` atteint 0, la condition `i >= 0` est toujours vraie, car `size_t` est un type non signé et ne peut pas être négatif. Par conséquent, la boucle ne se termine jamais et entraîne un débordement de la variable `i`.

    En pratique on utilisera simplement un `int` pour les variables d'induction néanmoins pour une grande portabilité on utilisera `int_fast32_t` ou `int_fast64_t` pour garantir une taille de variable optimale.

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

Notions que l'expression `while (1)` que l'on rencontre fréquemment dans des exemples n'est pas syntaxiquement exacte. Une condition de validité devrait être un booléen, soit vrai, soit faux. Or, la valeur scalaire `1` devrait préalablement être transformée en une valeur booléenne. Il est donc plus juste d'écrire `while (1 == 1)` ou simplement `while (true)`. D'ailleurs pourquoi utiliser `1` et non pas `42` ? Moi j'aime bien `while (42)`, c'est plus fun...

Certains développeurs préfèrent l'écriture `for (;;)` qui ne fait pas intervenir de conditions extérieures ou de valeurs bulgares, car, avant **C99** définir la valeur `true` était à la charge du développeur et on pourrait s'imaginer cette plaisanterie de mauvais goût :

```c
_Bool true = 0;

while (true) { /* ... */ }
```

Lorsque l'on a besoin d'une boucle infinie, il est généralement préférable de permettre au programme de se terminer correctement lorsqu'il est interrompu par le signal **SIGINT** (c. f. [signals][signals]). On rajoute alors une condition de sortie à la boucle principale :

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

`break`

: Cette instruction nterrompt la structure de contrôle en cours. Elle est valide pour `while`, `do`...`while`, `for` et `switch`.

`continue`

: Cette instruction interrompt le cycle en cours et passe directement au cycle suivant. Elle est valide pour `while`, `do`...`while` et `for`.

`goto`

: La redoutée instruction `goto` interrompt l'exécution et saute à un label situé ailleurs dans la même fonction.

`return`

: Cette instruction interrompt l'exécution de la fonction en cours et retourne à son point d'appel.

### `goto`

Il s'agit de l'instruction la plus controversée en C. Cherchez sur internet et les détracteurs sont nombreux, et ils ont partiellement raison, car dans la très vaste majorité des cas où vous pensez avoir besoin de `goto`, une autre solution plus élégante existe.

Néanmoins, il est important de comprendre que `goto` était dans certains langages de programmation comme BASIC, la seule structure de contrôle disponible permettant de faire des sauts. Elle est par ailleurs le reflet du langage machine, car la plupart des processeurs ne connaissent que cette instruction souvent appelée `JUMP`. Il est par conséquent possible d'imiter le comportement de n'importe quelle structure de contrôle si l'on dispose de `if` et de `goto`.

`goto` effectue un saut inconditionnel à un *label* défini en C par un [identificateur][identifier] suivi d'un `:`.

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

Le mot-clé `break` peut être utilisé dans une boucle ou dans un `switch`. Il permet d'interrompre l'exécution de la boucle ou de la structure `switch` la plus proche. Nous avions déjà évoqué l'utilisation dans un `switch` (c.f. [switch][switch]).

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
