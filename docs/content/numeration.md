# Numération

La numération désigne le mode de représentation des nombres (p. ex. cardinaux, ordinaux), leur base (système binaire, ternaire, quinaire, décimal ou vicésimal), ainsi que leur codification, IEEE 754, complément à un, complément à deux. Bien comprendre les bases de la numération est important pour l'ingénieur développeur, car il est souvent amené à effectuer des opérations de bas niveau sur les nombres.

Ce chapitre n'est essentiel qu'au programmeur de bas niveau, l'électronicien ou l'informaticien technique. Bien comprendre la numération permet de mieux se représenter la manière dont l'ordinateur traite les données au niveau le plus fondamental: le bit.

Un **bit** est l'unité d'information fondamentale qui peut prendre que deux états : `1` ou `0`. En électronique, cette information peut être stockée dans un élément mémoire par une charge électrique. Dans le monde réel, on peut stocker un bit avec une pièce de monnaie déposée sur le côté pile ou face. L'assemblage de plusieurs bits permet de stocker de l'information plus complexe.

!!! exercise "Pile ou face"

    Lors d'un tir à pile ou face de l'engagement d'un match de football, l'arbitre lance une pièce de monnaie qu'il rattrape et dépose sur l'envers de sa main. Lorsqu'il annonce le résultat de ce tir, quelle quantité d'information transmet-il ?

    ??? solution

        Il transmet un seul 1 bit : équipe A ou pile ou ``1``, équipe B ou face ou ``0``. Il faut néanmoins encore définir à quoi correspond cette information.

## Bases

Une base désigne la valeur dont les puissances successives interviennent dans l'écriture des nombres dans la numération positionnelle, laquelle est un procédé par lequel l'écriture des nombres est composée de chiffres ou symboles reliés à leur position voisine par un multiplicateur, appelé base du système de numération.

Sans cette connaissance à priori du système de numération utilisé, il vous est impossible d'interpréter ces nombres :

```
69128
11027
j4b12
>>!!0
九千十八
九千 零十八
```

