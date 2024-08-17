# Gestion de la mémoire

Vous l'aurez appris à vos dépens, l'erreur *Segmentation fault* (erreur de segmentation) arrive souvent lors du développement. Ce chapitre s'intéresse à la mémoire et vulgarise les concepts de segmentation et traite de l'allocation dynamique.

La mémoire d'un programme est découpée en [segments de données](https://fr.wikipedia.org/wiki/Segment_de_donn%C3%A9es). Les principaux segments sont :

`.text`

: Segment de code: les instructions du programme exécutable sont chargées dans ce segment.

`.rodata`

: Segment de constantes et chaînes de caractères: les constantes globales `const int = 13` et les chaînes de caractères sont enregistrées dans ce segment.

`.bss`

: Segment de variables initialisées: ce segment est garanti d'être initialisé à zéro lorsque le programme est chargé en mémoire. Les variables globales statiques tels que `static int foo = 0` seront stockées dans ce segment.

`.data`

: Segment de variables non initialisées: les variables globales non initialisées comme `static int bar;` seront placées dans ce segment.

`.heap`

: Segment de tas: les allocations dynamiques décrites plus bas dans ce chapitre sont déclarées ici.

`.stack`

: Segment de pile: la chaîne d'appel de fonction ainsi que toutes les variables locales sont mémorisées dans ce segment.


## Allocation statique

Jusqu'ici toutes les variables que nous avons déclarées ont été déclarées statiquement. C'est-à-dire que le compilateur est capable a priori de savoir combien de place prend telle ou telle variable et les agencer en mémoire dans les bons segments. On appelle cette méthode d'allocation de mémoire l'allocation statique.

