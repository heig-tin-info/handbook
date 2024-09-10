# Philosophie

La philosophie d'un bon développeur repose sur plusieurs principes de programmation relevant majoritairement du bon sens de l'ingénieur. Les vaudois l'appelant parfois: **le bon sens paysan** comme l'aurait sans doute confirmé  [Jean Villard dit Gilles](https://fr.wikipedia.org/wiki/Jean_Villard).

## Rasoir d'Ockham

![Illustration humoristique du rasoir d'Ockham](/assets/images/razor.jpg)

Le [rasoir d'Ockham](https://fr.wikipedia.org/wiki/Rasoir_d%27Ockham) expose en substance que les multiples ne doivent pas être utilisés sans nécessité. C'est un principe d'économie, de simplicité et de parcimonie. Il peut être résumé par la devise [Shadok](https://en.wikipedia.org/wiki/Les_Shadoks), non sans une pointe d'ironie : "Pourquoi faire simple quand on peut faire compliqué ?"

En philosophie, un [rasoir](https://fr.wikipedia.org/wiki/Rasoir_(philosophie)) est une méthode heuristique visant à éliminer les explications invraisemblables d'un phénomène donné. Ce principe tire son nom de Guillaume d'Ockham, un penseur du XIVe siècle, bien que son origine remonte probablement à Empédocle (Ἐμπεδοκλῆς), aux environs de 450 avant J.-C.

Ce principe trouve une résonance particulière en programmation, domaine où le développeur ne peut appréhender la totalité d'un logiciel, intrinsèquement insaisissable à l'œil humain. Seuls la simplicité et l'art de la conception logicielle peuvent le préserver du chaos, car un programme, quel qu'en soit l'envergure, peut demeurer limpide pour peu que chaque strate de son architecture reste claire et intelligible pour quiconque souhaiterait contribuer à l'œuvre d'autrui.

## L'effet Dunning-Kruger

L' est un biais cognitif qui se manifeste par une surestimation des compétences d'une personne. Les personnes les moins compétentes dans un domaine ont tendance à surestimer leurs compétences, tandis que les personnes les plus compétentes ont tendance à les sous-estimer.

L'effet [Dunning-Kruger](wiki:dunning-kruger) est un biais cognitif où les individus tendent à surestimer leurs compétences. Paradoxalement, ce sont les moins expérimentés dans un domaine qui s'illusionnent le plus sur leurs capacités, tandis que les experts, eux, ont tendance à sous-évaluer leur maîtrise.

![Illustration satirique de l'effet Dunning-Kruger](/assets/images/dunning-kruger.drawio)

J'ai souvent observé ce biais de surconfiance chez mes étudiants et collègues, et je n'en ai pas été exempt moi-même. Il est en effet difficile de jauger avec précision son propre niveau de compétence, et ce n'est qu'en se confrontant au regard critique de ses pairs que l'on prend véritablement conscience de ses lacunes. Soumettre son code à l'examen d'autrui peut être une démarche intimidante, mais elle s'avère être une source d'enrichissement inestimable.

!!! note

    L'effet Dunning-Kruger ne fait pas consensus au sein de la communauté scientifique, mais il est souvent cité en psychologie populaire.

## Ultracrépidarianisme

L'[ultracrépidarianisme](wiki:ultracrépidarianisme), terme rare mais puissant, désigne l'art de s'exprimer avec assurance sur des sujets que l'on ne maîtrise guère. Ce phénomène, aussi ancien que la parole elle-même, se manifeste lorsque des individus, ignorants des nuances et des subtilités d'un domaine, s'érigent en experts. Étienne Klein, physicien et philosophe des sciences, a popularisé ce mot en France, mettant en garde contre les dangers de cette posture, notamment à l'époque du Covid-19, où les voix des véritables spécialistes furent souvent noyées par le vacarme de ceux qui, en sachant moins, parlaient davantage.

Dans le domaine de l'informatique, ce travers est particulièrement prégnant. Les développeurs, en première ligne de la complexité technique, se voient fréquemment dictés leur conduite par ceux qui ne partagent ni leur expertise ni leur compréhension des enjeux. Directeurs, managers, clients – tous s'autorisent à émettre des avis, à imposer des choix, souvent au mépris des réalités techniques. Cette immixtion, loin d'être anodine, est une source constante de frustration. Pire encore, elle peut mener à des désastres techniques, notamment lorsque des décisions mal avisées entraînent une accumulation de dette technique, cette gangrène silencieuse du code que l'on reporte de corriger, jusqu'au jour où l'effort nécessaire pour la résorber devient titanesque, voire impossible.

Ainsi, l'ultracrépidarianisme, en s'infiltrant dans les rouages du développement logiciel, menace l'équilibre délicat entre création et rigueur, innovation et solidité. Il est un rappel de l'importance de la modestie, de la nécessité d'écouter ceux qui savent, et de la sagesse qu'il y a à reconnaître ses propres limites.

## Philosophie de conception

Ces principes constituent des lignes directrices essentielles pour aider le développeur à structurer son code de manière à le rendre plus lisible, plus maintenable et moins susceptible de contenir des erreurs humaines.

Il ne suffit pas qu'un programme fonctionne correctement ou qu'il satisfasse les attentes d'un supérieur hiérarchique; l'attitude du programmeur va bien au-delà du simple acte de coder. Cet état d'esprit ne s'enseigne pas, il s'acquiert avec l'expérience.

Voici les quatre principes les plus emblématiques :

DRY

: [Ne vous répétez pas.][dry] (*Do not repeat yourself.*)

KISS

: [Restez simple, stupide.][kiss] (*Keep it simple, stupid.*)

SSOT

: [Une seule source de vérité.][ssot] (*Single source of truth.*)

YAGNI

: [Vous n'en aurez pas besoin.][yagni] (*You ain't gonna need it.*)


[](){#dry}

### DRY

**Ne vous répétez pas** (*Don't Repeat Yourself*) ! Je le répète : **ne vous répétez pas** ! Ce principe fondamental du développement logiciel vise à éviter la [redondance de code](https://fr.wikipedia.org/wiki/Duplication_de_code). Dans leur ouvrage incontournable, [The Pragmatic Programmer](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer), Andrew Hunt et David Thomas le formulent ainsi :

> Dans un système, toute connaissance doit avoir une représentation unique, non ambiguë et faisant autorité.

En d'autres termes, le programmeur doit rester constamment vigilant, prêt à entendre une alarme mentale, rouge, vive et bruyante dès qu'il s'apprête à utiliser la combinaison ++ctrl+c++ (ou ++command+c++), suivie de ++ctrl+v++ (ou ++command+v++). Dupliquer du code, quelle que soit la quantité, est **toujours** une mauvaise pratique, car cela trahit souvent un [code smell](https://fr.wikipedia.org/wiki/Code_smell), signal évident que le code pourrait être simplifié et optimisé.

L'exemple de code suivant présente une violation du principe **DRY** : la fonction `display` est appelée deux fois. Dans les deux cas, elle reçoit un pointeur sur un fichier, ce qui indique qu'une simplification est possible.

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

[](){#kiss}

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

[](){#yagni}

### YAGNI

YAGNI est un anglicisme de *you ain't gonna need it* qui peut être traduit par: vous n'en aurez pas besoin. C'est un principe très connu en développent Agile XP ([Extreme Programming](https://fr.wikipedia.org/wiki/Extreme_programming)) qui stipule qu'un développeur logiciel ne devrait pas implémenter une fonctionnalité à un logiciel tant que celle-ci n'est pas absolument nécessaire.

Ce principe combat le biais du développeur à vouloir sans cesse démarrer de nombreux chantiers sans se focaliser sur l'essentiel strictement nécessaire d'un programme et permettant de satisfaire au cahier des charges convenu avec le partenaire/client.

[](){#ssot}

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

Le [Zen de Python](https://fr.wikipedia.org/wiki/Zen_de_Python) est un ensemble de 19 principes publiés en 1999 par Tim Peters. Largement accepté par la communauté de développeurs et il est connu sous le nom de **PEP 20**.

Voici le texte original anglais :

>Beautiful is better than ugly.<br>
>Explicit is better than implicit.<br>
>Simple is better than complex.<br>
>Complex is better than complicated.<br>
>Flat is better than nested.<br>
>Sparse is better than dense.<br>
>Readability counts.<br>
>Special cases aren't special enough to break the rules.<br>
>Although practicality beats purity.<br>
>Errors should never pass silently.<br>
>Unless explicitly silenced.<br>
>In the face of ambiguity, refuse the temptation to guess.<br>
>There should be one—and preferably only one—obvious way to do it.<br>
>Although that way may not be obvious at first unless you're Dutch.<br>
>Now is better than never.<br>
>Although never is often better than right now.<br>
>If the implementation is hard to explain, it's a bad idea.<br>
>If the implementation is easy to explain, it may be a good idea.<br>
>Namespaces are one honking great idea—let's do more of those!<br>


Un code est meilleur s'il est beau, esthétique, que les noms des variables, l'alignement et la mise en forme sont cohérents et forment une unité.

Un code se doit être explicite, et réellement traduire l'intention du développeur. Il est ainsi préférable d'écrire `#!c u = v / 4` plutôt que `#!c u >>= 2`. De la même manière, détecter si un nombre est pair est plus explicite avec `#!c if (n % 2 == 0)` que `#!c if (n & 1)`.

## The code taste

Voici une version améliorée de votre texte, en tenant compte du style que vous appréciez :

Lors d'une [conférence TED](https://www.ted.com/talks/linus_torvalds_the_mind_behind_linux) en 2016, le créateur de Linux, Linus Torvalds, introduisit un concept qu'il nomma *code taste*, que l'on pourrait traduire par *le goût du code*.

Il présenta l'exemple de code C suivant, interrogeant son auditoire sur le fait de savoir si ce code était de bon goût :

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

Torvalds répondit sans détour que ce code était de mauvais goût, le qualifiant de *vilain* et *moche*. En effet, ce test placé après la boucle `while` dénote par rapport au reste du code. Cette dissonance esthétique suggère qu'il existe une implémentation plus élégante, car lorsque le code paraît laid, il y a fort à parier qu'une solution de meilleur goût peut être trouvée. On dit dans ces cas-là que le code *sent* : ce test est superflu, et il doit exister une manière d'éviter de traiter un cas particulier en choisissant un algorithme mieux conçu.

En réalité, retirer un élément d'une liste chaînée requiert de gérer deux cas distincts :

- Si l'élément se trouve au début de la liste, il faut ajuster le pointeur `head`.
- Dans le cas contraire, il convient de modifier `prev->next`.

Après avoir questionné l'auditoire, Torvalds dévoila une nouvelle implémentation :

```c
void remove_list_entry(List* list, Entry* entry)
{
    Entry** indirect = &head;

    while ((*indirect) != entry)
        indirect = &(*indirect)->next;

    *indirect = entry->next;
}
```

La fonction originellement étalée sur dix lignes est désormais réduite à quatre. Bien que le nombre de lignes importe moins que la lisibilité, cette nouvelle version élimine la gestion des cas particuliers grâce à un adressage indirect beaucoup plus raffiné.

Cependant, un programmeur novice en C pourrait être déconcerté par l'emploi des doubles pointeurs et juger la première version plus lisible. Cela illustre à quel point la connaissance des structures de données et des algorithmes est cruciale pour écrire du code de qualité : on ne s'improvise pas développeur, c'est un art qui demande patience et apprentissage.

Un exemple similaire, plus accessible, est présenté par Brian Barto dans un article publié sur [Medium](https://medium.com/@bartobri/applying-the-linus-tarvolds-good-taste-coding-requirement-99749f37684a). Il y discute de l'initialisation à zéro de la bordure d'un tableau bidimensionnel :

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

**Mastodonte**

: Une fonction est plus longue qu'un écran de haut (~50 lignes)

**Titan**

: Un fichier est plus long que **1000 lignes**.

**Ligne Dieu**

: Une ligne beaucoup trop longue et *de facto* illisible.

**Usine à gaz**

: Une fonction à plus de **trois** paramètres

    ```c
    void make_coffee(int size, int mode, int mouture, int cup_size,
        bool with_milk, bool cow_milk, int number_of_sugars);
    ```

**Miroir magique**

: Du code est dupliqué. Du code est dupliqué.

**Pamphlets touristiques**

:   Les commentaires expliquent le comment du code et non le pourquoi

    ```c
    // Additionne une constante avec une autre pour ensuite l'utiliser
    double u = (a + cst);
    u /= 1.11123445143; // division par une constante inférieure à 2
    ```

**Arbre de Noël**

:   plus de deux structures de contrôles sont impliquées

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

**Téléportation sauvage**

:   Usage de `goto`, où quand le code saute d'un endroit à l'autre sans logique apparente.

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

**Jumeaux diaboliques**

:   Plusieurs variables avec des noms très similaires

    ```c
    int advice = 11;
    int advise = 12;
    ```

**Action à distance**

:  Une fonction qui tire les ficelles à distance grâce aux variables globales.

    ```c
    void make_coffee() {
        powerup_nuclear_reactor = true;
        number_of_coffee_beans_to_harvest = 62;
        ...
    }
    ```

**Ancre de bateau**

: Un composant inutilisé, mais gardé dans le logiciel pour des raisons politiques (YAGNI)

**Cyclomatisme aigu**

: Quand trop de structures de contrôles sont nécessaires pour traiter un problème apparemment simple

**Attente active**

: Une boucle qui ne contient qu'une instruction de test, attendant la condition

    ```c
    while (true) {
        if (finished) break;
    }
    ```

**Valeur Bulgare**

: Popularisé par Jacques-André Porchet, une grandeur Bulgare est une valeur magique qui n'a pas de sens pour un non-initié et qui semble être sortie de nulle part.

    ```c
    double it_works_with_this_value = 1.11123445143;
    ```

**Objet divin**

: Quand un composant logiciel assure trop de fonctions essentielles (KISS)

**Coulée de lave** [](){#lava-flow}

: Lorsqu'un code immature est mis en production

  En novembre 1990 à 14h25, la société AT&T effecue une mise à jour de son   réseau téléphonique. Un bug dans le code de mise à jour provoque un crash du réseau entraînant une interruption de service de 9 heures affectant quelque 50 millions d'appels et coûtant à l'entreprise 60 millions de dollars. (Source: [The 1990 AT&T Long Distance Network Collapse](https://users.csc.calpoly.edu/~jdalbey/SWE/Papers/att_collapse))

**Chirurgie au fusil de chasse**

: Quand l'ajout d'une fonctionnalité logicielle demande des changements multiples et disparates dans le code ([Shotgun surgery](https://en.wikipedia.org/wiki/Shotgun_surgery)).

## Conclusion

La quête d'un code de qualité repose sur des principes philosophiques et méthodologiques essentiels. Le **rasoir d'Ockham** encourage la simplicité en éliminant les éléments superflus, tandis que l'**effet Dunning-Kruger** met en garde contre la surestimation de ses compétences, rappelant l'importance de la remise en question et du retour critique. Des doctrines telles que **DRY** (ne vous répétez pas), **KISS** (restez simple), **SSOT** (une seule source de vérité) et **YAGNI** (vous n'en aurez pas besoin) guident le développeur vers une conception épurée et efficace.

Le **Zen de Python** illustre cette philosophie par dix-neuf aphorismes valorisant la beauté, la lisibilité et la simplicité du code. Linus Torvalds, créateur de Linux et de Git, a souligné l'importance du *code taste* ou "goût du code", démontrant qu'une implémentation élégante résulte souvent d'une réflexion profonde sur les structures de données et les algorithmes, plutôt que d'une complexité inutile.

Enfin, reconnaître et éviter les **odeurs de code** (*code smells*), ces indicateurs de mauvaise conception comme les fonctions tentaculaires, les duplications ou les commentaires mal pensés, est crucial. En identifiant ces *antipatterns* — qu'ils se manifestent sous la forme d'un "Arbre de Noël" de structures conditionnelles imbriquées ou d'une "Téléportation sauvage" via des `goto` intempestifs—le développeur s'assure de produire un code maintenable, clair et performant.
