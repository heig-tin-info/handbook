# Programmes et Processus

![Programmeuse en tenue décontractée à côté de 62'500 cartes perforées](../assets/images/vintage-programmer.jpg){width="60%"}

## Qu'est-ce qu'un programme?

Un [programme informatique](https://fr.wikipedia.org/wiki/Programme_informatique) est un ensemble d'opérations destinées à être exécutées par un ordinateur.

Un programme peut se décliner sous plusieurs formes :

- Code source
- Listing assembleur
- Exécutable binaire

Un processus est l'état d'un programme en cours d'exécution. Lorsqu'un programme est exécuté, il devient processus pendant un temps donné. Les [systèmes d'exploitation](https://fr.wikipedia.org/wiki/Syst%C3%A8me_d%27exploitation) tels que Windows sont dits [multitâches](https://fr.wikipedia.org/wiki/Multit%C3%A2che), il peuvent par conséquent faire tourner plusieurs processus en parallèle. Le temps processeur est ainsi partagé entre chaque processus.

### Code source

Le **code source** est généralement écrit par un ingénieur/développeur/informaticien. Il s'agit le plus souvent d'un fichier texte lisible par un être humain et souvent pourvu de commentaires facilitant sa compréhension. Selon le langage de programmation utilisé, la programmation peut être graphique comme avec les diagrammes [Ladder](https://fr.wikipedia.org/wiki/Langage_Ladder) utilisés dans les automates programmables et respectant la norme [IEC 61131-3](https://fr.wikipedia.org/wiki/CEI_61131-3), ou [LabView](https://en.wikipedia.org/wiki/LabVIEW) un outil de développement graphique.

Le plus souvent le code source est organisé en une [arborescence](https://fr.wikipedia.org/wiki/Arborescence) de fichiers. Des programmes complexes comme le noyau Linux contiennent plus de 100'000 fichiers et 10 millions de lignes de code, pour la plupart écrites en C.

### Exécutable binaire

Une fois compilé en [langage machine](https://fr.wikipedia.org/wiki/Langage_machine), il en résulte un fichier qui peut être exécuté soit par un système d'exploitation, soit sur une plateforme embarquée à microcontrôleur sans l'intermédiaire d'un système d'exploitation. On dit que ce type de programme est [bare metal](https://en.wikipedia.org/wiki/Bare_machine), qu'il s'exécute à même le métal.

Un exécutable binaire doit être compilé pour la bonne architecture matérielle. Un programme compilé pour un processeur INTEL ne pourra pas s'exécuter sur un processeur ARM, c'est pourquoi on utilise différents compilateurs en fonctions des architectures cibles. L'opération de compiler un programme pour une autre architecture, ou un autre système d'exploitation que celui sur lequel est installé le compilateur s'appelle la compilation croisée ([cross-compilation](https://en.wikipedia.org/wiki/Cross_compiler)).

Prenons l'exemple du programme suivant qui calcule la suite des nombres de Fibonacci :

```c
--8<-- "docs/assets/src/fibonacci.c"
```

Une fois [assemblé](<https://fr.wikipedia.org/wiki/Assembly_(informatique)>) le code  source est converti en langage assembleur, une version intermédiaire entre le C et le langage machine. L'exemple est compilé en utilisant gcc :

```console
gcc Fibonacci.c -o fibonacci.exe
objdump -d fibonacci.exe
```

On obtient un fichier similaire à ceci qui contient le code machine (`48 83 ec 20`), et l'équivalent en langage assembleur (`mov    %fs:0x28,%rax`):

```console
0000000000000680 <main>:
680:   41 55                   push   %r13
682:   41 54                   push   %r12
684:   48 8d 35 59 02 00 00    lea    0x259(%rip),%rsi
68b:   55                      push   %rbp
68c:   53                      push   %rbx
68d:   bf 01 00 00 00          mov    $0x1,%edi
692:   48 83 ec 18             sub    $0x18,%rsp
696:   64 48 8b 04 25 28 00    mov    %fs:0x28,%rax
69d:   00 00
69f:   48 89 44 24 08          mov    %rax,0x8(%rsp)
6a4:   31 c0                   xor    %eax,%eax
6a6:   e8 a5 ff ff ff          callq  650 <__printf_chk@plt>
6ab:   48 8d 74 24 04          lea    0x4(%rsp),%rsi
6b0:   48 8d 3d 49 02 00 00    lea    0x249(%rip),%rdi
6b7:   31 c0                   xor    %eax,%eax
6b9:   e8 a2 ff ff ff          callq  660 <__isoc99_scanf@plt>
6be:   48 8d 35 3e 02 00 00    lea    0x23e(%rip),%rsi
...
72e:   00 00
730:   75 0b                   jne    73d <main+0xbd>
732:   48 83 c4 18             add    $0x18,%rsp
736:   5b                      pop    %rbx
737:   5d                      pop    %rbp
738:   41 5c                   pop    %r12
73a:   41 5d                   pop    %r13
73c:   c3                      retq
73d:   e8 fe fe ff ff          callq  640 <__stack_chk_fail@plt>
742:   66 2e 0f 1f 84 00 00    nopw   %cs:0x0(%rax,%rax,1)
749:   00 00 00
74c:   0f 1f 40 00             nopl   0x0(%rax)
```

Avec un visualiseur hexadécimal, on peut extraire le langage machine du binaire exécutable. L'utilitaire `hexdump` est appelé avec deux options `-s` pour spécifier l'adresse de début, on choisit ici celle du début de la fonction `main` `0x680`, et `-n` pour n'extraire que les premiers 256 octets :

```console
$ hexdump -s0x680 -n256 a.out
0000680 5541 5441 8d48 5935 0002 5500 bf53 0001
0000690 0000 8348 18ec 4864 048b 2825 0000 4800
00006a0 4489 0824 c031 a5e8 ffff 48ff 748d 0424
00006b0 8d48 493d 0002 3100 e8c0 ffa2 ffff 8d48
00006c0 3e35 0002 3100 bfc0 0001 0000 7fe8 ffff
00006d0 8bff 2444 8504 74c0 4c3d 2d8d 0236 0000
00006e0 bc41 0001 0000 01bd 0000 3100 0fdb 001f
00006f0 da89 c031 894c bfee 0001 0000 8349 01c4
0000700 4be8 ffff 8dff 2b04 eb89 c589 6348 2444
0000710 4c04 e039 da73 0abf 0000 e800 ff10 ffff
0000720 c031 8b48 244c 6408 3348 250c 0028 0000
0000730 0b75 8348 18c4 5d5b 5c41 5d41 e8c3 fefe
0000740 ffff 2e66 1f0f 0084 0000 0000 1f0f 0040
0000750 ed31 8949 5ed1 8948 48e2 e483 50f0 4c54
0000760 058d 016a 0000 8d48 f30d 0000 4800 3d8d
0000770 ff0c ffff 15ff 0866 0020 0ff4 441f 0000
```

Il est facile de voir la correspondance entre l'assembleur et l'exécutable binaire. Les valeurs `41 55` puis `41 54` puis `48 8d 35 59` se retrouvent directement dans le *dump*: `5541 5441 8d48`. Si les valeurs sont interverties, c'est parce qu'un PC est *little-endian* (c.f. {numref}`endianess`), les octets de poids faible apparaissent par conséquent en premier dans la mémoire.

Sous Windows, l'extension des fichiers détermine leur type. Un fichier avec l'extension `.jpg` sera un fichier image du [Join Photographic Experts Group](https://fr.wikipedia.org/wiki/JPEG) et exécuter ce fichier correspond à l'ouvrir en utilisant l'application par défaut pour visualiser les images de ce type. Un fichier avec l'extension `.exe` est un exécutable binaire, et il sera exécuté en tant que programme par le système d'exploitation.

Sous POSIX (Linux, macOS, UNIX), les *flags* d'un fichier qualifient son type. Le programme `ls` permet de visualiser les flags du programme `Fibonacci` que nous avons compilé:

```console
$ ls -al a.out
-rwxr-xr-x 1 root ftp 8.3K Jul 17 09:53 Fibonacci
```

Les lettres `r-x` indiquent :

`r`

: Lecture autorisée

`w`

: Écriture autorisée

`x`

: Exécution autorisée

Ce programme peut-être exécuté par tout le monde, mais modifié que par l'utilisateur `root`.

### Entrées sorties

Tout programme doit pouvoir interagir avec son environnement. À l'époque des téléscripteurs, un programme interagissait avec un clavier et une imprimante matricielle. Avec l'arrivée des systèmes d'exploitation, le champ d'action fut réduit à des entrées :

- L'entrée standard `STDIN` fournit au programme du contenu qui est généralement fourni par la sortie d'un autre programme.
- Les arguments du programme `ARGV`
- Les variables d'environnement `ENVP`

Ainsi qu'à des sorties :

- La sortie standard `STDOUT` est généralement affichée à l'écran
- La sortie d'erreur standard `STDERR` contient des détails sur les éventuelles erreurs d'exécution du programme.

La figure suivante résume les interactions qu'un programme peut avoir sur son environnement. Les appels système ([syscall](https://fr.wikipedia.org/wiki/Appel_syst%C3%A8me)) sont des ordres transmis directement au système d'exploitation. Ils permettent par exemple de lire des fichiers, d'écrire à l'écran, de mettre le programme en pause ou de terminer le programme.

![Résumé des interactions avec un programme](../assets/images/program.drawio)

### Signaux

Lorsqu'un programme est en cours d'exécution, il peut recevoir de la part du système d'exploitation des [signaux](<https://fr.wikipedia.org/wiki/Signal_(informatique)>). Il s'agit d'une notification asynchrone envoyée à un processus pour lui signaler l'apparition d'un évènement.

Si, en utilisant Windows, vous vous rendez dans le [gestionnaire de tâches](https://fr.wikipedia.org/wiki/Gestionnaire_des_t%C3%A2ches_Windows) et que vous décidez de *Terminer une tâche*, le système d'exploitation envoie un signal au programme lui demandant de se terminer.

Sous Linux, habituellement, le *shell* relie certains raccourcis clavier à des signaux particuliers :

- ++ctrl+c++ envoie le signal `SIGINT` pour interrompre l'exécution d'un programme
- ++ctrl+z++ envoie le signal `SIGTSTP` pour suspendre l'exécution d'un programme
- ++ctrl+t++ envoie le signal `SIGINFO` permettant de visualiser certaines informations liées à l'exécution du processus.

Si le programme suivant est exécuté, il sera bloquant, c'est-à-dire qu'à moins d'envoyer un signal d'interruption, il ne sera pas possible d'interrompre le processus :

```c
int main(void)
{
    for(;;);
}
```

## Arguments et options

L'interpréteur de commande `cmd.exe` sous Windows ou `bash` sous Linux, fonctionne de façon assez similaire. L'**invite de commande** nommée *prompt* en anglais invite l'utilisateur à entrer une commande. Sous [DOS](https://fr.wikipedia.org/wiki/DOS) puis sous Windows cet invite de commande ressemble à ceci :

```console
C:\>
```

Sous Linux, le prompt est largement configurable et dépend de la distribution installée, mais le plus souvent il se termine par le caractère `$` ou `#`.

Une commande débute par le nom de cette dernière, qui peut être le nom du programme que l'on souhaite exécuter puis vient les arguments et les options.

- Une **option** est par convention un **argument** dont le préfixe est `-` sous Linux ou `/` sous Windows même si le standard GNU gagne du terrain. Aussi, le consensus le plus large semble être le suivant :
- Une option peut être exprimée soit sous format court `-o`, `-v`, soit sous format long `--output=`, `--verbose` selon qu'elle commence par un ou deux tirets. Une option peut être un booléenne (présence ou non de l'option), ou scalaire, c'est-à-dire être associée à une valeur `--output=foo.o`. Les options modifient le comportement interne d'un programme.

Un argument est une chaîne de caractères utilisée comme entrée au programme. Un programme peut avoir plusieurs arguments.

En C, c'est au développeur de distinguer les options des arguments, car ils sont tous passés par le paramètre `argv`:

```c
#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Liste des arguments et options passés au programme:\n");

    for (size_t i = 0; i < argc; i++) {
        printf("  %u. %s\n", i, argv[i]);
    }
}
```

```console
$ argverbose --help -h=12 3.14 'Baguette au beurre' $'\t-Lait\n\t-Viande\n\t-Oeufs\f'
Liste des arguments et options passés au programme :
0. ./a.out
1. --help
2. -h=12
3. 3.14
4. Baguette au beurre
5.  -Lait
    -Viande
    -Oeufs
```

### Norme POSIX

Le standard POSIX décrit une façon de distinguer des *options* passées à un programme. Par exemple, le programme [cowsay](https://en.wikipedia.org/wiki/Cowsay) peut être paramétré pour changer son comportement en utilisant des `options` standards comme `-d`. La fonction `getopt` disponible dans la bibliothèque `<unistd.h>` permet de facilement interpréter ces options.

```c
int getopt(int, char * const [], const char *);
```

### Extension GNU

Malheureusement, la norme POSIX ne spécifie que les options dites courtes (un tiret suivi d'un seul caractère). Une extension [GNU](https://fr.wikipedia.org/wiki/GNU) et son en-tête `<getopt.h>` permet l'accès à la fonction `getopt_long` laquelle permet d'interpréter aussi les options longues `--version` qui sont devenues très répandues.

```c
int getopt_long (int argc, char *const *argv, const char *shortopts,
                 const struct option *longopts, int *longind);
```

Ci-dessous une possible utilisation de cette fonction :

```c
--8<-- "docs/assets/src/options.c"
```

### Windows

Windows utilise à l'instar de `RDOS` ou [OpenVMS](https://en.wikipedia.org/wiki/OpenVMS), le caractère *slash* pour identifier ses options. Alors que sous POSIX l'affichage de la liste des fichiers s'écrira peut-être `ls -l -s D*`, sous Windows on utilisera `dir /q d* /o:s`.

## Fonction main

Le standard définit une fonction nommée `main` comme étant la fonction principale appelée à l'exécution du programme. Or, sur un système d'exploitation, la fonction `main` a déjà été appelée il y a belle lurette lorsque l'ordinateur a été allumé et que le [BIOS](https://en.wikipedia.org/wiki/BIOS) a chargé le système d'exploitation en mémoire. Dès lors la fonction `main` de notre programme [Hello World](c-lang.md#hello-world) n'est pas la première, mais est appelé.

### Qui appelle main ?

Un exécutable binaire à un format particulier appelé **ELF** ([Executable and Linkable Format](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format)) qui contient un **point d'entrée** qui sera l'adresse mémoire de début du programme. Sous un système POSIX ce point d'entrée est nommé `_init`. C'est lui qui est responsable de récolter les informations transmises par le système d'exploitation. Ce dernier transmet sur la **pile** du programme :

- Le nombre d'arguments `argc`
- La liste des arguments `argv`
- Les variables d'environnements `envp`
- Les pointeurs de fichiers sur `stdout`, `stdin`, `stderr`

C'est la fonction `__libc_start_main` de la bibliothèque standard qui a la responsabilité d'appeler la fonction `main`. Voici son prototype :

```c
int __libc_start_main(int (*main) (int, char**, char**),
    int argc, char** ubp_av,
    void (*init)(void),
    void (*fini)(void),
    void (*rtld_fini)(void),
    void (*stack_end)
);
```

### Valeur de retour

La fonction `main` renvoie toujours une valeur de retour qui agit comme le statut de sortie d'un programme ([exit status](https://en.wikipedia.org/wiki/Exit_status)). Sous POSIX et sous Windows, le programme parent s'attend à recevoir une valeur 32-bits à la fin de l'exécution d'un programme. L'interprétation est la suivante :

`0`

: Succès, le programme s'est terminé correctement.

`!0`

: Erreur, le programme ne s'est pas terminé correctement.

Par exemple le programme `printf` retourne dans le cas précis l'erreur 130 :

```console
$ printf '%d' 42
42
$ echo $?
0

$ printf '%d' 'I am not a number'
printf: I am not a number: invalid number
$ echo $?
130
```

## Entrées sorties standards

Le fichier d'en-tête `stdio.h` ([man stdio](http://man7.org/linux/man-pages/man3/stdio.3.html)) permet de simplifier l'interaction avec les fichiers. Sous Linux et MacOS principalement, mais d'une certaine manière également sous Windows, les canaux d'échanges entre un programme et son hôte (*shell*, gestionnaire de fenêtre, autre programme), se font par l'intermédiaire de fichiers particuliers nommés `stdin`, `stdout` et `stderr`.

La fonction de base est `putchar` qui écrit un caractère sur `stdout`:

```console
#include <stdio.h>

int main(void) {
    putchar('H');
    putchar('e');
    putchar('l');
    putchar('l');
    putchar('o');
    putchar('\n');
}
```

Bien vite, on préfèrera utiliser `printf` qui simplifie le formatage de chaînes de caractères et qui permet à l'aide de marqueurs (*tokens*) de formater des variables :

```c
#include <stdio.h>

int main(void) {
    printf("Hello\v");
    printf("%d, %s, %f", 0x12, "World!", 3.1415);
}
```

Il peut être nécessaire, surtout lorsqu'il s'agit d'erreurs qui ne concernent pas la sortie standard du programme, d'utiliser le bon canal de communication, c'est-à-dire `stderr` au lieu de `stdout`. La fonction `fprintf` permet de spécifier le flux standard de sortie :

```c
#include <stdio.h>

int main(void) {
    fprintf(stdout, "Sortie standard\n");
    fprintf(stderr, "Sortie d'erreur standard\n");
}
```

Pourquoi, me direz-vous, faut-il séparer la sortie standard du canal d'erreur? Le plus souvent un programme n'est pas utilisé seul, mais en conjonction avec d'autres programmes :

```console
$ echo "Bonjour" | tr 'A-Za-z' 'N-ZA-Mn-za-m' > data.txt
$ cat data.txt
Obawbhe
```

Dans cet exemple ci-dessus, le programme `echo` prend en argument la chaîne de caractère `Bonjour` qu'il envoie sur la sortie standard. Ce flux de sortie est relié au flux d'entrée du programme `tr` qui effectue une opération de [ROT13](https://fr.wikipedia.org/wiki/ROT13) et envoie le résultat sur la sortie standard. Ce flux est ensuite redirigé sur le fichier `data.txt`.
La commande suivante `cat` lis le contenu du fichier dont le nom est passé en argument et écrit le contenu sur la sortie standard.

Dans le cas où un de ces programmes génère une alerte (*warning*), le texte ne sera pas transmis le long de la chaîne, mais simplement affiché sur la console. Il est donc une bonne pratique que d'utiliser le bon flux de sortie: `stdout` pour la sortie standard et `stderr` pour les messages de diagnostic et les erreurs.

## Boucle d'attente

Comme évoqué, un programme est souvent destiné à tourner sur un système d'exploitation. Un programme simple comme celui-ci :

```c
int main(void) {
    for(;;) {}
}
```

consommera 100% des ressources du processeur. En d'autres termes, le processeur dépensera toute son énergie à faire 150 millions de calculs par seconde, pour rien. Et les autres processus n'auront que très peu de ressources disponibles pour tourner.

Il est grandement préférable d'utiliser des appels système pour indiquer au noyau du système d'exploitation que le processus souhaite être mis en pause pour un temps donné. Le programme suivant utilise la fonction standard `sleep` pour demander au noyau d'être mis en attente pour une période de temps spécifiée en paramètre.

```c
#include <unistd.h>

int main(void) {
    for(;;) {
        sleep(1 /* seconds */);

        ...
    }
}
```

Alternativement, lorsqu'un programme attend un retour de l'utilisateur par exemple en demandant la saisie au clavier d'informations, le système d'exploitation est également mis en attente et le processus ne consomme pas de ressources CPU. Le programme ci-dessous attend que l'utilisateur presse la touche entrée.

```c
#include <stdio.h>

int main(void) {
    for(;;) {
        getchar();
        printf("Vous avez pressé la touche enter (\\n)\n");
    }
}
```

!!! exercise "La fortune, la vache qui dit et le chat drôle"

    En rappelant l'historique des dernières commandes exécutées sur l'ordinateur du professeur pendant qu'il avait le dos tourné, vous tombez sur cette commande :

    ```bash
    $ fortune | cowsay | lolcat
    ```

    Quelle est sa structure et que fait-elle ?
