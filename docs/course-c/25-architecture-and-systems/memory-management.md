# Gestion de la Mémoire

Vous l'avez sans doute constaté à vos dépens : l'erreur *Segmentation fault* (ou erreur de segmentation) est un fléau fréquent lors du développement. Ce chapitre se propose de plonger dans les arcanes de la gestion de la mémoire, en vulgarisant les concepts de segmentation et en détaillant le mécanisme d'allocation dynamique.

Sur un ordinateur, un programme ne peut s'arroger toute la mémoire disponible. Cette ressource précieuse est partagée entre plusieurs programmes ainsi que le système d'exploitation, qui se charge de l'allouer de manière judicieuse à chaque programme tout en veillant à ce que ces derniers ne se chevauchent pas. On pourrait comparer ce processus à un service cadastral chargé de distribuer équitablement des parcelles de mémoire : chaque programme dispose de son propre espace, strictement délimité.

Cet espace mémoire alloué à un programme est structuré en différents segments, chacun dédié à une fonction spécifique. Les principaux segments sont donnés à la section suivante.

## Segments de mémoire

### `.text` ou `.code`

Le **Segment de code** contient les instructions du programme exécutable, autrement dit le code machine. Ce segment est en lecture seule, ce qui signifie qu'un programme ne peut pas modifier son propre code durant son exécution, garantissant ainsi l'intégrité du code.

### `.rodata`

Le **Segment de données en lecture seule** (*Read-Only Data*) est dédié aux constantes globales et aux chaînes de caractères définies comme littérales dans le code source. Par exemple, une constante globale telle que `const int = 13` ou une chaîne de caractères littérale comme `"abc"` sont stockées dans ce segment. Ces données, une fois définies, ne peuvent être modifiées en cours d'exécution.

### `.bss`

Le **Segment BSS** (*Block Started by Symbol*) est une section en mémoire réservée aux variables globales et statiques qui n'ont pas été initialisées explicitement. Historiquement, le terme "BSS" provient d'une directive utilisée dans les premiers assembleurs d'IBM pour réserver un bloc de mémoire sans y affecter de valeur initiale. Par exemple, si vous déclarez un tableau global `int x[1024];` sans lui assigner de valeurs, il sera placé dans le segment `.bss`. Le système d'exploitation se charge de l'initialiser à zéro lors du lancement du programme, assurant ainsi une base mémoire propre.

### `.data`

Le **Segment de données initialisées** stocke les variables globales et statiques qui ont été initialisées avec une valeur spécifique dans le code source. Contrairement au segment `.bss`, qui est réservé aux variables non initialisées, le segment `.data` contient des données explicitement définies. Par exemple, si vous déclarez `int x = 42;`, la valeur `42` sera stockée dans ce segment, prête à être utilisée dès le démarrage du programme.

### `.heap`

Le **Tas** (*Heap*) est une zone de mémoire à taille dynamique. Lorsqu'un programme nécessite de la mémoire supplémentaire durant son exécution, il peut en demander au système d'exploitation via un appel système. En C, cette interaction est généralement gérée par les fonctions `malloc` et `free` de la bibliothèque standard `<stdlib.h>`. Le tas est crucial pour l'allocation dynamique, permettant de réserver et de libérer de la mémoire selon les besoins spécifiques du programme.

### `.stack`

La **Pile** (*Stack*) est une zone de mémoire à taille fixe, utilisée principalement pour la gestion des appels de fonctions. Lorsqu'une fonction est appelée, les variables locales, les paramètres, ainsi que les informations nécessaires pour gérer l'appel et le retour de la fonction sont empilés sur la pile. La pile est également sollicitée par la fonction `alloca` de la bibliothèque `<malloc.h>`, qui permet d'allouer de la mémoire de manière temporaire. L'ordre d'exécution des fonctions étant imprévisible, la pile s'avère indispensable pour une gestion fluide et dynamique des ressources.

## Points de vigilance

Avant d'entrer dans le vif du sujet, il est important de souligner quelques points concernant la gestion de la mémoire en C :

**Segmentation fault**

: Cette erreur survient généralement lorsque le programme tente d'accéder à une zone de mémoire qui ne lui est pas allouée, violant ainsi les règles de segmentation imposées par le système d'exploitation.

**Finitude de la pile**

: Il est important de noter que la pile a une capacité limitée. Un usage excessif de la pile, par exemple via une récursion trop profonde, peut entraîner un débordement de pile (*stack overflow*), provoquant potentiellement une interruption du programme.

**Gestion de la mémoire dynamique**

: Lorsqu'une mémoire allouée dynamiquement via `malloc` n'est plus nécessaire, il est impératif de la libérer avec `free` pour éviter des fuites de mémoire (*memory leaks*), où des portions de mémoire restent inutilisables pour le système.

En synthèse, la gestion de la mémoire est un art délicat, où chaque segment joue un rôle précis pour assurer la stabilité et l'efficacité du programme. Une bonne compréhension de ces concepts est essentielle pour écrire du code robuste et performant.



