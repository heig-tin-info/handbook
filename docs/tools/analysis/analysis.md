# Diagnostics

Les outils de diagnostic permettent de comprendre le comportement d'un programme en cours d'exécution. Ils permettent de voir les appels système, les appels de fonctions, les appels de bibliothèques, les appels de fonctions système, les appels de fonctions de bibliothèques.

## time

`time` est une commande Unix qui permet de mesurer le temps d'exécution d'un programme. Elle est utilisée pour mesurer le temps d'exécution d'un programme et les ressources utilisées par ce programme. L'utilisation typique est la suivante:

```bash
time ./a.out
./a.out 1.23s user 0.10s system 78% cpu 1.23 total
```

On note plusieurs métriques:

- `user` est le temps passé dans l'espace utilisateur, c'est le temps réel passé par le programme à exécuter des instructions.
- `system` est le temps passé dans l'espace noyau, c'est le temps passé par le programme à exécuter des appels système.
- `wall` ou `real` est le temps réel passé par le programme à s'exécuter. C'est le temps qui s'écoule entre le lancement du programme et sa fin.
- `cpu` est le pourcentage de temps CPU utilisé par le programme.

Un programme multi-threadé peut utiliser plus de 100% de CPU si plusieurs threads sont exécutés en parallèle. Par exemple un programme qui s'exécuterait de manière parallèle sur 5 processeurs et dont le temps mur serait de 1 secondes, aurait un temps CPU de 500% et un temps `user` de 5 seconde.

## strace

Strace a été initialement écrit pour SunOS par Paul Kranenburg en 1991. Il a été porté sur Linux par Branko Lankester en 1992. Strace est un outil de diagnostic qui permet de suivre les appels système et les signaux reçus par un processus. Il est très utile pour comprendre le comportement d'un programme en cours d'exécution.

