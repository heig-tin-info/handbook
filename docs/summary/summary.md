---
orphan: true
---

# Résumé

## Introduction

Le langage C a créé en **1972** par [Brian Kernighan](https://fr.wikipedia.org/wiki/Brian_Kernighan) et [Dennis Ritchie](https://fr.wikipedia.org/wiki/Dennis_Ritchie) est s'est dès lors imposé comme le standard industriel pour la programmation embarquée et pour tout développement nécessitant de hautes performances.

Le langage est standardisé par l'ISO (standardisation internationale) et le standard le plus couramment utilisé en 2019 est encore [C99](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf).

Il faut retenir que le C est un langage dit :

- [Impératif](https://fr.wikipedia.org/wiki/Programmation_imp%C3%A9rative): programmation en séquences de commandes
- [Structuré](https://fr.wikipedia.org/wiki/Programmation_structur%C3%A9e): programmation impérative avec des structures de contrôle imbriquées
- [Procédural](https://fr.wikipedia.org/wiki/Programmation_proc%C3%A9durale): programmation impérative avec appels de procédures

Ce sont ses paradigmes de programmation

## Cycle de développement

Le cycle de développement se compose toujours des phases: étude, écriture du cahier des charges, de l'écriture des tests, de la conception du logiciel, du codage à proprement parler et des validations finales. Le modèle en cascade est un bon résumé très utilisé dans l'industrie :

:::{figure} {assets}/figures/dist/software-life-cycle/waterfall.*
Modèle en cascade
:::

## Cycle de compilation

Faire évoluer un logiciel est aussi un processus itératif :

- Editer le code avec un éditeur comme `vi` ou `vscode`
- Compilation et prétraitement
  : ```console
    $ gcc -std=c99 -O2 -Wall -c foo.c -o foo.o
    $ gcc -std=c99 -O2 -Wall -c bar.c -o bar.o
    ```
- Edition des liens
  : ```console
    $ gcc -o foobar foo.o bar.o -lm
    ```
- Tests

## Make

Souvent, pour s'éviter de répéter les mêmes commandes les développeurs utilisent un outil comme `make` qui tire des règles de compilations d'un fichier nommé `Makefile`. Cet outil permet d'automatiquement recompiler les fichiers qui ne sont plus à jour et régénérer automatiquement l'exécutable. Certaines recettes de `make` sont souvent utilisées comme :

- `make all` Pour compiler tout le projet
- `make clean` Pour supprimer tous les fichiers intermédiaires générés
- `make mrproper` Pour supprimer tous les fichiers intermédiaires ainsi que les exécutables produits.
- `make test` Pour exécuter les tests de validation

D'autres recettes peuvent être écrites dans le fichier `Makefile`, mais la courbe d'apprentissage du langage de `make` est raide.

## Linux/POSIX

Un certain nombre de commandes sont utilisées durant ce cours et voici un résumé de ces dernières

| Commande | Description                                                        |
| -------- | ------------------------------------------------------------------ |
| `cat`    | Affiche sur `stdout` le contenu d'un fichier                       |
| `ls`     | Liste le contenu du répertoire courant                             |
| `ls -al` | Liste le contenu du répertoire courant avec plus de détails        |
| `echo`   | Affiche sur `stdout` les éléments passés par argument au programme |
| `make`   | Outil d'aide à la compilation utilisant le fichier `Makefile`      |
| `gcc`    | Compilateur open source largement utilisé dans l'industrie         |
| `vi`     | Éditeur de texte ultra puissant, mais difficile à apprendre        |

### Programmation

## Diagramme de flux

Le diagramme de flux est beaucoup utilisé pour exprimer un algorithme comme celui d'Euclide pour
chercher le plus grand diviseur commun.

:::{figure} {assets}/figures/dist/algorithm/euclide-gcd.*
Algorithme de calcul du PGCD d'Euclide.
:::

### Langage C

## Caractères non imprimables

| Expression | Nom   | Nom anglais       | Description                                  |
| ---------- | ----- | ----------------- | -------------------------------------------- |
| `\n`       | `LF`  | *Line feed*       | Retour à la ligne                            |
| `\v`       | `VT`  | *Vertical tab*    | Tabulation verticale (entre les paragraphes) |
| `\f`       | `FF`  | *New page*        | Saut de page                                 |
| `\t`       | `TAB` | *Horizontal tab*  | Tabulation horizontale                       |
| `\r`       | `CR`  | *Carriage return* | Retour charriot                              |
| `\b`       | `BS`  | *Backspace*       | Retour en arrière, effacement d'un caractère |

## Fin de lignes

Les caractères de fin de ligne dépendent du système d'exploitation et sont appelés **EOL**: *End Of Line*.

| Expression | Nom    | Système d'exploitation       |
| ---------- | ------ | ---------------------------- |
| `\r\n`     | `CRLF` | Windows                      |
| `\r`       | `CR`   | Anciens Macintoshs (\< 2000) |
| `\n`       | `LF`   | Linux/Unix/POSIX             |

## Identificateurs

:::{figure} {assets}/figures/dist/grammar/identifier.*
Grammaire d'un identificateur C
:::

Le format des identificateurs peut également être exprimé par une expression régulière :

```text
^[a-zA-Z_][a-zA-Z0-9_]*$
```

## Variable

Une variable possède 6 paramètres: **nom**, **type**, **valeur**, **adresse**, **portée**, **visibilité**.

Elle peut être: **globale** et dans ce cas elle est automatiquement initialisée à 0 :

```c
int foo;

int main(void) {
    return foo;
}
```

Ou elle peut être locale et dans ce cas il est nécessaire de l'initialiser à une valeur :

```c
int main(void) {
    int foo = 0;
    return foo;
}
```

Il est possible de déclarer plusieurs variables d'un même type sur la même ligne :

```c
int i, j, k;
int m = 32, n = 22;
```

Les conventions de nommage pour une variable sont: `camelCase` et `snake_case`, certains utilisent la notation `PascalCase`.

Les termes `toto`, `tata`, `foo`, `bar` sont souvent utilisés comme noms génériques et sont appelés termes *métasyntaxiques*.

## Constantes littérales

Une constante littérale est une grandeur exprimant une valeur donnée qui n'est pas calculée à l'exécution :

| Expression | Type           | Description                                             |
| ---------- | -------------- | ------------------------------------------------------- |
| `6`        | `int`          | Valeur décimale                                         |
| `12u`      | `unsigned int` | Valeur non signée en notation décimale                  |
| `6l`       | `long`         | Valeur longue en notation décimale                      |
| `010`      | `int`          | Valeur octale                                           |
| `0xa`      | `int`          | Valeur hexadécimale                                     |
| `0b111`    | `int`          | Valeur binaire (uniquement `gcc`, pas standard **C99**) |
| `12.`      | `double`       | Nombre réel                                             |
| `'a'`      | `char`         | Caractère                                               |
| `"salut"`  | `char*`        | Chaîne de caractère                                     |

## Commentaires

Il existe deux types de commentaires :

- Les commentaires de lignes (depuis C99)

  ```c
  // This is a single line comment.
  ```

- Les commentaires de blocs

  ```c
  /* This is a
     Multi-line comment */
  ```

## Fonction main

La fonction main peut s'érire sous deux formes :

```c
int main(void) {
    return 0;
}
```

```c
int main(int argc, char *argv[]) {
    return 0;
}
```

### Numération

Les données dans l'ordinateur sont stockées sous forme binaire et le *type* d'une variable permet de définir son interprétation.

- Une valeur **entière** et **non signée** est exprimée sous la forme binaire pure :
  : ```text
    ┌─┬─┬─┬─┬─┬─┬─┬─┐
    │0│1│0│1│0│0│1│1│ = 0b1010011 = 83
    └─┴─┴─┴─┴─┴─┴─┴─┘
    ```
- Une valeur **entière** et **signée** est exprimée en complément à deux :
  : ```text
    ┌─┬─┬─┬─┬─┬─┬─┬─┐     ┌─┬─┬─┬─┬─┬─┬─┬─┐
    │1│1│0│1│0│0│1│1│ = ! │0│0│1│0│1│1│0│0│ = (-1) * (0b101100 + 1) = -45
    └─┴─┴─┴─┴─┴─┴─┴─┘     └─┴─┴─┴─┴─┴─┴─┴─┘
    ```
- Une valeur **réelle** ou **flottante** est exprimée selon le standard **IEEE-754** et comporte un bit de signe, un exposant et une mantisse.
  : ```
    ┌ Signe 1 bit
    │        ┌ Exposant 8 bits
    │        │                             ┌ Mantisse 23 bits
    ┴ ───────┴──────── ────────────────────┴──────────────────────────
    ┞─╀─┬─┬─┬─┬─┬─┬─┐┌─╀─┬─┬─┬─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┦
    │0│0│0│1│0│0│0│0││0│1│0│0│1│0│0│0││1│1│0│1│1│1│1│1││0│1│0│0│0│0│0│1│
    └─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘
    ```

### Opérateurs

Les opérateurs appliquent une opération entre une ou plusieurs valeurs :

- Les opérateurs **unaire** s'appliquent à un seul opérande (`!12`, `~23`)
- Les opérateurs standards s'appliquent à deux opérandes (`12 ^ 32`)

Les opérateurs ont une priorité et une direction d'associativité:

```text
u = ++a + b * c++ >> 3 ^ 2

Rang  Opérateur  Associativité
----  ---------  -------------
 1    ()++       -->
 2    ++()       <--
 2    +          <--
 2    *          <--
 5    >>         -->
 9    ^          -->
14    =          -->
```

Donc la priorité de ces opérations sera :

```text
(u = ((((++a) + (b * (c++))) >> 3) ^ 2))
```

Dans le cas des opérateurs de pré et post incrémentation, ils sont en effet les plus prioritaires mais leur action est décalée dans le temps au précédent/suivant point de séquence. C'est-à-dire :

```text
a += 1;
(u = (((a + (b * c)) >> 3) ^ 2));
c += 1;
```

## Valeur gauche

Une valeur gauche *lvalue* défini ce qui peut se trouver à gauche d'une affectation. C'est un terme qui apparaît souvent dans les erreurs de compilation. L'exemple suivant retourne l'erreur: *lvalue required as increment operand* car le résultat de `a + b` n'a pas d'emplacement mémoire et il n'est pas possible de l'assigner à quelque chose pour effectuer l'opération de pré-incrémentation.

```c
c = ++(a + b);
```

Dans cet exemple `c` est une valeur gauche

### Types de données

Dans 90% des cas, voici les types qu'un développeur utilisera en C et sur le modèle
de donnée **LP64**

| Type           | Profondeur | Description                      |
| -------------- | ---------- | -------------------------------- |
| `char`         | 8-bit      | Caractère ou valeur décimale     |
| `int`          | 32-bit     | Entier signé                     |
| `unsigned int` | 32-bit     | Entier non signé                 |
| `long long`    | 64-bit     | Entier signé                     |
| `float`        | 32-bit     | Nombre réel (23 bit de mantisse) |
| `double`       | 64-bit     | Nombre réel (54 bit de mantisse) |

Pour s'assurer d'une taille donnée on peut utiliser les types standard **C99** en incluant la bibliothèque `<stdint.h>`

```c
#include <stdint.h>

int main(void) {
    int8_t foo = 0;  // Valeur signée sur 8-bit
    uint32_t bar = 0;  // Valeur non signée sur 32-bit

    uint_least16_t = 0;  // Valeur non signée d'au moins 16-bit
}
```

Les valeurs signées sont exprimées en **complément à deux** c'est-à-dire que les valeurs maximales et minimales sont pour un entier 8-bit de `-128` à `+128`.

La construction des types standards :

:::{figure} {assets}/figures/dist/datatype/ansi-integers.*
:alt: "Entiers standardis\xE9s **C89**"
:width: 100 %
:::

La construction des types portables :

:::{figure} {assets}/figures/dist/datatype/c99-integers.*
:alt: "Entiers standardis\xE9s **C99**"
:width: 100 %
:::

## Caractères

Un caractère est une valeur binaire codée sur 8-bit et dont l'interprétation est confiée à une table de correspondance nommée ASCII :

:::{figure} {assets}/figures/dist/encoding/ascii.*
Table ANSI INCITS 4-1986 (standard actuel)
:::

Seul ces valeurs sont garanties d'être stockées sur 8-bit. Pour les caractères accentués ou les émoticônes, la manière dont ils sont codés en mémoire dépend de l'encodage des caractères. Souvent on utilise le type d'encodage **utf-8**.

Les écritures suivantes sont donc strictement identiques :

```c
char a;

a = 'a';
a = 0x61;
a = 97;
a = 0141;
```

## Chaîne de caractère

Une chaîne de caractère est exprimée avec des guillemets double. Une chaîne de caractère comporte toujours un caractère terminal `\0`.

```c
char str[] = "Hello";
```

La taille en mémoire de cette chaîne de caractère est de 6 *bytes*, 5 caractères et un caractère de terminaison.

## Booléens

En C la valeur `0` est considérée comme fausse (*false*) et une valeur différente de `0` est considérée comme vraie (*true*). Toutes les assertions suivantes sont vraies :

```c
if (42) { /* ... */ }
if (!0) { /* ... */ }
if (true && true || false) { /* ... */ }
```

Pour utiliser les mots clés `true` et `false` il faut utiliser la bibliothèque `<stdbool.h>`

## Promotion implicite

Un type est automatiquement et tacitement promu dans le type le plus général :

```c
char a;
int b;
long long c;
unsigned int d;

a + b // Résultat promu en `int`
a + c // Résultat promu en `long long`
b + d // Résultat promu en `int`
```

Attention aux valeurs en virgule flottante :

```c
int a = 9, b = 2;
double b;

a / b;  // Résultat de type entier, donc 4 et non 4.5
(float)a / b;  // Résultat de type float donc 4.5
b / a;  // Résultat en type double (promotion)
```

## Transtypage

Préfixer une variable ou une valeur avec `(int)` comme dans: `(int)a` permet de convertir explicitement cette variable dans le type donné.

Le transtypage peut être implicite par exemple dans `int a = 4.5`

Ou plus spécifiquement dans :

```c
float u = 0.0;
printf("%f", b); // Promotion implicite de `float` en `double`
```

### Structure de contrôle

## Séquence

Une séquence est déterminée par un bloc de code entre accolades :

```c
{
    int a = 12;
    b += a;
}
```

## Si, sinon

```c
if (condition)
{
    // Si vrai
}
else
{
    // Sinon
}
```

## Si, sinon si, sinon

```c
if (condition)
{
    // Si vrai
}
else if (autre_condition)
{
    // Sinon si autre condition valide
}
else
{
    // Sinon
}
```

## Boucle For

```c
for (int i = 0; i < 10; i++)
{
    // Block exécuté 10 fois
}

k = i; // Erreur car `i` n'est plus accessible ici...
```

## Boucle While

```c
int i = 10;

while (i > 0) {
    i--;
}
```

### Programmes et Processus

| Élément       | Description                                |
| ------------- | ------------------------------------------ |
| `stdin`       | Entrée standard                            |
| `stdout`      | Sortie standard                            |
| `stderr`      | Sortie d'erreur standard                   |
| `argc`        | Nombre d'arguments                         |
| `argv`        | Valeurs des arguments                      |
| `exit-status` | Status de sortie d'un programme `$?`       |
| `signaux`     | Interaction avec le système d'exploitation |

:::{figure} {assets}/figures/dist/process/program.*
Résumé des interactions avec un programme
:::

### Entrées Sorties

## `printf`

Les sorties formatées utilisent `printf` dont le format est :

```text
%[parameter][flags][width][.precision][length]type
```

`parameter` (optionnel)

: Numéro de paramètre à utiliser

`flags` (optionnel)

: Modificateurs: préfixe, signe plus, alignement à gauche ...

`width` (optionnel)

: Nombre **minimum** de caractères à utiliser pour l'affichage de la sortie.

`.precision` (optionnel)

: Nombre **minimum** de caractères affichés à droite de la virgule. Essentiellement, valide pour les nombres à virgule flottante.

`length` (optionnel)

: Longueur en mémoire. Indique la longueur de la représentation binaire.

`type`

: Type de formatage souhaité

:::{figure} {assets}/figures/dist/string/formats.*
Formatage d'un marqueur
:::

### Techniques de programmation

## Masque binaire

Pour tester si un bit est à un :

```c
if (c & 0x040)
```

Pour forcer un bit à zéro :

```c
c &= ~0x02;
```

Pour forcer un bit à un :

```c
c |= 0x02;
```

## Permuter deux variables sans valeur intermédiaire

```c
a = b ^ c;
b = a ^ c;
a = b ^ c;
```
