# L'ordinateur

Un ordinateur personnel (PC pour *Personal Computer*) est un appareil électronique de petite taille destiné à un usage individuel. Il se distingue des ordinateurs centraux (ou *mainframes*) et des serveurs, qui sont destinés à un usage professionnel ou collectif.

Néanmoins, quelle que soit la taille de l'ordinateur, les composants de base sont les mêmes. Un ordinateur est composé de plusieurs éléments principaux:

- Un **processeur** (ou *CPU* pour *Central Processing Unit*) qui exécute les instructions des programmes.
- De la **mémoire** (ou *RAM* pour *Random Access Memory*) qui stocke les données et les instructions des programmes en cours d'exécution.
- Un **disque dur** (ou *HDD* pour *Hard Disk Drive*) qui stocke les données de manière permanente.
- Une **carte graphique** qui affiche les images à l'écran.
- Une **carte mère** qui relie tous les composants entre eux.

## La RAM

La mémoire vive est une mémoire de stockage temporaire, on l'appelle également mémoire non volatile. Le plus souvent une mémoire vive est amovible, il s'agit d'une barrette enfichable sur la carte mère. Avec l'évolution de la technologie, ces mémoires sont carénées et munies d'un dissipateur thermique :

![2 x 16 GB DDR5 DIMM Corsair Vengeance](/assets/images/sdram-corsair-vengeance.avif){ width=50% }

Sous le capôt, on peut voir les puces de mémoire:

![Crucial DDR4 16 GB](/assets/images/sdram.webp){ width=50% }

Cette mémoire dispose de 16 Gibioctets de mémoire, soit $16 \times 2^30 = 17179869184$ octets. Chaque octet est composé de $8$ bits, soit $17179869184 \times 8 = 137438953472$ bits. Comme nous voyons $4$ puces de mémoire, chaque puce contient $4$ Gibioctets.

Généralement, ces mémoires sont vendues en nombre de bits, soit ici 32 Gibibits.

Sur le circuit électronique ou PCB (*Printed Circuit Board*), on voit les 4 puces de mémoire soudées. Il s'agit d'un composant de la société Micron, un MT40A1G8. La structure interne de cette mémoire est donnée par la *datasheet* du composant:

![MT40A1G8](/assets/images/mt40a1g8-functional.drawio)

Pour décoder ce schéma, intéressons-nous aux flèches de couleur. Il s'agit du bus d'adresse. Ce bus comporte 16 lignes en parallèle qui sont interfacées à deux blocs : le *Row Address MUX* et le *Column address counter*. Ces deux blocs permettent de sélectionner une cellule mémoire selon la mémoire, une cellule peut valoir 4, 8, 16 ou 32 bits.

Les cellules mémoires sont organisées and matrice ligne/colonne et chaque matrice est organisée en banque. C'est ce qu'on observe sur ce diagramme.

Une mémoire volatile est une mémoire qui perd son contenu lorsqu'elle n'est plus alimentée en électricité. La raison est simple. Stocker un état électrique demande de l'énergie pour accumuler des charges électriques. Si l'on fait l'analogie que l'électricité est de l'eau, alors chaque bit de la mémoire est un verre d'eau que l'on peut remplir ou vider. Le seul moyen de lire le contenu du verre est de voir s'il y a de l'eau dedans, c'est-à-dire de le vider. Si le verre est grand, alors il faut plus de temps pour le remplir et plus de temps pour le vider ceci présente plusieurs inconvénients :

1. La vitesse de lecture est plus lente.
2. La quantité d'eau (courant) pour remplir le verre est plus grande.
3. L'encombrement est plus grand puisque le verre est plus volumineux.

Aussi, le choix technologique est d'avoir des tout petits verres. Ils sont si petits que l'eau contenue s'évapore très vite. Pour éviter cela, on doit constamment remplir les verres. C'est ce que l'on appelle la *rafraîchissement* de la mémoire. Périodiquement, environ toutes les 64 ms, on doit réécrire le contenu de la mémoire pour éviter que l'information ne se perde. Heureusement pour nous, cette opération est transparente pour l'utilisateur, c'est le contrôleur de mémoire qui s'en charge.