Outre la position des symboles (l'ordre dans lequel ils apparaissent de gauche à droite) la base du système de numération utilisé est essentielle pour décoder ces nombres. Cette base définit combien de symboles différents possibles peuvent être utilisés pour coder une position.

!!! exercise Symboles binaires

    Dans la notation binaire, composés de 1 et de 0, combien de symboles existent et combien de positions y-a-t-il dans le nombre ``11001`` ?

    ??? solution

        Le nombre ``11001`` est composé de 5 positions et de deux symboles possibles par position : ``1`` et ``0``. La quantité d'information est donc de 5 bits.

### Système décimal

Le système décimal est le système de numération utilisant la base **dix** et le plus utilisé par les humains au vingt et unième siècle, ce qui n'a pas toujours été le cas. Par exemple, les anciennes civilisations de Mésopotamie (Sumer ou Babylone) utilisaient un système positionnel de base sexagésimale (60), la civilisation maya utilisait un système de base 20 de même que certaines langues celtiques dont il reste aujourd'hui quelques traces en français avec la dénomination *quatre-vingts*.

L'exemple suivant montre l'écriture de 1506 en écriture hiéroglyphique `(1000+100+100+100+100+100+1+1+1+1+1+1)`. Il s'agit d'une numération additive.

![1506 en écriture hiéroglyphique](../assets/figures/dist/encoding/hieroglyph.svg){width="20%"}

Notre système de représentation des nombres décimaux est le système de numération indo-arabe qui emploie une notation positionnelle et dix chiffres (ou symboles) allant de zéro à neuf :

```c
0 1 2 3 4 5 6 7 8 9
```

Un nombre peut être décomposé en puissance successives :

$$
1506_{10} = 1 \cdot 10^{3} + 5 \cdot 10^{2} + 0 \cdot 10^{1} + 6 \cdot 10^{0}
$$

La base dix n'est pas utilisée dans les ordinateurs, car elle nécessite la manipulation de dix états ce qui est difficile avec les systèmes logiques à deux états; le stockage d'un bit en mémoire étant généralement assuré par des transistors.

!!! exercise "Deux mains"

    Un dessin représentant deux mains humaines (composées chacune de cinq doigts) est utilisé pour représenter un chiffre. Les doigts peuvent être soit levés, soit baissés mais un seul doigt peut être levé. Quelle est la base utilisée ?

    ??? solution

        Deux mains de cinq doigts forment une paire composée de 10 doigts. Il existe donc dix possibilités, la base est donc décimale : 10.

        Si plusieurs doigts peuvent être levés à la fois, il faut réduire le système à l'unité de base "le doigt" pouvant prendre deux états : levé ou baissé. Avec dix doigts (dix positions) et 2 symboles par doigts, un nombre binaire est ainsi représenté.

### Système binaire

Le système binaire est similaire au système décimal, mais utilise la base deux. Les symboles utilisés pour exprimer ces deux états possibles sont d'ailleurs empruntés au système indo-arabe :

$$
\begin{bmatrix}
0\\
1
\end{bmatrix} =
\begin{bmatrix}
\text{true}\\
\text{false}
\end{bmatrix} =
\begin{bmatrix}
T\\
F
\end{bmatrix}
$$

En termes techniques ces états sont le plus souvent représentés par des signaux électriques dont souvent l'un des deux états est dit récessif tandis que l'autre est dit dominant. Par exemple si l'état `0` est symbolisé par un verre vide et l'état `1` par un verre contenant du liquide. L'état dominant est l'état `1`. En effet, si le verre contient déjà du liquide, en rajouter ne changera pas l'état actuel, il y aura juste plus de liquide dans le verre.

Un nombre binaire peut être également décomposé en puissance successives :

$$
1101_{2} = 1 \cdot 2^{3} + 1 \cdot 2^{2} + 0 \cdot 2^{1} + 1 \cdot 2^{0}
$$

Le nombre de possibilités pour un nombre de positions $E$ et une quantité de symboles (ou base) $b$ de 2 est simplement exprimé par :

$$
N = b^E
$$

Avec un seul `bit` il est donc possible d'exprimer 2 valeurs distinctes.

!!! exercise Base 2

    Combien de valeurs décimales peuvent être représentées avec 10-bits ?

    ??? solution

        Avec une base binaire 2 et 10 bits, le total représentable est :

        $$2^10 = 1024$$

        Soit les nombres de 0 à 1023.

### Système octal

Inventé par [Charles XII de Suède](https://fr.wikipedia.org/wiki/Charles_XII) , le système de numération octal utilise 8 symboles empruntés au système indo-arabe. Ce système pourrait avoir été utilisé par l'homme en comptant soit les jointures des phalanges proximales (trous entre les doigts), ou les doigts différents des pouces.

```text
0 1 2 3 4 5 6 7
```

Notons que l'utilisation des 8 premiers symboles du système indo-arabe est une convention d'usage bien pratique car tout humain occidental est familier de ces symboles. L'inconvénient est qu'un nombre écrit en octal pourrait être confondu avec un nombre écrit en décimal.

Comme pour le système décimal, un nombre octal peut également être décomposé en puissance successives :

$$
1607_{8} = 1 \cdot 8^{3} + 6 \cdot 8^{2} + 0 \cdot 8^{1} + 7 \cdot 8^{0}
$$

Au début de l'informatique, la base octale fut très utilisée, car il est très facile de la construire à partir de la numération binaire, en regroupant les chiffres par triplets :

```text
010'111'100'001₂ = 2741₈
```

En C, un nombre octal est écrit en préfixant la valeur à représenter d'un zéro. Attention donc à ne pas confondre :

```c
int octal = 042;
int decimal = 42;

assert(octal != decimal);
```

Il est également possible de faire référence à un caractère en utilisant l'échappement octal dans une chaîne de caractère :

```c
char cr = '\015';
char msg = "Hell\0157\040World!";
```

!!! important

    N'essayez pas de préfixer vos nombres avec des zéros lorsque vous programmer car ces nombres seraient alors interprétés en octal et non en décimal.

### Système hexadécimal

Ce système de numération positionnel en base 16 est le plus utilisé en informatique pour exprimer des grandeurs binaires. Il utilise les dix symboles du système indo-arabe, plus les lettres de A à F. Il n'y a pas de réel consensus quant à la casse des lettres qui peuvent être soit majuscules ou minuscules. Veillez néanmoins à respecter une certaine cohérence, ne mélangez pas les casses dans un même projet.

```text
0 1 2 3 4 5 6 7 8 9 A B C D E F
```

L'écriture peut également être décomposée en puissance successives :

$$
1AC7_{16} = (1 \cdot 16^{3} + 10 \cdot 16^{2} + 12 \cdot 16^{1} + 7 \cdot 16^{0})_{10} = 41415_{10}
$$

Il est très pratique en électronique et en informatique d'utiliser ce système de représentation ou chaque chiffre hexadécimal représente un quadruplet, soit deux caractères hexadécimaux par octet (n'est-ce pas élégant?):

```text
0101'1110'0001₂ = 5E1₁₆
```

L'ingénieur qui se respecte doit connaître par coeur la correspondance hexadécimale de tous les quadruplets aussi bien que ses tables de multiplication (qu'il connaît d'ailleurs parfaitement, n'est-ce pas ?)

