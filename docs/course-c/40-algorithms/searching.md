# Recherche

La recherche est une opération courante en informatique. Il existe plusieurs algorithmes de recherche, chacun ayant ses avantages et inconvénients. Les algorithmes de recherche les plus courants sont la recherche linéaire et la recherche binaire.

## Recherche linéaire

La recherche linéaire est une méthode simple pour trouver un élément dans un tableau. Elle consiste à parcourir naïvement tous les éléments du tableau, un par un, jusqu'à trouver l'élément recherché. Si l'élément est trouvé, la recherche s'arrête et renvoie la position de l'élément dans le tableau. Si l'élément n'est pas trouvé, la recherche renvoie une valeur spéciale pour indiquer que l'élément est absent.

Une implémentation pour une recherche d'entier serait la suivante :

```c
int linear_search(int *array, int size, int search) {
    for (int i = 0; i < size; ++i)
        if (array[i] == search)
            return i;
    return -1;
}
```

Une implémentation plus générique pour une recherche d'élément de type variable peut être réalisée en utilisant une fonction de comparaison laquelle retourne 0 si les deux éléments sont égaux, 1 si le premier est plus grand et -1 si le premier est plus petit.

```c
int cmp_int(void *a, void *b) {
    return *(int *)a - *(int *)b;
}

int linear_search(void *array, int size,
    int element_size, void *search, int (*cmp)(void *, void *)) {
    for (int i = 0; i < size; ++i)
        if (cmp(array + i * element_size, search) == 0)
            return i;
    return -1;
}
```

La complexité de la recherche linéaire est en $O(n)$, où $n$ est la taille du tableau. Si les recherches sont fréquentes, et que la fonction de comparaison est complexe, cette méthode n'est pas la plus efficace.

L'utilisation d'une fonction de comparaison permet de réaliser des recherches sur des tableaux qui ne se limitent pas à des entiers. On peut ainsi rechercher des chaînes de caractères, des structures ou des objets plus complexes. Voici par exemple une fonction de comparaison pour des chaînes de caractères :

```c
int cmp_str(void *a, void *b) {
    return strcmp((char *)a, (char *)b);
}
```

## Recherche dichotomique

La recherche dichotomique est une méthode plus efficace pour trouver un élément dans un tableau mais elle impose que ce dernier soit trié. Elle consiste à diviser le tableau en deux parties égales et à comparer l'élément recherché avec l'élément au milieu du tableau. Si l'élément est égal à l'élément au milieu, la recherche s'arrête. Sinon, si l'élément est plus petit, la recherche continue dans la première moitié du tableau, sinon dans la seconde moitié.

Cette méthode est celle que vous appliquez quand on vous demande de deviner un nombre choisi par un tiers entre 1 et 100. Plutôt que choisir une valeur aléatoire à chaque essai, vous annoncez en premier 50, puis 25 ou 75, puis 12 ou 37 ou 62 ou 87, etc. À chaque essai vous éliminez la moitié des possibilités. On dit que la progression est logarithmique en base 2.

Une implémentation pour une recherche d'entier serait la suivante :

```c
int binary_search(int *array, int size, int search) {
    int left = 0, right = size - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (array[mid] == search)
            return mid;
        if (array[mid] < search)
            left = mid + 1;
        else
            right = mid - 1;
    }
    return -1;
}
```

Elle peut également être généralisée avec une fonction de comparaison ou spécialisée pour un type particulier. La complexité de la recherche dichotomique est en $O(\log n)$, où $n$ est la taille du tableau. Cette méthode est donc beaucoup plus efficace que la recherche linéaire pour des tableaux de grande taille mais elle impose un tri préalable en $O(n \log n)$.

## Recherche par hashage

L'utilisation d'un tableau de hachage permet de réaliser des recherches en temps constant, en moyenne ($O(1)$). C'est donc une méthode encore plus performante que la recherche dichotomique. Elle nécessite également un prétraitement pour construire la table de hachage, en $O(n)$, mais elle est particulièrement adaptée pour des recherches fréquentes dans des ensembles de données volumineux.

La performance de la recherche dépend grandement de la fonction de hachage utilisée et du facteur de charge de la table de hachage. Si le facteur de charge est trop élevé, la recherche peut devenir linéaire.

