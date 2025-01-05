# Processeur

## Introduction

Le processeur, c'est le cerveau de l'ordinateur. C'est l'unité centrale de traitement (CPU) qui exécute les instructions et les calculs nécessaires pour faire fonctionner un système informatique. Par analogie à la [Machine de Turing][turingmachine], un processeur est un automate **Turing complet** qui exécute des instructions séquentiellement. Il a besoin pour cela d'une mémoire de travail pour stocker les calculs en cours, et une mémoire de programme qui contient la liste des instructions à exécuter.

Une mémoire fonctionne comme un livre, pour obtenir un contenu (données), on doit l'ouvrir à une page spécifique (adresse). En pratique les mémoires sont adressables par octets. Avec une adresse de 64 bits, on peut adresser 2^64 octets, soit 16 exaoctets, ce qui ne sera pas un problème pour les prochaines décennies.

Depuis le début de l'ère informatique, les processeurs n'ont cessé de se perfectionner pour offrir des performances toujours plus élevées. Les processeurs modernes sont des architectures très complexes que nous ne pourrons approfondir dans ce cours, mais nous allons voir les principaux composants et fonctionnalités qui les caractérisent.

![Puce de processeur](/assets/images/die-finger.png)

## Architecture de bus

Comme évoqué, le processeur intéragit principalement avec de la mémoire. Cette dernière peut être connectée au processeur de différentes manières. On parle de l'architecture de bus. Les deux principales architectures sont l'architecture Von Neumann et l'architecture Harvard. Elle sont deux modèles fondamentaux d'organisation d'un système informatique, qui se distinguent principalement par la façon dont elles gèrent la mémoire et le bus de données.

Chacune a ses avantages et inconvénients, et elles sont utilisées dans différents contextes selon les besoins spécifiques du système.

![Comparaison Havard et Von Neumann](/assets/images/von-neumann-harvard.drawio)

Dans le modèle de John von Neumann (a), les instructions et les données sont stockées dans une mémoire unifiée, et le processeur utilise le même bus pour accéder à la mémoire, qu'il s'agisse d'instructions ou de données. Cela rend l'architecture plus simple et plus flexible, mais peut entraîner des goulets d'étranglement si le processeur doit accéder à la mémoire pour les deux types d'opérations simultanément.

Avec l'architecture de Harvard, les instructions et les données sont stockées dans des mémoires séparées, chacune ayant son propre bus de données. Cela permet au processeur d'accéder simultanément à une instruction et à des données, améliorant les performances globales du système.

De nos jours, les processeurs modernes (x86-64, ARM, etc.) utilisent une architecture hybride qui combine des éléments des deux modèles. Par exemple, les caches de niveau 1 et 2 stockent à la fois les instructions et les données, tandis que la mémoire principale est organisée de manière Von Neumann. Cela permet de combiner les avantages des deux approches pour obtenir des performances optimales.

## Structure interne

Un processeur moderne prend la forme d'une puce de silicium (*die*) d'environ 1 à 2 cm². Elle contient plusieurs milliards de transistors sont organisés en différents blocs fonctionnels pour effectuer les opérations nécessaires au fonctionnement du processeur.

![Diagramme d'un processeur](/assets/images/cpu-diagram.drawio)

La figure ci-dessus représente un diagramme simplifié d'un processeur. Ce dernier se compose de 8 coeurs (ou *cores*) qui sont les unités de calcul principales du processeur. Historiquement les processeurs étaient monoprocesseurs, c'est-à-dire qu'ils ne disposaient que d'un seul coeur. Avec l'évolution de la technologie, et surtout l'impossibilité d'augmenter la fréquence des processeurs, les fabricants ont opté pour des processeurs multi-coeurs. Chaque coeur dispose d'un mémoire ultra rapide appelée **Mémoire cache L2**, c'est l'équivalent de votre mémoire de travail à court terme, celle qui vous permet par exemple de retenir un numéro de téléphone le temps de le composer. Au centre des coeurs, on trouve une autre mémoire cache appelée **Mémoire cache L3** qui est partagée par tous les coeurs, elle permet de faciliter l'accès aux données partagées entre plusieurs processus. En haut à gauche, il y a deux contrôleurs de mémoire RAM connecté vers l'extérieur sur les barettes de mémoire.
Le DMI (Direct Media Interface chez Intel) ou QPI (QuickPath Interconnect chez Intel) est un bus qui est destiné à connecter le processeur au **chipset** qui gère les périphériques externes (USB, SATA, Ethernet, etc.). Le bus PCIe (Peripheral Component Interconnect Express) est un bus qui permet de connecter des cartes d'extension comme des cartes graphiques ou des dispositifs de stockage NVMe. Enfin, souvent le processeur dispose d'une ou plusieurs connectivité USB 3.

Lorsque vous démarrez un programme, le système d'exploitation charge le programme en mémoire, puis choisit un coeur pour exécuter le programme. Un processeur à 8 coeurs peut donc exécuter jusqu'à 8 programmes en parallèle. Dans certaines conditions, on peut avoir jusqu'à 16 programmes en parallèle si le processeur dispose de l'hyper-threading. L'hyper-threading est une technologie qui permet à un coeur de simuler deux coeurs logiques, ce qui permet de mieux exploiter les ressources du processeur.

### Mémoire cache

La mémoire cache est un élément clé de la performance d'un processeur. Elle permet de stocker temporairement les données les plus fréquemment utilisées par le processeur, ce qui permet d'accélérer l'accès à ces données et d'améliorer les performances globales du système. Rappelez-vous que la vitesse de la lumière est limitée. Avec une autoroute de 20 à 30 cm de distance entre le processeur et la mémoire, plus les payages, les bouchons et les accidents, le processeur à le temps d'exécuter entre 50 et 200 opérations avant qu'une donnée ne puisse être écrite ou lue depuis la RAM. La mémoire cache est donc une mémoire tampon, placée le plus proche possible du processeur (sur la même puce). Un processeur moderne dispose de plusieurs niveau de cache.

**L1**

: Elle est très rapide, mais minuscule (quelques Kio). Elle est divisée en deux parties, une pour les instructions et une pour les données (selon le modèle de Harvard). Chaque coeur dispose de sa propre mémoire cache L1.


**L2**

: Elle est plus grande (quelques Mio) et plus lente que la L1. Elle est propre à chaque coeur mais contient les instructions et les données mélangées (selon le modèle de Von Neumann).

**L3**

: Elle est encore plus grande (quelques dizaines de Mio) et plus lente que la L2. Elle est partagée par tous les coeurs et contient les instructions et les données mélangées.

Voici sur la figure suivante un exemple de hiérarchie de mémoire cache pour un processeur moderne. Plus l'accès est rapide, plus la mémoire est petite et plus elle est proche du processeur.

![Hiérarchie des mémoires cache](/assets/images/cache-hierarchy.drawio)

Lorsque l'on cherche des performances, même si on ne connait pas bien le fonctionnement interne d'un processeur, il est important de comprendre que la mémoire cache joue un rôle crucial car un programme d'apparence bien écrit, mais qui ne tient pas compte des limites de la mémoire cache, peut être des dizaines de fois plus lent qu'un programme qui les prend en compte. Alors que faut-il savoir ?

Une mémoire cache est une mémoire temporaire, c'est votre pense bête qui permet de vous rappeler des fleurs du jardin de votre grand-mère. Sans sortir de chez vous vous pouvez savoir que de magnifiques renoncules poussent à l'ombre du cerisier. Cela reste vrai, pour autant qu'aucun mouton ne les ait mangées. Sans se rendre sur place, impossible de le savoir, et votre pense bête ne vous est ici d'aucune utilité. Un autre problème c'est que votre pense bête ne comporte que quelques pages, alors que le jardin de votre grand-mère c'est Versailles, vous ne pouvez pas tout noter.

Ce qu'il faut retenir, c'est qu'une mémoire cache ne reste utile que pour autant que les copies des données qu'elle contient soient à jour avec la mémoire principale. Si un autre programme ou un autre coeur processeur modifie les données en mémoire, la mémoire cache devra être mise à jour. De la même manière, si vous voulez accéder à une donnée que vous n'avez aps en cache, vous devez la charger depuis la mémoire principale, et remplacer une donnée existante dans la mémoire cache (car cette mémoire est petite). En termes technique, ces différents soucis ont des noms :

**Cohérence de cache**

: C'est le problème de s'assurer que les copies des données en cache sont à jour avec la mémoire principale. Il existe plusieurs protocoles de cohérence de cache, comme le protocole MESI (Modified, Exclusive, Shared, Invalid) qui permet de gérer les accès concurrents aux données.

**Consistance de cache**

: C'est le problème de s'assurer que les données en cache sont cohérentes entre elles. Par exemple, si un coeur modifie une donnée, les autres coeurs doivent être informés de ce changement pour éviter les incohérences.

Un programme qui intéragit avec la mémoire cache peut rencontrer deux cas de figures :

**Cache miss**

: C'est le problème de ne pas trouver une donnée en cache, ce qui oblige le processeur à la charger depuis la mémoire principale. Cela peut entraîner un ralentissement des performances, car l'accès à la mémoire principale est beaucoup plus lent que l'accès à la mémoire cache.

**Cache hit**

: C'est le contraire d'un cache miss, c'est-à-dire trouver une donnée en cache. Cela permet d'accélérer l'accès à la donnée, car elle est déjà stockée dans la mémoire cache (pour le coup c'est une bonne chose).

