# Jeu de la vie de Conway

Le jeu de la vie de Conway est un automate cellulaire inventé par le mathématicien John Horton Conway en 1970. C'est une simulation qui se déroule sur une grille bidimensionnelle infinie. Chaque cellule de la grille peut être dans un état mort ou vivant. L'état des cellules évolue en fonction de règles simples.

Un automate cellulaire est un modèle mathématique qui consiste en une grille de cellules qui peuvent être dans un état donné. Chaque cellule interagit avec ses voisines en fonction de règles prédéfinies. Les automates cellulaires sont utilisés pour modéliser des phénomènes naturels, des systèmes biologiques, des simulations, etc.

Chaque cellule peut être dans un état 0 (morte) ou 1 (vivante) en fonction de règles de transition. Les règles de transition définissent comment l'état d'une cellule évolue en fonction de l'état de ses voisines. Dans un automate bidimentionnel, donc une grille bidimensionnelle, chaque cellule a 8 voisines. On nomme ces voisines le voisinage de Moore où chaque voisin est numéroté ainsi :

![Voisinage de Moore](/assets/images/moore-neighbors.drawio)

Le format B/S est utilisé pour définir les règles de transition. B signifie *birth* (naissance) et S signifie *survival* (survie). Les règles sont définies par une liste de chiffres qui indiquent le nombre de voisins nécessaires pour qu'une cellule naisse ou survive. Par exemple, la règle `B3/S23` signifie qu'une cellule naît si elle a exactement 3 voisins et survit si elle a 2 ou 3 voisins. Certaines règles ont des noms spécifiques:

| Nom          | Règle        | Description                     |
| ------------ | ------------ | ------------------------------- |
| Game of Life | B3/S23       | La règle classique de Conway    |
| Mazes        | B3/S12345    | Dessine une sorte de labyrinthe |
| Mazectric    | B3/S1234     | Une autre variante              |
| HighLife     | B36/S23      | Une variante de Conway          |
| Day & Night  | B3678/S34678 | Une autre variante              |

## Implémentation

Pour implémenter le jeu de la vie de Conway, il faut une grille et un pas temporel pour faire évoluer les cellules. On peut utiliser un tableau à deux dimensions pour représenter la grille. Chaque cellule est représentée par un 0 (mort) ou un 1 (vivant). On peut bien entendu utiliser un tableau de taille fixe ou un tableau dynamique pour représenter la grille.

À chaque pas de temps, on applique les règles de transition pour chaque cellule. On peut utiliser un tableau temporaire pour stocker les nouvelles valeurs des cellules. On peut aussi utiliser un seul tableau pour stocker les valeurs actuelles et futures des cellules. Il suffit de basculer entre les deux tableaux à chaque pas de temps.

La complexité de l'algorithme est en $O(n^2)$ où $n$ est le nombre de cellules dans la grille. On sait que ce type d'algorithme est très gourmand en ressources et on est en droit de se demander s'il est possible de faire mieux.

L'algorithme de *Hashlife* est une optimisation de l'algorithme de Conway qui permet de réduire la complexité de l'algorithme à $O(n \log n)$. Il est basé sur une structure de données appelée *quadtree* qui permet de stocker les cellules vivantes de manière compacte. L'algorithme de *Hashlife* est plus complexe à implémenter mais il permet de gérer des grilles de taille importante de manière plus efficace au détriment de la complexité de l'algorithme et d'un espace de stockage plus important.
