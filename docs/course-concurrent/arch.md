# Architecture processeur

## Introduction

L'architecture d'un processeur est l'ensemble des éléments qui le compose et qui lui permettent de fonctionner. C'est un peu comme le corps humain, il y a des organes qui ont chacun un rôle bien précis.

## Historique

Les premiers processeurs étaient très simples, ils étaient composés de quelques milliers de transistors et avaient une fréquence de quelques MHz. Aujourd'hui, les processeurs sont composés de plusieurs milliards de transistors et ont une fréquence de plusieurs GHz.

Alain Turing a été l'un des premiers à imaginer un ordinateur, il a conçu un modèle théorique d'ordinateur appelé "Machine de Turing". C'est un modèle abstrait qui a permis de poser les bases de l'informatique moderne.

La machine de Turing permet de comprendre la notion de programme, de mémoire, de calcul, etc. Son fonctionnement est très simple:

- Elle possède une bande de papier infinie sur laquelle sont stockées des données.
- Une tête de lecture/écriture qui peut lire et écrire des données sur la bande.
- Un état interne qui permet de savoir ce que la machine est en train de faire.
- Un ensemble de règles qui permettent de changer l'état interne en fonction des données lues.

Avec ces quelques éléments simples, on peut montrer que l'on peut résoudre n'importe quel problème algorithmique. C'est ce qu'on appelle la "thèse de Church-Turing". La difficulté principale de ce modèle est de comment écrire les règles pour résoudre un problème donné. C'est là qu'intervient la programmation.

Lorsque les premiers ordinateurs ont vus le jours, il étaient composés d'éléments simples :

- Une mémoire volatile pour stocker les données et des états intermédiaires.
- Une mémoire non-volatile pour stocker des instructions a exécuter.
- Un processeur pour exécuter les instructions.

Ce processeur était également très simple. Il se composait d'une unité de calcul, d'une unité de contrôle et d'une unité de gestion de la mémoire.

L'unité de calcul nommé ALU (Arithmetic Logic Unit) permet de faire des opérations arithmétiques et logiques (addition, soustraction, multiplication, division, ET, OU, etc). L'unité de contrôle permet de lire les instructions en mémoire et de les exécuter. L'unité de gestion de la mémoire permet de lire et écrire des données en mémoire. Le jeu d'instruction était très simple, il se composait de quelques instructions seulement:

1. Déplacer une donnée de la mémoire vers l'ALU.
2. Déplacer une donnée de l'ALU vers la mémoire.
3. Faire une opération arithmétique ou logique sur les données de l'ALU.
4. Aller chercher une instruction à une adresse donnée en mémoire et la charger dans l'unité de contrôle.
5. Tester si une valeur est nulle et sauter à une adresse donnée si c'est le cas.

Avec les évolutions technologiques, de nombreux systèmes complexes ont été ajoutés.

Le premier constat de ces premiers ordinateurs est que le processeur était souvent plus rapide que la mémoire et qu'aller chercher une valeur en mémoire nécessitait plusieurs étapes. Durant ces étapes, le processeur devait attendre et n'utilisait pas son plein potentiel de calcul. On a alors ajouté un composant nommé *pipeline* qui permet d'exécuter les différentes étapes de la lecture d'une instruction en parallèle. Cela permet de réduire le temps d'attente du processeur. En effet, puisque le programme est exécuté séquentiellement, on sait que la prochaine instruction à exécuter est la suivante de celle en cours d'exécution. Si l'on dispose d'un pointeur `int *p` sur cett instruction, on sait que l'instruction suivante est localisée à `p + 1`. On peut alors anticiper la lecture de cette instruction en avance et la charger dans l'unité de contrôle. C'est ce qu'on appelle le *préchargement*. Typiquement un processeur dispose de 3 à 5 étages de pipeline dont chaque étage correspond à une étape de la lecture d'une instruction :

1. Préchargement de l'instruction.
2. Décodage de l'instruction.
3. Exécution de l'instruction.
4. Accès à la mémoire.
5. Écriture du résultat.

Hélas, le pipeline n'est pas sans inconvénient. En effet, si une instruction dépend du résultat d'une autre instruction, il faut attendre que cette dernière soit terminée pour pouvoir exécuter la première. C'est ce qu'on appelle un *hazard*. Il existe plusieurs types de hazard :

- *Data hazard* : lorsque deux instructions dépendent du même registre.
- *Control hazard* : lorsque le résultat d'une instruction conditionnelle n'est pas encore connu.