Table: Correspondance binaire, octal, hexadécimal

| Binaire    | Hexadécimal | Octal  | Décimal |
|------------|-------------|--------|---------|
| ``0b0000`` | ``0x0``     | ``00`` | ``0``   |
| ``0b0001`` | ``0x1``     | ``01`` | ``1``   |
| ``0b0010`` | ``0x2``     | ``02`` | ``2``   |
| ``0b0011`` | ``0x3``     | ``03`` | ``3``   |
| ``0b0100`` | ``0x4``     | ``04`` | ``4``   |
| ``0b0101`` | ``0x5``     | ``05`` | ``5``   |
| ``0b0110`` | ``0x6``     | ``06`` | ``6``   |
| ``0b0111`` | ``0x7``     | ``07`` | ``7``   |
| ``0b1000`` | ``0x8``     | ``10`` | ``8``   |
| ``0b1001`` | ``0x9``     | ``11`` | ``0``   |
| ``0b1010`` | ``0xA``     | ``12`` | ``10``  |
| ``0b1011`` | ``0xB``     | ``13`` | ``11``  |
| ``0b1100`` | ``0xC``     | ``14`` | ``12``  |
| ``0b1101`` | ``0xD``     | ``15`` | ``13``  |
| ``0b1110`` | ``0xE``     | ``16`` | ``14``  |
| ``0b1111`` | ``0xF``     | ``17`` | ``15``  |


Le fichier `albatros.txt` contient un extrait du poème de Baudelaire, l'ingénieur en proie à un bogue lié à de l'encodage de caractère cherche à comprendre et utilise le programme `hexdump`
pour lister le contenu hexadécimal de son fichier et il obtient la sortie suivante sur son terminal :