Son code source est bien entendu disponible sur [GitHub](https://github.com/strace/strace) et il est écrit en C.

L'utilisation typique est la suivante, où `PID` est le numéro de processus du programme à tracer.

```bash
strace -o /tmp/strace.log -f -e trace=all -p PID
```

Il est également possible d'exécuter un programme avec `strace` directement.

```bash
strace ./a.out
```

### Cas d'utilisation

#### Analyse de performance

Les performances d'un programme peuvent être impactées par des appels système trop nombreux. Lorsqu'un programme communique avec le système d'exploitation (lecture disque, réseau, etc.), il doit passer par des appels système. Ces appels peuvent être coûteux en temps et en ressources car ils nécessitent un changement de contexte entre le mode utilisateur et le mode noyau. C'est-à-dire que le programme doit se mettre en pause pour laisser le noyau effectuer l'opération demandée. Lors de la mesure du temps d'exécution d'un programme, par exemple avec `time`, on peut noter le temps *system* qui correspond au temps passé dans le noyau. Si ce temps est trop élevé, cela peut indiquer que le programme n'est pas efficace car il passe son temps à attendre des opérations d'entrée/sortie. `strace` permet dans ce cas de mesurer le nombre d'appels système et de les analyser pour comprendre pourquoi le programme est lent.

À titre d'exemple, prenons la sortie standard. Dans le standard POSIX, un programme n'est pas directement connecté à la sortie standard. La bibliothèque standard C utilise un tampon pour stocker les données avant de les envoyer à la sortie standard. Ce tampon est automatiquement vidé selon certaines conditions notamment:

- lorsqu'un caractère de fin de ligne est écrit,
- lorsque le programme se termine,
- lorsque le tampon est plein,
- lorsque le programme appelle `fflush` ou `fclose`.

Si vous écrivez par exemple le code suivant, ce n'est que lorsque le caractère `\n` est écrit que le tampon est vidé et que l'appel système `write` est effectué. On peut le vérifier avec `strace`

```c
printf("foo");
printf("bar");
printf("\n");
```

Cette exécution est reportée avec la ligne suivante. On observe que les trois opérations `printf` sont regroupées dans un seul appel système.

```text
write(1, "foobar\n", 7)                 = 7
```

En revanche, si le programme est modifié pour vider le tampon après chaque caractère, on observe davantage d'appels système:

```c
int main() {
   char *str = "foobar\n";
   while (*str) {
      putchar(*(str++));
      fflush(stdout);
   }
}
```

```text
write(1, "f", 1)     = 1
write(1, "o", 1)     = 1
write(1, "o", 1)     = 1
write(1, "b", 1)     = 1
write(1, "a", 1)     = 1
write(1, "r", 1)     = 1
write(1, "\n", 1)     = 1
```

#### Suivi des opérations d'entrée/sortie

`strace` permet de suivre les opérations d'entrée/sortie d'un programme. Cela peut être utile pour comprendre pourquoi un programme ne fonctionne pas correctement. Par exemple, si un programme lit un fichier et que le fichier n'est pas trouvé, `strace` permet de voir l'appel système `open` et le code d'erreur `ENOENT` qui indique que le fichier n'existe pas.

Dans ce cas on ne sera sensible qu'aux appels système `open`  et `write`:

```bash
strace -e trace=open,read,write ./a.out
```

#### Résolution des dépendances

Au début de l'exécution du programme, avant que le `main` ne soit exécuté, la bibliothèque standard C doit être chargée. `strace` permet de voir les dépendances du programme et les bibliothèques qui sont chargées. Cela peut être utile pour comprendre pourquoi un programme ne fonctionne pas correctement ou pourquoi il ne trouve pas une bibliothèque. On observera typiquement au début de la sortie de `strace` quelque chose de similaire à ceci :

```bash
execve("./a.out", ["./a.out"], 0x7ffec3bd4ef0 /* 50 vars */) = 0

brk(NULL) = 0x56475a63a000
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f2143f6f000
access("/etc/ld.so.preload", R_OK) = -1 ENOENT (No such file or directory)

openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=87775, ...}) = 0
mmap(NULL, 87775, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f2143f59000
close(3) = 0

openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\(...)"..., 832) = 832
pread64(3, "\6\0\0\0\4\0\0\0@\0(...)"..., 784, 64) = 784
fstat(3, {st_mode=S_IFREG|0755, st_size=2125328, ...}) = 0
pread64(3, "\6\0\0\0\4\0\0\0@(...)"..., 784, 64) = 784
mmap(NULL, 2170256, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f2143d47000
mmap(0x7f2143d6f000, ...)
mmap(0x7f2143ef7000, ...)
mmap(0x7f2143f46000, ...)
mmap(0x7f2143f4c000, ...)
close(3)
```

Analysons en détail les premières lignes de la sortie de `strace`:

1. `execve` démarre l'exécution du programme `./a.out`. C'est le tout premier appel système qui est effectué.
2. `brk` ajuste la taille du `heap` du programme. Appelé avec `NULL`, le noyau retourne la limite actuelle du `heap`.
3. `mmap` alloue de la mémoire, ici 8 kio pour des besoins internes.
4. `access("/etc/ld.so.preload")` permet d'injecter des bibliothèques avant le chargement des bibliothèques standard. Ici, le fichier n'existe pas. C'est notament utilisé pour les outils de *profiling*. On observe l'erreur `ENOENT` qui signifie que le fichier n'existe pas.
5. `openat` ouvre le fichier `/etc/ld.so.cache` qui contient les chemins des bibliothèques partagées précompilées. Le système y accède pour localiser rapidement les bibliothèques dynamiques nécessaires plutôt que de les charger depuis le disque
6. `mmap` alloue de l'espace mémoire pour le fichier `/etc/ld.so.cache`.
7. `close` ferme le fichier `/etc/ld.so.cache` une fois chargé.
8. `openat` permet de charger la bibliothèque standard C `libc.so.6` qui est située dans `/lib/x86_64-linux-gnu/`.
9. Les autres `mmap` permettent de charger la bibliothèque standard C en mémoire afin de pouvoir être utilisées par le programme.

On observe donc des éléments importants de l'exécution d'un programme. Les bibliothèques dynamiques sont chargées en mémoire au début de l'exécution du programme. Si ces bibliothèques sont absentes du système, il ne pourra pas être exécuté.

#### Suivi des threads

Lors d'un programme concurrent, il est possible de suivre la création et la terminaison des threads avec `strace`, notament au moyen des appels système `fork`, `clone` ou `exec`. Les appels à `futex` permettent de voir les opérations de synchronisation entre les threads utilisés par les mutex et les variables de condition.

### Fonctionnement interne

Le fonctionnement de cet outil repose sur `ptrace` qui est une fonction du noyau Linux qui permet de suivre l'exécution d'un processus. `strace` utilise cette fonction pour intercepter les appels système et les signaux. `ptrace` est notament utilisé par les débogueurs comme `gdb`. À chaque fois qu'un processus enfant execute un appel système, le processus traceur est notifié et peut inspecter les registres du processus enfant.

Pour mieux comprendre comment fonctionn `strace`, voici un exemple simple d'un programme C qui utilise `ptrace` pour tracer l'appel système `write` notament utilisé par `printf`.

```c
#include <errno.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
   pid_t child;
   child = fork();

   if (child == 0) {  // Child (executed under trace)
      // Allow parent to trace this process
      ptrace(PTRACE_TRACEME, 0, NULL, NULL);
      raise(SIGSTOP);  // Stop child to let parent catch up
      printf("Hello from the child process!\n");

   } else {  // Parent
      int status;
      waitpid(child, &status, 0);

      ptrace(PTRACE_SYSCALL, child, NULL, NULL);

      while (1) {
         struct user_regs_struct regs;

         waitpid(child, &status, 0);
         if (WIFEXITED(status)) break;

         ptrace(PTRACE_GETREGS, child, NULL, &regs);

         if (regs.orig_rax == SYS_write) {
            printf("Intercepted write syscall!\n");
            printf("File descriptor: %lld\n", regs.rdi);
            printf("Buffer address: %lld\n", regs.rsi);
            printf("Buffer size: %lld\n", regs.rdx);
         }
         ptrace(PTRACE_SYSCALL, child, NULL, NULL);  // Let child continue
         waitpid(child, &status, 0);                 // Wait for syscall exit
         if (WIFEXITED(status)) break;               // Child exited?

         ptrace(PTRACE_SYSCALL, child, NULL, NULL);
      }
   }
}
```

La sortie de ce programme est la suivante:

```text
Intercepted write syscall!
File descriptor: 1
Buffer address: 93866916508320
Buffer size: 30
Hello from the child process!
```

Ce programme utilise deux processus légers (threads), l'enfant simule le processus tracé et le parent est le traceur. Au moment du `fork` le programme est dupliqué et s'exécute en parallèle. Pour distinguer le parent de l'enfant, on utilise la valeur de retour de `fork`. Si la valeur est `0`, c'est que le processus est l'enfant, sinon c'est le parent. Il y a donc deux chemins possibles dans le programme.

L'enfant autorise le parent à le tracer avec `PTRACE_TRACEME` et se met en pause avec `raise(SIGSTOP);`. Le parent attend que l'enfant soit en pause avec `waitpid(child, &status, 0);` et commence à tracer les appels système avec `PTRACE_SYSCALL, child`. Cette instruction demande au noyau de laisser l'enfant continuer son exécution, mais avec une interception à chaque entrée et sortie d'un appel système. Cela signifie que chaque fois que l'enfant effectue un appel système, il sera suspendu, et le parent sera notifié. Le point de sortie de la boucle while est le test de `WIFEXITED` qui vérifie si le processus enfant s'est terminé, dans ce cas, le parent sort de la boucle.
L'appel `PTRACE_GETREGS` permet au parent de lire les registres du processus enfant. Ces registres contiennent des informations cruciales comme le numéro de l'appel système dans le registre `orig_rax` pour les systèmes `x86_64`. Si l'appel système intercepté est `SYS_write`, le parent affiche les informations sur l'appel système. Enfin, le parent laisse l'enfant continuer son exécution avec `PTRACE_SYSCALL` et attend le suivant.

## ltrace

`ltrace` (pour *library trace*) est un outil de diagnostic qui permet de suivre les appels aux fonctions des bibliothèques partagées. Il est très utile pour comprendre le comportement d'un programme en cours d'exécution. `ltrace` est un outil plus simple que `strace` car il ne suit que les appels de fonctions et non les appels système. Prenons l'exemple du programme suivant :

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    char *buffer = (char *)malloc(100);
    printf("Hello, World!\n");
    free(buffer);
}
```

L'appel de `ltrace` sur ce programme donne la sortie suivante :

```text
ltrace ./a.out
malloc(100)  = 0x55af7c6d42a0
puts("Hello, World!"Hello, World!)  = 14
free(0x55af7c6d42a0) = <void>
+++ exited (status 0) +++
```

On peut voir notament que le compilateur à remplacé `printf` par `puts` car aucun format n'est utilisé.

## perf

`perf` est un outil très puissant de diagnostic qui permet de suivre les performances d'un programme en analysant les compteurs matériels du processeur.

Le processeur est un organe très complexe qui contient de nombreux compteurs matériels qui permettent de mesurer des métriques comme le nombre de cycles d'horloge, l'utilisation de la mémoire cache, le predicteur d'embranchement, les changements de contexte, etc. Ces compteurs sont très utiles pour comprendre le comportement d'un programme et identifier les goulots d'étranglement.

Les PMU (*Performance Monitoring Units*) sont des composants matériels qui permettent de mesurer ces métriques. Les PMU sont spécifiques à chaque processeur et sont généralement accessibles via des instructions spécifiques.
Ils dépendent grandement du processeur utilisé. Par exemple, un processeur Intel Core i7 de 10e génération ne dispose pas des mêmes compteurs qu'un processeur AMD Ryzen 9. L'installation de `perf` n'est donc pas triviale, surtout sur des systèmes hypervisés ou virtualisés.

Par exemple sur WSL2, l'installation de `perf` nécessite de compiler un noyau Linux avec les options de débogage activées. Sur des systèmes comme macOS, `perf` n'est pas disponible car le noyau XNU ne fournit pas les mêmes fonctionnalités que le noyau Linux.

### Utilisation

Une utilisation typique de perf est d'analyser les pertes de performances lié à la mémoire cache. Prenons l'exemple d'une matrice 1000x1000 ou chaque élément est multiplié par 2. Le programme suivant effectue cette opération:

```c
#include <stdio.h>
#include <stdlib.h>

