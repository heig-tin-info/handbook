# Meson

## Qu'est-ce que Meson ?

[Meson](https://fr.wikipedia.org/wiki/Meson_(logiciel)) est un système de *build* open-source conçu pour être **simple**, **rapide**, et **multiplateforme**. Il est utilisé principalement pour gérer des projets en C, C++, mais il supporte également d'autres langages comme Python, Java, Rust, et plus encore. Meson a été créé avec un objectif clair : accélérer le processus de compilation, tout en simplifiant la gestion des projets et en réduisant les problèmes liés à la configuration.

Il génère des fichiers de build pour différents systèmes de build, comme [Ninja](https://fr.wikipedia.org/wiki/Ninja_(logiciel)) (qui est le plus couramment utilisé avec Meson pour sa vitesse). Contrairement à des outils comme [CMake](https://fr.wikipedia.org/wiki/CMake) ou [Autotools](https://fr.wikipedia.org/wiki/Autotools), Meson offre une syntaxe de configuration plus simple et plus lisible, et il gère mieux les projets complexes grâce à sa gestion automatique des dépendances.

## Histoire et motivation derrière Meson

Meson a été créé par Jussi Pakkanen en 2012, avec pour objectif de répondre à plusieurs limitations des outils de build traditionnels comme Make, Autotools ou même CMake. Il visait à résoudre des problèmes de complexité excessive, de vitesse de compilation, et à offrir une meilleure expérience utilisateur avec :

1. **Une syntaxe plus claire et concise** pour les fichiers de configuration.
2. **Une meilleure intégration avec Ninja** pour des builds plus rapides.
3. **Un support amélioré pour la compilation incrémentale**.
4. Une **portabilité facile** entre Linux, Windows, et macOS.
5. **Une gestion simplifiée des dépendances** et des sous-projets.

Meson a été rapidement adopté par de grands projets open-source, tels que **GNOME**, **X.org**, **GStreamer**, ou encore **systemd**, en raison de sa simplicité et de ses performances.

## Principe de fonctionnement

Meson fonctionne en deux étapes principales :

1. **Configuration** : Meson configure le projet, génère un ensemble de fichiers de build pour Ninja (ou d'autres systèmes), et vérifie les dépendances et les paramètres du compilateur.
2. **Build** : Ninja (ou un autre backend) est ensuite utilisé pour compiler et lier les fichiers sources.

Voici quelques caractéristiques clés :

- **Syntaxe simple** : Les fichiers `meson.build` sont simples à écrire et à comprendre.
- **Multiplateforme** : Supporte les systèmes Linux, macOS, Windows, etc.
- **Optimisation du parallélisme** : Utilise Ninja pour tirer parti des systèmes multi-cœurs.
- **Configuration rapide** : Par rapport à des outils comme CMake ou Autotools, Meson est conçu pour des configurations plus rapides.
- **Test et Benchmark** : Meson intègre directement des outils pour les tests unitaires et les benchmarks.

## Installation

Meson est écrit en Python, donc son installation est simple avec `pip` :

```bash
pip install meson
```

Ou sur certaines distributions Linux comme Ubuntu :

```bash
sudo apt-get install meson
```

Sur macOS avec Homebrew :

```bash
brew install meson
```

## Utilisation

Meson utilise des fichiers appelés `meson.build` pour définir la configuration de build. Prenons l'exemple d'un projet typique ayant la structure suivante :

```
project/
  src/
    main.c
    util.c
    util.h
  meson.build
  meson_options.txt
```

### Exemple

Le fichier `meson.build` utilise la syntaxe Meson basée sur Python pour configurer le projet. Voici un exemple simple :

```python
project('super-rocket', 'c',
  version: '1.0',
  default_options: ['warning_level=3', 'c_std=gnu11'])

executable('super-rocket',
  sources: ['src/main.c', 'src/server.c'],
  dependencies: [dependency('libuv')]
)
```

!!! note "Frustrations"

    Les développeurs de meson ont fait quelques choix que vous pourriez trouver frustrants. Par exemple, les fichiers de configuration sont écrits en Python, mais ils ne sont pas des scripts Python valides. Cela signifie que vous ne pouvez pas utiliser de variables, de boucles ou de conditions Python dans les fichiers de configuration.

    Les paramètres de configuration sont des chaînes de caractères dont aucune aide possible n'est fournie par l'IDE. Cela peut rendre la configuration plus difficile pour les nouveaux utilisateurs.

    La liste des fichiers source doit être écrite manuellement, ce qui peut être fastidieux pour les projets de grande taille. Il n'y a pas de moyen d'utiliser des expressions régulières ou un *glob* (comme `*.c`) pour inclure automatiquement tous les fichiers source. C'est un choix délibéré pour éviter les problèmes de répétabilité, mais cela peut être un inconvénient pour certains projets.

Ce fichier fait plusieurs choses: il définit le nom du projet (`my_program`) et le langage utilisé (`C`), ainsi que quelques options par défaut, il spécifie que l'exécutable `my_program` sera construit à partir des fichiers `main.c` et `server.c` enfin, il spécifie que le programme dépend de la bibliothèque **libuv**, en utilisant `dependency('libuv')` pour lier automatiquement cette bibliothèque au projet.

Nous prendrons pour l'exemple les fichiers suivants :

- Le fichier `main.c` est le point d'entrée du programme.

    ```c
    #include <stdio.h>
    #include "server.h"

    int main() { start_server(); }
    ```

- Le fichier `server.h` déclare la fonction `start_server`.

    ```c
    #pragma once
    void start_server();
    ```

-  Le fichier `server.c` implémente la logique du serveur, en utilisant **libuv** pour créer un serveur TCP.

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <uv.h> // Requires -std=gnu11
    #include "server.h"

    static void on_new_connection(uv_stream_t *server, int status) {
        if (status < 0) {
            fprintf(stderr, "New connection error %s\n", uv_strerror(status));
            return;
        }
        uv_tcp_t *client = (uv_tcp_t*) malloc(sizeof(uv_tcp_t));
        uv_tcp_init(uv_default_loop(), client);
        if (uv_accept(server, (uv_stream_t*) client) == 0)
            printf("Accepted new connection\n");
        else
            uv_close((uv_handle_t*) client, NULL);
    }

    void start_server() {
        uv_tcp_t server;
        uv_tcp_init(uv_default_loop(), &server);
        struct sockaddr_in addr;
        uv_ip4_addr("0.0.0.0", 7000, &addr);
        uv_tcp_bind(&server, (const struct sockaddr*)&addr, 0);
        int r = uv_listen((uv_stream_t*) &server, 128, on_new_connection);
        if (r) {
            fprintf(stderr, "Listen error %s\n", uv_strerror(r));
            return;
        }
        printf("Listening on port 7000\n");
        uv_run(uv_default_loop(), UV_RUN_DEFAULT);
    }
    ```

Si aucun `meson.build` n'existe, vous pouvez en créer un en utilisant la commande `meson init` :

```bash
meson init
```

Pour compiler ce projet on appelle la commande `meson` avec l'option `setup` pour configurer le projet, puis `compile` pour compiler les fichiers sources :

```bash
$ meson setup builddir
The Meson build system
Version: 1.3.2
Source dir: /home/ycr/meson-test
Build dir: /home/ycr/meson-test/builddir
Build type: native build
Project name: super-rocket
Project version: 1.0
C compiler for the host machine: cc (gcc 13.2.0
    "cc (Ubuntu 13.2.0-23ubuntu4) 13.2.0")
C linker for the host machine: cc ld.bfd 2.42
Host machine cpu family: x86_64
Host machine cpu: x86_64
Found pkg-config: YES (/usr/bin/pkg-config) 1.8.1
Run-time dependency libuv found: YES 1.48.0
Run-time dependency threads found: YES
Build targets in project: 1

Found ninja-1.11.1 at /usr/bin/ninja
```

Cette commande configure le projet dans un répertoire de build (`builddir`) et génère les fichiers nécessaires pour Ninja qui est le backend par défaut de Meson. Ensuite, on peut compiler le projet avec :

```bash
$ meson compile -C builddir
INFO: autodetecting backend as ninja
INFO: calculating backend command to run: /usr/bin/ninja
    -C /home/ycr/meson-test/builddir
ninja: Entering directory `/home/ycr/meson-test/builddir'
[3/3] Linking target super-rocket
```

De la même manière que CMake, meson utilise un répertoire de build séparé pour isoler les fichiers générés du code source. Cela permet de nettoyer facilement les fichiers de build en supprimant simplement le répertoire de build, mais cela demande une étape supplémentaire lors du build.

Une fois compilé, le programme peut être exécuté:

```bash
./builddir/super-rocket
```

Cela démarre le serveur, et il écoutera les connexions TCP sur le port 7000.

!!! tip "Extension vscode"

    Une extension **Meson** existe pour Visual Studio Code, qui fournit une coloration syntaxique pour les fichiers `meson.build` et des fonctionnalités de complétion automatique pour les options Meson.

## Cheatsheet

Voici une liste de commandes Meson couramment utilisées :

| Commande Meson                   | Description                                                 |
| -------------------------------- | ----------------------------------------------------------- |
| `meson setup builddir`           | Configure le projet dans le répertoire de build `builddir`. |
| `meson compile -C builddir`      | Compile le projet dans le répertoire de build `builddir`.   |
| `meson test -C builddir`         | Exécute les tests unitaires du projet.                      |
| `meson install -C builddir`      | Installe les fichiers du projet sur le système.             |
| `meson configure -Doption=value` | Configure le projet avec une option spécifique.             |
| `meson introspect`               | Affiche des informations sur le projet.                     |
