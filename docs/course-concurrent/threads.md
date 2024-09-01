# Threads

- [Threads](#threads)
  - [Introduction](#introduction)
  - [Threads au Niveau Utilisateur](#threads-au-niveau-utilisateur)
  - [Threads au Niveau Noyau](#threads-au-niveau-noyau)
  - [Modèle N:M](#modèle-nm)
  - [Conclusion](#conclusion)

## Introduction

La gestion de l'ordonnancement des processus et des threads (processus légers) par le noyau d'un système d'exploitation a évolué avec le temps, notamment sous les systèmes UNIX et Linux. Historiquement, en effet, les threads étaient souvent gérés au niveau utilisateur par des bibliothèques de threads, comme la bibliothèque POSIX Threads (pthreads) sous UNIX. Cette approche est connue sous le nom de threads au niveau utilisateur (User-Level Threads). Cependant, les systèmes modernes, y compris Linux, utilisent une approche différente qui permet une meilleure intégration avec l'ordonnanceur du noyau.

## Threads au Niveau Utilisateur

Dans les modèles de threads au niveau utilisateur, l'ordonnancement des threads est géré entièrement par la bibliothèque de threads dans l'espace utilisateur. Le noyau n'est pas conscient de la présence de threads au sein des processus ; il ne voit et n'ordonnance que des processus. Cette approche permet une grande flexibilité et une portabilité entre différents systèmes d'exploitation, mais présente plusieurs inconvénients :

- **Manque de Connaissance du Noyau** : comme le noyau n'est pas conscient des threads, il ne peut pas prendre de décisions d'ordonnancement basées sur l'état de tous les threads dans le système. Cela peut conduire à une utilisation sous-optimale des ressources, notamment sur les systèmes multiprocesseurs.
- **Blocage au Niveau du Processus** : Si un thread effectue un appel système bloquant, tout le processus (et donc tous ses threads) peut être bloqué, ce qui n'est pas idéal pour la concurrence.

## Threads au Niveau Noyau

Pour surmonter ces limitations, la plupart des systèmes d'exploitation modernes, y compris Linux, gèrent désormais les threads au niveau du noyau (Kernel-Level Threads). Dans ce modèle, le noyau est pleinement conscient de chaque thread et peut les ordonnancer indépendamment. Cela permet une meilleure utilisation des ressources sur les systèmes multicœurs, car le noyau peut répartir les threads sur différents processeurs.

- **Meilleure Concurrency** : Chaque thread peut être ordonnancé indépendamment, permettant à un processus de continuer à s'exécuter même si l'un de ses threads est bloqué.
- **Gestion des Priorités** : Le noyau peut ajuster les priorités des threads individuellement, offrant une granularité fine dans la gestion de l'ordonnancement.
- **Support Multiprocesseur** : Le noyau peut répartir les threads d'un même processus sur plusieurs cœurs, exploitant pleinement le matériel multiprocesseur.

## Modèle N:M

Il existe également un modèle hybride, le modèle N:M, qui tente de combiner les avantages des threads au niveau utilisateur et au niveau noyau. Dans ce modèle, N threads au niveau utilisateur sont mappés sur M threads au niveau noyau. Cela permet une certaine flexibilité dans la gestion des threads et peut améliorer la performance en réduisant le nombre de changements de contexte nécessaires. Cependant, ce modèle est complexe à implémenter et n'est pas largement utilisé dans les systèmes d'exploitation modernes.

## Conclusion

L'approche moderne de la gestion de l'ordonnancement des processus et des threads par le noyau offre une flexibilité, une efficacité et une scalabilité significativement meilleures par rapport aux méthodes historiques. Les threads au niveau noyau permettent une utilisation optimale du matériel multiprocesseur et multicœur, tout en offrant une gestion fine de la concurrence et de la parallélisation au sein des applications.

C++20 lui-même n'introduit pas de nouvelles fonctionnalités spécifiquement conçues pour les threads au niveau utilisateur, mais il continue de supporter le multithreading à travers sa bibliothèque standard, notamment avec `<thread>`, `<mutex>`, `<future>`, `<atomic>`, et d'autres facilités de synchronisation et de communication entre threads.

Les threads gérés par la bibliothèque standard C++ sont des threads au niveau système (ou noyau), ce qui signifie que leur création, destruction, et ordonnancement sont gérés par le système d'exploitation. Cela offre des avantages en termes de performances et d'utilisation sur des systèmes multicœurs, mais peut ne pas être idéal pour tous les cas d'utilisation, particulièrement ceux nécessitant un grand nombre de threads avec des changements de contexte fréquents.