Il est possible de s'affranchir du risque de collision en utilisant une table de hachage parfaite, mais cela implique une complexité bien plus grande pour la construction de la table. Une fonction de hashage parfaite est une fonction injective, c'est-à-dire qu'elle associe un élément unique à chaque clé sans risque de collision. Cette approche est particulièrement adaptés pour des ensemble de données statiques (connus à l'avance) et de petite taille.

## Localité des données

La complexité de recherche n'est pas le seul critère à prendre en compte pour choisir un algorithme de recherche. Le fonctionnement de l'ordinateur impose des contraintes matérielles qui peuvent influencer les performances. Par exemple, la recherche linéaire peut être plus rapide que la recherche dichotomique pour des tableaux de petite taille, car elle exploite mieux la localité des données en mémoire.

Nous l'avons abordé lors de l'explication du [fonctionnement de la mémoire][light-speed] que l'accès à la RAM est lent par rapport au processeur. Pour ce faire le processeur fait appel à une mémoire cache très rapide mais beaucoup plus petite. Lorsque vous parcourez un tableau, les éléments sont chargés en mémoire cache et la recherche linéaire exploite mieux cette localité des données. Si le tableau est très grand, à chaque saut de la recherche dichotomique vous ne profitez pas de la mémoire cache et le temps d'accès à la RAM devient prépondérant. Aussi dans l'élaboration d'un algorithme on cherche à optimiser la **localité des données**, à la fois spatiale (les éléments sont proches en mémoire) et temporelle (les éléments sont utilisés dans un court laps de temps) afin de minimiser les temps d'accès à la RAM.

## Recherche sur de gros volumes de données

Si on prend l'exemple d'un moteur de recherche sur internet, la recherche dichotomique n'est pas adaptée. En effet, les données sont stockées sur des serveurs distants et le temps d'accès à ces données est bien plus long que le temps de calcul de l'algorithme. Dans ce cas, la recherche par hashage est plus adaptée car elle permet de réduire le temps d'accès aux données en les regroupant localement. D'autre part, ce type de problème n'est pas implémenté avec un tableau d'entiers programmé en C. Lorsque la collection et le traitement des données deviennent trop volumineux, on utilise des bases de données car d'une part elles offrent les outils nécessaire à la gestion des données et d'autre part elles permettent le stockage des données sur un disque dur.

Dans les problèmes courants d'ingénierie, une base de données SQLite peut être un excellent choix pour stocker des données structurées et effectuer des recherches complexes. Voici un exemple de recherche sur une base de données SQLite :

```c
#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>

int create_and_insert(sqlite3 *db) {
    // Créer la table Personnes
    const char *sql_create_table =
        "CREATE TABLE IF NOT EXISTS people("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "age INT,"
        "firstname TEXT,"
        "lastname TEXT,"
        "salary REAL);";

    rc = sqlite3_exec(db, sql_create_table, 0, 0, &err_msg);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
        return 1;
    }

    // Insérer des données dans la table
    const char *sql_insert =
        "INSERT INTO people (age, lastname, firstname, salary) VALUES "
        "(25, 'Anderson', 'Alexandre', 4500),"
        "(35, 'Dupont',   'François',  3200),"
        "(28, 'Martin',   'Annabelle', 4800),"
        "(42, 'Favre',    'Fabrice',   5200),"
        "(30, 'Armand',   'Aurelie',   4100);";

    rc = sqlite3_exec(db, sql_insert, 0, 0, &err_msg);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
        return 1;
    }
    return 0;
}

int main(void) {
    sqlite3 *db;
    char *err_msg = 0;
    int rc;

    // Ouvrir ou créer la base de données
    rc = sqlite3_open("people.db", &db);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    // Créer et insérer des données dans la base de données
    if (create_and_insert(db)) {
        sqlite3_close(db);
        return 1;
    }

    // Requête pour trouver les personnes correspondant aux critères
    const char *sql_query =
        "SELECT * FROM people WHERE "
        "age BETWEEN 23 AND 42 AND "
        "(lastname LIKE 'A%' OR nom LIKE 'F%') AND "
        "LENGTH(firstname) = 8 AND "
        "salary > 4000;";

    sqlite3_stmt *stmt;
    rc = sqlite3_prepare_v2(db, sql_query, -1, &stmt, 0);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to execute query: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    // Exécuter la requête et afficher les résultats
    printf("Résultats de la recherche:\n");
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        int id = sqlite3_column_int(stmt, 0);
        int age = sqlite3_column_int(stmt, 1);
        const unsigned char *nom = sqlite3_column_text(stmt, 2);
        const unsigned char *prenom = sqlite3_column_text(stmt, 3);
        double salaire = sqlite3_column_double(stmt, 4);

        printf("ID: %d, Age: %d, Nom: %s, Prénom: %s, Salaire: %.2f\n",
               id, age, lastname, firstname, salary);
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
}
```

