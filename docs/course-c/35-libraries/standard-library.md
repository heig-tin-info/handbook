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

#### Fonctons Mathématiques

La bibliothèque mathématique est une des plus utilisées. Elle contient des fonctions pour les opérations mathématiques de base. Les fonctions sont définies pour les types `float`, `double` et `long double` avec les préfixes `f`, `l` et sans préfixe respectivement. Le fichier d'en-tête est le suivant et le flag de compilation est `-lm` :

```c
#include <math.h>
```

Table: Constantes mathématiques

| Constantes  | Description                  |
| ----------- | ---------------------------- |
| `M_PI`      | Valeur de :math:`\pi`        |
| `M_E`       | Valeur de :math:`e`          |
| `M_SQRT1_2` | Valeur de :math:`1/\sqrt(2)` |

!!! warning "Windows"

    Attention, ces constantes ne sont pas définies par le standard C, mais par le standard POSIX. Il est donc possible que certaines implémentations ne les définissent pas, en particulier sous Windows.

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

Le standard C99 a introduit l'en-tête `<tgmath.h>` qui donne accès à des fonctions génériques. Par exemple, `sin` peut être utilisé pour des `float`, `double` et `long double` sans avoir à choisir le nom de la fonction (`sinf`, `sin`, `sinl`), en outre les types complexes sont également supportés comme `csin` pour les complexes.

#### Chaînes de caractères

La bibliothèque `<string.h>` contient des fonctions pour manipuler les chaînes de caractères. Les fonctions sont définies pour les chaînes de caractères ASCII uniquement. On distingue deux famille de fonctions, les `mem` qui manipulent des régions mémoires et les `str` qui manipulent des chaînes de caractères. Le fichier d'en-tête est le suivant :

```c
#include <string.h>
```

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

##### `memset`

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

##### `memcpy` et `memmove`

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

##### `memcmp`

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

##### `memchr` et `str(r)chr`

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

##### `strlen`

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

##### `str(n)cpy`

Les fonctions `strcpy` et `strncpy` permettent de copier une chaîne de caractères. Leur prototype sont :

```c
char *strcpy(char *dest, const char *src);
char *strncpy(char *dest, const char *src, size_t n);
```

La fonction `strcpy` copie la chaîne de caractères `src` dans `dest`. La fonction `strncpy` copie au maximum `n` caractères de `src` dans `dest`. Si la chaîne `src` est plus longue que `n`, la chaîne `dest` ne sera pas terminée par `'\0'`.

##### `str(n)cat`

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

##### `strcmp` et `strncmp`

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

##### `strtok`

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

##### `strspn` et `strcspn`

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

##### `strpbrk`

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

##### `strcoll` et `strxfrm`

Les fonctions `strcoll` et `strxfrm` permettent de comparer des chaînes de caractères selon la locale. Elles sont l'abbréviation de *string collate* où *collate* fait référence au tri ou à l'ordre de classement des chaînes de caractères en fonction des conventions locales. `strxfrm` est l'abbréviation de *string transform* et permet de transformer une chaîne de caractères en une chaîne de caractères qui peut être comparée avec `strcmp`. Leur prototype est :

```c
int strcoll(const char *s1, const char *s2);
size_t strxfrm(char *dest, const char *src, size_t n);
```

Ces deux fonctions sont utilisées pour comparer des chaînes de caractères en tenant compte des conventions de tri locales, qui peuvent varier d'une langue ou d'un jeu de caractères à un autre. Elles sont principalement utilisées pour des opérations de tri ou de comparaison dans des contextes où il est important de respecter l'ordre défini par les paramètres régionaux (locales). Ces fonction utlisent donc les paramètres régionaux définis par la fonction `setlocale` de la bibliothèque `<locale.h>`.

Pourquoi ces deux fonctions étranges ? Comparer deux chaînes n'est pas facile surtout s'il y a des diacritiques. Selon la langue, les chaînes de caractères ne sont pas forcément comparées de la même manière. En français on considère alphabétiquement que `é` est juste après `e` dans l'alphabet, en anglais les deux lettres sont équivalentes. En suédois, les lettres `å`, `ä` sont placées après le `z`, et les règles sont nombreuses.

`strxfrm` permet de transformer une chaîne de caractères en une chaîne de caractères dite "collationnée" qui peut être comparée ensuite rapidement avec `strcmp`. Cela peut être utile lors de comparaison répétées.

Notons que ces fonctions ne sont plus vraiment utilisées car elles se limitent au jeux de caractères ISO-8859, et le support Unicode est limité. Pour une gestion correcte il vaut mieux faire appel à des bibliothèques plus spécialisées comme `ICU` qui offre la fonction `ucol_strcoll` pour comparer des chaînes de caractères Unicode.

##### `strerror`

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

#### Date et heure

La bibliothèque `<time.h>` contient des fonctions pour lire et convertir des dates et heures. Les fonctions sont définies pour les dates et heures en secondes depuis le 1er janvier 1970. Le fichier d'en-tête est le suivant :

```c
#include <time.h>
```

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

##### Stucture `tm`

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

##### `time`

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

##### `localtime` et `gmtime`

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

##### `asctime` et `ctime`

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

##### `strftime`

La fonction `strftime` permet de convertir un temps en chaîne de caractères en utilisant un format spécifique. Son prototype est le suivant :

```c
size_t strftime(char *s, size_t maxsize, const char *format,
                const struct tm *tm);
```

Elle prend en paramètre un pointeur sur une chaîne de caractères, la taille de la chaîne, un format et une structure `tm`. Elle retourne le nombre de caractères écrits dans la chaîne.

Table: Format de `strftime`

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
| `%r`   | Heure au format 12 heures (hh:mm:ss AM/PM)       | `"02:05:45 PM"`   |
| `%R`   | Heure au format 24 heures (hh:mm)                | `"14:05"`         |
| `%S`   | Secondes (00-60)                                 | `"45"`            |
| `%T`   | Heure au format 24 heures (hh:mm:ss)             | `"14:05:45"`      |
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

#### Types de données

La bibliothèque `<ctype.h>` contient des fonctions pour tester et convertir des caractères. Les fonctions sont définies pour les caractères ASCII uniquement, elle ne s'applique pas aux caractères Unicode, ni aux caractères étendus (au-delà de 127).

```c
#include <ctype.h>
```

Table: Fonctions de test de caractères

| Fonction   | Description                            |
| ---------- | -------------------------------------- |
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

| Constante     | Valeur        |
| ------------- | ------------- |
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
