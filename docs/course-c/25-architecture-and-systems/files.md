# Fichiers

## Système de fichiers

Dans un environnement POSIX tout est fichier. `stdin` est un fichier, une souris USB est un fichier, un clavier est un fichier, un terminal est un fichier, un programme est un fichier.

Les fichiers sont organisés dans une arborescence gérée par un [système de fichiers](https://fr.wikipedia.org/wiki/Syst%C3%A8me_de_fichiers). Sous Windows l'arborescence classique est :

```text
C :
├── Program Files         Programmes installés
├── Users                 Comptes utilisateur
│   └── John
│       ├── Desktop
│       ├── Documents
│       └── Music
└── Windows
    ├── Fonts             Polices de caractères
    ├── System32          Système d'exploitation 64-bits (oui, oui)
    └── Temp              Fichiers temporaires
```

Il y a une arborescence par disque physique `C:`, `D:`, une arborescence par chemin réseau `\\eistore2`, etc. Sous POSIX, la stratégie est différente, car il n'existe qu'un seul système de fichier dont la racine est `/`.

```text
/
├── bin                   Programmes exécutables cruciaux
├── dev                   Périphériques (clavier, souris ...)
├── usr
│   └── bin               Programmes installés
├── mnt                   Points de montage (disques réseaux, CD, clé USB)
│   └── eistore2
├── tmp                   Fichiers temporaires
├── home                  Comptes utilisateurs
│   └── john
│       └── documents
└── var                   Fichiers variables comme les logs ou les database
```

Chaque élément qui contient d'autres éléments est appelé un **répertoire** ou **dossier**, en anglais *directory*. Chaque répertoire contient toujours au minimum deux fichiers spéciaux :

`.`

: Un fichier qui symbolise le répertoire courant, celui dans lequel je me trouve

`..`

: Un fichier qui symbolise le répertoire parent, c'est à dire `home` lorsque je suis dans `john`.

La localisation d'un fichier au sein d'un système de fichier peut être soit **absolue** soit **relative**. Cette localisation s'appelle un **chemin** ou *path*. La convention est d'utiliser le symbole :

- Slash `/` sous POSIX
- Antislash `\` sous Windows

Le chemin `/usr/bin/.././bin/../../home/john/documents` est correct, mais il n'est pas [canonique](https://fr.wikipedia.org/wiki/Canonique_(math%C3%A9matiques)), on dit qu'il n'est pas résolu. La forme canonique est `/home/john/documents`.

Un chemin peut être relatif s'il ne commence **pas** par un `/`: `../bin`. Sous Windows du même acabit, mais la racine différemment selon le type de média `C:\`, `\\network`...

Lorsqu'un programme s'exécute, son contexte d'exécution est toujours par rapport à son emplacement dans le système de fichier, donc le chemin peut être soit relatif, soit absolu.

### Navigation

Sous Windows (PowerShell) ou un système **POSIX** (Bash/Sh/Zsh), la navigation dans une arborescence peut être effectuée en ligne de commande à l'aide des commandes (programmes) suivants :

`ls`

: est un raccourci du nom *list*, ce programme permet d'afficher sur la sortie standard le contenu d'un répertoire.

`cd`

: pour *change directory* permets de naviguer dans l'arborescence. Le programme prend en argument un chemin absolu ou relatif. En cas d'absence d'arguments, le programme redirige vers le répertoire de l'utilisateur courant.

## Format d'un fichier

Un fichier peut avoir un contenu arbitraire; une suite de zéro et d’un binaire. Selon l'interprétation, un fichier pourrait contenir une image, un texte ou un programme. Le cas particulier ou le contenu est lisible par un éditeur de texte, on appelle ce fichier un [fichier texte](https://fr.wikipedia.org/wiki/Fichier_texte). C'est-à-dire que chaque caractère est encodé sur 8-bit et que la table ASCII est utilisée pour traduire le contenu en un texte intelligible. Lorsque le contenu n'est pas du texte, on l'appelle un [fichier binaire](https://fr.wikipedia.org/wiki/Fichier_binaire).

La frontière est parfois assez mince, car parfois le fichier binaire peut contenir du texte intelligible, la preuve avec ce programme :

```c
#include <stdio.h>
#include <string.h>

int main(int* argc, char* argv[])
{
    static const char password[] = "un mot de passe secret";
    return strcmp(argv[1], password);
}
```

Si nous le compilons et cherchons dans son code binaire :

```text
$ gcc example.c
$ hexdump -C a.out | grep -C3 sec
06f0  f3 c3 00 00 48 83 ec 08  48 83 c4 08 c3 00 00 00 | ....H...H....... |
0700  01 00 02 00 00 00 00 00  00 00 00 00 00 00 00 00 | ................ |
0710  75 6e 20 6d 6f 74 20 64  65 20 70 61 73 73 65 20 | un mot de passe  |
0720  73 65 63 72 65 74 00 00  01 1b 03 3b 3c 00 00 00 | secret.....;<... |
0730  06 00 00 00 e8 fd ff ff  88 00 00 00 08 fe ff ff | ................ |
0740  b0 00 00 00 18 fe ff ff  58 00 00 00 22 ff ff ff | ........X..."... |
0750  c8 00 00 00 58 ff ff ff  e8 00 00 00 c8 ff ff ff | ....X........... |
```

Sous un système POSIX, il n'existe aucune distinction formelle entre un fichier binaire et un fichier texte. En revanche sous Windows, il existe une subtile différence concernant surtout le caractère de fin de ligne. La commande `copy a.txt + b.txt c.txt` considère des fichiers textes et ajoutera automatiquement une fin de ligne entre chaque partie concaténée, mais celle-ci `copy /b a.bin + b.bin c.bin` ne le fera pas.

## Ouverture d'un fichier

Sous POSIX, un programme doit demander au système d'exploitation l'accès à un fichier soit en lecture, soit en écriture soit les deux. Le système d'exploitation retourne un descripteur de fichier qui est simplement un entier unique pour le programme.

```c
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>

int main(void)
{
    int fd = open("toto", O_RDONLY);
    printf("%d\n", fd);
    getchar();
}
```

Lorsque le programme ci-dessus est exécuté, il va demander l'ouverture du fichier `toto` en lecture et recevoir un descripteur de fichier `fd` (*file descriptor*) positif en cas de succès ou négatif en cas d'erreur.

Dans l'exemple suivant, on compile, puis exécute en arrière-plan le programme qui ne se terminera pas puisqu'il attend un caractère d'entrée. L'appel au programme `ps` permet de lister la liste des processus en cours et la recherche de `test` permet de noter le numéro du processus, ici `6690`. Dans l'arborescence de fichiers, il est possible d'aller consulter les descripteurs de fichiers ouverts pour le processus concerné.

```console
$ gcc test.c -o test && ./test &
$ ps -u | grep test
ycr       6690  0.0  0.0  10540   556 pts/4    T    11:19   0:00 test
$ ls /proc/6690/fd
0  1  2  3
```

On observe que trois descripteurs de fichiers sont ouverts.

- `0` pour `STDIN`
- `1` pour `STDOUT`
- `2` pour `STDERR`
- `3` pour le fichier `toto` ouvert en lecture seule

La fonction `open` est en réalité un appel système qui n'est standardisé que sous POSIX, c'est-à-dire que son utilisation n'est pas portable. L'exemple cité est principalement évoqué pour mieux comprendre le mécanisme de fond pour l'accès aux fichiers.

En réalité la bibliothèque standard, respectueuse de C99, dispose d'une fonction `fopen` pour *file open* qui offre plus de fonctionnalités. Ouvrir un fichier se résume donc à

```c
#include <stdio.h>

int main(void)
{
    FILE *fp = fopen("toto", "r");

    if (fp == NULL) {
        return -1; // Error the file cannot be accessed
    }

    // ...
}
```

Le mode d'ouverture du fichier peut être :

`r`

: Ouverture en lecture seule depuis le début du fichier.

`r+`

: Ouverture pour lecture et écriture depuis le début du fichier.

`w`

: Ouverture en écriture. Le fichier est créé s'il n'existe pas déjà, sinon le contenu est effacé. Le pointeur de fichier est positionné au début de ce dernier.

`w+`

: Ouverture en écriture et lecture. Le fichier est créé s'il n'existe pas déjà. Le pointeur de fichier est positionné au début de ce dernier.

`a`

: Ouverture du fichier pour insertion. Le fichier est créé s'il n'existe pas déjà. Le pointeur est positionné à la fin du fichier.

`a+`

: Ouverture du fichier pour lecture et écriture. Le fichier est créé s'il n'existe pas déjà et le pointeur du fichier est positionné à la fin.

Sous Windows et pour soucis de compatibilité, selon la norme C99, le flag `b` pour *binary* existe. Pour ouvrir un fichier en mode binaire, on peut alors écrire `rb+`.

L'ouverture d'un fichier cause, selon le mode, un accès exclusif au fichier. C'est-à-dire que d'autres programmes ne pourront pas accéder à ce fichier. Il est donc essentiel de toujours refermer l'accès à un fichier dès lors que l'opération de lecture ou d'écriture est terminée :

```c
flose(fp);
```

On peut noter que sous POSIX, écrire sur `stdout` ou `stderr` est exactement la même chose qu'écrire sur un fichier, il n'y a aucune distinction.

!!! exercise "Numéro de ligne"

    Écrire un programme qui saisit le nom d'un fichier texte, ainsi qu'un texte à rechercher. Le programme affiche ensuite le numéro de toutes les lignes du fichier contenant le texte recherché.

    ```bash
    $ ./search
    Fichier: foo.txt
    Recherche: bulbe

    4
    5
    19
    132
    981
    ```

    Question subsidiaire: que fait le programme suivant :

    ```bash
    $ grep foo.txt bulbe
    ```

## Navigation dans un fichier

Lorsqu'un fichier est ouvert, un curseur virtuel est positionné soit au début soit à la fin du fichier. Lorsque des données sont lues ou écrites, c'est à la position de ce curseur, lequel peut être déplacé en utilisant plusieurs fonctions utilitaires.

La navigation dans un fichier n'est possible que si le fichier est *seekable*. Généralement les pointeurs de fichiers `stdin`, `stdout` et `stderr` ne sont pas *seekable*, et il n'est pas possible de se déplacer dans le fichier, mais seulement écrire dedans.

### fseek

La fonction `fseek` permet de déplacer le curseur dans un fichier ouvert. La signature de la fonction est la suivante :

```c
int fseek(FILE *stream, long int offset, int whence)
```

Le manuel [man fseek](http://man7.org/linux/man-pages/man3/fseek.3.html) indique les trois constantes possibles pour `whence`:

`SEEK_SET`

: Positionne le curseur au début du fichier.

`SEEK_CUR`

: Position courante du curseur. Permets d'ajouter un offset relatif à la position courante.

`SEEK_END`

: Positionne le curseur à la fin du fichier.


Si un fichier est seekable, il est possible de se déplacer dans le fichier. Par exemple, pour lire le dernier caractère d'un fichier :

```c
#include <stdio.h>

int main(void)
{
    FILE *fp = fopen("toto", "r");

    if (fp == NULL) return -1;

    fseek(fp, -1, SEEK_END);
    char c = fgetc
    printf("%c\n", c);
}
```

### ftell

Il est parfois utile de savoir où se trouve le curseur. `ftell()` retourne la position actuelle du curseur dans un fichier ouvert.

```c
char filename[] = "foo";

FILE *fp = fopen(filename, 'r');
fseek(fp, 0, SEEK_END);
long int size = ftell();

printf("The file %s has a size of %ld Bytes\n", filename, size);
```

### rewind

L'appel `rewind()` est équivalent à `(void) fseek(stream, 0L, SEEK_SET)` et permet de se positionner au début du fichier.

## Lecture / Écriture

La lecture, écriture dans un fichier s'effectue de manière analogue aux fonctions que nous avons déjà vues `printf` et `scanf` pour les flux standards (*stdout*, *stderr*), mais en utilisant les variantes préfixées de `f` :

| Fonction | Description |
| -------- | ----------- |
| `#!c int fscanf(FILE *stream, const char *format, ...)` | Lecture formattée |
| `#!c int fprintf(FILE *stream, const char *format, ...)` | Écriture formattée |
| `#!c int fgetc(FILE *stream)` | Lecture d'un caractère |
| `#!c int fputc(FILE *stream, char char)` | Écriture d'un caractère |
| `#!c char *fgets(char * restrict s, int n, FILE * restrict stream)` | Lecture d'une ligne |
| `#!c int fputs(const char * restrict s, FILE * restrict stream)` | Écriture d'une ligne |

L'utilisation avec `stdin` et `stdout` comme descripteur de fichier est possible, mais il est préférable dans ce cas d'utiliser les fonctions `scanf` et `printf` qui ont les mêmes fonctionnalités.

Les nouvelles fonctions à connaître sont les suivantes :

```c
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream)
```

Elle permet une lecture arbitraire de `nmemb * size` bytes depuis le flux `stream` dans le buffer `ptr`:

```c
int32_t buffer[12] = {0};
fread(buffer, 2, sizeof(int32_t), stdin);
printf("%x\n%x\n", buffer[0], buffer[1]);
```

Exemple d'utilisation :

```console
$ echo -e "0123abcdefgh" | ./a.out
33323130
64636261
```

On notera au passage la nature *little-endian* du système.

La seconde fonction est :

```c
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream)
```

La fonction est similaire à `fread` mais pour écrire sur un flux des données brutes.

## Buffer de fichier

Pour améliorer les performances, C99 prévoit (§7.19.3-3), un espace tampon pour les descripteurs de fichiers qui peuvent être :

1. `unbuffered` (`_IONBF`) : Pas de buffer, les caractères lus ou écrits sont acheminés le plus vite possible de la source à la destination.
2. `fully buffered` (`_IOFBF`) : Le buffer est rempli à chaque lecture ou écriture, puis vidé.
3. `line buffered` (`_IO_LBF`) : Le buffer est rempli à chaque retour à la ligne.

Il faut comprendre qu'à chaque instant un programme souhaite écrire dans un fichier, il doit générer un appel système et donc interrompre le noyau. Un programme qui écrirait caractère par caractère sur la sortie standard agirait de la même manière qu'un employé des postes qui irait distribuer son courrier en ne prenant qu'une enveloppe à la fois, de la centrale de distribution au destinataire.

Par défaut, un pointeur de fichier est *fully buffered*. C'est-à-dire que dans le cas du programme suivant devrait exécuter 10x l'appel système `write`, une fois par caractère.

```c
#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[])
{
    if (argc > 1 && strcmp("--no-buffering", argv[1]) == 0)
        setvbuf(stdout, NULL, _IONBF, 0);

    for (int i = 0; i < 10; i++)
        putchar('c');
}
```

Cependant le comportement réel est différent. Seulement si le buffer est désactivé, que le programme interrompt le noyau pour chaque caractère :

```console
$ gcc buftest.c -o buftest

$ strace ./buftest 2>&1 | grep write
write(1, "cccccccccc", 10cccccccccc)              = 10

$ strace ./buftest --no-buffering 2>&1 | grep write
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
write(1, "c", 1c)                        = 1
```

Le changement de mode peut être effectué avec la fonction `setbuf` ou `setvbuf`:

```c
#include <stdio.h>

int main(void) {
    char buf[1024];

    setbuf(stdout, buf);

    fputs("Allo ?");

    fflush(stdout);
}
```

La fonction `fflush` force l'écriture malgré l'utilisation d'un buffer.

## Fichiers et Flux

Historiquement les descripteurs de fichiers sont appelés `FILE` alors qu'ils sont préférablement appelés `streams` en C++. Un fichier au même titre que `stdin`, `stdout` et `stderr` sont des flux de données. La norme POSIX, décrit que par défaut les flux :

Table: Flux de données standards

| Flux   | Numéro | Description |
| ------ | --- | ----------- |
| `stdin`  | 0 | Flux d'entrée standard |
| `stdout` | 1 | Flux de sortie standard |
| `stderr` | 2 | Flux d'erreur standard |

Ces trois descripteurs de fichiers sont ouverts au début du programme. Le premier fichier ouvert par exemple avec `fopen` sera très probablement assigné à l'identifiant `3`, le suivant à `4`, etc.

Pour se convaincre de cela, on peut exécuter l'exemple suivant avec le programme `strace`:

```c
#include <stdio.h>

int main(void) {
    char c = fgetc(stdin);

    FILE *fd = fopen("file", "w");
    fputc(c, fd);
    fputc(c + 1, stdout);
    fputc(c + 2, stderr);
}
```

Pour mémoire, `strace` permet de capturer les appels système du programme passé en argument et de les afficher. Deux particularités de la commande exécutée sont `2>&1` qui redirige `stderr` vers `stdout` afin de pouvoir rediriger le flux vers `grep`. Ensuite `grep` permet de filtrer la sortie pour n'afficher que les lignes contenant `open`, `read`, `write` ou `close`:

```console
$ echo k | strace ./a.out 2>&1 | grep -P 'open|read|write|close'
read(0, "k\n", 4096)                    = 2
openat(AT_FDCWD, "file", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3
write(2, "m", 1m)                        = 1
write(3, "k", 1)                        = 1
write(1, "l", 1l)                        = 1
```

On peut voir qu’on lit `k\n` sur le flux `0`, soit `stdin`, puis que le fichier `file` est ouvert, il porte l'identifiant `3`, enfin on écrit sur `1`, `2` et `3`.

## Formats de sérialisation

Souvent les fichiers sont utilisés pour stocker de l'information organisée en grille, par exemple, la liste des températures maximales par ville et par mois :

| Pays      | Ville   | 01    | 02    | 03    | 04   | 05   | 06   | 07   | 08   | 09   | 10   | 11    | 12    |
| --------- | ------- | ----- | ----- | ----- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ----- | ----- |
| Suisse    | Zürich  | 0.3   | 1.3   | 5.3   | 8.8  | 13.3 | 16.4 | 18.6 | 18.0 | 14.1 | 9.9  | 4.4   | 1.4   |
| Italie    | Rome    | 7.5   | 8.2   | 10.2  | 12.6 | 17.2 | 21.1 | 24.1 | 24.5 | 20.8 | 16.4 | 11.4  | 8.4   |
| Allemagne | Berlin  | 0.6   | 2.3   | 5.1   | 10.2 | 14.8 | 17.9 | 20.3 | 19.7 | 15.3 | 10.5 | 6.0   | 1.33  |
| Yémen     | Aden    | 25.7  | 26.0  | 27.2  | 28.9 | 31.0 | 32.7 | 32.7 | 31.5 | 31.6 | 28.9 | 27.1  | 26.01 |
| Russie    | Yakutsk | -38.6 | -33.8 | -20.1 | -4.8 | 7.5  | 16.4 | 19.5 | 15.2 | 6.1  | -7.8 | -27.0 | -37.6 |

Il existe plusieurs manières d'écrire ces informations dans un fichier :

- Écriture tabulée
- Écriture avec remplissage
- Utiliser un langage de sérialisation de haut niveau comme JSON, YAML ou XML

### Format tabulé

Un fichier dit tabulé, utilise une [sentinelle](https://fr.wikipedia.org/wiki/Valeur_sentinelle), souvent le caractère de tabulation `\t` pour séparer les données. Chaque ligne du tableau est physiquement séparée de la suivante avec un `\n`:

```text
Pays\tVille\t01\t02\t03\t04\t05\t06\t07\t08\t09\t10\t11\t12\n
Suisse\tZürich\t0.3\t1.3\t5.3\t8.8\t13.3\t16.4\t18.6\t18.0\t14.1\t9.9\t4.4\t1.4\n
Italie\tRome\t7.5\t8.2\t10.2\t12.6\t17.2\t21.1\t24.1\t24.5\t20.8\t16.4\t11.4\t8.4\n
Allemagne\tBerlin\t0.6\t2.3\t5.1\t10.2\t14.8\t17.9\t20.3\t19.7\t15.3\t10.5\t6.0\t1.33\n
Yémen\tAden\t25.7\t26.0\t27.2\t28.9\t31.0\t32.7\t32.7\t31.5\t31.6\t28.9\t27.1\t26.01\n
Russie\tYakutsk\t-38.6\t-33.8\t-20.1\t-4.8\t7.5\t16.4\t19.5\t15.2\t6.1\t-7.8\t-27.0\t-37.6\n
```

Ce fichier peut être observé avec un lecteur hexadécimal :

```console
$ hexdump -C data.dat
00000000  50 61 79 73 09 56 69 6c  6c 65 09 30 31 09 30 32  |Pays.Ville.01.02|
00000010  09 30 33 09 30 34 09 30  35 09 30 36 09 30 37 09  |.03.04.05.06.07.|
00000020  30 38 09 30 39 09 31 30  09 31 31 09 31 32 0a 53  |08.09.10.11.12.S|
00000030  75 69 73 73 65 09 5a c3  bc 72 69 63 68 09 30 2e  |uisse.Z..rich.0.|
00000040  33 09 31 2e 33 09 35 2e  33 09 38 2e 38 09 31 33  |3.1.3.5.3.8.8.13|
00000050  2e 33 09 31 36 2e 34 09  31 38 2e 36 09 31 38 2e  |.3.16.4.18.6.18.|
00000060  30 09 31 34 2e 31 09 39  2e 39 09 34 2e 34 09 31  |0.14.1.9.9.4.4.1|
00000070  2e 34 0a 49 74 61 6c 69  65 09 52 6f 6d 65 09 37  |.4.Italie.Rome.7|
00000080  2e 35 09 38 2e 32 09 31  30 2e 32 09 31 32 2e 36  |.5.8.2.10.2.12.6|
00000090  09 31 37 2e 32 09 32 31  2e 31 09 32 34 2e 31 09  |.17.2.21.1.24.1.|
000000a0  32 34 2e 35 09 32 30 2e  38 09 31 36 2e 34 09 31  |24.5.20.8.16.4.1|
000000b0  31 2e 34 09 38 2e 34 0a  41 6c 6c 65 6d 61 67 6e  |1.4.8.4.Allemagn|
000000c0  65 09 42 65 72 6c 69 6e  09 30 2e 36 09 32 2e 33  |e.Berlin.0.6.2.3|
000000d0  09 35 2e 31 09 31 30 2e  32 09 31 34 2e 38 09 31  |.5.1.10.2.14.8.1|
000000e0  37 2e 39 09 32 30 2e 33  09 31 39 2e 37 09 31 35  |7.9.20.3.19.7.15|
000000f0  2e 33 09 31 30 2e 35 09  36 2e 30 09 31 2e 33 33  |.3.10.5.6.0.1.33|
00000100  0a 59 c3 a9 6d 65 6e 09  41 64 65 6e 09 32 35 2e  |.Y..men.Aden.25.|
00000110  37 09 32 36 2e 30 09 32  37 2e 32 09 32 38 2e 39  |7.26.0.27.2.28.9|
00000120  09 33 31 2e 30 09 33 32  2e 37 09 33 32 2e 37 09  |.31.0.32.7.32.7.|
00000130  33 31 2e 35 09 33 31 2e  36 09 32 38 2e 39 09 32  |31.5.31.6.28.9.2|
00000140  37 2e 31 09 32 36 2e 30  31 0a 52 75 73 73 69 65  |7.1.26.01.Russie|
00000150  09 59 61 6b 75 74 73 6b  09 2d 33 38 2e 36 09 2d  |.Yakutsk.-38.6.-|
00000160  33 33 2e 38 09 2d 32 30  2e 31 09 2d 34 2e 38 09  |33.8.-20.1.-4.8.|
00000170  37 2e 35 09 31 36 2e 34  09 31 39 2e 35 09 31 35  |7.5.16.4.19.5.15|
00000180  2e 32 09 36 2e 31 09 2d  37 2e 38 09 2d 32 37 2e  |.2.6.1.-7.8.-27.|
00000190  30 09 2d 33 37 2e 36 0a                           |0.-37.6.|
00000198
```

L'inconvénient de ce format est que pour obtenir directement la température du mois de mars à Berlin, sachant que Berlin est la quatrième ligne du fichier, il est nécessaire de parcourir le fichier depuis le début, car la longueur des lignes n'est à priori pas connue. On dit que la lecture séquentielle est facilitée, mais la lecture aléatoire est plus lente.

### Format avec remplissage

Pour pallier au défaut du format tabulé, il est possible d'écrire le fichier en utilisant un caractère de remplissage. Dans le fichier suivant, les mois de mai sont toujours alignés avec la
48e colonne :

```text
 0000000000111111111122222222223333333333444444444455555555556666666666777777777788
 0123456789012345678901234567890123456789012345678901234567890123456789012345678901
+---------+-------+-----+-----+-----+----+----+----+----+----+----+----+-----+---->

Pays      Ville   01    02    03    04   05   06   07   08   09   10   11    12
Suisse    Zürich  0.3   1.3   5.3   8.8  13.3 16.4 18.6 18.0 14.1 9.9  4.4   1.4
Italie    Rome    7.5   8.2   10.2  12.6 17.2 21.1 24.1 24.5 20.8 16.4 11.4  8.4
Allemagne Berlin  0.6   2.3   5.1   10.2 14.8 17.9 20.3 19.7 15.3 10.5 6.0   1.33
Yémen     Aden    25.7  26.0  27.2  28.9 31.0 32.7 32.7 31.5 31.6 28.9 27.1  26.01
Russie    Yakutsk -38.6 -33.8 -20.1 -4.8 7.5  16.4 19.5 15.2 6.1  -7.8 -27.0 -37.6
```

Idéalement on utilise comme caractère de remplissage le caractère nul `\0`, mais le caractère espace peut aussi convenir à condition que les données ne contiennent pas d'espace.

La lecture aléatoire de ce type de fichier est facilitée, car la position de chaque entrée est connue à l'avance, on sait par exemple que le pays est stocké sur 11 caractères, la ville sur 9 caractères et chaque température sur 7 caractères.

L'utilisation de `fseek` est par conséquent utile :

```c
int line = 2;
int month = 3;
double temperature;

fseek(fd, line * (11 + 9 + 12 * 7 + 1), SEEK_SET);
fseek(fd, 11 + 9 + month * 7 SEEK_CUR);
fscanf(fd, "%lf", &temperature);
```

L'inconvénient de ce format de fichier est la place qu'il prend en mémoire. L'autre problème est que si le nom d'une ville dépasse les 9 caractères alloués, il faut réécrire tout le fichier. Généralement ce problème est contourné en allouant des champs d'une taille suffisante, par exemple 256 caractères pour le nom des villes.

### Format sérialisé

Des langages de sérialisation permettent de structurer de l'information en utilisant un format spécifique. Ici [JSON](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation) :

```json
[
    {
        "pays": "Suisse",
        "ville": "Zürich",
        "mois": {
            "janvier": 0.3,
            "février": 1.3,
            "mars": 5.3,
            "avril": 8.8,
            "mai": 13.3,
            "juin": 16.4,
            "juillet": 18.6,
            "août": 18.0,
            "septembre": 14.1,
            "octobre": 9.9,
            "novembre": 4.4,
            "décembre": 1.4
        }
    },
    {
        "pays": "Italie",
        "ville": "Rome",
        "mois": {
            "janvier": 7.5,
            "février": 8.2,
            "mars": 10.2,
            "avril": 12.6,
            "mai": 17.2,
            "juin": 21.1,
            "juillet": 24.1,
            "août": 24.5,
            "septembre": 20.8,
            "octobre": 16.4,
            "novembre": 11.4,
            "décembre": 8.4
        }
    }
]
```

L'avantage de ce type de format est qu'il est facilement modifiable avec un éditeur de texte et qu'il est très interopérable. C'est-à-dire qu'il est facilement lisible depuis différents langages de programmation.

En C, on pourra utiliser la bibliothèque logicielle [json-c](https://github.com/json-c/json-c).

## Exercices de révision

!!! exercise "Variantes"

    Considérez les deux programmes ci-dessous très similaires.

    ```c
    #include <stdio.h>

    int main(void)
    {
        char texte[80];

        printf("Saisir un texte:");
        gets(texte);
        printf("Texte: %s\n", texte);
    }
    ```

    ```c
    #include <stdio.h>

    int main(void)
    {
        char texte[80];

        printf("Saisir un texte:");
        fgets(texte, 80, stdin);
        printf("Texte: %s\n", texte);
    }
    ```

    1. Quelle est la différence  entre ces 2 programmes ?
    2. Dans quel cas est-ce que ces programmes auront un comportement différent ?
    3. Quelle serait la meilleure solution ?