Si une donnée est accessible depuis le cache L1, elle peut être directement chargée dans le processeur en un seul cycle d'horloge. Si elle est accessible depuis le cache L2, cela prendra quelques cycles d'horloge supplémentaires. Voici un tableau récapitulatif des temps d'accès typiques pour chaque niveau de cache :

Table: Temps d'accès typiques pour chaque niveau de cache

| Niveau de cache | Temps d'accès (cycles d'horloge) | Taille de mémoire |
| --------------- | -------------------------------- | ----------------- |
| L1              | 4-5                              | 32 Kio            |
| L2              | 10-20                            | 256 Kio à 1 Mio   |
| L3              | 30-60                            | 2 Mio à 64 Mio    |
| RAM             | 100-200                          | 8 Gio à 64 Gio    |

La mémoire cache fonctionne sur le principe de la localité. On note deux types de localité :

**Localité temporelle**

: C'est le principe selon lequel si une donnée a été accédée récemment, il y a de fortes chances qu'elle soit accédée à nouveau dans un proche avenir. C'est pourquoi les données récemment accédées sont stockées en cache pour accélérer les accès futurs.

**Localité spatiale**

: C'est le principe selon lequel si une donnée a été accédée, il y a de fortes chances que les données voisines soient également accédées. C'est pourquoi les données sont stockées en blocs contigus en cache pour améliorer les performances.

Une donnée qui n'a pas été accédée depuis longtemps à de forte chance de ne plus être disponible dans le cache. De même, une donnée qui est très éloignée en mémoire d'une donnée récemment accédée a de forte chance de ne pas être en cache non plus. C'est pourquoi il est important de structurer son programme pour exploiter au mieux la localité temporelle et spatiale.

Un autre point fondamental à retenir est que la mémoire cache fonctionne sur le principe des **ligne de cache**. Une ligne de cache contient typiquement 64 octets de données, généralement contigus en mémoire. Lorsqu'une donnée est chargée depuis la RAM, le système va également charger les données voisines dans la même ligne de cache. Cela permet d'améliorer les performances en cas d'accès à des données voisines. En terme de vitesse de transfert c'est avantageux. Si vous faites venir un camion de babiolles de Zürich à Lausanne, cela prendra environ le même temps que que de faire venir 10 camions, ce qui limite c'est la vitesse de transfert.

Néanmoins ce mécanisme pose un problème. Si une donnée d'une ligne de cache est invalidée, c'est toute la ligne qui sera invalidée. Donc pour un byte de donnée modifié, c'est 64 bytes qui devront être rechargés depuis la mémoire principale.

Pour mieux comprendre ces limitations, prenons un exemple en C. Il s'agit d'une matrice de 100'000 x 100'000 éléments ou nous souhaitons calculer la somme de tous les éléments. On pourrait écrire le programme comme ceci :

```c
#include <stdio.h>

#define N 100'000

int matrix[N][N];

int main() {
    long long int sum = 0;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            sum += matrix[i][j];
        }
    }
    printf("Sum: %lld\n", sum);
}
```

Chaque ligne de la matrice consiste en environ 390 kib. Une ligne de cache L1 peut contenir 64 octets, soit 16 entiers de 4 octets. Au début du programme, lorsque l'on accède à `matrix[0][0]`, le processeur demande à L1 qui ne connait pas la donnée, qui demande à L2, qui n'a pas souvenir de cette valeur, qui demande à L3, qui décide enfin d'aller chercher l'information à la source en RAM. Au passage il peut détecter que les données voisines sont également utiles et il précharge plusieurs lignes de cache dans L3, L2 et L1. Si bien que les accès suivants sont beaucoup plus rapide.

Maintenant considérons le même programme mais avec une petite modification :

```c
sum += matrix[j][i];
```

On a inversé `i` et `j`. Au lieu de parcourir la matrice linéairement en mémoire, à chaque lecture on fait un saut de 390 kib. Cela signifie que les données voisines préchargées par le cache ne sont plus utiles. A chaque lecture, le cache doit aller chercher la donnée en RAM.

La première version du programme est environ 10 à 20 fois plus rapide que la seconde. Cela montre l'importance de la localité spatiale dans la performance d'un programme.

