## Mémoire partagée

Nous le verrons plus loin au chapitre sur la MMU, mais la mémoire d'un processus mémoire (programme) ne peut pas être accédée par un autre programme. Le système d'exploitation l'en empêche.

Lorsque l'on souhaite communiquer entre plusieurs programmes, il est possible d'utiliser différentes méthodes :

- les flux (fichiers, stdin, stdout...)
- la mémoire partagée
- les sockets

Vous avez déjà vu les flux au chapitre précédent, et les sockets ne font pas partie de ce cours d'introduction.

Notons que la mémoire partagée est un mécanisme propre à chaque système d'exploitation. Sous POSIX elle est normalisée et donc un programme compatible POSIX et utilisant la mémoire partagée pourra fonctionner sous Linux, WSL ou macOS, mais pas sous Windows.

C'est principalement l'appel système `mmap` qui est utilisé. Il permet de mapper ou démapper des fichiers ou des périphériques dans la mémoire.

```c
void *mmap(
    void *addr,
    size_t length, // Size in bytes
    int prot,      // Access protection (read/write/execute)
    int flags,     // Attributs (shared/private/anonymous...)
    int fd,
    int offset
);
```

Voici un exemple permettant de réserver un espace partagé en écriture et en lecture entre deux processus :

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

void* create_shared_memory(size_t size) {
    // Accessible en lecture et écriture
    int protection = PROT_READ | PROT_WRITE;

    // D'autres processus peuvent accéder à cet espace
    // lequel est anonyme
    // so only this process and its children will be able to use it:
    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    // The remaining parameters to `mmap()` are not important for this use case,
    // but the manpage for `mmap` explains their purpose.
    return mmap(NULL, size, protection, visibility, -1, 0);
}
```

### File memory mapping

Traditionnellement lorsque l'on souhaite travailler sur un fichier, il convient de l'ouvrir avec `fopen` et de lire son contenu. Lorsque cela est nécessaire, ce fichier est copié en mémoire :

```c
FILE *fp = fopen("foo", "r");
fseek(fp, 0, SEEK_END);
int filesize = ftell(fp);
fseek(fp, 0, SEEK_SET);
char *file = malloc(filesize);
fread(file, filesize, sizeof(char), fp);
fclose(fp);
```

Cette copie n'est pas nécessairement nécessaire. Une approche **POSIX**, qui n'est donc pas couverte par le standard **C99** consiste à lier le fichier dans un espace mémoire partagé.

Ceci nécessite l'utilisation de fonctions bas niveau.

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

int main() {
    int fd = open("foo.txt", O_RDWR, 0600);
    char *addr = mmap(NULL, 100, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    printf("Espace mappé à %p\n", addr);
    printf("Premiers caractères du fichiers : %.*s...\n", 20, addr);
}
```

Les avantages de cette méthode sont :

- pas nécessaire de copier l'intégralité du fichier en mémoire ;
- possibilité de partager le même fichier ouvert entre plusieurs processus ;
- possibilité laissée au système d'exploitation d'utiliser la RAM ou non si les ressources mémoires deviennent tendues.