#define SIZE 10000

int main() {
   // Allocate
   int **matrix = (int **)malloc(SIZE * sizeof(int *));
   for (int i = 0; i < SIZE; i++) matrix[i] = (int *)malloc(SIZE * sizeof(int));

   // Init
   for (int i = 0; i < SIZE; i++)
      for (int j = 0; j < SIZE; j++) matrix[i][j] = i + j;

         // Multiply
#if DIRECTION == 0
   for (int i = 0; i < SIZE; i++)
      for (int j = 0; j < SIZE; j++) matrix[i][j] *= 2;
#else
   for (int i = 0; i < SIZE; i++)
      for (int j = 0; j < SIZE; j++) matrix[j][i] *= 2;
#endif

   // Cleanup
   for (int i = 0; i < SIZE; i++) free(matrix[i]);
   free(matrix);
}
```

En compilant chaque programme avec la variable `DIRECTION` égale à `0` ou `1`, on peut observer les différences de performances. En effet, la mémoire est stockée de manière linéaire en mémoire, et en parcourant la matrice ligne par ligne ou colonne par colonne, on peut observer des différences de performances.

```bash
$ gcc -DDIRECTION=0 x.c && perf stat -e cache-misses,cycles,instructions ./a.out

       11048991      cache-misses:u
     1502929728      cycles:u
     4304906724      instructions:u

    0.384328204 seconds time elapsed

    0.314080000 seconds user
    0.070921000 seconds sys