```text
$ hexdump -C albatros.txt
00000000  53 6f 75 76 65 6e 74 2c  20 70 6f 75 72 20 73 27  |Souvent, pour s'|
00000010  61 6d 75 73 65 72 2c 20  6c 65 73 20 68 6f 6d 6d  |amuser, les homm|
00000020  65 73 20 64 27 c3 a9 71  75 69 70 61 67 65 0d 0a  |es d'..quipage..|
00000030  50 72 65 6e 6e 65 6e 74  20 64 65 73 20 61 6c 62  |Prennent des alb|
00000040  61 74 72 6f 73 2c 20 76  61 73 74 65 73 20 6f 69  |atros, vastes oi|
00000050  73 65 61 75 78 20 64 65  73 20 6d 65 72 73 2c 0d  |seaux des mers,.|
00000060  0a 51 75 69 20 73 75 69  76 65 6e 74 2c 20 69 6e  |.Qui suivent, in|
00000070  64 6f 6c 65 6e 74 73 20  63 6f 6d 70 61 67 6e 6f  |dolents compagno|
00000080  6e 73 20 64 65 20 76 6f  79 61 67 65 2c 0d 0a 4c  |ns de voyage,..L|
00000090  65 20 6e 61 76 69 72 65  20 67 6c 69 73 73 61 6e  |e navire glissan|
000000a0  74 20 73 75 72 20 6c 65  73 20 67 6f 75 66 66 72  |t sur les gouffr|
000000b0  65 73 20 61 6d 65 72 73  2e 0d 0a 0d 0a 2e 2e 2e  |es amers........|
000000c0  0d 0a 0d 0a 43 65 20 76  6f 79 61 67 65 75 72 20  |....Ce voyageur |
000000d0  61 69 6c 65 cc 81 2c 20  63 6f 6d 6d 65 20 69 6c  |aile.., comme il|
000000e0  20 65 73 74 20 67 61 75  63 68 65 20 65 74 20 76  | est gauche et v|
000000f0  65 75 6c 65 e2 80 af 21  0d 0a 4c 75 69 2c 20 6e  |eule...!..Lui, n|
00000100  61 67 75 c3 a8 72 65 20  73 69 20 62 65 61 75 2c  |agu..re si beau,|
00000110  20 71 75 27 69 6c 20 65  73 74 20 63 6f 6d 69 71  | qu'il est comiq|
00000120  75 65 20 65 74 20 6c 61  69 64 e2 80 af 21 0d 0a  |ue et laid...!..|
00000130  4c 27 75 6e 20 61 67 61  63 65 20 73 6f 6e 20 62  |L'un agace son b|
00000140  65 63 20 61 76 65 63 20  75 6e 20 62 72 c3 bb 6c  |ec avec un br..l|
00000150  65 2d 67 75 65 75 6c 65  2c 0d 0a 4c 27 61 75 74  |e-gueule,..L'aut|
00000160  72 65 20 6d 69 6d 65 2c  20 65 6e 20 62 6f 69 74  |re mime, en boit|
00000170  61 6e 74 2c 20 6c 27 69  6e 66 69 72 6d 65 20 71  |ant, l'infirme q|
00000180  75 69 20 76 6f 6c 61 69  74 e2 80 af 21           |ui volait...!|
0000018d
```

Il lit à gauche l'offset mémoire de chaque ligne, au milieu le contenu hexadécimal, chaque caractère encodé sur 8 bits étant symbolisés par deux caractères hexadécimaux, et à droite le texte où chaque caractère non imprimable est remplacé par un point. On observe notamment ici que :

- `é` de *équipage* est encodé avec `\xc3\xa9` ce qui est le caractère Unicode {unicode}`U+0065`
- `é` de *ailé* est encodé avec `e\xcc\x81`, soit le caractère e suivi du diacritique `´` {unicode}`U+0301`
- Une espace fine insécable `\xe2\x80\xaf` est utilisée avant les `!`, ce qui est le caractère unicode {unicode}`U+202F`, conformément à la recommandation de l'Académie française.

Ce fichier est donc convenablement encodé en UTF-8 quant au bogue de notre ami ingénieur il concerne probablement les deux manières distinctes utilisées pour encoder le `é`.

!!! exercise "Les chiffres hexadécimaux"

    Calculez la valeur décimale des nombres suivants et donnez le détail du calcul :

    ```text
    0xaaaa
    0b1100101
    0x1010
    129
    0216
    ```

    ??? solution

        ```c
        0xaaaa    ≡ 43690
        0b1100101 ≡   101
        0x1010    ≡  4112
        129       ≡   129 (n'est-ce pas ?)
        0216      ≡   142
        ```

!!! exercise "Albatros"

    Tentez de récupérer vous même le fichier :download:`albatros <../../assets/src/albatros.txt>` et d'afficher le même résultat que ci-dessus depuis un terminal de commande Linux.

    ```bash
    $ wget https://.../albatros.txt
    $ hexdump -C albatros.txt
    ```

    Si vous n'avez pas les outils ``wget`` ou ``hexdump``, tentez de les installer via la commande ``apt-get install wget hexdump``.

