# Système d'exploitation (POSIX)

## Processus

Un processus est un programme en cours d'exécution. Il est composé d'un espace d'adressage, d'un ensemble de ressources (fichiers, sockets, etc.) et d'un ou plusieurs threads. Un processus est identifié par un PID (Process IDentifier).

### États d'un processus

## Etat du processus

Nouveau (*New*) : Un processus vient d'être créé mais n'a pas encore été admis par l'ordonnanceur du système d'exploitation pour exécution.

Prêt (*Ready*) : Le processus est chargé en mémoire et attend qu'un processeur lui soit attribué par l'ordonnanceur pour exécuter ses instructions.

Exécution (*Running*) : Le processus est en cours d'exécution sur un processeur. Dans cet état, le processus effectue les opérations pour lesquelles il a été conçu.

En attente (*Waiting* ou *Blocked*) : Le processus ne peut pas exécuter tant qu'un certain événement n'a pas lieu, comme la fin d'une opération d'entrée/sortie. Dans cet état, le processus est suspendu et attend que la condition bloquante soit levée.

Terminé (*Terminated* ou *Zombie*) : Un processus entre dans cet état une fois qu'il a fini de s'exécuter. Cependant, il reste dans la table des processus jusqu'à ce que son processus parent récupère son code de sortie, permettant au système de libérer les ressources associées. Un processus en état "zombie" a terminé son exécution mais attend que son processus parent appelle wait() pour récupérer son statut de sortie.

Orphelin (*Orphan*) : Un processus devient orphelin si son processus parent se termine avant lui. Les processus orphelins sont adoptés par le processus init (PID 1), qui récupère automatiquement leur statut de sortie, évitant ainsi la création de zombies.

Interrompu (*Stopped*) : Un processus peut être mis en pause (ou arrêté temporairement) par un signal (par exemple, SIGSTOP). Il peut être repris plus tard (par exemple, avec le signal SIGCONT).

Zombie (*Zombie*) : Comme mentionné précédemment, un processus "zombie" ou "processus défunt" est un processus qui a terminé son exécution mais reste dans la table des processus parce que son processus parent n'a pas encore récupéré son statut de sortie. Cela permet au parent de récupérer les informations sur le statut de fin de son enfant. Un processus zombie ne consomme pas de ressources à part une entrée dans la table des processus.

## Création d'un processus

Sous les systèmes d'exploitation POSIX, il existe principalement deux façons de créer un processus :

### `fork()`

La fonction `fork()` est utilisée pour créer un nouveau processus, appelé processus enfant, qui est une copie du processus appelant (processus parent). L'enfant reçoit une copie des données du parent, mais les deux processus ont des espaces d'adressage séparés. Après le `fork()`, les deux processus (parent et enfant) continuent leur exécution à partir de l'instruction suivante après l'appel `fork()`. La principale différence entre eux est la valeur de retour de `fork()`: 0 pour l'enfant et l'ID du processus enfant (PID) pour le parent, ou -1 en cas d'échec.

### `exec()`

La famille de fonctions `exec()` est utilisée pour exécuter un nouveau programme dans l'espace d'adressage d'un processus. Cela remplace l'image du processus actuel par une nouvelle image de programme. Les différentes variantes de `exec()` (comme `execl()`, `execp()`, `execv()`, etc.) permettent de spécifier le programme à exécuter et de passer des arguments de différentes manières. Habituellement, `exec()` est appelé par un processus enfant après un fork() pour remplacer son image par celle du programme à exécuter, permettant ainsi au processus parent de continuer à exécuter son code original tout en lançant un nouveau programme dans le processus enfant.
Ces deux fonctions sont souvent utilisées ensemble pour créer un nouveau processus et exécuter un nouveau programme au sein de ce processus. Le modèle "fork-exec" est un motif commun dans les systèmes POSIX pour la création de processus et l'exécution de programmes. Ce mécanisme permet une grande flexibilité dans la gestion des processus, en permettant à un processus parent de contrôler l'exécution de processus enfants et de récupérer leur statut de sortie une fois qu'ils ont terminé.

### Exemple de zombie

