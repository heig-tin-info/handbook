# Bibliothèques standard

Aux premières heures de l'informatique (années 1950 et 1960), les programmeurs écrivaient du code très spécifique à la machine, généralement en langage assembleur. Il n'y avait pas de bibliothèques standard ou de frameworks, et les programmeurs devaient souvent écrire eux-mêmes des fonctionnalités de base comme la gestion des entrées/sorties ou les opérations mathématiques. L'idée de réutilisabilité de code était encore peu développée. Les langages étaient souvent conçus pour une seule machine, ce qui limitait les possibilités de portabilité.

Le langage C est l'un des premiers langages à introduire une bibliothèque standard appelée [C standard library](https://fr.wikipedia.org/wiki/Biblioth%C3%A8que_standard_du_C) (*libc*). Cette bibliothèque visait à fournir un ensemble de fonctions de base pour faciliter le développement d'applications. Elle contenait des fonctions pour la gestion des chaînes de caractères, des fichiers, de la mémoire, des maths, etc. Avant cela, ces fonctionnalités devaient être écrites par chaque programmeur pour chaque projet. L'ajout de cette bibliothèque standard a permis de simplifier considérablement le développement en évitant de réinventer la roue pour chaque projet.

Java, lancé par Sun Microsystems, a introduit une bibliothèque standard extrêmement riche dès sa première version, connue sous le nom de Java Standard Library. Elle couvrait un large éventail de domaines (gestion des entrées/sorties, interfaces graphiques, réseau, etc.). Le fait que Java soit livré avec une bibliothèque complète et uniforme a joué un rôle crucial dans sa popularité. Java a également introduit des frameworks comme **Swing** pour les interfaces graphiques et a encouragé l'utilisation d'APIs standardisées. Python, créé par Guido van Rossum en 1991, a aussi adopté très tôt l'idée d'une bibliothèque standard complète, appelée **Python Standard Library**. Python est souvent loué pour son approche "batteries included" ("batteries incluses"), signifiant que le langage fournit une vaste gamme d'outils prêts à l'emploi. Cela a fait de Python un langage très populaire pour le développement rapide d'applications.

Aujourd'hui, pratiquement tous les langages modernes (comme Rust, Go, Swift, Kotlin) sont livrés avec des bibliothèques standard étendues, ainsi que des frameworks et des outils de gestion de paquets (comme npm pour JavaScript, pip pour Python, cargo pour Rust, etc.). Ces outils permettent aux développeurs d’accéder à des milliers de bibliothèques tierces et à des frameworks qui simplifient la construction d’applications complexes.

En C, la situation n'a pas beaucoup évoluée depuis les années 70. Le langage C est un langage de bas niveau qui ne fournit toujours pas de bibliothèque standard étendue. Si une des raison est la portabilité des programmes, une autre raison est que le langage C est un langage minimaliste. Il a été conçu pour être simple et efficace, et les concepteurs ont délibérément choisi de ne pas inclure de fonctionnalités avancées dans le langage lui-même. Il existe donc en C une seule bibliothèque la *libc* qui souffre de quelques lacunes et incohérences par le fait de son ancienneté et de la nécessité de conserver la compatibilité avec les anciennes versions.

La *libc* reste néanmoins un outil indispensable pour le développeur C. Nous allons voir dans ce chapitre les différents fichiers d'en-tête et fonctions qu'elle propose en montrant quelques exemples d'utilisation.

Table: En-têtes standard

| En-tête                               | Description                                 | Standard |
| ------------------------------------- | ------------------------------------------- | -------- |
| [`<assert.h>`][libc-assert]           | Validation des prérequis                    | C89      |
| [`<complex.h>`][libc-complex]         | Nombres complexes                           | **C99**  |
| [`<ctype.h>`][libc-ctype]             | Tests                                       | C89      |
| [`<errno.h>`][libc-errno]             | Gestion des erreurs                         | C89      |
| [`<fenv.h>`][libc-fenv]               | Environnement de calcul flottant            | **C99**  |
| [`<float.h>`][libc-float]             | Constantes de précision des types flottants | C89      |
| [`<inttypes.h>`][libc-inttypes]       | Types entiers formatés                      | **C99**  |
| [`<iso646.h>`][libc-iso646]           | Alternative aux opérateurs (and, or)        | **C95**  |
| [`<limits.h>`][libc-limits]           | Limites des types entiers                   | C89      |
| [`<locale.h>`][libc-locale]           | Gestion des locales                         | C89      |
| [`<math.h>`][libc-math]               | Fonctions mathématiques                     | C89      |
| [`<setjmp.h>`][libc-setjmp]           | Gestion des sauts                           | C89      |
| [`<signal.h>`][libc-signal]           | Gestion des signaux                         | C89      |
| [`<stdalign.h>`][libc-stdalign]       | Alignement des types                        | **C11**  |
| [`<stdarg.h>`][libc-stdarg]           | Arguments variables                         | C89      |
| [`<stdatomic.h>`][libc-stdatomic]     | Opérations atomiques                        | **C11**  |
| [`<stdbit.h>`][libc-stdbit]           | Macros pour les bits                        | **C23**  |
| [`<stdbool.h>`][libc-stdbool]         | Type booléen                                | **C99**  |
| [`<stdckdint.h>`][libc-stdckdint]     | Macros de tests pour les entiers            | **C23**  |
| [`<stddef.h>`][libc-stddef]           | Macros standard                             | C89      |
| [`<stdint.h>`][libc-stdint]           | Types entiers standard                      | **C99**  |
| [`<stdio.h>`][libc-stdio]             | Entrées/sorties standard                    | C89      |
| [`<stdlib.h>`][libc-stdlib]           | Allocation dynamique                        | C89      |
| [`<stdnoreturn.h>`][libc-stdnoreturn] | Fonctions sans retour                       | **C11**  |
| [`<string.h>`][libc-string]           | Manipulation des chaînes de caractères      | C89      |
| [`<tgmath.h>`][libc-tgmath]           | Fonctions mathématiques génériques          | **C99**  |
| [`<threads.h>`][libc-threads]         | Gestion des threads                         | **C11**  |
| [`<time.h>`][libc-time]               | Date et heure                               | C89      |
| [`<uchar.h>`][libc-uchar]             | Caractères Unicode                          | **C11**  |
| [`<wchar.h>`][libc-wchar]             | Caractères larges                           | **C95**  |
| [`<wctype.h>`][libc-wctype]           | Tests larges                                | **C95**  |

