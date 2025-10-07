# Graphes

Un graphe est un ensemble de sommets reliés par des arêtes. Les graphes sont utilisés pour modéliser des relations entre des objets. Par exemple, un graphe peut être utilisé pour représenter un réseau social, un réseau de transport, un réseau de distribution, etc.

C'est une variante générale des arbres. Un arbre est un graphe particulier où chaque sommet est relié à un autre sommet par un chemin unique. Un graphe peut avoir des cycles, c'est-à-dire des chemins qui reviennent à leur point de départ.

## Types de graphes

### Forêts

Un [[graphe]] sans cycle est appelé une [[forêt]]. Une forêt est un ensemble d'arbres. Un arbre est un graphe [[connexe]] sans cycle.

![Exemple de forêt](/assets/images/forest.drawio)

### Graphes orientés

Un graphe orienté est un graphe dont les arêtes ont une direction. Les graphes orientés sont utilisés pour modéliser des relations asymétriques. Par exemple, un graphe orienté peut être utilisé pour représenter un réseau de transport où les arêtes représentent des routes à sens unique.

![Exemple de graphe orienté](/assets/images/oriented.drawio)

### Graphes pondérés

Un graphe pondéré est un graphe dont les arêtes ont un poids. Les graphes pondérés sont utilisés pour modéliser des relations quantitatives. Par exemple, un graphe pondéré peut être utilisé pour représenter un réseau de transport où les arêtes représentent des routes avec une longueur ou un coût associé.

![Exemple de graphe pondéré](/assets/images/weighted.drawio)

### Graphes bipartis

Un graphe biparti est un graphe dont les sommets peuvent être divisés en deux ensembles disjoints. Les arêtes d'un graphe biparti relient les sommets des deux ensembles. Les graphes bipartis sont utilisés pour modéliser des relations binaires. Par exemple, un graphe biparti peut être utilisé pour représenter des relations d'adjacence entre deux ensembles d'objets.

![Exemple de graphe biparti](/assets/images/bipartite.drawio)

## Représentation des graphes

Il existe plusieurs façons de représenter un graphe en mémoire. Les deux représentations les plus courantes sont les listes d'adjacence et les matrices d'adjacence.

### Liste d'adjacence

Dans une liste d'adjacence, chaque sommet est associé à une liste de ses voisins. Une liste d'adjacence est une structure de données dynamique qui permet d'ajouter et de supprimer des arêtes facilement. Cependant, elle nécessite généralement moins de mémoire que les matrices d'adjacence pour des graphes clairsemés.

### Matrice d'adjacence

Dans une matrice d'adjacence, chaque sommet est associé à une ligne et une colonne de la matrice. La valeur de la case (i, j) de la matrice indique s'il existe une arête entre les sommets i et j. Une matrice d'adjacence est une structure de données statique qui permet de vérifier rapidement l'existence d'une arête. Cependant, elle nécessite plus de mémoire que les listes d'adjacence.

## Parcours de graphes

Il existe plusieurs algorithmes pour parcourir un graphe. Les deux algorithmes les plus courants sont le parcours en profondeur (DFS) et le parcours en largeur (BFS).

### DFS

Le parcours en profondeur (Depth-First Search) est un algorithme récursif qui explore le graphe en profondeur. Il commence par un sommet de départ et explore tous les sommets accessibles depuis ce sommet avant de passer au suivant. L'algorithme DFS est utilisé pour trouver des cycles dans un graphe, pour vérifier la connexité d'un graphe, pour trouver des composantes fortement connexes, etc.

```c
void dfs(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v);
        }
    }
}
```

### BFS

Le parcours en largeur (Breadth-First Search) est un algorithme itératif qui explore le graphe en largeur. Il commence par un sommet de départ et explore tous les sommets à une distance k avant de passer à la distance k+1. L'algorithme BFS est utilisé pour trouver le plus court chemin entre deux sommets, pour trouver le nombre de composantes connexes, pour trouver le nombre de sommets à une distance donnée, etc.

```c
void bfs(int u) {
    Queue q = INIT_QUEUE;
    q.push(u);
    visited[u] = true;
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        for (int w : adj[v]) {
            if (!visited[w]) {
                q.push(w);
                visited[w] = true;
            }
        }
    }
}
```

### Dijkstra

L'algorithme de Dijkstra est un algorithme qui permet de trouver le plus court chemin entre un sommet de départ et tous les autres sommets d'un graphe pondéré. L'algorithme de Dijkstra est basé sur le parcours en largeur et utilise une file de priorité pour explorer les sommets dans l'ordre croissant de leur distance par rapport au sommet de départ.

```c
void dijkstra(int u) {
    PriorityQueue pq = INIT_PRIORITY_QUEUE;
    pq.push({0, u});
    dist[u] = 0;
    while (!pq.empty()) {
        int d = -pq.top().first;
        int v = pq.top().second;
        pq.pop();
        if (d > dist[v]) continue;
        for (auto [w, c] : adj[v]) {
            if (dist[v] + c < dist[w]) {
                dist[w] = dist[v] + c;
                pq.push({-dist[w], w});
            }
        }
    }
}
```