```cpp
#include <iostream>
#include <unistd.h> // Pour fork(), getpid(), sleep()
#include <sys/wait.h> // Pour wait()

int main() {
    pid_t pid = fork(); // Crée un nouveau processus

    if (pid == -1) {
        // En cas d'échec du fork()
        std::cerr << "Échec du fork()" << std::endl;
        return 1;
    } else if (pid > 0) {
        // Code exécuté par le processus parent
        std::cout << "Je suis le processus parent (PID: " << getpid() << "), et mon enfant a le PID " << pid << std::endl;
        std::cout << "Je dors 20 secondes. Vérifiez l'état du processus enfant avec 'ps -l'." << std::endl;
        sleep(20); // Le parent dort, laissant l'enfant devenir un zombie
        std::cout << "Le parent se réveille et se termine. Le processus enfant devrait être nettoyé." << std::endl;
    } else {
        // Code exécuté par le processus enfant
        std::cout << "Je suis le processus enfant (PID: " << getpid() << ") et je me termine." << std::endl;
        // L'enfant se termine immédiatement, devenant un zombie jusqu'à ce
        // que le parent termine son sommeil
    }
}
```

### Status des processus avec `ps`

Lorsque vous utilisez la commande `ps -l` sur un système UNIX ou Linux pour lister les processus avec des informations détaillées, vous pouvez observer différents états de processus représentés par des lettres. Voici les principaux états que vous pourriez voir :

**D**: Non interrompible (uninterruptible sleep) - Le processus est en attente d'une opération d'entrée/sortie et ne peut pas être interrompu.

**R**: Exécutable (running or runnable) - Le processus est en cours d'exécution sur un processeur ou en attente d'être exécuté.

**S** : Endormi (interruptible sleep) - Le processus attend un événement pour se poursuivre.

**T** : Arrêté (stopped) - Le processus a été arrêté, généralement par un signal de contrôle comme SIGSTOP.

**Z** : Zombie (defunct) - Le processus s'est terminé, mais des informations sont toujours conservées dans la table des processus car le processus parent n'a pas encore récupéré son statut de sortie.

**I** : Processus inactif (idle) - Utilisé pour les tâches du noyau.

**W** : Paginé - Un état obsolète non utilisé dans les versions modernes de Unix/Linux, indiquant qu'un processus était échangé (swapped out).
L'état du processus est une information clé pour comprendre ce que fait un processus à un moment donné. Les états comme "D" et "S" indiquent qu'un processus attend quelque chose pour continuer, tandis que "R" signifie que le processus est soit en cours d'exécution, soit prêt à être exécuté dès qu'un processeur est disponible. Les états "T" et "Z" sont des cas spéciaux, indiquant respectivement un processus arrêté et un processus qui s'est terminé mais dont les ressources ne sont pas encore totalement libérées par le système.

### Communication inter-processus (IPC)

Les processus dans les systèmes d'exploitation POSIX peuvent communiquer entre eux par plusieurs mécanismes de communication interprocessus (IPC - Inter-Process Communication). Ces mécanismes permettent aux processus de partager des données et de coordonner leurs actions. Voici les principaux moyens de communication interprocessus :

**Pipes (tuyaux)** : Un pipe permet à un flux de données de passer d'un processus à l'autre. Les pipes anonymes sont utilisés pour la communication entre un processus parent et son enfant ou entre enfants d'un même parent. Les pipes nommés (FIFOs) peuvent être utilisés entre n'importe quels processus sur le système.

**Signaux** : Les signaux sont des messages simples envoyés à un processus pour lui indiquer qu'un événement particulier s'est produit. Bien qu'ils ne transportent pas de grandes quantités de données, ils sont utiles pour contrôler les opérations des processus et pour la gestion d'événements asynchrones.

**Mémoire partagée** : La mémoire partagée est un segment de mémoire qui peut être accédé par plusieurs processus. C'est un moyen efficace pour échanger de grandes quantités de données entre processus, car elle évite la copie de données d'un espace d'adressage à l'autre.

**Sémaphores** : Les sémaphores sont utilisés pour synchroniser l'accès à des ressources partagées par plusieurs processus. Ils peuvent être utilisés pour éviter les conditions de course en contrôlant l'accès à des ressources telles que les fichiers ou les segments de mémoire partagée.

