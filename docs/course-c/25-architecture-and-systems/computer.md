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

### Architecture

Les architectures Von Neumann et Harvard sont deux modèles fondamentaux d'organisation d'un système informatique, qui se distinguent principalement par la façon dont elles gèrent la mémoire et le bus de données. Chacune a ses avantages et inconvénients, et elles sont utilisées dans différents contextes selon les besoins spécifiques du système.

![Comparaison Havard et Von Neumann](/assets/images/von-neumann-harvard.drawio)

Dans le modèle de John von Neumann, les instructions et les données sont stockées dans une mémoire unifiée, et le processeur utilise le même bus pour accéder à la mémoire, qu'il s'agisse d'instructions ou de données. Cela rend l'architecture plus simple et plus flexible, mais peut entraîner des goulets d'étranglement si le processeur doit accéder à la mémoire pour les deux types d'opérations simultanément.

Avec Harvard, les instructions et les données sont stockées dans des mémoires séparées, chacune ayant son propre bus de données. Cela permet au processeur d'accéder simultanément à une instruction et à des données, améliorant les performances globales du système.

De nos jours, les processeurs modernes (x86-64, ARM, etc.) utilisent une architecture hybride qui combine des éléments des deux modèles. Par exemple, les caches de niveau 1 et 2 stockent à la fois les instructions et les données, tandis que la mémoire principale est organisée de manière Von Neumann. Cela permet de combiner les avantages des deux approches pour obtenir des performances optimales.

### Chipset

![Chipset](/assets/images/chipset-cpu.drawio)

### Mémoire cache

![Hiérarchie mémoire](/assets/images/cache-hierarchy.drawio)

### Structure interne

