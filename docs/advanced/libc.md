# Bibliothèque standard C

La bibliothèque standard C est une bibliothèque de fonctions qui fournit des fonctionnalités de base pour la programmation en C. Elle est définie par la norme ISO C et est donc disponible sur tous les systèmes qui respectent cette norme.

Elle est sert d'intermédiaire entre le standard C (respect des en-têtes) et le système d'exploitation POSIX (appels systèmes).

## Liée dynamiquement par défaut

Prenons l'exemple d'un simple *Hello, World!* :

```c
#include <stdio.h>

int main() { printf("hello, world\n"); }
```

Habituellement, pour compiler ce programme, on utilise la commande `gcc` :

```bash
gcc hello.c
```

Si on exécute le programme en écoutant les appels systèmes avec `strace ./a.out`, on peut voir que le programme ouvre quelques fichiers :

```bash
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3"..., 832) = 832
...
```

Le programme `a.out` dépend de la bibliothèque `libc.so.6` qui est chargée dynamiquement. Cela permet de réduire la taille des programmes au détriments de la portabilité et d'un temps de chargement un peu plus long mais c'est un compromis jugé très acceptable.

Alternativement, on peut très facilement lier statiquement la bibliothèque standard C en utilisant l'option `-static` :

```bash
gcc -static hello.c
```

Enfin, rien ne nous oblige d'utiliser `libc`. La distribution Alpine par exemple utilise `musl` à la place de `glibc` pour des raisons de taille et de sécurité. Musl est très populaire dans le monde de l'embarqué. Essayons de compiler notre programme avec `musl` :

```bash
sudo apt install musl-tools
musl-gcc -static hello.c
```

Comparons la taille des exécutables :

| Mode de compilation | Bibliothèque | Taille |
| ------------------- | ------------ | ------ |
| Dynamique           | glibc        | 16K    |
| Dynamique           | musl         | 18K    |
| Statique            | glibc        | 767k   |
| Statique            | musl         | 33k    |