**Files de messages** : Les files de messages permettent aux processus d'envoyer et de recevoir des messages sous forme de files d'attente. Chaque message est une structure de données qui peut contenir des informations variées. Les files de messages sont utiles pour échanger de petites quantités de données de manière asynchrone.

**Sockets** : Les sockets permettent la communication entre processus sur le même ordinateur ou entre processus sur des ordinateurs différents dans un réseau. Ils supportent la communication en mode connecté (TCP) et non connecté (UDP) et sont la base de nombreuses communications réseau, y compris le Web.

Ces mécanismes offrent divers degrés d'abstraction et peuvent être choisis en fonction des besoins spécifiques en matière de communication interprocessus, comme la quantité de données à transférer, la nécessité de synchronisation ou la préférence entre la communication locale et la communication en réseau.

#### Exemple

```cpp
#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <signal.h>
#include <vector>

constexpr int SHM_SIZE = 1024; // Taille du segment de mémoire partagée
constexpr int NUM_CHILDREN = 10; // Nombre de processus enfants à créer

// Handler de signal pour les processus enfants
void signalHandler(int sig) {
    std::cout << "Processus " << getpid() << " lit la valeur." << std::endl;
    // Ici, vous accéderiez à la mémoire partagée pour lire la valeur
    // C'est une simplification; l'accès réel nécessiterait des pointeurs et une synchronisation
}

int main() {
    int shm_id = shmget(IPC_PRIVATE, SHM_SIZE, IPC_CREAT | 0666);
    if (shm_id < 0) {
        std::cerr << "Échec de la création de la mémoire partagée." << std::endl;
        return 1;
    }
    int* shared_memory = (int*)shmat(shm_id, nullptr, 0);
    *shared_memory = 0; // Initialisation de la mémoire partagée

    signal(SIGUSR1, signalHandler); // Configuration du handler de signal pour tous les processus

    std::vector<pid_t> children;

    // Création de 10 processus enfants
    for (int i = 0; i < NUM_CHILDREN; ++i) {
        pid_t pid = fork();
        if (pid == 0) { // Enfant
            // Boucle infinie pour que l'enfant reste actif
            while (true) pause(); // Attend le signal
            exit(0);
        } else if (pid > 0) { // Parent
            children.push_back(pid);
        } else {
            std::cerr << "Échec du fork()." << std::endl;
            return 1;
        }
    }

    // Code du processus parent pour modifier la mémoire partagée et envoyer des signaux
    while (true) {
        int val;
        std::cout << "Entrez une valeur à écrire dans la mémoire partagée: ";
        std::cin >> val;
        *shared_memory = val; // Écrit dans la mémoire partagée
        for (pid_t child : children) {
            kill(child, SIGUSR1); // Envoie un signal à chaque enfant
        }
    }

    // Nettoyage (pas atteint dans cet exemple simplifié)
    for (pid_t child : children) {
        int status;
        waitpid(child, &status, 0);
    }
    shmdt(shared_memory);
    shmctl(shm_id, IPC_RMID, nullptr);
}
```

Avec `htop`, vous pouvez observer les processus enfants en attente de signal. Utilisez la fonction `t` pour afficher le mode arbre. Vous pouvez également observer la mémoire partagée avec `ipcs -m`.

Dans cet exemple, un segment de mémoire partagée est créé pour stocker une valeur entière. Le processus parent écrit une valeur dans la mémoire partagée et envoie un signal à chaque processus enfant. Chaque processus enfant est configuré pour exécuter un gestionnaire de signal qui lit la valeur de la mémoire partagée. Cela permet de communiquer des données entre le processus parent et les processus enfants de manière asynchrone.

Néanmoins il faut d'avantage pour gérer la synchronisation et la communication entre les processus. Les exemples ci-dessus sont des simplifications pour illustrer les concepts de base.

#### Synchronisation de la mémoire partagée

Dans cet exemple, on se contente d'informer l'utilisateur qu'une valeur a été déposée dans la mémoire partagée mais on ne peut pas la lire directement. On a besoin d'un mécanisme de synchronisation.

