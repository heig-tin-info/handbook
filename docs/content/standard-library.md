# Bibliothèques

![Bibliothèque du Trinity College de Dublin](../assets/images/library.jpg)

Une bibliothèque informatique est une collection de fichiers comportant des fonctionnalités logicielles prêtes à l'emploi. La fonction `printf` est une de ces fonctionnalités et offerte par le header `<stdio.h>` faisant partie de la bibliothèque `libc6`.

L'anglicisme *library*, plus court à prononcer et à écrire est souvent utilisé en lieu et place de bibliothèque tant il est omniprésent dans le monde logiciel. Le terme `<stdlib.h>` étant la concaténation de *standard library* par exemple. Notez que librairie n'est pas la traduction correcte de *library* qui est un [faux ami](https://fr.wikipedia.org/wiki/Faux-ami).

Une *library*, à l'instar d'une bibliothèque, contient du contenu (livre écrit dans une langue donnée) et un index (registre). En informatique il s'agit d'un fichier binaire compilé pour une architecture donnée ainsi qu'un ou plusieurs fichiers d'en-tête (*header*) contenant les définitions de cette bibliothèque.

Dans ce chapitre on donnera plusieurs exemples sur un environnement POSIX. Sous Windows, les procédures choses sont plus compliquées, mais les concepts restent les mêmes.

## Exemple: libgmp

Voyons ensemble le cas de [libgmp](https://packages.debian.org/buster/libgmp-dev). Il s'agit d'une bibliothèque de fonctionnalités très utilisée et permettant le calcul arithmétique multiprécision en C. En observant le détail du paquet logiciel Debian on peut lire que `libgmp` est disponible pour différentes architectures `amd64`, `arm64`, `s390x`, `i386`, ... Un développement sur un Raspberry-PI nécessitera `arm64` alors qu'un développement sur un PC utilisera `amd64`. En [cliquant](https://packages.debian.org/buster/amd64/libgmp-dev/filelist) sur l'architecture désirée on peut voir que ce paquet se compose des fichiers suivants (list réduite aux fichiers concernant C :

```
# Fichier d'en-tête C
/usr/include/x86_64-linux-gnu/gmp.h

# Bibliothèque compilée pour l'architecture visée (ici amd64)
/usr/lib/x86_64-linux-gnu/libgmp.a
/usr/lib/x86_64-linux-gnu/libgmp.so

# Documentation de la libgmp
/usr/share/doc/libgmp-dev/AUTHORS
/usr/share/doc/libgmp-dev/README
/usr/share/doc/libgmp-dev/changelog.gz
/usr/share/doc/libgmp-dev/copyright
```

On a donc :

`gmp.h`

: Fichier d'en-tête à include dans un fichier source pour utiliser les fonctionnalités

`libgmp.a`

: Bibliothèque **statique** qui contient l'implémentation en langage machine des fonctionnalités à référer au *linker* lors de la compilation

`libgmp.so`

: Bibliothèque **dynamique** qui contient aussi l'implémentation en langage machine des fonctionnalités

Imaginons que l'on souhaite bénéficier des fonctionnalités de cette bibliothèque pour le calcul d'orbites pour un satellite d'observation de Jupyter. Pour prendre en main cet *libary* on écrit ceci :

```c
--8<-- "docs/assets/src/gmp.c"
```

Puis on compile :

```console
$ gcc gmp.c
gmp.c:1:10: fatal error: gmp.h: No such file or directory
#include <gmp.h>
        ^~~~~~~
compilation terminated.
```

Aïe! La bibliothèque n'est pas installée.

Debian/Ubuntu
: ```console
  $ sudo apt-get install libgmp-dev
  ```

Mac OS X
: ```console
  $ brew install gmp
  ```

Windows
: ```console
  ERREUR 404
  ```

Deuxième tentative :

```console
$ gcc gmp.c
/tmp/cc2FxDSy.o: In function `main':
gmp.c:(.text+0x6f): undefined reference to `__gmpz_init'
gmp.c:(.text+0x80): undefined reference to `__gmpz_set_ui'
gmp.c:(.text+0x96): undefined reference to `__gmpz_set_str'
gmp.c:(.text+0xb3): undefined reference to `__gmpz_out_str'
gmp.c:(.text+0xd5): undefined reference to `__gmpz_add_ui'
gmp.c:(.text+0xf2): undefined reference to `__gmpz_out_str'
gmp.c:(.text+0x113): undefined reference to `__gmpz_mul'
gmp.c:(.text+0x130): undefined reference to `__gmpz_out_str'
gmp.c:(.text+0x146): undefined reference to `__gmpz_clear'
collect2: error: ld returned 1 exit status
```

Cette fois-ci on peut lire que le compilateur à fait sont travail, mais ne parvient pas à trouver les symboles des fonctions que l'on utilise p.ex. `__gmpz_add_ui`. C'est normal parce que l'on n'a pas renseigné la bibliothèque à utiliser.

```console
$ gcc gmp.c -lgmp

$ ./a.out
19810983098510928501928599999999999990
19810983098510928501928600000000000002
392475051329485669436248957939688603493163430354043714007714400000000000004
```

Cette manière de faire utilise le fichier `libgmp.so` qui est la bibliothèque **dynamique**, c'est-à-dire que ce fichier est nécessaire pour que le programme puisse fonctionner. Si je donne mon exécutable à un ami qui n'as pas install libgmp sur son ordinateur, il ne sera pas capable de l'exécuter.

Alternativement on peut compiler le même programme en utilisant la librairie **statique**

```console
$ gcc gmp.c /usr/lib/x86_64-linux-gnu/libgmp.a
```

C'est-à-dire qu'à la compilation toutes les fonctionnalités ont été intégrées à l'exécutable et il ne dépend de plus rien d'autre que le système d'exploitation. Je peux prendre ce fichier le donner à quelqu'un qui utilise la même architecture et il pourra l'exécuter. En revanche, la taille du programme est plus grosse :

```console
# ~167 KiB
$ gcc gmp.c -l:libgmp.a
$ size a.out
text    data     bss     dec     hex filename
155494     808      56  156358   262c6 ./a.out

# ~8.5 KiB
$ gcc gmp.c -lgmp
$ size a.out
text    data     bss     dec     hex filename
2752     680      16    3448     d78 ./a.out
```

## Exemple: ncurses

La bibliothèque [ncurses](https://fr.wikipedia.org/wiki/Ncurses) traduction de *nouvelles malédictions* est une évolution de [curses](https://fr.wikipedia.org/wiki/Curses) développé originellement par [Ken Arnold](https://en.wikipedia.org/wiki/Ken_Arnold) . Il s'agit d'une bibliothèque pour la création d'interfaces graphique en ligne de commande, toujours très utilisée.

La bibliothèque permet le positionnement arbitraire dans la fenêtre de commande, le dessin de fenêtres, de menus, d'ombrage sous les fenêtres, de couleurs ...

![Exemple d'interface graphique écrite avec `ncurses`. Ici la configuration du noyau Linux.](../assets/images/linux-menuconfig.png)

L'écriture d'un programme Hello World avec cette bibliothèque pourrait être :

```c
#include <ncurses.h>

int main()
{
    initscr();              // Start curses mode
    printw("hello, world"); // Print Hello World
    refresh();              // Print it on to the real screen
    getch();                    // Wait for user input
    endwin();               // End curses mode

    return 0;
}
```

La compilation n'est possible que si :

1. La bibliothèque est installée sur l'ordinateur
2. Le lien vers la bibliothèque dynamique est mentionné à la compilation

```console
$ gcc ncurses-hello.c -ohello -lncurses
```

## Bibliothèques statiques

Une *static library* est un fichier binaire compilé pour une architecture donnée et portant les extensions :

- `.a` sur un système POSIX (Android, Mac OS, Linux, Unix)
- `.lib` sous Windows

Une bibliothèque statique n'est rien d'autre qu'une archive d’un ou plusieurs objets. Rappelons-le un objet est le résultat d'une compilation.

Par exemple si l'on souhaite écrire une bibliothèque statique pour le [code de César](https://fr.wikipedia.org/wiki/Chiffrement_par_d%C3%A9calage) on écrira un fichier source `caesar.c`:

```c title="caesar.c"
--8<-- "docs/assets/src/caesar.c"
```

Ainsi qu'un fichier d'en-tête `caesar.h`:

```c title="caesar.h"
--8<-- "docs/assets/src/caesar.h"
```

Pour créer une bibliothèque statique rien de plus facile. Le compilateur crée l'objet, l'archiver crée l'amalgame :

```console
$ gcc -c -o caesar.o caesar.c
$ ar rcs caesar.a caesar.o
```

Puis il suffit d'écrire un programme pour utiliser cette bibliothèque :

```c title="encrypt.c"
--8<-- "docs/assets/src/encrypt.c"
```

Et de compiler le tout. Ici on utilise `-I.` et `-L.` pour dire au compilateur de chercher le fichier d'en-tête et la bibliothèque dans le répertoire courant.

```console
$ gcc encrypt.c -I. -L. -l:caesar.a
```

La procédure sous Windows est plus compliquée et ne sera pas décrite ici.

## Bibliothèques dynamiques

Une *dynamic library* est un fichier binaire compilé pour une architecture donnée et portant les extensions :

- `.so` sur un système POSIX (Android, Mac OS, Linux, Unix)
- `.dll` sous Windows

L'avantage principal est de ne pas charger pour rien chaque exécutable compilé de fonctionnalités qui pourraient très bien être partagées. L'inconvénient est que l'utilisateur du programme doit impérativement avoir installé la bibliothèque. Dans un environnement POSIX les bibliothèques dynamiques disposent d'un emplacement spécifique ou elles sont toute stockées. Malheureusement sous Windows le consensus est plus partagé et il n'est pas rare de voir plusieurs applications différentes héberger une copie des *dll* localement si bien que l'avantage de la bibliothèque dynamique est anéanti par un défaut de cohérence.

Reprenant l'exemple de César vu plus haut, on peut créer une bibliothèque dynamique :

```console
$ gcc -shared -o libcaesar.so caesar.o
```

Puis compiler notre programme pour utiliser cette bibliothèque. Avec une bibliothèque dynamique, il faut spécifier au compilateur quels sont les chemins vers lesquels il pourra trouver les bibliothèques installées. Comme ici on ne souhaite pas **installer** la bibliothèque et la rendre disponible pour tous les programmes, il faut ajouter aux chemins par défaut, le chemin local `$(pwd .)`, en créant une **variable d'environnement** nommée `LIBRARY_PATH`.

```console
$ LIBRARY_PATH=$(pwd .) gcc encrypt.c -I. -lcaesar
```

Le problème est identique à l'exécution, car il faut spécifier (ici avec `LD_LIBRARY_PATH`) le chemin ou le système d'exploitation s'attendra à trouver la bibliothèque.

```console
$ LD_LIBRARY_PATH=$(pwd .) ./a.out ferrugineux
sreehtvarhk
```

Car sinon c'est l'erreur :

```console
$ LIBRARY_PATH=$(pwd .) ./a.out Hey?
./a.out: error while loading shared libraries: libcaesar.so :
cannot open shared object file: No such file or directory
```

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

!!! exercise Arc-cosinus

    La fonction Arc-Cosinus ``acos`` est-elle définie par le standard et dans quel fichier d'en-tête est-elle déclarée? Un fichier d'en-tête se termine avec l'extension ``.h``.

    ??? solution

        En cherchant ``man acos header`` dans Google, on trouve que la fonction ``acos`` est définie dans le header ``<math.h>``.

        Une autre solution est d'utiliser sous Linux la commande ``apropos``:

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

        La réponse est donc ``<math.h>``.

        Sous Windows avec Visual Studio, il suffit d'écrire ``acos`` dans un fichier source et d'appuyer sur ``F1``. L'IDE redirige l'utilisateur sur l'aide Microsoft [acos-acosf-acosl](https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/acos-acosf-acosl) qui indique que le header source est ``<math.h>``.
```

!!! exercise "Date"

    Lors du formatage d'une date, on y peut y lire ``%w``, par quoi sera remplacé ce *token* ?


### Fonctions d'intérêt

Il serait inutile ici de lister toutes les fonctions, les bibliothèques standard étant largement documentées sur internet. Il ne fait aucun doute que le développeur sera trouver comment calculer un sinus avec la fonction `sin`. Néanmoins l'existence de certaines fonctions peut passer inaperçues et c'est de celles-ci don't j'aimerais parler.

#### Math

Table: Constantes mathématiques

| Constantes       | Description                                           |
|------------------|-------------------------------------------------------|
| ``M_PI``         | Valeur de :math:`\pi`                                 |
| ``M_E``          | Valeur de :math:`e`                                   |
| ``M_SQRT1_2``    | Valeur de :math:`1/\sqrt(2)`                          |

Table: Fonctions mathématiques

| Fonction         | Description                                           |
|------------------|-------------------------------------------------------|
| ``exp(x)``       | Exponentielle :math:`e^x`                             |
| ``ldexp(x,n)``   | Exposant d'un nombre flottant :math:`x\cdot2^n`       |
| ``log(x)``       | Logarithme binaire :math:`\log_{2}(x)`                |
| ``log10(x)``     | Logarithme décimal :math:`\log_{10}(x)`               |
| ``pow(x,y)``     | Puissance :math:`x^y`                                 |
| ``sqrt(x)``      | Racine carrée :math:`\sqrt(x)`                        |
| ``cbrt(x)``      | Racine cubique :math:`\sqrt[3](x)`                    |
| ``hypot(x,y)``   | Hypoténuse optimisé :math:`\sqrt(x^2 + y^2)`          |
| ``ceil``         | Arrondi à l'entier supérieur                          |
| ``floor``        | Arrondi à l'entier inférieur                          |
```

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

| Fonction     | Description                              |
|--------------|------------------------------------------|
| ``isalnum``  | une lettre ou un chiffre                 |
| ``isalpha``  | une lettre                               |
| ``iscntrl``  | un caractère de commande                 |
| ``isdigit``  | un chiffre décimal                       |
| ``isgraph``  | un caractère imprimable ou le blanc      |
| ``islower``  | une lettre minuscule                     |
| ``isprint``  | un caractère imprimable (pas le blanc)   |
| ``ispunct``  | un caractère imprimable pas isalnum      |
| ``isspace``  | un caractère d'espace blanc              |
| ``isupper``  | une lettre majuscule                     |
| ``isxdigit`` | un chiffre hexadécimal                   |

#### Limites

Table: Valeurs limites pour les entiers signés et non signés

| Constante        | Valeur        |
|------------------|---------------|
| ``SCHAR_MIN``   | -128          |
| ``SCHAR_MAX``   | +127          |
| ``CHAR_MIN``    | 0             |
| ``CHAR_MAX``    | 255           |
| ``SHRT_MIN``    | -32768        |
| ``SHRT_MAX``    | +32767        |
| ``USHRT_MAX``   | 65535         |
| ``LONG_MIN``    | -2147483648   |
| ``LONG_MAX``    | +2147483647   |
| ``ULONG_MAX``   | +4294967295   |
| ``DBL_MAX``     | 1E+37 ou plus |
| ``DBL_EPSILON`` | 1E-9 ou moins |

## Autres bibliothèques

- GNU C Library ([glibc](https://www.gnu.org/software/libc/))
  - C11
  - POSIX.1-2008
  - IEEE 754-2008

### POSIX C Library

Le standard C ne définit que le minimum vital et qui est valable sur toutes les architectures pour autant que la *toolchain* soit compatible **C99**. Il existe néanmoins toute une collection d'autres fonctions manquantes :

- La communication entre les processus (deux programmes qui souhaitent communiquer entre eux)

    - `<sys/socket.h>`
    - `<sharedmemory.h>`

- La communication sur le réseau e.g. internet

    - `<sys/socket.h>`
    - `<arpa/inet.h>`
    - `<net/if.h>`

- Les tâches

    - `<thread.h>`

- Les traductions de chaînes p.ex. français vers anglais

    - `<iconv.h>`

- Les fonctions avancées de recherche de texte

    - `<regex.h>`

- Le log centralisé des messages (d'erreur)

    - `<syslog.h>`

Toutes ces bibliothèques additionnelles ne sont pas nécessairement disponibles sur votre ordinateur ou pour le système cible, surtout si vous convoitez une application *bare-metal*. Elles dépendent grandement du système d'exploitation utilisé, mais une tentative de normalisation existe et se nomme [POSIX](https://en.wikipedia.org/wiki/POSIX) (ISO/IEC 9945).

Généralement la vaste majorité des distributions Linux et Unix sont compatibles avec le standard POSIX et les bibliothèques ci-dessus seront disponibles à moins que vous ne visiez une architecture différente de celle sur laquelle s'exécute votre compilateur.

Le support POSIX sous Windows (Win32) n'est malheureusement que partiel et il n'est pas standardisé.

Un point d'entrée de l'API POSIX est la bibliothèque `<unistd.h>`.

### GNU GLIBC

La bibliothèque portable [GNULIB](https://www.gnu.org/software/gnulib/) est la bibliothèque standard référencée sous Linux par `libc6`.

### Windows C library

La bibliothèque Windows [Windoes API](https://docs.microsoft.com/en-us/windows/win32/apiindex/windows-api-list) offre une interface au système de fichier, au registre Windows, aux imprimantes, à l'interface de fenêtrage, à la console et au réseau.

L'accès à cet API est offert par un unique point d'entrée [windows.h](https://en.wikipedia.org/wiki/Windows.h) qui regroupe certains en-têtes standards (`<stdarg.h>`, `<string.h>`, ...), mais pas tous (😔) ainsi que les en-têtes spécifiques à Windows tels que :

`<winreg.h>`

: Pour l'accès au registre Windows

`<wincon.h>`

: L'accès à la console

La documentation est disponible en ligne depuis le site de Microsoft, mais n'est malheureusement pas complète et souvent il est difficile de savoir sur quel site trouver la bonne version de la bonne documentation. Par exemple, il n'y a aucune documentation claire de `LSTATUS` pour la fonction [RegCreateKeyExW](https://docs.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regcreatekeyexw) permettant de créer une entrée dans la base de registre.

Un bon point d'entrée est le [Microsoft API and reference catalog](https://msdn.microsoft.com/library).

Quelques observations :

- Officiellement Windows est compatible avec C89 (ANSI C) (c.f. [C Language Reference](https://docs.microsoft.com/en-us/cpp/c-language/c-language-reference?view=vs-2019))
- L'API Windows n'est pas officiellement compatible avec C99, mais elle s'en approche, il n'y pas ou peu de documents expliquant les différences.
- Microsoft n'a aucune priorité pour développer son support C, il se focalise davantage sur C++ et C#, c'est pourquoi certains éléments du langage ne sont pas ou peu documentés.
- Les [types standards Windows](https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types) différent de ceux proposés par C99. Par exemple `LONG32` remplace `int32_t`.
