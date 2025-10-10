# Bibliothèques

![Bibliothèque du Trinity College de Dublin](/assets/images/library.jpg)

Une bibliothèque logicielle est un ensemble de fichiers proposant des fonctionnalités prêtes à l'emploi. L'appel à `printf` en est un exemple emblématique : la fonction est déclarée dans l'en-tête `<stdio.h>` et son implémentation est fournie par la bibliothèque standard `libc`.

Dans la pratique, l'anglicisme *library* est très courant, car il est bref et universel dans le milieu informatique. Il ne faut toutefois pas le confondre avec l'anglais *bookstore*, qui correspond à notre « librairie ». Les bibliothèques logicielles se composent le plus souvent d'un ou plusieurs fichiers binaires compilés pour une architecture donnée et d'en-têtes (*headers*) décrivant les fonctions disponibles.

Les exemples qui suivent sont tirés d'un environnement POSIX. Sous Windows, la procédure diffère légèrement, mais les concepts restent les mêmes : une bibliothèque expose des fonctions ou des structures de données, et un programme les relie lors de l'édition des liens.

## Exemple : libgmp

[libgmp](https://packages.ubuntu.com/jammy/libgmp-dev) fournit des fonctions d'arithmétique multiprécision très utilisées. En consultant le paquet Debian, on constate qu'il existe des variantes pour plusieurs architectures (`amd64`, `arm64`, `s390x`, `i386`, etc.). Un ordinateur de bureau x86_64 nécessitera la variante `amd64`, tandis qu'un Raspberry Pi demandera `arm64`. La liste des fichiers installés pour l'architecture choisie comprend notamment :

```
# Fichier d'en-tête C
/usr/include/x86_64-linux-gnu/gmp.h

# Bibliothèque compilée pour l'architecture visée (ici amd64)
/usr/lib/x86_64-linux-gnu/libgmp.a
/usr/lib/x86_64-linux-gnu/libgmp.so

# Documentation de libgmp
/usr/share/doc/libgmp-dev/AUTHORS
/usr/share/doc/libgmp-dev/README
/usr/share/doc/libgmp-dev/changelog.gz
/usr/share/doc/libgmp-dev/copyright
```

On y retrouve donc :

`gmp.h`
: Fichier d'en-tête à inclure pour utiliser les fonctionnalités.

`libgmp.a`
: Bibliothèque **statique** contenant l'implémentation en langage machine des fonctions. Elle doit être mentionnée explicitement lors de l'édition des liens.

`libgmp.so`
: Bibliothèque **dynamique** qui contient elle aussi le code machine, mais qui sera chargée au moment de l'exécution.

Supposons que l'on souhaite calculer des orbites pour un satellite d'observation de Jupiter. Pour apprivoiser cette *library*, on écrit :

```c
--8<-- "docs/assets/src/gmp.c"
```

Première tentative de compilation :

```console
$ gcc gmp.c
gmp.c:1:10: fatal error: gmp.h: No such file or directory
#include <gmp.h>
         ^~~~~~~
compilation terminated.
```

La bibliothèque n'est pas installée sur la machine. On l'installe alors :

=== "Ubuntu"

    ```console
    $ sudo apt-get install libgmp-dev
    ```

=== "macOS"

    ```console
    $ brew install gmp
    ```

Nouvelle compilation :

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

Cette fois, le compilateur a bien produit un fichier objet, mais l'éditeur de liens ne sait pas où trouver les symboles, comme `__gmpz_add_ui`. Il suffit de préciser la bibliothèque à charger :

```console
$ gcc gmp.c -lgmp

$ ./a.out
19810983098510928501928599999999999990
19810983098510928501928600000000000002
392475051329485669436248957939688603493163430354043714007714400000000000004
```

La commande ci-dessus utilise `libgmp.so`, la version dynamique. L'exécutable obtenu reste donc dépendant de la présence de libgmp sur la machine cible. Si l'on transmet le binaire à une personne qui n'a pas installé la bibliothèque, l'exécution échouera.

On peut au contraire créer un exécutable autonome en liant explicitement la bibliothèque statique :

```console
$ gcc gmp.c /usr/lib/x86_64-linux-gnu/libgmp.a
```

Dans ce cas, tout le code nécessaire est intégré dans l'exécutable et il suffit de partager ce fichier avec quelqu'un utilisant la même architecture. Le revers de la médaille est la taille plus importante du binaire :

```console
# ~167 KiB
$ gcc gmp.c -l:libgmp.a
$ size a.out
   text    data     bss     dec     hex filename
 155494     808      56  156358   262c6 ./a.out

# ~8.5 KiB
$ gcc gmp.c -lgmp
$ size a.out
  2752     680      16    3448     d78 ./a.out
```

## Exemple : ncurses

La bibliothèque [ncurses](https://fr.wikipedia.org/wiki/Ncurses), évolution de [curses](https://fr.wikipedia.org/wiki/Curses) conçue par [Ken Arnold](https://en.wikipedia.org/wiki/Ken_Arnold), permet de créer des interfaces textuelles riches. Elle offre le positionnement arbitraire du curseur, le dessin de fenêtres, de menus, d'ombres ou encore de jeux de couleurs.

Figure : Exemple d'interface graphique écrite avec `ncurses`. Ici, la configuration du noyau Linux.

![Exemple avec ncurses](/assets/images/linux-menuconfig.png)

Un programme minimal peut ressembler à ceci :

```c
#include <ncurses.h>

int main(void)
{
    initscr();              // Démarrer ncurses
    printw("hello, world"); // Afficher un message
    refresh();              // Mettre à jour l'écran réel
    getch();                // Attendre une frappe
    endwin();               // Quitter ncurses proprement

    return 0;
}
```

La compilation n'aboutit que si la bibliothèque est installée **et** si le lien est mentionné :

```console
$ gcc ncurses-hello.c -o hello -lncurses
```

## Bibliothèques statiques

Une *static library* est une archive d'objets compilés pour une architecture donnée. On rencontre les extensions suivantes :

- `.a` sur les systèmes POSIX (GNU/Linux, macOS, Unix, Android) ;
- `.lib` sous Windows.

Pour illustrer la création d'une bibliothèque statique, reprenons le [chiffrement de César](https://fr.wikipedia.org/wiki/Chiffrement_par_d%C3%A9calage). On écrit d'abord un fichier source `caesar.c` :

```c title="caesar.c"
--8<-- "docs/assets/src/caesar.c"
```

et le fichier d'en-tête correspondant :

```c title="caesar.h"
--8<-- "docs/assets/src/caesar.h"
```

La création de la bibliothèque se déroule en deux étapes : génération de l'objet, puis archivage :

```console
$ gcc -c -o caesar.o caesar.c
$ ar rcs caesar.a caesar.o
```

On peut ensuite écrire un programme utilisateur :

```c title="encrypt.c"
--8<-- "docs/assets/src/encrypt.c"
```

La compilation se fait en précisant où trouver les en-têtes (`-I.`) et la bibliothèque (`-L.`) :

```console
$ gcc encrypt.c -I. -L. -l:caesar.a
```

Sous Windows, les outils diffèrent et la procédure demande quelques étapes supplémentaires, que nous n'abordons pas ici.

## Bibliothèques dynamiques

Une *dynamic library* est, elle aussi, un binaire compilé pour une architecture donnée. Elle porte en général l'extension :

- `.so` sur les systèmes POSIX ;
- `.dll` sous Windows.

Son avantage principal est de partager le code entre plusieurs exécutables, réduisant l'espace disque et la mémoire consommée. En contrepartie, l'utilisateur doit disposer de la bibliothèque au moment de l'exécution. Sous un environnement POSIX, les bibliothèques dynamiques sont stockées dans des répertoires dédiés et référencées par l'éditeur de liens. Sous Windows, l'organisation est moins uniformisée et chaque application peut embarquer sa propre copie des `.dll`.

En reprenant l'exemple du chiffrement de César, on produit d'abord la bibliothèque dynamique :

```console
$ gcc -shared -o libcaesar.so caesar.o
```

Pour compiler le programme, il faut indiquer les chemins dans lesquels chercher les bibliothèques. Comme nous ne souhaitons pas installer `libcaesar.so` globalement, nous ajoutons le répertoire courant à la variable d'environnement `LIBRARY_PATH` au moment de la compilation :

```console
$ LIBRARY_PATH=$(pwd .) gcc encrypt.c -I. -lcaesar
```

À l'exécution, la même logique s'applique avec `LD_LIBRARY_PATH`, afin que le système sache où charger la bibliothèque :

```console
$ LD_LIBRARY_PATH=$(pwd .) ./a.out ferrugineux
sreehtvarhk
```

En omettant cette variable, on obtient l'erreur suivante :

```console
$ LIBRARY_PATH=$(pwd .) ./a.out Hey?
./a.out: error while loading shared libraries: libcaesar.so: cannot open shared object file: No such file or directory
```