## La Malédiction de la Dimensionnalité

L'un des principaux problèmes rencontrés lorsqu'on travaille avec des données en plusieurs dimensions est ce que l'on appelle aussi le "fléau de la dimension". Ce terme inventé par Richard Bellman en 1961 décrit plusieurs phénomènes qui rendent la manipulation des données multidimensionnelles plus complexe que celle des données unidimensionnelles. En particulier, les points de données deviennent de plus en plus dispersés dans l'espace au fur et à mesure que la dimension augmente, ce qui rend plus difficile la localisation rapide d'un voisin proche.

La difficulté réside dans l'imposibilité d'inférer des relations entre les données pour optimiser la recherche. Par exemple, si vous avez un tableau de 1000 éléments, vous pouvez diviser le tableau en 10 blocs de 100 éléments et effectuer une recherche dichotomique sur chaque bloc. Si vous avez un tableau de 1000 éléments en 2 dimensions, vous ne pouvez pas diviser le tableau en 10 blocs de 100 éléments dans chaque dimension. Vous devez diviser le tableau en 100 blocs de 10 éléments dans chaque dimension, soit 1000 blocs au total. La recherche dichotomique n'est plus efficace.

Le problème est encore plus complexe lorsque la recherche porte sur une combinaison de plusieurs dimensions. Par exemple, vous stocker des coordonnées géographiques (latitude et longitude) et vous cherchez à trouver les points les plus proches d'un point donné. La recherche dichotomique ne fonctionne pas dans ce cas. Une approche courante pour ce type de recherche est d'utiliser des arbres de recherche multidimensionnels, tels que les arbres KD (K-dimensional trees) ou les arbres R (R-trees).

## K-D Tree

Le K-D Tree est une structure de données arborescente qui permet de stocker des points en plusieurs dimensions. Il est utilisé pour effectuer des recherches spatiales efficaces, telles que la recherche des points les plus proches d'un point donné. Le principe de l'arbre KD est de diviser l'espace en deux à chaque niveau de l'arbre, en alternant les dimensions.

![Représentation du K-D Tree](/assets/images/kd-tree.drawio)

Lors de l'insertion de chaque point, le plan est divisé en deux parties égales (gauche/droite) ou (haut/bas) selon la parité du niveau de l'arbre. Au niveau stockage, on utilise un arbre binaire:

![Arbre binaire du K-D Tree](/assets/images/kd-tree-nodes.drawio)

On sait qu'un arbre binaire peut être représenté sous forme d'une liste, la représentation ci-dessus peut-être ainsi représentée avec avec :

```c
int nodes[] = {1, 2, 3, 5, -1, 4, -1, 6, 8, -1, -1, -1, -1, -1, 7};
```

La valeur `-1` indique un noeud vide. La racine de l'arbre est le premier élément de la liste, ici `1`. Les enfants d'un noeud `i` sont `2*i` et `2*i+1`. Par exemple, les enfants de `1` sont `2` et `3`. Si l'arbre n'est pas complet et fortement déséquilibré, le stockage ne sera pas optimal car la plupart des noeuds seront vides. Dans ce cas il est plus élégant de représenter l'arbre avec une liste chaînée.

Bien entendu, les noeuds seront plus complexes que des entiers, un noeud peut par exemple être associé à un identifiant, et ses coordonnées X et Y:

```c
typedef struct node {
    int id;
    double x, y;
} Node;
```

Dans notre exemple pour économiser de l'espace, nous pouvons utiliser une liste pour les noeuds, et un tableau pour l'arbre:

```c
Node nodes[] = {
    {1, 10.6, 4.6},
    {2,  7.1, 3.9},
    {3, 12.6, 6.7},
    {4, 14.6, 1.6},
    {5,  3.6, 2.6},
    {6,  2.6, 0.6},
    {7,  2.4, 1.6},
    {8,  4.6, 1.4}
};

int tree[] = {0, 1, 2, 4, -1, 3, -1, 5, 7, -1, -1, -1, -1, -1, 6};
```