### Conversions de bases

La conversion d'une base quelconque en système décimal utilise la relation suivante :

$$
\sum_{i=0}^{n-1} h_i\cdot b^i
$$

où:

$n$

: Le nombre de chiffres (ou positions)

$b$

: La base du système d'entrée (ou nombre de symboles)

$h_i$

: La valeur du chiffre à la position $i$

Ainsi, la valeur `AP7` exprimée en base tritrigesimale (base 33) et utilisée pour représenter les plaques des véhicules à Hong Kong peut se convertir en décimal après avoir pris connaissance de la correspondance d'un symbole [tritrigesimal](https://en.wikipedia.org/wiki/List_of_numeral_systems) vers le système décimal :

```text
Tritrigesimal -> Décimal :

 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15

 G  H  I  K  L  M  N  P  R  S  T  U  V  W  X  Y  Z
16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32

Conversion :

AP7 -> 10 * pow(33, 2) + 23 * pow(33, 1) + 7 * pow(33, 0) -> 11'656
```

La conversion d'une grandeur décimale vers une base quelconque est malheureusement plus compliquée et nécessite d'appliquer un algorithme.

La conversion d'un nombre du système décimal au système binaire s'effectue simplement par une suite de divisions pour lesquelles on notera le reste.

Pour chaque division par 2, on note le reste et tant que le quotient n'est pas nul, on itère l'opération. Le résultat en binaire est la suite des restes lus dans le sens inverse :

```text
n = 209

209 / 2 == 104, 209 % 2 == 1  ^ sens de lecture des restes
104 / 2 ==  52, 104 % 2 == 0  |
 52 / 2 ==  26,  52 % 2 == 0  |
 26 / 2 ==  13,  26 % 2 == 0  |
 13 / 2 ==   6,  13 % 2 == 1  |
  6 / 2 ==   3,   6 % 2 == 0  |
  3 / 2 ==   1,   3 % 2 == 1  |
  1 / 2 ==   0,   1 % 2 == 1  |

209 == 0b11010001
```

!!! exercise "La numération Shadock"

    ![Les Shadocks](../assets/images/shadocks.svg){height="150px"}

    Les Shadocks ne connaissent que quatre mots: ``GA``, ``BU``, ``ZO``, ``MEU``. La vidéo [Comment compter comme les Shadocks](https://www.youtube.com/watch?v=lP9PaDs2xgQ>) en explique le principe.

    Convertir ``−⨼○◿○`` (``BU ZO GA MEU GA``) en décimal.

    ??? solution

        Le système Shadock est un système quaternaire similaire au système du génome humain basé sur quatre bases nucléiques. Assignons donc aux symboles Shadocks les symboles du système indo-arabe que nous connaissons mieux :

        ```text
        0 ○ (GA)
        1 − (BU)
        2 ⨼ (ZO)
        3 ◿ (MEU)
        ```

        Le nombre d'entrée ``−⨼O◿O`` peut ainsi s'exprimer :

        ```text
        −⨼○◿○ ≡ 12030₄
        ```

        En appliquant la méthode du cours, on obtient :

        $$
            1 \cdot 4^4 + 2 \cdot 4^3 + 0 \cdot 4^2 + 3 \cdot 4^1 + 0 \cdot 4^0 = 396_{10}
        $$

        !!! hint

            Depuis un terminal Python vous pouvez simplement utiliser ``int("12030", 4)``

## Entiers relatifs

Vous le savez maintenant, l'interprétation d'une valeur binaire n'est possible qu'en ayant connaissance de son encodage et s'agissant d'entiers, on peut se demander comment stocker des valeurs négatives car il n'existe pas de symboles pour le signe `-` (ni même d'ailleurs `+`).

Une approche naïve est de réserver une partie de la mémoire pour des entiers positifs et une autre pour des entiers négatifs et stocker la correspondance binaire/décimale simplement. L'ennui pour les **variables** c'est que le contenu peut changer et qu'il serait préférable de stocker le signe avec la valeur.

### Bit de signe

