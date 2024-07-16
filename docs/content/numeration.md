# Numération

La numération désigne le mode de représentation des nombres (p. ex. cardinaux, ordinaux), leur base (système binaire, ternaire, quinaire, décimal ou vicésimal), ainsi que leur codification, IEEE 754, complément à un, complément à deux. Bien comprendre les bases de la numération est important pour l'ingénieur développeur, car il est souvent amené à effectuer des opérations de bas niveau sur les nombres.

Ce chapitre n'est essentiel qu'au programmeur de bas niveau, l'électronicien ou l'informaticien technique. Bien comprendre la numération permet de mieux se représenter la manière dont l'ordinateur traite les données au niveau le plus fondamental: le bit.

## Le bit

Un **bit** est l'unité d'information fondamentale qui ne peut prendre que deux états : `1` ou `0`. En électronique, cette information peut être stockée dans un élément mémoire par une charge électrique. Dans le monde réel, on peut stocker un bit avec une pièce de monnaie déposée sur le côté pile ou face. L'assemblage de plusieurs bits permet de stocker de l'information plus complexe.

Le bit est l'abréviation de *binary digit* (chiffre binaire) et est central à la théorie de l'information. Le concept a été popularisé par Claude Shannon dans son article fondateur de la théorie de l'information en 1948: *A Mathematical Theory of Communication*. Shannon y introduit le bit comme unité de mesure de l'information.

S'il existe un meuble avec huit casiers assez grands pour une pomme, et que l'on souhaite connaître le nombre de possibilités de rangement, on sait que chaque casier peut contenir une pomme ou aucune. Le nombre de possibilités est alors de $2^8 = 256$. La quantité d'information nécessaire à connaître l'état du meuble est de 8 bits.

On pourrait utiliser ce meuble, et ces pommes pour représenter son âge. Une personne de 42 ans n'aurait pas besoin de 42 pommes, mais seulement de 3. En effet, si on représente l'absence de pomme par `0` et la présence d'une pomme par `1`, on obtient :

```text
0 0 1 0 1 0 1 0
```

Si l'on souhaite représenter l'état d'un meuble beaucoup plus grand, par exemple un meuble de 64 casiers, la quantité d'information représentable est de $2^{64} = 18'446'744'073'709'551'616$, ou 64 bits. Cela permet de représenter le nombre de grains de sable sur Terre, le nombre de secondes dans 584'942 années, ou le nombre de combinaisons possibles pour un mot de passe de 8 caractères.

Les informaticiens ont l'habitude de regrouper les bits par 8 pour former un **octet**. Un octet peut donc représenter $256$ valeurs différentes. Un octet est souvent appelé un **byte** en anglais, mais ce terme est ambigu, car il peut également désigner un groupe de bits de taille variable.

Lorsque vous achetez un disque de stockage pour votre ordinateur, vous pouvez par exemple lire sur l'emballage que le disque a une capacité de 1 To (Téra-octet). Un Téra-octet est égal à $2^{40}$ octets, soit $1'099'511'627'776$ octets. Un octet égant égal à 8 bits, donc un Téra-octet est égal à $8'796'093'022'208$ bits. À titre d'information l'entièreté de Wikipedia en pèse environ 22 Go (Giga-octet). On peut donc dire que notre disque de 1 To permettrait de stocker 45 copies de Wikipedia.

Pour représenter l'état de Wikipedia, il suffirait donc d'avoir $10'225'593'776'312$ pommes et de l'armoire appropriée.

!!! exercise "Pile ou face"

    Lors d'un tir à pile ou face de l'engagement d'un match de football, l'arbitre lance une pièce de monnaie qu'il rattrape et dépose sur l'envers de sa main. Lorsqu'il annonce le résultat de ce tir, quelle quantité d'information transmet-il ?

    ??? solution

        Il transmet un seul 1 bit : équipe A ou pile ou `1`, équipe B ou face ou `0`. Il faut néanmoins encore définir à quoi correspond cette information.

