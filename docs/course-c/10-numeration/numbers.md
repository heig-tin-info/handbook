# Nombres
Vous avez tous appris dans votre enfance à compter, puis vous avez appris que les nombres se classifient dans des ensembles. Les mathématiciens ont défini des ensembles de nombres pour lesquels des propriétés particulières sont vérifiées ; ces ensembles sont imbriqués les uns dans les autres, et chaque ensemble est un sous-ensemble de l'ensemble suivant.

$$
\mathbb{N} \in \mathbb{Z} \in \mathbb{Q} \in \mathbb{R} \in \mathbb{C} \in \mathbb{H} \in \mathbb{O} \in \mathbb{S}
$$

![Ensemble des nombres]({assets}/images/ensembles.drawio)

Les ensembles de nombres sont :

- $\mathbb{N}$ : ensemble des entiers naturels (0, 1, 2, 3, ...)
- $\mathbb{Z}$ : ensemble des entiers relatifs (..., -3, -2, -1, 0, 1, 2, 3, ...)
- $\mathbb{D}$ : ensemble des décimaux (-0.1, 0, 0.1, 0.2, 0.3, ...)
- $\mathbb{Q}$ : ensemble des rationnels (0, 1, 1/2, 1/3, 1/4, ...)
- $\mathbb{R}$ : ensemble des réels ($\pi$, $\sqrt{2}$, ...)
- $\mathbb{C}$ : ensemble des complexes ($i$, $1 + i$, ...)
- $\mathbb{H}$ : ensemble des quaternions ($1 + i + j + k$, ...)
- $\mathbb{O}$ : ensemble des octonions
- $\mathbb{S}$ : ensemble des sédénions

!!! info "Quaternions, octonions et sédénions"

    Les quaternions, octonions et sédénions sont des nombres hypercomplexes qui généralisent les nombres complexes. Ils sont utilisés en physique pour décrire les rotations dans l'espace.

    Les quaternions sont utilisés en informatique pour représenter les rotations en 3D. Les octonions et sédénions sont des généralisations des quaternions, mais ils sont moins utilisés en pratique.

    A chaque fois que s'éloigne du réel (et c'est une manière amusante de le dire), on perd des propriétés intéressantes. Les nombres complexes ne sont pas ordonnés, les quaternions ne sont pas commutatifs, les octonions ne sont pas associatifs, et les sédénions ne sont même pas alternatifs. Un nombre alternatif est un nombre pour lequel la formule suivante est vérifiée :

    $$
    (a \cdot a) \cdot b = a \cdot (a \cdot b)$
    $$

    En pratique dans une carrière d'ingénieur, vous n'aurez jamais à manipuler ni des quaternions, ni octonions ou sédénions. Les nombres complexes sont néanmoins une extension des nombres réels qui sont utilisés en physique et en mathématiques.

Un nombre arbitraire n'est pas directement associé à une quantité d'information. Le nombre $\pi$ est irrationnel, c'est-à-dire qu'il ne se termine jamais et ne se répète jamais. Il est donc impossible de stocker $\pi$ en mémoire, car il faudrait une quantité infinie de bits pour le représenter.

