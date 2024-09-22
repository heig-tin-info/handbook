# Introduction

## Sécurité du langage C

Le langage C est un langage de programmation qui permet de manipuler directement la mémoire de l'ordinateur. Cela permet de réaliser des programmes très performants, mais cela peut aussi être dangereux. En effet, si un programme écrit en C contient une erreur, il peut provoquer des bugs, des plantages, voire des failles de sécurité.

Le langage n'est pas équipé de mécanismes de sécurité avancés comme le Java ou le C#, qui sont des langages de programmation plus modernes. Il n'y a pas de gestion de dépasserment de tampon, de vérification de la mémoire, de vérification des types, etc. Il est facile de *jardiner* la mémoire, c'est-à-dire d'écrire dans des zones mémoires qui ne nous appartiennent pas.

Des langages plus modernes comme le Zig ou le Rust ont été créés pour pallier à ces problèmes. Ils sont plus sécurisés, mais aussi plus complexes à apprendre.

Par ailleurs le C souffre de son ancienneté et de l'impérieuse nécessité de conserver une compatibilité ascendante. Cela signifie que des fonctionnalités obsolètes ou dangereuses sont toujours présentes dans le langage. Des correctifs ont été apportés principalement par l'ajout de nouvelles bibliothèques ou fonctions.

### Fonctions dangereuses

Vous avez peut être vu des fonctions en C se terminant par le suffixe `_s` comme `strcpy_s`, `strcat_s`, `sprintf_s`, etc. Ces fonctions sont des versions sécurisées des fonctions classiques `strcpy`, `strcat`, `sprintf`, etc. Elles vérifient que la taille des buffers est suffisante pour contenir les données à copier. Si ce n'est pas le cas, elles ne copient pas les données et retournent une erreur. Ces fonctions sécurisées sont plus lentes que les fonctions classiques, mais elles sont plus sûres.

Voici la liste des fonctions sécurisées offertes par le langage, jusqu'à C23 :

Table: Fonctions sécurisées du langage C

| Fonction      | Description                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| `strcpy_s`    | Copie une chaîne de caractères dans un buffer, avec vérification de la taille du buffer                 |
| `strcat_s`    | Concatène deux chaînes de caractères avec vérification de la taille du buffer                           |
| `sprintf_s`   | Écrit une chaîne de caractères formatée dans un buffer avec vérification de la taille du buffer         |
| `strncpy_s`   | Copie une chaîne de caractères dans un buffer avec une taille maximale                                  |
| `strncat_s`   | Concatène deux chaînes de caractères avec une taille maximale et vérification de la taille du buffer    |
| `snprintf_s`  | Écrit une chaîne de caractères formatée dans un buffer avec une taille maximale et vérification         |
| `memcpy_s`    | Copie une zone mémoire dans une autre zone mémoire, avec vérification de la taille du buffer            |
| `memmove_s`   | Copie une zone mémoire dans une autre zone mémoire, même si les zones se chevauchent, avec vérification |
| `memset_s`    | Remplit une zone mémoire avec une valeur donnée, avec vérification du tampon                            |
| `fopen_s`     | Ouvre un fichier de manière sécurisée                                                                   |
| `freopen_s`   | Rouvre un fichier existant de manière sécurisée                                                         |
| `tmpfile_s`   | Crée un fichier temporaire sécurisé                                                                     |
| `getc_s`      | Lit un caractère d'un fichier de manière sécurisée                                                      |
| `fgets_s`     | Lit une ligne de texte d'un fichier de manière sécurisée, avec gestion de la taille du buffer           |
| `fread_s`     | Lit des blocs de données d'un fichier dans un buffer sécurisé, avec vérification des tailles            |
| `strerror_s`  | Renvoie un message d'erreur de manière sécurisée                                                        |
| `bsearch_s`   | Recherche un élément dans un tableau trié de manière sécurisée                                          |
| `qsort_s`     | Trie un tableau de manière sécurisée                                                                    |
| `fscanf_s`    | Lit des données formatées depuis un fichier de manière sécurisée                                        |
| `sscanf_s`    | Lit des données formatées depuis une chaîne de caractères de manière sécurisée                          |
| `vsnprintf_s` | Écrit une chaîne de caractères formatée dans un buffer avec une taille maximale et vérification         |
| `vsscanf_s`   | Lit des données formatées depuis une chaîne de caractères de manière sécurisée                          |
| `vswscanf_s`  | Lit des données formatées depuis une chaîne de caractères de manière sécurisée                          |
| `wcscpy_s`    | Copie une chaîne de caractères larges dans un buffer, avec vérification de la taille du buffer          |
| `wcscat_s`    | Concatène deux chaînes de caractères larges avec vérification de la taille du buffer                    |
| `wcsncpy_s`   | Copie une chaîne de caractères larges dans un buffer avec une taille maximale                           |
| `strtok_s`    | Découpe une chaîne de caractère en tokens de manière sécurisée                                          |