## Les préfixes

On l'a vu, le nombre de bits peut être très grand et même divisé par 8 pour obtenir un nombre d'octets, il est difficile avec des nombres simples de représenter ces quantités. C'est pourquoi on utilise des préfixes.

Avec le système international d'unités, on utilise des préfixes pour exprimer des multiples de 10. Par exemple, un kilogramme est égal à 1000 grammes. La tonne est égale à 1000 kilogrammes.

En informatique, comme on utilise un système binaire en puissance de deux, rajouter un bit double la quantité d'information. On utilise donc des préfixes pour exprimer des multiples de 2. Un kilo-octet est égal à 1000 octets $10^3$, mais un kibi-octet est égal à 1024 octets $2^10$. Les préfixes binaires sont définis par l'IEC (International Electrotechnical Commission) et sont les suivants :

=== "Préfixes standards"

    | Préfixe | Symbole | $10^n$    |
    |---------|---------|-----------|
    | Kilo    | K       | $10^3$    |
    | Méga    | M       | $10^6$    |
    | Giga    | G       | $10^9$    |
    | Téra    | T       | $10^{12}$ |
    | Peta    | P       | $10^{15}$ |
    | Exa     | E       | $10^{18}$ |
    | Zetta   | Z       | $10^{21}$ |
    | Yotta   | Y       | $10^{24}$ |

=== "Préfixes binaires"

    | Préfixe | Symbole | $2^{10n}$ |
    |---------|---------|-----------|
    | Kibi    | Ki      | $2^{10}$  |
    | Mébi    | Mi      | $2^{20}$  |
    | Gibi    | Gi      | $2^{30}$  |
    | Tébi    | Ti      | $2^{40}$  |
    | Pébi    | Pi      | $2^{50}$  |
    | Exbi    | Ei      | $2^{60}$  |
    | Zebi    | Zi      | $2^{70}$  |
    | Yobi    | Yi      | $2^{80}$  |

!!! info

    Les préfixes binaires sont méconnus et peu utilisés par le marketing. Les disques durs sont souvent vendus en Go (Giga-octets) alors que les systèmes d'exploitation les affichent en Gio (Gibi-octets). Il est donc important de bien comprendre la différence entre ces deux unités.

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

    Dans la notation binaire, composés de 1 et de 0, combien de symboles existent et combien de positions y-a-t-il dans le nombre `11001` ?

    ??? solution

        Le nombre `11001` est composé de 5 positions et de deux symboles possibles par position : `1` et `0`. La quantité d'information est donc de 5 bits.

### Système décimal

Le système décimal est le système de numération utilisant la base **dix** et le plus utilisé par les humains au vingt et unième siècle, ce qui n'a pas toujours été le cas. Par exemple, les anciennes civilisations de Mésopotamie (Sumer ou Babylone) utilisaient un système positionnel de base sexagésimale (60), la civilisation maya utilisait un système de base 20 de même que certaines langues celtiques dont il reste aujourd'hui quelques traces en français avec la dénomination *quatre-vingts*.

L'exemple suivant montre l'écriture de 1506 en écriture hiéroglyphique `(1000+100+100+100+100+100+1+1+1+1+1+1)`. Il s'agit d'une numération additive.

![1506 en écriture hiéroglyphique](../assets/images/hieroglyph.drawio){width="20%"}

Notre système de représentation des nombres décimaux est le système de numération indo-arabe qui emploie une notation positionnelle et dix chiffres (ou symboles) allant de zéro à neuf :

```c
0 1 2 3 4 5 6 7 8 9
```

Un nombre peut être décomposé en puissance successive :

$$
1506_{10} = 1 \cdot 10^{3} + 5 \cdot 10^{2} + 0 \cdot 10^{1} + 6 \cdot 10^{0}
$$