```cpp
#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <signal.h>
#include <vector>
#include <semaphore.h>

constexpr int SHM_SIZE = sizeof(int); // Taille du segment de mémoire partagée pour stocker un entier
constexpr int NUM_CHILDREN = 10; // Nombre de processus enfants à créer

int* shared_memory; // Pointeur vers la mémoire partagée
sem_t* sem; // Pointeur vers le sémaphore

void signalHandler(int sig) {
    sem_wait(sem); // Attendre pour accéder à la section critique
    std::cout << "Processus " << getpid() << " lit la valeur " << *shared_memory << "." << std::endl;
    sem_post(sem); // Libérer l'accès à la section critique
}

int main() {
    // Création de la mémoire partagée
    int shm_id = shmget(IPC_PRIVATE, SHM_SIZE, IPC_CREAT | 0666);
    if (shm_id < 0) {
        std::cerr << "Échec de la création de la mémoire partagée." << std::endl;
        return 1;
    }
    shared_memory = (int*)shmat(shm_id, nullptr, 0);

    // Initialisation du sémaphore dans la mémoire partagée
    sem = new sem_t;
    if (sem_init(sem, 1, 1) == -1) { // 1 pour partage entre processus
        std::cerr << "Erreur d'initialisation du sémaphore." << std::endl;
        return 1;
    }

    signal(SIGUSR1, signalHandler); // Configuration du gestionnaire de signal

    std::vector<pid_t> children;

    // Création des processus enfants
    for (int i = 0; i < NUM_CHILDREN; ++i) {
        pid_t pid = fork();
        if (pid == 0) { // Enfant
            while (true) pause(); // Attend le signal
            exit(0);
        } else if (pid > 0) { // Parent
            children.push_back(pid);
        } else {
            std::cerr << "Échec du fork()." << std::endl;
            return 1;
        }
    }

    // Code du processus parent pour lire et mettre à jour la mémoire partagée
    while (true) {
        int val;
        std::cout << "Entrez une valeur à écrire dans la mémoire partagée: ";
        std::cin >> val;
        sem_wait(sem); // Accéder à la section critique
        *shared_memory = val; // Écrire dans la mémoire partagée
        sem_post(sem); // Libérer l'accès
        for (pid_t child : children) {
            kill(child, SIGUSR1); // Signaler aux enfants de lire la valeur
        }
    }

    // Nettoyage (non atteint dans cet exemple)
    for (pid_t child : children) {
        int status;
        waitpid(child, &status, 0);
    }
    shmdt(shared_memory);
    shmctl(shm_id, IPC_RMID, nullptr);
    sem_destroy(sem);
    delete sem;
}
```

## Processus léger versus processus (clone/fork)

Sous Linux, l'appel système utilisé pour créer des threads est `clone()` ou, dans certains cas, des variantes comme `fork()` ou `vfork()`. Cependant, `clone()` est plus flexible et permet une plus grande personnalisation du partage d'espace d'adressage, des fichiers, des signaux, etc., ce qui le rend particulièrement adapté pour la création de threads.

`clone()` : Cet appel système est utilisé pour créer un processus léger (un thread, dans ce contexte). Contrairement à `fork()`, qui duplique le processus appelant dans un nouveau processus avec un espace d'adressage séparé, `clone()` permet de spécifier exactement quels éléments (espace d'adressage, table des fichiers ouverts, espace des signaux, etc.) doivent être partagés entre le thread appelant et le nouveau thread. Cela permet une création de thread plus efficace et un partage de ressources entre les threads.

### Processus

Un processus est une instance d'un programme en cours d'exécution. Chaque processus possède son propre espace d'adressage virtuel, ses propres ressources (comme des descripteurs de fichiers) et son propre contexte d'exécution (registres, pile, etc.). Les processus sont isolés les uns des autres, ce qui signifie que sans mécanismes de communication inter-processus (IPC), ils ne peuvent pas directement partager de données. L'isolation entre les processus assure la sécurité et la stabilité du système, car l'erreur dans un processus ne peut pas corrompre directement l'espace mémoire d'un autre processus.

### Thread (Processus léger)

