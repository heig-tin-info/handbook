---
epigraph:
    text: "Le problème fondamental de la communication est celui de reproduire en un point, soit exactement, soit approximativement, un message sélectionné à un autre point."
    source: Claude Shannon
---

# Entrées Sorties

Un programme informatique se compose d'entrées (`stdin`) et de sorties (`stdout` et `stderr`).

Pour faciliter la vie du programmeur, les bibliothèques standard offrent toute une panoplie de fonctions pour formater les sorties et interpréter les entrées.

Les fonctions phares sont `printf` pour le formatage de chaîne de caractères et `scanf` pour la lecture de chaînes de caractères. Ces dernières fonctions se déclinent en plusieurs variantes que nous verrons plus tard. La liste citée est non exhaustive, mais largement documentée ici: [`<stdio.h>`](http://man7.org/linux/man-pages/man3/stdio.3.html).

Les fonctions que nous allons aborder dans ce chapitre sont données par la table suivante. Pour davantage de fonctions, vous pouvez vous rendre au chapitre traitant de la bibliothèque standard [stdio][libc-stdio].

Table: Fonctions d'entrées/sorties principales

| Fonction           | Type   | Description                                                    |
| ------------------ | ------ | -------------------------------------------------------------- |
| [putchar][putchar] | Sortie | Écrit un caractère sur la sortie standard                      |
| [puts][puts]       | Sortie | Écrit une chaîne de caractères sur la sortie standard          |
| [printf][printf]   | Sortie | Écrit une chaîne de caractères formatée sur la sortie standard |
| [getchar][getchar] | Entrée | Lit un caractère sur l'entrée standard                         |
| [gets][gets]       | Entrée | Lit une chaîne de caractères sur l'entrée standard             |
| [scanf][scanf]     | Entrée | Lit une chaîne de caractères formatée sur l'entrée standard    |

## Sorties non formatées

Ces fonctions sont très basiques et permettent d'écrire des caractères ou des chaînes de caractères sur la sortie standard.

[](){#putchar}

### Putchar

Cette fonction prend en paramètre un **seul** caractère et l'écrit sur la sortie standard. Elle est définie dans la bibliothèque `stdio.h`.

```c
#include <stdio.h>

int main() {
    putchar('H');
    putchar('e');
    putchar('l');
    putchar('l');
    putchar('o');
    putchar('\n');
}
```

!!! warning

    Attention à utiliser des apostrophes simples `'` pour les caractères. Si vous utilisez des guillemets doubles `"` vous obtiendrez une erreur de compilation.

On sait que les caractères sont des entiers, donc on peut écrire `putchar(65)` pour écrire le caractère `A`. Donc le programme suivant écrit la même chose que le précédent :

```c
#include <stdio.h>

int main() {
    putchar(72);
    putchar(101);
    putchar(108);
    putchar(108);
    putchar(111);
    putchar('\n');
}
```

[](){#puts}

### Puts

La fonction `puts` est une fonction de la bibliothèque standard C qui permet d'écrire une chaîne de caractères sur la sortie standard. Notons qu'elle ajoute automatiquement un retour à la ligne à la fin de la chaîne.

```c
#include <stdio.h>

int main() {
    puts("hello, world"); // Un retour à la ligne est ajouté automatiquement
}
```

Notez ici qu'on utilise des guillemets doubles `"` pour les chaînes de caractères.



## Sorties formatées

Convertir un nombre en une chaîne de caractères n'est pas trivial. Prenons l'exemple de la valeur `123`. Il faut pour cela diviser itérativement le nombre par 10 et calculer le reste :

```text
Etape  Opération  Resultat  Reste
-----  ---------  --------  -----
1      123 / 10   12        3
2      12 / 10    1         2
3      1 / 10     0         1
```

Comme on ne sait pas à priori combien de caractères on aura, et que ces caractères sont fournis depuis le chiffre le moins significatif, il faudra inverser la chaîne de caractères produite.

Voici un exemple possible d'implémentation :

```c
--8<-- "docs/assets/src/iota.c"
```

Cette implémentation pourrait être utilisée de la façon suivante :

```c
#include <stdlib.h>

int main(void)
{
    int num = 123;
    char buffer[10];

    itoa(num, buffer);
}
```

[](){#functionprintf}

### Printf

Vous conviendrez que devoir manuellement convertir chaque valeur n'est pas des plus pratique, c'est pourquoi `printf` rend l'opération bien plus aisée en utilisant des marques substitutives (*placeholder*). Ces spécifié débutent par le caractère `%` suivi du formatage que l'on veut appliquer à une variable passée en paramètres. L'exemple suivant utilise `%d` pour formater un entier non signé.

```c
#include <stdio.h>

int main()
{
    int32_t earth_perimeter = 40075;
    printf("La circonférence de la terre vaut vaut %d km", earth_perimeter);
}
```

Le standard C défini le prototype de `printf` comme étant :

```c
int printf(const char *restrict format, ...);
```

Il définit que la fonction `printf` prend en paramètre un format suivi de `...`. La fonction `printf` comme toutes celles de la même catégorie sont dites [variadiques](https://fr.wikipedia.org/wiki/Fonction_variadique#C), c'est-à-dire qu'elles peuvent prendre un nombre variable d'arguments. Il y aura autant d'arguments additionnels que de marqueurs utilisés dans le format. Ainsi le format `"Mes nombres préférés sont %d et %d, mais surtout %s"` demandera trois paramètres additionnels :

La fonction retourne le nombre de caractères formatés ou `-1` en cas d'erreur.

La construction d'un marqueur est loin d'être simple, mais heureusement on n'a pas besoin de tout connaître et la page Wikipédia [printf format string](https://en.wikipedia.org/wiki/Printf_format_string) est d'une grande aide. Le format de construction est le suivant :

```c
%[parameter][flags][width][.precision][length]type
```

`parameter` (optionnel)

: Numéro de paramètre à utiliser

`flags` (optionnel)

: Modificateurs: préfixe, signe plus, alignement à gauche ...

`width` (optionnel)

: Nombre **minimum** de caractères à utiliser pour l'affichage de la sortie.

`.precision` (optionnel)

: Nombre **minimum** de caractères affichés à droite de la virgule. Essentiellement, valide pour les nombres à virgule flottante.

`length` (optionnel)

: Longueur en mémoire. Indique la longueur de la représentation binaire.

`type`

: Type de formatage souhaité

![Formatage d'un marqueur](/assets/images/formats.drawio)

Voici quelques exemples :

Table: Exemple de formatage avec printf

| Exemple                            | Sortie      | Taille |
| ---------------------------------- | ----------- | ------ |
| `#!c printf("%c", 'c')`            | `c`         | 1      |
| `#!c printf("%d", 1242)`           | `1242`      | 4      |
| `#!c printf("%10d", 42)`           | `       42` | 10     |
| `#!c printf("%07d", 42)`           | `0000042`   | 7      |
| `#!c printf("%+-5dfr", 23)`        | `+23   fr`  | 6      |
| `#!c printf("%5.3f", 314.15)`      | `314.100`   | 7      |
| `#!c printf("%*.*f", 4, 2, 102.1)` | `102.10`    | 7      |
| `#!c printf("%8x", 57005)`         | `    dead`  | 6      |
| `#!c printf("%s", "Hello")`        | `Hello`     | 5      |

On peut s'intéresser à comment `printf` fonctionne en interne. Le premier argument est une chaîne de caractère qui est le motif de formatage. Il peut contenir des caractères spéciaux *placeholder* qui seront interceptés par `printf` pour être remplacés par les arguments suivants après avoir été convertis.

Pour bien comprendre, on peut imaginer une implémentation naïve de `printf` que nous appellerons `my_printf` et qui se basera sur une fonction de sortie non formatée `putchar`.

Cette fonction ne sera capable que de traiter les marqueurs `%d` et `%c`, c'est suffisant pour comprendre le principe. Également, elle prendra toujours deux arguments, donc une valeur à afficher, ceci pour ne pas s'encombrer de la gestion de la liste variable d'arguments qui est un sujet avancé.

```c
void my_printf(char format[], int a) {
    // On parcourt la chaîne de caractères tant que l'on ne rencontre
    // pas le caractère de fin de chaîne
    for (int i = 0; format[i] != '\0'; i++) {
        // Si on rencontre un caractère %, on regarde le caractère suivant
        if (format[i] == '%') {
            // Est-ce que ce caractère est spécial ?
            switch (format[++i]) {
                case 'd': {
                    char str[32] = {0};
                    my_itoa(int a, str);
                    for (int j = 0; str[j] != '\0'; j++) {
                        putchar(str[j]);
                    }
                    break;
                }
                case 'c':
                    // Affiche le caractère en ASCII
                    putchar(a);
                    break;
                default:
                    // On affiche le caractère tel quel,
                    // ce qui permet d'afficher le caractère %
                    putchar(format[i]);
            }
        } else {
            putchar(format[i]);
        }
    }
}
```

!!! exercise

    Indiquez les erreurs dans les instructions suivantes :

    ```c
    printf("%d%d\n", 10, 20);
    printf("%d, %d, %d\n", 10, 20);
    printf("%d, %d, %d, %d\n", 10, 20, 30, 40.);
    printf("%*d, %*d\n", 10, 20);
    printf("%6.2f\n", 10);
    printf("%10s\n", 0x9f);
    ```

## Entrées non formatées

[](){#getchar}
### Getchar

La fonction `getchar` est une fonction de la bibliothèque standard C qui permet de lire un caractère sur l'entrée standard. Elle est définie dans la bibliothèque `stdio.h`. Elle retourne un entier qui correspond à la valeur ASCII du caractère lu.

```c
#include <stdio.h>

int main() {
    int c;
    while ((c = getchar()) != EOF) {
        printf("Caractère lu : %c\n", c);
    }
}
```

Notez ici l'utilisation de `EOF` qui est une constante définie dans la bibliothèque `stdio.h` et qui signifie *End Of File*. Elle est utilisée pour détecter la fin d'un fichier.

Lorsque vous exécutez ce programme, vous pouvez saisir des caractères au clavier. Pour terminer la saisie, vous pouvez utiliser la combinaison de touches ++Ctrl+D++ sur Linux ou ++Ctrl+Z++ sur Windows.

[](){#gets}
### Gets

La fonction `gets` est une fonction de la bibliothèque standard C qui permet de lire une chaîne de caractères sur l'entrée standard. Elle est définie dans la bibliothèque `stdio.h`.

Elle est déconseillée, car elle ne permet pas de spécifier la taille maximale de la chaîne à lire. Cela peut entraîner des débordements de mémoire si un utilisateur saisit une chaîne de caractères trop longue que le programme ne peut pas stocker.

```c
#include <stdio.h>

int main() {
    char str[128];
    gets(str);
    printf("Chaîne lue : %s\n", str);
}
```

!!! warning

    La fonction `gets` est déconseillée. Il est préférable d'utiliser la fonction `fgets` qui permet de spécifier la taille maximale de la chaîne à lire.

## Entrées formatées

Les fonctions de lecture de chaînes de caractères sont plus complexes que les fonctions d'écriture. En effet, il est nécessaire de spécifier le format de la chaîne à lire.

[](){#scanf}

### Scanf

À l'instar de la sortie formatée, il est possible de lire les saisies au clavier ou *parser* une chaîne de caractères, c'est-à-dire faire une [analyse syntaxique](https://fr.wikipedia.org/wiki/Analyse_syntaxique) de son contenu pour en extraire de l'information.

La fonction `scanf` est par exemple utilisée à cette fin :

```c
#include <stdio.h>

int main()
{
    int favorite;

    printf("Quelle est votre nombre favori ? ");
    scanf("%d", &favorite);

    printf("Saviez-vous que votre nombre favori, %d, est %s ?\n",
        favorite,
        favorite % 2 ? "impair" : "pair");
}
```

Cette fonction utilise l'entrée standard `stdin`. Il est donc possible soit d'exécuter ce programme en mode interactif :

```console
$ ./a.out
Quelle est votre nombre favori ? 2
Saviez-vous que votre nombre favori, 2, est pair ?
```

soit d'exécuter ce programme en fournissant le nécessaire à stdin :

```console
$ echo "23" | ./a.out
Quel est votre nombre favori ? Saviez-vous que votre nombre favori, 23, est impair ?
```

On observe ici un comportement différent, car le retour clavier lorsque la touche *enter* est pressée n'est pas transmis au programme, mais c'est le shell qui l'intercepte.

Le format de `scanf` se rapproche de `printf` mais en plus simple. Le [man scanf](https://linux.die.net/man/3/scanf) ou même la page Wikipédia de [scanf](https://en.wikipedia.org/wiki/Scanf_format_string) renseigne sur son format.

Cette fonction tient son origine une nouvelle fois de [ALGOL 68](https://en.wikipedia.org/wiki/ALGOL_68) (`readf`), elle est donc très ancienne.

La compréhension de `scanf` n'est pas évidente et il est utile de se familiariser sur son fonctionnement à l'aide de quelques exemples.

Le programme suivant lit un entier et le place dans la variable `n`. `scanf` retourne le nombre d'assignements réussis. Ici, il n'y a qu'un *placeholder*, on s'attend naturellement à lire `1` si la fonction réussit. Le programme écrit ensuite les nombres dans l'ordre d'apparition.

```c
#include <stdio.h>

int main(void)
{
    int i = 0, n;

    while (scanf("%d", &n) == 1)
        printf("%i\t%d\n", ++i, n);
    return 0;
}
```

Si le code est exécuté avec une suite arbitraire de nombres :

```text
456 123 789     456 12
456 1
    2378
```

il affichera chacun des nombres dans l'ordre d'apparition :

```console
$ cat << EOF | ./a.out
456 123 789     456 12
456 1
    2378
EOF
1       456
2       123
3       789
4       456
5       12
6       456
7       1
8       2378
```

Voyons un exemple plus complexe (c.f. C99 §7.19.6.2-19).

```c
int count;
float quantity;
char units[21], item[21];

do {
    count = scanf("%f%20s de %20s", &quant, units, item);
    scanf("%*[^\n]");
} while (!feof(stdin) && !ferror(stdin));
```

Lorsqu'exécuté avec ce contenu :

```text
2 litres de lait
-12.8degrés Celsius
beaucoup de chance
10.0KG de
poussière
100ergs d’énergie
```

Le programme se déroule comme suit :

```c
quantity = 2; strcpy(units, "litres"); strcpy(item, "lait");
count = 3;

quantity = -12.8; strcpy(units, "degrees");
count = 2; // "C" échoue lors du test de "d" (de)

count = 0; // "b" de "beaucoup" échoue contre "%f" s'attendant à un float

quantity = 10.0; strcpy(units, "KG"); strcpy(item, "poussière");
count = 3;

count = 0; // "100e" échoue contre "%f", car "100e3" serait un nombre valable
count = EOF; // Fin de fichier
```

Dans cet exemple, la boucle `do`... `while` est utilisée, car il n'est pas simplement possible de traiter le cas `while(scanf(...) > 0` puisque l'exemple cherche à montrer les cas particuliers où justement, la capture échoue. Il est nécessaire alors de faire appel à des fonctions de plus bas niveau `feof` pour détecter si la fin du fichier est atteinte, et `ferror` pour détecter une éventuelle erreur sur le flux d'entrée.

La directive `scanf("%*[^\n]");` étant un peu particulière, il peut valoir la peine de s'y attarder un peu. Le *flag* `*`, différent de `printf` indique d'ignorer la capture en cours. L'exemple suivant montre comment ignorer un mot.

```c
#include <assert.h>
#include <stdio.h>

int main(void) {
    int a, b;
    char str[] = "24 kayaks 42";

    sscanf(str, "%d%*s%d", &a, &b);
    assert(a == 24);
    assert(b == 42);
}
```

Ensuite, `[^\n]`. Le marqueur `[`, terminé par `]` cherche à capturer une séquence de caractères parmi une liste de caractères acceptés. Cette syntaxe est inspirée des [expressions régulières](https://fr.wikipedia.org/wiki/Expression_r%C3%A9guli%C3%A8re) très utilisées en informatique. Le caractère `^` à une signification particulière, il indique que l'on cherche à capturer une séquence de caractères parmi une liste de caractères **qui ne sont pas acceptés**. C'est une sorte de négation. Dans le cas présent, cette directive `scanf` cherche à consommer tous les caractères jusqu'à une fin de ligne, car, dans le cas ou la capture échoue à `C` de `Celsius`, le pointeur de fichier est bloqué au caractère `C` et au prochain tour de boucle, `scanf` échouera au même endroit. Cette instruction est donc utilisée pour repartir sur des bases saines en sautant à la prochaine ligne.

!!! exercise "scanf sur des entiers et des réels"

    Considérant les déclarations :

    ```c
    int i, j, k;
    float f;
    ```

    Donnez les valeurs de chacune des variables après exécution. Chaque ligne est indépendante des autres.

    ```c
    i = sscanf("1 12.5", "%d %d, &j, &k);
    sscanf("12.5", "%d %f", &j, %f);
    i = sscanf("123 123", "%d %f", &j, &f);
    i = sscanf("123a 123", "%d %f", &j, &f);
    i = sscanf("%2d%2d%f", &j, &k, &f);
    ```

!!! exercise "Saisie de valeurs"

    Considérant les déclarations suivantes, donner la valeur des variables après l'exécution des instructions données avec les captures associées :

    ```c
    int i = 0, j = 0, n = 0;
    float x = 0;
    ```

    | no  | Expression                              | Entrée          |
    | --- | --------------------------------------- | --------------- |
    | 1   | `#!c n = scanf("%1d%1d", &i, &j);`      | `12\n`          |
    | 2   | `#!c n = scanf("%d%d", &i, &j);`        | `1 , 2\n`       |
    | 3   | `#!c n = scanf("%d%d", &i, &j);`        | `-1   -2\n`     |
    | 4   | `#!c n = scanf("%d%d", &i, &j);`        | `-  1  -  2\n`  |
    | 5   | `#!c n = scanf("%d,%d", &i, &j);`       | `1  ,  2\n`     |
    | 6   | `#!c n = scanf("%d ,%d", &i, &j);`      | `1  ,  2\n`     |
    | 7   | `#!c n = scanf("%4d %2d", &i, &j);`     | `1 234\n`       |
    | 8   | `#!c n = scanf("%4d %2d", &i, &j);`     | `1234567\n`     |
    | 9   | `#!c n = scanf("%d%*d%d", &i, &j);`     | `123 456 789\n` |
    | 10  | `#!c n = scanf("i=%d , j=%d", &i, &j);` | `1 , 2\n`       |
    | 11  | `#!c n = scanf("i=%d , j=%d", &i, &j);` | `i=1, j=2\n`    |
    | 12  | `#!c n = scanf("%d%d", &i, &j);`        | `1.23 4.56\n`   |
    | 13  | `#!c n = scanf("%d.%d", &i, &j);`       | `1.23 4.56\n`   |
    | 14  | `#!c n = scanf("%x%x", &i, &j);`        | `12 2a\n`       |
    | 15  | `#!c n = scanf("%x%x", &i, &j);`        | `0x12 0X2a\n`   |
    | 16  | `#!c n = scanf("%o%o", &i, &j);`        | `12 018\n`      |
    | 17  | `#!c n = scanf("%f", &x);`              | `123\n`         |
    | 18  | `#!c n = scanf("%f", &x);`              | `1.23\n`        |
    | 19  | `#!c n = scanf("%f", &x);`              | `123E4\n`       |
    | 20  | `#!c n = scanf("%e", &x);`              | `12\n`          |

    ??? solution

        | `Q` | `i`      | `j`   | `n`  | Remarque                       |
        | --- | -------- | ----- | ---- | ------------------------------ |
        | 1   | `1`      | `2`   | `2`  |                                |
        | 2   | `1`      | `0`   | `1.` | `j` n'est pas lue car arrêt    |
        |     |          |       |      | prématuré sur `,`              |
        | 3   | `-1`     | `-2`  | `2`  |                                |
        | 4   | `0`      | `0`   | `0.` | `i` n'est pas lue car arrêt    |
        |     |          |       |      | prématuré sur `-`              |
        | 5   | `1`      | `0`   | `1.` |                                |
        | 6   | `1`      | `2`   | `2`  |                                |
        | 7   | `1`      | `23`  | `2`  |                                |
        | 8   | `1234`   | `56`  | `2`  |                                |
        | 9   | `123`    | `789` | `2`  |                                |
        | 10  | `0`      | `0`   | `0`  |                                |
        | 11  | `1`      | `2`   | `2`  |                                |
        | 12  | `1`      | `0`   | `1`  |                                |
        | 13  | `1`      | `23`  | `2`  |                                |
        | 14  | `18`     | `42`  | `2`  |                                |
        | 15  | `10`     | `1`   | `2.` | Le chiffre 8 interdit en octal |
        |     |          |       |      | provoque un arrêt              |
        |     | `x`      | `n`   |      |                                |
        | 16  | `123.`   | `1`   |      |                                |
        | 17  | `1.23`   | `1`   |      |                                |
        | 18  | `1.23E6` | `1`   |      |                                |
        | 19  | `12`     | `1`   |      |                                |

!!! exercise "Chaînes de formats"

    1. Saisir 3 caractères consécutifs dans des variables `i`, `j`, `k`.
    2. Saisir 3 nombres de type float séparés par un point-virgule et un nombre quelconque d'espaces dans des variables `x`, `y` et `z`.
    3. Saisir 3 nombres de type double en affichant avant chaque saisie le nom de la variable et un signe `=`, dans des variables `t`, `u` et `v`.

    ??? solution

        1. Saisir 3 caractères consécutifs dans des variables `i`, `j`, `k`.

            ```c
            scanf("%c%c%c", &i, &j, &k);
            ```

        2. Saisir 3 nombres de type float séparés par un point-virgule et un nombre quelconque d'espaces dans des variables `x`, `y` et `z`.

            ```c
            scanf("%f ;%f ;%f", &x, &y, &z);
            ```

        3. Saisir 3 nombres de type double en affichant avant chaque saisie le nom de la variable et un signe `=`, dans des variables `t`, `u` et `v`.

            ```c
            printf("t="); scanf("%f", &t);
            printf("u="); scanf("%f", &u);
            printf("v="); scanf("%f", &v);
            ```

### Saisie de chaîne de caractères

Lors d'une saisie de chaîne de caractères, il est nécessaire de **toujours** indiquer une taille maximum de chaîne comme `%20s` qui limite la capture à 20 caractères, soit une chaîne de 21 caractères avec son `\0`. Sinon, il y a risque de [fuite mémoire](https://fr.wikipedia.org/wiki/Fuite_de_m%C3%A9moire) :

```c
int main(void) {
    char a[6];
    char b[10] = "Râteau";

    char str[] = "jardinage";
    sscanf(str, "%s", a);

    printf("a. %s\nb. %s\n", a, b);
}
```

```console
$ ./a.out
a. jardinage
b. age
```

Ici la variable b contient `age` alors qu'elle devrait contenir `râteau`. La raison est que le mot capturé `jardinage` est trop long pour la variable `a` qui n'est disposée à stocker que 5 caractères imprimables. Il y a donc dépassement de mémoire et comme vous le constatez, le compilateur ne génère aucune erreur. La bonne méthode est donc de protéger la saisie ici avec `%5s`.

En mémoire, ces deux variables sont adjacentes et naturellement `a[7]` est équivalente à dire *la septième case mémoire à partir du début de \`\`a\`\`*.

```text
     a[6]              b[10]
┞─┬─┬─┬─┬─┬─┦┞─┬─┬─┬─┬─┬─┬─┬─┬─┬─┦
│ │ │ │ │ │ ││R│â│t│e│a│u│ │ │ │ │
└─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
```

### Saisie arbitraire

Comme brièvement évoqué plus haut, il est possible d'utiliser le marqueur `[` pour capturer une séquence de caractères. Imaginons que je souhaite capturer un nombre en [tetrasexagesimal](https://en.wikipedia.org/wiki/Base64) (base 64). Je peux écrire :

```c
char input[] = "Q2hvY29sYXQ";
char output[128];
sscanf(input, "%127[0-9A-Za-z+/]", &output);
```

Dans cet exemple je capture les nombres de 0 à 9 `0-9` (10), les caractères majuscules et minuscules `A-Za-z` (52), ainsi que les caractères `+`, `/` (2), soit 64 caractères. Le buffer d'entrée étant fixé à 128 positions, la saisie est contrainte à 127 caractères imprimables.

!!! exercise "Bugs"

    Parmi les instructions ci-dessous, indiquez celles qui sont correctes et celle qui comporte des erreurs. Pour celles comportant des erreurs, détaillez la nature des anomalies.

    ```c
    short i;
    long j;
    unsigned short u;
    float x;
    double y;
    printf(i);
    scanf(&i);
    printf("%d", &i);
    scanf("%d", &i);
    printf("%d%ld", i, j, u);
    scanf("%d%ld", &i, j);
    printf("%u", &u);
    scanf("%d", &u);
    printf("%f", x);
    scanf("%f", &x);
    printf("%f", y);
    scanf("%f", &y);
    ```

    ??? solution

        ```c
        // Incorrect ! Le premier paramètre de printf doit être la chaîne de format.
        printf(i);

        // Incorrect ! Le premier paramètre de scanf doit être la chaîne de format.
        scanf(&i);

        // Correct, mais surprenant.
        // Cette instruction affichera l’adresse de I, et non pas sa valeur !
        printf("%d", &i);

        // Incorrect. Le paramètre i est de type short, alors que la chaîne de
        // format spécifie un type int. Fonctionnera sur les machines dont le type
        // short et int sont identiques
        scanf("%d", &i);

        // Incorrect, la troisième variable passée en paramètre ne sera pas affichée.
        printf("%d%ld", i, j, u);

        // Incorrect ! Le premier paramètre est de type short alors que int
        // est spécifié dans la chaîne de format.
        // Le deuxième paramètre n’est pas passé par adresse, ce qui va
        // probablement causer une erreur fatale.
        scanf("%d%ld", &i, j);

        // Correct, mais étonnant. Affiche l’adresse de la variable u.
        printf("%u", &u);

        // Incorrect ! Le paramètre est de type unsigned short, alors que
        // la chaîne de format spécifie int. Fonctionnera pour les valeurs
        // positives sur les machines dont le type short et int sont identiques.
        // Pour les valeurs négatives, le résultat sera l’interprétation non
        // signée de la valeur en complément à 2.
        scanf("%d", &u);

        // Correct, mais x est traité comme double.
        printf("%f", x);

        // Correct.
        scanf("%f", &x);

        // Correct ! %f est traité comme double par printf !
        printf("%f", y);

        // Incorrect ! La chaîne de format spécifie float,
        // le paramètre passé est l’adresse d’une variable de type double.
        scanf("%f", &y);
        ```

!!! exercise "Test de saisir correcte"

    Écrivez un programme déclarant des variables réelles `x`, `y` et `z`, permettant de
    saisir leur valeur en une seule instruction, et vérifiant que les 3 valeurs ont bien
    été assignées. Dans le cas contraire, afficher un message du type "données
    invalides".

    ??? solution

        ```c
        int n;
        float x, y, z;
        printf("Donnez les valeurs de x, y et z :");
        n = scanf("%f%f%f", &x, &y, &z);
        if (n != 3)
        printf("Erreur de saisie.\n");
        ```

!!! exercise "Produit scalaire"

    Écrire un programme effectuant les opérations suivantes :

    - Saisir les coordonnées réelles `x1` et `y1` d’un vecteur `v1`.
    - Saisir les coordonnées réelles `x2` et `y2` d’un vecteur `v2`.
    - Calculer le produit scalaire. Afficher un message indiquant si les vecteurs sont orthogonaux ou non.

    ??? solution

        ```c
        #include <stdio.h>
        #include <stdlib.h>

        int main(void)
        {
            float x1, y1
            printf("Coordonnées du vecteur v1 séparées par un \";\" :\n");
            scanf("%f ;%f", &x1, &y1);

            float x2, y2;
            printf("Coordonnées du vecteur v2 séparées par un \";\" :\n");
            scanf("%f ;%f", &x2, &y2);

            float dot_product = x1 * x2 + y1 * y2;
            printf("Produit scalaire : %f\n", dot_product);
            if (dot_product == 0.0)
                printf("Les vecteurs sont orthogonaux.\n");
        }
        ```

        Ce programme risque de ne pas bien détecter l’orthogonalité de certains vecteurs, car le test d’égalité à 0 avec les virgules flottantes pourrait mal fonctionner. En effet, pour deux vecteurs orthogonaux, les erreurs de calcul en virgule flottante pourraient amener à un produit scalaire calculé très proche, mais cependant différent de zéro.
        On peut corriger ce problème en modifiant le test pour vérifier si le produit scalaire est très petit, par exemple compris entre `-0.000001` et `+0.000001`:

        ```c
        if (dot_product >= -1E-6 && dot_product <= 1E-6)
        ```

        Ce qui peut encore s’écrire en utilisant la fonction valeur absolue :

        ```c
        if (fabs(dot_product) <= 1E-6)
        ```

!!! exercise "Crampes de doigts"

    Votre collègue n'a pas cessé de se plaindre de crampes... aux doigts... Il a écrit le programme suivant avant de prendre congé pour se rendre chez son médecin.

    Grâce à votre esprit affuté et votre œil perçant, vous identifiez 13 erreurs. Lesquelles sont-elles ?

    ```text
    #include <std_io.h>
    #jnclude <stdlib.h>
    INT Main()
    {
    int a, sum;
    printf("Addition de 2 entiers a et b.\n");

    printf("a: ")
    scanf("%d", a);

    printf("b: ");
    scanf("%d", &b);

    /* Affichage du résultat
    somme = a - b;
    Printf("%d + %d = %d\n", a, b, sum);

    retturn EXIT_FAILURE;
    }
    }
    ```

    ??? solution

        Une fois la correction effectuée, vous utilisez l'outil de `diff` pour montrer les différences :

        ```diff
        1,3c1,3
        <         #include <stdio.h>
        <         #include <stdlib.h>
        <         int main()
        ---
        >         #include <std_io.h>
        >         #jnclude <stdlib.h>
        >         INT Main()
        5c5
        <         int a, b, sum;
        ---
        >         int a, sum;
        9c9
        <         scanf("%d", &a);
        ---
        >         scanf("%d", a);
        14,16c14,16
        <         /* Affichage du résultat */
        <         sum = a + b;
        <         printf("%d + %d = %d\n", a, b, sum);
        ---
        >         /* Affichage du résultat
        >         somme = a - b;
        >         Printf("%d + %d = %d\n", a, b, sum);
        18c18,19
        <         return EXIT_SUCCESS;
        ---
        >         return EXIT_FAILURE;
        >         }
        ```

!!! exercise "Géométrie affine"

    Considérez le programme suivant :

    ```c
    #include <stdio.h>
    #include <stdlib.h>

    int main(void)
    {
        float a;
        printf("a = ");
        scanf("%f", &a);

        float b;
        printf("b = ");
        scanf("%f", &b);

        float x;
        printf("x = ");
        scanf("%f", &x);

        float y = a * x + b;

        printf("y = %f\n", y);
    }
    ```

    1. À quelle ligne commence l'exécution de ce programme ?
    2. Dans quel ordre s'exécutent les instructions ?
    3. Décrivez ce que fait ce programme étape par étape
    4. Que verra l'utilisateur à l'écran ?
    5. Quelle est l'utilité de ce programme ?

    ??? solution

        1. Ligne 6
        2. C est un langage impératif, l'ordre est séquentiel du haut vers le bas
        3. Les étapes sont les suivantes :

            1. Demande de la valeur de `a` à l'utilisateur
            2. Demande de la valeur de `b` à l'utilisateur
            3. Demande de la valeur de `x` à l'utilisateur
            4. Calcul de l'image affine de `x` (équation de droite)
            5. Affichage du résultat

        4. Que verra l'utilisateur à l'écran ?

            - Il verra `y = 12` pour `a = 2; x = 5; b = 2`

        5. Quelle est l'utilité de ce programme ?

            - Le calcul d'un point d'une droite

!!! exercise "Équation de droite"

    L'exercice précédent souffre de nombreux défauts. Sauriez-vous les identifier et perfectionner l'implémentation de ce programme ?

    ??? solution

        Citons les défauts de ce programme :

        - Le programme ne peut pas être utilisé avec les arguments, uniquement en mode interactif
        - Les invités de dialogue `a = `, `b = ` ne sont pas clair, `a` et `b` sont associés à quoi ?
        - La valeur de retour n'est pas exploitable directement.
        - Le nom des variables utilisé n'est pas clair.
        - Aucune valeur par défaut.

        Une solution possible serait :

        ```c
        --8<-- "docs/assets/src/linear.c"
        ```

!!! exercise "Loi d'Ohm"

    Écrivez un programme demandant deux réels `tension` et `résistance`, et affichez ensuite le `courant`. Prévoir un test pour le cas où la résistance serait nulle.


!!! exercise "Tour Eiffel"

    Considérons le programme suivant :

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    int main()
    {
        printf("Quel angle mesurez-vous en visant le sommet du bâtiment (en degrés): ");
        float angle_degre;
        scanf("%f", &angle_degrees);
        float angle_radian = angle_degrees * M_PI / 45.;

        printf("À quelle distance vous trouvez vous du bâtiment (en mètres): ");
        float distance;
        scanf("%f", &distance);

        float height = distance / tan(angle_radian);
        printf("La hauteur du bâtiment est : %g mètres.\n", height);
    }
    ```

    1. Que fait le programme étape par étape ?
    2. Que verra l'utilisateur à l'écran ?
    3. À quoi sert ce programme ?
    4. Euh, mais ? Ce programme comporte des erreurs, lesquelles ?
    5. Implémentez-le et testez-le.

!!! exercise "Hyperloop"

    [Hyperloop](https://fr.wikipedia.org/wiki/Hyperloop) (aussi orthographié **Hyperl∞p**) est un projet ambitieux d'Elon Musk visant à construire un moyen de transport ultra rapide utilisant des capsules voyageant dans un tube sous vide. Ce projet est analogue à celui étudié en suisse et nommé [Swissmetro](https://fr.wikipedia.org/wiki/Swissmetro), mais abandonné en 2009.

    Néanmoins, les ingénieurs suisses avaient à l'époque écrit un programme pour calculer, compte tenu d'une vitesse donnée, le temps de parcours entre deux villes de Suisse.

    Écrire un programme pour calculer la distance entre deux villes de suisse parmi lesquelles proposées sont :

    - Genève
    - Zürich
    - Bâle
    - Bern
    - St-Galle

    Considérez une accélération de 0.5 g pour le calcul de mouvement, et une vitesse maximale de 1220 km/h.

## Portabilité des formats

Les formats de `scanf` et `printf` sont dépendants de la plateforme. Par exemple, `%d` est un entier signé, `%u` un entier non signé, `%ld` est un entier long signé. Néanmoins ces formats ne sont pas portables, car selon le [modèle de données][datamodel] de la machine, un entier long peut être de 32 bits ou de 64 bits.

Cela n'a pas une grande importance si vous utilisez les types standards (comme `int`, `long`, `short`, `char`), mais si vous utilisez des types spécifiques comme `int32_t`, `int64_t`, `uint32_t`, `uint64_t`, vous devez utiliser les formats spécifiques de la bibliothèque `inttypes.h`. Voici la table de correspondance des formats :

Table: Formats portables

| Type     | Format |
| -------- | ------ |
| int8_t   | PRId8  |
| int16_t  | PRId16 |
| int32_t  | PRId32 |
| int64_t  | PRId64 |
| uint8_t  | PRIu8  |
| uint16_t | PRIu16 |
| uint32_t | PRIu32 |
| uint64_t | PRIu64 |

On peut ajouter des options à ces formats, par exemple pour afficher un entier en hexadécimal, on utilise `%PRIx32` pour un entier 32 bits. Pour la valeur en octal, on utilise `%PRIo32`.

Table: Options des formats portables

| Option | Description |
| ------ | ----------- |
| x      | Hexadécimal |
| o      | Octal       |
| u      | Non signé   |
| d      | Signé       |

L'utilisation est particulière car il faut utiliser la macro `PRI` pour définir le format. Par exemple, pour afficher un entier 32 bits en hexadécimal, on utilise :

```c
#include <inttypes.h>
#include <stdio.h>

int main(void)
{
    int32_t i = 0x12345678;
    printf("i = %" PRIx32 "\n", i);
}
```

!!! exercise "Constantes littérales caractérielles"

    Indiquez si les constantes littérales suivantes sont valides ou invalides.

    /// html | div[class='two-column-list']

    1. `'a'`
    2. `'A'`
    3. `'ab'`
    4. `'\x41'`
    5. `'\041'`
    6. `'\0x41'`
    7. `'\n'`
    8. `'\w'`
    9. `'\t'`
    10. `'\xp2'`
    11. `"abcdef"`
    12. `"\abc\ndef"`
    13. `"\'\"\\"`
    14. `"hello \world!\n"`

    ///

!!! exercise "Chaînes de formatage"

    Pour les instructions ci-dessous, indiquer quel est l'affichage obtenu.

    ```c
    char a = 'a';
    short sh1 = 5;
    float f1 = 7.0f;
    int i1 = 7, i2 = 'a';
    ```

    1. `#!c printf("Next char: %c.\n", a + 1);`
    2. `#!c printf("Char: %3c.\n", a);`
    3. `#!c printf("Char: %-3c.\n", a);`
    4. `#!c printf("Chars: \n-%c.\n-%c.\n", a, 'z' - 1);`
    5. `#!c printf("Sum: %i\n", i1 + i2 - a);`
    6. `#!c printf("Taux d’erreur\t%i %%\n", i1);`
    7. `#!c printf("Quel charabia horrible:\\\a\a\a%g\b\a%%\a\\\n", f1);`
    8. `#!c printf("Inventaire: %i4 pieces\n", i1);`
    9. `#!c printf("Inventory: %i %s\n", i1, "pieces");`
    10. `#!c printf("Inventaire: %4i pieces\n", i1);`
    11. `#!c printf("Inventaire: %-4i pieces\n", i1);`
    12. `#!c printf("Mixed sum: %f\n", sh1 + i1 + f1);`
    13. `#!c printf("Tension: %5.2f mV\n", f1);`
    14. `#!c printf("Tension: %5.2e mV\n", f1);`
    15. `#!c printf("Code: %X\n", 12);`
    16. `#!c printf("Code: %x\n", 12);`
    17. `#!c printf("Code: %o\n", 12);`
    18. `#!c printf("Value: %i\n", -1);`
    19. `#!c printf("Value: %hi\n", 65535u);`
    20. `#!c printf("Value: %hu\n", -1);`
