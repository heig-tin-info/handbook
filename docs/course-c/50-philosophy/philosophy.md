# Philosophie

La philosophie d'un bon développeur repose sur plusieurs principes de programmation relevant majoritairement du bon sens de l'ingénieur. Les vaudois l'appelant parfois: **le bon sens paysan** comme l'aurait sans doute confirmé feu [Jean Villard dit Gilles](https://fr.wikipedia.org/wiki/Jean_Villard).

## Rasoir d'Ockham

![Illustration humoristique du rasoir d'Ockham]({assets}/images/razor.jpg)

Le [rasoir d'Ockham](https://fr.wikipedia.org/wiki/Rasoir_d%27Ockham) expose en substance que les multiples ne doivent pas être utilisés sans nécessité. C'est un principe d'économie, de simplicité et de parcimonie. Il peut être résumé par la devise [Shadok](https://en.wikipedia.org/wiki/Les_Shadoks) : "Pourquoi faire simple quand on peut faire compliqué ?"

En philosophie un [rasoir](<https://fr.wikipedia.org/wiki/Rasoir_(philosophie)>) est un principe qui permet de *raser* des explications improbables d'un phénomène. Ce principe tient son nom de Guillaume d'Ockham (XIVe siècle) alors qu'il date probablement d'Empédocle (Ἐμπεδοκλῆς) vers 450 av. J.-C.

Il trouve admirablement bien sa place en programmation où le programmeur ne peut conserver une vue d'ensemble sur un logiciel qui est par nature invisible à ses yeux. Seuls la simplicité et l'art de la conception logicielle sauvent le développeur de la noyade, car un programme peut rester simple, quelle que soit sa taille et si chaque strate de conception reste évidente et compréhensible pour celui qui chercherait à contribuer au projet d'autrui.

## L'effet Dunning-Kruger

L'[effet Dunning-Kruger](https://fr.wikipedia.org/wiki/Effet_Dunning-Kruger) est un biais cognitif qui se manifeste par une surestimation des compétences d'une personne. Les personnes les moins compétentes dans un domaine ont tendance à surestimer leurs compétences, tandis que les personnes les plus compétentes ont tendance à les sous-estimer.

![Illustration satirique de l'effet Dunning-Kruger]({assets}/images/dunning-kruger.drawio)

J'ai vu bien souvent chez mes étudiants et collègues ce biais de surconfiance, et je l'ai moi-même expérimenté. Il est difficile de se rendre compte de son propre niveau de compétence, et il est souvent nécessaire de se confronter à des pairs pour se rendre compte de ses lacunes. Soumettre son code à la critique est par bien des égard une perspective effrayante, mais c'est aussi une source d'enrichissement inestimable.

!!! note

    L'effet Dunning-Kruger ne fait pas consensus au sein de la communauté scientifique, mais il est souvent cité en psychologie populaire.

## Philosophie de conception

Ces principes sont des lignes directrices aidant le développeur à organiser son code pour le rendre plus lisible, plus maintenable, et moins sensible aux erreurs humaines.

Il ne suffit pas d'avoir un programme qui fonctionne, et un supérieur hiérarchique heureux, l'attitude du programmeur transcende l'acte singulier de coder. Cette état d'esprit ne s'enseigne pas, elle vient avec l'exérience.

Voici les quatre principes les plus connus :

<div class="grid cards" markdown>

- **DRY** [Ne vous répétez pas.][dry]{ data-preview }

    ---

    *Do not repeat yourself.*

- **KISS** [Restez simple, stupide.][kiss]{ data-preview }

    ---

    *Keep it simple, stupid.*

    ---

- **SSOT** [Une seule source de vérité.][ssot]{ data-preview }

    ---

    *Single source of truth.*

- **YAGNI** [Vous n'en aurez pas besoin.][yagni]{ data-preview }

    ---

    *You ain't gonna need it.*

</div>

### DRY

**Ne vous répétez pas** (*Don't Repeat Yourself*)! Je répète, **ne vous répétez pas** ! Il s'agit d'une philosophie de développement logiciel évitant la [redondance de code](https://fr.wikipedia.org/wiki/Duplication_de_code). L'excellent livre [The Pragmatic Programmer](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer) de Andrew Hunt et David Thomas décrit cette philosophie en ces termes :

> Dans un système, toute connaissance doit avoir une représentation unique, non ambiguë, faisant autorité.

En d'autres termes, le programmeur doit avoir sans cesse à l'esprit une sonnette d'alarme prête à vrombir lorsque qu'il presse machinalement ++ctrl+c++ ( ++command+c++ ) suivi de ++ctrl+v++ ( ++command+v++ ). Dupliquez du code et, quelle que soit l'envergure de texte concerné est **toujours** une mauvaise pratique, car c'est le plus souvent le signe évident d'un [code smell](https://fr.wikipedia.org/wiki/Code_smell) indiquant que le code peut être simplifié et optimisé.

Le code suivant comprend une erreur **DRY** car la fonction display est appelée deux fois. Dans les deux cas de figure, la fonction `display` reçoit un pointeur sur un fichier, il est donc possible de simplifier ce code.

```c
FILE *fp = NULL;
if (argc > 1) {
    fp = fopen(argv[1], "r");
    display(fp);
}
else {
    display(stdin);
}
```

Voici la version corrigée :

```c
FILE *fp = argc > 1 ? fopen(argv[1], "r") : stdin;
display(fp);
```

### KISS

[Keep it simple, stupid](https://fr.wikipedia.org/wiki/Principe_KISS) est une ligne directrice de conception qui encourage la simplicité d'un développement. Elle est similaire au rasoir d'Ockham, mais plus commune en informatique. Énoncé par [Eric Steven Raymond](https://fr.wikipedia.org/wiki/Eric_Raymond) puis par le [Zen de Python](https://fr.wikipedia.org/wiki/Zen_de_Python) un programme ne doit faire qu'une chose, et une chose simple. C'est une philosophie grandement respectée dans l'univers Unix/Linux. Chaque programme de base du *shell* (`ls`, `cat`, `echo`, `grep`...) ne fait qu'une tâche simple, le nom est court et simple à retenir.

La fonction suivante n'est pas **KISS** car elle est responsable de plusieurs tâches : vérifier les valeurs d'un set de donnée et les afficher :

```c
int process(Data *data, size_t size) {
    // Check consistency and display
    for (int i = 0; i < size; i++) {
        if (data[i].value <= 0)
            data[i].value = 1;

        printf("%lf\n", 20 * log10(data[i].value));
    }
}
```

Il serait préférable de la découper en deux sous-fonctions :

```c
#define TO_LOG(a) (20 * log10(a))

int fix_data(Data *data, const size_t size) {
    for (int i = 0; i < size; i++) {
        if (data[i].value <= 0)
            data[i].value = 1;
    }
}

int display(const Data *data, const size_t size) {
    for (int i = 0; i < size; i++)
        printf("%lf\n", TO_LOG(data[i].value));
}
```

### YAGNI

YAGNI est un anglicisme de *you ain't gonna need it* qui peut être traduit par: vous n'en aurez pas besoin. C'est un principe très connu en développent Agile XP ([Extreme Programming](https://fr.wikipedia.org/wiki/Extreme_programming)) qui stipule qu'un développeur logiciel ne devrait pas implémenter une fonctionnalité à un logiciel tant que celle-ci n'est pas absolument nécessaire.

Ce principe combat le biais du développeur à vouloir sans cesse démarrer de nombreux chantiers sans se focaliser sur l'essentiel strictement nécessaire d'un programme et permettant de satisfaire au cahier des charges convenu avec le partenaire/client.

### SSOT

Ce principe tient son acronyme de [single source of truth](https://en.wikipedia.org/wiki/Single_source_of_truth). Il adresse principalement un défaut de conception relatif aux métadonnées que peuvent être les paramètres d'un algorithme, le modèle d'une base de données ou la méthode usitée d'un programme à collecter des données.

Un programme qui respecte ce principe évite la duplication des données. Des défauts courants de conception sont :

- indiquer le nom d'un fichier source dans le fichier source ;

    ```c
    /**
     * @file main.c
     */
    ```

- stocker la même image, le même document dans différents formats ;

    ```bash
    convert input.jpg -resize 800x800 image-small.jpg
    convert input.jpg -resize 400x400 image-smaller.jpg
    convert input.jpg -resize 10x10 image-tiny.jpg
    git add image-small.jpg image-smaller.jpg image-tiny.jpg
    ```

- stocker dans une base de données le nom *Doe*, prénom *John* ainsi que le nom complet ;

    ```sql
    INSERT INTO users (first_name, last_name, full_name)
    VALUES ('John', 'Doe', 'John Doe');
    ```

- avoir un commentaire C ayant deux vérités contradictoires ;

    ```c
    int height = 206; // Size of Hafþór Júlíus Björnsson which is 205 cm
    ```

- conserver une copie des mêmes données sous des formats différents (un tableau de données brutes et un tableau des mêmes données, mais triées).

    ```bash
    ssconvert data.csv data.xlsx
    libreoffice --headless --convert-to pdf fichier.csv
    git add data.csv data.xlsx data.pdf # Beurk !
    git commit -m "Add all data formats"
    ```

## Zen de Python

Python est un langage de programmation qui devient très populaire, il est certes moins performant que C, mais il se veut être de très haut niveau.

Le [Zen de Python](https://fr.wikipedia.org/wiki/Zen_de_Python) est un ensemble de 19 principes publiés en 1999 par Tim Peters. Largement accepté par la communauté de développeurs et il est connu sous le nom de **PEP 20**.

Voici le texte original anglais :

!!! quote "Zen of Python par Tim Peters"

    Beautiful is better than ugly.<br>
    Explicit is better than implicit.<br>
    Simple is better than complex.<br>
    Complex is better than complicated.<br>
    Flat is better than nested.<br>
    Sparse is better than dense.<br>
    Readability counts.<br>
    Special cases aren't special enough to break the rules.<br>
    Although practicality beats purity.<br>
    Errors should never pass silently.<br>
    Unless explicitly silenced.<br>
    In the face of ambiguity, refuse the temptation to guess.<br>
    There should be one—and preferably only one—obvious way to do it.<br>
    Although that way may not be obvious at first unless you're Dutch.<br>
    Now is better than never.<br>
    Although never is often better than right now.[n 1]<br>
    If the implementation is hard to explain, it's a bad idea.<br>
    If the implementation is easy to explain, it may be a good idea.<br>
    Namespaces are one honking great idea—let's do more of those!<br>


Un code est meilleur s'il est beau, esthétique, que les noms des variables, l'alignement et la mise en forme sont cohérents et forment une unité.

Un code se doit être explicite, et réellement traduire l'intention du développeur. Il est ainsi préférable d'écrire `#!c u = v / 4` plutôt que `#!c u >>= 2`. De la même manière, détecter si un nombre est pair est plus explicite avec `#!c if (n % 2 == 0)` que `#!c if (n & 1)`.

## The code taste

Dans une [conférence](https://www.ted.com/talks/linus_torvalds_the_mind_behind_linux) TED en 2016, le créateur de Linux, Linus Torvald évoqua un principe nommé *code taste* traduisible par *avoir du goût pour le code*.

Il évoqua l'exemple C suivant et demanda à l'auditoire si ce code est de bon goût :

```c
void remove_list_entry(List* list, Entry* entry)
{
    Entry* prev = NULL;
    Entry* walk = list->head;

    while (walk != entry) {
        prev = walk;
        walk = walk->next;
    }

    if (!prev)
        list->head = entry->next;
    else
        prev->next = entry->next;
}
```

Il répondit que ce code est de mauvais goût, qu'il est *vilain* et *moche*, car ce test placé après la boucle `while` jure avec le reste du code et que parce que ce code semble laid, il doit y avoir une meilleure implémentation de meilleur goût. On dit dans ce cas de figure que le code *sent*, ce test est de trop, et il doit y avoir un moyen d'éviter de traiter un cas particulier en utilisant un algorithme meilleur.

Enlever un élément d'une liste chaînée nécessite de traiter deux cas :

- Si l'élément est au début de la liste, il faut modifier `head`
- Sinon il faut modifier l'élément précédent `prev->next`

Après avoir longuement questionné l'auditoire, il présente cette nouvelle implémentation :

```c
void remove_list_entry(List* list, Entry* entry)
{
    Entry** indirect = &head;

    while ((*indirect) != entry)
        indirect = &(*indirect)->next;

    *indirect = entry->next;
}
```

La fonction originale de 10 lignes de code a été réduite à 4 lignes et bien que le nombre de lignes compte moins que la lisibilité du code, cette nouvelle implémentation élimine le traitement des cas d'exception en utilisant un adressage indirect beaucoup plus élégant.

Néanmoins, le néophyte en programmation C pourrait être dérouté par l'usage de double pointeurs et trouverait que la première implémentation est plus lisible. Cela souligne l'importance de la connaissance des structures de données et des algorithmes pour écrire du code de qualité, on ne s'improvise pas développeur&nbsp;: c'est un art.

Un autre exemple similaire et plus simple à comprendre est présenté par Brian Barto sur un article publié sur [Medium](https://medium.com/@bartobri/applying-the-linus-tarvolds-good-taste-coding-requirement-99749f37684a). Il donne l'exemple de l'initialisation à zéro de la bordure d'un tableau bidimensionnel :

```c
for (size_t row = 0; row < GRID_SIZE; ++row)
{
    for (size_t col = 0; col < GRID_SIZE; ++col)
    {
        if (row == 0)
            grid[row][col] = 0; // Top Edge

        if (col == 0)
            grid[row][col] = 0; // Left Edge

        if (col == GRID_SIZE - 1)
            grid[row][col] = 0; // Right Edge

        if (row == GRID_SIZE - 1)
            grid[row][col] = 0; // Bottom Edge
    }
}
```

On constate plusieurs fautes de goût :

1. `GRID_SIZE` pourrait être différent de la réelle taille de `grid`
2. Les valeurs d'initialisation sont dupliquées
3. La complexité de l'algorithme est de $O(n^2)$ alors que l'on ne s'intéresse qu'à la bordure du tableau.

Voici une solution plus élégante :

```c
const size_t length = sizeof(grid[0]) / sizeof(grid[0][0]);
const int init = 0;

for (size_t i = 0; i < length; i++)
{
    grid[i][0] = grid[0][i] = init; // Top and Left
    grid[length - 1][i] = grid[i][length - 1] = init; // Bottom and Right
}
```

## L'odeur du code (*code smell*)

Un code *sent* si certains indicateurs sont au rouge. On appelle ces indicateurs des [antipatterns](https://fr.wikipedia.org/wiki/Antipattern). Voici quelques indicateurs les plus courants :

- **Mastodonte** Une fonction est plus longue qu'un écran de haut (~50 lignes)

- Un fichier est plus long que **1000 lignes**.

- **Ligne Dieu**, une ligne beaucoup trop longue et *de facto* illisible.

- Une fonction à plus de **trois** paramètres

    ```c
    void make_coffee(int size, int mode, int mouture, int cup_size,
        bool with_milk, bool cow_milk, int number_of_sugars);
    ```

- **Copier coller**, du code est dupliqué

- Les commentaires expliquent le comment du code et non le pourquoi

    ```c
    // Additionne une constante avec une autre pour ensuite l'utiliser
    double u = (a + cst);
    u /= 1.11123445143; // division par une constante inférieure à 2
    ```

- **Arbre de Noël**, plus de deux structures de contrôles sont impliquées

    ```c
    if (a > 2) {
        if (b < 8) {
            if (c ==12) {
                if (d == 0) {
                    exception(a, b, c, d);
                }
            }
        }
    }
    ```

- Usage de `goto`

    ```c
    loop:
        i +=1;
        if (i > 100)
            goto end;
    happy:
        happy();
        if (j > 10):
            goto sad;
    sad:
        sad();
        if (k < 50):
            goto happy;
    end:
    ```

- Plusieurs variables avec des noms très similaires

    ```c
    int advice = 11;
    int advise = 12;
    ```

- **Action à distance** par l'emploi immodéré de variables globales

    ```c
    void make_coffee() {
        powerup_nuclear_reactor = true;
        number_of_coffee_beans_to_harvest = 62;
        ...
    }
    ```

- **Ancre de bateau**, un composant inutilisé, mais gardé dans le logiciel pour des raisons politiques (YAGNI)

- **Cyclomatisme aigu**, quand trop de structures de contrôles sont nécessaires pour traiter un problème apparemment simple

- **Attente active**, une boucle qui ne contient qu'une instruction de test, attendant la condition

    ```c
    while (true) {
        if (finished) break;
    }
    ```

- **Objet divin** quand un composant logiciel assure trop de fonctions essentielles (KISS)

- **Coulée de lave** lorsqu'un code immature est mis en production

    En novembre 1990 à 14h25, la société AT&T effecue une mise à jour de son   réseau téléphonique. Un bug dans le code de mise à jour provoque un crash du   réseau entraînant une interruption de service de 9 heures affectant quelque   50 millions d'appels et coûtant à l'entreprise 60 millions de dollars. (Source&nbsp;: [The 1990 AT&T Long Distance Network Collapse](https://users.csc.calpoly.edu/~jdalbey/SWE/Papers/att_collapse))

- **Chirurgie au fusil de chasse** quand l'ajout d'une fonctionnalité logicielle demande des changements multiples et disparates dans le code ([Shotgun surgery](https://en.wikipedia.org/wiki/Shotgun_surgery)).
