# Structures

Les structures sont des déclarations spécifiques permettant de regrouper une liste de variables dans un même bloc mémoire et permettant de s'y référer à partir d'une référence commune. Historiquement le type `struct` a été dérivé de `ALGOL 68`. Il est également utilisé en C++ et est similaire à une classe.

Il faut voir une structure comme un conteneur à variables qu'il est possible de véhiculer comme un tout.

La structure suivante décrit un agrégat de trois grandeurs scalaires formant un point tridimensionnel :

```c
struct {
    double x;
    double y;
    double z;
};
```

Il ne faut pas confondre l'écriture ci-dessus avec ceci, dans lequel il y a un bloc de code avec trois variables locales déclarées :

```c
{
    double x;
    double y;
    double z;
};
```

En utilisant le mot-clé `struct` devant un bloc, les variables déclarées au sein de ce bloc ne seront pas réservées en mémoire. Autrement dit, il ne sera pas possible d'accéder à `x` puisqu'il n'existe pas de variable `x`. En revanche, un nouveau conteneur contenant trois variables est défini, mais pas encore déclaré.

La structure ainsi déclarée n'est pas très utile telle quelle, en revanche elle peut-être utilisée pour déclarer une variable de type `struct` :

```c
struct {
    double x;
    double y;
    double z;
} point;
```

À présent on a déclaré une variable `point` de type `struct` contenant trois éléments de type `double`. L'affectation d'une valeur à cette variable utilise l'opérateur `.` :

```c
point.x = 3060426.957;
point.y = 3192003.220;
point.z = 4581359.381;
```

Comme `point` n'est pas une primitive standard, mais un conteneur à primitive, il n'est pas correct d'écrire `point = 12`. Il est essentiel d'indiquer quel élément de ce conteneur on souhaite accéder.

