# Make

## Introduction

`make` est un outil de gestion de projet qui permet de compiler des programmes C/C++ de manière efficace. `make` utilise un fichier `Makefile` qui contient les règles de compilation.

Le langage Make est très ancien (1976) et n'est pas très lisible aux yeux des débutants. Cependant, il est très puissant et permet de gérer des projets de grande envergure. Voici un exemple de `Makefile` générique pour compiler un programme en C :

```make
CC=gcc
CFLAGS=-std=c17 -O3 -Wall -Werror -pedantic
LDFLAGS=-lm
EXEC=main
SRCS=$(wildcard *.c)
OBJS=$(SRCS:.c=.o)

all: $(EXEC)

-include $(OBJS:.o=.d)

$(EXEC): $(OBJS)
    $(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
    $(CC) -o $@ -c $< $(CFLAGS) -MMD -MP

clean:
    $(RM) -f $(OBJS) $(EXEC) $(OBJS:.o=.d)

.PHONY: all clean
```

Make utilise des variables spéciales et l'appel de macros. Les variables sont définies avec `VAR=valeur` et appelées avec `$(VAR)`.

Table: Variables Make

| Variable            | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| `CC`                | Compilateur (convention)                                   |
| `CFLAGS`            | Options de compilation (convention)                        |
| `LDFLAGS`           | Options d'édition de liens (convention)                    |
| `EXEC`              | Nom du fichier exécutable (convention)                     |
| `SRCS`              | Liste des fichiers sources                                 |
| `OBJS`              | Liste des fichiers objets                                  |
| `$@`                | Nom de la cible                                            |
| `$^`                | Liste des dépendances                                      |
| `$<`                | Première dépendance                                        |
| `%.o`               | Jalon générique pour tous les fichiers en `.o`             |
| `$(wildcard *.foo)` | Liste des fichiers `.foo` dans le répertoire courant       |
| `$(RM)`             | Commande de suppression de fichiers sur le système courant |

Le fonctionnement de Make est en soi assez simple. Des règles sont définies avec `cible: dépendances` et les commandes à exécuter pour générer la cible.

Dans l'exemple ci-dessus, la règle `all` dépend de `$(EXEC)`, autrement dit le fichier `main`. Pour générer `main`, Make recherche une autre règle du même nom. Il trouve `main: $(OBJS)` qui dépend de tous les fichiers objets. Pour générer un fichier objet, Make recherche une autre règle permettant de générer les fichiers objets nécessaires. Il trouve `%.o: %.c` qui dépend de tous les fichiers sources. Une fois les fichiers objets générés, Make peut générer l'exécutable `main`.

Make fonctionne de manière incrémentale. Si un fichier source est modifié, Make ne recompile que les fichiers objets nécessaires. Cela permet de gagner du temps lors du développement. Il se base sur les dates de modification des fichiers pour déterminer si un fichier doit être recompilé ou non.

Ce mode de fonctionnement peut créer des problèmes avec les fichiers d'en-tête. En effet, si un fichier d'en-tête est modifié, Make ne recompile pas les fichiers sources qui incluent ce fichier d'en-tête puisque les fichiers d'en-tête n'apparaissent dans aucune règles. Pour résoudre ce problème, il est possible de générer des fichiers de dépendances avec l'option `-MMD -MP` du compilateur GCC. Ces fichiers de dépendances sont inclus dans le `Makefile` avec l'option `!include $(OBJS:.o=.d)`. Ils contiennent la liste des fichiers d'en-tête inclus par chaque fichier source qui indique par exemple que l'objet `main.o` dépend du fichier `add.h`. Ainsi, si `add.h` est modifié, Make recompile `main.o` et regénère l'exécutable `main`.

## Utilisation

Pour utiliser Make, il suffit de créer un fichier `Makefile` dans le répertoire du projet. Ensuite, il suffit de taper la commande `make` dans un terminal pour compiler le projet. Pour nettoyer les fichiers temporaires, il suffit de taper la commande `make clean`.

Voici l'exemple de création d'un programme en C avec deux fichiers C et un fichier d'en-tête :

=== "main.c"

    ```c
    #include "add.h"
    #include <stdio.h>

    int main() {
        const int a = 2, b = 3;
        printf("Somme de %d+%d = %d\n", a, b, add(a, b));
    }
    ```

=== "add.h"

    ```c
    #pragma once
    int add(int a, int b);
    ```

=== "add.c"

    ```c
    int add(int a, int b) {
        return a + b;
    }
    ```

Votre `Makefile` devrait ressembler à ceci :

```make
CC=gcc
CFLAGS=-std=c17 -O3 -Wall -Werror -pedantic
LDFLAGS=-lm # Si vous utilisez la librairie mathématique
EXEC=main

all: $(EXEC)

$(EXEC): main.o add.o
    $(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c | add.h
    $(CC) -o $@ -c $< $(CFLAGS)

clean:
    $(RM) -f *.o $(EXEC)
```
