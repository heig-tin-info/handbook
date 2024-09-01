# Mémoire cache

Chaque processeur possède une [mémoire cache](https://en.wikipedia.org/wiki/Cache_(computing)) qui permet de stocker des données et des instructions pour les rendre plus rapidement accessibles. La mémoire cache est plus rapide que la mémoire principale (RAM) mais elle est aussi plus petite. Il existe plusieurs niveaux de cache (L1, L2, L3) qui sont de plus en plus grands et de plus en plus lents. Le dernier rampart avant la RAM est aussi appelé le cache de dernier niveau (LLC).

Le principal problème des ordinateurs modernes est que l'accès à la mémoire RAM est extrêmement lent (50 à 200 cycles) par rapport à la vitesse du processeur. Il y a plusieurs raison à cela, la première est que la mémoire RAM est souvent déportée du processeur (sur une carte mère) et que la vitesse de la lumière est limitée : avec une distance de 20 cm (40 cm allé retour) il faut 1.33 nanosecond soit déjà entre 5 et 10 cycles processeur. La seconde raison est que la mémoire RAM est composée de condensateurs qui se déchargent et qui doivent être rechargés à chaque lecture, on appelle cela le rafraichissement: toutes les 7.8us un ordinateur à un hoquet et les accès RAM sont ralentis. Ces deux raisons ajouté à tous les circuits logiques qui doivent être configurés pour acheminer l'information d'un point à l'autre font que l'accès à la mémoire RAM est très lente.

Pour palier à ce problème la notion de mémoire cache a été introduite. Le premier processeur doté d'une mémoire cache est le Motorola 68000 en 1979.

Un ennui majeur est que plus une mémoire est rapide plus elle est volumineuse et plus elle est volumineuse plus elle est chère. Une solution à ce problème est d'utiliser plusieurs niveaux de cache. Le cache est très rapide mais aussi très volumineux en surface de silicium, il est donc très cher. Il représente environ 20% de la surface d'un processeur.

## Organisation de la mémoire cache

La mémoire cache est organisée en lignes de cache. Chaque ligne de cache identifiée par un index contient un bloc de données et un tag. Le tag est un identifiant unique pour chaque bloc de données. Lorsqu'un processeur veut accéder à une donnée, il va d'abord chercher le tag dans le cache, si le tag est trouvé alors le processeur a trouvé la donnée et il peut l'utiliser. Si le tag n'est pas trouvé alors le processeur doit aller chercher la donnée dans la mémoire RAM, ou dans un autre cache.

Typiquement un cache L1 sur un processeur x86 contient 32 Ko de données et 32 Ko d'instructions. Une ligne de cache contient généralement 64 octets.

Lorsqu'une donnée est chargée en mémoire, par exemple l'accès à un élément d'un tableau, le processeur profite de la localité spatiale pour charger en mémoire les données voisines. La localité spatiale est le fait que les données voisines d'une donnée sont souvent utilisées en même temps. Parallèlement, on appelle  localité temporelle le fait que les données sont souvent réutilisées plusieurs fois.

Prenons l'exemple d'un tableau de 128 éléments de 4 bytes (int). Si j'accède à l'élément 0, le processeur va automatiquement charger en mémoire les éléments 0 à 15 dans le cache. Si j'accède à l'élément 16, le processeur doit aller chercher les éléments 16 à 31 dans la mémoire RAM. Si j'accède à l'élément 0 une seconde fois, le processeur n'a pas besoin d'aller chercher les données dans la mémoire RAM car elles sont déjà dans le cache, ceci jusqu'à concurrence de la taille du cache.

## Cache miss et cache hit

Lorsqu'un processeur cherche une donnée dans le cache, il peut y avoir deux cas de figure: le cache **hit** et le cache **miss**.

Un cache hit est le cas où le processeur trouve la donnée dans le cache. C'est le cas le plus rapide car le processeur n'a pas besoin d'aller chercher la donnée dans la mémoire RAM.

Un cache miss est le cas où le processeur ne trouve pas la donnée dans le cache. C'est le cas le plus lent car le processeur doit aller chercher la donnée dans la mémoire RAM. Il existe plusieurs types de cache miss, citons-en quelques uns:

1. **Compulsory miss**: C'est le premier accès à une donnée. Le processeur ne peut pas savoir à l'avance si la donnée est dans le cache ou non. Il doit donc aller chercher la donnée dans la mémoire RAM. Ce type de cache miss est inévitable.
2. **Capacity miss**: Le cache est plein et le processeur doit remplacer une ligne de cache pour pouvoir stocker une nouvelle donnée. Ce type de cache miss est inévitable.
3. **Conflict miss**: Deux données différentes ont le même tag. Ce type de cache miss est évitable en choisissant judicieusement les tags.
4. **Coherence miss**: Un autre processeur a modifié la donnée. Ce type de cache miss est évitable en utilisant des protocoles de cohérence de cache.

Plusieurs raisons peuvent expliquer un cache miss.

## True sharing

Le true sharing est le cas où deux processeurs partagent la même donnée. Cela peut causer des ralentissements importants dans un programme concurrent car les deux processeurs doivent se synchroniser pour éviter les problèmes de cohérence de cache à chaque accès à la donnée partagée.

## False sharing

Le false sharing est un problème qui survient lorsqu'un processeur modifie une donnée non partagée mais sur la même ligne de cache qu'une autre donnée. Cela survient typiquement dans le cas de la programmation concurrente. Lorsqu'un processeur modifie une donnée, il doit invalider la ligne de cache de l'autre processeur. Si les deux processeurs modifient des données qui sont sur la même ligne de cache, alors les deux processeurs doivent se synchroniser.

On appelle cela le false sharing car les deux processeurs ne partagent pas la même donnée mais ils partagent la même ligne de cache.

En C++17 le concept de `std::hardware_destructive_interference_size` permet de connaître la taille d'une ligne de cache. Il n'est néanmoins pas disponible dans tous les compilateurs. On peut utiliser la valeur 64 octets pour la plupart des processeurs.

## Compteur de performance

Un processeur moderne possède des compteurs de performance qui permettent de mesurer le comportement du processeeur. A chaque mauvaise prédiction d'embranchement, à chaque ralentissement d'un calcul FPU, à chaque évènement du cache (miss, hit, etc) un compteur est incrémenté. Ces compteurs sont accessibles via l'outil `perf` sur Linux et `VTune` sur Windows. Ce sont des outils indispensables pour mesurer les performances d'un programme.

## Exemples

Dans ce chapitre, l'objectif est de sensibilier le lecteur aux ralentissements causés par le matériel. Il ne suffit pas de faire de la programmation concurrente en cherchant à paralleliser un maximum de tâches pour obtenir un programme plus rapide. Il est nécessaire de prendre en compte les problèmes de cohérence de cache et de localité spatiale.

Plusieurs exemples vont être donnés:

- Rafraichissement de la mémoire
- Localité spatiale
- True sharing
- False sharing
- Prédiction de branchement

Pour chaque exemple, il est important de désactiver certaines fonctionnalités du processeur pour éviter des comportement inattendus.

1. Désactiver la randomisation de l'espace d'adressage, c'est à dire que les adresses mémoires sont toujours les mêmes à chaque exécution du programme.

   ```bash
   $ sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"
   ```

2. Désactiver le turbo mode, c'est à dire que le processeur ne peut pas augmenter sa fréquence pour accélérer les calculs.

   ```bash
   $ sudo bash -c "echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo"
   ```

3. Désactiver l'hyper-threading, c'est à dire que chaque coeur du processeur est utilisé par un seul thread. Cela doit être fait pour chaque coeur du processeur.

   ```bash
    $ sudo bash -c "echo 0 > /sys/devices/system/cpu/cpuX/online"
    ```

4. Désactiver le C-state, c'est à dire que le processeur ne peut pas passer en mode veille pour économiser de l'énergie.

    ```bash
    $ sudo cpupower frequency-set --governor performance
    ```

### Localité spatiale

Prenons l'exemple d'une matrice de NxN éléments. Si on parcourt la matrice par ligne, on profite de la localité spatiale car les éléments d'une ligne sont souvent utilisés en même temps.

En revanche si on parcourt la matrice par colonne, on ne profite pas de la localité spatiale car les éléments d'une colonne ne sont pas utilisés en même temps. Le cache est rapidement plein et le processeur doit aller chercher les données dans la mémoire RAM.

Le code [locality-line.cpp](locality-line.cpp) met en évidence la différence de performance entre un parcours par ligne et un parcours par colonne.

Pour le cas d'une matrice de 10'000x10'000 entiers 32-bits, on obtient les résultats suivants:

```
$ g++ -DCOLUMN -O3 locality-line.cpp && ./a.out
Somme en ligne : 4999999950000000
Temps d'accès: 0.772923 s

$ g++ -DLINE -O3 locality-line.cpp && ./a.out
Somme en ligne : 4999999950000000
Temps d'accès: 0.0275642 s
```

On observe que le parcours par ligne est 28 fois plus rapide que le parcours par colonne.

## Références

- https://medium.com/@techhara/speed-up-c-false-sharing-44b56fffe02b
- https://github.com/Kobzol/hardware-effects
- https://blog.cloudflare.com/every-7-8us-your-computers-memory-has-a-hiccup/
