# Compilation séparée

## Unité de traduction

En programmation, on appelle *translation unit* (unité de traduction) toute portion de code qui peut être **compilée** en un **objet** sans dépendre d'autres fichiers. Dans la plupart des cas, une unité de traduction correspond à un fichier C unique.

## Diviser pour mieux régner

Tout comme un magazine illustré distingue ses rubriques (sport, actualités, météo, annonces) pour améliorer la lisibilité, un code source gagne à être structuré en composants. Ces éléments fonctionnels sont répartis dans plusieurs fichiers, souvent entretenus par des personnes différentes.

Gardons en tête quelques règles de bon sens :

- une fonction ne devrait pas dépasser la hauteur d'un écran (~50 lignes) ;
- un fichier ne devrait pas excéder 1 000 lignes ;
- une ligne ne devrait pas s'étirer au-delà de 80 caractères.

Lorsque le volume de code augmente, la lecture, la compréhension et le débogage deviennent rapidement ardus, même pour une équipe expérimentée. Diviser son travail en plusieurs fichiers permet de retrouver de la clarté. Prenons un exemple simple de programme qui manipule des nombres complexes. Notre projet comporte trois fichiers :

```console
$ tree
.
├── complex.c
├── complex.h
└── main.c
```

Le programme principal et la fonction `main` sont contenus dans `main.c`, tandis que le module `complex` repose sur deux fichiers : `complex.h`, l'en-tête, et `complex.c`, l'implémentation proprement dite.

Le fichier `main.c` doit inclure `complex.h` afin d'utiliser correctement les fonctions du module de gestion des nombres complexes. Exemple :

```c
// fichier main.c
#include "complex.h"

int main() {
    Complex c1 = { .real = 1., .imag = -3. };
    complex_fprint(stdout, c1);
}
```

```c
// fichier complex.h
#ifndef COMPLEX_H
#define COMPLEX_H

#include <stdio.h>

typedef struct Complex {
    double real;
    double imag;
} Complex, *pComplex;

void complex_fprint(FILE *fp, const Complex c);

#endif // COMPLEX_H
```

```c
// fichier complex.c
#include "complex.h"

void complex_fprint(FILE* fp, const Complex c) {
    fprintf(fp, "%+.3lf + %+.3lf\n", c.real, c.imag);
}
```

L'un des bénéfices majeurs de cette organisation est la réutilisation. Un module logiciel bien conçu pourra servir dans plusieurs applications sans que l'on ait à réinventer la roue.

Dans un environnement POSIX, ce projet se compile ainsi :

```console
gcc -c complex.c -o complex.o
gcc -c main.c -o main.o
gcc complex.o main.o -oprogram -lm
```

Nous détaillerons plus loin les éléments théoriques qui se cachent derrière ces commandes.

## Module logiciel

Les applications modernes s'appuient fréquemment sur des modules logiciels externes, eux-mêmes partagés entre plusieurs projets. Cette démarche est payante à plusieurs titres :

- les modules externes sont maintenus par d'autres développeuses et développeurs, ce qui réduit la quantité de code à écrire localement ;
- ces modules bénéficient souvent d'une documentation et de tests robustes, d'où une prise en main rapide ;
- la lisibilité du programme s'améliore grâce à un découpage clair en ensembles fonctionnels ;
- des modules autonomes et bien définis peuvent être réutilisés sur plusieurs projets sans effort supplémentaire.