Le *control hazard* apparaît typiquement lorsque l'on fait un saut conditionnel (`if`, `for`, `while`...). En effet, le processeur ne sait pas si le saut doit être effectué ou non avant d'avoir exécuté l'instruction conditionnelle. Sur des microcontrolleurs simples, une des deux branches de la condition est privilégiée. On précharge cette branche dans le pipeline et si la condition est fausse, on annule les résultats de l'exécution ce qui équivaut à vider intégralement le pipeline. Le coût est important car le processeur doit alors attendre que le pipeline se remplisse à nouveau avant de pouvoir exécuter la prochaine instruction.

Avec la complexification des processeurs modernes, le `pipeline` est devenu de plus en plus long. Aujourd'hui, un processeur moderne dispose de 15 à 20 étages de pipeline. Le problème des hazards est devenu de plus en plus important.

Un processeur moderne s'est donc équipé d'un autre mécanisme pour pallier ce problème que l'on nomme le predicteur d'embranchement. En effet, si le processeur peut prédire si un saut doit être effectué ou non, il peut précharger la bonne instruction dans le pipeline. Si la prédiction est bonne, on gagne du temps, sinon on perd du temps. Il existe plusieurs stratégies de prédiction de branchement :

- *Prédiction statique* : on prédit que le saut est toujours effectué ou non.
- *Prédiction dynamique* : on prédit le saut en fonction de l'historique des sauts précédents.

Les processeurs modernes conservent donc une table de prédiction de branchement qui permet de stocker l'historique des sauts précédents pour chaque instruction de conditions. Si un saut est souvent effectué, on prédit qu'il le sera à nouveau.

Néanmoins, il reste une difficulté majeure à résoudre, les latences mémoires. En effet, plus la mémoire est grosse et éloignée du processeur, plus le temps d'accès est long.

A titre d'exemple, une mémoire DDR4 a une latence de 15 ns alors qu'un processeur moderne a une fréquence de 3 GHz soit une latence de 0.33 ns. Cela signifie que le processeur doit attendre 45 cycles pour accéder à la mémoire. En pratique, c'est encore pire car la mémoire est souvent partagée entre plusieurs processeurs et doit être synchronisée. D'autre part, les mémoires sont organisées en pages mémoires, changer de page demande un temps supplémentaire. Le délai peut être de plusieurs centaines de cycles pour lire une donnée isolée en RAM.

Pour palier à ce problème, les processeurs se sont équipés de mémoires intermédiaires nommées mémoires caches. On distingue ajourd'hui 3 niveaux de caches :

- L1 : cache de niveau 1, très rapide, souvent intégré dans le coeur du processeur et à proximité directe de l'ALU.
- L2 : cache de niveau 2, plus lent que le L1 mais plus gros.
- L3 : cache de niveau 3, plus lent que le L2 mais plus gros et partagé entre plusieurs coeurs processeur.

Ceci nous amène aux architectures modernes multicoeurs. Un processeur Intel ou AMD moderne comporte très souvent 6 ou 8 processeurs indépendants reliés entre eux par une mémoire cache de niveau L3. Chaque coeur dispose de sa propre mémoire cache de niveau L1 et L2.

## Processeur moderne

La figure suivante représente la vue aérienne d'un processeur moderne. Le *die* ou substrat en silicium fait environ 1 à 2 cm de côté et comporte plusieurs milliards de transistors. Le savoir faire des ingénieurs est très gardé mais en observant la structure du die, on peut deviner les différents composants qui le compose.

![cpu](/assets/images/die.jpeg)

On peut voir sur cette figure la mémoire cache de niveau L3 facilement identifiable à son pattern de grille. On peut également voir les différents coeurs qui l'entourent, ils se ressemblent tous et on voit qu'ils sont également composés d'un motif répétitif qui est la mémoire cache de niveau L1 et L2. Souvent ces processeurs intègrent également une partie GPU qui est utilisée pour les calculs graphiques lorsqu'il n'y a pas de carte graphique intégrée.

Si l'on s'intéresse à un coeur en particulier, on peut voir qu'il est composé de plusieurs éléments. Tout d'abord à droite on trouve la mémoire cache L2 qui représente environ 20% de la surface du coeur. Ensuite le prédicteur d'embranchement très proche du cache L1 contenant les prochaines instructions à exécuter. Le décodeur d'instructions est à proximité du I-Cache et du prédicteur d'embranchement. Il est couplé à un ordonnanceur de micro-opérations qui adresse chaque calcul soit sur l'ALU pour de la virgule fixe, soit sur la FPU pour les calculs en virgule flottante. Dans la partie inférieure, on trouve l'ALU 64-bits, le cache de données L1 et le gestionnaire de mémoire permettant de lire/écrire des données en mémoire.

![core](/assets/images/zen2.png)