On peut se réserver un bit de signe, par exemple le 8{sup}`ième` bit d'un `char`.

```text
┌─┐┌─┬─┬─┬─┬─┬─┬─┐
│0││1│0│1│0│0│1│1│ = (0 * (-1)) * 0b1010011 = 83
└─┘└─┴─┴─┴─┴─┴─┴─┘
┌─┐┌─┬─┬─┬─┬─┬─┬─┐
│1││1│0│1│0│0│1│1│ = (1 * (-1)) * 0b1010011 = -83
└─┘└─┴─┴─┴─┴─┴─┴─┘
```

Cette méthode impose le sacrifice d'un bit et donc l'intervalle représentable est ici de `[-127..127]`. On ajoutera qu'il existe alors deux zéros, le zéro négatif `0b00000000`, et le zéro positif `0b10000000` ce qui peut poser des problèmes pour les comparaisons.

```text
000   001   010   011   100   101   110   111
-+-----+-----+-----+-----+-----+-----+-----+--->

000   001   010   011   100   101   110   111
-+-----+-----+-----+->  -+-----+-----+-----+---> Méthode du bit de signe
 0     1     2     3     0    -1    -2    -3
```

De plus les additions et soustractions sont difficiles, car il n'est pas possible d'effectuer des opérations simples :

```text
  00000010 (2)
- 00000101 (5)
----------
  11111101 (-125)    2 - 5 != -125
```

En résumé, la solution utilisant un bit de signe pose deux problèmes :

1. Les opérations ne sont plus triviales, et un algorithme particulier doit être mis en place.
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

Ainsi, il est facile d'écrire le complément à neuf :

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

(twos-complement)=

### Complément à deux

Le {index}`complément à deux` n'est rien d'autre que le complément à un **plus** un. C'est donc une amusante plaisanterie des informaticiens dans laquelle les étapes nécessaires sont :

1. Calculer le complément à un du nombre d'entrées.
2. Ajouter 1 au résultat.

Oui, et alors, quelle est la valeur ajoutée ? Surprenamment, on résout tous les problèmes amenés par le complément à un :

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

Vous l'aurez compris, le complément à deux est le mécanisme le plus utilisé dans les ordinateurs moderne pour représenté les nombres entiers négatifs.

## Opérations logiques

Les opérations logiques sont introduites par l'[algèbre de Boole](<https://fr.wikipedia.org/wiki/Alg%C3%A8bre_de_Boole_(logique)>) et permettent de combiner plusieurs grandeurs binaires en utilisant des opérations.

### Opérations bit à bit

Les {index}`opérations bit à bit` (*bitwise*) disponibles en C sont les suivantes :

Table: Opérateurs bit à bit

| Opérateur | Description       | Exemple                         |
|-----------|-------------------|---------------------------------|
| ``&``     | Conjonction (ET)  | ``(0b1101 & 0b1010) == 0b1000`` |
| ``|``     | Disjonction (OU)  | ``(0b1101 | 0b1010) == 0b1111`` |
| ``^``     | XOR binaire       | ``(0b1101 ^ 0b1010) == 0b0111`` |
| ``~``     | Complément à un   | ``~0b11011010 == 0b00100101``   |
| ``<<``    | Décalage à gauche | ``(0b1101 << 3) == 0b1101000``  |
| ``>>``    | Décalage à droite | ``(0b1101 >> 2) == 0b11``       |


!!! important

    Ne pas confondre l'opérateur `!` et l'opérateur `~`. Le premier est la négation d'un nombre tandis que l'autre est l'inversion bit à bit. La négation d'un nombre différent de zéro donnera toujours `0` et la négation de zéro donnera toujours `1`.

#### Conjonction

La conjonction ou **ET logique** ($\wedge$) est identique à la multiplication appliquée bit à bit et ne génère pas de retenue.

Table: Conjonction bit à bit

| $A ∧ B$ | $A=0$ | $A=1$ |
| ------- | ----- | ----- |
| $B=0$   | 0     | 0     |
| $B=1$   | 0     | 1     |

