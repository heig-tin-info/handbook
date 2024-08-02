# Bibliothèques

![Bibliothèque du Trinity College de Dublin]({assets}/images/library.jpg)

Une bibliothèque informatique est une collection de fichiers comportant des fonctionnalités logicielles prêtes à l'emploi. La `printf` est une de ces fonctionnalités et offerte par le header `<stdio.h>` faisant partie de la bibliothèque `libc6`.

L'anglicisme *library*, plus court à prononcer et à écrire est souvent utilisé en lieu et place de bibliothèque tant il est omniprésent dans le monde logiciel. Le terme `<stdlib.h>` étant la concaténation de *standard library* par exemple. Notez que librairie n'est pas la traduction correcte de *library* qui est un [faux ami](https://fr.wikipedia.org/wiki/Faux-ami).

Une *library*, à l'instar d'une bibliothèque, contient du contenu (livre écrit dans une langue donnée) et un index (registre). En informatique il s'agit d'un fichier binaire compilé pour une architecture donnée ainsi qu'un ou plusieurs fichiers d'en-tête (*header*) contenant les définitions de cette bibliothèque.

Dans ce chapitre on donnera plusieurs exemples sur un environnement POSIX. Sous Windows, les procédures choses sont plus compliquées, mais les concepts restent les mêmes.

## Exemple: libgmp

Voyons ensemble le cas de [libgmp](https://packages.ubuntu.com/jammy/libgmp-dev). Il s'agit d'une bibliothèque de fonctionnalités très utilisée et permettant le calcul arithmétique multiprécision en C. En observant le détail du paquet logiciel Debian on peut lire que `libgmp` est disponible pour différentes architectures `amd64`, `arm64`, `s390x`, `i386`, ... Un développement sur un Raspberry-PI nécessitera `arm64` alors qu'un développement sur un PC utilisera `amd64`. En [cliquant](https://packages.ubuntu.com/jammy/amd64/libgmp-dev/filelist) sur l'architecture désirée on peut voir que ce paquet se compose des fichiers suivants (list réduite aux fichiers concernant C):

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

Aïe! La bibliothèque n'est pas installée...

Pour l'installer, cela dépend de votre système d'exploitation :

=== "Ubuntu"

    ```console
    $ sudo apt-get install libgmp-dev
    ```

=== "macOS"

    ```console
    $ brew install gmp
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

Figure: Exemple d'interface graphique écrite avec `ncurses`. Ici la configuration du noyau Linux.

![Exemple avec ncurses]({assets}/images/linux-menuconfig.png)

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