### Pipeline

Un processeur moderne utilise une technique appelée **pipeline** pour accélérer l'exécution des instructions. Le pipeline est une série d'étapes que chaque instruction doit traverser pour être exécutée. Chaque étape du pipeline effectue une partie de l'exécution de l'instruction, ce qui permet au processeur d'exécuter plusieurs instructions en parallèle. Un pipeline typique comporte 5 étapes :

1. **Fetch** : L'instruction est chargée depuis la mémoire.
2. **Decode** : L'instruction est décodée pour déterminer l'opération à effectuer.
3. **Execute** : L'opération est exécutée.
4. **Memory** : Les données sont lues ou écrites en mémoire.
5. **Write-back** : Le résultat est écrit dans le registre de destination.

Sur la figure suivante, un exemple d'un pipeline simplifié pour 4 et 7 niveaux est illustré.

![Aperçu d'un pipeline](/assets/images/pipeline.drawio)

Les processeurs modernes utilisent des pipelines beaucoup plus complexes à environ 20 niveaux.

Pour mieux illustrer le concept, imaginons une cuisine dans un grand restaurant.

1. Le serveur va chercher la commande
2. Le chef de cuisine décode la commande
3. Un commis prépare les ingrédients
4. Un autre commis peluche des légumes
5. Un autre commis prépare la viande
6. Un autre dresse le plat
7. Un serveur apporte le plat à la table

À chaque intervalle temporel, un nouveau plat est préparé. Le serveur peut chercher une commande par *cycle* (temps nécessaire pour servir un plat). L'avantage c'est que pendant que le chef decode la commande $k$, un commis prépare les ingrédients du plat $k-1$, un autre peluche les légumes du plat $k-2$ et le serveur apporte le plat $k-5$.

Imaginez maintenant que le chef de cuisine se trompe de commande, il doit tout arrêter et recommencer. C'est ce qu'on appelle un *pipeline stall*. Cela arrive lorsque le processeur ne peut pas continuer à exécuter les instructions suivantes car il attend le résultat d'une instruction précédente. Cela peut se produire lorsqu'une instruction dépend d'une autre instruction qui n'a pas encore été exécutée, ou lorsqu'une instruction accède à une donnée qui n'est pas encore disponible en mémoire.

En pratique cela arrive à chaque embranchement `if`, `for`, `while`... car ces évènements sont imprévisibles. Tant que le processeur ne sait pas le résultat d'une condition, il ne sait pas s'il doit préparer les instructions qui suivent directement ou celles qui suivent le `else`. Durant ces évènements le *pipeline* est vidé et il doit être rechargé. Avec un *pipeline* à 20 niveaux, c'est 20 cycles d'horloge qui sont perdus.

Dans le code suivant, l'instruction `if` pourrait prendrait soit `1` soit `20` cycles d'horloge une fois sur deux.

```c
if (rand() % 2 == 0) {
    printf("a");
} else {
    printf("b");
}
```

Ceci est vrai sur de petites architectures. Sur des processeurs modernes, un processeur dispose d'un prédicteur d'embranchement qui permet de prédire le résultat d'une condition. Si le prédicteur se trompe, le processeur doit vider le pipeline et le recharger, ce qui peut entraîner un ralentissement des performances. Dans le cas de notre exemple, le processeur ne peut pas prédire le résultat de `rand() % 2`, donc l'exécution est peu performante car un choix sur deux mène à une rupture de pipeline.

Les processeurs modernes sont très efficaces pour prédire les prochains embranchements basé sur des motifs observables dans les décisions passées. Prenons l'exemple suivant.

```c
while(*(ptr++) != '\0') {
    // do something
}
```

Le processeur peut prédire qu'il y a plus de chance que la boucle continue plutôt qu'elle s'arrête au prochain cycle. Il privilégiera la branche `true` et préchargera les instructions suivantes. Le prédicteur se trompera à la fin de la chaîne de caractères, et il devra vider le pipeline, mais cela n'arrivera qu'une fois.

Sur de petits microcontrôleurs ou des architectures plus anciennes, il n'y a pas de prédicteur d'embranchement, et donc les décisions (p.ex. `if`) sont très coûteuses en termes de performances, on privilégiera alors une architecture de programme qui minimise la prise de décision.

### Coeur

Le coeur du processeur est un monstre de technologies. Il est composé de plusieurs unités fonctionnelles qui travaillent ensemble pour exécuter les instructions.

![Die shot d'un coeur de processeur de 2009](/assets/images/die.drawio)

L'objectif ici n'est pas d'entrer dans le détail de chaque unité, mais d'avoir un aperçu général du fonctionnement. La figure suivante représente la structure interne d'un processeur moderne.

![Diagramme d'un coeur de processeur](/assets/images/cpu-core-diagram2.drawio)

On voit le cache L3 partagé par tous les coeurs, en dehors de ce dernier. Le cache L2 est propre à chaque coeur et communique par un bus à 256 bit avec le cache L1. Le cache L1 est divisé en deux parties, une pour les instructions et une pour les données.

Prenons le chemin d'une instruction. Une fois chargée dans L1, l'unité de *Fetch* s'occupe de charger l'instruction dans le pipeline. L'unité de *Decode* décode l'instruction pour déterminer l'opération à effectuer. Dans un processeur moderne, une instruction assembleur est en réalité scindée en plusieurs micro-opérations qui sont exécutées par les différentes unités fonctionnelles du processeur. Les instructions font souvent références à des registres du processeur, qui sont des emplacements de mémoire ultra-rapide utilisés pour stocker des données temporaires. Ces registres sont renommés (rebaptisés) pour accroître les performances de calculs. Aussi, les micro opérations sont réagencées pour optimiser l'utilisation des unités fonctionnelles. Par exemple, si une instruction doit attendre le résultat d'une autre instruction, le processeur peut exécuter une autre instruction en attendant. C'est ce qu'on appelle l'exécution **hors ordre**.

Ces micro-opérations une fois établies sont placées dans une file d'attente pour ensuite être transmises aux unités fonctionnelles via l'*issue port*.

On distingue généralement les unités fonctionnelles suivantes :

- **Unité arithmétique et logique (ALU)** : Elle effectue les opérations arithmétiques et logiques sur des entiers.
- **Unité de calcul en virgule flottante (FPU)** : Elle effectue les opérations arithmétiques sur des nombres à virgule flottante.
- **Unité de calcul d'adresse (AGU)** : Elle calcule les adresses mémoire pour les accès en lecture et en écriture.
- **Unité de branchement (Branch Unit)** : Elle gère les instructions de branchement (if, for, while, etc.).

## Registres

Traditionnellement, dans un processeur, l'utilisateur dispose de registres de travail. Ce sont des emplacements de mémoire ultra-rapide utilisés pour stocker des données temporaires. Les registres sont des emplacements de mémoire ultra-rapide utilisés pour stocker des données temporaires. Ils sont utilisés pour stocker les données et les résultats intermédiaires des calculs effectués par le processeur. Les registres sont des emplacements de mémoire ultra-rapide utilisés pour stocker des données temporaires. Ils sont utilisés pour stocker les données et les résultats intermédiaires des calculs effectués par le processeur.

Imaginons un processeur très primitif. Il ne peut faire cinq choses :

- Additionner deux registres
- Soustraire deux registres
- Déplacer une valeur d'un registre à un autre
- Sauter à une autre instruction
- Sauter à une autre instruction si un registre est nul

La programmation est impérative, les instructions sont exécutées séquentiellement. Pour déplacer une valeur du registre `R0` au registre `R1`, on écrirait `MOV R1, R0`. Pour ajouter deux valeurs, on écrirait `ADD R2, R0, R1`. Pour sauter à une autre instruction si un registre est nul, on écrirait `JNZ R0, 10` (sauter à l'instruction 10 si `R0` n'est pas nul).

Tenant compte de ces précisions, l'algorithme serait alors le suivant, où le calcul du reste de la division est calculé par des soustractions successives :

```nasm
01 MOV R0, 30   # a
02 MOV R1, 42   # b
03 MOV R2, R1   # Met b dans R2
04 JNZ R2, 6    # Si b vaut 0 alors saute à l'instruction 6
05 JMP 16       # Saute à l'instruction 16
06 MOV R3, R0   # Met a dans R3
07 MOV R4, 0    # Met 0 dans R4
08 SUB R3, R1   # Soustrait b à a
09 JNZ R3, 11   # Si le résultat est nul, saute à l'instruction 11
10 JMP 13       # Saute à l'instruction 13
11 ADD R4, 1    # Incrémente le reste de la division
12 JMP 8        # Saute à l'instruction 8 (boucle)
13 MOV R0, R1   # Met b dans a
14 MOV R1, R3   # Met le reste de la division dans b
15 JMP 3        # Saute à l'instruction 3 (boucle)
16 NOP          # Fin du programme
```

Dans un processeur moderne, il y a également des registres mais qui ont des noms différents. Par exemple, dans un processeur x86-64, on a les registres suivants :

- **Registres généraux** : RAX, RBX, RCX, RDX, RSI, RDI, RBP, RSP, R8-R15
- **Registres de segment** : CS, DS, ES, FS, GS, SS
- **Registres d'index** : RSI, RDI, RBP, RSP
- **Registres de pointeur** : RIP, RFLAGS
- **Registres de contrôle** : CR0-CR4
- **Registres SIMD** : XMM0-XMM15, YMM0-YMM15, ZMM0-ZMM31

Depuis longtemps, les processeurs sont capables d'exécuter plusieurs instructions en parallèle. Cela signifie que les registres sont partagés entre les différentes instructions. Par exemple, si une instruction veut ajouter deux valeurs, elle doit attendre que les registres soient disponibles et c'est un goulet d'etranglement. Pour éviter cela, les processeurs modernes utilisent une technique appelée **renommage des registres**. Les registres que l'on utiliise pour programmer n'existe pas réellement dans le processeur mais ils sont associés à des registres physiques. Cela permet d'éviter les conflits entre instructions qui voudraient utiliser le même registre en même temps.

On appelle ces architectures des architectures **hors-ordre** superscalaires. Cela signifie que les instructions sont exécutées dans l'ordre dans lequel elles sont décodées, mais les résultats peuvent être renvoyés dans un ordre différent. Cela signifie que les instructions peuvent être exécutées dans un ordre différent de celui dans lequel elles apparaissent dans le code source.

Les processeurs comme les Intel Core i7/i9, AMD Ryzen, etc. utilisent ce concept.

Voici comment cela fonctionne :

1. Lorsqu'une instruction est décodée, le processeur associe chaque registre architectural à un registre physique. Le processeur gère une table de renommage qui fait correspondre chaque registre architectural à un registre physique.
2. Exécution hors-ordre : Les instructions sont exécutées dans l'ordre dans lequel elles sont décodées, mais les résultats peuvent être renvoyés dans un ordre différent. Cela signifie que les instructions peuvent être exécutées dans un ordre différent de celui dans lequel elles apparaissent dans le code source.
3. Retirement (retrait) : une fois que les instructions sont exécutées et validées, les résultats des registres physiques sont reflétés dans les registres architecturaux lors de l'étape de retrait (retirement). À ce stade, le programmeur ou le système voit les registres comme étant mis à jour dans l'ordre correct.

Les éléments clés de ce concept sont le *Reorder Buffer* et le *Retirement Unit*. Le *Reorder Buffer (ROB)* permet au processeur de garder une trace des instructions en cours d'exécution hors-ordre et il s'assure que les instructions sont retirées (c'est-à-dire, finalisées et appliquées aux registres architecturaux) dans le bon ordre, tel que prévu par le programmeur. Au moment du retrait, via le ROB, les résultats des registres physiques sont copiés vers les registres architecturaux visibles par le programmeur. C'est ce moment-là où, du point de vue du programmeur, le registre RAX ou RBX est mis à jour.

## L'assembleur

Avant le C, le Fortran ou le Cobol, il était possible de programmer directement en assembleur. L'assembleur est le langage du plus bas niveau que l'on puisse utiliser pour programmer un ordinateur. Il se compose des instructions primitives que le processeur peut exécuter directement. Ces instructions primitives sont généralement très simples, comme ajouter deux nombres, déplacer des données d'un emplacement à un autre, ou effectuer des opérations logiques sur des bits.

Nos processeurs modernes étant déjà très complexes, les instructions de base de l'assembleur sont également complexes. L'architecture X86-64 dispose d'environ 200 instructions différentes. Charger une valeur à une adresse mémoire contenue dans le registre `RBX` dans le registre `RAX` s'écrirait `MOV RAX, [RBX]`, et cette ligne d'assembleur peut être traduite en langage machine `488B03`.

```txt
4  Utilisation des registres étendus (64 bits)
8  Utilisation des registres hauts (RAX, RBX)
8B Instruction MOV
03 ModRM qu'il faut décortiquer:
   0b00  Adressage indirect
   0b000 Registre 0 (RAX)
   0b011 Registre 3 (RBX)
```

Ecrire un programme en langage machine est compliqué et fastidieux. C'est pourquoi on utilise un langage textuel appelé assembleur qui peut facilement être converti en langage machine.

Pour mieux comprendre, admettons que l'on souhaite réécrire notre programme `hello.c` mais en assembleur (`hello.s`). Ici, il ne faut pas imaginer accéder directement à l'écran pour écrire du texte. Il faut passer par le système d'exploitation. Pour cela, on utilise les appels systèmes. C'est exactement ce que fait `printf`. Vous noterez la présence de nombreux commentaires, il est courant d'ajouter des commentaires pour mieux expliquer le code assembleur qui est souvent, par sa nature assez cryptique :

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
    xor rdi, rdi            ; Code de sortie 0 (plus rapide que mov rdi, 0)
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

## Fonctionnalités internes

### Protection ring

Les *protection rings* (ou anneaux de protection) sont un mécanisme de sécurité utilisé dans l'architecture des processeurs, principalement dans les systèmes d'exploitation modernes, pour contrôler l'accès aux ressources du système par différents types de code (comme les applications ou les composants du système d'exploitation).

L'idée des anneaux de protection repose sur la séparation des niveaux de privilège ou de contrôle en plusieurs couches. Chaque couche, ou ring (anneau), est un niveau de privilège qui détermine ce qu’un programme ou une instruction peut faire. Dans l'architecture x86 d'Intel, il y a généralement quatre anneaux (de 0 à 3), bien que les systèmes d'exploitation modernes n’utilisent souvent que deux de ces niveaux (Ring 0 et Ring 3).

![Anneaux de protection](/assets/images/protection-rings.drawio)

Le ring 0 correspond au noyau (kernel) du système d'exploitation, qui a accès à toutes les ressources matérielles de l'ordinateur. Il peut exécuter n'importe quelle instruction, accéder à la mémoire directement, et gérer le matériel sans restriction. On parle souvent de mode superviseur ou mode noyau pour désigner les opérations effectuées dans cet anneau. C’est le niveau le plus privilégié.

Les niveaux intermédiaires 1 et 2 peuvent être utilisés par certains systèmes pour les pilotes ou des services du système qui ont besoin d'un accès contrôlé aux ressources, mais ne nécessitent pas le même niveau de privilège que le noyau. Toutefois, la plupart des systèmes d'exploitation modernes ne les utilisent pas directement.

Enfin, le niveau 3 est réservé aux applications utilisateur. Il s’agit du mode utilisateur (user mode), dans lequel les programmes n’ont pas un accès direct au matériel ou à la mémoire, et doivent passer par des appels système pour demander des services au noyau. En cas de violation des règles (comme essayer d’accéder directement au matériel), une exception ou une erreur est générée, et le programme est bloqué.

### Mémoire cache

Cache L1, L2, L3, Le cache L1 est apparu dans les années 1980, le cache L2 est apparu dans les années 1990 (d'abord externe, puis intégré), et le cache L3 est devenu standard dans les années 2000.

### FPU

Précision simple, double, étendue (Extended Precision),  Apparue avec les coprocesseurs mathématiques (x87 FPU), et les extensions SSE ont introduit la gestion des calculs en virgule flottante sur des registres 128-bit.

### Virtualisation (Intel VT-x, AMD-V)

Support pour l'exécution de machines virtuelles directement via le matériel, introduit dans les années 2000.

### Réduction de consommation

(Intel SpeedStep, AMD Cool'n'Quiet)** : Ces technologies permettent au processeur de diminuer sa consommation en adaptant dynamiquement sa fréquence et son voltage.

### Pipeline

Pipelines avec plusieurs niveaux (Netburst), La microarchitecture Netburst d'Intel Pentium 4 introduit des pipelines de plus de 30 niveaux pour viser des fréquences élevées, bien que cela ait compromis les performances générales.

### Micro-opérations et scheduling

Les architectures modernes décomposent les instructions complexes en micro-opérations (Intel Core) pour mieux les planifier via un scheduler intégré.

### ALU

L'*Arithmetic Logic Unit* (ALU) est l'une des principales composantes d'un processeur. C'est l'unité qui effectue les opérations arithmétiques et logiques sur les données. L'ALU est capable d'effectuer des opérations telles que l'addition, la soustraction, la multiplication, la division, les opérations logiques (ET, OU, NON, XOR), les décalages de bits, etc.

### Barrel Shifter

Le *barrel shifter* est un circuit logique qui permet de décaler un nombre binaire vers la gauche ou vers la droite. Il est utilisé dans les processeurs pour effectuer des opérations de décalage et de rotation sur les données. Sur un processeur 32 bits, le *barrel shifter* peut effectuer des décalages de 1 à 31 bits en une seule opération, ce qui le rend très efficace pour les opérations de manipulation de bits.

![Barrel Shifter](/assets/images/barrel-shifter.drawio)

Rappelons qu'un décalage des bits vers la gauche correspond à une multiplication par 2, tandis qu'un décalage vers la droite correspond à une division par 2. Les puissance de 2 sont donc très efficaces car elles correspondent à des décalages de bits pouvant être effectués très rapidement par le *barrel shifter*.

Un *barrel shifter* peut également gérer la rotation des bits, c'est-à-dire déplacer les bits d'un mot binaire d'un certain nombre de positions vers la gauche ou vers la droite, en déplaçant les bits qui sortent d'un côté à l'autre du mot. Cela permet de réaliser des opérations de permutation et de cryptographie sur les données.

Dans un processeur ARM, une instruction de décalage peut être incluse directement dans une instruction arithmétique, ce qui permet d'effectuer des opérations de décalage en même temps que des opérations arithmétiques, sans avoir besoin d'une instruction séparée pour le décalage :

```assembly
ADD r0, r1, r2, LSR #5  ; r0 = (r1 + r2) >> 5
```

### SSE et AVX

Les instructions SSE (*Streaming SIMD Extensions*) sont une extension de l'architecture x86 introduite par Intel en 1999 avec les processeurs Pentium III. Elles permettent d'effectuer des opérations vectorielles sur des registres de 128 bits (`xmm`), ce qui améliore les performances pour les calculs intensifs en parallèle.

Les instructions AVX (*Advanced Vector Extensions*) sont une extension de l'architecture x86 introduite par Intel en 2011 avec les processeurs Sandy Bridge. Elles permettent d'effectuer des opérations vectorielles sur des registres de 256 bits (`ymm`), et avec l'AVX-512 des registres de 512 bits (`zmm`), ce qui améliore les performances pour les calculs intensifs en parallèle.

Le SIMD (*Single Instruction, Multiple Data*) est une technique de parallélisme de données qui permet d'effectuer la même opération sur plusieurs données simultanément.

Les applications possibles sont nombreuses: filtre d'image, mélange de couleurs, compression d'image, traitement audio, multiplication de matrices, etc.

Dans gcc, on peut utiliser les options `-msse` ou `-msse2` pour activer les instructions SSE, alternativement on peut utiliser `-march=skylake` pour activer les instructions SIMD spécifiques à l'architecture du processeur.

```c
void compute(const float * restrict a,
             const float * restrict b, float * restrict c)
{
    for (int i = 0; i < 8; i++)
        c[i] = a[i] + b[i];
}
```

Ce code compile en donnant l'assembleur suivant:

```nasm
compute:
  vmovups ymm0, ymmword ptr [rdi]
  vaddps  ymm0, ymm0, ymmword ptr [rsi]
  vmovups ymmword ptr [rdx], ymm0
  vzeroupper
  ret
```

Notons ici que le mot clé `restrict` est indispensable pour indiquer au compilateur que les pointeurs ne se chevauchent pas.

L'instruction `vmovups` charge un vecteur de 8 floats (format spécifié avec `ymmword`) dans le registre `ymm0`. L'instruction `vaddps` additionne les éléments d'un vecteur de nombre flottants (`ps` pour *packed single-precision floating-point values*). `ymm0` contient déjà les valeurs de `a`, on ajoute donc les valeurs de `b`. Enfin, l'instruction `vmovups` stocke le résultat dans le tableau `c`. L'instruction `vzeroupper` est utilisée pour réinitialiser les registres AVX supérieurs.

Avant les architectures superscalaires, le code assembleur généré aurait été probablement similaire à ceci :

```nasm
compute:
  fld DWORD PTR [rdi]
  fadd DWORD PTR [rsi]
  fstp DWORD PTR [rdx]

  fld DWORD PTR [rdi+4]
  fadd DWORD PTR [rsi+4]
  fstp DWORD PTR [rdx+4]

  fld DWORD PTR [rdi+8]
  fadd DWORD PTR [rsi+8]
  fstp DWORD PTR [rdx+8]

  fld DWORD PTR [rdi+12]
  fadd DWORD PTR [rsi+12]
  fstp DWORD PTR [rdx+12]

  ; Répéter pour les 4 autres éléments...

  ret
```

La comparaison des performances est évidente, les instructions SIMD permettent de traiter 8 éléments en une seule instruction, tandis que les instructions FPU ne peuvent traiter qu'un seul élément à la fois. Il faut environ 7 cycles d'horloge avec SSE/AVX contre 60 à 70 cycles avec FPU.


## Compatibilité

Nous avons vu, les processeurs évoluent au fil des générations le SS2 a été introduit avec le Pentium III, l'AVX 256 bits avec Sandy Bridge, l'AVX 512 bits avec Skylake, etc. Cela pose un problème de compatibilité car si vous compilez avec `gcc` votre programme aujourd'hui, il ne fonctionnera probablement pas sur une ancienne architecture, pourtant c'est un exécutable x86-64 en format ELF.

Par défaut, `gcc` compile pour une architecture générique, c'est à dire qu'il fait un compromis entre les différentes architectures pour garantir une certaine compatibilité. Pour compiler pour une architecture spécifique, il faut utiliser l'option `-march`:

```bash
gcc -march=skylake main.c
```

Notons que si ce programme est executé sur un processeur plus ancien, il ne fonctionnera pas, le processeur ne comprendra pas certaines instructions et générera une exception matérielle (généralement *Illegal Instruction*). Cela se traduit par le signal `SIGILL` envoyé à un processus lorsqu'il tente d'exécuter une instruction illégale. Sans gestion de cette exception, le processus sera arrêté avec un message d'erreur :

```text
Illegal instruction (core dumped)
```

Il y a donc un compromis à faire entre la performance et la compatibilité. Si vous développez un logiciel grand public, vous voudrez probablement le rendre compatible avec un maximum de processeurs, mais si vous développez un logiciel pour un environnement spécifique, vous pouvez optimiser pour une architecture particulière. C'est pour cette raison que sous Linux/Unix il est courant de compiler ses logiciels soi-même pour obtenir les meilleures performances, c'est notament le cas de la distribution Gentoo dans lequel l'utilisateur doit compiler la plupart des logiciels (ce qui est un enfer pour les non-geeks).

Lorsque vous télécharge un binaire, par exemple Gimp, il sera compilé pour une architecture générique, ce qui garantit une certaine compatibilité, mais il ne sera pas optimisé pour votre processeur. Si vous voulez obtenir les meilleures performances, vous devrez le compiler vous-même.

Sous Windows, cette culture de la compilation est moins répandue, les logiciels sont généralement distribués sous forme de binaire, et il est rare de trouver des versions optimisées pour une architecture spécifique et de nombreux logiciels sont très peu optimisés.

## Extensions x86

Effectivement, il existe d'autres extensions pour l'architecture x86, notamment **CLMUL**, **RDRAND**, et **TXT**. Voici la table mise à jour avec ces extensions et d'autres supplémentaires :

Table: Résumé des extensions x86 les plus courantes

| Extension | Description                                                                                                                                                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AES-NI    | Instructions matérielles pour accélérer les opérations de chiffrement et de déchiffrement AES.                                                                                                                                              |
| AVX       | Advanced Vector Extensions, extension SIMD pour améliorer les performances des calculs flottants et vectoriels, notamment dans les applications scientifiques et multimédia.                                                                |
| AVX2      | Advanced Vector Extensions 2, amélioration de l'AVX avec prise en charge des entiers 256 bits et optimisation des opérations sur des données vectorielles.                                                                                  |
| AVX-512   | Advanced Vector Extensions 512 bits, extension SIMD avec des registres de 512 bits pour des performances accrues dans les calculs intensifs, utilisé dans les applications scientifiques, cryptographiques et de machine learning.          |
| BMI1/BMI2 | Bit Manipulation Instructions, ensembles d'instructions pour la manipulation efficace des bits et des entiers, utiles dans des opérations comme le hachage ou la compression de données.                                                    |
| CLMUL     | Carry-less Multiplication, instructions pour la multiplication sans retenue, souvent utilisées dans les algorithmes cryptographiques, notamment pour l'implémentation de Galois/Counter Mode (GCM).                                         |
| FMA3      | Fused Multiply-Add 3, permet de réaliser une multiplication suivie d'une addition en une seule instruction, réduisant le temps de calcul et améliorant la précision.                                                                        |
| FMA4      | Fused Multiply-Add 4, similaire au FMA3 mais avec une légère différence dans la gestion des opérandes, utilisé principalement par AMD.                                                                                                      |
| MMX       | MultiMedia eXtensions, première extension SIMD d'Intel conçue pour améliorer les performances des applications multimédia telles que le traitement d'images, l'audio et la vidéo.                                                           |
| RDRAND    | Random Number Generator, instruction pour générer des nombres aléatoires de manière matérielle, utile dans les applications cryptographiques et de sécurité.                                                                                |
| RDSEED    | Random Seed Generator, similaire à RDRAND, mais conçu pour générer des graines (seeds) pour des générateurs de nombres aléatoires avec des propriétés cryptographiques renforcées.                                                          |
| SSE       | Streaming SIMD Extensions, extension SIMD améliorant les performances des calculs en virgule flottante, notamment dans les applications graphiques et de jeu.                                                                               |
| SSE2      | Streaming SIMD Extensions 2, extension de SSE avec support des entiers 128 bits et des nombres en virgule flottante double précision.                                                                                                       |
| SSE3      | Streaming SIMD Extensions 3, extension de SSE2 avec des instructions supplémentaires pour améliorer les performances en virgule flottante et pour le multithreading.                                                                        |
| SSE4      | Streaming SIMD Extensions 4, extension de SSE3, optimisée pour les calculs complexes, notamment les opérations de traitement d'images et de vidéo.                                                                                          |
| SSE4.1    | Streaming SIMD Extensions 4.1, sous-ensemble de SSE4, avec des instructions supplémentaires pour la manipulation de données et la gestion de texte.                                                                                         |
| SSE4.2    | Streaming SIMD Extensions 4.2, ajoute des instructions pour l'accélération des comparaisons de chaînes de caractères, utile dans les applications de traitement de texte et de recherche.                                                   |
| SSSE3     | Supplemental Streaming SIMD Extensions 3, améliore SSE3 avec des instructions supplémentaires pour la manipulation de données packées, utilisées dans les algorithmes de cryptographie et de hachage.                                       |
| TXT       | Trusted Execution Technology, technologie visant à assurer une exécution sécurisée en garantissant que le matériel, le firmware et les logiciels utilisés au démarrage sont intègres et sécurisés.                                          |
| TSX       | Transactional Synchronization Extensions, extension pour améliorer les performances du parallélisme matériel et logiciel en permettant la synchronisation transactionnelle, réduisant les conflits dans les accès concurrents à la mémoire. |
| VNNI      | Vector Neural Network Instructions, extension SIMD pour accélérer les réseaux neuronaux et les calculs d'inférence en intelligence artificielle, notamment pour le traitement de données de machine learning.                               |

## Principales architectures

Les différentes architectures sont très nombreuses et évoluent rapidement, néanmoins les compilateurs restent compatibles avec les anciennes architectures. Voici une liste des principales architectures x86-64 et de leurs principales caractéristiques ainsi que les options `-march` associées pour `gcc`. Elles peuvent être utiles pour optimiser un programme pour une architecture spécifique.

Nous citerons ici les deux grandes familles de processeurs, Intel et AMD, ainsi que quelques autres architectures.

### Intel

Table: Principales architectures Intel

| Architecture    | `-march`         | Année | Fonctionnalités                                            |
| --------------- | ---------------- | ----- | ---------------------------------------------------------- |
| Nocona          | `nocona`         | 2004  | Première architecture x86-64 d'Intel, supporte SSE3        |
| Core 2          | `core2`          | 2006  | Supporte SSSE3, architecture Core                          |
| Nehalem         | `nehalem`        | 2008  | SSE4.2, Hyper-Threading, intégration du contrôleur mémoire |
| Westmere        | `westmere`       | 2010  | AES-NI, PCLMULQDQ (opérations cryptographiques)            |
| Sandy Bridge    | `sandybridge`    | 2011  | Support AVX, architecture micro-ops                        |
| Ivy Bridge      | `ivybridge`      | 2012  | AVX, F16C (conversion flottants 16 bits)                   |
| Haswell         | `haswell`        | 2013  | AVX2, FMA3, BMI1/BMI2, TSX                                 |
| Broadwell       | `broadwell`      | 2014  | Intel SGX, instructions ADX, RDSEED                        |
| Skylake         | `skylake`        | 2015  | Speed Shift, SGX amélioré, amélioration IPC                |
| Skylake-AVX512  | `skylake-avx512` | 2017  | AVX-512, support d'extensions SIMD                         |
| Cascade Lake    | `cascadelake`    | 2019  | AVX-512 amélioré, DL Boost (VNNI)                          |
| Tiger Lake      | `tigerlake`      | 2020  | AVX-512 VBMI, GFNI, meilleures performances graphiques     |
| Alder Lake      | `alderlake`      | 2021  | Architecture hybride (P-cores/E-cores), DDR5, PCIe 5.0     |
| Sapphire Rapids | `sapphirerapids` | 2022  | AMX (Advanced Matrix Extensions), AVX-512, DDR5            |
| Raptor Lake     | `raptorlake`     | 2022  | Successeur d'Alder Lake, architecture hybride              |
| Meteor Lake     | `meteorlake`     | 2023  | Chiplet design, PCIe 5.0, LPDDR5                           |

### AMD

Table: Principales architectures AMD

| Architecture       | `-march`    | Année | Fonctionnalités                                   |
| ------------------ | ----------- | ----- | ------------------------------------------------- |
| K8 (Athlon 64)     | `k8`        | 2003  | Première architecture x86-64 d'AMD, supporte SSE2 |
| Barcelona          | `barcelona` | 2007  | SSE4a, améliorations cache                        |
| Bulldozer          | `bdver1`    | 2011  | AVX, FMA4, architecture modulaire                 |
| Piledriver         | `bdver2`    | 2012  | FMA3, améliorations IPC                           |
| Zen (Ryzen 1000)   | `znver1`    | 2017  | AVX2, SMT (Simultaneous Multithreading), PCIe 3.0 |
| Zen 2 (Ryzen 3000) | `znver2`    | 2019  | PCIe 4.0, amélioration IPC, 7 nm                  |
| Zen 3 (Ryzen 5000) | `znver3`    | 2020  | Amélioration IPC, nouveau design de cache         |
| Zen 4 (Ryzen 7000) | `znver4`    | 2022  | Support DDR5, PCIe 5.0, gravure en 5 nm           |

### Autres architectures

Table: Autres architectures

| Architecture  | `-march`       | Année | Fonctionnalités Supplémentaires                                |
| ------------- | -------------- | ----- | -------------------------------------------------------------- |
| Atom          | `atom`         | 2008  | Faible consommation, optimisé pour l'efficacité                |
| Silvermont    | `silvermont`   | 2013  | Optimisé pour les systèmes basse puissance, pas de support AVX |
| Tremont       | `tremont`      | 2019  | Utilisé dans les processeurs basse consommation d'Intel        |
| Gracemont     | `gracemont`    | 2021  | Basse consommation pour Alder Lake, pas de support AVX-512     |
| Sierra Forest | `sierraforest` | 2023  | Haute efficacité, multi-core pour les centres de données       |

### Gamme x86-64-vN

Table: Versions de l'architecture x86-64

| Nom de l'Architecture | Option GCC `-march` | Fonctionnalités Supplémentaires                          |
| --------------------- | ------------------- | -------------------------------------------------------- |
| x86-64                | `x86-64`            | Basique 64 bits, compatible avec les premiers cpu x86-64 |
| x86-64-v2             | `x86-64-v2`         | Ajoute SSE3, SSSE3, SSE4.1, SSE4.2, Popcnt               |
| x86-64-v3             | `x86-64-v3`         | Ajoute AVX, AVX2, FMA, BMI1, BMI2, MOVBE                 |
| x86-64-v4             | `x86-64-v4`         | Ajoute AVX-512, support d'instructions plus modernes     |

## Historique

Ci-dessous se trouve la chronologie des principales évolutions des processeurs.

### Avant 1970

Les premiers ordinateurs utilisaient des tubes à vide et des relais pour effectuer des calculs.

En 1945, l'architecture de Von Neumann introduit le concept de programme stocké, où les instructions et les données sont placées dans une même mémoire.

Près de dix ans plus tard, en 1954, les transistors remplacent les tubes à vide, réduisant ainsi la taille et la consommation d'énergie des ordinateurs.

En 1964, l'IBM System/360 inaugure l'architecture CISC (Complex Instruction Set Computing), avec un jeu d'instructions complexe permettant de nombreuses opérations.

La technologie MOS (Metal-Oxide-Semiconductor) permet de réduire encore la taille des transistors et d'accroître la densité des circuits intégrés. Le premier microprocesseur, l'Intel 4004, un modèle 4 bits, fait son apparition en 1971. Il fonctionne à une fréquence de 740 kHz et contient 2 300 transistors, réalisant 92 000 opérations par seconde, contre 3,6 milliards pour un processeur moderne. Gravé en 10 µm, il est bien loin des procédés actuels en 7 nm.

### Années 1970

La mémoire cache fait ses débuts avec l'IBM System/360 Model 85, permettant de stocker temporairement les données les plus fréquemment utilisées afin d'accélérer les accès mémoire.

En 1974, les premières unités de calcul en virgule flottante (FPU, Floating Point Unit) apparaissent avec les processeurs Intel 8008 et 8080 pour prendre en charge les calculs en virgule flottante.

En 1978, l'Intel 8086 introduit l'architecture x86, avec des registres de 16 bits et la segmentation de la mémoire. La mémoire est alors divisée en segments de 64 Ko, chaque segment étant lui-même découpé en blocs de 16 octets. Ce mécanisme permet une gestion plus efficace de la mémoire en segments de taille variable.

En 1982, le mode protégé est introduit avec l'Intel 80286, offrant une gestion plus rigoureuse de la mémoire grâce à des niveaux de privilèges, équivalents aux anneaux de protection dans les systèmes Unix.

En 1985, l'Intel 80386 introduit l'architecture x86 en 32 bits avec un bus d'adressage de 32 bits et un mode de mémoire virtuelle, permettant de gérer jusqu'à 4 Go de mémoire physique. Cette architecture perdurera jusqu'à l'arrivée des processeurs 64 bits développés dans les années 2000.

Le concept de pipeline, qui permet d'exécuter plusieurs instructions en parallèle, est introduit avec l'Intel 80486 en 1989, améliorant ainsi considérablement les performances. Les premiers caches de niveau L2 apparaissent également, ajoutés de manière externe au processeur.

### Années 1990

Intel introduit, avec le processeur Pentium, le premier coprocesseur mathématique directement intégré, permettant de réaliser plus rapidement les calculs en virgule flottante. Un pipeline à cinq étapes est également implémenté dans l'Intel 80486 pour améliorer le traitement parallèle.

En 1995, avec le Pentium Pro, un prédicteur d'embranchements est introduit, optimisant les performances en prédisant les sauts conditionnels afin d'éviter les ruptures de pipeline.

Le cache de niveau L2 est finalement intégré directement au processeur.

En 1999, Intel lance les instructions SIMD (Single Instruction, Multiple Data) avec les extensions SSE (Streaming SIMD Extensions), augmentant ainsi les performances dans les calculs vectoriels.

### Années 2000

Le premier bus externe 64 bits apparaît avec le Pentium 4 en 2000, facilitant la gestion d'une plus grande quantité de mémoire, tandis que le pipeline est étendu à 20 étapes pour atteindre des fréquences plus élevées.

En 2001, Intel introduit les SSE2 (Streaming SIMD Extensions 2) afin d'améliorer les performances des calculs en virgule flottante.

Le cache de niveau 3 (L3) fait son apparition en 2004 avec les processeurs Itanium 2 et Xeon, optimisant les performances des accès mémoire.

En 2006, les premiers processeurs multi-cœurs, avec l'Intel Core Duo, voient le jour, et la technologie Hyper-Threading est intégrée, améliorant les performances des applications multi-threadées.

En 2008, Intel introduit la technologie Smart Cache, permettant un partage dynamique du cache entre les cœurs, augmentant ainsi l'efficacité du processeur. Les procédés de fabrication sont réduits à 45 nm et les fréquences des processeurs atteignent 3 GHz.

### Années 2010

En 2010, Intel introduit le QuickPath Interconnect (QPI) pour remplacer le bus frontal, améliorant les performances de l'interconnexion entre les différents composants.

En 2011, l'extension AVX (Advanced Vector Extensions) vient enrichir les instructions SIMD de la technologie SSE, optimisant ainsi les performances dans les calculs scientifiques.

La génération Skylake, en 2014, introduit des modes d'économie d'énergie sophistiqués pour réduire la consommation. Les procédés de fabrication sont abaissés à 14 nm, améliorant à la fois les performances et l'efficacité énergétique. Les processeurs atteignent alors des fréquences de 4 GHz.

### Années 2020

La technologie EUV (Extreme Ultraviolet Lithography) permet de réduire les procédés de fabrication à 7 nm, compensant l'impossibilité d'augmenter davantage la fréquence des processeurs en raison des contraintes thermiques.

En 2021, l'architecture hybride Alder Lake est introduite, combinant des cœurs à haute performance et des cœurs à haute efficacité pour un meilleur équilibre entre performances et efficacité énergétique.

Les processeurs modernes comptent entre 8 et 24 cœurs, et malgré leur prix comparable à celui de l'Intel 4004 de 1971, leur puissance de calcul est 15,36 milliards de fois supérieure (en tenant compte du fait que l'Intel 4004 fonctionnait en 4 bits et ne pouvait réaliser que quelques centaines d'opérations flottantes par seconde).

## Travaux intéressants

Le **LC-3** est un processeur pédagogique conçu pour l'apprentissage de l'architecture des ordinateurs. Il est simple, mais suffisamment complet pour illustrer les concepts fondamentaux de l'architecture des ordinateurs. Il est utilisé dans de nombreux cours d'informatique pour enseigner les principes de base de l'architecture des ordinateurs.

Le **SAP-1** (Simple As Possible) est un autre processeur pédagogique conçu pour être simple et facile à comprendre. Il est basé sur des registres de décalage et des circuits logiques discrets, ce qui le rend idéal pour l'apprentissage des bases de l'architecture des ordinateurs.

Le **RISC-V** est une architecture de jeu d'instructions ouverte et libre, conçue pour être simple, modulaire et extensible. Elle est de plus en plus populaire dans le domaine de l'informatique, en particulier pour les applications embarquées et les systèmes à faible consommation d'énergie.