## Mémoire de programme

Nous avons vu plus haut que la mémoire d'un programme est divisée en plusieurs segments. En réalité, l'organisation interne de la mémoire d'un programme est indépendante du système d'exploitation. C'est le compilateur et surtout la bibliothèque standard qui se charge de gérer les différents segments mémoires.

Néanmoins si l'on considère la bibliothèque standard `libc` qui est utilisée par la plupart des programmes C, on peut observer que la mémoire d'un programme est organisée de la manière suivante :

![Organisation de mémoire d'un programme](/assets/images/program-memory.drawio)

On observe que le tas et la pile vont à leur rencontre, et que lorsqu'ils se percutent c'est le crash avec l'erreur bien connue [stack overflow](https://fr.wikipedia.org/wiki/D%C3%A9passement_de_pile).

### Allocation statique

Jusqu'à présent, toutes les variables que nous avons déclarées l'ont été de manière statique. Cela signifie que le compilateur peut, dès la compilation, déterminer la taille nécessaire pour chaque variable et les organiser en mémoire dans les segments appropriés. Cette méthode est connue sous le nom d'allocation de mémoire statique.

Pour les variables globales, le compilateur se charge de les initialiser à zéro et de les placer dans les segments `.bss`, `.data` ou `.rodata` selon qu'elles soient initialisées ou non.

Pour les variables locales (celles déclarées à l'intérieur d'une fonction), le compilateur les place sur la pile. La pile est un segment de mémoire dont la croissance est inversée par rapport à la mémoire générale : elle commence à une adresse élevée et s'étend vers les adresses plus basses. Lorsqu'une fonction est appelée, ses variables locales sont empilées sur cette pile, un peu comme on empilerait des assiettes dans une cuisine. Une fois la fonction terminée, ces variables sont dépilées, libérant ainsi l'espace mémoire qu'elles occupaient.

Considérons la déclaration suivante, qui alloue un tableau de 1024 entiers 64 bits, initialisés à zéro et stockés dans le segment `.bss`. Ce segment étant dédié aux variables non initialisées, le système d'exploitation se chargera de les initialiser à zéro :

```c
static int64_t vector[1024];
```

Dans cet exemple, le tableau vector occupe 64 Kio de mémoire (1024 entiers de 64 bits). Comme le tableau est déclaré sans valeur initiale explicite (en dehors de l'initialisation à zéro par défaut), il est placé dans le segment `.bss`, ce qui signifie que le système d'exploitation se chargera de le remplir de zéros.

En revanche, la déclaration suivante crée un tableau de 1024 entiers 64 bits, mais avec une initialisation partielle :

```c
static int64_t vector[1024] = {.[42]=1};
```

Ici, l'élément à l'index 42 du tableau est initialisé à 1, tandis que tous les autres éléments doivent être explicitement initialisés à zéro par le programme. Cette déclaration force le tableau à être placé dans le segment `.data` parce qu'il contient une valeur initiale spécifique autre que zéro. Le programme est donc responsable de l'initialisation des autres éléments du tableau.

Il faut noter que le compilateur peut optimiser l'allocation de mémoire statique en regroupant les variables globales et statiques similaires dans des zones mémoires contiguës. Cela permet d'optimiser l'accès à ces variables et de réduire la fragmentation de la mémoire. Il n'y a donc aucune garantie que les variables globales déclarées les unes à la suite des autres dans le code source seront stockées dans des emplacements mémoires contigus.

!!! bug "La pomme est plus verte chez le voisin"

    Considérons le code suivant :

    ```c
    static int32_t a = 42;
    static int32_t b = 23;

    int main() {
      int32_t *p = &a;
      p[1] = 666;

      printf("%d\n", b);
    }
    ```

    Le programme compile sans erreur, et lors de l'exécution il est très probable que vous obteniez la valeur `666` affichée à l'écran. Pourquoi ? Parce qu'il est très probable que les variables `a` et `b` soient stockées dans des emplacements mémoires contigus, et que l'opération `p[1] = 666` modifie en réalité la valeur de `b`.

    Néanmoins, le standard C ne garantit pas que les variables globales soient stockées dans des emplacements mémoires contigus. Ce code est donc non portable et peut produire des résultats inattendus sur d'autres compilateurs ou architectures.

### Allocation dynamique

Il est des circonstances ou un programme ne sait pas combien de mémoire il a besoin. Par exemple un programme qui compterait le nombre d'occurrences de chaque mot dans un texte devra se construire un index de tous les mots qu'il découvre lors de la lecture du fichier d'entrée. A priori, ce fichier d'entrée étant inconnu au moment de l'exécution du programme, l'espace mémoire nécessaire à construire ce dictionnaire de mots est également inconnu.

L'approche la plus naïve serait d'anticiper le cas le plus défavorable. Le dictionnaire Littré comporte environ 132'000 mots tandis que le Petit Larousse Illustré 80'000 mots environ. Pour se donner une bonne marge de manœuvre et anticiper les anglicismes et les noms propres. Il suffirait de réserver un tableau de 1 million de mots de 10 caractères soit un peu plus de 100 MiB de mémoire quand bien même le fichier qui serait lu ne comporterait que 2 mots: `Hello World!`.

Vous l'avez deviné, l'approche naïve est à proscrire. D'une part parce que vous n'avez aucune garantie que le nombre de mots ne dépassera pas 1 million, d'autre part parce que vous allez probablement gaspiller de la mémoire laissée inutilisée.

L'approche correcte est d'allouer la mémoire au moment où on en a besoin, c'est ce que l'on appelle l'[allocation dynamique de mémoire](https://fr.wikipedia.org/wiki/Tas_(allocation_dynamique)).

Lorsqu'un programme a besoin de mémoire, il peut générer un appel système pour demander au système d'exploitation le besoin de disposer de plus de mémoire. En pratique on utilise trois fonctions de la bibliothèque standard `<stdlib.h>`:

`void *malloc(size_t size)`

: Alloue dynamiquement un espace mémoire de `size` bytes. Le terme *malloc* découle de *Memory ALLOCation*.

`void *calloc(size_t nitems, size_t size)`

: Fonctionne de façon similaire à `malloc` mais initialise l'espace alloué à zéro.

`void free(void *ptr)`

: Libère un espace préalablement alloué par `malloc` ou `calloc`

Comme évoqué plus haut, l'allocation dynamique se fait sur le `tas` (segment `.heap`) qui est de taille variable. À chaque fois qu'un espace mémoire est demandé, `malloc` recherche dans le segment un espace vide de taille suffisante, s'il ne parvient pas, il exécute l'appel système [sbrk](https://en.wikipedia.org/wiki/Sbrk) qui permet de déplacer la frontière du segment mémoire et donc d'agrandir le segment.

Considérons la figure suivante. En abscisse le temps et verticalement l'espace mémoire à des instants données. Le segment `.heap` croît au fur et à mesure des appels à `malloc`. Au début on réserve un espace de deux `char` dont l'adresse est récupérée dans le pointeur `a`. Puis, on réserve un espace de 1 `char` supplémentaire pour le pointeur `b`. Lorsque `free` est appelé sur `a`, l'espace mémoire est libéré et peut être réutilisé par un appel ultérieur à `malloc`. Enfin, on réserve un espace de 1 `char` pour le pointeur `c`. À l'issue de cette exécution, on peut constater que la mémoire a été fragmentée. C'est-à-dire que l'espace mémoire alloué au programme comporte des trous.

![Allocation et libération mémoire](/assets/images/malloc.drawio)

À la fin de l'exécution du programme, ce dernier consomme sur le *heap* trois bytes d'espace mémoire bien qu'il n'en utilise que deux. Imaginez un programme qui alloue et libère de la mémoire de manière répétée, il est probable que la fragmentation mémoire s'installe et que le programme consomme beaucoup plus de mémoire que nécessaire. Ces problèmes de fragmentation sont fréquents dans de gros programmes. N'avez-vous jamais été contraint de redémarrer votre navigateur web car il consommait trop de mémoire mais qu'aucun onglet n'était ouvert ? C'est probablement dû à un problème de fragmentation mémoire.

En pratique, nous verrons que le système d'exploitation est capable de gérer la fragmentation mémoire dans une certaine mesure en déplaçant les blocs mémoires pour les regrouper grace à un mécanisme appelé [MMU](https://en.wikipedia.org/wiki/Memory_management_unit). Ce mécanisme n'existe cependant pas sur des petites architectures matérielles comme les microcontrôleurs. C'est pourquoi les développeurs évitent autant que possible l'allocation dynamique de mémoire sur ces plateformes.

## La pile

Lorsqu'un programme s'exécute, l'ordre dont les fonctions s'exécutent n'est pas connu à priori. L'ordre d'exécution des fonctions dans l'exemple suivant est inconnu par le programme et donc les éventuelles variables locales utilisées par ces fonctions doivent dynamiquement être allouées. Elle fonctionne sur le principe **LIFO** (*Last In First Out*), c'est-à-dire que la dernière variable allouée est la première à être libérée.

Comme évoqué la pile est un segment de mémoire à taille fixe qui est utilisée pour stocker les variables locales, les paramètres des fonctions, les informations de retour des fonctions, les données retournées par les fonctions et les zones allouées par la fonction `alloca`.

Comme le montre la table suivante, Windows ne déroge pas à la règle en faisant bande à part avec une taille de pile de 1 MiB. Les autres systèmes d'exploitation ont plutôt une taille de pile de 8 MiB. Cette différence est très importante car elle présente le risque pour un programme développé et testé sous Linux de ne pas fonctionner sous Windows en raison de l'utilisation de la pile.

Table: Taille de la pile pour quelques architectures

| Système d'exploitation | Taille de la pile |
| ---------------------- | ----------------- |
| Windows                | 1 MiB             |
| Linux                  | 8 MiB             |
| macOS                  | 8 MiB             |
| Solaris                | 8 MiB             |

À titre d'exemple, le programme suivant fonctionne très bien sous Linux mais pas sous Windows ou l'erreur *segmentation fault* est levée.

```c
int main() {
   char a[4 * 1024 * 1024];  // 4 MiB
}
```

Pour éviter ce genre de problème, il est recommandé de ne pas utiliser la pile pour stocker des données de grande taille, préférez l'allocation dynamique sur le tas.

[](){#stack-plumbing}

### Fonctionnement de la pile


La pile utilise deux registres essentiels généralement stockés directement dans le processeur. Il s'agit du *Stack Pointer* et du *Frame Pointer*.

**Le Stack Pointer (SP)**

: Il pointe vers le sommet de la pile, c'est-à-dire l'adresse mémoire où la prochaine donnée sera ajoutée ou retirée. Dans une architecture x86, le Stack Pointer est généralement stocké dans le registre `esp` (32 bits) ou `rsp` (64 bits).

**Le Frame Pointer (FP)** ou **Base Pointer (BP)**

: Il sert de référence pour accéder aux variables locales et aux paramètres d'une fonction. Il reste constant pendant toute la durée de l'exécution d'une fonction. Dans une architecture x86, le Frame Pointer est généralement stocké dans le registre `ebp` (32 bits) ou `rbp` (64 bits).

Lorsque vous appelez une fonction, les éléments suivants sont généralement ajoutés à la pile (l'ordre peut légèrement varier selon l'architecture et le compilateur) :

1. **L'adresse de retour** : L'adresse à laquelle le programme doit revenir après l'exécution de la fonction.
2. **Les paramètres de la fonction** : Les arguments surnuméraires passés à la fonction.
3. **Le Frame Pointer (ancien)** : La sauvegarde de l'ancien Frame Pointer pour restaurer l'état de la pile lors du retour de la fonction.
4. **Les variables locales** : L'espace pour les variables locales de la fonction est réservé dans la pile.

Prenons l'exemple du programme suivant qui calcule la conjecture de Syracuse (ou de Collatz) pour un nombre donné. Ce programme récursif affiche les nombres de la séquence de Collatz pour un nombre donné et retourne le nombre de niveaux de la séquence. Si la profondeur de récursion dépasse 100, le programme renvoie -1 et si le nombre atteint 1, le programme renvoie le niveau actuel de la séquence, c'est la condition de sortie de la récursion.

```c linenums="1"
#include <stdint.h>
#include <stdio.h>

int collatz(int64_t n, int64_t i) {
   printf("%ld ", n);
   int64_t level = i + 1;
   if (n == 1) return level;
   if (i > 100) return -1;
   int64_t next = n % 2 == 0 ? n / 2 : 3 * n + 1;
   return collatz(next, level);
}

int main() {
   collatz(12, 0);
   return 0;
}
```

Pour analyser comment la pile est utilisée dans ce programme, nous allons utiliser le débogueur `gdb`. Tout d'abord il faut compiler le programme avec le flag `-g` pour inclure les informations de débogage :

```bash
gcc -g collatz.c -o collatz
```

Puis exécutez le programme avec `gdb` :

```bash
gdb ./collatz
```

Depuis GDB on va tout d'abord ajouter un point d'arrêt à la fin de l'exécution (ligne 15) puis lancer l'exécution du programme :

```bash
(gdb) break 15
Breakpoint 1 at 0x1179: file collatz.c, line 15.
(gdb) run
Starting program: /path/to/collatz
12 6 3 10 5 16 8 4 2 1
```

Le programme s'arrête à la fin de l'exécution. Nous pouvons maintenant examiner la pile en affichant les 100 dernières valeurs 64 bits l'adresse du Frame Pointer (FP) moins 0x300 octets. Ces valeurs sont un peu une devinette, il faut "fouiller" un peu pour identifier ce qui nous intéresse car on ne sait pas trop combien d'éléments ont été ajoutés à la pile. Voici comment cela peut être fait :

```text
(gdb) x/100g $rbp - 0x300
0x7fffffffda40: 0x7fffffffda70 0x555555555178
0x7fffffffda50: 9       1
0x7fffffffda60: 10      0                       << (3)
0x7fffffffda70: 0x7fffffffdaa0 0x5555555551e6
0x7fffffffda80: 8       2
0x7fffffffda90: 9       1
0x7fffffffdaa0: 0x7fffffffdad0 0x5555555551e6
0x7fffffffdab0: 7       4
0x7fffffffdac0: 8       2
0x7fffffffdad0: 0x7fffffffdb00 0x5555555551e6
0x7fffffffdae0: 6       8
0x7fffffffdaf0: 7       4
0x7fffffffdb00: 0x7fffffffdb30 0x5555555551e6
0x7fffffffdb10: 5       16
0x7fffffffdb20: 6       8
0x7fffffffdb30: 0x7fffffffdb60 0x5555555551e6
0x7fffffffdb40: 4       5
0x7fffffffdb50: 5       16
0x7fffffffdb60: 0x7fffffffdb90 0x5555555551e6
0x7fffffffdb70: 3       10
0x7fffffffdb80: 4       5
0x7fffffffdb90: 0x7fffffffdbc0 0x5555555551e6
0x7fffffffdba0: 2       3
0x7fffffffdbb0: 3       10
0x7fffffffdbc0: 0x7fffffffdbf0 0x5555555551e6
0x7fffffffdbd0: 1       6
0x7fffffffdbe0: 2       3                       << ...
0x7fffffffdbf0: 0x7fffffffdc20 0x5555555551e6   << FP, adresse de retour (2)
0x7fffffffdc00: 0       12                      << i, n (1)
0x7fffffffdc10: 1       6                       << level, next
0x7fffffffdc20: 0x7fffffffdc30 0x5555555551ff   << FP, adresse de retour
0x7fffffffdc30: 0x7fffffffdcd0 0x7ffff7dc21ca
0x7fffffffdc40: 0x7fffffffdc80 0x7fffffffdd58
```

Avec la commande suivante, on prend note de la valeur actuelle du Frame Pointer. C'est la valeur de base au niveau du `main`. Les appels successifs à `collatz` ont été empilés et comme la pile descend, on aura tout en bas l'adresse de retour de `main` :

```bash
(gdb) info register rbp
rbp            0x7fffffffdc30      0x7fffffffdc30
```

À partir de cela et en analysant la pile, on peut voir comment les valeurs sont empilées et désempilées lors des appels de fonctions. On y retrouve les variables locales `level` et `next` ainsi que les arguments sauvegardés pour les appels récursifs de `collatz` (les valeurs de `n` et `i`). On peut facilement identifier les différentes *frames* de pile avec la valeur sauvegardée du Frame Pointer.

En (1), il y a le passage initial des arguments depuis le `main`, `collatz` a été appelé avec `collatz(12, 0)`. En (2), on voit l'adresse du précédent *frame* (`0x7fffffffdc20`). En (3) la dernière valeur de `n` et `i` avant le retour de la fonction.

La figure ci-dessous résume graphiquement le fonctionnement de la pile. On y voit deux *frames* liées entre elles par le *frame pointer*. Les adresses de retours correspondent à la ligne 10 et 14 du programme, soit l'emplacement des appels de fonctions.

![Pile d'exécution](/assets/images/stack.drawio)

### Passage des arguments

En pratique, les arguments des fonctions ne sont pas entièrement passés sur la pile pour des questions de performances. Sur une architecture x86-64, les 6 premiers arguments sont passés dans les registres processeur `rdi`, `rsi`, `rdx`, `rcx`, `r8` et `r9`. Les arguments suivants sont passés sur la pile. Dans notre exemple, nous voyons malgré tout que les arguments `n` et `i` sont passés sur la pile mais il s'agit d'une sauvegarde locale car la fonction est récursive et à chaque appel, les registres seraient écrasés.

## Allocation dynamique sur le tas

L'allocation dynamique permet de réserver - lors de l'exécution - une
zone mémoire dont on vient de calculer la taille. La limite de mémoire est techniquement celle de la machine. Un ordinateur avec 32 Gio de RAM peut allouer 32 Gio de mémoire dynamique mais partagée entre tous les programmes en cours d'exécution.

C'est la fonction *malloc* (memory allocation) qui est utilisée pour demander de la mémoire. Cette fonction est implémentée dans la librairie standard du langage C. Elle peut si nécessaire, demander au système d'exploitation de lui allouer de la mémoire par l'intermédiaire d'un appel système comme *sbrk* ou *mmap*. En effet, les appels systèmes sont coûteux en temps et en ressources car le système d'exploitation doit interrompre le programme changer de contexte pour exécuter le code du noyau puis revenir au programme. C'est pourquoi la fonction *malloc* ne demande pas systématiquement de la mémoire au système d'exploitation. Elle dispose d'une mémoire tampon qu'elle alloue progressivement. Ce n'est que lorsque cette mémoire tampon est épuisée, qu'elle demande alors de la mémoire au système d'exploitation. Contrairement aux idées reçues, les appels à *malloc* ne sont pas systématiquement coûteux.

### Allocation

Pour utiliser l'allocation dynamique de mémoire il est nécessaire d'inclure le fichier *stdlib.h*. Si l'on souhaite allouer un tableau de 1024 entiers 32 bits (soit 4 Kio), on écrira :

```c
int main() {
   int *data = (int*)malloc(1024 * sizeof(int));
   if (data == NULL) {
      fprintf(stderr, "Impossible d'allouer la mémoire\n");
      return 1;
   }
   for (int i = 0; i < 1024; i++) data[i] = i;

   free(data);
}
```

Dans cet exemple, la fonction *malloc* retourne un pointeur sur la zone de mémoire demandée. Si l'allocation échoue, la fonction retourne `NULL`. Il est important de vérifier que l'allocation a réussi avant d'utiliser le pointeur retourné. Si l'allocation a échoué, il est recommandé de gérer l'erreur et de ne pas continuer l'exécution du programme.

L'allocation peut échouer dans les cas suivants :

- L'ordinateur n'a plus de mémoire disponible.
- La taille demandée est trop grande.
- La mémoire est fragmentée et il n'y a pas de blocs contigus suffisamment grands pour satisfaire la demande.
- Le système d'exploitation a mis en place des quotas de mémoire pour les processus.

Une fois que l'on s'est assuré que `*data` contient bien une adresse mémoire valide, on peut l'utiliser comme un tableau classique. Notons au passage que la mémoire allouée dynamiquement n'est pas initialisée. Il est donc nécessaire de l'initialiser avant de l'utiliser. Une manière simple est d'appeler la fonction *memset* de la librairie standard *string.h* :

```c
memset(data, 0, 1024 * sizeof(int));
```

Cette fonction initialise la zone mémoire pointée par `data` avec des zéros. Comme il est fréquent de demander de la mémoire initialisée, la fonction *calloc* est souvent utilisée à la place de *malloc*. Elle joue les deux rôles : allouer de la mémoire et l'initialiser à zéro.

```c
int *data = (int*)calloc(1024, sizeof(int));
```

!!! bug "Fuite mémoire"

    La difficulté principale de ce mécanisme est que si l'on perd une référence sur la mémoire allouée, il est impossible de la libérer. C'est ce que l'on appelle une fuite mémoire (*memory leak*). Cela peut arriver assez facilement:

    ```c
    int main() {
      int *data = (int*)malloc(1024 * sizeof(int));

      data = (int*)42; // Fuite mémoire, on écrase le pointeur et on ne pourra plus libérer la mémoire allouée
    }
    ```

    Dans cet exemple, le pointeur `data` est écrasé par la valeur `42`. La mémoire allouée par `malloc` est perdue et ne peut plus être libérée.

Notez que les protoypes de `malloc` (*Memory ALLOCate*) et `calloc` (*Continuous ALLOCate*) diffèrent légèrement :

```c
void *malloc(size_t size);
void *calloc(size_t nitems, size_t size);
```

L'un prend `size` correspondant à la taille en octets de la mémoire à allouer, l'autre prend `nitems` et `size` correspondant respectivement au nombre d'éléments et à la taille en octets de chaque élément.

La justification principale de cette différence est historique. `malloc` est plus ancienne et a été introduite dans les premières versions du langage C. `calloc` est apparue plus tard et a été conçue pour simplifier l'allocation de tableaux. En effet, il est plus naturel de spécifier le nombre d'éléments et la taille de chaque élément pour allouer un tableau. (c.f. [SO](https://stackoverflow.com/a/12555996/2612235).

### Libération

Une fois que le travail est terminé, il est nécessaire de libérer la mémoire allouée dynamiquement. C'est la fonction *free* qui est utilisée pour cela. Le prototype de la fonction est le suivant :

```c
void free(void *ptr);
```

Elle prend en paramètre un pointeur vers la zone mémoire à libérer.

Dois-je appeler `free` à la fin du main ? Dans un programme C, appeler `free` pour libérer la mémoire allouée dynamiquement (par `malloc`, `calloc`, ou `realloc`) avant la fin du `main` est une bonne pratique, mais ce n'est pas strictement nécessaire dans tous les cas.

Un cas pour lequel il est nécessaire d'appeler `free` avant la fin du `main` est lorsqu'un développeur utilise des outils d'analyse de mémoire comme Valgrind. Ces outils peuvent signaler des "fuites" de mémoire si des allocations ne sont pas libérées à la fin du programme, même si le système d'exploitation récupère automatiquement toute la mémoire allouée à la fin du programme.

En résumé, bien que ce ne soit pas strictement nécessaire d'appeler `free` avant la fin du `main` dans tous les cas, le faire est considéré comme une bonne pratique et contribue à maintenir un code propre et sans fuites de mémoire.

### Réallocation

Parfois, il est nécessaire de modifier la taille d'une zone mémoire déjà allouée. C'est la fonction *realloc* qui est utilisée pour cela. Le prototype de la fonction est le suivant :

```c
void *realloc(void *ptr, size_t size);
```

Elle prend en paramètre un pointeur vers la zone mémoire à réallouer et la nouvelle taille de la zone mémoire. La fonction retourne un pointeur vers la nouvelle zone mémoire allouée comme pour `malloc`. Si la réallocation échoue, la fonction retourne `NULL` et la zone mémoire initiale reste inchangée. Aussi, pour éviter les fuites mémoire, on veillera à ne pas perdre la référence sur la zone mémoire initiale avant d'avoir récupéré le pointeur de la zone mémoire réallouée.

```c
int main() {
   // Allocation
   int *data = (int*)malloc(1024 * sizeof(int));
   if (data == NULL) return 1;

   // Réallocation
   int *new_data = (int*)realloc(data, 2048 * sizeof(int));
   if (new_data == NULL) return 1;
   data = new_data;

   // Libération
   free(data);
}
```

Notons que la nouvelle zone mémoire allouée par `realloc` n'est pas nécessairement à la même adresse que la zone mémoire initiale. En effet, si la zone mémoire qui suit la zone mémoire initiale est libre, `realloc` peut simplement étendre la zone mémoire initiale et la valeur du pointeur reste inchangée. Dans le cas contraire, il allouera une nouvelle zone mémoire, copiera les données de la zone mémoire initiale dans la nouvelle zone mémoire et libérera la zone mémoire initiale.

En d'autres termes, des appels trop fréquents à `realloc` peuvent entraîner des copies inutiles de données et des performances médiocres. Il est donc recommandé de réserver la mémoire en une seule fois si possible. Prenons l'exemple suivant :

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
   size_t size = 1;
   char *data = (char *)malloc(size);
   if (data == NULL) return 1;

   while (!feof(stdin)) {
      data[size++ - 1] = getchar();
      {
         char *new_data = (char *)realloc(data, size);
         if (new_data == NULL) return 1;
         data = new_data;
      }
   }

   printf("%s\n", data);
   free(data);
}
```

Le programme lit des caractères depuis l'entrée standard et les stocke dans un tableau dynamique. À chaque itération, il réalloue la mémoire pour stocker un caractère supplémentaire. Cette approche est inefficace car elle entraîne une copie potentielle de la mémoire à chaque itération. Il est préférable de réserver la mémoire en une seule fois en utilisant une taille de mémoire suffisamment grande pour stocker tous les caractères.

En pratique on utilise fréquemment un paramètre supplémentaire nommé facteur de croissance qui permet de réallouer la mémoire en fonction de la taille actuelle. Avec un facteur de croissance de 2, lorsqu'on réalloue la mémoire, on double la taille de la zone mémoire. Cela permet de limiter le nombre d'appels à `realloc` et donc de limiter les copies inutiles de données. Voici le même programme que ci-dessus mais avec un facteur de croissance de 2 :

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
   size_t size = 1;
   size_t capacity = 128;
   char *data = (char *)malloc(capacity);
   if (data == NULL) return 1;

   while (!feof(stdin)) {
      data[size++ - 1] = getchar();
      if (size >= capacity) {
         capacity *= 2;
         char *new_data = (char *)realloc(data, capacity);
         if (new_data == NULL) return 1;
         data = new_data;
      }
   }

   printf("%s\n", data);
   free(data);
}
```

Ici, deux variables sont utilisées `size` qui correspond à la taille actuelle du tableau et `capacity` qui correspond à la capacité totale du tableau. Lorsque la taille du tableau atteint sa capacité, on double la capacité du tableau et on réalloue la mémoire.

### Allocation dynamique sur la pile

L'allocation dynamique sur la pile est équivalente à l'allocation sur
le tas sauf qu'elle est plus rapide (pas de recherche par le système
d'un espace suffisant et continu) et qu'elle ne nécessite pas de
libération.

On utilisera la fonction *alloca* (memory allocation) pour réserver de
la mémoire. Cette fonction n'initialise pas la zone réservée.

```c
void* alloca(size_t size);
```

Il est nécessaire d'inclure le fichier *malloc.h* pour utiliser cette
fonction d'allocation mémoire sur la pile.

L'avantage par rapport à `malloc` est que la mémoire est libérée automatiquement à la sortie de la fonction. C'est donc une solution idéale pour allouer de la mémoire temporaire dans une fonction. Par exemple, si vous avez besoin d'un tableau temporaire pour effectuer un calcul, vous pouvez utiliser `alloca` pour réserver la mémoire nécessaire. Néanmoins vous devez vous assurer que la mémoire allouée ne dépasse pas la taille de la pile qui est de 1 MiB sous Windows et 8 MiB sous Linux et macOS.

Les inconvénients sont que la fonction `alloca` n'est pas standardisée et n'est pas disponible sur toutes les plateformes.

Voici un exemple de fonctionnement:

```c
#include <alloca.h>

void foo() {
   int *data = (int*)alloca(1024 * sizeof(int));
   for (int i = 0; i < 1024; ++i) data[i] = i;
}
```

!!! warning "Non standard"

    Comme évoqué la fonction `alloca` n'est pas standardisée et n'est pas disponible sur toutes les plateformes. Il est recommandé de ne pas l'utiliser dans un code portable.

## Gestion interne de la mémoire

Pour mieux comprendre la tuyauterie de l'allocation dynamique de mémoire, attardons-nous un peu sur la gestion interne de la mémoire.

### Fragmentation mémoire

On peut observer à la figure suivante montre qu'après un appel successif de `malloc` et de `free` des espaces mémoire non utilisés peuvent apparaître entre des régions utilisées. Ces *trous* sont appelés fragmentation mémoire.

Dans la figure suivante, on suit l'évolution de l'utilisation du *heap* au cours de la vie d'un programme. Au début ➀, la mémoire est libre. Tant que de la mémoire est allouée sans libération (`free`), aucun problème de fragmentation ➁. Néanmoins, après un certain temps la mémoire devient fragmentée ➂ ; il reste dans cet exemple 2 emplacements de taille 2, un emplacement de taille 5 et un emplacement de taille 8. Il est donc impossible de réserver un espace de taille 9 malgré que l'espace cumulé libre est suffisant.

![Fragmentation mémoire](/assets/images/fragmentation.drawio)

Dans une petite architecture, l'allocation et la libération fréquente d'espaces mémoire de taille arbitraire sont malvenues. Une fois que la fragmentation mémoire est installée, il n'existe aucun moyen de soigner le mal si ce n'est au travers de l'ultime solution de l'informatique : [éteindre puis redémarrer](https://www.youtube.com/watch?v=nn2FB1P_Mn8).

### MMU

Les systèmes d'exploitation modernes (Windows, Linux, macOS...) utilisent tous un dispositif matériel nommé [MMU](https://en.wikipedia.org/wiki/Memory_management_unit) pour *Memory Management Unit*. La MMU est responsable de créer un espace mémoire **virtuel** entre l'espace physique. Cela crée une indirection supplémentaire, mais permet de réorganiser la mémoire physique sans compromettre le système.

En pratique l'espace de mémoire virtuelle est toujours beaucoup plus grand que l'espace physique. Cela permet de s'affranchir dans une large mesure de problèmes de fragmentation, car si l'espace virtuel est suffisamment grand, il y aura statistiquement plus de chance d'y trouver un emplacement non utilisé.

La programmation sur de petites architectures matérielles (microcontrôleurs, DSP) ne possède pas de MMU et dès lors l'allocation dynamique est généralement à proscrire à moins qu'elle soit faite en connaissance de cause et en utilisant des mécanismes comme les *memory pool*.

Dans la figure ci-dessous. La mémoire physique est représentée à droite en termes de pages mémoires physiques (*Physical Pages* ou **PP**). Il s'agit de blocs mémoires contigus d'une taille fixe, par exemple 64 kb. Chaque page physique est mappée dans une table propre à chaque processus (programme exécutable). On y retrouve quelques propriétés utiles à savoir, est-ce que la page mémoire est accessible en écriture, est-ce qu'elle peut contenir du code exécutable ? Une propriété peut indiquer par exemple si la page mémoire est valide. Chacune de ces entrées est considérée comme une page mémoire virtuelle (*virtual page* **VP**).

![Mémoire virtuelle](/assets/images/mmu.drawio)

### Mémoire cache

La mémoire cache est un dispositif matériel qui permet de stocker temporairement des données fréquemment utilisées. Elle est utilisée pour accélérer l'accès à la mémoire principale. La mémoire cache est généralement plus rapide que la mémoire principale, mais elle est aussi plus petite. Il existe plusieurs niveaux de cache, le cache de niveau 1 (L1) est le plus rapide mais aussi le plus petit, le cache de niveau 2 (L2) est plus lent mais plus grand, et ainsi de suite.

### Erreurs de segmentation

Lorsqu'un programme tente d'accéder à un espace mémoire qui n'est pas mappé dans la MMU, ou que cet espace mémoire ne permet pas le type d'accès souhaité : par exemple une écriture dans une page en lecture seule. Le système d'exploitation tue le processus avec une erreur *Segmentation Fault*. C'est la raison pour laquelle, il n'est pas systématique d'avoir une erreur de segmentation en cas de jardinage mémoire. Tant que les valeurs modifiées sont localisées au sein d'un bloc mémoire autorisé, il n'y aura pas d'erreur.

L'erreur de segmentation est donc générée par le système d'exploitation en levant le signal **SIGSEGV** (Violation d'accès à un segment mémoire, ou erreur de segmentation).

### Memory Pool

Un *memory pool* est une méthode faisant appel à de l'allocation dynamique de blocs de taille fixe. Lorsqu'un programme doit très régulièrement allouer et désallouer de la mémoire, il est préférable que les blocs mémoires aient une taille fixe. De cette façon, après un `free`, la mémoire libérée est assez grande pour une allocation ultérieure.

Lorsqu'un programme est exécuté sous Windows, macOS ou Linux, l'allocation dynamique standard `malloc`, `calloc`, `realloc` et `free` sont performant et le risque de crash dû à une fragmentation mémoire est rare.

En revanche, lors de l'utilisation sur de petites architectures (microcontrôleurs) qui n'ont pas de système sophistiqué pour gérer la mémoire, il est parfois nécessaire d'écrire son propre système de gestion de mémoire.
