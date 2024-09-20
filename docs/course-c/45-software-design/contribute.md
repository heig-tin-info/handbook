# Projet open-source

Le langage C est encore beaucoup utilisé dans de gros projets qui demande une grande performance. On peut notament citer les projets suivants :

| Projet    | Watch | Fork  | Stars | Commits |
| --------- | ----- | ----- | ----- | ------- |
| Linux     | 7940  | 53k   | 177k  | 1.3M    |
| Git       | 2402  | 25.4k | 51.6k | 74k     |
| Vim       | 676   | 5.4k  | 35.9k | 20k     |
| SQLite    | 119   | 944k  | 6.2k  | 30k     |
| Gimp      | -     | 434   | 310k  | 53k     |
| FFmpeg    | 1438  | 12k   | 44.5k | 117k    |
| Wireshark | 300   | 1.8k  | 7k    | 93k     |
| Nginx     | 994   | 6.7k  | 21k   | 8.2k    |
| Apache    | 238   | 1.1k  | 3.5k  | 34k     |

[Le noyau Linux](https://github.com/torvalds/linux)

: Étant donné qu'il est le noyau de la plupart des distributions Linux et que Linux est présent sur des millions de serveurs, smartphones (via Android), et appareils IoT, on peut parler de milliards d'utilisateurs indirects.

[Git](https://github.com/git/git)

: Comme le système de contrôle de version le plus populaire, utilisé par GitHub, GitLab, Bitbucket, et d'autres plateformes, il est utilisé par des dizaines de millions de développeurs dans le monde.

[Vim](https://github.com/vim/vim)

: En tant qu'éditeur de texte, il est très populaire parmi les développeurs et les administrateurs système. Il est difficile de quantifier précisément son nombre d'utilisateurs, mais il est inclus par défaut dans de nombreuses distributions Linux et est couramment utilisé par des millions de développeurs.

[SQLite](https://github.com/sqlite/sqlite)

: Utilisé dans des milliards de dispositifs, que ce soit dans les navigateurs web, les téléphones mobiles, ou les systèmes embarqués. C’est probablement le SGBD le plus déployé au monde.

[Gimp](https://gitlab.gnome.org/GNOME/gimp)

: C'est une alternative open-source populaire à des logiciels comme Adobe Photoshop. Son nombre d'utilisateurs est dans l'ordre des millions, surtout parmi les amateurs de design graphique open-source.

[FFmpeg](https://github.com/FFmpeg/FFmpeg)

: Très utilisé dans l'industrie pour le traitement de vidéos, souvent intégré dans d'autres logiciels, ce qui rend difficile le comptage. Toutefois, son usage est très répandu dans les systèmes multimédia, donc potentiellement des centaines de millions d'utilisateurs finaux.

[Wireshark](https://github.com/wireshark/wireshark)

: Cet outil de capture et d'analyse de paquets réseau est indispensable pour les ingénieurs réseau et les chercheurs en sécurité, comptant probablement des millions d'utilisateurs dans ces domaines spécialisés.

[Nginx](https://github.com/nginx/nginx)

: Utilisé comme serveur web ou reverse proxy, il alimente une grande partie des sites web dans le monde. Selon certaines estimations, il gère plus de 30 % des sites web actifs, ce qui se traduit par des centaines de millions d'utilisateurs finaux.

[Apache HTTP Server](https://github.com/apache/httpd)

: Autre serveur web très populaire, il est utilisé sur une part significative des sites web. Bien que Nginx l'ait surpassé en popularité dans certains cas, Apache reste extrêmement répandu.

## Cas de figure Git

Vous souhaitez contribuer au projet Git. La première étape est de trouver le code source. Ce n'est pas une grosse difficulté. Google donne rapidement l'information que Git est hébergé sur GitHub:

Il suffit alors de cloner le projet Git sur votre machine locale sans historique. Cela permet de gagner du temps et de l'espace disque.

```bash
git clone --depth=1 https://github.com/git/git.git
cd git
```

Un bref perçu du contenu du répertoire cloné montre des fichiers sources C, un Makefile et un fichier INSTALL. C'est tout ce qu'il nous faut.

```bash
$ ls
CODE_OF_CONDUCT.md  editor.h            merge-ort.c        reset.h
COPYING             entry.c             merge-ort.h        resolve-undo.c
Documentation       entry.h             merge-recursive.c  resolve-undo.h
GIT-VERSION-GEN     environment.c       merge-recursive.h  revision.c
INSTALL             environment.h       merge.c            revision.h
LGPL-2.1            ewah                merge.h            run-command.c
Makefile            exec-cmd.c          mergesort.h        run-command.h
README.md           exec-cmd.h          mergetools         sane-ctype.h
RelNotes            fetch-negotiator.c  midx-write.c       scalar.c
SECURITY.md         fetch-negotiator.h  midx.c             send-pack.c
abspath.c           fetch-pack.c        midx.h             send-pack.h
...
```

On notera que le projet contient les fichiers bien connus:

- `.editorconfig` pour définir les règles de formatage du code
- `.gitattributes` pour définir les attributs des fichiers
- `.clang-format` pour définir les règles de formatage du code C
- `.gitignore` pour ignorer les fichiers inutiles
- `.gitmodules` pour définir les sous-modules Git
- `LICENSE` pour la licence du projet
- `COPYING` pour la licence du projet
- `Makefile` pour la compilation du projet
- `README.md` pour la documentation du projet

Avec `less INSTALL`, on peut prendre connaissance des instructions d'installation.

```bash
less INSTALL
                Git installation

Normally you can just do "make" followed by "make install", and that
will install the git programs in your own ~/bin/ directory. ...

Alternatively you can use autoconf generated ./configure script to
set up install paths (via config.mak.autogen), so you can write instead

        $ make configure ;# as yourself
        $ ./configure --prefix=/usr ;# as yourself
        $ make all doc ;# as yourself
        # make install install-doc install-html;# as root
...
```

Nous allons donc créer un préfixe local pour ne pas polluer notre système.

```bash
mkdir _install
make configure prefix=$(pwd)/_install
```

Le script `configure` est maintenant généré, il nous permet de configurer le projet, c'est à dire de choisir les options de compilation. Si l'on exécute configure avec l'option `--help`, on obtient la liste des options disponibles.

```bash
./configure --help
...
  --with-libpcre          synonym for --with-libpcre2
  --with-libpcre2         support Perl-compatible regexes via libpcre2
                          (default is NO)
...
```

On peut voir par exemple que Git est compilé par défaut sans `libpcre`. Cette bibliothèque permet le support avancé des expressions régulières Perl. Souvent les connaisseurs de Perl préfère cette senteur aux expressions régulières POSIX. Pour pouvoir l'utiliser il faut donc activer cette option, et nécessairement disposer de la bibliothèque `libpcre2` sur le système.

On commence donc par installer cette bibliothèque:
```bash
sudo apt install libpcre2-dev
```

Puis configurer le projet:

```bash
$ ./configure --with-libpcre2 --prefix=$(pwd)/_install
configure: Setting lib to 'lib' (the default)
configure: Will try -pthread then -lpthread to enable POSIX Threads.
configure: CHECKS for site configuration
checking for gcc... gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables...
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether the compiler supports GNU C... yes
checking whether gcc accepts -g... yes
checking for gcc option to enable C11 features... none needed
checking for stdio.h... yes
checking for stdlib.h... yes
...
checking for pcre2_config_8 in -lpcre2-8... yes
...
configure: creating ./config.status
config.status: creating config.mak.autogen
config.status: executing config.mak.autogen commands
```

A présent, on peut compiler le projet:

```bash
make -j16 V=1
```

L'option `-j16` permet de compiler en parallèle sur 16 threads. Cela accélère la compilation en utilisant mieux les ressources de la machine. `V=1` active le mode verbeux pour afficher les commandes exécutées ce qui peut être plus intéressant pour comprendre ce qui se passe.

Analysons un peu la sortie de la commande `make`:

```bash
$ make -j16 V=1
GIT_VERSION = 2.46.GIT
    * new build flags
    * new link flags
    * new prefix flags
/bin/sh ./generate-cmdlist.sh \
         \
        command-list.txt >command-list.h
gcc -o hex.o -c -MF ./.depend/hex.o.d -MQ hex.o -MMD -MP    -g -O2  -I. \
-DHAVE_SYSINFO -DGIT_HOST_CPU="\"x86_64\"" -DUSE_LIBPCRE2 -DHAVE_ALLOCA_H \
-DUSE_CURL_FOR_IMAP_SEND -DSUPPORTS_SIMPLE_IPC -DSHA1_DC \
-DSHA1DC_NO_STANDARD_INCLUDES -DSHA1DC_INIT_SAFE_HASH_DEFAULT=0 \
-DSHA1DC_CUSTOM_INCLUDE_SHA1_C="\"git-compat-util.h\"" -DSHA1DC_CUSTOM_INCLUDE_UBC_CHECK_C="\"git-compat-util.h\"" -DSHA256_BLK  \
-DHAVE_PATHS_H -DHAVE_STRINGS_H -DHAVE_DEV_TTY -DHAVE_CLOCK_GETTIME \
-DHAVE_CLOCK_MONOTONIC -DHAVE_SYNC_FILE_RANGE -DHAVE_GETDELIM \
'-DPROCFS_EXECUTABLE_PATH="/proc/self/exe"' -DFREAD_READS_DIRECTORIES \
-DSHELL_PATH='"/bin/sh"'  hex.c
...
```

On observe que Make compile tous les fichiers en appelant `gcc` avec des options spécifiques. On en connait déjà quelques unes.

```bash
gcc
   -o hex.o         # Nom du fichier objet de sortie
                    # (généralement le nom du fichier source avec .o)
   -c               # Compile sans lier, juste pour générer l'objet

   # Gestion des dépendances (pour la recompilation automatique)
   -MF ./.depend/hex.o.d -MQ hex.o -MMD -MP

   -g   # Génère des informations de débogage
   -O2  # Optimisation de niveau 2
   -I.  # Ajoute le répertoire courant pour les #include

   -DUSE_LIBPCRE2  # Définit le symbole USE_LIBPCRE2, puisque nous
                   # avons activé l'option --with-libpcre2

    hex.c          # Fichier source à compiler
```

Les options `-D` peuvent être assez nombreuses selon le projet, elles permettent de "communiquer" avec le code source via des directives de préprocesseur. Dans le code source pour détecter si le support `libpcre2` est activé on peut trouver des lignes comme:

```c
#ifdef USE_LIBPCRE2
#  include <pcre2.h>
#endif
```

À la fin de la compilation, le Makefile appellera le linker pour générer l'exécutable final. On reconnait facilement la ligne car c'est celle qui contient tous les fichiers objets générés.

```bash
gcc -g -O2 -I.
    -o git \
    git.o builtin/add.o builtin/am.o builtin/annotate.o builtin/apply.o \
    builtin/archive.o builtin/bisect.o builtin/blame.o builtin/branch.o \
    builtin/bugreport.o builtin/bundle.o builtin/cat-file.o builtin/check-attr.o
    builtin/check-ignore.o builtin/check-mailmap.o builtin/check-ref-format.o \
    builtin/checkout--worker.o builtin/checkout-index.o builtin/checkout.o \
    builtin/clean.o builtin/clone.o builtin/column.o builtin/commit-graph.o \
    ...
    libgit.a xdiff/lib.a reftable/libreftable.a libgit.a \
    -lpcre2-8 -lz  -lrt
```

On voit que le projet est lié avec `libpcre2-8`, `z` et `rt`. La bibliothèque `z` est la bibliothèque standard de compression `zlib`. La bibliothèque `rt` est la bibliothèque de temps réel. Les bibliothèques statiques `libgit.a`, `xdiff/lib.a`, `reftable/libreftable.a` sont des bibliothèques internes au projet qui ont été compilées en même temps que le projet.

Enfin, on peut installer le projet dans le répertoire `_install` et exécuter Git:

```bash
$ make install
$ ./_install/bin/git --version
git version 2.46.GIT
```

Comme pour la plupart des projets, ce dernier dispose d'une panoplie de tests unitaires et fonctionnels. Pour les exécuter, il suffit de lancer la commande `make test`:

```bash
make test
    SUBDIR git-gui
    SUBDIR gitk-git
    SUBDIR templates
make -C t/ all
make[1]: Entering directory '/home/ycr/git/t'
rm -f -r 'test-results'
GIT_TEST_EXT_CHAIN_LINT=0 && export GIT_TEST_EXT_CHAIN_LINT && make aggregate-results-and-cleanup
make[2]: Entering directory '/home/ycr/git/t'
*** t0000-basic.sh ***
ok 1 - verify that the running shell supports "local"
ok 2 - .git/objects should be empty after git init in an empty repo
ok 3 - .git/objects should have 3 subdirectories
...
ok 2598 - checkout attr= ident aeol=crlf core.autocrlf=true core.eol= file=LF_mix_CR
ok 2599 - checkout attr= ident aeol=crlf core.autocrlf=true core.eol= file=LF_nul
ok 2600 - ls-files --eol -d -z
# passed all 2600 test(s)
```

Ce projet est assez simple à compiler et à tester. Il est bien documenté et les tests sont clairs. Néanmoins il ne dépend pas de beaucoup de bibliothèques externes. Pour des projets plus complexes, la gestion des dépendances peut être un vrai casse-tête. Prenons un autre exemple, celui de Gimp.

## Cas de figure Gimp

Gimp est un logiciel de retouche d'image très populaire. C'est la version libre de Adobe Photoshop. Il est écrit en C et utilise de nombreuses bibliothèques externes. Pour compiler Gimp, il faut donc installer toutes ces bibliothèques. La liste des dépendances est longue et varie selon les distributions.

![Gimp](/assets/images/gimp.png)

En cherchant sous Google "gimp source code", on tombe sur le site officiel:

https://www.gimp.org/source/

Il est indiqué que le code source est hébergé sur le référentiel de GNOME, un environnement de bureau libre pour les systèmes Unix. Ce site redirige sur https://developer.gimp.org/ où l'on trouve les instructions pour les développeurs. De liens en liens on arrive sur la page [Building GIMP](https://developer.gimp.org/core/setup/build/) qui donne les instructions pour compiler Gimp.

Il est indiqué que Gimp utilise l'environnement Meson pour la compilation. Meson est un système de build open-source qui permet de générer des fichiers de configuration pour les projets C/C++. Il est écrit en Python et est très rapide.

Les [instructions](https://developer.gimp.org/core/setup/build/2.99/INSTALL) indiquent certaines dépendences:

pkg-config

: Pkg-config est un outil qui permet de récupérer les options de compilation et de liens pour les bibliothèques installées sur le système. Il sera utilisé par Meson pour trouver les bibliothèques nécessaires à la compilation.

gettext

: Gettext est une bibliothèque qui permet de gérer les chaînes de caractères multilingues. Elle est utilisée par Gimp pour les traductions. C'est la bibliothèque de facto utilisée pour l'internationalisation des logiciels libres.

gegl et babl

: GEGL (Generic Graphics Library) est une bibliothèque de traitement d'image non-destructif. Elle est utilisée par Gimp pour les opérations de traitement d'image. BABL est une bibliothèque de conversion de couleurs. Elle est utilisée par GEGL pour les conversions de couleurs. Ces bibliothèques sont intrinsèquement liées à Gimp.

gtk3

: GTK3 est la bibliothèque graphique utilisée par Gimp pour l'interface utilisateur. Elle est basée sur le langage de programmation C et est très populaire pour les applications graphiques sous Linux. GTK3 dépend également de `glib` et `Pango`.

Comme il s'agit d'un gros projet, nous allons devoir installer un certain nombre de dépendances qui ne seront pas nécessairement utiles ensuite sur notre ordinateur. La bonne approche est de s'isoler dans un environnement virtuel. Docker est une bonne alternative. Comme Gimp est développé sous Debian, nous allons utiliser une image Docker Debian pour compiler le projet.

```bash
$ docker run -it debian:latest
Unable to find image 'debian:latest' locally
latest: Pulling from library/debian
903681d87777: Pull complete
Digest: sha256:aadf411dc9ed5199bc7dab48b3e6ce18f8bbee4f170127f5ff1b75cd8035eb36
Status: Downloaded newer image for debian:latest
root@8c6a00ea1cf7:/#
```

La première étape *Preparing for Building* propose d'installer le projet dans un répertoire local. Nous allons commencer par créer un dossier `gimp` et fixer quelques variables d'environnement:

```bash
apt update
apt install build-essential cmake make git meson ninja-build bison flex pkg-config gettext
```

```bash
mkdir gimp && cd gimp
export GIMP_DIR=$(pwd)
export GIMP_PREFIX=$GIMP_DIR/_install

# Assuming that you have toolchain installed
# If this don't work, so manually set the dirs
LIB_DIR=$(cc -print-multi-os-directory | sed 's/\.\.\///g')
cc -print-multiarch | grep . && LIB_SUBDIR=$(echo $(cc -print-multiarch)'/')

# Used to detect the build dependencies
export PKG_CONFIG_PATH="${GIMP_PREFIX}/${LIB_DIR}/${LIB_SUBDIR}
pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"

# Used to find the libraries at runtime
export LD_LIBRARY_PATH="${GIMP_PREFIX}/${LIB_DIR}/${LIB_SUBDIR}$
{LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

# Used to find the glib-introspection dependencies
export XDG_DATA_DIRS="${GIMP_PREFIX}/share:/usr/share
${XDG_DATA_DIRS:+:$XDG_DATA_DIRS}"

# Used to find introspection files
export GI_TYPELIB_PATH="${GIMP_PREFIX}/${LIB_DIR}/${LIB_SUBDIR}
girepository-1.0${GI_TYPELIB_PATH:+:$GI_TYPELIB_PATH}"

# Used by Autotools to find its tools
export ACLOCAL_FLAGS="-I $GIMP_PREFIX/share/aclocal $ACLOCAL_FLAGS"

export XDG_DATA_DIRS="${GIMP_PREFIX}/share:/usr/local/share:/usr/share"
export PATH="${GIMP_PREFIX}/bin:$PATH"
```

En suivant la documentation, on installe quelques dépendences, sachant qu'il y en aura probablement d'autres à installer au fur et à mesure:

```bash
apt install graphviz libswscale-dev libsuitesparse-dev libpng-dev
libtiff-dev librsvg2-dev \
liblcms2-dev libmypaint-dev mypaint-brushes  libmng-dev libwmf-dev \
libaa1-dev libgs-dev libheif-dev gobject-introspection libgirepository1.0-dev
```

500 MB plus tard, nous avons installé les dépendances de base. Nous allons maintenant cloner le projet Gimp:

### Installation de BABL

```bash
git clone --depth=1 https://gitlab.gnome.org/GNOME/babl.git
cd babl
meson setup --prefix $GIMP_PREFIX -Denable-gir=true _build
ninja -C _build install
```

### Installation de GEGL

```bash
git clone --depth=1 https://gitlab.gnome.org/GNOME/gegl.git
cd gegl
meson setup --prefix $GIMP_PREFIX -Dintrospection=true -Dcairo=enabled -Dumfpack=enabled -Dworkshop=true _build
ninja -C _build install
```

### Installation de GIMP

```bash
git clone --depth=1 --shallow-submodules  https://gitlab.gnome.org/GNOME/gimp.git
cd gimp
git submodule update --init
meson setup --prefix $GIMP_PREFIX _build
Run-time dependency atk found: NO (tried pkgconfig and cmake)

meson.build:364:0: ERROR: Dependency "atk" not found, tried pkgconfig and cmake
```

Nous avons un problème. La dépendance `atk` n'est pas trouvée. Un rapide coup d'oeil à la documentation nous indique que `atk` est une bibliothèque graphique et la version 2.4.0 est nécessaire. Or la version que l'on trouve sous Debian est `libatk1.0-dev` qui est la 2.30.0. Comme seule la version mineure est différente il ne devrait pas y avoir de problème de compatibilité. Nous allons donc installer la version 2.30.0 et voir si cela fonctionne.

```bash
apt install libatk1.0-dev
```

Notons que la bibliothèque se nomme `libatk1.0-dev` le `1.0` est la version de l'API mais cela ne signifie pas que la version de la bibliothèque est 1.0. En fait tant que l'API est compatible, la version installée peut être plus récente. On peut noter toutefois que normalement si une version majeur change, cela signifie une rupture de compatibilité dans l'API. Ici on voit que les développeurs ont décidé de ne pas rompre la compatibilité.

Rebolote, on relance la configuration de Gimp:

```bash
meson setup --prefix $GIMP_PREFIX 'python-fu-eval' is n_build
Run-time dependency exiv2 found: NO (tried pkgconfig and cmake)
```

On va donc installer `libexiv2-dev` et `libgexiv2-dev`. Au prochain problème, on installera la dépendance manquante et ainsi de suite jusqu'à ce que la configuration se passe sans erreur :

```bash
apt install libgirepository1.0-dev libgtk-3-dev glib-networking appstream \
libappstream-glib-dev libxmu-dev libbz2-dev libpoppler-glib-dev python3-gi \
xsltproc xvfb  libc6-dev gi-docgen gjs luajit libxml2-utils \
desktop-file-utils iso-codes libopenjp2-7-dev libjxl-dev libasound2-dev \
libgudev-1.0-dev libcfitsio-dev xdg-utils libunwind-dev lua5.1 libxpm-dev \
libopenexr-dev libvala-0.56-dev valac qoi python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

Une fois configuré il suffit de compiler le projet:

```bash
ninja -C _build install
```

Et voilà, Gimp est installé dans le répertoire `_install`.

### Reproduction

Si vous essayez de reproduire cet exemple vous aurez probablement d'autres erreurs car vous n'avez pas les mêmes version. Dans cet exemple, nous avons utilisé Debian Bookworm (12)

gimp

: e89bb33408c5ed006b7b92fbb7c793dde169b02a

gegl

: 72d86816289c11fdd871b701827f8bf0016a7f4f

babl

: c5f97c86224a473cc3fea231f17adef84580f2cc

### Dépendances

On voit après cet exemple que certains projets peuvent être complexes à compiler. Les problèmes récurrents sont :

- Vous ne lisez pas la documentation
- Vous êtes trop pressé et vous ne lisez pas les messages d'erreur
- Vous pensez avoir lu la documentation mais vous n'avez pas vraiment lu la documentation

En dehors de ces quelques problèmes, il y a certaines dépendances qui dépendent de la distribution Linux/Unix que vous avez, les noms de bibliothèques ne sont pas nécessairement les mêmes, ou les version génèrent des conflits.

Dans cet exemple, nous avons été contraint de compiler GEGL et BABL depuis les sources avec des options spécifiques pour être compatible avec la dernière version de Gimp sous Git

Ce que nous avons vu ici c'est que les dépendances dans un projet logiciel peuvent être nombreuses.

Vous pouvez vous demander pourquoi utiliser autant de bibliothèques externes ? La réponse est simple : pour ne pas réinventer la roue. Les bibliothèques externes sont souvent des projets open-source très bien maintenus et testés. Elles permettent de gagner du temps et de l'argent en réutilisant du code existant. Par exemple dans le cas de Gimp, la bibliothèque `aa` est utilisée pour convertir des images en ASCII art. La bibliothèque `iso-codes` permet de connaître les noms des pays dans différentes langues. La bibliothèque `heif` permet le support des images en format natif des iPhones récents. On peut citer `lcms2` pour la gestion des couleurs via le standard ICC, ou la bibliothèque `mypaint` pour la gestion des pinceaux et des calques de peinture.