Avec cette opération l'état dominant est le `0` et l'état récessif est le `1`. Il suffit qu'une seule valeur soit à zéro pour forcer le résultat à zéro :

```c
assert(0b1100 & 0b0011 & 0b1111 & 0 == 0)
```

Cet opérateur est d'ailleurs souvent utilisé pour imposer une valeur nulle suivant une condition. Dans l'exemple suivant le Balrog est réduit à néant par Gandalf :

```c
balrog = 0b1100110101;
gandalf = 0;

balrog = balrog & gandalf; // You shall not pass!
```

#### Disjonction

La disjonction ou **OU logique** ($\lor$) s'apparente à l'opération `+`.

| $A ∨ B$ | $A=0$ | $A=1$ |
| ------- | ----- | ----- |
| $B=0$   | 0     | 1     |
| $B=1$   | 1     | 1     |

Ici l'état dominant est le `1` car il force n'importe quel `0` à changer d'état :

```c
bool student = false; // Veut pas faire ses devoirs ?
bool teacher = true;

student = student | teacher; // Tes devoirs tu feras...
```

#### Disjonction exclusive

Le **OU exclusif** ($\oplus$ ou $\veebar$) est une opération curieuse mais extrêmement puissante et utilisée en cryptographie.

En électronique sur les symboles CEI, l'opération logique est nommée `=1` car si le résultat de l'addition des deux opérandes est différent de `1`, la sortie sera nulle. Lorsque `A` et `B` valent `1` la somme vaut `2` et donc la sortie est nulle.

Table: Disjonction exclusive

| $A \veebar B$ | $A=0$ | $A=1$ |
| ------- | ----- | ----- |
| $B=0$   | 0     | 1     |
| $B=1$   | 1     | 0     |

L'opération présente une propriété très intéressante : elle est réversible.

```c
assert(1542 ^ 42 ^ 42 == 1542)
```

Par exemple il est possible d'inverser la valeur de deux variables simplement :

```c
int a = 123;
int b = 651;

a ^= b;
b ^= a;
a ^= b;

assert(a == 651);
assert(b == 123);
```

#### Complément à un

Le complément à un ($\lnot$) est simplement la valeur qui permet d'inverser bit à bit une valeur :

Table: Complément à un

| $A$ | $\lnot~A$ |
| --- | -------- |
| 0   | 1 |
| 1   | 0 |


### Opérateurs arithmétiques

Les opérations arithmétiques nécessitent le plus souvent d'une communication entre les bits.
C'est-à-dire en utilisant une retenue (*carry*). En base décimale, on se souvient de l'addition que l'on écrivait dans les petites écoles :

```text
  ¹¹    ← retenues
  123₁₀
+  89₁₀
-----
  212₁₀
```

En arithmétique binaire, c'est exactement la même chose :

| A   | B   | A + B | C   |
| --- | --- | ----- | --- |
| 0   | 0   | 0     | 0   |
| 0   | 1   | 1     | 0   |
| 1   | 0   | 1     | 0   |
| 1   | 1   | 0     | 1   |

```text
 ¹¹¹  ¹¹¹
  11100101₂
+  1100111₂
----------
 101001100₂
```