La base dix n'est pas utilisée dans les ordinateurs, car elle nécessite la manipulation de dix états, ce qui est difficile avec les systèmes logiques à deux états; le stockage d'un bit en mémoire étant généralement assuré par des transistors.

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

Un nombre binaire peut être également décomposé en puissance successive :

$$
1101_{2} = 1 \cdot 2^{3} + 1 \cdot 2^{2} + 0 \cdot 2^{1} + 1 \cdot 2^{0}
$$

Le nombre de possibilités pour un nombre de positions $E$ et une quantité de symboles (ou base) $b$ de 2 est simplement exprimé par :

$$
N = b^E
$$

Avec un seul `bit` il est donc possible d'exprimer 2 valeurs distinctes.

!!! exercise "Base 2"

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

Notons que l'utilisation des 8 premiers symboles du système indo-arabe est une convention d'usage bien pratique, car tout humain occidental est familier de ces symboles. L'inconvénient est qu'un nombre écrit en octal pourrait être confondu avec un nombre écrit en décimal.

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

L'écriture peut également être décomposée en puissance successive :

$$
1AC7_{16} = (1 \cdot 16^{3} + 10 \cdot 16^{2} + 12 \cdot 16^{1} + 7 \cdot 16^{0})_{10} = 41415_{10}
$$

Il est très pratique en électronique et en informatique d'utiliser ce système de représentation ou chaque chiffre hexadécimal représente un quadruplet, soit deux caractères hexadécimaux par octet (n'est-ce pas élégant?):

```text
0101'1110'0001₂ = 5E1₁₆
```

L'ingénieur qui se respecte doit connaître par cœur la correspondance hexadécimale de tous les quadruplets aussi bien que ses tables de multiplication (qu'il connaît d'ailleurs parfaitement, n'est-ce pas ?)

Table: Correspondance binaire, octal, hexadécimal

| Binaire    | Hexadécimal | Octal  | Décimal |
|------------|-------------|--------|---------|
| `0b0000` | `0x0`     | `00` | `0`   |
| `0b0001` | `0x1`     | `01` | `1`   |
| `0b0010` | `0x2`     | `02` | `2`   |
| `0b0011` | `0x3`     | `03` | `3`   |
| `0b0100` | `0x4`     | `04` | `4`   |
| `0b0101` | `0x5`     | `05` | `5`   |
| `0b0110` | `0x6`     | `06` | `6`   |
| `0b0111` | `0x7`     | `07` | `7`   |
| `0b1000` | `0x8`     | `10` | `8`   |
| `0b1001` | `0x9`     | `11` | `0`   |
| `0b1010` | `0xA`     | `12` | `10`  |
| `0b1011` | `0xB`     | `13` | `11`  |
| `0b1100` | `0xC`     | `14` | `12`  |
| `0b1101` | `0xD`     | `15` | `13`  |
| `0b1110` | `0xE`     | `16` | `14`  |
| `0b1111` | `0xF`     | `17` | `15`  |


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

Ce fichier est donc convenablement encodé en UTF-8 quant au bogue de notre ami ingénieur, il concerne probablement les deux manières distinctes utilisées pour encoder le `é`.

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

    Si vous n'avez pas les outils `wget` ou `hexdump`, tentez de les installer via la commande `apt-get install wget hexdump`.

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