![Diagramme d'un processeur](/assets/images/cpu-diagram.drawio)

### Coeur

![Diagramme d'un coeur de processeur](/assets/images/cpu-core-diagram.drawio)

#### Registres

Dans une architecture super-scalaire hors-ordre (*out-of-order*) comme le x86-64, lorsqu'un programme est écrit en assembleur ou en langage machine, il fait appel à des registres architecturaux comme RAX, RBX etc. Ces registres font partie du **modèle de programmation** x86-64 et chaque programmeur ou compilateur les voit comme des éléments physiques qu'ils peuvent manipuler.

Cependant, dans un processeur moderne hors-ordre (comme les Intel Core i7/i9, AMD Ryzen, etc.), la réalité matérielle est plus complexe. Les registres que le programmeur n'existent pas directement sous cette forme dans le matériel. Les processeurs modernes sont capables d'exécuter plusieurs instructions en parallèle grâce à une technique appelée exécution **hors-ordre**. Dans ce contexte, il est nécessaire de gérer plusieurs versions d'un même registre (comme RAX) à différents moments, car plusieurs instructions peuvent essayer de modifier ou d'utiliser ce registre de manière simultanée ou presque.

C'est là qu'intervient le concept de renommage des registres. Le processeur dispose d'un ensemble de registres physiques (ou registres de données) qui stockent les valeurs des registres architecturaux. Ces registres physiques sont opaques pour le programmeur. Lorsque le processeur exécute un programme, il utilise une technique appelée renommage des registres pour associer temporairement chaque registre architectural (comme RAX) à un registre physique spécifique. Cela permet au processeur d'éviter les conflits entre instructions qui voudraient utiliser le même registre en même temps.

Voici comment cela fonctionne :

1. Lorsqu'une instruction est décodée, le processeur associe chaque registre architectural à un registre physique. Le processeur gère une table de renommage qui fait correspondre chaque registre architectural à un registre physique.
2. Exécution hors-ordre : Les instructions sont exécutées dans l'ordre dans lequel elles sont décodées, mais les résultats peuvent être renvoyés dans un ordre différent. Cela signifie que les instructions peuvent être exécutées dans un ordre différent de celui dans lequel elles apparaissent dans le code source.
3. Retirement (retrait) : une fois que les instructions sont exécutées et validées, les résultats des registres physiques sont reflétés dans les registres architecturaux lors de l'étape de retrait (retirement). À ce stade, le programmeur ou le système voit les registres comme étant mis à jour dans l'ordre correct.

Le *Reorder Buffer (ROB)* est une structure clé dans ce processus. Il permet au processeur de garder une trace des instructions en cours d'exécution hors-ordre et il s'assure que les instructions sont retirées (c'est-à-dire, finalisées et appliquées aux registres architecturaux) dans le bon ordre, tel que prévu par le programmeur. Au moment du retrait, via le ROB, les résultats des registres physiques sont copiés vers les registres architecturaux visibles par le programmeur. C'est ce moment-là où, du point de vue du programmeur, le registre RAX ou RBX est mis à jour.

### L'assembleur

Le saviez-vous, il n'est pas indispensable de connaître le C pour développer des programmes sur un ordinateur. 85% des processeurs équipant les ordinateurs personnels sont sur une base x86-64. C'est à dire que si l'on connaît l'architecture, on peut écrire des programmes directement en assembleur. C'est un langage de bas niveau qui permet de contrôler directement le processeur.

Admettons que l'on souhaite réécrire notre programme `hello.c` mais en assembleur. Ici, il ne faut pas imaginer accéder directement à l'écran pour écrire du texte. Il faut passer par le système d'exploitation. Pour cela, on utilise les appels systèmes. C'est exactement ce que fait `printf`.

```nasm
section .data
    message db "Hello, World!", 0xA
    len equ $-message       ; Taille du message

section .text
global _start

_start:
    ; Appel système pour écrire (sys_write)
    mov rax, 1              ; Numéro d'appel système pour sys_write
    mov rdi, 1              ; Descripteur de fichier 1 (stdout)
    mov rsi, message        ; Adresse du message
    mov rdx, len            ; Longueur du message
    syscall                 ; Appel système

    ; Appel système pour terminer le programme (sys_exit)
    mov rax, 60             ; Numéro d'appel système pour sys_exit
    xor rdi, rdi            ; Code de sortie 0
    syscall                 ; Appel système
```

Pour le compiler, on utilisera `nasm` et `ld`:

```bash
nasm -f elf64 hello.s -o hello.o
ld hello.o -o hello
```

Ce programme ne comporte que deux appel systèmes `write` et `exit`.

Admettons que l'on souhaite multiplier 12345 avec 67890 et afficher le résultat sur la sortie standard. Ce programme est déjà plus compliqué. Les deux valeurs peuvent être stockées dans un registre 64-bit comme `rax` et `rbx`. Pour afficher le résultat, il faut convertir le nombre en chaîne de caractères, c'est ce que fait normalement `%d` dans `printf` mais ici nous sommes en assembleur, nous n'avons pas accès à cette fonction facilement. La stratégie est donc de diviser le nombre par 10 et de stocker le reste dans un tampon. On répète l'opération jusqu'à ce que le quotient soit nul. Ensuite, on inverse le tampon pour obtenir le nombre correct.

```nasm
section .data
    message db "12345 * 67890 = "  ; Message à afficher
    len equ $-message              ; Taille du message

section .bss
    buffer resb 20                     ; Tampon pour stocker le résultat converti

section .text
global _start

; Fonction int_to_string : Convertit un entier en chaîne de caractères
; Entrée : rdi = entier à convertir, rsi = tampon pour stocker la chaîne (ptr)
; Sortie : rbx = longueur de la chaîne (entier)
int_to_string:
    mov rbx, 0              ; Longueur initiale de la chaîne
    mov rcx, 10             ; Diviseur (10 pour conversion décimale)

.convert_loop:
    xor rdx, rdx            ; Réinitialiser rdx
    div rcx                 ; Diviser rax par 10, quotient dans rax, reste dans rdx
    add dl, '0'             ; Convertir le chiffre en caractère ASCII
    dec rsi                 ; Déplacer le pointeur dans le tampon
    mov [rsi], dl           ; Stocker le caractère dans le tampon
    inc rbx                 ; Augmenter la longueur de la chaîne
    test rax, rax           ; Vérifier si le quotient est zéro
    jnz .convert_loop       ; Si ce n'est pas zéro, continuer la conversion

    ; Retourner le début de la chaîne
    mov rax, rsi            ; Placer le pointeur vers la chaîne convertie dans rax
    ret

_start:
    ; Afficher le message
    ; rax = 1 (sys_write), rdi = 1 (stdout), rsi = message, rdx = len
    mov rax, 1
    mov rdi, 1
    mov rsi, message
    mov rdx, len
    syscall

    ; Multiplication non signée de 12345 par 67890
    mov rax, 12345
    mov rbx, 67890
    imul rax, rbx

    ; Appel de la sous-routine pour convertir l'entier en chaîne
    ; rdi = rax (résultat calcul), rsi = buffer + 20 (fin du tampon)
    mov rdi, rax
    mov rsi, buffer + 20
    call int_to_string

    ; Afficher le résultat (chaîne convertie)
    ; rax = 1 (sys_write), rdi = 1 (stdout), rdx = longueur de la chaîne
    mov rax, 1
    mov rdi, 1
    mov rdx, rbx
    syscall

    ; Fin du programme
    ; rax = 60 (sys_exit), rdi = 0 (code de sortie)
    mov rax, 60
    xor rdi, rdi
    syscall
```

### SSE

Les instructions SSE (*Streaming SIMD Extensions*) sont une extension de l'architecture x86 introduite par Intel en 1999 avec les processeurs Pentium III. Elles permettent d'effectuer des opérations vectorielles sur des registres de 128 bits, ce qui améliore les performances pour les calculs intensifs en parallèle.

Le SIMD (*Single Instruction, Multiple Data*) est une technique de parallélisme de données qui permet d'effectuer la même opération sur plusieurs données simultanément.

Les applications possibles sont : filtre d'image, mélange de couleurs, compression d'image, traitement audio, multiplication de matrices, etc.

On peut par exemple additionner $[a_1, a_2, a_3, a_4]$ avec $[b_1, b_2, b_3, b_4]$ en une seule instruction:

```nasm
section .data
    ; Tableaux de 4 floats (single precision, 32 bits)
    a: dd 1.1, 2.2, 3.3, 4.4
    b: dd 5.5, 6.6, 7.7, 8.8

add_floats:
    ; Charger les 4 floats dans xmm0 et xmm1
    movaps xmm0, [a]        ; Charger les 4 floats (32 bits chacun)
    movaps xmm1, [b]        ; Charger les 4 floats à partir de [b]

    addps xmm0, xmm1        ; Additionner les 4 floats dans xmm0

    mulps xmm0, xmm0        ; Carré des 4 floats dans xmm0
```

Dans gcc, on peut utiliser les options `-msse` ou `-msse2` pour activer les instructions SSE, alternativement on peut utiliser `-march=native` pour activer les instructions SIMD spécifiques à l'architecture du processeur.

Hélas, ni gcc ni clang ne semblent pas être très performants. Même avec ces options, il est incapable de vectoriser convenablement les opérations. L'alternative est d'utiliser la bibliothèque intrinsèque de gcc pour les instructions SIMD `<xmmintrin.h>`:

```c
#include <xmmintrin.h>

void compute(const float *a, const float *b, float *c) {
#if 0
    __m128 va = _mm_loadu_ps(a);
    __m128 vb = _mm_loadu_ps(b);
    __m128 vc = _mm_add_ps(va, vb);
    _mm_storeu_ps(c, vc);
#else
    c[0] = a[0] + b[0];
    c[1] = a[1] + b[1];
    c[2] = a[2] + b[2];
    c[3] = a[3] + b[3];
#endif
}
```

L'objectif est d'obtenir le code suivant :

```nasm
compute:
  vmovups xmm0, xmmword ptr [rdi]
  vaddps xmm0 , xmm0, xmmword ptr [rsi]
  vmovups xmmword ptr [rdx], xmm0
  ret
```

### AVX

Les instructions AVX (*Advanced Vector Extensions*) sont une extension de l'architecture x86 introduite par Intel en 2011 avec les processeurs Sandy Bridge. Elles permettent d'effectuer des opérations vectorielles sur des registres de 256 bits, ce qui améliore les performances pour les calculs intensifs en parallèle.

Voici l'exemple d'une addition de 8-float en utilisant les instructions AVX:

```nasm
section .data
    ; Tableau de 8 floats (single precision, 32 bits)
    numbers: dd 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8

add_floats:
    ; Initialiser les registres
    lea rdi, [numbers]        ; Charger l'adresse de départ du tableau dans rdi
    vpxor ymm0, ymm0, ymm0    ; Initialiser ymm0 à zéro pour la somme

    ; Charger les 8 floats dans ymm1
    vmovaps ymm1, [rdi]       ; Charger les 8 floats (32 bits chacun)
                              ; à partir de [numbers]

    ; Additionner les 8 floats
    vaddps ymm0, ymm0, ymm1   ; Additionner les 8 floats dans ymm0

    ; Réduction des 8 valeurs dans ymm0 pour obtenir la somme finale
    vhaddps ymm0, ymm0, ymm0  ; Addition horizontale des paires d'éléments
    vhaddps ymm0, ymm0, ymm0  ; Répéter pour réduire encore les valeurs
    vhaddps ymm0, ymm0, ymm0  ; Une dernière fois pour obtenir la somme finale

    ; À ce point, la somme finale des 8 floats est dans le registre ymm0[0]
```

Sans système de vectorisation, il faut plus d'instruction :

```nasm
section .data
    numbers: dd 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8

add_floats:
    lea rdi, [numbers]        ; Charger l'adresse de départ du tableau dans rdi

    ; Charger et ajouter les flottants avec la FPU
    fld dword [rdi]           ; Charger le premier float sur la pile FPU
    fld dword [rdi + 4]       ; Charger le deuxième float
    fadd                      ; Ajouter le deuxième au premier
    fld dword [rdi + 8]       ; Charger le troisième float
    fadd                      ; Ajouter le troisième au résultat
    fld dword [rdi + 12]      ; Charger le quatrième float
    fadd                      ; Ajouter le quatrième au résultat
    fld dword [rdi + 16]      ; Charger le cinquième float
    fadd                      ; Ajouter le cinquième au résultat
    fld dword [rdi + 20]      ; Charger le sixième float
    fadd                      ; Ajouter le sixième au résultat
    fld dword [rdi + 24]      ; Charger le septième float
    fadd                      ; Ajouter le septième au résultat
    fld dword [rdi + 28]      ; Charger le huitième float
    fadd                      ; Ajouter le huitième au résultat

    ; À ce point, la somme est au sommet de la pile FPU (ST(0))
```

## Processeur minimal

Pour mieux comprendre le fonctionnement d'un processeur, il est intéressant de concevoir un processeur minimal.
Imaginons donc un processeur le plus simple sachant qu'un compromis doit être trouvé entre simplicité et fonctionnalité.

En effet, un processeur dispose des caractéristiques fondamentales suivantes :

- Largeur du bus de données
- Nombre d'instructions

Avec un jeu d'instruction très réduit comme comme sur l'OISC (*One Instruction Set Computer*) ou le CPU Zero, on peut concevoir un processeur minimaliste avec l'instruction *Subtract and Branch if Negative* (SBN). C'est une instruction qui soustrait deux valeurs et saute à une adresse si le résultat est négatif. Avec cette seule instruction, il est possible de simuler toutes les opérations qui seraient normaelemnt effectuées par un ensemble d'instructions plus riche comme l'addition, la soustraction, les comparaisons et les sauts conditionnels.

La quantité d'instructions dans un processeur classifie sa nature, on distingue les processeurs RISC (*Reduced Instruction Set Computer*) et CISC (*Complex Instruction Set Computer*). Les processeurs RISC ont un jeu d'instructions réduit, ce qui les rend plus simples et plus rapides. Les processeurs CISC ont un jeu d'instructions plus riche, ce qui les rend plus complexes mais plus polyvalents. Il y eut longtemps le débat entre les deux architectures, mais de nos jours, les processeurs modernes sont hybrides, ils combinent les avantages des deux architectures.

Pour notre processeur, on retiendra une dizaine d'instructions regroupant les opérations de base comme l'addition, la soustraction, les opérations logiques, les sauts conditionnels et les opérations de transfert de données.

Sur la figure suivante, on peut voir l'architecture minimale d'un processeur avec un jeu d'instructions réduit:

![Architecture minimale](/assets/images/cpu-zero.drawio)


- `ADD` : additionne `A` et `B` et stocke le résultat dans `C`
- `SUB` : soustrait `A` et `B` et stocke le résultat dans `C`
- `AND` : fait un `ET` logique entre `A` et `B` et stocke le résultat dans `C`
- `OR` : fait un `OU` logique entre `A` et `B` et stocke le résultat dans `C`
- `XOR` : fait un `OU EXCLUSIF` logique entre `A` et `B` et stocke le résultat dans `C`
- `JNZ` : si `A` est non nul, saute à l'instruction `B`
- `MOV A, Rx` : copie le registe `Rx` dans `A`
- `MOV B, Rx` : copie le registe `Rx` dans `B`
- `MOV Rx, C` : copie `C` dans le registe `Rx`
- `MOV Rx, Ry` : copie le registe `Ry` dans le registe `Rx`
- `MOV Rx, @Ry,Ry+1` : copie la valeur pointée par le registe `Ry` dans le registe `Rx`

- L'architecture est 8-bit, et la mémoire est de 256 bytes.
- L'adresse `0x0000` est le point d'entrée du programme.
- L'adresse `0xFFFE` est la queue d'entrée, une valeur lue
- L'adresse `0xFFFF` est la queue de sortie, l'affichage de la sortie, chaque valeur écrite est imprimée en ASCII sur une imprimante.

OP: `Opcode`, c'est le code de l'instruction à exécuter. Il est chargé dans l'ALU pour sa configuration. Si l'OP est `ADD` l'ALU exécute combinatoirement l'addition de `A` et `B` et le résultat est disponible sur `C`.

ST: C'est le statut de l'ALU. On y trouve les flags `Z` (zero), `N` (negative), `C` (carry) et `O` (overflow).

PC: C'est le pointeur d'instruction. Il pointe sur l'adresse de la prochaine instruction à exécuter.

ADDH et ADDL c'est l'adresse de la mémoire à laquelle on veut accéder.

`DATA` c'est la valeur lue, ou que l'on souhaite écrire dans la mémoire.

Ce CPU à un pipeline simple. A chaque coup d'horloge :

1. PC est copié dans l'adresse de la mémoire à laquelle on veut accéder.
2. RD est activé pour lire la mémoire.
3. La valeur lue est chargée dans OP.
4. L'instruction est exécutée.
5. PC est incrémenté de 1.

Exemple d'exécution de `MOV A, R0` :

1. L'OE est activé sur R0.
2. Latch est activé sur A.
3. Latch est désactivé sur A.
4. L'OE est désactivé.

- 16 instructions donc 4 bits pour l'OP
- 8 registres donc 3 bits pour les registres


| Opcode     | Instruction | Exemple     | Description                           |
| ---------- | ----------- | ----------- | ------------------------------------- |
| 0b0000xxxx | ADD         |             |                                       |
| 0b0001xxxx | SUB         |             |                                       |
| 0b0010xxxx | AND         |             |                                       |
| 0b0011xxxx | OR          |             |                                       |
| 0b0100xxxx | XOR         |             |                                       |
| 0b0101xxxx | JNZ         | 0b0101'xxxx | Saut relatif de B (PC += B) si A != 0 |
| 0b01100rrr | MOV A, Rx   | 0b0110'0001 | MOV A, R1                             |
| 0b01101rrr | MOV B, Rx   | 0b0111'0010 | MOV B, R2                             |
| 0b0111xrrr | MOV Rx, C   | 0b0111'1000 | MOV R0, C                             |
| 0b10rrrsss | MOV Rx, Ry  | 0b1000'0010 | MOV R0, R2                            |
| 0b11rrrsss | MOV Rx, @Ry | 0b1100'0010 | MOV R0, @(R2, R3)                     |


## Barrel Shifter

Le *barrel shifter* est un circuit logique qui permet de décaler un nombre binaire vers la gauche ou vers la droite. Il est utilisé dans les processeurs pour effectuer des opérations de décalage et de rotation sur les données. Sur un processeur 32 bits, le *barrel shifter* peut effectuer des décalages de 1 à 31 bits en une seule opération, ce qui le rend très efficace pour les opérations de manipulation de bits.

![Barrel Shifter](/assets/images/barrel-shifter.drawio)

Rappelons qu'un décalage des bits vers la gauche correspond à une multiplication par 2, tandis qu'un décalage vers la droite correspond à une division par 2. Les puissance de 2 sont donc très efficaces car elles correspondent à des décalages de bits pouvant être effectués très rapidement par le *barrel shifter*.

Un *barrel shifter* peut également gérer la rotation des bits, c'est-à-dire déplacer les bits d'un mot binaire d'un certain nombre de positions vers la gauche ou vers la droite, en déplaçant les bits qui sortent d'un côté à l'autre du mot. Cela permet de réaliser des opérations de permutation et de cryptographie sur les données.

Dans un processeur ARM, une instruction de décalage peut être incluse directement dans une instruction arithmétique, ce qui permet d'effectuer des opérations de décalage en même temps que des opérations arithmétiques, sans avoir besoin d'une instruction séparée pour le décalage :

```assembly
ADD r0, r1, r2, LSR #5  ; r0 = (r1 + r2) >> 5
```