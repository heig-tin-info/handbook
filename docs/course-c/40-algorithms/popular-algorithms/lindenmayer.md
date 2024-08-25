# L-Système (Lindenmayer System)

Un L-Système est un système de réécriture de chaînes de caractères inventé en 1968 par le biologiste hongrois Astrid Lindenmayer. Il est utilisé pour modéliser la croissance des plantes, la morphogenèse, la fractale, etc. On peut définir ce sytème comme une forme de grammaire générative.

### Définition

Un L-Système est défini par un alphabet, un axiome et un ensemble de règles de réécriture. L'axiome est la chaîne de départ. Les règles de réécriture définissent comment les symboles de l'axiome sont remplacés par d'autres symboles.

Nous avons donc:

Axiome

: C'est le point de départ de la réécriture. C'est une chaîne de caractères.

Règles de production

: Chaque règle séparée par des virgules définissent comment un symbole est remplacé par une autre chaîne de caractères.

Angle

: C'est l'angle de rotation pour les symboles `+` et `-`. À chaque fois que l'on rencontre un `+`, on tourne à droite de l'angle. À chaque fois que l'on rencontre un `-`, on tourne à gauche de l'angle. Les angles peuvent être cumulatifs : `++` signifie tourner deux fois à droite.

Itérations

: C'est le nombre de fois que l'on applique les règles de réécriture à l'axiome.

Longueur

: C'est la longueur de chaque segment de la courbe pour chaque symbole.

### Grammaire

En 3 dimensions, on dispose des coordonnées $x$, $y$ et $z$ ainsi que des rotations $\alpha$, $\beta$ et $\gamma$.

- `+` : tourner à droite autour de l'axe $z$ de l'angle $\alpha$
- `-` : tourner à gauche autour de l'axe $z$ de l'angle $\alpha$
- `&` : tourner en bas autour de l'axe $y$ de l'angle $\beta$
- `^` : tourner en haut autour de l'axe $y$ de l'angle $\beta$
- `\` : tourner à droite autour de l'axe $x$ de l'angle $\gamma$
- `/` : tourner à gauche autour de l'axe $x$ de l'angle $\gamma$
- `|` : tourner de 180° autour de l'axe $z$, correspond à `++` ou `--`.
- `[` : sauvegarder la position et l'angle
- `]` : restaurer la position et l'angle
- Les lettres sont des symboles de dessin

### Exemple

Prenons cette définition :

```yml
name: Koch snowflake
axiom: F
angle: 90
iterations: 3
length: 20
rules:
  F: F+F-F-F+F
```

L'axiome est `F`. On a une règle de réécriture `F -> F+F-F-F+F`. On applique cette règle 3 fois.

1. Itération 0: `F`
2. Itération 1: `F+F-F-F+F`
3. Itération 2: `F+F-F-F+F + F+F-F-F+F - F+F-F-F+F - F+F-F-F+F + F+F-F-F+F`
4. Et ainsi de suite...

Imaginez que vous tenez un crayon et que vous suivez les instructions pour dessiner la courbe. À chaque `F`, vous avancez de 20 pixels. À chaque `+`, vous tournez de 90° à droite. À chaque `-`, vous tournez de 90° à gauche.

## Évolution

On peut imaginer de généraliser le L-Système en ajoutant des variables, des fonctions, des conditions, etc. On peut également ajouter des règles de réécriture conditionnelles, des règles de réécriture probabilistes.

Imaginons une définition formelle en YAML :

```yml
name: Nom du L-Système
axiom: Chaîne de départ
angle: Angle de rotation par défaut
iterations: Nombre d'itérations
length: Longueur de chaque segment par défaut
rules:
    A: A+B
    B: A-B
actions:
```

Imaginons les actions suivantes:

```yml
actions:
    forward(length): Avancer de length, length est optionnel
    rotate(alpha, beta, gamma): Tourner de angle
    color(r, g, b): Changer la couleur du crayon
    color(name): Changer la couleur du crayon par une couleur nommée
    save(): Sauvegarder la position et l'angle
    restore(): Restaurer la position et l'angle
    width(size): Changer la taille du crayon
variables:
    level: Niveau de récursion
```