[](){#libc-assert}
## `<assert.h>`

On peut bien se demander à quoi sert un en-tête `<assert.h>` qui ne contient qu'une seule fonction. La fonction `assert` est une fonction très utile pour valider des prérequis. Elle s'utilise principalement pour du débogage mais parfois pour s'assurer qu'une expression qui à priori ne devrait jamais valoir `false` est bien vraie. L'en-tête offre deux prototypes qui sont en réalité des macros :

```c
int assert(int expression);
static_assert(int expression, "message");
```

L'utilisation de assert permet de détecter les erreurs pendant la phase de développement ou de test. Si une condition critique n'est pas respectée (par exemple, un pointeur nul ou une division par zéro), le programme s'arrête avec une information précieuse pour le débogage.

```c
#include <assert.h>
#include <memory.h>
int main() {
    void *p = malloc(10);
    assert(p != NULL);
    ...
}
```

La grande force d'assert est qu'elle peut être désactivée dans un environnement de production en définissant la macro `NDEBUG`. Lorsque `NDEBUG` est défini, toutes les assertions sont remplacées par des expressions nulles (ne font rien), ce qui élimine toute surcharge due aux vérifications. D'une façon simplifiée, `NDEBUG` pourrait être implémenté comme ceci :

```c
#ifdef NDEBUG
    #define assert(ignore) ((void)0)
#else
    #define assert(expr) \
        ((expr) ? (void)0 : __assert_fail(#expr, __FILE__, __LINE__, __func__))
#endif
```

Si vous souhaitez désactiver les assertions, vous pouvez aussi le faire en ajoutant `-DNDEBUG` à la ligne de commande du compilateur. Par exemple :

```bash
gcc -DNDEBUG -o foo main.c
```

!!! warning "Avant l'en-tête"

    Il est important de déclarer `NDEBUG` avant d'inclure l'en-tête `<assert.h>`. En effet, l'en-tête `<assert.h>` va définir la macro `assert` qui sera utilisée dans le code. Si `NDEBUG` est défini après l'inclusion de l'en-tête, la macro `assert` ne sera pas correctement définie.

[](){#libc-errno}
## `<errno.h>`

La bibliothèque `<errno.h>` est utilisée pour gérer les erreurs. Elle définit une variable **globale** `errno` qui est un entier qui contient le code de l'erreur modifié par certaines fonctions de la bibliothèque standard.

Des macros sont également définies selon le standard POSIX pour les codes d'erreurs. Par exemple, `EACCES` pour une erreur d'accès, `ENOENT` pour un fichier ou répertoire inexistant, `ENOMEM` pour une erreur d'allocation mémoire, etc. La liste étant relativement longue elle peut être consultée directmenet sur le [standard POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/errno.h.html). Néanmoins voici les erreurs les plus courantes :

Table: Codes d'erreurs POSIX les plus courants

| Code           | Description                                  |
| -------------- | -------------------------------------------- |
| `EACCES`       | Permission refusée (p.ex. sur un fichier)    |
| `EADDRINUSE`   | Adresse déjà utilisée (socket)               |
| `ECONNREFUSED` | Connexion refusée (socket)                   |
| `EDOM`         | Erreur de domaine mathématique               |
| `EEXIST`       | Fichier existe déjà                          |
| `EINVAL`       | Argument invalide                            |
| `ENOENT`       | Fichier ou répertoire inexistant             |
| `ENOMEM`       | Pas assez de mémoire disponible              |
| `ENOSPC`       | Plus d'espace disponible sur le périphérique |

Par exemple, lors du calcul du logarithme d'un nombre négatif, la fonction `log` va définir `errno` à `EDOM` pour indiquer une erreur de domaine. Il est possible de réinitialiser `errno` à zéro en utilisant la fonction `clearerr` ou `errno = 0`.

```c
#include <stdio.h>
#include <math.h>
#include <errno.h>
#include <string.h>

int main(void)
{
    errno = 0;
    printf("log(-1.0) = %f\n", log(-1.0)); // Domain error
    printf("%s\n\n",strerror(errno));

    errno = 0;
    printf("log(0.0)  = %f\n", log(0.0));
    printf("%s\n",strerror(errno)); // Numerical result out of range
}
```

[](){#libc-math}
## `<math.h>`

La bibliothèque mathématique est une des plus utilisées. Elle contient des fonctions pour les opérations mathématiques de base. Les fonctions sont définies pour les types `float`, `double` et `long double` avec les préfixes `f`, `l` et sans préfixe respectivement. Le fichier d'en-tête est le suivant et le flag de compilation est `-lm`.

Table: Constantes mathématiques

| Constantes  | Description            |
| ----------- | ---------------------- |
| `M_PI`      | Valeur de $\pi$        |
| `M_E`       | Valeur de $e$          |
| `M_SQRT1_2` | Valeur de $1/\sqrt(2)$ |

!!! warning "Windows"

    Attention, ces constantes ne sont pas définies par le standard C, mais par le standard POSIX. Il est donc possible que certaines implémentations ne les définissent pas, en particulier sous Windows.

Table: Fonctions mathématiques

| Fonction     | Description                               |
| ------------ | ----------------------------------------- |
| `exp(x)`     | Exponentielle $e^x$                       |
| `ldexp(x,n)` | Exposant d'un nombre flottant $x\cdot2^n$ |
| `log(x)`     | Logarithme binaire $\log_{2}(x)$          |
| `log10(x)`   | Logarithme décimal $\log_{10}(x)$         |
| `pow(x,y)`   | Puissance $x^y$                           |
| `sqrt(x)`    | Racine carrée $\sqrt(x)$                  |
| `cbrt(x)`    | Racine cubique $\sqrt[3](x)$              |
| `hypot(x,y)` | Hypoténuse optimisé $\sqrt(x^2 + y^2)$    |
| `ceil`       | Arrondi à l'entier supérieur              |
| `floor`      | Arrondi à l'entier inférieur              |

Notons par exemple que la fonction `hypot` peut très bien être émulée facilement en utilisant la fonction `sqrt`. Néanmoins elle existe pour deux raisons élémentaires :

1. Éviter les dépassements (*overflow*).
2. Une meilleure optimisation du code.

Souvent, les processeurs sont équipés de coprocesseurs arithmétiques capables de calculer certaines fonctions plus rapidement.

Le standard C99 a introduit l'en-tête [`<tgmath.h>`][libc-tgmath] qui donne accès à des fonctions génériques. Par exemple, `sin` peut être utilisé pour des `float`, `double` et `long double` sans avoir à choisir le nom de la fonction (`sinf`, `sin`, `sinl`), en outre les types complexes sont également supportés comme `csin` pour les complexes.

[](){#libc-fenv}
## `<fenv.h>`

La bibliothèque `<fenv.h>` est étroitement liée aux calculs mathématique et permet de manipuler l'environnement de calcul flottant. Elle permet de contrôler les modes de calculs, les exceptions et les arrondis. Les fonctions sont définies pour les types `float`, `double` et `long double` avec les préfixes `f`, `l` et sans préfixe respectivement.

La structure `fenv_t` contient l'état de l'environnement de calcul flottant et la structure `fexcept_t` contient les exceptions de calcul flottant. Ces structures sont opaques et ne doivent pas être manipulées directement, elles dépendent de l'implémentation et peuvent varier d'un système à l'autre. Néanmoins pour X86, voici à quoi elles pourraient ressembler pour les curieux.

```c
typedef struct {
    // Mot de contrôle de la FPU.
    union {
        unsigned int __control_word;
        struct {
            // Masque des exceptions de la FPU
            unsigned int IM : 1;  // Invalid Operation
            unsigned int DM : 1;  // Denormalized Operand
            unsigned int ZM : 1;  // Zero-Divide
            unsigned int OM : 1;  // Overflow
            unsigned int UM : 1;  // Underflow
            unsigned int PM : 1;  // Precision
            unsigned int _Reserved : 2;
            // Gestion de l'arrondi et de la précision
            unsigned int PC : 2;  // Precision Control
            unsigned int RC : 2;  // Rounding Control mode
            unsigned int _FPUReserved : 3;
            unsigned int IC : 1;  // Plus utilisé
        };
    };

    // Word de statut de la FPU (indicateurs d'état et d'exception)
    union {
        unsigned int __status_word;
        struct {
            // Indicateurs d'exception
            unsigned int IE : 1;  // Invalid Operation Exception
            unsigned int DE : 1;  // Denormalized Operand Exception
            unsigned int ZE : 1;  // Zero-Divide Exception
            unsigned int OE : 1;  // Overflow Exception
            unsigned int UE : 1;  // Underflow Exception
            unsigned int PE : 1;  // Precision Exception
            unsigned int SF : 1;  // Stack Fault
            unsigned int ES : 1;  // Exception Summary Status

            // Indicateurs d'état pour le stockage de valeurs
            // intermédiaires durant les calculs
            unsigned int C0 : 1;
            unsigned int C1 : 1;
            unsigned int C2 : 1;
            unsigned int Top : 3;  // Position du sommet de la pile
            unsigned int C3 : 1;
            unsigned int Busy : 1;  // FPU occupée
        };
    };
    unsigned int __tag_word;
    unsigned int __fpu_ip; // Instruction pointer
    unsigned int __fpu_cs; // Code segment
    unsigned int __opcode; // Opcode de l'opération en cours
    unsigned int __fpu_dp; // Data pointer
    unsigned int __mxcsr; // Registre MXCSR (contrôle des exceptions SSE)
    unsigned int __mxcsr_mask; // Masque de contrôle MXCSR
} fenv_t;
```

### Contrôle des exceptions

Il est possible de gérer les exceptions de calculs flottants comme :

- la division par zéro,
- le dépassement de capacité (*overflow*),
- un résultat non numérique (*NaN*),
- un sous-dépassement de capacité (*underflow*),
- une perte de précision.

Dans certains programmes, notamment ceux impliquant des calculs numériques intensifs ou critiques (comme en science ou en ingénierie), il est important de savoir si une opération en virgule flottante a échoué ou produit un résultat incorrect.

```c
#include <stdio.h>
#include <fenv.h>
#pragma STDC FENV_ACCESS ON  // NECESSAIRE

int main() {
    feclearexcept(FE_ALL_EXCEPT); // Efface anciennes exceptions

    double result = 1.0 / 0.0; // Division par zéro

    if (fetestexcept(FE_DIVBYZERO)) {
        printf("Erreur : division par zéro détectée\n");
    }
}
```

### Contrôle de l'arrondi

Il est aussi possible contrôler la manière dont les résultats des opérations en virgule flottante sont arrondis. Par défaut, les opérations en virgule flottante arrondissent au plus proche, mais vous pouvez modifier ce comportement pour arrondir vers zéro, vers l'infini, ou vers moins l'infini.

Nous avions vu [précédemment][rounding] que l'arrondi d'un nombre est compliqué. La norme IEEE 754 définit plusieurs modes d'arrondis. La fonction `fesetround` permet de définir le mode d'arrondi. Les modes possibles sont donnés par la table suivante :

Table: Modes d'arrondis

| Mode            | Description                 | $-3.5$ | $-2.5 | $2.5 | 3.5$ |
| --------------- | --------------------------- | ------ | ----- | ---- | ---- |
| `FE_TONEAREST`  | Arrondi bancaire            | $-4$   | $-2$  | $2$  | $4$  |
| `FE_DOWNWARD`   | Arrondi vers zéro           | $-4$   | $-3$  | $2$  | $3$  |
| `FE_UPWARD`     | Arrondi vers l'infini       | $-3$   | $-2$  | $3$  | $4$  |
| `FE_TOWARDZERO` | Arrondi vers moins l'infini | $-3$   | $-2$  | $2$  | $3$  |
| `round()`       | Comparaison avec `round`    | $-4$   | $-3$  | $3$  | $4$  |

```c
fesetround(FE_TONEAREST);
int rounded = nearbyint(3.5);
```

L'arrondi bancaire minimise les biais d'arrondi lorsqu'on fait des calculs sur de grandes quantités de données. En arrondissant vers l'entier pair dans les cas où un nombre tombe exactement à mi-chemin entre deux entiers, cette méthode réduit l'accumulation d'erreurs statistiques qui peuvent survenir avec d'autres méthodes d'arrondi. En effet les valeurs sont arrondies vers l'entier **pair** le plus proche. Voici quelques exemples :

```text
-1.5 -> -2
-0.5 ->  0
 0.5 ->  0
 1.5 ->  2
 2.5 ->  2
 3.5 ->  4
```

!!! warning "round"

    La configuration du mode d'arrondi avec `fesetround` affecte les fonctions `nearbyint`, `rint` mais pas `round`.

    La fonction `round` utilise un arrondi spécifique appelé *round half away from zero* qui arrondit les valeurs à l'entier le plus proche en s'éloignant de zéro.

Notez que la différence entre `rint` et `nearbyint` est que `nearbyint` ne génère pas d'exception en cas de dépassement de capacité (*overflow*).

[](){#libc-float}
## `<float.h>`

La bibliothèque `<float.h>` contient des constantes qui définissent la précision des types flottants sur l'architecture cible. Les constantes sont définies pour les types `float`, `double` et `long double`.

On y retrouve `FLT_ROUNDS` qui indique le mode d'arrondi par défaut utilisé à la compilation.

Dans IEEE 754, l'exposant est de base 2, c'est ce qu'on appelle le *radix*. Il peut être contrôlé avec la macro `FLT_RADIX`. Les constantes `DBL_DIG` et `LDBL_DIG` indiquent le nombre de chiffres significatifs que l'on peut stocker dans un `double` et un `long double` respectivement.

!!! info "Autre base ?"

    Aujourd'hui quasiment 100 pour cent des ordinateurs utilisent le radix 2. Néanmoins, à une certaine époque le radix 10 était utilisé sur certaines architectures comme le l'IBM 650 (1953).

    La norme IEEE 754-2008 permet d'utiliser le radix 16, 10 ou 2. Elle défini notament la repséentation **DFP** (*Decimal Floating Point*) qui permet de représenter les nombres décimaux de manière exacte. Cependant l'implémentation physique d'une FPU en radix 10 est plus complexe et moins performante c'est pour cela que la vaste majorité des processeurs utilisent le radix 2 suffisant pour la plupart des applications.

[](){#libc-complex}
## `<complex.h>`

La bibliothèque `<complex.h>` permet de manipuler les nombres complexes. Les fonctions sont définies pour les types `float`, `double` et `long double` avec les préfixes `f`, `l` et sans préfixe respectivement.

Un nombre complexe est défini par une partie réelle et une partie imaginaire. Le type `_Complex` est un type de base, mais il peut être utilisé de manière plus simple avec la macro `complex`. Pour définir un nombre complexe, on utilise la notation `a + bi` où `a` est la partie réelle et `b` la partie imaginaire.

```c
#include <complex.h>

int main() {
    double complex z = 1.0 + 2.0 * I;
    double complex w = 3.0 + 4.0 * I;
    double complex sum = z + w;
    printf("Somme : %f + %fi\n", creal(sum), cimag(sum));

    // Nombre imaginaire pur
    double imaginary = -2.0 * I;
}
```

La constante `I` est bien entendue définie comme `1.0i`. Toutes les fonctions complexes se déclines en trois versions:

Table: Variantes de type complexe

| Type          | Exemple de fonction |
| ------------- | ------------------- |
| `float`       | `cabsf`, `csinf`    |
| `double`      | `cabs`, `csin`      |
| `long double` | `cabsl`, `csinl`    |

Table: Fonctions complexes

| Fonction    | Description               |
| ----------- | ------------------------- |
| `cabs(z)`   | Module                    |
| `cacos(z)`  | Arc cosinus               |
| `cacosh(z)` | Arc cosinus hyperbolique  |
| `carg(z)`   | Argument     $\arg(z)$    |
| `casin(z)`  | Arc sinus                 |
| `casinh(z)` | Arc sinus hyperbolique    |
| `catan(z)`  | Arc tangente              |
| `catanh(z)` | Arc tangente hyperbolique |
| `ccos(z)`   | Cosinus                   |
| `ccosh(z)`  | Cosinus hyperbolique      |
| `cexp(z)`   | Exponentielle  $e^z$      |
| `cimag(z)`  | Partie imaginaire $\Im z$ |
| `clog(z)`   | Logarithme  $\log(z)$     |
| `conj(z)`   | Conjugaison $\bar(z)$     |
| `cpow(z,w)` | Puissance  $z^w$          |
| `creal(z)`  | Partie réelle $\Re z$     |
| `csin(z)`   | Sinus                     |
| `csinh(z)`  | Sinus hyperbolique        |
| `csqrt(z)`  | Racine carrée  $\sqrt{z}$ |
| `ctan(z)`   | Tangente                  |
| `ctanh(z)`  | Tangente hyperbolique     |

Certaines extensions prévue possiblement avec C23 amènerait des fonctionnalités supplémentaires telles que `cexp2`, `clog2`, `cexp10`, `clog10`, `crootn` ...


[](){#libc-iso646}
## `<iso646.h>`

L'en-tête `<iso646.h>` est une extension du standard C95 qui définit des alternatives aux opérateurs logiques. Les opérateurs logiques sont définis avec des symbols (`&&`, `||`, `!`) mais pour des raisons de lisibilité, il est possible de les définir en anglais (`and`, `or`, `not`).

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

Je vous recommande personnellement de ne pas utiliser ces macros. Elles ne sont pas très utilisées et peuvent rendre le code moins lisible pour les autres développeurs.

[](){#libc-limits}

## `<limits.h>`

La bibliothèque `<limits.h>` contient des constantes qui définissent les limites des types entiers de base. Les constantes sont définies pour les types `char`, `short`, `int`, `long`, `long long` et `float`, `double`, `long double`.

Table: Limites des entiers de base

| Constante    | Description                               | LP64                 |
| ------------ | ----------------------------------------- | -------------------- |
| `CHAR_BIT`   | Nombre de bits dans un `char`             | 8                    |
| `CHAR_MAX`   | Valeur maximale d'un `char`               | 127                  |
| `CHAR_MIN`   | Valeur minimale d'un `char`               | -128                 |
| `SCHAR_MAX`  | Valeur maximale d'un `signed char`        | 127                  |
| `SCHAR_MIN`  | Valeur minimale d'un `signed char`        | -128                 |
| `UCHAR_MAX`  | Valeur maximale d'un `unsigned char`      | 255                  |
| `SHRT_MAX`   | Valeur maximale d'un `short`              | 32767                |
| `SHRT_MIN`   | Valeur minimale d'un `short`              | -32768               |
| `USHRT_MAX`  | Valeur maximale d'un `unsigned short`     | 65535                |
| `INT_MAX`    | Valeur maximale d'un `int`                | 2147483647           |
| `INT_MIN`    | Valeur minimale d'un `int`                | -2147483648          |
| `UINT_MAX`   | Valeur maximale d'un `unsigned int`       | 4294967295           |
| `LONG_MAX`   | Valeur maximale d'un `long`               | 9223372036854775807  |
| `LONG_MIN`   | Valeur minimale d'un `long`               | -9223372036854775808 |
| `ULONG_MAX`  | Valeur maximale d'un `unsigned long`      | 18446744073709551615 |
| `LLONG_MAX`  | Valeur maximale d'un `long long`          | 9223372036854775807  |
| `LLONG_MIN`  | Valeur minimale d'un `long long`          | -9223372036854775808 |
| `ULLONG_MAX` | Valeur maximale d'un `unsigned long long` | 18446744073709551615 |

[](){#libc-locale}
## `<locale.h>`

En jargon informatique, la *locale* est un ensemble de paramètres qui définissent les conventions culturelles d'une région. Cela inclut la langue, le format de date, le format de nombre, etc. La bibliothèque `<locale.h>` permet de manipuler ces paramètres.

Un système d'exploitation défini généralement une locale par défaut. Par exemple, un système en français utilisera la locale `fr_FR`. Le premier paramètre est la langue de la locale et le second et le pays. Il existe en effet des différences entre le français suisse `fr_CH` et le français canadien `fr_CA`.

Ces conventions sont définie par la norme ISO 15897 et font de surcroît partie du standard POSIX.

L'en-tête `<locale.h>` contient donc des fonctions pour manipuler les locales.

Table: Contenu de locale.h

| Fonction     | Description                          |
| ------------ | ------------------------------------ |
| `setlocale`  | Définit la locale                    |
| `localeconv` | Récupère les paramètres de la locale |
| `lconv`      | Structure retournée par `localeconv` |

Voici un exemple:

```c
#include <locale.h>
#include <stdio.h>

int main() {
    setlocale(LC_ALL, "fr_FR");
    struct lconv *locale = localeconv();
    printf("Séparateur de milliers : %s\n", locale->thousands_sep);
    printf("Séparateur décimal : %s\n", locale->decimal_point);
}
```

La structure `lconv` est définie comme suit :

```c
struct lconv {
    char *decimal_point;  // Séparateur décimal
    char *thousands_sep;  // Séparateur de milliers
    char *grouping;       // Taille des groupes de milliers
    char *int_curr_symbol; // Symbole de la monnaie
    char *currency_symbol; // Symbole de la monnaie
    char *mon_decimal_point; // Séparateur décimal de la monnaie
    char *mon_thousands_sep; // Séparateur de milliers de la monnaie
    char *mon_grouping;      // Taille des groupes de milliers de la monnaie
    char *positive_sign;     // Signe positif
    char *negative_sign;     // Signe négatif
    char int_frac_digits;    // Décimales pour la monnaie
    char frac_digits;        // Décimales
    char p_cs_precedes;      // Symbole avant la monnaie
    char p_sep_by_space;     // Espace entre la monnaie et le montant
    char n_cs_precedes;      // Symbole avant la monnaie négative
    char n_sep_by_space;     // Espace entre la monnaie négative et le montant
    char p_sign_posn;        // Position du signe positif
    char n_sign_posn;        // Position du signe négatif
};
```

Voici un exemple plus complet :

```c
#include <locale.h>

int main() {
    char country[] = "EN";
    printf("Vous parlez français, tant mieux. Quel est votre pays ? ");
    if (scanf("%2s", &country) != 1) {
        printf("Erreur de saisie\n");
        return 1;
    }
    for (int i = 0; country[i]; i++) country[i] = toupper(country[i]);

    char locale[6];
    snprintf(locale, 6, "fr_%s", country);

    setlocale(LC_ALL, locale);

    float apple_unit_price;
    printf("Quel est le prix d'une pomme ? ");
    if (scanf("%f", &apple_unit_price) != 1) {
        printf("Erreur de saisie\n");
        return 1;
    }
    const int quantity = 10;
    const float ten_apples_price = apple_unit_price * quantity;

    printf("Le prix de %d pommes est de %.2f %s\n",
        quantity, ten_apples_price, localeconv()->currency_symbol);
}
```

Avec la fonction `setlocale`, il est possible de ne définir qu'une partie des conventions à utiliser. Par exemple, si on ne veut changer que le format de date, on peut utiliser `setlocale(LC_TIME, "fr_FR")`.

Table: Catégories de locales

| Catégorie     | Description               |
| ------------- | ------------------------- |
| `LC_ALL`      | Toutes les catégories     |
| `LC_COLLATE`  | Comparaison de chaînes    |
| `LC_CTYPE`    | Caractères et conversions |
| `LC_MONETARY` | Format monétaire          |
| `LC_NUMERIC`  | Format numérique          |
| `LC_TIME`     | Format de date et heure   |

[](){#libc-setjmp}
## `<setjmp.h>`

La bibliothèque `<setjmp.h>` permet de gérer les exceptions en C. Elle fournit deux fonctions `setjmp` et `longjmp` qui permettent de sauvegarder l'état du programme et de le restaurer à un point donné.

En pratique il est très rare d'utiliser ces fonctions, elles sont aussi dangereuses que les `goto` et peuvent rendre le code difficile à lire et à maintenir. Néanmoins dans des cas très spécifiques, elles peuvent s'avérer très utiles, notament pour simuler des exceptions avec des directives [préprocesseur][preprocessor-exceptions].

Nous avons vu que le compilateur utilise [la pile][stack-plumbing] pour stocker les variables locales et le contexte d'appel des fonctions. Dans chaque *frame* de la pile, on trouve l'adresse de retour permettant de continuer l'exécution d'une fonction dans la fonction appelante une fois la fonction courrante terminée. Ceci permet de communiquer hiérarchiquement entre les fonctions. Il n'est pas possible par exemple de remonter à la fonction `main` depuis une fonction `baz` appelée par `bar` appelée par `foo`, appelée par `main`.

Ce n'est pas possible... sauf si on triche un peu. La fonction `setjmp` permet de sauvegarder l'état du programme à un point donné. C'est-à-dire que si on sauve le contexte de `main` dans un espace mémoire séparé avant la chaîne d'appel de fonctions enfants, on pourrait manipuler le stack pour revenir à `main` depuis `baz`. C'est très exactement ce que fait `setjmp`.

La fonction `setjmp` prend un seul argument qui est une structure de type `jmp_buf`. Cette structure est opaque car elle dépend du compilateur et de la manière dont le stack est implémenté. Néanmoins sur une architecture x86, elle pourrait ressembler à ceci :

```c
typedef struct {
    unsigned int __eip; // Instruction pointer
    unsigned int __esp; // Stack pointer
    unsigned int __ebp; // Base pointer
    unsigned int __ebx; // Base register
    unsigned int __esi; // Source index
    unsigned int __edi; // Destination index
} jmp_buf[1];
```

Il s'agit des registres du processeur concernés par la gestion du stack et le déroulement du programme. Le registre `eip` par exemple est le pointeur d'instruction. Il contient l'adresse de la prochaine instruction à exécuter. Si ce registre est modifié, le programme saute à une autre adresse. C'est ce que fait entre autre le `goto`, il modifie `eip` pour sauter à une autre adresse.

Pour marquer un point de retour, on utilise `setjmp` qui sauvegarde l'état du programme dans la structure `jmp_buf`. On peut ensuite revenir à ce point avec `longjmp`. La fonction `longjmp` prend deux arguments, la structure `jmp_buf` et une valeur de retour qui peut être utilisée pour savoir pourquoi on est revenu à ce point. Voici un exemple :

```c
#include <setjmp.h>

jmp_buf env; // Doit être transverse à toutes les fonctions, donc globale

void foo() { longjmp(env, 42); }
void bar() { foo(); }
void baz() { bar(); }
int main() {
    int ret = setjmp(env); // Sauvegarde l'état du programme
    if (ret == 0) {
        printf("Première exécution\n");
        baz();
    } else {
        printf("Retour à setjmp avec %d\n", ret);
    }
}
```

Lors de l'appel de `setjmp`, la fonction retourne 0. Cette valeur peut être utilisée pour tester si c'est la première fois que la fonction est appelée ou si c'est un retour de `longjmp`. Dans ce cas, la fonction retourne la valeur passée à `longjmp`.

[](){#libc-signal}
## `<signal.h>`

Les signaux sont des mécanismes spécifiques aux systèmes d'exploitations qui permettent de communiquer entre les processus (programmes) et le noyau. Un signal ne véhicule pas de données, il permet simplement de réveiller un processus pour lui indiquer qu'un événement s'est produit. Alternativement un signal peut être émis par un processus pour demander au noyau de réaliser une action.

Les signaux sont fondamentaux au sein d'un OS et de ce fait ils sont standardisés par POSIX. Windows utilise également des signaux mais ils diffèrent un peu. En C, la bibliothèque `<signal.h>` permet de manipuler les signaux de manière portable avec quelques nuances. Voici les types de signaux les plus courants :

Table: Signaux POSIX (liste non exhaustive)

| Signal    | Description                        |
| --------- | ---------------------------------- |
| `SIGABRT` | Abandon du processus               |
| `SIGALRM` | Alarme horloge                     |
| `SIGFPE`  | Erreur de calcul flottant          |
| `SIGILL`  | Instruction illégale               |
| `SIGINT`  | Interruption depuis le clavier     |
| `SIGKILL` | Arrêt forcé du processus           |
| `SIGPIPE` | Écriture dans un tube sans lecteur |
| `SIGSEGV` | Violation de segmentation          |
| `SIGTERM` | Demande d'arrêt du processus       |
| `SIGUSR1` | Signal utilisateur 1               |
| `SIGUSR2` | Signal utilisateur 2               |

La fonction `abort()` disponible dans `<stdlib.h>` envoie un signal `SIGABRT` pour arrêter le programme. Une violation d'accès à un espace mémoire non alloué envoie un signal `SIGSEGV` (la fameuse erreur de segmentation). Un dépassement de capacité en virgule flottante envoie un signal `SIGFPE`.

Pour envoyer un signal à un processus depuis le terminal, on utilise la commande `kill`. Par exemple, pour envoyer un signal `SIGUSR1` au processus 1234, on utilise la commande `kill -SIGUSR1 1234`. Le 1234 est le PID (*Process ID*) du processus car chaque programme qui s'exécute a un identifiant unique attribué par le système d'exploitation. Le nom de la commande `kill` peut être trompeur car elle n'arrête pas le processus, elle lui envoie un signal. Le nom vient historiquement du fait que le signal par défaut est `SIGTERM` qui demande au processus de s'arrêter.

Dans un programme C il est possible de capturer les signaux reçus en installant des *handlers*. Il s'agit d'une fonction qui sera appelée de manière évènementielle lorsqu'un signal est reçu. Ces *handlers* court-circuitent donc le comportement normal du programme en interrompant l'action en cours. Voici un exemple pour capturer le signal `SIGINT` qui est envoyé lorsqu'on appuie sur `Ctrl+C` pour interrompre un programme depuis le terminal :

```c
#include <signal.h>
#include <stdio.h>

void sigint_handler(int signum) {
    printf("Vous partez déjà ? :(\n");
    exit(0);
}

void jeudredi() {
    char fruits[] = {"banane", "kiwi", "ananas", "mangue", "cerise"};
    int i = 0;
    while(1) {
        printf("Il est très bon ce coktail à la %s !\n", fruits[i++ % 5]);
        sleep(1); // Pause d'une seconde
    }
}

int main() {
    signal(SIGINT, sigint_handler);
    jeudredi();
}
```

[](){#libc-stdalign}
## `<stdalign.h>`

La bibliothèque `<stdalign.h>` fournit des fonctions pour manipuler l'alignement des données en mémoire. L'alignement est une notion importante en informatique car les processeurs sont plus efficaces lorsqu'ils accèdent à des données alignées. Imaginez un camion qui transporte des palettes de marchandises. La logistique est faite de manière à ce que les palettes soient facile à charger et décharger du camion avec un minimum de manutention. Imaginez maintenant que vous voulez prendre un élément d'une palette. Cela demande plus de travail parce que vous devez extraire l'élément et trouver un autre outil pour le transporter. Un ordinateur 64-bits sur une architecture x86 a beaucoup de faciliter à véhiculer des mots de 8 octets et il s'arrangera en mémoire à disposer les données de la taille d'une palette (64-bits) de façon à ce que son accès soit le plus rapide possible.

La fonction `alignof` retourne l'alignement d'un type donné. Par exemple, `alignof(int)` retourne 4 sur une architecture x86 32-bits et 8 sur une architecture x86 64-bits. La fonction `alignas` permet de spécifier l'alignement d'une variable ou d'une structure. Dans cet exemple, on demande à ce que la variable `a` soit alignée sur 16 octets. L'adresse de `a` sera donc un multiple de 16. On peut le vérifier avec la fonction `alignof`.

```c
#include <stdio.h>
#include <stdalign.h>

int main() {
    alignas(16) int a;
    printf("Alignement de int : %zu\n", alignof(int));
    printf("Adresse de 'a' : %p\n", (void*)&a);
}
```

L'utilité de cette fonction est limitée en pratique. Elle est principalement utilisée pour manipuler des données SIMD (*Single Instruction Multiple Data*) ou pour optimiser les performances de certaines structures de données. On peut l'utiliser égalemenr pour accroître l'interopérabilité entre le C et d'autres langages de programmation.

Une utilisation courante est avec des structures. L'exemple suivant montre une structure de 13 bytes mais le processeur, selon l'architecture pourrait décider de stocker le `char` sur 4 bytes et la structure serait donc de 16 bytes. On peut forcer l'alignement de la structure manuellement avec `alignas(16)`.

```c
struct alignas(16) Data {
    char c;    // 1 octet
    int i;     // 4 octets
    double d;  // 8 octets
};
```

[](){#libc-stdarg}
## `<stdarg.h>`

Ne vous êtes-vous jamais demandé quel est le prototype de `printf` ? Comment se fait-il que cette fonction puisse prendre un nombre variable d'arguments ? La réponse est la bibliothèque `<stdarg.h>` qui permet de manipuler les arguments d'une fonction variable. Observons le prototype de `printf` :

```c
int printf(const char *format, ...);
```

Notez les points de suspension `...` après le format. Il s'agit d'une fonction variadic, c'est-à-dire qu'elle peut prendre un nombre variable d'arguments. Rappelez-vous en relisant le chapitre sur la pile, que lorsqu'une fonction est appelée, les différents arguments sont empilés sur la pile. Il est techniquement possible d'empiler autant d'arguments que l'on veut sans changer le comportement de la fonction. Cette dernière lira simplements les arguments à partir de la base du *frame pointer*.

Le fichier d'en-tête déclare 4 macros et un type :

Table: Macros pour les fonctions à arguments variables

| Macro      | Description                      |
| ---------- | -------------------------------- |
| `va_list`  | Type de la liste d'arguments     |
| `va_start` | Initialise la liste d'arguments  |
| `va_arg`   | Récupère un argument de la liste |
| `va_copy`  | Copie une liste d'arguments      |
| `va_end`   | Termine la liste d'arguments     |

Imaginons le cas de figure suivant. Nous souhaitons écrire une fonction qui affiche la somme des valeurs passées en arguments et nous ne savons pas le nombre de valeurs qui seront passées. Voici comment procéder:

```c
#include <stdarg.h>
#include <stdio.h>

int sum(int count, ...) {
    va_list args;
    va_start(args, count);
    int sum = 0;
    for (int i = 0; i < count; i++) sum += va_arg(args, int);
    va_end(args);
    return sum;
}

int main() {
    printf("Somme : %d\n", sum(3, 1, 2, 3));
    printf("Somme : %d\n", sum(5, 1, 2, 3, 4, 5));
}
```

Dans une fonction dont le prototype autorise un nombre variable d'arguments, l'ellipse `...` est utilisée après au moins un argument fixe qui pourrait représenter le nombre d'arguments à suivre. Dans la fonction `printf` ce nombres est caché dans le format, en comptant le nombre de `%`. Dans cette fonction, une liste d'arguments `args` est déclarée. Lors de l'appel de `va_start`, la liste est initialisée à partir de l'argument suivant `count`. En pratique `va_list` est un pointeur sur la pile qui pointe sur l'argument suivant `count`. La fonction `va_arg` permet de récupérer les arguments un par un de façon portable. En pratique elle déréférence le pointeur et retourne le type spécifié comme deuxième argument. Enfin, `va_end` termine la liste d'arguments.

Voici ci-dessous comment elle pourrait être implémentée, néanmoins ces macros utilisent des fonctions précompilées (p. ex: `__builtin_va_start`) qui sont spécifiques à chaque compilateur.

```c
typedef struct {
    unsigned int gp_offset;  // Offset dans les registres généraux
    unsigned int fp_offset;  // Offset dans les registres flottants
    void* overflow_arg_area; // Pointeur vers les arguments passés sur la pile
    void* reg_save_area;     // Pointeur vers les registres sauvegardés
} va_list;

// Macro générique pour récupérer la taille d'un type
#define type_size(type) _Generic((type), \
    int: sizeof(int), \
    double: sizeof(double), \
    float: sizeof(float), \
    char: sizeof(char), \
    default: sizeof(void*))

#define va_start(ap, last) __va_start(ap, &last, type_size(last))
#define va_arg(ap, type) \
    *((type*)(ap.overflow_arg_area)); \
    ap.overflow_arg_area += type_size(type)
#define va_end(ap) (void)0

void __va_start(va_list_hack* ap, void* last, size_t last_size) {
    void *stack_pointer;
    ap->overflow_arg_area = (void*)((char*)(&last) + last_size);
    ap->gp_offset = 0;
    ap->fp_offset = 0;
    ap->reg_save_area = NULL;
}
```

[](){#libc-stdatomic}
## `<stdatomic.h>`

Cet en-tête concerne la notion d'atomicité en programmation concurrente, et il pourrait s'agir d'un cours à part entière. L'atomicité est la propriété d'une opération qui est exécutée en une seule étape sans être interrompue. En d'autres termes, une opération atomique est une opération qui est soit complètement exécutée, soit pas du tout. Lorsqu'un programme utilise des *threads* (sous-programmes exécutés en parallèle), il est possible que deux exécutions parallèles tentent de modifier la même variable en même temps. Cela peut poser de gros problèmes de corruption de données. Vous savez par exemple qu'un entier est stocké sur 4 octets. On peut néanmoins imaginer une fonction d'échange de deux variables un peu naive qui traite chaque octet séparément.

```c
union Int { int i; char c[4]; };

void swap(int *a, int *b) {
    union Int tmp;
    tmp.i = *a;
    for (int i = 0; i < 4; i++) {
        char t = ((union Int)*a).c[i];
        ((union Int)*a).c[i] = ((union Int)*b).c[i];
        ((union Int)*b).c[i] = t;
    }
}
```

Dans le cas ou deux processus séparés essaient de traiter la valeur de `a` envoyée, l'un à `swap` et l'autre à `printf`. Le résultat dépendra et l'ordre d'exécution des instructions, et il se peut que printf affiche déjà quelque chose alors que `swap` n'a pas encore terminé. C'est ce qu'on appelle une condition de course. Bien entendu en pratique personne n'écrirait une fonction d'échange de variables de cette manière. Toutefois, pour résoudre ce type de problème on utilise des fonctions atomiques qui ajoutent une couche de protection à des variables partagées entre plusieurs *threads*.

Par conséquent, il est nécessaire d'utiliser un accesseur atomique pour lire et écrire la variable :

```c
#include <stdatomic.h>

int main() {
    atomic_int a = 42;
    atomic_store(&a, 42);     // Écriture atomique
    int b = atomic_load(&a);  // Lecture atomique
    atomic_fetch_add(&a, 1);  // Incrémentation atomique de 1
    atomic_fetch_sub(&a, 1);  // Soustraction atomique de 1
    atomic_fetch_or(&a, 1);   // ...
    atomic_fetch_and(&a, 1);
    atomic_fetch_xor(&a, 1);
    atomic_exchange(&a, 42);  // Notre fonction swap atomic
    atomic_compare_exchange_strong(&a, &b, 42);
    atomic_compare_exchange_weak(&a, &b, 42);
}
```

Pour de plus emples informations sur la programmation concurrente, je vous redirige sur un cours dédié à ce sujet.

[](){#libc-stdbit}
## `<stdbit.h>`

Cette bibliothèque a été introduite avec le standard C23 et elle permet de manipuler les bits de manière portable en fournissant des macros pour les opérations bit à bit. Les macro suivantes sont disponibles :

Table: Macros bit à bit dans C23

| Macro           | Description                                           |
| --------------- | ----------------------------------------------------- |
| `stdc_popcount` | Compte le nombre de bits à 1                          |
| `stdc_clz`      | Compte le nombre de bits à 0 avant le premier bit à 1 |
| `stdc_ctz`      | Compte le nombre de bits à 0 après le dernier bit à 1 |
| `stdc_rotl`     | Rotation à gauche                                     |
| `stdc_rotr`     | Rotation à droite                                     |
| `stdc_bswap`    | Inversion des octets                                  |

Bien entendu pour ces opérations, il est nécessaire de connaître la taille du type utilisé. C'est pourquoi ces macros sont génériques et utilisent `_Generic` pour déterminer la taille du type. Une rotation à droite pourrait être implémentée naïvement avec une macro :

```c
#define stdc_rotl(x, n) \
    ((x << (n % (sizeof(x) * CHAR_BIT))) | (x >> ((sizeof(x) * CHAR_BIT) -
    (n % (sizeof(x) * CHAR_BIT)))))
```

Néanmoins ces fonctions sont faites pour profiter des instructions spécifiques des processeurs modernes qui permettent de réaliser ces opérations de manière plus efficace. En effet dans l'architecture X86 par exemple il existe la directive assembleur `ror` pour la rotation à droite et `rol` pour la rotation à gauche. Ces instructions sont plus rapides que la méthode naïve ci-dessus mais elles n'existent pas nécessairement dans toutes les architectures. Du reste, si on essaye de compiler cette macro avec gcc et observons l'assembler généré, on constate que le compilateur utilise bien l'instruction `ror` pour la rotation à droite. Il est donc capable de comprendre le code et de l'optimiser en conséquence.

[](){#libc-stdbool}
## `<stdbool.h>`

Cette bibliothèque est apparue en C99 et après 20 ans d'attente, elle introduit enfin le type booléen `bool` et les valeurs `true` et `false`. Cet en-tête est par conséquent l'un des plus simple de la bibliothèque standard, car il ne contient que trois lignes :

```c
#define bool _Bool
#define true 1
#define false 0
```

Quelle belle mascarade ! On définit `bool` comme `_Bool`... En réalité ce dernier est un type natif du langage alors que `bool` n'est qu'une macro. C'est-à-dire que sans include `<stdbool.h>` vous pouvez tout de même définir un booléen en utilisant `_Bool`. Néanmoins, l'intérêt de cette bibliothèque est de standardiser le type booléen et les valeurs `true` et `false` pour une meilleure portabilité du code.

On peut s'interroger pourquoi le standard à décidé, plutôt que d'ajouter un nouveau type `bool` natif, que de le définir dans un en-tête supplémentaire et de définir le type avec un `_` en préfixe. Le langage C a une longue histoire et de nombreux programmes n'ont pas attendu la sortie de cette bibliothèque pour définir leur propre type booléen. Il était donc nécessaire de ne pas casser la compatibilité avec les anciens programmes. C'est pourquoi le type `_Bool` a été introduit sous cette nomenclature. L'histoire est similaire avec `_Complex` et `_Imaginary` de la bibliothèque `<complex.h>`.

Notez que le `_Bool` est un type très particulier car il est en réalité souvent implémenté comme un entier 8-bit. Rappelez-vous que le processeur aime manipuler des mots de la taille de son bus de données. C'est pourquoi un booléen est souvent stocké sur 32-bits même si un seul bit suffirait. C'est pourquoi on peut stocker des valeurs autres que `true` et `false` dans un booléen. Par exemple, `bool b = 42` est tout à fait valide en C. En réalité, `true` et `false` sont des macros qui valent respectivement 1 et 0. C'est pourquoi on peut les utiliser pour initialiser des booléens.

```c
_Bool b = 1;
printf("%ld\n", sizeof(b)); // Affiche 1
*((int*)&b) += 10; // Bypass le système de typage
printf("%hhd\n", (int)b); // Affiche 11
```

Il est nécessaire de gruger pour ajouter 10 car naïvement le compilateur implémente `b += 10` avec :

```
movs    r3, #1          // Sauve 1 et non 10 dans r3
```

Dans le cas des tableaux, ne perdez pas à l'esprit qu'un tableau de booléens est un tableau d'octets:

```c
bool bool_array[8] = {true, false, true, true, false, false, true, true};
assert(sizeof(bool_array) == 8);
```

[](){#libc-stdckdint}
## `<stdckdint.h>`

Cette bibliothèque est apparue en C23 et propose des fonctions arithmétiques pour les opérations de base comme l'addition, la soustraction, et la multiplication, mais avec une **détection explicite de l'overflow**. L'abbréviation `ckd` signifie *checked*. Les fonctions introduites par cet en-tête sont :

Table: Fonctions de détection de l'overflow

| Fonction  | Description                                 |
| --------- | ------------------------------------------- |
| `ckd_add` | Addition avec détection de l'overflow       |
| `ckd_sub` | Soustraction avec détection de l'overflow   |
| `ckd_mul` | Multiplication avec détection de l'overflow |

Lorsque deux entiers sont additionnés, il est possible que le résultat dépasse la capacité de stockage de l'entier. Par exemple, si on additionne $2^31 - 1$ à 1, on obtient $-2^31$. C'est ce qu'on appelle un *overflow*. En C, l'overflow est un comportement **indéfini**, c'est-à-dire que le compilateur est libre de décider du comportement du programme. En pratique, la plupart des compilateurs vont simplement ignorer l'overflow et le résultat sera tronqué. C'est pourquoi il est important de vérifier les overflows lorsqu'on travaille avec des entiers.

Avant l'introduction de cette bibliothèque, un dépassement de capacité devrait être manuellement implémenté :

```c
int add(int a, int b) {
    if (a > 0 && b > INT_MAX - a) {
        // Overflow détecté
    } else
        return a + b;
}
```

Avec la bibliothèque `<stdckdint.h>`, il est possible de détecter l'overflow de manière plus élégante :

```c
#include <stdckdint.h>

int add(int a, int b) {
    int result;
    if (ckd_add(a, b, &result)) {
        // Overflow détecté
    } else
        return result;
}
```

[](){#libc-stddef}
## `<stddef.h>`

La bibliothèque `<stddef.h>` fournit quelques définitions utiles tel que donné par la table suivante :

Table: Définitions de stddef.h

| Macro         | Description                            |
| ------------- | -------------------------------------- |
| `NULL`        | Pointeur nul                           |
| `offsetof`    | Offset d'un membre d'une structure     |
| `ptrdiff_t`   | Type pour les différences de pointeurs |
| `size_t`      | Type pour les tailles d'objets         |
| `wchar_t`     | Type pour les caractères larges        |
| `nullptr_t`   | Pointeur null (C23)                    |
| `max_align_t` | Type pour l'alignement maximal         |

L'implémentation probable de ces macros est la suivante :

```c
#define NULL ((void*)0)
#define offsetof(type, member) ((size_t)&((type*)0)->member)
typedef unsigned long size_t
typedef ptrdiff_t long
typedef int wchar_t`
```

Concernant les pointeurs, s'il est parfaitement correct de tester si un pointeur vaut 0 (`if (ptr == 0)`), il est recommandé d'utiliser `NULL` pour plus de clarté. Le standard C23 à introduit le type `nullptr_t` pour les pointeurs nuls. Il est recommandé de l'utiliser à la place de `NULL`.

`max_align_t`

: Il s'agit d'un type un type introduit en C11 pour représenter l'alignement maximal possible pour n'importe quel type. Il est utilisé pour définir des types alignés de manière optimale. Par exemple, si on veut définir une structure alignée sur 16 octets, on peut utiliser `max_align_t` pour définir le type de la structure.

`size_t`

: Il s'agit d'un type non signé qui est utilisé pour représenter la taille d'un objet en mémoire. Il est utilisé pour les fonctions qui retournent la taille d'un objet, comme `strlen` ou `sizeof`. Il est défini tel que sa taille soit suffisante, en pratique 64-bits sur une architecture 64-bits.

`ptrdiff_t`

: Il s'agit d'un type signé qui est utilisé pour représenter la différence entre deux pointeurs. Lorsque l'on veut calculer `ptr_p - ptr_q` on obtient un entier dont la valeur maximale dépend de la taille de la mémoire adressable.

[](){#libc-inttypes}
[](){#libc-stdint}
## `<inttypes.h>` et `<stdint.h>`

Ces deux bibliothèques répondent au besoin d'avoir des types entiers d'une taille contrôlée et surtout portable. En effet, nous avons vu que les types standards (`int`, `short`, `long`...) dépendent du modèle de données de l'architecture cible. Un `long` n'aura pas la même taille sur Linux ou Windows par exemple.

L'en-tête `<stint.h>` fourni trois types de base :

Table: Catégories de types entiers portables

| Exemple         | Description                                   |
| --------------- | --------------------------------------------- |
| `int8_t`        | Entier signé sur 8 bits                       |
| `int8_fast8_t`  | Entier signé d'au moins 8 bits le plus rapide |
| `int8_least8_t` | Entier signé d'au moins 8 bits, le plus petit |

Ces catégories sont disponibles our les longueurs 8, 16, 32, 64 bits. Les types sont définis pour les entiers signés et non signés. Par exemple, `int8_t` est un entier signé sur 8 bits, `uint8_t` est un entier non signé sur 8 bits.

Dans le cas ou on aurait besoin d'une variable pouvant contenir les valeurs de 0 à 255 mais que la taille de l'entier importe peu pour autant que le processeur n'ait pas de coût supplémentaire à manipuler la variable, on peut utiliser `uint_fast8_t`.

À l'inverse, si le besoin est d'avoir une variable qui peut contenir les valeurs de 0 à 255 avec la taille la plus petite possible (idéalement 8 bits), on utilisera `uint_least8_t`.

Enfin, dans le cas (le plus rare) ou on aurait besoin exactement d'un entier non signé de 8 bits, on utilisera `uint8_t`. Néanmoins ce type présente une contrainte importante car toutes les architectures ne sont pas nécessairement prévues pour manipuler des entiers de 8 bits. Par exemple le SHARC d'Analog Devices est un processeur 32 bits qui n'a pas de support natif pour les entiers de 8 bits. L'utilisation de `uint8_t` résulterait en une erreur de compilation.

L'en-tête `<stdint.h>` fournit également des macros utiles pour connaître le choix de l'implémentation. Par exemple, `INT_FAST8_WIDTH` donne la largeur de l'entier le plus rapide selon la machine cible.

On aura également les valeurs minimum et maximum que peut contenir chacun des types entiers. Par exemple, `INT8_MIN` et `INT8_MAX` pour les entiers signés sur 8 bits.

Dans une boucle `for` opérant sur un tableau de 100 éléments, il serait correct d'utiliser le type `uint_fast8_t` pour l'index de la boucle. Néanmoins pour des raisons de lisibilités, il est souvent préférable d'utiliser simplement `int` qui, selon le standard, garanti d'être capable de contenir la taille du tableau.

```c
#include <stdint.h>

int main() {
    for (int_fast8_t i = 0; i < 100; i++) {
        ...
    }
}
```

En outre, pour des raisons de cohérence, certaines normes pour l'avionique ou le médical imposent que les constantes littérales soient explicitement typées. On connaît déjà les suffixes `u`, `ull` pour les entiers de base, mais on peut également utiliser les macros de `<stdint.h>` pour les constantes littérales.

```c
uint8_t a = UINT8_C(42);
```

L'utilisation de ces types spécifiques dans des fonctions d'entrées sortie (p. ex. `printf`) doit aussi être faite cohérence. Un `int32_t` n'est pas compatible avec `%d` sur toutes les architectures. Il est préférable d'utiliser les macros de `<inttypes.h>` pour les spécifier.

```c
int32_t a = 42;
printf("%" PRId32 "\n", a);
```

[](){#libc-stdio}
## `<stdio.h>`

La bibliothèque `<stdio.h>` est l'une des bibliothèques les plus importantes en C. Elle fournit des fonctions pour l'entrée et les sorties, c'est-à-dire pour lire et écrire des données depuis et vers la console. Elle fournit également des fonctions pour lire et écrire des fichiers.

La plupart des fonctions de cette bibliothèque ont déjà été abordées dans les chapitres précédents. Voici ci-dessous un résumé des fonctions qu'elle contient. Le `(f)` indique que la fonction peut être utilisée pour lire ou écrire depuis un fichier, elle prend un pointeur de type `FILE` en premier argument. Le `(w)` indique que la fonction est prévue pour les caractères larges (`wchar_t`).

Table: Fonctions de stdio.h

| Fonction       | Description                                                          |
| -------------- | -------------------------------------------------------------------- |
| `(f)get(w)c`   | Lit un caractère depuis l'entrée standard ou un fichier              |
| `(f)get(w)s`   | Lit une ligne depuis l'entrée standard ou un fichier                 |
| `(f)put(w)c`   | Écrit un caractère vers l'entrée standard ou un fichier              |
| `(f)put(w)s`   | Écrit une chaîne de caractères vers la sortie standard ou un fichier |
| `clearerr`     | Réinitialise l'état d'erreur d'un flux                               |
| `fclose`       | Ferme un fichier ouvert                                              |
| `feof`         | Vérifie si la fin du fichier est atteinte                            |
| `ferror`       | Vérifie si une erreur est survenue dans le flux                      |
| `fflush`       | Vide le tampon de sortie d'un flux                                   |
| `fgetpos`      | Obtient la position actuelle dans un fichier sous forme de `fpos_t`  |
| `fileno`       | Obtient le descripteur de fichier associé à un flux                  |
| `flockfile`    | Verrouille un flux pour les opérations multithreadées                |
| `fopen`        | Ouvre un fichier pour la lecture, l'écriture ou l'ajout              |
| `fread`        | Lit des blocs d'octets depuis un flux                                |
| `freopen`      | Ouvre à nouveau un fichier sur un flux de fichier existant           |
| `fscanf`       | Lit des données formatées depuis un fichier                          |
| `fseek`        | Positionne le curseur de lecture/écriture dans un fichier            |
| `fsetpos`      | Définit la position actuelle dans un fichier selon un objet `fpos_t` |
| `ftell`        | Renvoie la position actuelle dans un fichier                         |
| `ftrylockfile` | Tente de verrouiller un flux pour les opérations multithreadées      |
| `funlockfile`  | Déverrouille un flux verrouillé                                      |
| `fwrite`       | Écrit des blocs d'octets vers un flux                                |
| `perror`       | Affiche un message d'erreur basé sur la dernière erreur rencontrée   |
| `remove`       | Supprime un fichier                                                  |
| `rename`       | Renomme un fichier                                                   |
| `rewind`       | Remet le curseur au début d'un fichier                               |
| `scanf`        | Lit des données formatées depuis l'entrée standard                   |
| `setbuf`       | Définit un tampon pour un flux                                       |
| `setvbuf`      | Définit le mode de tampon pour un flux                               |
| `sscanf`       | Lit des données formatées depuis une chaîne                          |
| `tmpfile`      | Crée et ouvre un fichier temporaire qui est supprimé à la fermeture  |
| `tmpnam`       | Génère un nom de fichier temporaire unique                           |
| `ungetc`       | Remet un caractère dans le flux pour qu'il soit lu à nouveau         |
| `ungetwc`      | Remet un caractère large dans le flux                                |

Table: Fonctions d'affichage formaté

| Fonction    | Description                                                          |
| ----------- | -------------------------------------------------------------------- |
| `vfprintf`  | Écrit une sortie formatée sur un flux avec une liste variadiques     |
| `vprintf`   | Écrit une sortie formatée sur `stdout` avec une liste variadiques    |
| `vsprintf`  | Écrit une sortie formatée dans une chaîne avec une liste variadiques |
| `vfwprintf` | Version large de `vfprintf` pour les caractères larges (`wchar_t`)   |
| `vwprintf`  | Version large de `vprintf` pour les caractères larges (`wchar_t`)    |
| `vswprintf` | Version large de `vsprintf` pour les caractères larges (`wchar_t`)   |
| `fprintf`   | Écrit une sortie formatée dans un fichier                            |
| `printf`    | Écrit une sortie formatée sur `stdout`                               |
| `sprintf`   | Écrit une sortie formatée dans une chaîne                            |
| `snprintf`  | Écrit une sortie formatée dans une chaîne avec une taille limitée    |
| `fwprintf`  | Version large de `fprintf` pour les caractères larges (`wchar_t`)    |
| `wprintf`   | Version large de `printf` pour les caractères larges (`wchar_t`)     |
| `swprintf`  | Version large de `sprintf` pour les caractères larges (`wchar_t`)    |

Table: Constantes et types de stdio.h

| Constante/Type | Description                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| `EOF`          | Constante retournée par les fonctions de lecture lorsqu'une fin de fichier ou une erreur est rencontrée |
| `NULL`         | Pointeur nul utilisé pour représenter l'absence d'objet                                                 |
| `FILENAME_MAX` | Longueur maximale d'un nom de fichier                                                                   |
| `FOPEN_MAX`    | Nombre maximal de fichiers pouvant être ouverts simultanément                                           |
| `L_tmpnam`     | Longueur minimale d'un tampon pour `tmpnam`                                                             |
| `BUFSIZ`       | Taille du tampon par défaut pour les opérations de lecture/écriture                                     |
| `TMP_MAX`      | Nombre maximal de noms uniques générés par `tmpnam`                                                     |
| `SEEK_SET`     | Indique le début du fichier pour `fseek` et `fseeko`                                                    |
| `SEEK_CUR`     | Indique la position actuelle dans le fichier pour `fseek` et `fseeko`                                   |
| `SEEK_END`     | Indique la fin du fichier pour `fseek` et `fseeko`                                                      |
| `stderr`       | Flux de sortie d'erreur standard                                                                        |
| `stdin`        | Flux d'entrée standard                                                                                  |
| `stdout`       | Flux de sortie standard                                                                                 |
| `FILE`         | Type opaque représentant un flux de fichier                                                             |
| `fpos_t`       | Type utilisé pour stocker la position dans un fichier                                                   |

[](){#libc-stdlib}
## `<stdlib.h>`

Cette bibliothèque contient des fonctions éparses qui ne sont pas assez importantes pour être regroupées dans une bibliothèque dédiée. Contrairement aux langages plus récents (comme C++ ou Java), C n'a pas été conçu avec une philosophie de modularité stricte pour les bibliothèques. Les fonctions étaient rassemblées par utilité pratique plutôt que par sujet spécifique, et les bibliothèques étaient assez limitées en nombre pour garder le langage simple et portable. On y retrouve les catégories suivantes :

- Gestion de la mémoire
- Conversion de chaînes en types numériques
- Gestion du programme
- Nombres aléatoires
- Algorithmes de recherche et de tri

Table: Fonctions diverses de stdlib.h

| Fonction        | Description                                                                        |
| --------------- | ---------------------------------------------------------------------------------- |
| `abort`         | Arrête le programme de manière anormale sans nettoyage des ressources              |
| `exit`          | Arrête le programme de manière normale avec nettoyage des ressources               |
| `quick_exit`    | Arrête le programme de manière normale sans nettoyage complet des ressources (C11) |
| `_Exit`         | Arrête le programme de manière normale sans nettoyage des ressources (C99)         |
| `atexit`        | Enregistre une fonction à appeler lors de l'appel à `exit`                         |
| `at_quick_exit` | Enregistre une fonction à appeler lors de l'appel à `quick_exit` (C11)             |
| `getenv`        | Récupère la valeur d'une variable d'environnement                                  |
| `setenv`        | Ajoute ou modifie une variable d'environnement (POSIX, non standard)               |
| `putenv`        | Ajoute ou modifie une variable d'environnement                                     |
| `unsetenv`      | Supprime une variable d'environnement (POSIX, non standard)                        |
| `system`        | Exécute une commande système dans un shell                                         |
| `rand`          | Génère un nombre pseudo-aléatoire                                                  |
| `srand`         | Initialise le générateur de nombres pseudo-aléatoires                              |
| `mblen`         | Retourne le nombre d'octets d'un caractère multioctet dans une chaîne              |

Table: Gestion de la mémoire de stdlib.h

| Fonction             | Description                                                |
| -------------------- | ---------------------------------------------------------- |
| `malloc`             | Alloue un bloc de mémoire                                  |
| `calloc`             | Alloue et initialise un bloc de mémoire                    |
| `realloc`            | Redimensionne un bloc de mémoire précédemment alloué       |
| `free`               | Libère un bloc de mémoire précédemment alloué              |
| `aligned_alloc`      | Alloue un bloc de mémoire aligné (C11)                     |
| `free_sized`         | Libère un bloc de mémoire de taille spécifiée (C23)        |
| `free_aligned_sized` | Libère un bloc de mémoire aligné de taille spécifiée (C23) |

Table: Algorithmes de recherche et de tri de stdlib.h

| Fonction  | Description                                                                        |
| --------- | ---------------------------------------------------------------------------------- |
| `bsearch` | Recherche un élément dans un tableau trié en utilisant une fonction de comparaison |
| `qsort`   | Trie un tableau en utilisant un algorithme de tri rapide (quick sort)              |

Table: Opérations sur les nombres de stdlib.h

| Fonction | Description                                                                            |
| -------- | -------------------------------------------------------------------------------------- |
| `abs`    | Calcule la valeur absolue d'un entier (`int`)                                          |
| `labs`   | Calcule la valeur absolue d'un entier long (`long`)                                    |
| `llabs`  | Calcule la valeur absolue d'un long long (`long long`) (C99)                           |
| `div`    | Effectue une division entière et retourne le quotient et le reste pour les `int`       |
| `ldiv`   | Effectue une division entière pour les `long` et retourne quotient et reste            |
| `lldiv`  | Effectue une division entière pour les `long long` et retourne quotient et reste (C99) |

Table: Fonctions de conversion de chaînes de stdlib.h

| Fonction   | Description                                                                |
| ---------- | -------------------------------------------------------------------------- |
| `atof`     | Convertit une chaîne de caractères en double (`double`)                    |
| `atoi`     | Convertit une chaîne de caractères en entier (`int`)                       |
| `atol`     | Convertit une chaîne de caractères en long (`long`)                        |
| `atoll`    | Convertit une chaîne de caractères en long long (`long long`) (C99)        |
| `mbstowcs` | Convertit une chaîne multioctet en chaîne de caractères larges (`wchar_t`) |
| `mbtowc`   | Convertit un caractère multioctet en caractère large (`wchar_t`)           |
| `strtod`   | Convertit une chaîne en double (`double`)                                  |
| `strtof`   | Convertit une chaîne en float (`float`) (C99)                              |
| `strtol`   | Convertit une chaîne en long (`long`), avec une base personnalisable       |
| `strtold`  | Convertit une chaîne en long double (`long double`) (C99)                  |
| `strtoll`  | Convertit une chaîne en long long (`long long`) (C99)                      |
| `strtoul`  | Convertit une chaîne en unsigned long (`unsigned long`)                    |
| `strtoull` | Convertit une chaîne en unsigned long long (`unsigned long long`) (C99)    |
| `wcstombs` | Convertit une chaîne de caractères larges en chaîne multioctet             |
| `wctomb`   | Convertit un caractère large (`wchar_t`) en multioctet                     |

Table: Constantes et types de stdlib.h

| Constante/Type | Description                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------------- |
| `EXIT_SUCCESS` | Indique une terminaison réussie du programme (valeur utilisée avec `exit`)                          |
| `EXIT_FAILURE` | Indique une terminaison échouée du programme (valeur utilisée avec `exit`)                          |
| `NULL`         | Pointeur nul, utilisé pour initialiser ou tester des pointeurs                                      |
| `RAND_MAX`     | Valeur maximale que peut retourner `rand`                                                           |
| `MB_CUR_MAX`   | Taille maximale d'un caractère multioctet pour la locale courante                                   |
| `size_t`       | Type pour représenter des tailles et des dimensions                                                 |
| `div_t`        | Structure retournée par `div` contenant le quotient et le reste                                     |
| `ldiv_t`       | Structure retournée par `ldiv` contenant le quotient et le reste                                    |
| `lldiv_t`      | Structure retournée par `lldiv` (C99) contenant le quotient et le reste                             |
| `wchar_t`      | Type pour représenter un caractère large                                                            |
| `mbstate_t`    | Type utilisé pour conserver l'état entre conversions de caractères multioctets et caractères larges |

[](){#libc-stdnoreturn}
## `<stdnoreturn.h>`

Cette bibliothèque est apparue en C11 et elle introduit le type `noreturn` qui est utilisé pour indiquer qu'une fonction ne retourne jamais. Cela permet au compilateur d'optimiser le code en supprimant les instructions de retour de la fonction. En pratique, cela permet de gagner quelques cycles d'horloge. Voici un exemple d'utilisation :

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdnoreturn.h>

noreturn void exit_now(int i)
{
    if (i > 0)
        exit(i);

    // Si i <= 0, le comportement est indéfini
}

int main(void)
{
    puts("Se prépare à terminer le programme...");
    exit_now(2);
    puts("On sait que ce code n'est jamais exécuté.");
}
```

Avant C23, il fallait utiliser `_Noreturn`.

[](){#libc-string}
## `<string.h>`

La bibliothèque `<string.h>` contient des fonctions pour manipuler les chaînes de caractères. Les fonctions sont définies pour les chaînes de caractères ASCII uniquement. On distingue deux famille de fonctions, les `mem` qui manipulent des régions mémoires et les `str` qui manipulent des chaînes de caractères.

La table suivante résume les fonctions les plus utilisées. On notera que les lettres entre parenthèses indiquent les variantes des fonctions. La fonction `strcpy` existe en version `strncpy` qui permet de copier une chaîne en spécifiant la taille maximale à copier. On notera `n` pour les fonctions dont la taille maximum de la chaîne peut être spécifiée, `r` pour *reverse* et `c` pour *not in*.

Table: Fonctions sur les chaînes de caractères

| Fonction    | Description                                                 |
| ----------- | ----------------------------------------------------------- |
| `memset`    | Remplissage d'une région mémoire                            |
| `memcpy`    | Copie d'une région mémoire                                  |
| `memmove`   | Copie d'une région mémoire avec superposition               |
| `memcmp`    | Comparaison de deux régions mémoire                         |
| `memchr`    | Recherche d'un caractère dans une région mémoire            |
| `strlen`    | Longueur de la chaîne                                       |
| `str(n)cpy` | Copie d'une chaîne                                          |
| `str(n)cat` | Concaténation de deux chaînes                               |
| `str(n)cmp` | Comparaison de deux chaînes                                 |
| `str(r)chr` | Recherche d'un caractère dans une chaîne                    |
| `strstr`    | Recherche d'une sous-chaîne dans une chaîne                 |
| `strtok`    | Découpe une chaîne en morceaux                              |
| `strspn`    | Longueur du préfixe d'une chaîne                            |
| `strcspn`   | Longueur du préfixe qui ne contient pas certains caractères |
| `strpbrk`   | Recherche d'un caractère dans une liste                     |
| `strcoll`   | Comparaison de chaînes selon la locale                      |
| `strxfrm`   | Transformation de chaînes selon la locale                   |
| `strerror`  | Message d'erreur associé à un code d'erreur                 |

### `memset`

La fonction memset permet de remplir une région mémoire avec une valeur donnée. Son prototype est :

```c
void *memset(void *s, int c, size_t n);
```

Elle est utilisée principalement pour initialiser ou réinitialiser un tableau en une seule instruction qui sera plus performante qu'une boucle. L'exemple suivant initialise un tableau de 100 éléments avec la valeur 42:

```c
char array[100];
memset(array, 42, sizeof(array));
```

Notez que la valeur est un byte. Memset ne peut pas être utilisé pour initialiser un tableau avec une valeur de type `int` par exemple.

### `memcpy` et `memmove`

Les deux fonctions permettent de copier des régions mémoires d'une adresse à une autre. Leur prototype est le suivant :

```c
void *memmove(void *dest, const void *src, size_t n)
void *memcpy(void *dest, const void *src, size_t n)
```

La différence principale est que `memcpy` ne traite pas les cas où les deux régions mémoire se superposent. `memmove` est plus sûr et plus lent que `memcpy`. En effet, `memmove` doit vérifier si les deux régions mémoire se superposent et dans ce cas, elle doit copier les données dans un buffer temporaire avant de les copier dans la région de destination. `memcpy` ne fait pas cette vérification et copie directement les données.

Pour comprendre ce problème de superposition prenons l'exemple ci-dessous. La fonction `memcpy` est réimplémentée pour avoir une résultat prévisible. Un pointeur `p` est déclaré et un pointeur `q` correspond à l'adresse de `p` mais décalé de deux éléments. Les deux espaces mémoire se superposent donc. Après copie on devrait obtenir `12345` dans `q` mais après la copie mais on obtient `12121`. Il y a donc un problème.

```c
int mymemcpy(void *dest, const void *src, size_t n) {
   char *d = dest;
   const char *s = src;
   for (size_t i = 0; i < n; i++) d[i] = s[i];
   return 0;
}

int main() {
   char s[] = "12345..";
   char *p = s;
   char *q = p + 2;
   mymemcpy(q, p, 5);
   for (int i = 0; i < 5; i++) printf("%c", q[i]);
   printf("\n");
}
```

Pour vous en convaincre, vous pouvez vous aider de la figure suivante.

![memcpy](/assets/images/memcpy.drawio)

En réalité, le fonctionnement de `memcpy` n'est pas si simple. En effet, le compilateur peut optimiser le code et utiliser des instructions SIMD pour copier les données. Cela va également dépendre du niveau d'optimisation du compilateur. En exécutant le même code avec `memcpy`, je n'obtiens pas le même résultat, en observant le code assembleur généré pour `memcpy`, on observe que les premiers 4 octets sont copiés en une seule instruction, le cinquième octet est copié en une instruction séparée. Ce qui donne comme résultat `12343`.

```text
mov rcx, qword ptr [rbp - 128]  ; Charge l'adresse de destination (q) dans rcx
mov rdx, qword ptr [rbp - 120]  ; Charge l'adresse source (p) dans rdx
mov esi, dword ptr [rdx]        ; Charge les 4 premiers octets dans esi
mov dword ptr [rcx], esi        ; Copie ces 4 octets dans la destination
mov r8b, byte ptr [rdx + 4]     ; Charge le 5e octet de la source dans r8b
mov byte ptr [rcx + 4], r8b     ; Copie le 5e octet dans la destination
```

Pour s'affranchir de ce type de problème, il est préférable d'utiliser  `memmove` lorsque vous n'êtes pas sûr que les deux régions mémoire ne se superposent pas.

### `memcmp`

La fonction `memcmp` permet de comparer deux régions mémoires. Son prototype est :

```c
int memcmp(const void *s1, const void *s2, size_t n);
```

On utilise typiquement `memcmp` pour comparer deux structures. Il n'est en effet pas possible de comparer deux structures directement avec l'opérateur `==`. On utilisera plutôt :

```c
struct Person {
    char firstname[64];
    char lastname[64];
    Genre genre;
    int age;
};

Person p, q;
// Do something with p and q

if (memcmp(&p, &p, sizeof(struct Person)) == 0)
    printf("Les deux personnes sont identiques\n");
```

!!! bug "Comparaison de chaînes de caractères"

    Attention néanmoins au cas de figure donné. Les champs `firstname` et `lastname` sont des buffers de 64 caractères. Si les deux structures contiennent les mêmes prénoms et noms il n'y a aucune garantie que les deux structures soient égales. En effet, après le caractère `'\0'`, rien n'oblige l'utilisateur à remplir le reste du buffer avec des `'\0'`.

    Il serait ici préférable de tester individuellement les champs de la structure.

### `memchr` et `str(r)chr`

Les fonctions `memchr`, `strchr` et `strrchr` permettent de rechercher un caractère dans une région mémoire. Leurs prototypes sont :

```c
void *memchr(const void *s, int c, size_t n);
char *strchr(const char *s, int c);
char *strrchr(const char *s, int c);
```

Une utilisaiton typique de `strchr` ou `strrchr` est de rechercher l'occurence d'un caractère dans une chaîne de caractères. La fonction s'arrête dès qu'elle trouve le caractère recherché ou qu'elle atteint la fin de la chaîne.

```c
char *s = "Anticonsitutionnellement";
char *p = strchr(s, 'i');
assert(p != NULL); // Caractère trouvé
assert(*p == 'i'); // Caractère trouvé est 'i'
assert(p - s == 3); // Position de 'i' dans la chaîne

// Recherche depuis la fin
p = strrchr(s, 'i');
assert(p - s == 12); // Dernière position de 'i' dans la chaîne
```

Dans le cas de `memchr`, il est possible de chercher n'importe quelle valeur de byte, y compris `'\0'`. En revanche, il est nécessaire de spécifier la taille de la région mémoire à parcourir.

### `strlen`

La fonction `strlen` permet de calculer la longueur d'une chaîne de caractères. Son prototype est :

```c
size_t strlen(const char *s);
```

Son implémentation pourrait être la suivante :

```c
size_t strlen(const char *s) {
    size_t i = 0;
    while (s[i] != '\0') i++;
    return i;
}
```

### `str(n)cpy`

Les fonctions `strcpy` et `strncpy` permettent de copier une chaîne de caractères. Leur prototype sont :

```c
char *strcpy(char *dest, const char *src);
char *strncpy(char *dest, const char *src, size_t n);
```

La fonction `strcpy` copie la chaîne de caractères `src` dans `dest`. La fonction `strncpy` copie au maximum `n` caractères de `src` dans `dest`. Si la chaîne `src` est plus longue que `n`, la chaîne `dest` ne sera pas terminée par `'\0'`.

### `str(n)cat`

Les fonctions `strcat` et `strncat` permettent de concaténer deux chaînes de caractères. Leur prototype sont :

```c
char *strcat(char *dest, const char *src);
char *strncat(char *dest, const char *src, size_t n);
```

La fonction `strcat` concatène la chaîne de caractères `src` à la fin de `dest`. La fonction `strncat` concatène au maximum `n` caractères de `src` à la fin de `dest`. Si la chaîne `src` est plus longue que `n`, la chaîne `dest` ne sera pas terminée par `'\0'`.

```c
char dest[20] = "Hello, "; // dest est plus grand que src !
char src[] = "World!";
strcat(dest, src);
printf("%s\n", dest);  // Affiche "Hello, World!"
```

L'implémentation de `strcat` pourrait être la suivante :

```c
char *strcat(char *dest, const char *src) {
    while (*dest != '\0') ++dest;
    while ((*dest++ = *src++) != '\0');
    return dest;
}
```

### `strcmp` et `strncmp`

La fonction `strcmp` permet de comparer deux chaînes de caractères. Son prototype est :

```c
int strcmp(const char *s1, const char *s2);
```

Elle sera utilisée principalement pour comparer deux chaînes de caractères. Une utlisation typique est de tester si deux chaînes sont égales. Par exemple :

```c
char *owner = "John";
char user[64];
if (scanf("%63s", user) == 1 && memcmp(owner, user) == 0) {
    printf("Welcome John!\n");
}
```

Le `strncmp` permet de forcer la comparaison à s'arrêter après un certain nombre de caractères. C'est particulièrement utile pour le traitement des arguments de ligne de commande. Par exemple :

```c
if (strncmp(argv[1], "--filename=", 11) == 0) {
    printf("Ouverture du fichier %s\n", argv[1] + 11);
}
```

### `strtok`

La fonction `strtok` permet de découper une chaîne de caractères en morceaux. Il s'agit de l'abbréviation de *string token*. Son prototype est :

```c
char *strtok(char *str, const char *delim);
```

La première fois que la fonction est appelée, elle prend en paramètre la chaîne à découper. Les appels suivants doivent passer `NULL` en premier paramètre. La fonction retourne un pointeur sur le début du morceau suivant. La fonction modifie la chaîne passée en paramètre en insérant des `'\0'` à la place des délimiteurs.

```c
char s[] = "mais,ou,est,donc,or,ni,car";
char *token = strtok(s, ",");
while (token != NULL) {
    printf("%s\n", token);
    token = strtok(NULL, ",");
}
```

### `strspn` et `strcspn`

Les fonctions `strspn` et `strcspn` permettent de calculer la longueur du préfixe d'une chaîne qui contient ou ne contient pas certains caractères. Leur prototype est :

```c
size_t strspn(const char *s, const char *accept);
size_t strcspn(const char *s, const char *reject);
```

Une utilisation typique de `strspn` est de valider une chaîne de caractères. Par exemple, pour valider un nombre entier :

```c
char *s = "12345";
if (strspn(s, "0123456789") == strlen(s)) {
    printf("La chaîne %s est un nombre entier\n", s);
}
```

Inversement, `strcspn` permet de valider une chaîne de caractères qui ne contient pas certains caractères. Par exemple pour aider Georges Perec à écrire un lipogramme sans la lettre `e` :

```c
char *s = "La disparition";
if (strcspn(s, "e") == strlen(s)) {
    printf("La chaîne %s ne contient pas la lettre 'e'\n", s);
}
```

### `strpbrk`

La fonction `strpbrk` permet de rechercher un caractère dans une liste de caractères. Son prototype est :

```c
char *strpbrk(const char *s, const char *accept);
```

Elle retourne un pointeur sur le premier caractère de `s` qui appartient à `accept`. Par exemple, pour chercher les opérateurs utilisés dans une chaîne de caractères :

```c
char *s = "1 + 2 * 4 + 8";

while (s = strpbrk(s, "+-*/%%")) {
    printf("Opérateur trouvé : %c\n", *s);
    s++;
}
```

### `strcoll` et `strxfrm`

Les fonctions `strcoll` et `strxfrm` permettent de comparer des chaînes de caractères selon la locale. Elles sont l'abbréviation de *string collate* où *collate* fait référence au tri ou à l'ordre de classement des chaînes de caractères en fonction des conventions locales. `strxfrm` est l'abbréviation de *string transform* et permet de transformer une chaîne de caractères en une chaîne de caractères qui peut être comparée avec `strcmp`. Leur prototype est :

```c
int strcoll(const char *s1, const char *s2);
size_t strxfrm(char *dest, const char *src, size_t n);
```

Ces deux fonctions sont utilisées pour comparer des chaînes de caractères en tenant compte des conventions de tri locales, qui peuvent varier d'une langue ou d'un jeu de caractères à un autre. Elles sont principalement utilisées pour des opérations de tri ou de comparaison dans des contextes où il est important de respecter l'ordre défini par les paramètres régionaux (locales). Ces fonction utlisent donc les paramètres régionaux définis par la fonction `setlocale` de la bibliothèque `<locale.h>`.

Pourquoi ces deux fonctions étranges ? Comparer deux chaînes n'est pas facile surtout s'il y a des diacritiques. Selon la langue, les chaînes de caractères ne sont pas forcément comparées de la même manière. En français on considère alphabétiquement que `é` est juste après `e` dans l'alphabet, en anglais les deux lettres sont équivalentes. En suédois, les lettres `å`, `ä` sont placées après le `z`, et les règles sont nombreuses.

`strxfrm` permet de transformer une chaîne de caractères en une chaîne de caractères dite "collationnée" qui peut être comparée ensuite rapidement avec `strcmp`. Cela peut être utile lors de comparaison répétées.

Notons que ces fonctions ne sont plus vraiment utilisées car elles se limitent au jeux de caractères ISO-8859, et le support Unicode est limité. Pour une gestion correcte il vaut mieux faire appel à des bibliothèques plus spécialisées comme `ICU` qui offre la fonction `ucol_strcoll` pour comparer des chaînes de caractères Unicode.

### `strerror`

La fonction `strerror` permet de récupérer un message d'erreur associé à un code d'erreur. Son prototype est :

```c
char *strerror(int errnum);
```

Elle est utilisée principalement pour afficher des messages d'erreur associés à des codes d'erreur. Par exemple :

```c
FILE *f = fopen("file.txt", "r");
if (f == NULL) {
    fprintf(stderr, "Erreur lors de l'ouverture du fichier : %s\n",
      strerror(errno));
}
```

[](){#libc-tgmath}
## `<tgmath.h>`

La bibliothèque `<tgmath.h>` est une bibliothèque de type générique qui permet de définir des fonctions mathématiques qui acceptent des arguments de différents types. Par exemple, la fonction `sqrt` peut accepter un argument de type `float`, `double` ou `long double`.

Il est courant de ne pas utiliser la bonne fonction mathématique pour un type donné. Par exemple, on peut appeler `sqrt` avec un argument de type `float` alors que la fonction `sqrtf` est plus adaptée peut entraîner une perte de performance, l'inverse peut entraîner une perte de précision. La bibliothèque `<tgmath.h>` permet de résoudre ce problème en définissant des fonctions mathématiques génériques qui acceptent des arguments de différents types.

Cette [généricité][generickw] est permise à l'aide du mot clé `_Generic` introduit en C11.

La bibliothèque redéfini les fonctions mathématiques de la bibliothèque `<math.h>`, pour l'utiliser il suffit d'inclure l'en-tête `<tgmath.h>` à la place de `<math.h>`. Par exemple, pour calculer la racine carrée d'un nombre, on peut utiliser la fonction `sqrt` de la bibliothèque `<tgmath.h>` :


[](){#libc-threads}
## `<threads.h>`

La bibliothèque `<threads.h>` contient des fonctions pour créer et gérer des threads. Les threads sont aussi nommés des processus légers qui partagent le même espace mémoire. Un thread peut être vu comme un sous-programme parallèle tournant dans le même programme. Les fonctions offertes par le standard sont les suivantes :

Table: Fonctions sur les threads

| Fonction        | Description                               |
| --------------- | ----------------------------------------- |
| `thrd_create`   | Crée un nouveau thread                    |
| `thrd_exit`     | Termine le thread                         |
| `thrd_join`     | Attend la fin d'un thread                 |
| `thrd_sleep`    | Met le thread en sommeil                  |
| `thrd_yield`    | Passe la main à un autre thread           |
| `mtx_init`      | Initialise un mutex                       |
| `mtx_lock`      | Verrouille un mutex                       |
| `mtx_trylock`   | Tente de verrouiller un mutex             |
| `mtx_unlock`    | Déverrouille un mutex                     |
| `mtx_destroy`   | Détruit un mutex                          |
| `cnd_init`      | Initialise une variable de condition      |
| `cnd_signal`    | Signale une variable de condition         |
| `cnd_broadcast` | Signale toutes les variables de condition |
| `cnd_wait`      | Attend une variable de condition          |
| `cnd_destroy`   | Détruit une variable de condition         |

Pour plus de détails sur le fonctionnement des threads, vous pouvez consulter un cours spécialisé sur la programmation concurrente.

[](){#libc-time}
## `<time.h>`

La bibliothèque `<time.h>` contient des fonctions pour lire et convertir des dates et heures. Les fonctions sont définies pour les dates et heures en secondes depuis le 1er janvier 1970.

Table: Fonctions sur les dates et heures

| Fonction    | Description                                |
| ----------- | ------------------------------------------ |
| `time`      | Temps écoulé depuis le 1er janvier 1970    |
| `localtime` | Convertit le temps en heure locale         |
| `gmtime`    | Convertit le temps en heure UTC            |
| `asctime`   | Convertit le temps en chaîne de caractères |
| `ctime`     | Convertit le temps en chaîne de caractères |
| `strftime`  | Convertit le temps en chaîne de caractères |
| `mktime`    | Convertit une structure en temps           |
| `difftime`  | Différence entre deux temps                |
| `clock`     | Temps CPU utilisé par le programme         |

### Stucture `tm`

Les fonctions de date et d'heure utilisent la structure `tm` pour représenter les dates et heures. La structure est définie comme suit :

```c
struct tm {
    int tm_sec;   // Secondes (0-59)
    int tm_min;   // Minutes (0-59)
    int tm_hour;  // Heures (0-23)
    int tm_mday;  // Jour du mois (1-31)
    int tm_mon;   // Mois (0-11)
    int tm_year;  // Année - 1900
    int tm_wday;  // Jour de la semaine (0-6, dimanche = 0)
    int tm_yday;  // Jour de l'année (0-365)
    int tm_isdst; // Heure d'été (0, 1, -1)
};
```

### `time`

La fonction `time` permet de récupérer le temps écoulé depuis le 1er janvier 1970. Elle prend en paramètre un pointeur sur un `time_t` qui contiendra le temps écoulé. Ce dernier peut être `NULL` si on ne souhaite pas récupérer le temps. Le prototype de la fonction est le suivant :

```c
time_t time(time_t *t);
```

Un exemple d'utilisation est le suivant :

```c
time_t t;
time(&t);
printf("Time since 1st January 1970 : %ld seconds\n", t);

// Ou sans récupérer le temps
printf("Time since 1st January 1970 : %ld seconds\n", time(NULL));
```

Pourquoi le 1er janvier 1970 ? C'est une convention qui remonte aux premiers systèmes Unix. Le temps est stocké en secondes depuis cette date. C'est ce qu'on appelle le temps Unix ou temps POSIX.

!!! bug "Problème de l'an 2038"

    Le temps Unix est stocké sur 32 bits. Cela signifie que le temps Unix ne pourra plus être stocké sur 32 bits à partir du 19 janvier 2038. C'est ce qu'on appelle le bug de l'an 2038. Il est donc nécessaire de passer à un temps stocké sur 64 bits pour éviter ce problème.

    La taille de `time_t` dépend de l'implémentation. Sur la plupart des systèmes, `time_t` est un alias pour `long`. Sur les systèmes 64 bits, `time_t` est un alias pour `long long`.

Pourquoi avoir deux moyen de retourner le temps ? C'est une question de style. Certains préfèrent récupérer le temps dans une variable, d'autres préfèrent le récupérer directement sans variable intermédiaire.

### `localtime` et `gmtime`

Ces deux fonctions permettent de convertir un temps en heure locale ou en heure UTC. Leur prototype est le suivant :

```c
struct tm *localtime(const time_t *timep);
struct tm *gmtime(const time_t *timep);
```

`localtime` se base sur les paramètres régionaux fixés dans le système pour déterminer le fuseau horaire. Elle tient compte de l'ajustement pour l'heure d'été. `gmtime` en revanche se base sur le fuseau horaire UTC et ne tient pas compte de l'heure d'été.

Un exemple d'utilisation est le suivant :

```c
time_t t;
time(&t);
struct tm *tm = localtime(&t);
printf("Heure locale : %d:%d:%d\n", tm->tm_hour, tm->tm_min, tm->tm_sec);
```

### `asctime` et `ctime`

Les fonctions `asctime` et `ctime` permettent de convertir un temps en chaîne de caractères. Leur prototype est le suivant :

```c
char *asctime(const struct tm *tm);
char *ctime(const time_t *timep);
```

L'une prend en paramètre une structure `tm` et l'autre un temps. Elles retournent une chaîne de caractères représentant le temps. Par exemple :

```c
time_t current_time = time(NULL);
struct tm *local_tm = localtime(&current_time);
printf("Heure locale : %s", asctime(local_tm));
// Affiche par exemple "Sun Sep 16 01:03:52 1973\n" (locale en anglais)
//          "Dimanche 16 Septembre 01:03:52 1973\n" (locale en français)
```

Pour afficher l'heure actuelle, on peut également utiliser `ctime` :

```c
time_t current_time = time(NULL);
printf("Heure locale : %s", ctime(&current_time));
```

### `strftime`

La fonction `strftime` permet de convertir un temps en chaîne de caractères en utilisant un format spécifique. Son prototype est le suivant :

```c
size_t strftime(char *s, size_t maxsize, const char *format,
                const struct tm *tm);
```

Elle prend en paramètre un pointeur sur une chaîne de caractères, la taille de la chaîne, un format et une structure `tm`. Elle retourne le nombre de caractères écrits dans la chaîne.

Table: Format de strftime

| Format | Description                                      | Exemple de sortie |
| ------ | ------------------------------------------------ | ----------------- |
| `%A`   | Nom complet du jour de la semaine                | `"Sunday"`        |
| `%a`   | Nom abrégé du jour de la semaine                 | `"Sun"`           |
| `%B`   | Nom complet du mois                              | `"January"`       |
| `%b`   | Nom abrégé du mois                               | `"Jan"`           |
| `%C`   | Siècle (les deux premiers chiffres de l'année)   | `"20"` pour 2024  |
| `%d`   | Jour du mois (01-31)                             | `"17"`            |
| `%D`   | Date au format `MM/DD/YY`                        | `"09/17/24"`      |
| `%e`   | Jour du mois (1-31, avec espace si un chiffre)   | `"17"` ou `" 7"`  |
| `%F`   | Date au format `YYYY-MM-DD`                      | `"2024-09-17"`    |
| `%H`   | Heure (00-23, format 24 heures)                  | `"14"`            |
| `%I`   | Heure (01-12, format 12 heures)                  | `"02"`            |
| `%j`   | Jour de l'année (001-366)                        | `"260"`           |
| `%k`   | Heure (0-23, avec espace si chiffre)             | `" 2"`            |
| `%l`   | Heure (1-12, avec espace si chiffre, 12 heures)  | `" 2"`            |
| `%M`   | Minutes (00-59)                                  | `"05"`            |
| `%m`   | Mois (01-12)                                     | `"09"`            |
| `%n`   | Saut de ligne                                    | `"\n"`            |
| `%p`   | Indicateur AM ou PM                              | `"PM"`            |
| `%P`   | Indicateur am ou pm (minuscule)                  | `"pm"`            |
| `%r`   | Heure au format 12 heures (`hh:mm:ss` AM/PM)     | `"02:05:45 PM"`   |
| `%R`   | Heure au format 24 heures (`hh:mm`)              | `"14:05"`         |
| `%S`   | Secondes (00-60)                                 | `"45"`            |
| `%T`   | Heure au format 24 heures (`hh:mm:ss`)           | `"14:05:45"`      |
| `%u`   | Numéro du jour de la semaine (1-7, lundi = 1)    | `"2"` pour mardi  |
| `%U`   | Numéro de la semaine (00-53, dimanche)           | `"37"`            |
| `%W`   | Numéro de la semaine (00-53, lundi)              | `"37"`            |
| `%V`   | Numéro de la semaine ISO 8601 (01-53, lundi)     | `"38"`            |
| `%w`   | Numéro du jour de la semaine (0-6, dimanche = 0) | `"0"`             |
| `%x`   | Représentation locale de la date                 | `"09/17/24"`      |
| `%X`   | Représentation locale de l'heure                 | `"14:05:45"`      |
| `%y`   | Année (00-99, deux derniers chiffres)            | `"24"`            |
| `%Y`   | Année (tous les chiffres)                        | `"2024"`          |
| `%z`   | Décalage UTC (format +hhmm)                      | `"+0200"` (UTC+2) |
| `%Z`   | Nom du fuseau horaire                            | `"CEST"`          |
| `%%`   | Symbole `%`                                      | `"%"`             |

Queqlues notes sur les formats :

- Le `%S` peut retourner 60 lorsqu'une seconde intercalaire est insérée. Une second intercalaire est une seconde ajoutée à la fin d'une minute pour compenser la rotation de la Terre.
- La différence entre `%U` et `%W` est que `%U` commence la semaine le dimanche alors que `%W` commence la semaine le lundi. Les américains utilisent `%U` alors que les européens utilisent `%V`.

Voici un exemple d'utilisation :

```c
#include <stdio.h>
#include <time.h>

int main() {
    // Obtenir l'heure locale
    time_t current_time = time(NULL);
    struct tm *local_tm = localtime(&current_time);

    // Formater la date et l'heure
    char buffer[100];
    strftime(buffer, sizeof(buffer),
      "Aujourd'hui, c'est %A, %d %B %Y, et il est %T.", local_tm);

    printf("%s\n", buffer);
}
```

Il pourrait afficher:

```text
Aujourd'hui, c'est vendredi, 17 septembre 2024, et il est 14:05:45.
```

[](){#libc-uchar}

## `<uchar.h>`

Apparue avec la norme C11, cette bibliothèque contient des fonctions pour gérer les caractères Unicode. Elle contient des fonctions pour convertir des caractères en minuscules ou majuscules, pour tester si un caractère est un chiffre, une lettre, etc.

Un caractère multi-octets (*multibyte*) est un caractère qui nécessite plus d'un octet pour être stocké. Nous avons que la norme [Unicode][unicode] définit un jeu de caractères universel qui peut être représenté en binaire avec des caractères de 8-bit (UTF-8). Cela permet de stocker théoriquement jusqu'à 4 294 967 295 caractères différents.

Le C étant un langage ancien, il a été conçu à une époque où seul la table ASCII existait. Néanmoins, certaines langues comme le chinois nécessitaient plus de 256 caractères. Pour cela, le C a introduit le concept de caractères larges (*wide characters*) qui étaient initialement stockés sur 16-bits (`short`). Néanmoins, avec l'arrivée de l'Unicode, il n'est pas rare de trouver des caractères qui nécessitent 32-bits. Or, les *wide-chars* historiques du C ne sont que sur 16-bits (sous Windows) et 32-bits (sous Unix). Pour palier à ce problème de portabilité, la norme C11 a introduit la bibliothèque `<uchar.h>` qui permet de gérer les caractères Unicode convenablement.

La bibliothèque définit deux types supplémentaires:

```c
char16_t; // 16-bit pour l'UTF-16
char32_t; // 32-bit pour l'UTF-32
```

Contrairement à UTF-8 qui est un encodage variable : de 1 à 4 bytes, l'UTF-16 et l'UTF-32 sont des encodages fixes (à moins d'utiliser des *surrogatges*). Comme la plupart des systèmes utilisent massivement l'UTF-8, la bibliothèque offre des fonctions de conversion entre les différents encodages.

Table: Fonctions de conversion de caractères

| Fonction   | Description                                |
| ---------- | ------------------------------------------ |
| `c16rtomb` | Convertit un caractère 16-bit en UTF-8     |
| `c32rtomb` | Convertit un caractère 32-bit en UTF-8     |
| `mbrtoc16` | Convertit un caractère UTF-8 en 16-bit     |
| `mbrtoc32` | Convertit un caractère UTF-8 en 32-bit     |
| `c16rtowc` | Convertit un caractère 16-bit en wide char |
| `c32rtowc` | Convertit un caractère 32-bit en wide char |
| `wctoc16`  | Convertit un wide char en 16-bit           |
| `wctoc32`  | Convertit un wide char en 32-bit           |

Le standard C nomme `mb` (`multibyte`) pour se référer à UTF-8.

L'inconvénient majeur d'UTF-8 c'est qu'il est impossible d'éditer un caractère à un endroit précis sans devoir possiblement décaler tous les caractères suivants. Remplacer un `e` (stocké sur 1 byte) par un émoji (stocké sur 4 bytes), nécessite de décaler tout le texte de 3 bytes. Suivant la taille de la chaîne cela peut être fastidieux. C'est pourquoi l'UTF-32 est souvent utilisé pour les traitements internes. On perd de la place mémoire car un texte en UTF-32 est jusqu'à 4 fois plus gros qu'en UTF-8, mais on gagne en temps de traitement car aucun déclage n'est nécessaire. En outre, le processeur étant plus à l'aise avec les données alignées sur 32-bits, les traitements sont plus rapides.

Prenons l'exemple d'un algorithme qui inverse une chaîne de caractères UTF-8 et affiche le résultat. Sans cette bibliothèque, il n'est pas trivial de le faire car les caractères unicode peuvent être stockés sur plusieurs bytes. Ici on commence par convertir la chaîne UTF-8 en UTF-32 pour avoir une chaîne simple à traiter, on inverse ensuite la chaîne UTF-32, puis on la reconvertit en UTF-8 pour l'affichage. Une implémentation est donnée dans la section [algorithmes][utf8-reverse].

[](){#libc-wchar}

## `<wchar.h>`

Cette bibliothèque supplémente d'autres bibliothèques pour gérer les caractères larges (wide characters). Ci-dessous la table d'équilvalence:

Table: Fonctions liées aux caractères larges

| Fonction   | Description                                    | Équivalent |
| ---------- | ---------------------------------------------- | ---------- |
| `wcstol`   | Convertit une chaîne en long                   | `strtol`   |
| `wcstoul`  | Convertit une chaîne en unsigned long          | `strtoul`  |
| `wcstoll`  | Convertit une chaîne en long long              | `strtoll`  |
| `wcstoull` | Convertit une chaîne en unsigned long long     | `strtoull` |
| `wcstof`   | Convertit une chaîne en float                  | `strtof`   |
| `wcstod`   | Convertit une chaîne en double                 | `strtod`   |
| `wcstold`  | Convertit une chaîne en long double            | `strtold`  |
| `wcscpy`   | Copie une chaîne                               | `strcpy`   |
| `wcsncpy`  | Copie une chaîne                               | `strncpy`  |
| `wcscat`   | Concatène deux chaînes                         | `strcat`   |
| `wcsncat`  | Concatène deux chaînes                         | `strncat`  |
| `wcscmp`   | Compare deux chaînes                           | `strcmp`   |
| `wcsncmp`  | Compare deux chaînes                           | `strncmp`  |
| `wcschr`   | Recherche un caractère dans une chaîne         | `strchr`   |
| `wcsrchr`  | Recherche un caractère dans une chaîne         | `strrchr`  |
| `wcscoll`  | Compare deux chaînes                           | `strcoll`  |
| `wcslen`   | Calcule la longueur d'une chaîne               | `strlen`   |
| `wcsxfrm`  | Transforme une chaîne                          | `strxfrm`  |
| `wmemcmp`  | Compare deux régions mémoire                   | `memcmp`   |
| `wmemchr`  | Recherche un caractère dans une région mémoire | `memchr`   |
| `wmemcpy`  | Copie une région mémoire                       | `memcpy`   |
| `wmemmove` | Copie une région mémoire                       | `memmove`  |
| `wmemset`  | Remplit une région mémoire                     | `memset`   |


[](){#libc-wctype}
[](){#libc-ctype}

## `<(w)ctype.h>`

La bibliothèque `<ctype.h>` contient des fonctions pour tester et convertir des caractères. Les fonctions sont définies pour les caractères ASCII uniquement, elle ne s'applique pas aux caractères Unicode, ni aux caractères étendus (au-delà de 127). La bibliothèque `<wctype.h>` est similaire mais pour les caractères larges (wide characters).

Table: Fonctions de test de caractères

| ctype      | wctype      | Description                            |
| ---------- | ----------- | -------------------------------------- |
| `isalnum`  | `iswalnum`  | une lettre ou un chiffre               |
| `isalpha`  | `iswalpha`  | une lettre                             |
| `iscntrl`  | `iswcntrl`  | un caractère de commande               |
| `isdigit`  | `iswdigit`  | un chiffre décimal                     |
| `isgraph`  | `iswgraph`  | un caractère imprimable ou le blanc    |
| `islower`  | `iswlower`  | une lettre minuscule                   |
| `isprint`  | `iswprint`  | un caractère imprimable (pas le blanc) |
| `ispunct`  | `iswpunct`  | un caractère imprimable pas isalnum    |
| `isspace`  | `iswspace`  | un caractère d'espace blanc            |
| `isupper`  | `iswupper`  | une lettre majuscule                   |
| `isxdigit` | `iswxdigit` | un chiffre hexadécimal                 |

En plus de ces fonctions de test, il existe des fonctions de conversion de casse définies dans `<wctype.h>` :

Table: Fonctions de conversion de casse

| Fonction    | Description                                       |
| ----------- | ------------------------------------------------- |
| `towlower`  | Convertit une lettre en minuscule                 |
| `towupper`  | Convertit une lettre en majuscule                 |
| `towctrans` | Convertit un caractère selon la locale `LC_CTYPE` |



## Exercices de révision

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