L'accès à un élément s'écrirait alors : `nodes[tree[1]]` pour accéder au noeud `2`, à condition que le noeud ne soit pas vide.

### Recherche du voisin le plus proche

Pour rechercher le voisin le plus proche d'un point donné dans un K-D Tree, on utilise une méthode de recherche récursive qui exploite la structure de l'arbre pour réduire efficacement l'espace de recherche. Le processus commence par la recherche du point cible en parcourant l'arbre, en suivant les divisions du plan à chaque niveau. Lorsque le point cible est trouvé ou que l'on atteint une feuille, on remonte l'arbre en vérifiant à chaque nœud si celui-ci est plus proche du point cible que les $k$ points actuellement dans la liste des plus proches voisins. Pour maintenir cette liste, on utilise généralement une file de priorité (ou un max-heap) qui garde toujours les
$k$ points les plus proches trouvés jusqu'à présent.

Lors de la remontée, on compare également la distance entre le plan de séparation du nœud courant et le point cible. Si cette distance est inférieure à la distance du plus éloigné des $k$ voisins actuels, cela signifie qu'il pourrait y avoir un voisin plus proche de l'autre côté du plan. Dans ce cas, la recherche est également effectuée dans la sous-arborescence opposée.

Prenons un exemple concret. Sur la figure suivante, on prend le point P $(3.2, 2.3)$ comme point cible comme présenté sur la figure suivante :

