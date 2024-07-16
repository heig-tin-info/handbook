# Compilation séparée

## Unité de traduction

En programmation, on appelle *translation unit* (unité de traduction), un code qui peut être **compilé** en un **objet** sans autre dépendance externe. Le plus souvent, une unité de traduction correspond à un fichier C.

## Diviser pour mieux régner

De même qu'un magazine illustré est divisé en sections pour accroître la lisibilité (sport, news, annonces, météo) de même un code source est organisé en éléments fonctionnels le plus souvent séparés en plusieurs fichiers et ces derniers parfois maintenus par différents développeurs.

Rappelons-le (et c'est très important) :

- une fonction ne devrait pas dépasser un écran de haut (~50 lignes) ;
- un fichier ne devrait pas dépasser 1000 lignes ;
- une ligne ne devrait pas dépasser 80 caractères.

Donc à un moment, il est essentiel de diviser son travail en créant plusieurs fichiers.

Ainsi, lorsque le programme commence à être volumineux, sa lecture, sa compréhension et sa mise au point deviennent délicates même pour le plus aguerri des développeurs. Il est alors essentiel de scinder le code source en plusieurs fichiers. Prenons l'exemple d'un programme qui effectue des calculs sur les nombres complexes. Notre projet est donc constitué de trois fichiers :

```console
$ tree
.
├── complex.c
├── complex.h
└── main.c
```

Le programme principal et la fonction `main` est contenu dans `main.c` quant au module *complex* il est composé de deux fichiers : `complex.h` l'en-tête et `complex.c`, l'implémentation du module.

Le fichier `main.c` devra inclure le fichier `complex.h` afin de
pouvoir utiliser correctement les fonctions du module de gestion des
nombres complexes. Exemple :

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

Un des avantages majeurs à la création de modules est qu'un module
logiciel peut être réutilisé pour d'autres applications. Plus besoin de
réinventer la roue à chaque application !

Cet exemple sera compilé dans un environnement POSIX de la façon suivante :

```console
gcc -c complex.c -o complex.o
gcc -c main.c -o main.o
gcc complex.o main.o -oprogram -lm
```

Nous verrons plus bas les éléments théoriques vous permettant de mieux comprendre ces lignes.

## Module logiciel

Les applications modernes dépendent souvent de nombreux modules logiciels externes aussi utilisés dans d'autres projets. C'est avantageux à plus d'un titre :

- les modules externes sont sous la responsabilité d'autres développeurs et le programme a développer comporte moins de code ;
- les modules externes sont souvent bien documentés et testés et il est facile de les utiliser ;
- la lisibilité du programme est accrue, car il est bien découpé en des ensembles fonctionnels ;
- les modules externes sont réutilisables et indépendants, ils peuvent donc être réutilisés sur plusieurs projets.

Lorsque vous utilisez la fonction `printf`, vous dépendez d'un module externe nommé `stdio`. En réalité l'ensemble des modules `stdio`, `stdlib`, `stdint`, `ctype`... sont tous groupés dans une seule bibliothèque logicielle nommée `libc` disponible sur tous les systèmes compatibles POSIX. Sous Linux, le pendant libre `glibc` est utilisé. Il s'agit de la bibliothèque [GNU C Library](https://fr.wikipedia.org/wiki/GNU_C_Library).

Un module logiciel peut se composer de fichiers sources, c'est-à-dire un ensemble de fichiers `.c` et `.h` ainsi qu'une documentation et un script de compilation (`Makefile`). Alternativement, un module logiciel peut se composer de bibliothèques déjà compilées sous la forme de fichiers `.h`, `.a` et `.so`. Sous Windows on rencontre fréquemment l'extension `.dll`. Ces fichiers compilés ne donnent pas accès au code source, mais permettent d'utiliser les fonctionnalités quelles offrent dans des programmes C en mettant à disposition un ensemble de fonctions documentées.

## Compilation avec assemblage différé

Lorsque nous avions compilé notre premier exemple [Hello World](c-lang.md#hello-world) nous avions simplement appelé `gcc` avec le fichier source `hello.c` qui nous avait créé un exécutable `a.out`. En réalité, GCC est passé par plusieurs sous-étapes de compilation :

1. **Préprocessing** : les commentaires sont retirés, les directives préprocesseur sont remplacées par leur équivalent C.
2. **Compilation** : le code C d'une seule *translation unit* est converti en langage machine en un fichier objet `.o`.
3. **Édition des liens** : aussi nommés *link*, les différents fichiers objets sont réunis en un seul exécutable.

Lorsqu'un seul fichier est fourni à GCC, les trois opérations sont effectuées en même temps, mais ce n'est plus possible aussitôt que le programme est composé de plusieurs unités de translation (plusieurs fichiers C). Il est alors nécessaire de compiler manuellement chaque fichier source et d'en créer.

La figure suivante résume les différentes étapes de GCC. Les pointillés indiquent à quel niveau les opérations peuvent s'arrêter. Il est dès lors possible de passer par des fichiers intermédiaires assembleur (`.s`) ou objets (`.o`) en utilisant la bonne commande.

![Étapes intermédiaires de compilation avec GCC](../assets/images/gcc.drawio)


Notons que ces étapes existent, quel que soit le compilateur ou le système d'exploitation. Nous retrouverons ces exactes mêmes étapes avec Microsoft Visual Studio, mais le nom des commandes et les extensions des fichiers peuvent varier s'ils ne respectent pas la norme POSIX (et GNU).

Notons que généralement, seul deux étapes de GCC sont utilisées :

1. Compilation avec `gcc -c <fichier.c>`, ceci génère automatiquement un fichier `.o` du même nom que le fichier d'entrée.
2. Édition des liens avec `gcc <fichier1.o> <fichier2.o> ...`, ceci génère automatiquement un fichier exécutable `a.out`.

## Fichiers d'en-tête (*header*)

Les fichiers d'en-tête (`.h`) sont des fichiers écrits en langage C, mais qui ne contiennent pas d'implémentation de fonctions. Un tel fichier ne contient donc pas de `while`, de `for` ou même de `if`. Par convention, ces fichiers ne contiennent que :

- Des prototypes de fonctions (ou de variables).
- Des déclarations de types (`typedef`, `struct`).
- Des définitions préprocesseur (`#include`, `#define`).

Nous l'avons vu dans le chapitre sur le préprocesseur, la directive `#include` ne fais qu'inclure le contenu du fichier cible à l'emplacement de la directive. Il est donc possible (mais fort déconseillé), d'avoir la situation suivante :

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

Lorsque l'on observe le résultat du préprocesseur, on s'aperçoit que toutes les directives préprocesseur ont disparues et que la directive `#include` a été remplacée par de contenu de `foobar.def`. Remarquons que le fichier est inclus deux fois, nous verrons plus loin comme éviter cela.

Nous avons vu au chapitre sur les [prototypes de fonctions](functions.md#function-prototype) qu'il est possible de ne déclarer que la première ligne d'une fonction. Ce prototype permet au compilateur de savoir combien d'arguments est composé une fonction sans nécessairement disposer de l'implémentation de cette fonction. Aussi on trouve dans tous les fichiers d'en-tête des déclarations en amont (*forward declaration*). Dans le fichier d'en-tête `stdio.h` on trouvera la ligne : `int printf( const char *restrict format, ... );`.

```bash
$ cat << EOF > main.c
→ #include <stdio.h>
→ int main() { }
→ EOF
$ gcc -E main.c | grep -P '\bprintf\b'
extern int printf (const char *__restrict __format, ...);
```

Notons qu'ici le prototype est précédé par le mot clé `extern`. Il s'agit d'un mot clé **optionnel** permettant de renforcer l'intention du développeur que la fonction déclarée n'est pas inclue dans fichier courant, mais qu'elle est implémentée ailleurs, dans un autre fichier. Et c'est le cas, car `printf` est déjà compilée quelque part dans la bibliothèque `libc` inclue par défaut lorsqu'un programme C est compilé dans un environnement POSIX.

Un fichier d'en-tête contiendra donc tout le nécessaire utile à pouvoir utiliser une bibliothèque externe.

### Protection de réentrance

La protection de réentrence aussi nommée *header guards* est une solution au problème d'inclusion multiple. Si par exemple on définit dans un fichier d'en-tête un nouveau type et que l'on inclut ce fichier, mais que ce dernier est déjà inclus par une autre bibliothèque, une erreur de compilation apparaîtra :

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

Dans cet exemple l'utilisateur ne sait pas forcément que `bar.h` est déjà inclus avec `foo.h` et le résultat après pré-processing est le suivant :

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

Une solution à ce problème est d'ajouter des gardes d'inclusion multiple par exemple avec ceci:

```c
#ifndef BAR_H
#define BAR_H

typedef struct Bar {
int b, a, r;
} Bar;

#endif // BAR_H
```

Si aucune définition du type `#define BAR_H` n'existe, alors le fichier `bar.h` n'a jamais été inclus auparavant et le contenu de la directive `#ifndef BAR_H` dans lequel on commence par définir `BAR_H` est exécuté. Lors d'une future inclusion de `bar.h`, la valeur de `BAR_H` aura déjà été définie et le contenu de la directive `#ifndef BAR_H` ne sera jamais exécuté.

Alternativement, il existe une solution **non standard**, mais supportée par la plupart des compilateurs. Elle fait intervenir un pragma :

```c
#pragma once

typedef struct Bar {
int b, a, r;
} Bar;
```

Cette solution est équivalente à la méthode traditionnelle et présente plusieurs avantages. C'est tout d'abord une solution atomique qui ne nécessite pas un `#endif` à la fin du fichier. Il n'y a ensuite pas de conflit avec la règle SSOT, car le nom du fichier `bar.h` n'apparaît pas dans le fichier `BAR_H`.

## En profondeur

Pour mieux comprendre la compilation séparée, tentons d'observer le code assembleur généré. Considérons le fichier `foo.c` :

```c
int bar(int);

int foo(int a) {
    return bar(a) + 42;
}
```

Puisqu'il ne contient pas de fonction main, il n'est pas possible de compiler ce fichier en un exécutable car il manque un point d'entrée :

```sh
gcc foo.c
/usr/bin/ld: /usr/lib/x86_64-linux-gnu/Scrt1.o: in function '_start':
(.text+0x24): undefined reference to 'main'
collect2: error: ld returned 1 exit status
```

Le *linker* se termine avec une erreur : *référence à 'main' inexistante*.

En revanche, il est possible de compiler un objet, c'est à dire générer les instructions assembleur. La fonction `bar` étant manquante, le compilateur suppose qu'elle existe quelque part en mémoire et se contentera de dire *moi j'appelle cette fonction ou qu'elle se trouve*.

```sh
$objdump -d foo.o

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

On constate à la ligne `19` que l'addition à bien lieu `eax + 42`, et que l'appel de la fonction `bar` se produit à la ligne `14`.

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
$objdump -d main.o

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

On observe l'appel de la fonction `foo` à la ligne `1f` et l'appel de `printf` à la ligne `32`.

L'assemblage de ces deux fichiers en un exécutable résout les liens en modifiant les adresses d'appel des fonctions puisqu'elles sont maintenant connues (notons que certaines lignes ont été retirées pour plus de lisibilité) :

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

On constate que les appels de fonctions ont été bien remplacés par les bons noms :

- `115d` Appel de `bar`
- `1186` Appel de `foo`
- `1199` Appel de `printf`
