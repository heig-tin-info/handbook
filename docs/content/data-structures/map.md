# Tableaux de hachage

Les tableaux de hachage (*Hash Table*) sont une structure particulière dans laquelle une fonction dite de *hachage* est utilisée pour transformer les entrées en des indices d'un tableau.

L'objectif est de stocker des chaînes de caractères correspondant a des noms simples ici utilisés pour l'exemple. Une possible répartition serait la suivante :

![Tableau de hachage simple](../../assets/images/hash-linear.drawio)

Si l'on cherche l'indice correspondant à `Ada`, il convient de pouvoir calculer la valeur de l'indice correspondant à partir de la valeur de la chaîne de caractère. Pour calculer cet indice aussi appelé *hash*, il existe une infinité de méthodes. Dans cet exemple, considérons une méthode simple. Chaque lettre est identifiée par sa valeur ASCII et la somme de toutes les valeurs ASCII est calculée. Le modulo 10 est ensuite calculé sur cette somme pour obtenir une valeur entre 0 et 9. Ainsi nous avons les calculs suivants :

```console
Nom    Valeurs ASCII     Somme  Modulo 10
---    --------------    -----  ---------
Mia -> {77, 105, 97}  -> 279 -> 4
Tim -> {84, 105, 109} -> 298 -> 1
Bea -> {66, 101, 97}  -> 264 -> 0
Zoe -> {90, 111, 101} -> 302 -> 5
Jan -> {74, 97, 110}  -> 281 -> 6
Ada -> {65, 100, 97}  -> 262 -> 9
Leo -> {76, 101, 111} -> 288 -> 2
Sam -> {83, 97, 109}  -> 289 -> 3
Lou -> {76, 111, 117} -> 304 -> 7
Max -> {77, 97, 120}  -> 294 -> 8
Ted -> {84, 101, 100} -> 285 -> 10
```

Pour trouver l'indice de `"Mia"` il suffit donc d'appeler la fonction suivante :

```c
int hash_str(char *s) {
    int sum = 0;
    while (*s != '\0') sum += s++;
    return sum % 10;
}
```

L'assertion suivante est donc vraie :

```c
assert(strcmp(table[hash_str("Mia")], "Mia") == 0);
```

Rechercher `"Mia"` et obtenir `"Mia"` n'est certainement pas l'exemple le plus utile. Néanmoins il est possible d'encoder plus qu'une chaîne de caractère et utiliser plutôt une structure de donnée :

```c
struct Person {
    char name[3 + 1 /* '\0' */];
    struct {
        int month;
        int day;
        int year;
    } born;
    enum {
        JOB_ASTRONOMER,
        JOB_INVENTOR,
        JOB_ACTRESS,
        JOB_LOGICIAN,
        JOB_BIOLOGIST
    } job;
    char country_code; // For example 41 for Switzerland
};
```

Dans ce cas, le calcul du hash se ferait sur la première clé d'un élément :

```c
int hash_person(struct Person person) {
    int sum = 0;
    while (*person.name != '\0') sum += s++;
    return sum % 10;
}
```

L'accès à une personne à partir de la clé se résout donc en `O(1)` car il n'y a aucune itération ou recherche à effectuer.