#### `gets`

La fonction `gets` est une fonction dangereuse qui a été retirée du langage avec C11 et marquée obsolète en C99. Elle lit une ligne de texte depuis l'entrée standard et la stocke dans un buffer. Le problème, entre autre partagé par d'autres fonctions, est que la fonction ne vérifie pas la taille du buffer, ce qui peut provoquer un dépassement de tampon. Il est recommandé d'utiliser la fonction `fgets` à la place, qui prend en paramètre la taille du buffer. Pour comprendre le problème, voici un exemple de code vulnérable :

```c
#include <stdio.h>

int main() {
   char buffer[10];
   char password[10];
   gets(buffer);

   printf("Buffer :   '%s'\n", buffer);
   printf("Password : '%s'\n", password);
}
```

Dans cet exemple, l'utilisateur peut entrer une chaîne de caractères de plus de 10 caractères, ce qui provoquera un dépassement de tampon. La fonction `gets` ne vérifie pas la taille du buffer et écrira dans la mémoire adjacente, en l'occurrence la variable `password`. Cela peut être exploité par un attaquant pour écrire du code malveillant dans la mémoire et exécuter ce code.

#### `scanf`

La fonction `scanf` est une autre fonction dangereuse comme `gets` ne vérifie pas la taille du buffer. L'erreur classique se produit avec le format `%s` qui lit une chaîne de caractères sans vérifier la taille du buffer. Une solution est d'utiliser `%10s` pour limiter la taille de la chaîne à 10 caractères plus le caractère nul de fin de chaîne.


### Mauvaises pratiques

Cette section regroupe les mauvaises pratiques constatées lors mon expérience professionnelle de développeurs ainsi que les pièges dans lesquels mes étudiants tombent régulièrement.

#### Retour de scanf

Bon sang, c'est probablement ce que je répète le plus souvent: **Toujours vérifier la valeur de retour de `scanf`**. Cette fonction retroune le nombre d'éléments qui a été lus, ou `EOF` si la fin du fichier est atteinte. Si vous attendez de lire 3 variables, vous devez vérifier que le retour est bien égal à 3. Sinon, vous avez un problème.

```c
int a, b, c;
if (scanf("%d %d %d", &a, &b, &c) != 3) {
    fprintf(stderr, "Erreur de lecture\n");
    return 1;
}
```

#### Realloc

La fonction `realloc` est une fonction dangereuse car elle peut échouer et retourner `NULL`. Si vous ne stocker pas le retour de `realloc` dans une variable temporaire, vous allez perdre le pointeur sur la mémoire allouée précédemment et vous ne pourrez plus jamais la libérer. C'est pourquoi la valeur de retour de `realloc` doit toujours être stockées dans un pointeur temporaire et vérifiée.

```c
int *tab = malloc(10 * sizeof(int));
if (tab == NULL) {
    fprintf(stderr, "Erreur d'allocation\n");
    return 1;
}

{
    int *tmp = realloc(tab, 20 * sizeof(int));
    if (tmp == NULL) {
        fprintf(stderr, "Erreur de réallocation\n");
        free(tab);
        return 1;
    }
    tab = tmp;
}
```

#### Erreur et free

Lorsqu'une erreur survient dans une fonction, il est important de libérer les ressources allouées avant de quitter la fonction. Si vous oubliez de libérer la mémoire allouée, vous aurez une fuite de mémoire. Cela peut être critique dans un programme qui tourne en continu, car la mémoire allouée ne sera jamais libérée et le programme finira par planter. Lorsque vous avez plusieurs éléments à nettoyer, c'est l'une des seule fois où il est acceptable d'utiliser un `goto`:

```c
void function() {
    if (test_error1) goto error;
    // ...
    if (test_error2) goto error;
    // ...
    if (test_error3) goto error;
    // ...

  error:
    free(ptr1);
    free(ptr2);
    free(ptr3);
    return;
}
```

### Vulnérabilités

Ce chapitre aborde les vulnérabilités classiques en C tel que le *buffer overflow*, le *remote code execution*, l'attaque par format de chaîne, l'attaque de type, etc.

#### Buffer overflow