![Recherche d'une zone dans un K-D Tree](/assets/images/kd-tree-search.drawio)

Pour trouver le voisin le plus proche voici les opérations :

1. **Descente dans l'arbre (recherche initiale)**:
   - On commence par comparer le point \( P \) avec le nœud de la racine en fonction de la dimension actuelle (par exemple, si l'arbre est divisé selon les coordonnées \( x \) et \( y \), on commence par comparer les \( x \)).
   - On continue de descendre dans l'arbre en suivant les enfants gauche ou droit en fonction de la position du point \( P \) par rapport au plan de séparation de chaque nœud. À chaque étape, on réduit l'espace de recherche en alternant les dimensions, jusqu'à atteindre une feuille. Cette feuille correspond au point de l'arbre qui est le plus proche dans l'une des dimensions de \( P \).

2. **Remontée dans l'arbre (recherche du point le plus proche)**:
   - Une fois la feuille atteinte, on enregistre ce point comme le point le plus proche trouvé jusqu'à présent. Cependant, il est possible que le point le plus proche ne soit pas dans la sous-arborescence de cette feuille, mais plutôt dans une autre branche de l'arbre.
   - En remontant l'arbre, on évalue chaque nœud parent pour vérifier s'il pourrait contenir un point plus proche que le point le plus proche actuel. Pour cela, on calcule la distance entre \( P \) et le point stocké dans le nœud courant, ainsi que la distance entre \( P \) et le plan de séparation de ce nœud.

   - Si la distance du plan de séparation est inférieure à la distance au point le plus proche actuel, cela signifie que l'autre sous-arborescence (côté opposé du plan) pourrait contenir un point plus proche de \( P \). On doit donc explorer cette autre sous-arborescence, ce qui implique de descendre dans cette sous-arborescence comme on l'a fait initialement.

3. **Exploration de la sous-arborescence opposée**:
   - Lors de l'exploration de cette sous-arborescence opposée, on suit un processus similaire en descendant jusqu'à une feuille et en comparant chaque nœud avec le point le plus proche actuellement connu.
   - Si un point plus proche est trouvé dans cette sous-arborescence, il remplace le point le plus proche actuel.

4. **Terminaison**:
   - Le processus se poursuit jusqu'à ce que l'on ait remonté jusqu'à la racine, en explorant potentiellement plusieurs sous-arborescences opposées en fonction de la distance au plan de séparation.
   - À la fin de ce processus, le point le plus proche trouvé sera le plus proche de \( P \) dans l'ensemble du K-D Tree.

En pratique, suivant notre exemple, on part de (1). Au premier niveau de l'arbre on sait que les enfants correspondent à l'axe des abscisses et comme $3.2 < 10.6$ on prend le fils gauche. On descend donc jusqu'à (2). Cette fois-ci c'es selon l'axe des ordonnées que l'on compare ce qui nous emmène à (5), puis (6), puis (7). La descente s'arrête là car on à atteint une feuille. À partir de maintenant on entre dans la seconde phase. On remonte alors l'arbre en vérifiant si le sous-arbre opposé pourrait contenir des points plus proches.Comme le plan de séparation de (6) est plus éloigné que (7) on explore pas la région au dessus de (6). On continue la remontée jusqu'à (5). Cette fois-ci la distance de séparation est plus proche (`abs(P.x - 7.x) = 0.8` et `abs(P.x - 5,x) = 0.4`) donc, il se peut que la région à droite de (5) contienne un point plus proche. On entre alors dans a troisième phase : l'exploration de la partie droite de (5). On descend alors jusqu'à (8) qui est une feuille, et qui de surcroît est plus éloigné que (7).

### Recherche des k-voisins les plus proches

Pour rechercher les $k$ voisins les plus proches d'un point donné dans un K-D Tree, on utilise une méthode similaire à la recherche du voisin le plus proche, mais en maintenant une liste des $k$ points les plus proches trouvés jusqu'à présent. Lors de la remontée dans l'arbre, on compare chaque nœud parent avec les points de la liste des $k$ voisins les plus proches. Si le nœud parent est plus proche que le point le plus éloigné de la liste, on l'ajoute à la liste et on retire le point le plus éloigné. On continue ce processus jusqu'à ce que l'arbre soit entièrement exploré. Cela correspond à utiliser une structure de données de file de priorité (ou max-heap) pour maintenir les $k$ points les plus proches. La méthode est donc très similaire à la recherche du voisin le plus proche, mais avec une gestion plus complexe de la liste des voisins.

La recherche des $k$ voisins est donc une opération en $O(k \log n)$.

### Recherche des voisins dans un cercle

Reconsidérons notre figure précédente. On souhaite maintenant chercher les points à l'intérieur du cercle jaune de diamètre $3.75$. Pour cela on commence par chercher le point le plus proche de $P$ comme précédemment. On remonte l'arbre en vérifiant si le plan de séparation est à une distance inférieure à $3.75$ du point $P$. Dit autrement, est-ce que le cercle coupe le plan de séparation. Si c'est le cas on explore l'autre sous-arbre. On continue ce processus jusqu'à ce que l'on ait exploré tous les sous-arbres dont le plan de séparation est à une distance inférieure à $3.75$ de $P$.

### Implémentation

L'implémentation passe par la définition d'un noeud:

```c
typedef struct Node {
   int id;
   double x, y;
   struct Node *left, *right;
} Node;

Node* insert(Node* root, Node* new_node, int depth) {
   if (root == NULL) return new_node;

   int cd = depth % 2;

   if ((cd == 0 && new_node->x < root->x) || (cd == 1 && new_node->y < root->y))
      root->left = insert(root->left, new_node, depth + 1);
   else
      root->right = insert(root->right, new_node, depth + 1);

   return root;
}

void search_closest(Node* root, double x, double y, int depth,
                    ClosestNode* closest) {
   if (root == NULL) return;

   double d = squared_distance(root->x, root->y, x, y);
   if (d < closest->distance) {
      closest->node = root;
      closest->distance = d;
   }

   int cd = depth % 2;

   // Quelle sous-arborescence est la plus proche ?
   Node* nearer_subtree = NULL;
   Node* farther_subtree = NULL;
   if ((cd == 0 && x < root->x) || (cd == 1 && y < root->y)) {
      nearer_subtree = root->left;
      farther_subtree = root->right;
   } else {
      nearer_subtree = root->right;
      farther_subtree = root->left;
   }

   // Rechercher d'abord dans la sous-arborescence la plus proche
   search_closest(nearer_subtree, x, y, depth + 1, closest);

   // Vérifier si nous devons explorer la sous-arborescence plus éloignée
   double dist_to_plane = (cd == 0) ? (x - root->x) : (y - root->y);
   if (dist_to_plane * dist_to_plane < closest->distance)
      search_closest(farther_subtree, x, y, depth + 1, closest);
}
```

Pour insérer un noeud à la position `x`, `y`, on utilisera :

```c
Node* new_node = (Node*)malloc(sizeof(Node));
new_node->x = x;
new_node->y = y;
new_node->left = new_node->right = NULL;
*root = insert(*root, new_node, 0);
```

Et pour rechercher l'élément le plus proche de `x`, `y` on utilisera :

```c
ClosestNode closest;
closest.node = NULL;
closest.distance = DBL_MAX;

search_closest(root, x, y, 0, &closest);
```