Archimère disait : Δός μοι πᾶ στῶ καὶ τὰν γᾶν κινάσω (Donnez-moi un point d'appui et je soulèverai le monde). Le Créateur, s'il existe, aurait pu dire : Donnez moi un nombre et je vous construirai l'univers ! Bien entendu la quantité d'information dans l'univers est colossale, elle croît avec l'entropie et donc avec le temps qui passe.

!!! info Minecraft

    Dans Minecraft, lorsque vous créez un monde, vous pouvez utiliser une graine pour générer un monde aléatoire. Cette graine est un nombre fini qui sert de base à l'algorithme de génération de monde. Si vous utilisez la même graine, vous obtiendrez le même monde.

    Mais pour que cela fonctionne il faut le code source de Minecraft, lui aussi c'est une succession de 0 et de 1, et donc c'est un nombre, lui aussi fini.

    Enfin, lorsque vous jouez, vos actions génèrent de l'information qui influence le monde, et donc la quantité d'information dans le monde croît. C'est pour cela que plus vous jouez, plus la sauvegarde de votre monde devient grande, mais vous pouvez la représenter aussi avec un nombre fini.

Les mémoires des ordinateurs ne sont pas infinies, elles sont limitées par la quantité de transistors qui les composent. Il n'est donc pas possible d'y stocker n'importe quel nombre. $\pi$ ne peut pas être stocké en mémoire, mais une approximation de $\pi$ peut l'être.

Aussi, l'informatique impose certaines limitations sur les nombres que l'on peut manipuler. Les nombres entiers sont les plus simples à manipuler, mais ils sont limités par la taille de la mémoire et la manière dont on les enregistre en mémoire. C'est ce que nous allons voir.

## Entiers naturels

En mathématiques, un [entier naturel](https://fr.wikipedia.org/wiki/Entier_naturel) est un nombre positif ou nul. Chaque nombre à un successeur unique et peut s'écrire avec une suite finie de chiffres en notation décimale positionnelle, et donc sans signe et sans virgule. L'ensemble des entiers naturels est défini de la façon suivante :

$$
\mathbb{N} = {0, 1, 2, 3, ...}
$$

Les entiers sont les premiers types de données manipulés par les ordinateurs. Ils sont stockés en mémoire sous forme de bits. En choisissant la taille de stockage des entiers, on détermine la plage de valeurs que l'on peut représenter. Un entier de 8 bits peut représenter $2^8 = 256$ valeurs différentes, de 0 à 255. Un entier de 16 bits peut représenter $2^{16} = 65536$ valeurs différentes, de 0 à 65535.

!!! example

    Le nombre 142 peut s'écrire sur 8 bits en binaire, avec une notation positionnelle (où les bits sont alignés par poids décroissants) on peut écrire :

    $$
    \begin{array}{cccccccc}
    2^7 & 2^6 & 2^5 & 2^4 & 2^3 & 2^2 & 2^1 & 2^0 \\
    1 & 0 & 0 & 0 & 1 & 1 & 1 & 0 \\
    \end{array}
    $$

La taille de stockage d'un entier détermine donc ses limites. Si cette manière est élégante, elle ne permet pas de représenter des valeurs négatives. Pour cela, on aura recours aux entiers relatifs.

## Entiers relatifs

Mathématiquement un **entier relatif** appartient à l'ensemble $\mathbb{Z}$:

$$
\mathbb{Z} = {..., -3, -2, -1, 0, 1, 2, 3, ...}
$$

Vous le savez maintenant, l'interprétation d'une valeur binaire n'est possible qu'en ayant connaissance de son encodage et s'agissant d'entiers, on peut se demander comment stocker des valeurs négatives, car manque une information permettant d'encoder le symbole pour le signe `-` (ni même d'ailleurs `+`).

Une approche naïve serait de réserver une partie de la mémoire pour des entiers positifs et une autre pour des entiers négatifs et stocker la correspondance binaire/décimale simplement. Un peu comme si vous aviez deux boîtes chez vous, l'une pour les choses qui se mangent (le frigo) et une pour les choses qui ne se mangent plus (la poubelle).

L'ennui pour les **variables** c'est que le contenu peut changer et qu'un nombre négatif pourrait très bien devenir positif après un calcul. Il faudrait alors le déplacer d'une région mémoire à une autre. Ce n'est donc pas la meilleure méthode.

On pourrait alors renseigner la nature du nombre, c'est-à-dire son signe avec sa valeur.

### Bit de signe

Pourquoi ne pas se réserver un bit de signe, par exemple le 8^e^ bit de notre nombre de 8 bits, pour indiquer si le nombre est positif ou négatif ?

```text
┌─┐┌─┬─┬─┬─┬─┬─┬─┐
│0││1│0│1│0│0│1│1│ = (0 * (-1)) * 0b1010011 = 83
└─┘└─┴─┴─┴─┴─┴─┴─┘
┌─┐┌─┬─┬─┬─┬─┬─┬─┐
│1││1│0│1│0│0│1│1│ = (1 * (-1)) * 0b1010011 = -83
└─┘└─┴─┴─┴─┴─┴─┴─┘
```

Cette méthode impose le sacrifice d'un bit et donc l'intervalle représentable est ici n'est plus que de `[-127..127]`. Elle présente un autre inconvénient majeur : la représentation de zéro.

Il existe alors deux zéros, le zéro négatif `0b00000000`, et le zéro positif `0b10000000` ce qui peut poser des problèmes pour les comparaisons. Est-ce que $0$ est égal $-0$ ? En un sens oui, mais en termes de l'information stockée, ce n'est pas le même nombre.

En termes de calcul, l'addition ne fonctionne plus si on raisonne sur les bits. Car si on additionne au zéro positif (`0b10000000`) la valeur 1 on aura 1, mais si on additionne au zéro négatif (`0b00000000`) la valeur 1 on obtiendra -1. C'est un peu déroutant.

```text
000   001   010   011   100   101   110   111
-+-----+-----+-----+-----+-----+-----+-----+--->

000   001   010   011   100   101   110   111
-+-----+-----+-----+->  -+-----+-----+-----+---> Méthode du bit de signe
 0     1     2     3     0    -1    -2    -3
```

Il faudrait donc trouver une méthode qui permettrait de conserver la possibilité de faire les opérations directement en binaire. En d'autres termes on aimerait pouvoir calculer en base deux sans se soucier du signe :

```text
  00000010 (2)
- 00000101 (5)
----------
  11111101 (-125)    2 - 5 != -125
```

Si on résume, la solution proposée qui utilise un bit de signe pose deux problèmes :

1. Les opérations ne sont plus triviales, et un algorithme particulier doit être mis en place pour les gérer.
2. Le double zéro (positif et négatif) est gênant.

### Complément à un

Le **complément à un** est une méthode plus maline utilisée dans les premiers ordinateurs comme le [CDC 6600](https://fr.wikipedia.org/wiki/Control_Data_6600) (1964) ou le [UNIVAC 1107](https://en.wikipedia.org/wiki/UNIVAC_1100/2200_series) (1962). Il existe également un bit de signe, mais il est implicite.

Le complément à un tire son nom de sa définition générique nommée *radix-complement* ou complément de base et s'exprime par :

$$
b^n - y
$$

où

$b$

: La base du système positionnel utilisé

$n$

: Le nombre de chiffres maximal du nombre considéré

$y$

: La valeur à complémenter.

Ainsi, il est facile d'écrire le complément à neuf d'un nombre en base dix, car on s'arrange pour que chaque chiffre composant le nombre on trouve un autre chiffre dont la somme est égale à neuf.

```
0 1 2 3 4 5 6 7 8 9
        |
        | Complément à 9
        v
9 8 7 6 5 4 3 2 1 0
```

On notera avec beaucoup d'intérêt qu'un calcul est possible avec cette méthode. À gauche on a une soustraction classique, à droite on remplace la soustraction par une addition ainsi que les valeurs négatives par leur complément à 9. Le résultat `939` correspond à `60`.

```
  150      150
- 210    + 789
-----    -----
  -60      939
```

Notons que le cas précis de l'inversion des chiffres correspond au complément de la base, moins un. L'inversion des bits binaire est donc le complément à $(2-1) = 1$.

```
000   001   010   011   100   101   110   111
-+-----+-----+-----+-----+-----+-----+-----+--->

000   001   010   011   100   101   110   111
-+-----+-----+-----+-> <-+-----+-----+-----+--- complément à un
 0     1     2     3    -3    -2    -1     0
```

Reprenons l'exemple précédent de soustraction, on notera que l'opération fonctionne en soustrayant 1 au résultat du calcul.

```
  00000010 (2)
+ 11111010 (-5)
----------
  11111101 (-3)
-        1
----------
  11111011 (-4)
```

En résumé, la méthode du complément à 1 :

1. Les opérations redeviennent presque triviales, mais il est nécessaire de soustraire 1 au résultat (c'est dommage).
2. Le double zéro (positif et négatif) est gênant.

[](){#twos_complement}
### Complément à deux

Le complément à deux n'est rien d'autre que le complément à un **plus** un. C'est donc une amusante plaisanterie des informaticiens. Car dans un système binaire, le nombre de symboles et de 2 (`0` et `1`). On ne peut pas trouver un chiffre tel que la somme fasse `2`. C'est la même idée que de demander le complément à 10 en base 10.

Pour réaliser ce complément à deux (complément à un plus un), il y a deux étapes :

1. Calculer le complément à un du nombre d'entrées.
2. Ajouter 1 au résultat.

Oui, et alors, en quoi cela change la donne ? Surprenamment, on résout tous les problèmes amenés par le complément à un :

```
000   001   010   011   100   101   110   111
-+-----+-----+-----+-----+-----+-----+-----+--->
 0     1     2     3     4     5     6     7     sans complément
 0     1     2     3    -3    -2    -1     0     complément à un
 0     1     2     3    -4    -3    -2    -1     complément à deux
```

Au niveau du calcul :

```
  2        00000010
- 5      + 11111011   (~0b101 + 1 == 0b11111011)
---     -----------
 -3        11111101   (~0b11111101 + 1 == 0b11 == 3)
```

Les avantages :

1. Les opérations sont triviales.
2. Le problème du double zéro est résolu.
3. On gagne une valeur négative `[-128..+127]` contre `[-127..+127] avec les méthodes précédemment étudiées`.

Vous l'aurez compris, le complément à deux est le mécanisme le plus utilisé dans les ordinateurs modernes pour représenter les nombres entiers négatifs.

## Les nombres réels

Mathématiquement, les [nombres réels](https://fr.wikipedia.org/wiki/Nombre_r%C3%A9el) $\mathbb{R}$, sont des nombres qui peuvent être représentés par une partie entière, et une liste finie ou infinie de décimales. En informatique, stocker une liste infinie de décimale demanderait une quantité infinie de mémoire et donc, la [précision arithmétique](https://fr.wikipedia.org/wiki/Pr%C3%A9cision_arithm%C3%A9tique) est contrainte.

Au début de l'ère des ordinateurs, il n'était possible de stocker que des nombres entiers, mais
le besoin de pouvoir stocker des nombres réels s'est rapidement fait sentir. La transition s'est faite progressivement, d'abord par l'apparition de la [virgule fixe](https://fr.wikipedia.org/wiki/Virgule_fixe), puis par la [virgule flottante](https://fr.wikipedia.org/wiki/Virgule_flottante).

Le premier ordinateur avec une capacité de calcul en virgule flottante date de 1942 (ni vous ni moi n'étions probablement nés) avec le [Zuse's Z4](https://fr.wikipedia.org/wiki/Zuse_4), du nom de son inventeur [Konrad Zuse](https://fr.wikipedia.org/wiki/Konrad_Zuse).

### Virgule fixe

Prenons l'exemple d'un nombre entier exprimé sur 8-bits, on peut admettre facilement que bien qu'il s'agisse d'un nombre entier, une virgule pourrait être ajoutée au bit zéro sans en modifier sa signification.

```text
┌─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│0│1│0│0│1│1│ = 2^6 + 2^4 + 2^1 + 2^0 = 64 + 16 + 2 + 1 = 83
└─┴─┴─┴─┴─┴─┴─┴─┘
                , / 2^0     ----> 83 / 1 = 83
```

Imaginons à présent que nous déplacions cette virgule virtuelle de trois éléments sur la gauche. En admettant que deux ingénieurs se mettent d'accord pour considérer ce nombre `0b01010011` avec une virgule fixe positionnée au quatrième bit, l'interprétation de cette grandeur serait alors la valeur entière divisée par 8 ($2^3$). On parvient alors à exprimer une grandeur réelle comportant une partie décimale :

```text
┌─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│0│1│0│0│1│1│ = 2^6 + 2^4 + 2^1 + 2^0 = 64 + 16 + 2 + 1 = 83
└─┴─┴─┴─┴─┴─┴─┴─┘
          ,       / 2^3     ----> 83 / 8 = 10.375
```

Cependant, il manque une information. Un ordinateur, sans yeux et sans bon sens, est incapable sans information additionnelle d'interpréter correctement la position de la virgule puisque sa position n'est encodée nulle part. Et puisque la position de cette virgule est dans l'intervalle `[0..7]`, il serait possible d'utiliser trois bits supplémentaires à cette fin :

```text
┌─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│0│1│0│0│1│1│ = 2^6 + 2^4 + 2^1 + 2^0 = 64 + 16 + 2 + 1 = 83
└─┴─┴─┴─┴─┴─┴─┴─┘
          ┌─┬─┬─┐
          │0│1│1│ / 2^3     ----> 83 / 8 = 10.375
          └─┴─┴─┘
```

Cette solution est élégante, mais demande à présent 11-bits contre 8-bits initialement. Un ordinateur n'étant doué que pour manipuler des paquets de bits souvent supérieurs à 8, il faudrait ici soit étendre inutilement le nombre de bits utilisés pour la position de la virgule à 8, soit tenter d'intégrer cette information, dans les 8-bits initiaux.

### Virgule flottante

Imaginons alors que l'on sacrifie 3 bits sur les 8 pour encoder l'information de la position de la virgule. Appelons l'espace réservé pour positionner la virgule l' [exposant](<https://fr.wikipedia.org/wiki/Exposant_(math%C3%A9matiques)>) et le reste de l'information la [mantisse](https://fr.wikipedia.org/wiki/Mantisse), qui en mathématique représente la partie décimale d'un logarithme (à ne pas confondre avec la [mantis shrimp](https://fr.wikipedia.org/wiki/Stomatopoda), une quille ou crevette-mante boxeuse aux couleurs particulièrement chatoyantes).

```
  exp.  mantisse
┞─┬─┬─╀─┬─┬─┬─┬─┦
│0│1│0│1│0│0│1│1│ = 2^4 + 2^1 + 2^0 = 16 + 2 + 1 = 19
└─┴─┴─┴─┴─┴─┴─┴─┘
   └────────────> / 2^1 ----> 19 / 2 = 9.5
```

Notre construction nous permet toujours d'exprimer des grandeurs réelles, mais avec ce sacrifice, il n'est maintenant plus possible d'exprimer que les grandeurs comprises entre $1\cdot2^{7}=0.0078125$ et $63$. Ce problème peut être aisément résolu en augmentant la profondeur mémoire à 16 ou 32-bits. Ajoutons par ailleurs que cette solution n'est pas à même d'exprimer des grandeurs négatives.

Dernière itération, choisissons d'étendre notre espace de stockage à ,4 octets. Réservons un bit de signe pour exprimer les grandeurs négatives, 8 bits pour l'exposant et 23 bits pour la mantisse :

```
 ┌ Signe 1 bit
 │        ┌ Exposant 8 bits
 │        │                             ┌ Mantisse 23 bits
 ┴ ───────┴──────── ────────────────────┴──────────────────────────
┞─╀─┬─┬─┬─┬─┬─┬─┐┌─╀─┬─┬─┬─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│0│1│0│0│0│0││0│1│0│0│1│0│0│0││1│1│0│1│1│1│1│1││0│1│0│0│0│0│0│1│
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘
```

Peu à peu, nous nous rapprochons du *Standard for Floating-Point Arithmetic* ([IEEE 754](https://fr.wikipedia.org/wiki/IEEE_754)). La formule de base est la suivante :

$$
x = s\cdot b^e\sum_{k=1}^p f_k\cdot b^{-k},\; e_{\text{min}} \le e \le e_{\text{max}}
$$

Avec :

$s$

: Signe ($\pm1$)

$b$

: Base de l'exposant, un entier $>1$.

$e$

: Exposant, un entier entre $e_\text{min}$ et $e_\text{max}$

$p$

: Précision, nombre de digits en base $b$ de la mantisse

$f_k$

: Entier non négatif plus petit que la base $b$.

Étant donné que les ordinateurs sont plus à l'aise à la manipulation d'entrées binaire, la base est 2 et la norme IEEE nomme ces nombres `binary16`, `binary32` ou `binary64`, selon le nombre de bits utilisé pour coder l'information. Les termes de *Single precision* ou *Double precision* sont aussi couramment utilisés.

Les formats supporté par un ordinateur ou qu'un microcontrôleur équipé d'une unité de calcul en virgule flottante ([FPU](https://en.wikipedia.org/wiki/Floating-point_unit) pour *Floating point unit*) sont les suivants :

| IEEE-754   | Exposant | Mantisse | Signe |
| ---------- | -------- | -------- | ----- |
| `binary32` | 8 bits   | 23 bits  | 1 bit |
| `binary64` | 11 bits  | 52 bits  | 1 bit |

Prenons le temps de faire quelques observations.

- Une valeur encodée en virgule flottante sera toujours une approximation d'une grandeur réelle.
- La précision est d'autant plus grande que le nombre de bits de la mantisse est grand.
- La base ayant été fixée à 2, il est possible d'exprimer $1/1024$ sans erreur de précision, mais pas $1/1000$.
- Un ordinateur qui n'est pas équipé d'une FPU sera beaucoup plus lent [(10 à 100x)](https://stackoverflow.com/a/15585448/2612235) pour faire des calculs en virgule flottante.
- Bien que le standard **C99** définisse les types virgule flottante `float`, `double` et `long double`, ils ne définissent pas la précision avec laquelle ces nombres sont exprimés, car cela dépend de l'architecture du processeur utilisé.

### Simple précision

Le type `float` aussi dit à précision simple utilise un espace de stockage de 32-bits organisé en 1 bit de signe, 8 bits pour l'exposant et 23 bits pour la mantisse. Les valeurs pouvant être exprimées sont de :

- $\pm\inf$ lorsque l'exposant vaut `0xff`
- $(-1)^{\text{sign}}\cdot2^{\text{exp} - 127}\cdot1.\text{significand}$
- $0$ lorsque la mantisse vaut `0x00000`

La valeur de 1.0 est encodée :

$$
\begin{align*}
0\:01111111\:00000000000000000000000_2 &= \text{3f80}\: \text{0000}_{16} \\
&= (-1)^0 \cdot 2^{127-127} \cdot \frac{(2^{23} + 0)}{2^{23}} \\
&= 2^{0} \cdot 1.0 = 1.0
\end{align*}
$$

La valeur maximale exprimable :

$$
\begin{align*}
0\:11111110\:11111111111111111111111_2 &= \text{7f7f}\: \text{ffff}_{16} \\
&= (-1)^0 \cdot 2^{254-127} \cdot \frac{(2^{23} + 838'607)}{2^{23}} \\
&≈ 2^{127} \cdot 1.9999998807 \\
&≈ 3.4028234664 \cdot 10^{38}
\end{align*}
$$

La valeur de $-\pi$ (pi) est :

$$
\begin{align*}
1\:10000000\:10010010000111111011011_2 &= \text{4049}\: \text{0fdb}_{16} \\
&= (-1)^1 \cdot 2^{128-127} \cdot \frac{(2^{23} + 4'788'187)}{2^{23}} \\
&≈ -1 \cdot 2^{1} \cdot 1.5707963 \\
&≈ -3.14159274101
\end{align*}
$$

Vient s'ajouter les valeurs particulières suivantes :

```
0 00000000 00000000000000000000000₂ ≡ 0000 0000₁₆ ≡ 0
0 11111111 00000000000000000000000₂ ≡ 7f80 0000₁₆ ≡ inf
1 11111111 00000000000000000000000₂ ≡ ff80 0000₁₆ ≡ −inf
```

!!! info "Les nombres subnormaux"

    On l'a vu un nombre en virgule flottante simple précision s'écrit sous la forme :

    $$ (-1)^s \times (1.m) \times 2^{(e - Bias)} $$

    Les nombres subnormaux sont des nombres qui ne respectent pas la norme IEEE 754, mais qui sont tout de même représentables. Ils sont utilisés pour représenter des nombres très petits, proches de zéro. En effet, la norme IEEE 754 impose que le premier bit de la mantisse soit toujours égal à 1, ce qui implique que le nombre 0 ne peut pas être représenté. Les nombres subnormaux permettent de représenter des nombres très proches de zéro, en diminuant la précision de la mantisse.

### Double précision

La double précision est similaire à la simple précision, mais avec une mantisse à **52 bits** et **11 bits** d'exposants.

!!! exercise "Expressions arithmétiques flottantes"

    Donnez la valeur des expressions ci-dessous :

    ```text
    25. + 10. + 7. – 3.
    5. / 2.
    24. + 5. / 2.
    25. / 5. / 2.
    25. / (5. / 2.)
    2. * 13. % 7.
    1.3E30 + 1.
    ```

### Quadruple précision

Bien que ce soit marginal dans le monde de l'informatique, la quadruple précision est une norme IEEE 754 qui utilise 128 bits pour stocker les nombres réels. Elle est utilisée pour des calculs scientifiques nécessitant une très grande précision comme au CERN ou pour l'étude de modèles cosmologiques.

La quadruple précision offre une précision de 34 chiffres significatifs, soit environ 112 bits de précision. Elle est codée sur 128 bits.

Il est possible de l'utiliser avec certains compilateurs C comme GCC en utilisant le type `__float128` de la bibliothèque `<quadmath.h>`.

!!! warning

    Son utilisation ralenti considérablement les calculs, car les processeurs actuels ne sont pas optimisés pour ce type de calculs. Un processeur peut faire des calculs sur 64 bits en une seule opération, mais pour des calculs en quadruple précision, il doit faire plusieurs opérations pour chaque chiffre.

## Nombres complexes

En C, il est possible de définir des nombres complexes en utilisant le type `complex` de la bibliothèque `<complex.h>`. Les nombres complexes sont composés de deux parties, la partie réelle et la partie imaginaire. Ils sont souvent utilisés en mathématiques pour représenter des nombres qui ne peuvent pas être exprimés avec des nombres réels. Ils ont été introduits avec la version C99 du langage C.

Néanmoins les nombres complexes ne sont pas supportés par les opérateurs du langage, il est nécessaire d'utiliser des fonctions spécifiques pour effectuer des opérations sur les nombres complexes.

!!! note

    Dans des langages plus haut niveau comme le C++, le C# ou Python, les nombres complexes sont supportés nativement.

    Exemple en Python :

    ```python
    from math import sqrt
    a, b, c = 1, 2, 3
    delta = b**2 - 4*a*c # Calcul du discriminant qui sera négatif
    x1, x1 = (-b + sqrt(delta)) / (2*a), (-b - sqrt(delta)) / (2*a)
    ```

    `x1` et `x2` sont des nombres complexes.

```c
#include <stdio.h>
#include <complex.h>

int main() {
    double complex z1 = 1.0 + 2.0*I;
    double complex z2 = 3.0 + 4.0*I;

    printf("z1 = %.1f + %.1fi\n", creal(z1), cimag(z1));
    printf("z2 = %.1f + %.1fi\n", creal(z2), cimag(z2));

    double complex sum = z1 + z2;
    double complex product = z1 * z2;

    printf("sum = %.1f + %.1fi\n", creal(sum), cimag(sum));
    printf("product = %.1f + %.1fi\n", creal(product), cimag(product));

    return 0;
}
```

## Format Q (virgule fixe)

Le format [Q](<https://en.wikipedia.org/wiki/Q_(number_format)>) est une notation en virgule fixe dans laquelle le format d'un nombre est représenté par la lettre **Q** suivie de deux nombres :

1. Le nombre de bits entiers
2. Le nombre de bits fractionnaires

Ainsi, un registre 16 bits contenant un nombre allant de +0.999 à -1.0 s'exprimera **Q1.15** soit 1 + 15 valant 16 bits.

Pour exprimer la valeur pi (3.1415...) il faudra au minimum 3 bits pour représenter la partie entière, car le bit de signe doit rester à zéro. Le format sur 16 bits sera ainsi **Q4.12**.

La construction de ce nombre est facile :

1. Prendre le nombre réel
2. Le multiplier par 2 à la puissance du nombre de bits
3. Prendre la partie entière

```text
1.    3.1415926535
2.    2**12 * 3.1415926535 = 12867.963508736
3.    12867
```

Pour convertir un nombre **Q4.12** en sa valeur réelle il faut :

1. Prendre le nombre encodé en **Q4.12**
2. Diviser sa valeur 2 à la puissance du nombre de bits

```text
1.    12867
2.    12867 / 2**12 = 3.141357421875
```

On note une perte de précision puisqu'il n'est pas possible d'encoder un tel nombre dans seulement 16 bits. L'incrément positif minimal serait : $1 / 2^12 = 0.00024$. Il convient alors d'arrondir le nombre à la troisième décimale, soit 3.141.

Les opérations arithmétiques sont possibles facilement entre des nombres de mêmes types.

!!! info "Sinus rapide"

    Avec des architectures qui ne supportent pas les nombres réels, il est possible de calculer une bonne approximation du sinus en utilisant une approximation avec une série de Taylor. Les calculs sont effecutés en virgule fixe. Voici un exemple d'implémentation:

    ```c
    /**
     * A 5-order polynomial approximation to sin(x).
     * @param i   angle (with 2^15 units/circle)
     * @return    16 bit fixed point Sine value (4.12) (ie: +4096 = +1 & -4096 = -1)
     *
     * The result is accurate to within +- 1 count. ie: +/-2.44e-4.
     */
    int16_t fpsin(int16_t i)
    {
        // Convert (signed) input to a value between 0 and 8192.
        // (8192 is pi/2, which is the region of the curve fit).
        i <<= 1;
        uint8_t c = i<0; // set carry for output pos/neg

        if(i == (i|0x4000)) // flip input value to corresponding value in range [0..8192)
            i = (1<<15) - i;
        i = (i & 0x7FFF) >> 1;

        /**
         * The following section implements the formula:
         *  = y * 2^-n * ( A1 - 2^(q-p)* y * 2^-n * y * 2^-n *
         *  [B1 - 2^-r * y * 2^-n * C1 * y]) * 2^(a-q)
         * Where the constants are defined as follows:
         */
        enum {A1=3370945099UL, B1=2746362156UL, C1=292421UL};
        enum {n=13, p=32, q=31, r=3, a=12};

        uint32_t y = (C1*((uint32_t)i))>>n;
        y = B1 - (((uint32_t)i*y)>>r);
        y = (uint32_t)i * (y>>n);
        y = (uint32_t)i * (y>>n);
        y = A1 - (y>>(p-q));
        y = (uint32_t)i * (y>>n);
        y = (y+(1UL<<(q-a-1)))>>(q-a); // Rounding

        return c ? -y : y;
    }
    ```

    Source : [5th Order Polynomial Fixed-Point Sine Approximation](https://www.nullhardware.com/blog/fixed-point-sine-and-cosine-for-embedded-systems/)

### Addition

L'addition peut se faire avec ou sans saturation :

```c
typedef int16_t Q;
typedef Q Q12;

Q q_add(Q a, Q b) {
    return a + b;
}

Q q_add_sat(Q a, Q b) {
    int32_t res = (int32_t)a + (int32_t)b;
    res = res > 0x7FFF ? 0x7FFF : res
    res = res < -1 * 0x8000 ? -1 * 0x8000 : res;
    return (Q)res;
}
```

### Multiplication

Soit deux nombres 0.9 et 3.141 :

```text
┌─┬─┬─┬─╀─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│0│0│1│1│1│0││0│1│1│0│0│1│1│0│ Q4.12 (0.9) 3686
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘

┌─┬─┬─┬─╀─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│1│1│0│0│1│0││0│1│0│0│0│0│1│1│ Q4.12 (3.141) 12867
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘
```

Multiplier ces deux valeurs revient à une multiplication sur 2 fois la taille. Le résultat doit être obtenu sur 32-bits sachant que les nombres **Q** s'additionnent comme **Q4.12** x **Q4.12** donnera **Q8.24**.

On voit immédiatement que la partie entière vaut 2, donc 90% de 3.14 donnera une valeur en dessous de 3. Pour reconstruire une valeur **Q8.8** il convient de supprimer les 16-bits de poids faible.

```text
3686 * 12867 = 47227762

┌─┬─┬─┬─┬─┬─┬─┬─┦┌─┬─┬─┬─┬─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┐┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│0│0│0│0│1│0││1│1│0│1│0│0│0│0││1│0│1│0│0│0│1│1││0│1│1│1│0│0│1│0│ Q8.24
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘

┌─┬─┬─┬─┬─┬─┬─┬─┦┌─┬─┬─┬─┬─┬─┬─┬─┦
│0│0│0│0│0│0│1│0││1│1│0│1│0│0│0│0│ Q8.8
└─┴─┴─┴─┴─┴─┴─┴─┘└─┴─┴─┴─┴─┴─┴─┴─┘
```

```c
inline Q q_sat(int32_t x) {
    x = x > 0x7FFF ? 0x7FFF : x
    x = x < -1 * 0x8000 ? -1 * 0x8000 : x;
    return (Q)x;
}

inline int16_t q_mul(int16_t a, int16_t b, char q)
{
    int32_t c = (int32_t)a * (int32_t)b;
    c += 1 << (q - 1);
    return sat(c >> q);
}

inline int16_t q12_mul(int16_t a, int16_t b)
{
    return q_mul(a, b, 12);
}
```
