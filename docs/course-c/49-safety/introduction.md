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

| Fonction     | Description                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------- |
| `strcpy_s`   | Copie une chaîne de caractères dans un buffer, avec vérification de la taille du buffer                 |
| `strcat_s`   | Concatène deux chaînes de caractères avec vérification de la taille du buffer                           |
| `sprintf_s`  | Écrit une chaîne de caractères formatée dans un buffer avec vérification de la taille du buffer         |
| `strncpy_s`  | Copie une chaîne de caractères dans un buffer avec une taille maximale                                  |
| `strncat_s`  | Concatène deux chaînes de caractères avec une taille maximale et vérification de la taille du buffer    |
| `snprintf_s` | Écrit une chaîne de caractères formatée dans un buffer avec une taille maximale et vérification         |
| `memcpy_s`   | Copie une zone mémoire dans une autre zone mémoire, avec vérification de la taille du buffer            |
| `memmove_s`  | Copie une zone mémoire dans une autre zone mémoire, même si les zones se chevauchent, avec vérification |
| `memset_s`   | Remplit une zone mémoire avec une valeur donnée, avec vérification du tampon                            |
| `fopen_s`    | Ouvre un fichier de manière sécurisée                                                                   |
| `freopen_s`  | Rouvre un fichier existant de manière sécurisée                                                         |
| `tmpfile_s`  | Crée un fichier temporaire sécurisé                                                                     |
| `getc_s`     | Lit un caractère d'un fichier de manière sécurisée                                                      |
| `fgets_s`    | Lit une ligne de texte d'un fichier de manière sécurisée, avec gestion de la taille du buffer           |
| `fread_s`    | Lit des blocs de données d'un fichier dans un buffer sécurisé, avec vérification des tailles            |
| `strerror_s` | Renvoie un message d'erreur de manière sécurisée                                                        |
| `bsearch_s`  | Recherche un élément dans un tableau trié de manière sécurisée                                          |
| `qsort_s`    | Trie un tableau de manière sécurisée                                                                    |
| `fscanf_s`   | Lit des données formatées depuis un fichier de manière sécurisée                                        |
| `sscanf_s`   | Lit des données formatées depuis une chaîne de caractères de manière sécurisée                          |

### Mauvaises pratiques

(à compléter)

### Hacking

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