Ces coordonnées sont un clin d'œil aux [Pierres du Niton](https://fr.wikipedia.org/wiki/Pierres_du_Niton) qui sont deux blocs de roche erratiques déposés par le glacier du Rhône lors de son retrait après la dernière glaciation. Les coordonnées sont exprimées selon un repère géocentré ; l'origine étant le centre de la Terre. Ces pierres sont donc situées à 4.5 km du centre de la Terre, une valeur qui aurait représenté, pour être convenablement déterminée, un sacré défi pour [Axel Lidenbrock](https://fr.wikipedia.org/wiki/Voyage_au_centre_de_la_Terre) et son fulmicoton.

Généralement les structures sont utilisées pour communiquer des données complexes entre différentes fonctions d'un même fichier ou entre différents fichiers. C'est pour cette raison que l'on retrouve généralement ces définitions en dehors de toute fonction :

```c
struct Point {
    double x;
    double y;
};

struct Point point_add(struct Point a, struct Point b) {
    return (struct Point){
        .x = a.x + b.x,
        .y = a.y + b.y
    };
}

void point_print(struct Point p) {
    printf("(%g,%g)", p.x, p.y);
}

int main(void) {
    struct Point p = {1., 2.};
    struct Point q = {3., 4.};
    struct Point r = point_add(p, q);
    point_print(r);
}
```

## Structures nommées

L'écriture que l'on a vue initialement `struct { ... };` est appelée structure anonyme, c'est-à-dire qu'elle n'a pas de nom. Telle quelle elle ne peut pas être utilisée et elle ne sert donc pas à grand chose. En revanche, il est possible de déclarer une variable de ce type en ajoutant un identificateur à la fin de la déclaration `struct { ... } nom;`. Néanmoins la structure est toujours anonyme.

Le langage C prévoit la possibilité de nommer une structure pour une utilisation ultérieure en rajoutant un nom après le mot clé `struct` :

```c
struct Point {
    double x;
    double y;
    double z;
};
```

Pour ne pas confondre un nom de structure avec un nom de variable, on préférera un identificateur en capitales ou en écriture *camel-case*. Maintenant qu'elle est nommée, il est possible de déclarer plusieurs variables de ce type ailleurs dans le code :

```c
struct Point foo;
struct Point bar;
```

Dans cet exemple, on déclare deux variables `foo` et `bar` de type `struct Point`. Il est donc possible d'accéder à `foo.x` ou `bar.z`.

Rien n'empêche de déclarer une structure nommée et d'également déclarer une variable par la même occasion :

```c
struct Point {
    double x;
    double y;
    double z;
} foo;
struct Point bar;
```

Notons que les noms de structures sont stockés dans un espace de noms différent de celui des variables. C'est-à-dire qu'il n'y a pas de collision possible et qu'un identifiant de fonction ou de variable ne pourra jamais être comparé à un identifiant de structure. Aussi, l'écriture suivante, bien que perturbante, est tout à fait possible :

```c
struct point { double x; double y; double z; };
struct point point;
point.x = 42;
```

## Initialisation

Une structure se comporte à peu de chose près comme un tableau sauf que les éléments de la structure ne s'accèdent pas avec l'opérateur crochet, `[]` mais avec l'opérateur `.`. Néanmoins une structure est représentée en mémoire comme un contenu linéaire. Notre structure `struct Point` serait identique à un tableau de trois `double` et par conséquent l'initialisation suivante est possible :

```c
struct Point point = { 3060426.957, 3192003.220, 4581359.381 };
```

Néanmoins on préfèrera la notation suivante, équivalente :

```c
struct Point point = { .x=3060426.957, .y=3192003.220, .z=4581359.381 };
```

Comme pour un tableau, les valeurs omises sont initialisées à zéro. Et de la même manière qu'un tableau, il est possible d'initialiser une structure à zéro avec `= {0};`.

Il faut savoir que **C99** restreint l'ordre dans lequel les éléments peuvent être initialisés. Ce dernier doit être l'ordre dans lequel les variables sont déclarées dans la structure.

Notons que des structures comportant des types différents peuvent aussi être initialisées de la même manière :

```c
struct Product {
    int weight; // Grams
    double price; // Swiss francs
    int category;
    char name[64];
}

struct Product apple = {321, 0.75, 24, "Pomme Golden"};
```

## Tableaux de structures

Une structure est un type comme un autre. Tout ce qui peut être fait avec `char` ou `double` peut donc être fait avec `struct`. Et donc, il est aussi possible de déclarer un tableau de structures. Ici, donnons l'exemple d'un tableau de points initialisés :

```c
struct Point points[3] = {
    {.x=1, .y=2, .z=3},
    {.z=1, .x=2, .y=3},
    {.y=1}
};
```

Assigner une nouvelle valeur à un point est facile :

```c
point[2].x = 12;
```

## Structures en paramètres

L'intérêt d'une structure est de pouvoir passer ou retourner un ensemble de données à une fonction. On a vu qu'une fonction ne permet de retourner qu'une seule primitive. Une structure est ici considérée comme un seul conteneur et l'écriture suivante est possible :

```c
struct Point generate_point(void) {
    struct Point p = {
        .x = rand(),
        .y = rand(),
        .z = rand()
    };

    return p;
}
```

Il est également possible de passer une structure en paramètre d'une fonction :

```c
double norm(struct point p) {
    return sqrt(p.x * p.x + p.y * p.y + p.z * p.z);
}

int main(void) {
    struct Point p = { .x = 12.54, .y = -8.12, .z = 0.68 };

    double n = norm(p);
}
```

Contrairement aux tableaux, les structures sont toujours passées par valeur, c'est-à-dire que l'entier du contenu de la structure sera copié sur la pile (*stack*) en cas d'appel à une fonction. En revanche, en cas de passage par pointeur, seule l'adresse de la structure est passée à la fonction appelée qui peut dès lors modifier le contenu :

```c
struct Point {
    double x;
    double y;
};

void foo(struct Point m, struct Point *n) {
    m.x++;
    n->x++;
}

int main(void) {
    struct Point p = {0}, q = {0};
    foo(p, &q);
    printf("%g, %g\n", p.x, q.x);
}
```

Le résultat affiché sera `0.0, 1.0`. Seule la seconde valeur est modifiée.

!!! hint
    Lorsqu'un membre d'une structure est accédé, via son pointeur, on utilise la notation `->` au lieu de `.` car il est nécessaire de déréférencer le pointeur. Il s'agit d'un sucre syntaxique permettant d'écrire `p->x` au lieu de `(*p).x`

## Structures flexibles

Introduits avec C99, les membres de structures flexibles ou *flexible array members* (§6.7.2.1) est un membre de type tableau d'une structure défini sans dimension. Ces membres ne peuvent apparaître qu'à la fin d'une structure.

```c
struct Vector {
    char name[16]; // name of the vector
    size_t len; // length of the vector
    double array[]; // flexible array member
};
```

Cette écriture permet par exemple de réserver un espace mémoire plus grand que la structure de base, et d'utiliser le reste de l'espace comme tableau flexible.

```c
struct Vector *vector = malloc(1024);
strcpy(vector->name, "Mon vecteur");
vector->len = 1024 - 16 - 4;
for (int i = 0; i < vector->len; i++)
    vector->array[i] = ...
```

Ce type d'écriture est souvent utilisé pour des contenus ayant un en-tête fixe comme des images BMP ou des fichiers sons WAVE.

## Structure de structures

On comprend aisément que l'avantage des structures et le regroupement de variables. Une structure peut être la composition d'autres types composites.

Nous déclarons ici une structure `struct Line` composée de `struct Point` :

```c
struct Line {
    struct Point a;
    struct Point b;
};
```

L'accès à ces différentes valeurs s'effectue de la façon suivante :

```c
struct Line line = {.a.x = 23, .a.y = 12, .b.z = 33};
printf("%g, %g", line.a.x, line.b.x);
```

## Alignement mémoire

Une structure est agencée en mémoire dans l'ordre de sa déclaration. C'est donc un agencement linéaire en mémoire :

```c
struct Line lines[2]; // Chaque point est un double, codé sur 8 bytes.
```

Ci-dessous est représenté l'offset mémoire (en bytes) à laquelle est stocké chaque membre de la structure, ainsi que l'élément correspondant.

```text
0x0000 line[0].a.x
0x0008 line[0].a.y
0x0010 line[0].a.z
0x0018 line[0].b.x
0x0020 line[0].b.y
0x0028 line[0].b.z
0x0030 line[1].a.x
0x0038 line[1].a.y
0x0040 line[1].a.z
0x0048 line[1].b.x
0x0050 line[1].b.y
0x0048 line[1].b.z
```

Néanmoins dans certains cas, le compilateur se réserve le droit d'optimiser l' [alignement mémoire](https://fr.wikipedia.org/wiki/Alignement_en_m%C3%A9moire). Une architecture 32-bits aura plus de facilité à accéder à des grandeurs de 32 bits or, une structure composée de plusieurs entiers 8-bits demanderait au processeur un coût additionnel pour optimiser le stockage d'information. Considérons par exemple la structure suivante :

```c
struct NoAlign
{
    int8_t c;
    int32_t d;
    int64_t i;
    int8_t a[3];
};
```

Imaginons pour comprendre qu'un casier mémoire sur une architecture 32-bits est assez grand pour y stocker 4 bytes. Tentons de représenter en mémoire cette structure en *little-endian*, en considérant des casiers de 32-bits :

```text
 c    d             i              a
┞─╀─┬─┬─┐ ┌─╀─┬─┬─┐ ┌─┬─┬─┬─┐ ┌─╀─┬─┬─┐
│c│d│d│d│ │d│i│i│i│ │i│i│i│i│ │i│a│a│a│
│0│0│1│2│ │3│0│1│2│ │3│4│5│6│ │7│0│1│2│
└─┴─┴─┴─┘ └─┴─┴─┴─┘ └─┴─┴─┴─┘ └─┴─┴─┴─┘
    A         B         C         D
```

On constate que la valeur `d` est à cheval entre deux casiers. De même que la valeur `i` est répartie sur trois casiers au lieu de deux. Le processeur communique avec la mémoire en  utilisant des *bus mémoire*, ils sont l'analogie d'une autoroute qui ne peut accueillir que des voitures, chacune ne pouvant transporter que 4 passagers. Un passager ne peut pas arpenter l'autoroute sans voiture. Le processeur est la gare de triage et s'occupe de réassembler les passagers, et l'opération consistant à demander à un passager de sortir de la voiture `B` pour s'installer dans une autre, ou même se déplacer de la place du conducteur à la place du passager arrière prend du temps.

Le compilateur sera donc obligé de faire du zèle pour accéder à d. formellement l'accès à `d` pourrait s'écrire ainsi :

```c
int32_t d = (data[0] << 8) | (data[1] & 0x0F);
```

Pour éviter ces manœuvres, le compilateur, selon l'architecture donnée, va insérer des éléments de rembourrage (*padding*) pour forcer l'alignement mémoire et ainsi optimiser les lectures. Ce sont des éléments vides qui ne sont pas accessibles par l'utilisateur final. Dit autrement, c'est comme choisir de ne mettre qu'un seul passager dans la voiture. Ce n'est pas optimal sur le plan du bilan carbone, mais c'est plus rapide pour le processeur.

La même structure que ci-dessus sera fort probablement implémentée de la façon suivante :

```c
struct Align
{
    int8_t c;
    int8_t __pad1[3]; // Inséré par le compilateur
    int32_t d;
    int64_t i;
    int8_t a[3];
    int8_t __pad2; // Inséré par le compilateur
};
```

En reprenant notre analogie de voitures, le stockage est maintenant fait comme ceci :

```text
┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐
│c│ │ │ │ │d│d│d│d│ │i│i│i│i│ │i│i│i│i│ │a│a│a│ │
│0│ │ │ │ │0│1│2│3│ │0│1│2│3│ │4│5│6│7│ │0│1│2│ │
└─┴─┴─┴─┘ └─┴─┴─┴─┘ └─┴─┴─┴─┘ └─┴─┴─┴─┘ └─┴─┴─┴─┘
    A         B         C         D         E
```

Le compromis est qu'une voiture supplémentaire est nécessaire, mais le processeur n'a plus besoin de réagencer les passagers.
L'accès à `d` est ainsi facilité au détriment d'une perte substantielle de l'espace de stockage.

Ceci étant, en changeant l'ordre des éléments dans la structure pour que chaque membre soit aligné sur 32-bits, il est possible d'obtenir un meilleur compromis :

```c
struct Align
{
    int32_t d;
    int64_t i;
    int8_t a[3];
    int8_t c;
};
```

```text
┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐
│d│d│d│d│ │i│i│i│i│ │i│i│i│i│ │a│a│a│c│
│0│1│2│3│ │0│1│2│3│ │4│5│6│7│ │0│1│2│3│
└─┴─┴─┴─┘ └─┴─┴─┴─┘ └─┴─┴─┴─┘ └─┴─┴─┴─┘
    A         B         C         D
```

L'option `-Wpadded` de GCC permet de lever une alerte lorsqu'une structure est alignée par le compilateur. Si l'on utilise par exemple une structure pour écrire un fichier binaire respectant un format précis par exemple l'en-tête d'un fichier BMP. Et que cette structure `BitmapFileHeader` est enregistrée avec `fwrite(header, sizeof(BitmapFileHeader), ...)`. Si le compilateur rajoute des éléments de rembourrage, le fichier BMP serait alors compromis. Il faudrait donc considérer l'alerte `Wpadded` comme une erreur critique.

Pour pallier à ce problème, lorsqu'une structure mémoire doit être respectée dans un ordre précis. Une option de compilation non standard existe. La directive `#pragma pack` permet de forcer un type d'alignement pour une certaine structure. Considérons par exemple la structure suivante :

```c
struct Test
{
    char a;
    int b;
    char c;
};
```

Elle serait très probablement représentée en mémoire de la façon suivante :

```text
┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐
│a│ │ │ │ │b│b│b│b│ │c│ │ │ │
│0│ │ │ │ │0│1│2│3│ │0│ │ │ │
└─┴─┴─┴─┘ └─┴─┴─┴─┘ └─┴─┴─┴─┘
    A         B         C
```

En revanche si elle est décrite en utilisant un *packing* sur 8-bits, avec `#pragma pack(1)` on aura l'alignement mémoire suivant :

```text
┌─┬─┬─┬─┐ ┌─┬─┬─┬─┐
│a│b│b│b│ │b│c│ │ │
│0│0│1│2│ │3│1│ │ │
└─┴─┴─┴─┘ └─┴─┴─┴─┘
    A         B
```

## Fichier WAV

Le format de fichier WAV est un format de fichier standard pour les fichiers audio numériques. Il est basé sur le format RIFF (Resource Interchange File Format) qui est un format de fichier générique pour l'échange de données. Ce format est très ancien et a été introduit par Microsoft en 1991. Il est néanmoins encore utilisé aujourd'hui pour stocker des fichiers audio non compressés car il est simple et ne nécessite pas de licence.

Prenons l'exemple concrêt de la structure d'un fichier audio WAV :

![Fichier WAV](/assets/images/wav.drawio)

Cette structure peut être définie de la façon suivante :

```c
#pragma pack(1)
struct WavHeader
{
    char riff_tag[4];
    uint32_t file_size;
    char wave_tag[4];
    char fmt_tag[4];
    uint32_t fmt_length;
    uint16_t audio_format;
    uint16_t num_channels;
    uint32_t sample_rate;
    uint32_t byte_rate;
    uint16_t block_align;
    uint16_t bits_per_sample;
    char data_tag[4];
    uint32_t data_size;
};
```

Conserver le bon alignement mémoire est ici crutial car l'objectif est d'écrire les données dans un fichier audio. Voici l'exemple d'un programme qui génère un fichier audio :

```c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>

#define SAMPLE_RATE 44100 // Fréquence d'échantillonnage [Hz]
#define AMPLITUDE 32760   // Amplitude du signal (valeur maximale pour 16 bits)

#pragma pack(1)
struct WavHeader
{
    char riff_tag[4];
    uint32_t file_size;
    char wave_tag[4];
    char fmt_tag[4];
    uint32_t fmt_length;
    uint16_t audio_format;
    uint16_t num_channels;
    uint32_t sample_rate;
    uint32_t byte_rate;
    uint16_t block_align;
    uint16_t bits_per_sample;
    char data_tag[4];
    uint32_t data_size;
};

int generate_sine_wave(const char *filename, double frequency, double duration)
{
    const int num_samples = (int)(SAMPLE_RATE * duration);
    int16_t *buffer = (int16_t *)malloc(num_samples * sizeof(int16_t));

    // Remplissage du buffer avec le signal sinusoidal
    for (int i = 0; i < num_samples; ++i) {
        buffer[i] = (int16_t)(AMPLITUDE * sin(2.0 * M_PI *
                              frequency * i / SAMPLE_RATE));
    }

    // Initialisation de l'en-tête WAV avec une liste d'initialisation
    struct WavHeader header = {
        .riff_tag = {'R', 'I', 'F', 'F'},
        .file_size = 36 + num_samples * sizeof(int16_t),
        .wave_tag = {'W', 'A', 'V', 'E'},
        .fmt_tag = {'f', 'm', 't', ' '},
        .fmt_length = 16,
        .audio_format = 1,
        .num_channels = 1,
        .sample_rate = SAMPLE_RATE,
        .byte_rate = SAMPLE_RATE * sizeof(int16_t),
        .block_align = sizeof(int16_t),
        .bits_per_sample = 16,
        .data_tag = {'d', 'a', 't', 'a'},
        .data_size = num_samples * sizeof(int16_t)};

    // Écriture dans le fichier
    FILE *file = fopen(filename, "wb");
    if (!file)
    {
        printf("Erreur lors de l'ouverture du fichier %s\n", filename);
        free(buffer);
        return -1;
    }

    fwrite(&header, sizeof(struct WavHeader), 1, file);
    fwrite(buffer, sizeof(int16_t), num_samples, file);
    fclose(file);
    free(buffer);
    return 0;
}

int main() {
    generate_sine_wave("sine.wav", 440.0, 5.0);
}
```

# Champs de bits

Les champs de bits sont des structures dont une information supplémentaire est ajoutée: le nombre de bits utilisés.

Prenons l'exemple du [module I2C](http://www.ti.com/lit/ug/sprug03b/sprug03b.pdf) du microcontrôleur TMS320F28335. Le registre `I2CMDR` décrit à la page 23 est un registre 16-bits qu'il conviendrait de décrire avec un champ de bits :

```c
struct I2CMDR {
    int  bc  :3;
    bool fdf :1;
    bool stb :1;
    bool irs :1;
    bool dlb :1;
    bool rm  :1;
    bool xa  :1;
    bool trx :1;
    bool mst :1;
    bool stp :1;
    bool _reserved :1;
    bool stt  :1;
    bool free :1;
    bool nackmod :1;
};
```

Activer le bit `stp` (bit numéro 12) devient une opération triviale :

```c
struct I2CMDR i2cmdr;

i2cmdr.stp = true;
```

Alors qu'elle demanderait une manipulation de bit sinon :

```c
int32_t i2cmdr;

i2cmdr |= 1 << 12;
```

Notons que les champs de bits, ainsi que les structures seront déclarés différemment selon que l'architecture cible est *little-endian* ou *big-endian*.

Cette technique est particulièrement utile pour manipuler des registres de microcontrôleurs ou des fichiers binaires, elle est souvent couplée à des unions pour permettre un accès soit par champ de bits, soit par entier.

## Compound Literals

Naïvement traduit en *littéraux composés*, un *compound literal* est une méthode de création d'un type composé "à la volée" utilisé de la même façon que les transtypages.

Reprenons notre structure Point `struct Point` vue plus haut. Si l'on souhaite changer la valeur du point `p` il faudrait on pourrait écrire ceci :

```c
struct Point p; // Déclaré plus haut

// ...

{
    struct Point q = {.x=1, .y=2, .z=3};
    p = q;
}
```

Notons que passer par une variable intermédiaire `q` n'est pas très utile. Il serait préférable d'écrire ceci :

```c
p = {.x=1, .y=2, .z=3};
```

Néanmoins cette écriture mènera à une erreur de compilation, car le compilateur cherchera à déterminer le type de l'expression `{.x=1, .y=2, .z=3}`. Il est alors essentiel d'utiliser la notation suivante :

```c
p = (struct Point){.x=1, .y=2, .z=3};
```

Cette notation de littéraux composés peut également s'appliquer aux tableaux. L'exemple suivant montre l'initialisation d'un tableau à la volée passé à la fonction `foo` :

```c
void foo(int array[3]) {
    for (int i = 0; i < 3; i++) printf("%d ", array[i]);
}

void main() {
    foo((int []){1,2,3});
}
```

!!! exercise "Mendeleïev"

    Chaque élément du tableau périodique des éléments comporte les propriétés suivantes :

    - Un nom jusqu'à 20 lettres
    - Un symbole jusqu'à 2 lettres
    - Un numéro atomique de 1 à 118 (2019)
    - Le type de l'élément

        - Métaux (Alcalin, Alcalino-terreux, Lanthanides, Actinides, Métaux de transition, Métaux pauvres)
        - Métalloïdes
        - Non-métaux (Autres, Halogène, Gaz noble)

    - La période: un entier de 1 à 7
    - Le groupe: un entier de 1 à 18

    Déclarer une structure de données permettant de stocker tous les éléments chimiques de telle façon qu'ils puissent être accédés comme :

    ```c
    assert(strcmp(table.element[6].name, "Helium") == 0);
    assert(strcmp(table.element[54].type, "Gaz noble") == 0);
    assert(table.element[11].period == 3);

    Element *el = table.element[92];
    assert(el->atomic_weight == 92);
    ```

## Création de types

Le mot clé `typedef` permet de déclarer un nouveau type. Il est particulièrement utilisé conjointement avec les structures et les unions afin de s'affranchir de la lourdeur d'écriture (préfixe `struct`), et dans le but de cacher la complexité d'un type à l'utilisateur qui le manipule.

L'exemple suivant déclare un type `Point` et un prototype de fonction permettant l'addition de deux points.

```c
typedef struct {
    double x;
    double y;
} Point;

Point add(Point a, Point b);
```

## Types de données abstraits

Un [type de donnée abstrait](wiki:abstract-type) (**ADT** pour Abstract Data Type) cache généralement une structure dont le contenu n'est pas connu de l'utilisateur final. Ceci est rendu possible par le standard (C99 §6.2.5) par l'usage de types incomplets.

Pour mémoire, un type incomplet décrit un objet dont on ne connaît pas sa taille en mémoire.

L'exemple suivant déclare un nouveau type structure qui n'est alors pas (encore) connu dans le fichier courant :

```c
typedef struct Unknown *Known;

int main() {
    Known foo; // Autorisé, le type est incomplet

    foo + 1; // Impossible car la taille de foo est inconnue.
    foo->key; // Impossible car le type est incomplet.
}
```

De façon générale, les types abstraits sont utilisés dans l'écriture de bibliothèques logicielles lorsqu'il est important que l'utilisateur final ne puisse pas compromettre le contenu du type et en forçant cet utilisateur à ne passer que par des fonctions d'accès.

Prenons le cas du fichier `foobar.c` lequel décrit une structure `struct Foo` et un type `Foo`. Notez que le type peut être déclaré avant la structure. `Foo` restera abstrait jusqu'à la déclaration complète de la structure `struct Foo` permettant de connaître sa taille. Ce fichier contient également trois fonctions :

- `init` permet d'initialiser la structure ;
- `get` permet de récupérer la valeur contenue dans `Foo` ;
- `set` permet d'assigner une valeur à `Foo`.

En plus, il existe un compteur d'accès `count` qui s'incrémente lorsque l'on assigne une valeur et se décrémente lorsque l'on récupère une valeur.

```c
#include <stdlib.h>

typedef struct Foo Foo;

struct Foo {
    int value;
    int count;
};

void init(Foo** foo) {
    *foo = malloc(sizeof(Foo)); // Allocation dynamique
    (*foo)->count = (*foo)->value = 0;
}

int get(Foo* foo) {
    foo->count--;
    return foo->value;
}

void set(Foo* foo, int value) {
    foo->count++;
    foo->value = value;
}
```

Évidemment, on ne souhaite pas qu'un petit malin compromette ce compteur en écrivant maladroitement :

```c
foo->count = 42; // Hacked this !
```

Pour s'en protéger, on a recours à la compilation séparée (voir chapitre sur la compilation séparée [TranslationUnits]) dans laquelle le programme est découpé en plusieurs fichiers. Le fichier `foobar.h` contiendra tout ce qui doit être connu du programme principal, à savoir les prototypes des fonctions, et le type abstrait :

```c
#pragma once

typedef struct Foo Foo;

void init(Foo** foo);
int get(Foo* foo);
void set(Foo* foo, int value);
```

Ce fichier sera inclus dans le programme principal `main.c` :

```c
#include "foobar.h"
#include <stdio.h>

int main() {
    Foo *foo;

    init(&foo);
    set(foo, 23);
    printf("%d\n", get(foo));
}
```

En résumé, un type abstrait impose l'utilisation de fonctions intermédiaires pour modifier le type. Dans la grande majorité des cas, ces types représentent des structures qui contiennent des informations internes qui ne sont pas destinées à être modifiées par l'utilisateur final.