Les attaquants peuvent exploiter les dépassements de tampon pour écraser les adresses de retour sur la pile, permettant ainsi l'exécution de code arbitraire. Il s'agit de l'une des failles de sécurité les plus critiques dans les programmes C. Par exemple, dans une fonction vulnérable, l'attaquant peut injecter un shellcode dans le tampon et modifier l'adresse de retour pour pointer vers ce shellcode.

#### Remote code execution

Les dépassements de tampon, mal gérés, peuvent permettre à un attaquant de contrôler à distance le flux d'exécution d'un programme C, menant à une exécution de code arbitraire à distance.

#### Attaque par format de chaîne

En utilisant des chaînes de format mal sécurisées dans des fonctions comme `printf`, un attaquant peut accéder à des zones de mémoire sensibles, voire exécuter du code arbitraire.

```c
char userInput[100];
scanf("%s", userInput);
printf(userInput);  // Vulnérabilité de format
```

#### Attaque de type

L'attaque *use-after-free* consiste à exploiter un pointeur qui pointe vers une zone mémoire qui a été libérée. L'attaquant peut alors réallouer cette zone mémoire et écrire du code malveillant dedans.


### Thread Safety

Un programme ou une fonction est dit *thread-safe* lorsqu'il peut être utilisé simultanément par plusieurs threads sans risque de corruption de données, d'interblocage ou de conditions de concurrence. En C, la gestion de la concurrence est laissée à la charge du programmeur. Il est donc de la responsabilité du développeur de garantir la *thread-safety* de son code. Néanmoins le développeur n'a pas une maîtrise complète de son code code,  certaines fonctions de la bibliothèque standard sont précompilées et l'implémentation est généralement opaque à l'utilisateur. Un certain nombre de ces fonctions ne sont pas *thread-safe*.

En effet, certaines fonctions sont dites *stateful*, c'est-à-dire qu'elles utilisent des variables globales pour conserver un état entre les appels. Cela peut poser problème si plusieurs threads utilisent la même fonction en même temps. L'exemple ls plus évident est la fonction `rand` qui utilise une variable globale pour conserver l'état du générateur de nombres pseudo-aléatoires. Chaque appel à `rand` modifie cette variable globale et donc influence le résultat des appels suivants. Une autre fonction bien connue est `strtok` qui utilise également un état interne et qui n'est par conséquent pas *thread-safe*. Pour cette dernière, il est recommandé d'utiliser la fonction `strtok_r` à la place, qui est la version sécurisée.

Certains langages plus modernes comme le Rust ou le Go intègrent nativement la gestion de la concurrence dans le langage. En Rust, par exemple, le compilateur vérifie à la compilation que le code est *thread-safe* et ne contient pas de conditions de concurrence. En Go, la gestion de la concurrence est simplifiée par l'utilisation de goroutines et de canaux, mais en C, il faut gérer la concurrence manuellement.

Ce qu'il faut retenir c'est que la majorité des fonctions de la bibliothèque standard du C ne sont pas *thread-safe*. Il est donc important de faire les recherches préalables avant de les utiliser dans un contexte multithreadé.

## Normes

Dans le domaine du développement en C, la sécurité et la qualité du code sont régies par des normes rigoureuses qui visent à assurer la fiabilité et la robustesse des systèmes, notamment dans les secteurs critiques tels que l’automobile, le médical et l’aérospatial. Ces normes permettent de prévenir les erreurs fatales et de garantir un code de haute qualité, en particulier dans des environnements où les conséquences d’une défaillance peuvent être graves. Elles définissent un ensemble de bonnes pratiques et de contraintes visant à minimiser les comportements indéfinis, les vulnérabilités, et à maximiser la sûreté fonctionnelle.

### MISRA C