!!! exercise "Additions binaires"

    Une unité de calcul arithmétique (ALU) est capable d'effectuer les 4 opérations de bases comprenant additions et soustractions.

    Traduisez les opérandes ci-dessous en binaire, puis poser l'addition en binaire.

    1. $1 + 51$
    2. $51 - 7$
    3. $204 + 51$
    4. $204 + 204` (sur 8-bits$

    ??? solution

        1. $1 + 51$

            ```text
                    ¹¹
                      1₂
            +   110011₂  (2⁵ + 2⁴ + 2¹+ 2⁰ ≡ 51)
            ----------
                110100₂
            ```

        2. $51 - 7$

            ```text
              …¹¹¹  ¹¹
              …000110011₂  (2⁵ + 2⁴ + 2¹ + 2⁰ ≡ 51)
            + …111111001₂  (complément à deux) 2³ + 2¹ + 2⁰ ≡ 111₂ → !7 + 1 ≡ …111001₂)
              -----------
              …000101100₂  (2⁵ + 2³ + 2₂ ≡ 44)
            ```

        3. $204 + 51$

            ```text
                11001100₂
            +     110011₂
              -----------
              …011111111₂  (2⁸ - 1 ≡ 255)
            ```

        4. $204 + 204$ (sur 8-bits)

            ```text
                ¹|¹  ¹¹
                |11001100₂
            +   |11001100₂
              ---+--------
                1|10011000₂  (152, le résultat complet devrait être 2⁸ + 152 ≡ 408)
            ```

### Lois de De Morgan

Les [lois de De Morgan](https://fr.wikipedia.org/wiki/Lois_de_De_Morgan) sont des identités logiques formulées il y a près de deux siècles: sachant qu'en logique classique, la négation d'une conjonction implique la disjonction des négations et que la conjonction de négations implique la négation d'une disjonction, on peut alors exprimer que :

$$
\begin{align*}
& \neg (P \land Q) \Rightarrow ((\neg P) \lor (\neg Q)) \\
& ((\neg P) \land (\neg Q)) \Rightarrow \neg (P \lor Q)
\end{align*}
$$

Ces opérations logiques sont très utiles en programmation où elles permettent de simplifier certains algorithmes.

À titre d'exemple, les opérations suivantes sont donc équivalentes :

```c
int a = 0b110010011;
int b = 0b001110101;

assert(a | b == ~a & ~b);
assert(~a & ~b == ~(a | b));
```

En logique booléenne on exprime la négation par une barre p.ex. $\bar{P}$.

!!! exercise "De Morgan"

    Utiliser les relations de De Morgan pour simplifier l'expression suivante

    $$
    D \cdot E + \bar{D} + \bar{E}
    $$

    ??? solution

        Si l'on applique De Morgan ($\bar{XY} = \bar{X} + \bar{Y}$):

        $$
        D \cdot E + \bar{D} + \bar{E}
        $$

### Arrondi

En programmation, la notion d'arrondi ([rounding](https://en.wikipedia.org/wiki/Rounding)) est beaucoup plus complexe qu'imaginée. Un nombre réel peut être converti en un nombre entier de plusieurs manières dont voici une liste non exhaustive :

- **tronqué** (*truncate*) lorsque la partie fractionnaire est simplement enlevée
- **arrondi à l'entier supérieur** (*rounding up*)
- **arrondi à l'entier inférieur** (*rounding down*)
- **arrondi en direction du zéro** (*rounding towards zero*)
- **arrondi loin du zéro** (*rounding away from zero*)
- **arrondi au plus proche entier** (*rounding to the nearest integer*)
- **arrondi la moitié en direction de l'infini** (*rounding half up*)

Selon le langage de programmation et la méthode utilisée, le mécanisme d'arrondi sera différent. En C, la bibliothèque mathématique offre les fonctions `ceil` pour l'arrondi au plafond (entier supérieur), `floor` pour arrondi au plancher (entier inférieur) et `round` pour l'arrondi au plus proche (*nearest*). Il existe également fonction `trunc` qui tronque la valeur en supprimant la partie fractionnaire.

Le fonctionnement de la fonction `round` n'est pas unanime entre les mathématiciens et les programmeurs. C utilise l'arrondi au plus proche, c'est à dire que -23.5 donne -24 et 23.5 donnent 24.

!!! note

    En Python ou en Java, c'est la méthode du *commercial rounding* qui a été choisie. Elle peut paraître contre-intuitive, car `round(3.5)` donne 4, mais `round(4.5)` donne 4 aussi.


!!! exercise "Swap sans valeur intermédiaire"

    Soit deux variables entières ``a`` et ``b``, chacune contenant une valeur différente. Écrivez les instructions permettant d'échanger les valeurs de a et de b sans utiliser de valeurs intermédiaires. Indice: utilisez l'opérateur XOR ``^``.

    Testez votre solution...

    ??? solution

        ```c
        a ^= b;
        b ^= a;
        a ^= b;
        ```