$ gcc -DDIRECTION=1 x.c && perf stat -e cache-misses,cycles,instructions ./a.out

       23466037      cache-misses:u
     4320403836      cycles:u
     4304906756      instructions:u

    0.966821928 seconds time elapsed

    0.886317000 seconds user
    0.080574000 seconds sys
```

Dans un cas, le compteur `cache-misses` est bien plus élevé que dans l'autre. Ce la arrive lors de problèmes de localités spatiales ou temporelles. Dans le premier cas, les données sont chargées dans le cache et restent en cache, alors que dans le second cas, le cache ne peut pas être utilisé efficacement. Le programme est 3x plus lent dans le second cas, pour une simple inversion dans la boucle.

### WSL2

Malheureusement `perf` ne fonctionne pas nativement sous WSL2. WSL2 exécute Linux dans une machine virtuelle légère (Hyper-V), mais n'a pas d'accès direct aux compteurs matériels, essentiels pour perf. Cela signifie que les événements liés aux performances matérielles, tels que les cycles d'horloge du processeur, les instructions, et les caches, ne sont pas accessibles.

La première étape est d'installer les paquets nécessaires:

```bash
sudo apt install build-essential flex bison libssl-dev \
libelf-dev libpfm4-dev libtraceevent-dev asciidoc xmlto
```

On *clone* ensuite le noyau Linux de WSL2 en n'oubliant pas le `--depth=1` pour ne récupérer que le dernier *commit*.

```bash
git clone --depth=1 https://github.com/microsoft/WSL2-Linux-Kernel.git
```

L'outil `perf` est inclus dans le noyau, et l'objectif est de le compiler. Pour ce faire, on se place dans le répertoire du noyau et on copie la configuration du noyau actuel.

```bash
cd WSL2-Linux-Kernel/tools/perf
make
sudo make prefix=/usr install
```

Vous pouvez désormais utiliser `perf` pour diagnostiquer les performances de vos programmes sous WSL2. Il est possible de vérifier les événements disponibles avec `perf list`. Il se peut que sur votre système, certains événements ne soient pas disponibles.

```txt
$ perf list
  branch-instructions OR branches      [Hardware event]
  branch-misses                        [Hardware event]
  bus-cycles                           [Hardware event]
  cache-misses                         [Hardware event]
  cache-references                     [Hardware event]
  cpu-cycles OR cycles                 [Hardware event]
  instructions                         [Hardware event]
  ref-cycles                           [Hardware event]
  alignment-faults                     [Software event]
  bpf-output                           [Software event]
  cgroup-switches                      [Software event]
  context-switches OR cs               [Software event]
  cpu-clock                            [Software event]
  cpu-migrations OR migrations         [Software event]
  dummy                                [Software event]
  emulation-faults                     [Software event]
  major-faults                         [Software event]
  minor-faults                         [Software event]
  page-faults OR faults                [Software event]
  task-clock                           [Software event]
  duration_time                        [Tool event]
  user_time                            [Tool event]
  system_time                          [Tool event]
