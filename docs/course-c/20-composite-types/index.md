# Types Composites

Un type composite est un type de données qui est construit à partir d'autres types de données plus simples ou primitifs (comme `int`, `char`, etc.). Ces types permettent de regrouper plusieurs éléments de données sous une seule entité, ce qui est essentiel pour organiser des structures de données plus complexes dans les programmes. En C on retrouve les types composites suivants:

**Les tableaux**

: Un tableau est une collection d'éléments de même type organisée de manière continuë en mémoire.

**Les structures** (struct)

: Une structure est un type composite qui regroupe des éléments de données, appelés membres qui peuvent être de types différents.

**Les unions**

: Une union est similaire à une structure, mais tous les membres partagent la même zone mémoire. Cela signifie qu'une union ne peut stocker qu'une seule valeur à la fois parmi ses membres.

**Les énumérations** (enum)

: Une énumération est un type composite qui associe des noms symboliques à des valeurs intégrales. Bien que techniquement les énumérations soient des types scalaires, elles sont souvent considérées dans le cadre des types composites en raison de leur capacité à représenter des ensembles de valeurs possibles.

**Les chaînes de caractères**

: Les chaînes de caractères sont techniquement des tableaux de caractères (char), mais elles peuvent être considérées comme un type composite en raison de la manière dont elles sont manipulées et utilisées pour représenter du texte.

En combinant des tableaux, des structures avec des pointeurs on peut créer des types composites encore plus complexes que l'on appellera des conteneurs de données.