La [déclaration statique](https://fr.wikipedia.org/wiki/Allocation_de_m%C3%A9moire#Allocation_statique) suivante déclare un tableau de 1024 entiers 64-bits initialisés à zéro et stockés dans le segment `.bss`, soit 64 kio :

```
static int64_t vector[1024] = {0};
```

## Allocation dynamique

Il est des circonstances ou un programme ne sait pas combien de mémoire il a besoin. Par exemple un programme qui compterait le nombre d'occurrences de chaque mot dans un texte devra se construire un index de tous les mots qu'il découvre lors de la lecture du fichier d'entrée. A priori, ce fichier d'entrée étant inconnu au moment de l'exécution du programme, l'espace mémoire nécessaire à construire ce dictionnaire de mots est également inconnu.

L'approche la plus naïve serait d'anticiper le cas le plus défavorable. Le dictionnaire Littré comporte environ 132'000 mots tandis que le Petit Larousse Illustré 80'000 mots environ. Pour se donner une bonne marge de manœuvre et anticiper les anglicismes et les noms propres. Il suffirait de réserver un tableau de 1 million de mots de 10 caractères soit un peu plus de 100 MiB de mémoire quand bien même le fichier qui serait lu ne comporterait que 2 mots: `Hello World!`.

L'approche correcte est d'allouer la mémoire au moment où on en a besoin, c'est ce que l'on appelle l'[allocation dynamique](https://fr.wikipedia.org/wiki/Tas_(allocation_dynamique)).

Lorsqu'un programme a besoin de mémoire, il peut générer un appel système pour demander au système d'exploitation le besoin de disposer de plus de mémoire. En pratique on utilise deux fonctions de la bibliothèque standard `<stdlib.h>`:

`void *malloc(size_t size)`

: Alloue dynamiquement un espace mémoire de `size` bytes. Le terme *malloc* découle de *Memory ALLOCation*.

`void *calloc(size_t nitems, size_t size)`

: Fonctionne de façon similaire à `malloc` mais initialise l'espace alloué à zéro.

`void free(void *ptr)`

: Libère un espace préalablement alloué par `malloc` ou `calloc`

L'allocation se fait sur le `tas` (*heap*) qui est de taille variable. À chaque fois qu'un espace mémoire est demandé, `malloc` recherche dans le segment un espace vide de taille suffisante, s'il ne parvient pas, il exécute l'appel système [sbrk](https://en.wikipedia.org/wiki/Sbrk) qui permet de déplacer la frontière du segment mémoire et donc d'agrandir le segment.

![Allocation et libération mémoire](/assets/images/malloc.drawio)

## Mémoire de programme

Les segments mémoires sont une construction de la bibliothèque standard, selon la bibliothèque utilisée et à fortiori le système d'exploitation utilisé, l'agencement mémoire peut varier.

Néanmoins une bonne représentation est la suivante :

![Organisation de mémoire d'un programme](/assets/images/program-memory.drawio)

On observe que le tas et la pile vont à leur rencontre, et que lorsqu'ils se percutent c'est le crash avec l'erreur bien connue [stack overflow](https://fr.wikipedia.org/wiki/D%C3%A9passement_de_pile).

## La pile

Lorsqu'un programme s'exécute, l'ordre dont les fonctions s'exécutent n'est pas connu à priori. L'ordre d'exécution des fonctions dans l'exemple suivant est inconnu par le programme et donc les éventuelles variables locales utilisées par ces fonctions doivent dynamiquement être allouées.

```c
#include <stdio.h>
#include <stdlib.h>

double square(double num) {
    return num * num
}

double cube(double num) {
    return num * num * num;
}

int main(void) {
    double num = 10;

    for (size_t i = 0; i < 10; i++) {
        if (rand() % 2) {
            num = square(num);
        } else {
            num = cube(num);
        }
    }

    printf("%f\n", num);
}
```

Lors d'un appel de fonction, le compilateur ajoute avant la première instruction du code caché permettant d'empiler sur un espace mémoire dédié (*stack*) les variables locales dont il a besoin ainsi que certaines informations telles que l'adresse mémoire de retour.

## Allocation dynamique sur le tas

L'allocation dynamique permet de réserver - lors de l'exécution - une
zone mémoire dont on vient de calculer la taille. On utilisera la
fonction *malloc* (memory allocation) pour réserver de la mémoire. Cette
fonction n'initialise pas la zone réservée.

```c
typedef unsigned int size_t;
void* malloc(size_t size);
```

Il est nécessaire d'inclure le fichier *stdlib.h* pour utiliser les
fonctions d'allocation mémoire. Par exemple, pour réserver un tableau de
n valeurs de type *double* :

```c
int n;
double * zone_acquisition; // pointeur sur la zone à réserver

n = 100;

zone_acquisition = (double*)malloc(n * sizeof(double));
```

### Allocation dynamique sur le tas avec mise à zéro

On utilisera la fonction *calloc* (memory allocation) pour réserver de
la mémoire avec initialisation automatique de la zone réservée.

```c
void * calloc (size_t count, size_t size);
```

Cette fonction réserve *count* x *size* octets en mémoire et
l'initialise à zéro.

### Modification de la taille d'une zone déjà allouée sur le tas

Si l'on veut agrandir une zone déjà allouée avec *malloc* ou *calloc*,
on utilisera la fonction suivante :

```c
void * realloc (void * ptr, size_t size);
```

Elle permet de :

- réallouer un bloc de mémoire avec une nouvelle taille
- si ptr est NULL, créer un nouveau bloc
- si la réallocation échoue, retourner NULL ; le bloc passé en
  paramètre reste alors inchangé
- en cas de succès, l'adresse retournée peut être différente de ptr ; le
  bloc initialement pointé par ptr a alors été libéré
- le bloc réalloué est initialisé avec le contenu du bloc ptr ;
  l'espace supplémentaire est non initialisé

### Libération

Le tas n'étant pas extensible à l'infini, il faut libérer la mémoire dès
que l'on n'en a plus l'utilité.

```c
void free(void *memblock);
```

Une fois libérée, la mémoire (donc son pointeur) ne doit plus être
utilisée sous peine de corrompre des données du système.

```c
int n;
double * zone_acquisition; // pointeur sur la zone à réserver

n=100;

zone_acquisition = (double*) malloc ( n * sizeof(double) );

// utilisation...

free(zone_acquisition); // libère la mémoire
```

De la même manière, il ne faut pas libérer un bloc qui n'a pas été
alloué. Si on ne libère pas la mémoire, elle reste allouée pour
l'application et la zone disponible diminue. Il peut arriver qu'il ne
reste plus d'espace disponible pour l'allocation dynamique ; cela peut
entraver la bonne marche de l'ordinateur. Ce problème est souvent dû à
des erreurs de conception des applications qui ne libèrent pas tous les
blocs alloués ; on observe alors un phénomène de fuite mémoire qui cause
le plantage de la machine. Selon les fréquences d'allocation et de non
libération, ces problèmes peuvent survenir immédiatement, ou après
plusieurs jours de fonctionnement, ce qui complique grandement les
opérations de debug...

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
fonction d'allocation mémoire sur la pile. L'espace est libéré à la
sortie de la fonction appelante. On veillera tout particulièrement à ce
que le pointeur ayant reçu l'adresse de la zone mémoire réservée ne soit
pas exploité en dehors de la fonction (puisque la zone est libérée quand
on en sort).

### Limite d'utilisation de la pile

L'espace mémoire utilisé par la pile est une zone dont l'usage est
uniquement dédié au programme. Si plusieurs programmes cohabitent en
mémoire, ils auront chacun leur propre pile.

Cet espace mémoire dédié à la pile est de taille fixe et définie lors de
la compilation du programme.

La pile reçoit les éléments suivants :

- les variables locales aux fonctions,
- les variables déclarées comme paramètres dans les fonctions,
- les informations liées aux mécanismes d'appel et de retour des
  fonctions,
- les données retournées par les fonctions,
- les zones allouées par la fonction `alloca`.

Étant donné que la taille de la pile est fixe, il y a un risque qu'elle
soit trop petite pour supporter toutes les informations que votre
programme doit y placer. Si cela se produit, il y a corruption de la
mémoire puisque la pile 'déborde' et que vous dépassez la zone qui lui
est dédiée.

Les événements suivants peuvent générer des débordements de piles :

- trop de variables locales (par exemple un grand tableau),
- trop d'appels de fonctions en cascade,
- utilisation de fonctions récursives (qui s'autoappellent).

Dans le jargon informatique, on appelle ça du *jardinage* puisque vous
allez piétiner les zones mémoires voisines sans en avoir la permission.

Le compilateur (en réalité l'éditeur de liens - le *linker*) vous permet
de spécifier la taille de la pile ; c'est une de ses nombreuses options.

## Variables automatiques

Une variable est dite *automatique* lorsque sa déclaration est faite au sein d'une fonction. La variable d'itération `int i` dans une boucle `for` est dite automatique. C'est-à-dire que le compilateur a le choix de placer cette variable :

- sur la pile ;
- dans un registre mémoire processeur.

Jadis, le mot clé `register` était utilisé pour forcer le compilateur à placer une variable locale dans un registre processeur pour obtenir de meilleures performances. Aujourd'hui, les compilateurs sont assez malins pour déterminer automatiquement les variables souvent utilisées.

## Fragmentation mémoire

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

#### Erreurs de segmentation (*segmentation fault*)

Lorsqu'un programme tente d'accéder à un espace mémoire qui n'est pas mappé dans la MMU, ou que cet espace mémoire ne permet pas le type d'accès souhaité : par exemple une écriture dans une page en lecture seule. Le système d'exploitation tue le processus avec une erreur *Segmentation Fault*. C'est la raison pour laquelle, il n'est pas systématique d'avoir une erreur de segmentation en cas de jardinage mémoire. Tant que les valeurs modifiées sont localisées au sein d'un bloc mémoire autorisé, il n'y aura pas d'erreur.

L'erreur de segmentation est donc générée par le système d'exploitation en levant le signal **SIGSEGV** (Violation d'accès à un segment mémoire, ou erreur de segmentation).

### Memory Pool

Un *memory pool* est une méthode faisant appel à de l'allocation dynamique de blocs de taille fixe. Lorsqu'un programme doit très régulièrement allouer et désallouer de la mémoire, il est préférable que les blocs mémoires aient une taille fixe. De cette façon, après un `free`, la mémoire libérée est assez grande pour une allocation ultérieure.

Lorsqu'un programme est exécuté sous Windows, macOS ou Linux, l'allocation dynamique standard `malloc`, `calloc`, `realloc` et `free` sont performant et le risque de crash dû à une fragmentation mémoire est rare.

En revanche, lors de l'utilisation sur de petites architectures (microcontrôleurs) qui n'ont pas de système sophistiqué pour gérer la mémoire, il est parfois nécessaire d'écrire son propre système de gestion de mémoire.
