# Threads

## Introduction

La gestion de l'ordonnancement des processus et des threads (processus légers) par le noyau d'un système d'exploitation a évolué avec le temps, notamment sous UNIX et Linux. Historiquement, les threads étaient souvent gérés au niveau utilisateur par des bibliothèques spécialisées, comme POSIX Threads (pthreads). Cette approche est connue sous le nom de threads au niveau utilisateur (*user-level threads*). Les systèmes modernes, dont Linux, privilégient désormais un modèle plus étroitement intégré à l'ordonnanceur du noyau.

## Threads au Niveau Utilisateur

Dans les modèles de threads au niveau utilisateur, l'ordonnancement est géré entièrement par la bibliothèque de threads dans l'espace utilisateur. Le noyau ignore la présence de threads au sein des processus : il ne voit et n'ordonnance que des processus. Cette approche offre une grande flexibilité et une bonne portabilité entre systèmes d'exploitation, mais présente plusieurs inconvénients :

- **Manque de connaissance du noyau** : comme le noyau ignore l'existence des threads, il ne peut pas prendre de décisions d'ordonnancement fondées sur l'état global du système. Cela conduit à une utilisation sous-optimale des ressources, notamment sur les machines multiprocesseurs.
- **Blocage au niveau du processus** : si un thread effectue un appel système bloquant, tout le processus — et donc tous ses threads — peut être bloqué, ce qui nuit à la concurrence.

## Threads au Niveau Noyau

Pour surmonter ces limitations, la plupart des systèmes d'exploitation modernes, y compris Linux, gèrent désormais les threads au niveau du noyau (*kernel-level threads*). Dans ce modèle, le noyau est pleinement conscient de chaque thread et peut les ordonnancer indépendamment. Cela permet une meilleure utilisation des ressources sur les systèmes multicœurs, car le noyau peut répartir les threads sur différents processeurs.

- **Meilleure concurrence** : chaque thread peut être ordonnancé indépendamment, ce qui permet à un processus de continuer à s'exécuter même si l'un de ses threads est bloqué.
- **Gestion des priorités** : le noyau peut ajuster les priorités des threads individuellement, offrant une granularité fine dans la gestion de l'ordonnancement.
- **Prise en charge du multiprocesseur** : le noyau peut répartir les threads d'un même processus sur plusieurs cœurs, exploitant pleinement le matériel disponible.

## Modèle N:M

Il existe également un modèle hybride, dit modèle N:M, qui tente de combiner les avantages des threads au niveau utilisateur et au niveau noyau. Dans ce modèle, N threads au niveau utilisateur sont mappés sur M threads au niveau noyau. Cette approche offre une certaine flexibilité dans la gestion des threads et peut améliorer les performances en réduisant le nombre de changements de contexte nécessaires. Toutefois, elle reste complexe à implémenter et n'est pas largement adoptée dans les systèmes d'exploitation modernes.

## Conclusion

L'approche moderne de la gestion de l'ordonnancement des processus et des threads par le noyau offre une flexibilité, une efficacité et une évolutivité nettement supérieures aux méthodes historiques. Les threads au niveau noyau permettent une utilisation optimale du matériel multiprocesseur et multicœur, tout en offrant une gestion fine de la concurrence et de la parallélisation au sein des applications.

C++20 n'introduit pas de nouvelles fonctionnalités spécifiquement conçues pour les threads au niveau utilisateur, mais continue de prendre en charge le multithreading via sa bibliothèque standard, notamment avec `<thread>`, `<mutex>`, `<future>`, `<atomic>` et d'autres primitives de synchronisation et de communication.

Les threads gérés par la bibliothèque standard C++ sont des threads au niveau système (ou noyau), ce qui signifie que leur création, leur destruction et leur ordonnancement sont gérés par le système d'exploitation. Cela offre des avantages en termes de performances et d'utilisation sur des systèmes multicœurs, mais ne convient pas à tous les cas d'usage, en particulier lorsque l'on a besoin d'un grand nombre de threads avec des changements de contexte fréquents.