Lorsque vous utilisez la fonction `printf`, vous dépendez d'un module externe nommé `stdio`. En réalité, l'ensemble des modules `stdio`, `stdlib`, `stdint`, `ctype`, etc. est regroupé au sein d'une unique bibliothèque logicielle nommée `libc`, disponible sur tous les systèmes compatibles POSIX. Sous GNU/Linux, on utilise généralement sa version libre `glibc`, c'est-à-dire la [GNU C Library](https://fr.wikipedia.org/wiki/GNU_C_Library).

Un module logiciel peut se composer de fichiers sources, c'est-à-dire de fichiers `.c` et `.h`, accompagnés d'une documentation et d'un script de compilation (`Makefile`). À l'inverse, il peut également être fourni directement sous forme binaire, via des fichiers `.h`, `.a` et `.so`. Sous Windows, on rencontre fréquemment l'extension `.dll`. Ces fichiers compilés ne dévoilent pas le code source, mais ils mettent à disposition un ensemble de fonctions documentées que l'on peut relier depuis un programme C.

## Compilation avec assemblage différé

Lorsque nous avons compilé notre premier exemple [Hello World][hello-world], nous avons simplement invoqué `gcc` sur le fichier source `hello.c`, ce qui a produit un exécutable `a.out`. En réalité, GCC enchaîne plusieurs étapes distinctes :

1. **Prétraitement** : les commentaires sont retirés et les directives du préprocesseur sont remplacées par leur équivalent en C.
2. **Compilation** : le code C d'une *translation unit* est transformé en langage machine dans un fichier objet `.o`.
3. **Édition des liens** (*linking*) : les différents fichiers objets sont rassemblés pour former un exécutable unique.

Lorsqu'un seul fichier est fourni à GCC, ces trois opérations s'exécutent en une seule commande. Dès qu'un projet comporte plusieurs unités de traduction, il faut en revanche compiler chaque fichier séparément, puis demander explicitement l'édition des liens.

La figure suivante résume ces étapes. Les pointillés indiquent à quel niveau le processus peut s'interrompre. On peut ainsi générer des fichiers intermédiaires assembleur (`.s`) ou objets (`.o`) en ajoutant les options appropriées.

![Étapes intermédiaires de compilation avec GCC](/assets/images/gcc.drawio)


Ces étapes existent quel que soit le compilateur ou le système d'exploitation. On les retrouve par exemple dans Microsoft Visual Studio, même si les commandes et les extensions de fichiers diffèrent lorsqu'elles ne suivent pas les conventions POSIX (et GNU).

En pratique, on ne retient souvent que deux commandes :

1. `gcc -c <fichier.c>` : génère un fichier objet `.o` portant le même nom que le fichier source ;
2. `gcc <fichier1.o> <fichier2.o> ...` : assemble les objets listés en un exécutable `a.out` (ou en un fichier nommé via l'option `-o`).

## Fichiers d'en-tête (*header*)

Les fichiers d'en-tête (`.h`) sont des fichiers écrits en langage C, mais qui ne contiennent pas d'implémentation de fonctions. Un tel fichier ne contient donc pas de `while`, de `for` ou même de `if`. Par convention, ces fichiers ne contiennent que :

- Des prototypes de fonctions (ou de variables).
- Des déclarations de types (`typedef`, `struct`).
- Des définitions préprocesseur (`#include`, `#define`).

Comme nous l'avons vu dans le chapitre sur le préprocesseur, la directive `#include` ne fait qu'insérer le contenu du fichier cible à l'emplacement de la directive. Il est donc possible (mais fortement déconseillé) d'obtenir la situation suivante :

```c title="main.c"
int main() {
   #include "foobar.def"
}
```

Et le fichier `foobar.def` pourrait contenir :

```c title="foobar.def"
#ifdef FOO
printf("hello foo!\n");
#else
printf("hello bar!\n");
#endif
```

Vous noterez que l'extension de `foobar` n'est pas `.h` puisque le contenu n'est pas un fichier d'en-tête. `.def` ou n'importe quelle autre extension pourrait donc faire l'affaire ici.

Dans cet exemple, le préprocesseur ne fait qu'inclure le contenu du fichier `foobar.def` à l'emplacement de la définition `#include "foobar.def"`. Voyons-le en détail :

```console
$ cat << EOF > main.c
int main() {
    #include "foobar.def"
    #include "foobar.def"
}
EOF

$ cat << EOF > foobar.def
#ifdef FOO
printf("hello foo!\n");
#else
printf("hello bar!\n");
#endif
EOF

$ gcc -E main.c | sed '/^#/ d'
int main() {
printf("hello bar\n");
printf("hello bar\n");
}
```

En observant le résultat du préprocesseur, on s'aperçoit que toutes les directives ont disparu et que `#include` a été remplacé par le contenu de `foobar.def`. Le fichier est inclus deux fois ; nous verrons plus loin comment éviter ce piège.

Nous avons vu au chapitre sur les [prototypes de fonctions][function-prototype] qu'il est possible de ne déclarer que la première ligne d'une fonction. Ce prototype permet au compilateur de connaître le nombre d'arguments attendus sans disposer immédiatement de l'implémentation. On trouve donc dans tous les fichiers d'en-tête des déclarations en amont (*forward declarations*). Dans `stdio.h`, on lira par exemple : `int printf( const char *restrict format, ... );`.

```bash
$ cat << EOF > main.c
→ #include <stdio.h>
→ int main() { }
→ EOF
$ gcc -E main.c | grep -P '\bprintf\b'
extern int printf (const char *__restrict __format, ...);
```

Notons qu'ici le prototype est précédé par le mot-clé `extern`. Ce mot-clé **optionnel** précise que la fonction déclarée n'est pas implémentée dans le fichier courant, mais ailleurs. C'est bien le cas : `printf` est déjà compilée dans la bibliothèque `libc`, liée par défaut lorsqu'un programme C est compilé dans un environnement POSIX.

Un fichier d'en-tête contiendra donc tout le nécessaire utile à pouvoir utiliser une bibliothèque externe.

### Protection de réentrance

La protection de réentrance, aussi nommée *header guard*, répond au problème des inclusions multiples. Si l'on définit un nouveau type dans un fichier d'en-tête et que ce fichier est inclus deux fois par des chemins différents, une erreur de compilation apparaîtra :

```bash
$ cat << EOF > main.c
→ #include "foo.h"
→ #include "bar.h"
→ int main() {
→    Bar bar = {0};
→    foo(bar);
→ }
→ EOF

$ cat << EOF > foo.h
→ #include "bar.h"
→
→ extern void foo(Bar);
→ EOF

$ cat << EOF > bar.h
→ typedef struct Bar {
→    int b, a, r;
→ } Bar;
→ EOF

$ gcc main.c
In file included from main.c:2:0 :
bar.h:1:16: error: redefinition of ‘struct Bar’
typedef struct Bar {
                ^~~
In file included from foo.h:1:0,
                from main.c:1 :
bar.h:1:16: note: originally defined here
typedef struct Bar {
                ^~~
In file included from main.c:2:0 :
bar.h:3:3: error: conflicting types for ‘Bar’
} Bar;
^~~
...
```

Dans cet exemple, la personne qui écrit `main.c` ignore que `bar.h` est déjà inclus via `foo.h`. Après prétraitement, le résultat est le suivant :

```bash
$ gcc -E main.c | sed '/^#/ d'
typedef struct Bar {
int b, a, r;
} Bar;

extern void foo(Bar);
typedef struct Bar {
int b, a, r;
} Bar;
int main() {
Bar bar = {0};
foo(bar);
}
```

On y retrouve la définition de `Bar` deux fois et donc, le compilateur génère une erreur.

Pour résoudre cette difficulté, on ajoute des gardes d'inclusion multiple, par exemple :

```c
#ifndef BAR_H
#define BAR_H

typedef struct Bar {
int b, a, r;
} Bar;

#endif // BAR_H
```

Si aucune définition `#define BAR_H` n'existe, c'est que le fichier `bar.h` n'a encore jamais été inclus et le contenu de la directive `#ifndef BAR_H` — qui commence par définir `BAR_H` — est exécuté. Lors d'une inclusion ultérieure, `BAR_H` sera déjà défini et le contenu de la directive sera ignoré.

Il existe aussi une solution **non standard**, mais supportée par la plupart des compilateurs :

```c
#pragma once

typedef struct Bar {
int b, a, r;
} Bar;
```

Cette directive est équivalente à la méthode traditionnelle et présente plusieurs avantages. Elle est atomique — pas besoin de `#endif` — et respecte naturellement la règle *single source of truth*, car le nom du fichier n'est pas dupliqué dans une constante.

## En profondeur

Pour mieux comprendre la compilation séparée, tentons d'observer le code assembleur généré. Considérons le fichier `foo.c` :

```c
int bar(int);

int foo(int a) {
    return bar(a) + 42;
}
```

Puisqu'il ne contient pas de fonction `main`, il est impossible d'en faire un exécutable : il manque un point d'entrée.

```sh
gcc foo.c
/usr/bin/ld: /usr/lib/x86_64-linux-gnu/Scrt1.o: in function '_start':
(.text+0x24): undefined reference to 'main'
collect2: error: ld returned 1 exit status
```

L'éditeur de liens signale alors l'erreur suivante : *référence à 'main' inexistante*.

En revanche, on peut compiler un objet, c'est-à-dire générer les instructions assembleur. La fonction `bar` étant manquante, le compilateur suppose qu'elle sera fournie ailleurs et se contente de dire : *j'appellerai cette fonction, où qu'elle se trouve*.

```sh
$ objdump -d foo.o

foo.o:     file format elf64-x86-64

Disassembly of section .text:

0000000000000000 <foo>:
 0:   f3 0f 1e fa       endbr64
 4:   55                push   %rbp
 5:   48 89 e5          mov    %rsp,%rbp
 8:   48 83 ec 10       sub    $0x10,%rsp
 c:   89 7d fc          mov    %edi,-0x4(%rbp)
 f:   8b 45 fc          mov    -0x4(%rbp),%eax
12:   89 c7             mov    %eax,%edi
14:   e8 00 00 00 00    callq  19 <foo+0x19>
19:   83 c0 2a          add    $0x2a,%eax
1c:   c9                leaveq
1d:   c3                retq
```

On constate à la ligne `19` que l'addition a bien lieu (`eax + 42`) et que l'appel de `bar` se produit à la ligne `14`.

Maintenant, considérons le programme principal :

```c
#include <stdio.h>

int foo(int);

int bar(int a) {
    return a * 2;
}

int main() {
    printf("%d", foo(42));
}
```

En générant l'objet `gcc -c main.c`, on peut également afficher l'assembleur généré avec `objdump` :

```sh
$ objdump -d main.o

main.o:     file format elf64-x86-64

Disassembly of section .text:

0000000000000000 <bar>:
 0:   f3 0f 1e fa             endbr64
 4:   55                      push   %rbp
 5:   48 89 e5                mov    %rsp,%rbp
 8:   89 7d fc                mov    %edi,-0x4(%rbp)
 b:   8b 45 fc                mov    -0x4(%rbp),%eax
 e:   01 c0                   add    %eax,%eax
10:   5d                      pop    %rbp
11:   c3                      retq

0000000000000012 <main>:
12:   f3 0f 1e fa             endbr64
16:   55                      push   %rbp
17:   48 89 e5                mov    %rsp,%rbp
1a:   bf 2a 00 00 00          mov    $0x2a,%edi
1f:   e8 00 00 00 00          callq  24 <main+0x12>
24:   89 c6                   mov    %eax,%esi
26:   48 8d 3d 00 00 00 00    lea    0x0(%rip),%rdi
2d:   b8 00 00 00 00          mov    $0x0,%eax
32:   e8 00 00 00 00          callq  37 <main+0x25>
37:   b8 00 00 00 00          mov    $0x0,%eax
3c:   5d                      pop    %rbp
3d:   c3                      retq
```

On observe l'appel de `foo` à la ligne `1f` et celui de `printf` à la ligne `32`.

L'assemblage de ces deux fichiers en un exécutable résout les liens en mettant à jour les adresses d'appel des fonctions désormais connues (certaines lignes sont retirées ci-dessous pour alléger la lecture) :

```sh
$ gcc foo.o main.o
$ objdump -d a.out

a.out:     file format elf64-x86-64

Disassembly of section .text:

0000000000001149 <foo>:
    1149:       f3 0f 1e fa             endbr64
    114d:       55                      push   %rbp
    114e:       48 89 e5                mov    %rsp,%rbp
    1151:       48 83 ec 10             sub    $0x10,%rsp
    1155:       89 7d fc                mov    %edi,-0x4(%rbp)
    1158:       8b 45 fc                mov    -0x4(%rbp),%eax
    115b:       89 c7                   mov    %eax,%edi
    115d:       e8 05 00 00 00          callq  1167 <bar>
    1162:       83 c0 2a                add    $0x2a,%eax
    1165:       c9                      leaveq
    1166:       c3                      retq

0000000000001167 <bar>:
    1167:       f3 0f 1e fa             endbr64
    116b:       55                      push   %rbp
    116c:       48 89 e5                mov    %rsp,%rbp
    116f:       89 7d fc                mov    %edi,-0x4(%rbp)
    1172:       8b 45 fc                mov    -0x4(%rbp),%eax
    1175:       01 c0                   add    %eax,%eax
    1177:       5d                      pop    %rbp
    1178:       c3                      retq

0000000000001179 <main>:
    1179:       f3 0f 1e fa             endbr64
    117d:       55                      push   %rbp
    117e:       48 89 e5                mov    %rsp,%rbp
    1181:       bf 2a 00 00 00          mov    $0x2a,%edi
    1186:       e8 be ff ff ff          callq  1149 <foo>
    118b:       89 c6                   mov    %eax,%esi
    118d:       48 8d 3d 70 0e 00 00    lea    0xe70(%rip),%rdi
    1194:       b8 00 00 00 00          mov    $0x0,%eax
    1199:       e8 b2 fe ff ff          callq  1050 <printf@plt>
    119e:       b8 00 00 00 00          mov    $0x0,%eax
    11a3:       5d                      pop    %rbp
    11a4:       c3                      retq
    11a5:       66 2e 0f 1f 84 00 00    nopw   %cs:0x0(%rax,%rax,1)
    11ac:       00 00 00
    11af:       90                      nop
```

On constate que les appels de fonctions ont été correctement résolus :

- `115d` appel de `bar` ;
- `1186` appel de `foo` ;
- `1199` appel de `printf`.