Les caractéristiques de la mémoire sont les suivantes:

| Caractéristique           | Valeur | Unité |
| ------------------------- | ------ | ----- |
| Capacité                  | 32     | Gib   |
| Tension d'alimentation    | 1.2    | V     |
| Fréquence                 | 1600   | MHz   |
| Temps de rafraîchissement | 64     | ms    |
| Nombre de banques         | 16     |       |
| Technologie               | DDR4   |       |

### Technologies

Il existe plusieurs technologies de mémoire vive. Les plus courantes sont: SDRAM, DDR, DDR2, DDR3, DDR4. Contrairement à la SDRAM qui est une mémoire synchrone, les mémoires DDR (*Double Data Rate*) sont des mémoires asynchrones. Cela signifie que la mémoire peut lire et écrire des données sur le flanc montant et descendant du signal d'horloge ce qui double la bande passante de la mémoire. Chaque génération améliore les performances en augmentant la fréquence de fonctionnement, la densité des puces mémoires et en réduisant la tension d'alimentation.

[](){#light-speed}
### Vitesse de la lumière

![Autoroute de l'information](/assets/images/highway.png)

La vitesse de la lumière est de 299 792 458 m/s. Elle est fixée par la convention du mètre. C'est la vitesse maximale que peut atteindre un objet dans l'univers. Pour donner un ordre de grandeur, un signal électrique se propage dans un câble à environ 2/3 de la vitesse de la lumière. Cela signifie que pour parcourir 1 mètre, un signal électrique met environ 5 ns.

Plus haut on a vu que le bus de données de la mémoire est souvent de 64-bits. Cela correspond à une autoroute de 64 voies avec quelques limitations :

- Les voies sont unidirectionnelles, c'est-à-dire que l'on ne peut circuler que dans un sens.
- Les voies sont séparées par des barrières, c'est-à-dire que l'on ne peut pas changer de voie.
- Les véhicules se déplacent tous à la vitesse d'environ 540 millions de km/h. Ils ne peuvent pas freiner, accélérer ou s'arrêter.

Pour transmettre une information, par exemple un nombre entier de 64 bits (`long long` en C), il faut faire entrer 64 véhicules sur chacune des voies. Chaque véhicule représente un bit. Pour que l'information soit transmise, il faut que les 64 véhicules soient alignés et qu'ils arrivent tous au même moment.

Sur la figure suivante, on voit le routage d'un circuit électronique. En rose, ce sont les composants physiques. À gauche un processeur et au milieu en bas deux circuits mémoire labélisés *DDR1* et *DDR2*. En bleu clair ce sont les lignes électriques qui relient les composants. On observe des tas de petites circonvolutions. Les lignes sont artificiellement rallongées pour que la longueur de chaque voie de l'autoroute soit la même, afin de garantir une vitesse de propagation identique pour chaque ligne de donnée.

![Routage d'une mémoire](/assets/images/sdram-layout.png)

Vous me direz, oui, mais 540 millions de km/h c'est super rapide et sur ce circuit les lignes ne font pas plus de 10 cm ce qui représente 600 ps pour parcourir la distance. Oui, mais voilà, on communique sur cette autoroute à 2000 MT/s (mégatransferts par seconde). Cela signifie que 2'000'000 de véhicules entrent sur chaque voie de l'autoroute chaque seconde circuler sur chaque voie de l'autoroute chaque seconde. N'est-ce pas incroyable?

Malgré ces performances, la mémoire reste un goulot d'étranglement pour les processeurs. En effet, les processeurs sont de plus en plus rapides et les mémoires ne suivent pas le rythme. Un processeur qui calcule à 4 GHz peut exécuter 4 milliards d'instructions par seconde. Si chaque instruction nécessite un accès mémoire et que cet accès prend 100 cycles d'horloge, alors le processeur ne pourra exécuter que 40 millions d'instructions par seconde. Cela signifie que le processeur ne sera utilisé qu'à 1% de sa capacité.

## Le disque dur

![Disque dur](/assets/images/hdd.jpg)

Le disque dur est un dispositif de stockage de masse. Il est composé de plusieurs plateaux magnétiques qui tournent à grande vitesse. Un bras mécanique se déplace sur les plateaux pour lire ou écrire les données. Les disques durs sont lents par rapport à la mémoire vive. Ils sont utilisés pour stocker des données de manière permanente.

De nos jours ces disques sont remplacés par des disques SSD (*Solid State Drive*) qui sont plus rapides et plus fiables. Les disques SSD sont composés de mémoire flash qui ne nécessite pas de pièces mobiles. Contrairement à la mémoire vive, les disques SSD sont des mémoires non volatiles. Cela signifie que les données sont conservées même lorsque l'alimentation est coupée.

![SSD de 2 TiB](/assets/images/ssd-990pro.avif){ width=50% }

Mais si les SSD peuvent stocker beaucoup plus de données sur le même espace, pourquoi sont-ils plus lents que la mémoire vive? La raison est simple. Les disques SSD sont organisés en blocs de données, que l'on appelle *pages* et *clusters*. Pour lire ou écrire une donnée, il faut lire ou écrire tout le bloc. Cela signifie que si l'on veut lire un octet, il faut lire 4'096 octets. C'est ce que l'on appelle le *page size*.

La communication entre le processeur et le disque SSD ou HDD utilise un protocole de communication série appelé *SATA* (*Serial ATA*). Ce protocole permet de transférer des données à une vitesse de 6 Gbit/s. Cela signifie que pour transférer un octet, il faut 8 bits, soit 8 ns. Cela semble rapide, mais si l'on veut lire un bloc de 4'096 octets, il faut 32'768 bits, soit 32'768 x 8 ns = 262'144 ns, soit 262 µs. C'est 262'144 fois plus lent que la mémoire vive.

Pour interfacer le processeur avec le disque dur, on utilise un contrôleur de disque. Ce contrôleur est un circuit électronique qui gère les accès disque. Il est composé lui-même d'un microprocesseur, de mémoire vive et de mémoire flash.

## La carte mère

![Carte mère](/assets/images/motherboard.webp){ width=50% }

La carte mère est le composant principal de l'ordinateur. C'est elle qui relie tous les composants entre eux. Elle est composée d'un circuit imprimé sur lequel sont soudés les différents composants et une grande quantité de connecteurs.

Le cœur de la carte mère est le **chipset**. C'est un ensemble de circuits électroniques qui gère les communications entre les différents composants. Il est composé de deux parties:

- Le **Northbridge** qui gère les communications entre le processeur, la mémoire vive et la carte graphique.
- Le **Southbridge** qui gère les communications entre les périphériques de stockage, les ports USB, les ports SATA, etc.

Le **chipset** est relié au processeur par un bus de données appelé **FSB** (*Front Side Bus*). Ce bus transporte les données entre le processeur et le chipset. La configuration du chipset est stockée dans une mémoire flash appelée **BIOS** (*Basic Input/Output System*). Le BIOS est un logiciel qui permet de configurer les paramètres de la carte mère.

À l'époque le BIOS offrait un accès très minimaliste à l'utilisateur. On pouvait le configurer avec un clavier et un écran qui n'affichait que des caractères.

De nos jours, le BIOS a été remplacé par l'**UEFI** (*Unified Extensible Firmware Interface*). L'UEFI est un logiciel plus évolué qui permet de configurer la carte mère avec une interface graphique. Il est possible de configurer la carte mère avec une souris et un écran tactile.

## Le processeur

Le processeur est le cerveau de l'ordinateur. C'est lui qui exécute les instructions des programmes. La figure suivante montre un processeur Intel i7-12700K dans son format LGA 1700. C'est à dire qu'il comporte 1700 broches pour se connecter à la carte mère.

![Processeur Intel i7](/assets/images/cpu-i7.png)

Sur les 1700 broches on distingue plusieurs types de broches:

- Les broches d'alimentation qui représentent 40..60% des broches. Elles sont nécessaires pour alimenter le processeur avec une tension de 1.2V.
- Le contrôleur mémoire (DDR4/DDR5) qui permet de connecter la mémoire vive au processeur. Cela représente environ 5..15% des broches.
- Les interfaces PCIe qui permettent de connecter des cartes d'extension comme des cartes graphiques, des cartes réseau, des cartes son, etc. Ce processeur supporte jusqu'à 20 lignes différentielles soit 40 broches.
- L'accès DMI, c'est l'interface entre lwe processeur et le chipset. Un DMI 4.0 x8 signifie qu'il y a 8 lignes (Rx/Tx), soit envron 16 broches.
- L'USB, quelques dizaines de broches.
- Le contrôleur graphique intégré (iGPU) qui comporte des ports HDMI/DisplayPort pour connecter un écran directement au processeur.
- Les interconnexions spécifiques (I2C, SPI, etc.)

Si on consulte le SDM (*Software Developer Manual*) d'Intel, un document de 5000 pages, on peut trouver des informations très intéressntes. Par exemple le chapitre sur les types numériques montre les différents type d'entiers ( `byte`, `word`, `dword`, `qword`), de flottants (`half`, `single`, `double`, `extended`) et de vecteurs (`xmm`, `ymm`, `zmm`, `kmm`). Il est expliqué que le processeur fonctionne avec le complément à 2 pour les entiers et le IEEE 754 pour les flottants, qu'il est en *little-endian* et que les registres sont de 64 bits. Le langage C au final est très proche de l'assembleur du processeur.

### Protection ring

Les *protection rings* (ou anneaux de protection) sont un mécanisme de sécurité utilisé dans l'architecture des processeurs, principalement dans les systèmes d'exploitation modernes, pour contrôler l'accès aux ressources du système par différents types de code (comme les applications ou les composants du système d'exploitation).

L'idée des anneaux de protection repose sur la séparation des niveaux de privilège ou de contrôle en plusieurs couches. Chaque couche, ou ring (anneau), est un niveau de privilège qui détermine ce qu’un programme ou une instruction peut faire. Dans l'architecture x86 d'Intel, il y a généralement quatre anneaux (de 0 à 3), bien que les systèmes d'exploitation modernes n’utilisent souvent que deux de ces niveaux (Ring 0 et Ring 3).

![Anneaux de protection](/assets/images/protection-rings.drawio)

Le ring 0 correspond au noyau (kernel) du système d'exploitation, qui a accès à toutes les ressources matérielles de l'ordinateur. Il peut exécuter n'importe quelle instruction, accéder à la mémoire directement, et gérer le matériel sans restriction. On parle souvent de mode superviseur ou mode noyau pour désigner les opérations effectuées dans cet anneau. C’est le niveau le plus privilégié.

Les niveaux intermédiaires 1 et 2 peuvent être utilisés par certains systèmes pour les pilotes ou des services du système qui ont besoin d'un accès contrôlé aux ressources, mais ne nécessitent pas le même niveau de privilège que le noyau. Toutefois, la plupart des systèmes d'exploitation modernes ne les utilisent pas directement.

Enfin, le niveau 3 est réservé aux applications utilisateur. Il s’agit du mode utilisateur (user mode), dans lequel les programmes n’ont pas un accès direct au matériel ou à la mémoire, et doivent passer par des appels système pour demander des services au noyau. En cas de violation des règles (comme essayer d’accéder directement au matériel), une exception ou une erreur est générée, et le programme est bloqué.

### Bref historique

#### 1978 : Processeurs 16 bits

L'introduction des processeurs 8086 et 8088 a marqué le début de l'architecture IA-32 avec des registres 16 bits et une adresse mémoire maximale de 1 Mo. La segmentation permettait d'adresser jusqu'à 256 Ko sans changement de segment, ouvrant la voie à une gestion plus efficace de la mémoire.

#### 1982 : Intel 286

Le processeur Intel 286 a introduit le mode protégé, permettant une meilleure gestion de la mémoire avec un adressage sur 24 bits et la possibilité de gérer jusqu'à 16 Mo de mémoire physique. Le mode protégé apportait également des mécanismes de protection tels que la vérification des limites des segments et plusieurs niveaux de privilèges.

#### 1985 : Intel 386

Première architecture véritablement 32 bits, l'Intel 386 a introduit des registres 32 bits et un bus d'adressage permettant de gérer jusqu'à 4 Go de mémoire physique. Il proposait aussi un mode de mémoire virtuelle et un modèle mémoire à pages de 4 Ko, facilitant la gestion efficace de la mémoire.

#### 1989 : Intel 486

Le processeur Intel 486 a ajouté des capacités de traitement parallèle avec cinq étapes de pipeline d’exécution, permettant l’exécution simultanée d'instructions. Il a également introduit un cache de 8 Ko sur la puce et un coprocesseur mathématique intégré (FPU).

#### 1993 : Intel Pentium

L'Intel Pentium a marqué une nouvelle avancée avec l'ajout de deux pipelines d'exécution, permettant l'exécution de deux instructions par cycle d'horloge. Il a également intégré un système de prédiction de branchement et augmenté le bus de données externe à 64 bits. Plus tard, la technologie MMX a été introduite, optimisant le traitement parallèle de données pour les applications multimédia.

#### 1995 : Famille P6

La famille P6 a apporté une nouvelle microarchitecture superscalaire avec un processus de fabrication de 0,6 micron, améliorant considérablement les performances tout en maintenant la compatibilité avec les technologies existantes.

#### 2000 : Intel Pentium 4

Basé sur l'architecture NetBurst, le Pentium 4 a introduit les extensions SIMD Streaming (SSE2), puis SSE3, pour accélérer les calculs multimédias. Le support du 64 bits avec l'Intel 64 architecture a également fait son apparition, ainsi que la technologie Hyper-Threading pour exécuter plusieurs threads simultanément.

#### 2001 : Intel Xeon

La gamme Xeon, basée également sur l'architecture NetBurst, a été conçue pour les serveurs multiprocesseurs et les stations de travail. Elle a introduit le multithreading (Hyper-Threading) et, plus tard, des processeurs multi-cœurs pour augmenter les performances dans les environnements professionnels.

#### 2008 : Intel Core i7

La microarchitecture Nehalem, utilisée dans la première génération d'Intel Core i7, a marqué l'avènement du 45 nm, avec des fonctionnalités comme le Turbo Boost, l’Hyper-Threading, un contrôleur mémoire intégré, et un cache Smart Cache de 8 Mo. Le lien QuickPath Interconnect (QPI) a remplacé l’ancien bus pour des échanges plus rapides avec le chipset.

#### 2011 : Intel Core Sandy Bridge

Cette génération, construite en 32 nm, a apporté des améliorations en termes de performance et d'efficacité énergétique, avec des innovations comme l'intégration des graphismes dans le processeur et l'Intel Quick Sync Video. La gamme incluait les processeurs Core i3, i5, et i7.

#### 2012 : Intel Core Ivy Bridge

L'Ivy Bridge a introduit une finesse de gravure de 22 nm, permettant une meilleure gestion de la consommation énergétique tout en améliorant les performances graphiques et générales du processeur. Cette génération a également marqué l'arrivée de processeurs Xeon plus puissants pour les serveurs.

#### 2013 : Intel Core Haswell

La quatrième génération, basée sur l’architecture Haswell, a continué d'améliorer les performances et l'efficacité énergétique, tout en proposant des améliorations comme l’intégration de la gestion de l’alimentation et des performances graphiques améliorées pour répondre aux besoins des utilisateurs modernes.

Ce résumé souligne les progrès constants en termes de puissance de traitement, de gestion mémoire, de parallélisme, et d’efficacité énergétique des processeurs Intel au fil des générations.