Cette [vidéo](https://www.youtube.com/watch?v=KyUTuwz_b7Q) YouTube explique bien le fonctionnement des tableaux de hachage.

### Collisions

Lorsque la **fonction de hachage** est mal choisie, un certain nombre de collisions peuvent apparaître. Si l'on souhaite par exemple ajouter les personnes suivantes :

```text
Sue -> {83, 117, 101} -> 301 -> 4
Len -> {76, 101, 110} -> 287 -> 1
```

On voit que les positions `4` et `1` sont déjà occupées par Mia et Tim.

Une stratégie de résolution s'appelle [Open adressing](https://en.wikipedia.org/wiki/Open_addressing). Parmi les possibilités de cette stratégie, le *linear probing* consiste à vérifier si la position du tableau est déjà occupée et en cas de collision, chercher la prochaine place disponible dans le tableau :

```c
Person people[10] = {0}

// Add Mia
Person mia = {.name="Mia", .born={.day=1,.month=4,.year=1991}};
int hash = hash_person(mia);
while (people[hash].name[0] != '\0') hash++;
people[hash] = mia;
```

Récupérer une valeur dans le tableau demande une comparaison supplémentaire :

```c
char key[] = "Mia";
int hash = hash_str(key)
while (strcmp(people[hash], key) != 0) hash++;
Person person = people[hash];
```

Lorsque le nombre de collisions est négligeable par rapport à la table de hachage, la recherche d'un élément est toujours en moyenne égale à $O(1)$, mais lorsque le nombre de collisions est prépondérant, la complexité se rapproche de celle de la recherche linéaire $O(n)$ et on perd tout avantage à cette structure de donnée.

Dans le cas extrême, pour garantir un accès unitaire pour tous les noms de trois lettres, il faudrait un tableau de hachage d'une taille $26^3 = 17576$ personnes. L'empreinte mémoire peut être considérablement réduite en stockant non pas une structure `struct Person` mais plutôt l'adresse vers cette structure :

```c
struct Person *people[26 * 26 * 26] = { NULL };
```

Dans ce cas exagéré, la fonction de hachage pourrait être la suivante :

```c
int hash_name(char name[4]) {
    int base = 26;
    return
        (name[0] - 'A') * 1 +
        (name[1] - 'a') * 26 +
        (name[2] - 'a') * 26 * 26;
}
```

### Facteur de charge

Le facteur de charge d'une table de hachage est donné par la relation :

$$
\text{Facteur de charge} = \frac{\text{Nombre total d'éléments}}{\text{Taille de la table}}
$$

Plus ce facteur de charge est élevé, dans le cas du *linear probing*, moins bon sera la performance de la table de hachage.

Certains algorithmes permettent de redimensionner dynamiquement la table de hachage pour conserver un facteur de charge le plus faible possible.

### Chaînage

Le chaînage ou *chaining* est une autre méthode pour mieux gérer les collisions. La table de hachage est couplée à une liste chaînée.

![Chaînage d'une table de hachage](../../assets/images/hash-table.drawio)

### Fonction de hachage

Nous avons vu plus haut une fonction de hachage calculant le modulo sur la somme des caractères ASCII d'une chaîne de caractères. Nous avons également vu que cette fonction de hachage est source de nombreuses collisions. Les chaînes `"Rea"` ou `"Rae"` auront les même *hash* puisqu'ils contiennent les mêmes lettres. De même une fonction de hachage qui ne répartit pas bien les éléments dans la table de hachage sera mauvaise. On sait par exemple que les voyelles sont nombreuses dans les mots et qu'il n'y en a que six et que la probabilité que nos noms de trois lettres contiennent une voyelle en leur milieu est très élevée.

L'idée générale des fonctions de hachage est de répartir **uniformément** les clés sur les indices de la table de hachage. L'approche la plus courante est de mélanger les bits de notre clé dans un processus reproductible.

Une idée **mauvaise** et **à ne pas retenir** pourrait être d'utiliser le caractère pseudo-aléatoire de `rand` pour hacher nos noms :

```c
#include <stdlib.h>
#include <stdio.h>

int hash(char *str, int mod) {
    int h = 0;
    while(*str != '\0') {
        srand(h + *str++);
        h = rand();
    }
    return h % mod;
}

int main() {
    char *names[] = {
        "Bea", "Tim", "Len", "Sam", "Ada", "Mia",
        "Sue", "Zoe", "Rae", "Lou", "Max", "Tod"
    };
    for (int i = 0; i < sizeof(names) / sizeof(*names); i++)
        printf("%s : %d\n", names[i], hash(names[i], 10));
}
```

Cette approche nous donne une assez bonne répartition :

```console
$ ./a.out
Bea : 2
Tim : 3
Len : 0
Sam : 3
Ada : 4
Mia : 3
Sue : 6
Zoe : 5
Rae : 8
Lou : 0
Max : 3
Tod : 1
```

Dans la pratique, on utilisera volontiers des fonctions de hachage utilisées en cryptographies tels que [MD5](https://en.wikipedia.org/wiki/MD5) ou `SHA`. Considérons par exemple la première partie du poème Chanson de Pierre Corneille :

```console
$ cat chanson.txt
Si je perds bien des maîtresses,
J'en fais encor plus souvent,
Et mes voeux et mes promesses
Ne sont que feintes caresses,
Et mes voeux et mes promesses
Ne sont jamais que du vent.

$ md5sum chanson.txt
699bfc5c3fd42a06e99797bfa635f410  chanson.txt
```

Le *hash* de ce texte est exprimé en hexadécimal ( `0x699bfc5c3fd42a06e99797bfa635f410`). Converti en décimal `140378864046454182829995736237591622672` il peut être réduit en utilisant le modulo. Voici un exemple en C :

```c
#include <stdlib.h>
#include <stdio.h>
#include <openssl/md5.h>
#include <string.h>

int hash(char* str, int mod) {
    // Compute MD5
    unsigned int output[4];
    MD5_CTX md5;
    MD5_Init(&md5);
    MD5_Update(&md5, str, strlen(str));
    MD5_Final((char*)output, &md5);

    // 128-bits --> 32-bits
    unsigned int h = 0;
    for (int i = 0; i < sizeof(output)/sizeof(*output); i++) {
        h ^= output[i];
    }

    // 32-bits --> mod
    return h % mod;
}

int main() {
    char *text[] = {
        "La poule ou l'oeuf?",
        "Les pommes sont cuites!",
        "Aussi lentement que possible",
        "La poule ou l'oeuf.",
        "La poule ou l'oeuf!",
        "Aussi vite que nécessaire",
        "Il ne faut pas lâcher la proie pour l’ombre.",
        "Le mieux est l'ennemi du bien",
    };

    for (int i = 0; i < sizeof(text) / sizeof(*text); i++)
        printf("% 2d. %s\n", hash(text[i], 10), text[i]);
}
```

```console
$ gcc hash.c -lcrypto
$ ./a.out
1. La poule ou l'oeuf?
2. Les pommes sont cuites!
3. Aussi lentement que possible
4. La poule ou l'oeuf.
5. La poule ou l'oeuf!
6. Aussi vite que nécessaire
8. Il ne faut pas lâcher la proie pour l’ombre.
9. Le mieux est l'ennemi du bien
```

On peut constater qu'ici les indices sont bien répartis et que la fonction de hachage choisie semble uniforme.