Un thread, souvent appelé un processus léger, est une unité d'exécution qui peut être créée au sein d'un processus. Contrairement aux processus, les threads d'un même processus partagent le même espace d'adressage et peuvent accéder aux mêmes données en mémoire. Cela facilite le partage d'informations et la communication entre les threads, mais requiert également une synchronisation soignée pour éviter les conditions de course et les incohérences de données. Les threads ont leur propre pile d'exécution et leur propre contexte de registres, mais partagent d'autres ressources avec les threads du même processus, comme les descripteurs de fichiers et les segments de mémoire alloués.

### Différences clés

Isolation : Les processus sont isolés les uns des autres, tandis que les threads partagent l'espace d'adressage du processus qui les a créés.
Création et terminaison : Créer un nouveau processus est généralement plus coûteux en termes de ressources et de temps que créer un thread. De même, terminer un processus et nettoyer ses ressources est plus lourd que terminer un thread.

Communication : La communication entre processus nécessite l'utilisation de mécanismes IPC, tels que les files de messages, les tubes (pipes), la mémoire partagée, etc. En revanche, les threads peuvent communiquer directement en lisant et écrivant dans la mémoire partagée du processus, bien que cela nécessite une synchronisation, comme l'utilisation de verrous ou de sémaphores.
Utilisation : Les processus sont utiles pour exécuter des tâches isolées et sécurisées, sans risque d'interférence directe entre elles. Les threads sont préférés pour les tâches qui nécessitent un partage intensif de données ou une communication rapide entre les unités d'exécution au sein d'une même application.

En résumé, bien que les threads (ou processus légers) et les processus servent tous deux à exécuter des tâches de manière concurrente, ils diffèrent par leur niveau d'isolation, leurs coûts de création et de gestion, ainsi que par leur manière de communiquer et de partager des données.

## Appel système `clone()`

```cpp
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

// Taille de la pile allouée pour le thread créé par clone
#define STACK_SIZE (1024 * 1024)

// La fonction à exécuter dans le thread
int threadFunction(void *arg) {
    printf("Bonjour du thread!\n");
    return 0;
}

int main() {
    // Alloue de l'espace pour la pile du thread
    char *stack = (char *)malloc(STACK_SIZE);
    if (stack == NULL) {
        perror("malloc");
        exit(1);
    }

    // Prépare le sommet de la pile pour le nouveau thread (clone grandit vers le bas)
    char *stackTop = stack + STACK_SIZE;

    // Crée le thread. Les flags déterminent quels éléments sont partagés.
    // CLONE_VM partage l'espace d'adressage, et SIGCHLD est utilisé pour que waitpid() puisse être utilisé.
    pid_t pid = clone(threadFunction, stackTop, CLONE_VM | SIGCHLD, NULL);

    if (pid == -1) {
        perror("clone");
        exit(1);
    }

    // Attend que le thread (processus) créé se termine
    if (waitpid(pid, NULL, 0) == -1) {
        perror("waitpid");
        exit(1);
    }

    // Nettoie
    free(stack);

    printf("Thread terminé\n");
}
```

## Signaux

Sous les systèmes d'exploitation POSIX, les signaux sont des messages logiciels envoyés à un processus pour lui indiquer qu'un événement particulier s'est produit. Les signaux sont utilisés pour gérer les interruptions, les erreurs et les événements asynchrones, et peuvent être envoyés par le noyau, par d'autres processus ou par le processus lui-même.

Voici les signaux POSIX standard et leurs descriptions :