```

## valgrind

`valgrind` est un outil de diagnostic qui permet de suivre les erreurs de mémoire dans un programme. Il est très utile pour comprendre le comportement d'un programme en cours d'exécution. `valgrind` est un outil plus simple que `strace` car il ne suit que les erreurs de mémoire et non les appels système.

L'outil est disponible sur Ubuntu et dérivés avec la commande suivante:

```bash
sudo apt install valgrind
```

L'utilisation typique est de lancer un programme avec `valgrind` pour détecter les erreurs de mémoire. Par exemple, pour un programme `a.out`:

```bash
valgrind ./a.out
```

Voici une liste des fonctionnalités typiques de `valgrind`:

- **Détection des fuites de mémoire** : Valgrind permet de trouver les allocations de mémoire qui ne sont pas libérées, aidant à identifier les **fuites de mémoire** dans les programmes.

- **Détection des erreurs de mémoire** : Il détecte les **accès illégaux** à la mémoire, tels que l'accès à des zones mémoire non allouées, l'utilisation de mémoire après qu'elle a été libérée (**use-after-free**), ou encore les **buffer overflows**.

- **Détection des erreurs d'initialisation de mémoire** : Valgrind repère l'utilisation de variables non initialisées en mémoire, ce qui peut provoquer des comportements imprévisibles.

- **Profilage de la gestion de la mémoire** : Il vous montre comment la mémoire est allouée et libérée pendant l'exécution, permettant d'optimiser l'utilisation de la mémoire et de détecter les problèmes de fragmentation.

- **Débogage multithread** : Valgrind aide à détecter les **erreurs de synchronisation** dans les programmes multithread, comme les **data races** (accès concurrents non protégés à des variables partagées) ou les **verrous non libérés**.

- **Vérification des appels système incorrects** : Valgrind détecte les mauvais usages des appels système, comme la fermeture de descripteurs de fichiers qui ne sont pas ouverts.

- **Analyse des performances** : Avec l'outil **Callgrind** (inclus dans Valgrind), il permet de **profiler les programmes** en comptant les instructions exécutées et en générant des informations sur l'utilisation du CPU et des fonctions, utile pour l'optimisation des performances.

- **Simulation de cache CPU** : Avec **Cachegrind**, Valgrind peut simuler le comportement des caches CPU et montrer le nombre de cache misses (défauts de cache) pour aider à améliorer l'efficacité des programmes en matière de gestion de cache.

- **Détection des erreurs de pile** : Il vérifie l'utilisation correcte de la pile (stack), détectant les débordements et erreurs de gestion dans la pile d'appels.