[MISRA](https://fr.wikipedia.org/wiki/MISRA_C) (*Motor Industry Software Reliability Association*) est un ensemble de règles de codage destinées à améliorer la sécurité et la qualité du code en langage C, initialement développé pour l'industrie automobile. Au fil des années, MISRA C est devenu une référence non seulement dans le domaine de l’automobile, mais aussi dans d’autres industries où la sécurité est primordiale.

Les règles de MISRA C ont pour but d’éviter des constructions de code dangereuses, de limiter l’utilisation de certaines fonctionnalités du langage C susceptibles de provoquer des comportements indéfinis, et d’améliorer la lisibilité et la maintenabilité du code. Il existe plusieurs versions de la norme (p. ex. : MISRA C:1998, MISRA C:2004, MISRA C:2012), chacune apportant des évolutions pour prendre en compte les nouvelles réalités du développement logiciel.

Les règles de MISRA C sont classées en trois catégories :

**Règles obligatoires (*Mandatory*)**

:   Elles doivent impérativement être respectées sans exception. Leur violation peut conduire à des comportements indéterminés, des bugs critiques, voire des failles de sécurité. Voici un exemple de règle obligatoire :

    >Ne jamais utiliser la fonction dangereuse `malloc()` dans un contexte temps réel sans vérifier si la mémoire a bien été allouée.

**Règles nécessaires (Required)**

:   Ces règles doivent être suivies, mais elles permettent une certaine flexibilité si des justifications solides sont fournies. Si une règle n’est pas respectée, il est impératif de documenter la raison de l'écart et de prouver que la sécurité n'en est pas compromise. Voici un exemple :

    >Limiter l’usage des conversions implicites de types pour éviter des erreurs de précision.

**Règles recommandées (Advisory)**

:   Elles sont fortement encouragées pour améliorer la qualité générale du code, mais leur non-application n’est pas forcément dangereuse, à condition qu’elle soit justifiée, par exemple :

    >Préférer l’utilisation de macros à la place des constantes magiques dans le code pour améliorer la lisibilité.

Un concept clé de la norme MISRA C est la **matrice de justification**. Lorsqu’une règle **Required** ou **Advisory** n’est pas respectée, il est indispensable d’expliquer pourquoi et de justifier la décision. Cette documentation précise pourquoi l’écart est acceptable et quelles précautions ont été prises pour atténuer les risques associés.

Par exemple, si une équipe de développement choisit de ne pas respecter une règle concernant l'utilisation d'une fonction spécifique dans un système embarqué critique, une analyse approfondie doit être effectuée pour démontrer que cette décision n’aura pas d’impact négatif sur la sécurité globale du système.

MISRA C favorise donc une approche pragmatique où l’objectif n’est pas de suivre aveuglément les règles, mais de les appliquer intelligemment, en justifiant tout écart d’une manière rigoureuse et traçable.

Certaines règles MISRA peuvent sembler restrictives ou contraignantes et ne servir ni la lisibilité du code, ni la sécurité. Par exemple, la règle recommandée MISRA-C:2012 15.5 décrète que : *A function should have a single point of exit at the end*. Dit autremement, une fonction ne peut pas avoir plusieurs `return`.

Le point de retour unique est requis par la norme IEC 61508, qui concerne les systèmes embarqués critiques ainsi que l'ISO 26262 pour l'industrie automobile. L'argumentaire est qu'un retour prématuré peut mener à des omission involontaires de nettoyage de la mémoire ou de libération de ressources.

Ces règles, nombreuses, ont des rationels toujours fondés mais qui peuvent parfois être en contradiction avec les bonnes pratiques de développement moderne. Prenons l'exemple suivant de cette fonction qui n'a qu'un point de retour. Elle implique un schéma plus compliqué et une variable supplémentaire pour stocker le résultat de retour.

```c
int foo(FILE *fp, char *buffer, size_t size) {
    int error = 0;
    if (fp != NULL) {
        if (buffer != NULL) {
            if (size > 0) {
                fread(buffer, 1, size, fp);
            } else {
                error = 4;
            }
        } else {
            error = 3;
        }
    } else {
        error = 2;
    }
    return error;
}
```

En s'autorisant plusieurs points de retour, le code est plus lisible et plus concis :

```c
int foo(FILE *fp, char *buffer, size_t size) {
    if (fp == NULL) return 2;
    if (buffer == NULL) return 3;
    if (size == 0) return 4;
    fread(buffer, 1, size, fp);
    return 0;
}
```

L'objectif n'est pas ici de vous monter contre MISRA-C qui est une excellente norme, mais de vous montrer qu'il est important d'avoir un esprit critque et de ne pas suivre aveuglément les règles. Cette règle en question n'est que recommandée, la norme vous pousse à vous interroger sur la pertinence de l'appliquer ou non, de s'assurer que vous comprenez les risques et les bénéfices.

Voici pour information quelques règles de la norme MISRA C:2012 :

Table: Exemples de règles MISRA C:2012

| Règle     | Description                                                               | Catégorie |
| --------- | ------------------------------------------------------------------------- | --------- |
| Rule 1.1  | Les fichiers source ne doivent pas contenir de code non standard          | Mandatory |
| Rule 1.2  | Les fichiers source doivent être conformes à la norme ISO 9899:1999       | Mandatory |
| Rule 2.1  | Tout code inutile doit être supprimé                                      | Required  |
| Rule 8.7  | Les objets non utilisés doivent être supprimés                            | Required  |
| Rule 10.1 | Les types de données ne doivent pas être mélangés dans les expressions    | Required  |
| Rule 11.3 | Un cast entre des pointeurs de types différents ne doit pas être effectué | Required  |
| Rule 14.3 | Les contrôles de boucles doivent être constants et définis                | Required  |
| Rule 15.5 | Il doit y avoir une clause `default` dans chaque instruction `switch`     | Required  |
| Rule 16.7 | Les arguments de fonction ne doivent pas être ignorés                     | Required  |
| Rule 17.2 | Les index des tableaux doivent être dans les limites du tableau           | Required  |
| Rule 18.1 | La mémoire dynamique (`malloc`, `free`) ne doit pas être utilisée         | Required  |
| Rule 8.13 | Les variables automatiques doivent être initialisées avant utilisation    | Advisory  |
| Rule 17.5 | Ne pas accéder directement à un tableau avec des pointeurs                | Advisory  |
| Rule 20.4 | Ne pas utiliser `printf`, `scanf`, `sprintf` de la bibliothèque standard  | Advisory  |

### ISO 26262

La norme **ISO 26262** est une norme internationale pour la sécurité fonctionnelle (*functional safety*) dans l'industrie automobile. Elle couvre le cycle de vie entier du développement des systèmes embarqués dans les véhicules, de la conception initiale à la production et la maintenance. Cette norme est cruciale dans les véhicules modernes où l’électronique et le logiciel jouent un rôle fondamental dans la sécurité (systèmes d’assistance à la conduite, gestion moteur, etc.).

Les exigences clés de cette norme sont :

**Classification ASIL** (*Automotive Safety Integrity Level*)

: Elle indique le niveau de criticité du système. Il est classé de **A** (le plus faible) à **D** (le plus critique), et les exigences de développement augmentent avec le niveau de criticité. Par exemple, un système de freinage ABS est classé ASIL D, car une défaillance de ce système peut entraîner des accidents graves.

**Tests et couverture du code**

: La norme impose la réalisation de tests rigoureux pour garantir que le code est exempt de bugs critiques. Un niveau de couverture du code élevé est exigé, souvent plus de 95 pour cent, avec des tests unitaires, des tests de stress et des tests d’intégration qui couvrent aussi bien les chemins normaux que les cas extrêmes.

**Vérification et validation**

: Un processus rigoureux de vérification et de validation doit être mis en place pour s’assurer que toutes les exigences de sécurité sont respectées. Cela inclut des revues de code, des tests de sécurité, des analyses de risques, etc.

Rappelez-vous, développer du code pour l'automobile c'est lent, c'est cher, c'est compliqué. C'est lent car chaque changement doit être validé, chaque ligne de code doit être testée. C'est cher car les tests sont coûteux et les outils sont chers (parce qu'ils sont certifiés). C'est compliqué car il faut respecter des normes, des standards, des processus.

### IEC 62304

La norme **IEC 62304** est une norme internationale dédiée aux logiciels de dispositifs médicaux. Elle spécifie les processus de développement, de maintenance et de gestion des risques associés aux logiciels critiques utilisés dans les appareils médicaux, tels que les systèmes de monitoring, les appareils d’imagerie médicale ou encore les pacemakers.

Elle est très similaires à l'ISO 26262, mais adaptée aux dispositifs médicaux. Les exigences de sécurité sont tout aussi strictes, car une défaillance d’un logiciel médical peut avoir des conséquences dramatiques pour les patients. La classification médicale est similaire à l'ASIL de l'ISO 26262, allant de **A** (le moins critique) à **C** (le plus critique).

## Compilateur certifié

Dans le contexte de l’application des normes comme l’ISO 26262 et l’IEC 62304, le choix du compilateur est critique. Un compilateur non certifié peut introduire des comportements non déterministes ou des optimisations dangereuses qui ne respectent pas les contraintes de sûreté.

Contrairement à ce que l’on pourrait penser, des compilateurs populaires comme **GCC** ou **Clang** ne sont pas certifiés pour une utilisation dans des systèmes critiques nécessitant une conformité aux normes de sécurité. Cela signifie que, bien qu’ils soient extrêmement performants et largement utilisés dans l’industrie générale, ils ne peuvent pas être utilisés tels quels dans des systèmes répondant à des normes comme l’ISO 26262 ou l’IEC 62304.

Pour les projets critiques, des compilateurs certifiés tels que **Green Hills**, **IAR Systems**, ou **Tasking** sont souvent utilisés. Ces compilateurs sont conformes aux exigences de sécurité, et leur comportement est rigoureusement vérifié pour garantir qu’ils ne produisent pas de code incorrect ou dangereux dans des environnements critiques. Ces compilateurs offrent également des fonctionnalités de suivi et d’audit qui facilitent la conformité avec les normes de sécurité. Ils intègrent généralement MISRA C et d’autres règles de codage directement.