| Signal        | Description                                         |
| ------------- | --------------------------------------------------- |
| SIGHUP(1)     | Terminaison du terminal ou du processus contrôlant  |
| SIGINT(2)     | Interruption depuis le clavier                      |
| SIGQUIT(3)    | Interruption depuis le clavier avec un core dump    |
| SIGILL(4)     | Instruction illégale                                |
| SIGTRAP(5)    | Trace ou point d'arrêt                              |
| SIGABRT(6)    | Signal d'abandon                                    |
| SIGBUS(7)     | Erreur de bus                                       |
| SIGFPE(8)     | Erreur arithmétique                                 |
| SIGKILL(9)    | Terminaison forcée                                  |
| SIGUSR1(10)   | Signal utilisateur 1                                |
| SIGSEGV(11)   | Violation de la segmentation                        |
| SIGUSR2(12)   | Signal utilisateur 2                                |
| SIGPIPE(13)   | Écriture sur un tube sans lecteur                   |
| SIGALRM(14)   | Alarme horloge                                      |
| SIGTERM(15)   | Terminaison                                         |
| SIGSTKFLT(16) | Erreur de pile                                      |
| SIGCHLD(17)   | Enfant terminé ou arrêté                            |
| SIGCONT(18)   | Continuer l'exécution, si arrêté                    |
| SIGSTOP(19)   | Arrêt de l'exécution du processus                   |
| SIGTSTP(20)   | Arrêt de l'exécution du processus depuis le clavier |
| SIGTTIN(21)   | Lecture depuis le terminal en arrière-plan          |
| SIGTTOU(22)   | Écriture sur le terminal en arrière-plan            |
| SIGURG(23)    | Données urgentes sur le socket                      |
| SIGXCPU(24)   | Temps CPU écoulé                                    |
| SIGXFSZ(25)   | Taille de fichier maximale dépassée                 |
| SIGVTALRM(26) | Alarme virtuelle                                    |
| SIGPROF(27)   | Profilage du signal                                 |
| SIGWINCH(28)  | Changement de taille de fenêtre                     |
| SIGIO(29)     | Événement d'entrée/sortie asynchrone                |
| SIGPWR(30)    | Événement d'alimentation                            |
| SIGSYS(31)    | Erreur système                                      |

Les signaux les plus couramment utilisés sont `SIGINT` (interruption depuis le clavier), `SIGTERM` (terminaison) et `SIGKILL` (terminaison forcée). Ces signaux sont souvent utilisés pour demander à un processus de se terminer ou de réagir à des événements utilisateur.

## Information sur un processus

### `pstree`

Pour afficher l'arborescence des processus, vous pouvez utiliser la commande pstree. Par exemple, pour afficher l'arborescence des processus pour l'utilisateur actuel, vous pouvez exécuter :

Exercice :

Essayez de lancer un programme en arrière-plan (par exemple, ./myprogram &) et utilisez pstree pour voir comment il est lié à d'autres processus.

```bash
$ pstree
```

### `proc`

Exécutez le programme suivant:

```cpp
// Read string and print it
#include <iostream>

int main()
{
    std::string s;
    std::cin >> s;
    std::cout << s << std::endl;
    return 0;
}
```

```bash
$ g++ -o read read.cpp
$ ./read &
[1] 12345
$ cat /proc/12345/status
$ cat /proc/12345/maps
$ cat /proc/12345/smaps
```

## Appels système utiles

| Appel système         | Description                                                                          |
| --------------------- | ------------------------------------------------------------------------------------ |
| `fork()`              | Crée un nouveau processus en dupliquant le processus appelant.                       |
| `exec()`              | Exécute un nouveau programme dans le contexte du processus appelant.                 |
| `wait()`              | Attend la terminaison d'un processus enfant.                                         |
| `waitpid()`           | Attend la terminaison d'un processus enfant spécifique.                              |
| `clone()`             | Crée un nouveau processus léger (thread) avec des options de partage personnalisées. |
| `kill()`              | Envoie un signal à un processus.                                                     |
| `signal()`            | Configure un gestionnaire de signal pour un signal donné.                            |
| `pipe()`              | Crée un tube (pipe) pour la communication entre processus.                           |
| `shmget()`            | Alloue un segment de mémoire partagée.                                               |
| `shmat()`             | Attache un segment de mémoire partagée à l'espace d'adressage d'un processus.        |
| `sem_init()`          | Initialise un sémaphore pour la synchronisation entre processus.                     |
| `mmap()`              | Mappe un fichier ou un périphérique dans l'espace d'adressage d'un processus.        |
| `mprotect()`          | Modifie les protections d'accès pour une région de mémoire.                          |
| `munmap()`            | Supprime un mappage de mémoire.                                                      |
| `nice()`              | Modifie la priorité de planification d'un processus.                                 |
| `sched_setaffinity()` | Modifie l'affinité du processeur pour un processus.                                  |
| `getpriority()`       | Obtient la priorité de planification d'un processus.                                 |
| `setpriority()`       | Modifie la priorité de planification d'un processus.                                 |