Ainsi, la valeur `AP7` exprimée en base tritrigesimale (base 33) et utilisée pour représenter les plaques des véhicules à Hong Kong peut se convertir en décimales après avoir pris connaissance de la correspondance d'un symbole [tritrigesimal](https://en.wikipedia.org/wiki/List_of_numeral_systems) vers le système décimal :

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

    ![Les Shadocks](../assets/images/shadocks.svg){height="300px"}

    Les Shadocks ne connaissent que quatre mots: `GA`, `BU`, `ZO`, `MEU`. La vidéo [Comment compter comme les Shadocks](https://www.youtube.com/watch?v=lP9PaDs2xgQ>) en explique le principe.

    Convertir `−⨼○◿○` (`BU ZO GA MEU GA`) en décimal.

    ??? solution

        Le système Shadock est un système quaternaire similaire au système du génome humain basé sur quatre bases nucléiques. Assignons donc aux symboles Shadocks les symboles du système indo-arabe que nous connaissons mieux :

        ```text
        0 ○ (GA)
        1 − (BU)
        2 ⨼ (ZO)
        3 ◿ (MEU)
        ```

        Le nombre d'entrée `−⨼O◿O` peut ainsi s'exprimer :

        ```text
        −⨼○◿○ ≡ 12030₄
        ```

        En appliquant la méthode du cours, on obtient :

        $$
            1 \cdot 4^4 + 2 \cdot 4^3 + 0 \cdot 4^2 + 3 \cdot 4^1 + 0 \cdot 4^0 = 396_{10}
        $$

        !!! hint

            Depuis un terminal Python vous pouvez simplement utiliser `int("12030", 4)`

## Entiers simples

Les entiers sont les premiers types de données manipulés par les ordinateurs. Ils sont stockés en mémoire sous forme de bits. En choisissant la taille de stockage des entiers, on détermine la plage de valeurs que l'on peut représenter. Un entier de 8 bits peut représenter $2^8 = 256$ valeurs différentes, de 0 à 255. Un entier de 16 bits peut représenter $2^{16} = 65536$ valeurs différentes, de 0 à 65535.

Cette manière est élégante, mais elle ne permet pas de représenter des valeurs négatives. Pour cela, on aura recours aux entiers relatifs.

## Entiers relatifs

Vous le savez maintenant, l'interprétation d'une valeur binaire n'est possible qu'en ayant connaissance de son encodage et s'agissant d'entiers, on peut se demander comment stocker des valeurs négatives, car il n'existe pas de symboles pour le signe `-` (ni même d'ailleurs `+`).

Une approche naïve est de réserver une partie de la mémoire pour des entiers positifs et une autre pour des entiers négatifs et stocker la correspondance binaire/décimale simplement. L'ennui pour les **variables** c'est que le contenu peut changer et qu'il serait préférable de stocker le signe avec la valeur.

### Bit de signe

On peut se réserver un bit de signe, par exemple le 8{sup}`e` bit d'un `char`.

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

[](){#twos_complement}

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

## Les nombres réels

Mathématiquement, les [nombres réels](https://fr.wikipedia.org/wiki/Nombre_r%C3%A9el) $\mathbb{R}$, sont des nombres qui peuvent être représentés par une partie entière, et une liste finie ou infinie de décimales. En informatique, stocker une liste infinie de décimale demanderait une quantité infinie de mémoire et donc, la [précision arithmétique](https://fr.wikipedia.org/wiki/Pr%C3%A9cision_arithm%C3%A9tique) est contrainte.

Au début de l'ère des ordinateurs, il n'était possible de stocker que des nombres entiers, mais
le besoin de pouvoir stocker des nombres réels s'est rapidement fait sentir. La transition s'est faite progressivement, d'abord par l'apparition de la [virgule fixe](https://fr.wikipedia.org/wiki/Virgule_fixe), puis par la [virgule flottante](https://fr.wikipedia.org/wiki/Virgule_flottante).

Le premier ordinateur avec une capacité de calcul en virgule flottante date de 1942 (ni vous ni moi n'étions probablement né) avec le [Zuse's Z4](https://fr.wikipedia.org/wiki/Zuse_4), du nom de son inventeur [Konrad Zuse](https://fr.wikipedia.org/wiki/Konrad_Zuse).

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

Le type `float` aussi dit à {index}`précision simple` utilise un espace de stockage de 32-bits organisé en 1 bit de signe, 8 bits pour l'exposant et 23 bits pour la mantisse. Les valeurs pouvant être exprimées sont de :

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
