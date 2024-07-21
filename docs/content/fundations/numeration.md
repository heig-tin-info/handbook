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

![1506 en écriture hiéroglyphique]({assets}/images/hieroglyph.drawio){width="20%"}

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

``` { .c .annotate }
int octal = 042; // (1)!
int decimal = 42;

assert(octal != decimal);
```

1. La valeur `042` est un nombre octal, soit $4 \cdot 8^1 + 2 \cdot 8^0 = 34$ en décimal. En C un nombre octal est préfixé par un zéro.

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

    Tentez de récupérer vous même le fichier :download:`albatros <{assets}/src/albatros.txt>` et d'afficher le même résultat que ci-dessus depuis un terminal de commande Linux.

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

    ![Les Shadocks]({assets}/images/shadocks.svg){height="300px"}

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

## Nombres

![Ensemble des nombres]({assets}/images/ensembles.drawio)

Vous avez tous appris dans votre enfance à compter, puis vous avez appris que les nombres se classifient dans des ensembles. Les mathématiciens ont défini des ensembles de nombres pour lesquels des propriétés particulières sont vérifiées ; ces ensembles sont imbriqués les uns dans les autres, et chaque ensemble est un sous-ensemble de l'ensemble suivant.

$$
\mathbb{N} \in \mathbb{Z} \in \mathbb{Q} \in \mathbb{R} \in \mathbb{C} \in \mathbb{H} \in \mathbb{O} \in \mathbb{S}
$$

- $\mathbb{N}$ : ensemble des entiers naturels (0, 1, 2, 3, ...)
- $\mathbb{Z}$ : ensemble des entiers relatifs (..., -3, -2, -1, 0, 1, 2, 3, ...)
- $\mathbb{D}$ : ensemble des décimaux (-0.1, 0, 0.1, 0.2, 0.3, ...)
- $\mathbb{Q}$ : ensemble des rationnels (0, 1, 1/2, 1/3, 1/4, ...)
- $\mathbb{R}$ : ensemble des réels ($\pi$, $\sqrt{2}$, ...)
- $\mathbb{C}$ : ensemble des complexes ($i$, $1 + i$, ...)
- $\mathbb{H}$ : ensemble des quaternions ($1 + i + j + k$, ...)
- $\mathbb{O}$ : ensemble des octonions
- $\mathbb{S}$ : ensemble des sédénions

!!! note "Quaternions, octonions et sédénions"

    Les quaternions, octonions et sédénions sont des nombres hypercomplexes qui généralisent les nombres complexes. Ils sont utilisés en physique pour décrire les rotations dans l'espace.

    Les quaternions sont utilisés en informatique pour représenter les rotations en 3D. Les octonions et sédénions sont des généralisations des quaternions, mais ils sont moins utilisés en pratique.

    A chaque fois que s'éloigne du réel (et c'est une manière amusante de le dire), on perd des propriétés intéressantes. Les nombres complexes ne sont pas ordonnés, les quaternions ne sont pas commutatifs, les octonions ne sont pas associatifs, et les sédénions ne sont même pas alternatifs. Un nombre alternatif est un nombre pour lequel la formule

    $$
    (a \cdot a) \cdot b = a \cdot (a \cdot b)$
    $$

     est vérifiée.

     En pratique dans une carrière d'ingénieur, vous n'aurez jamais à manipuler ni des quaternions, ni octonions ou sédénions. Les nombres complexes sont néanmoins une extension des nombres réels qui sont utilisés en physique et en mathématiques.

Un nombre arbitraire n'est pas directement associé à une quantité d'information. Le nombre $\pi$ est irrationnel, c'est à dire qu'il ne se termine jamais et ne se répète jamais. Il est donc impossible de stocker $\pi$ en mémoire, car il faudrait une quantité infinie de bits pour le représenter.

Archimère disait : Δός μοι πᾶ στῶ καὶ τὰν γᾶν κινάσω (Donnez-moi un point d'appui et je soulèverai le monde). Le Créateur, s'il existe, aurait pu dire : Donnez moi un nombre et je vous construirai l'univers ! Bien entendu la quantité d'information dans l'univers est colossale, elle croît avec l'entropie et donc avec le temps qui passe.

!!! info Minecraft

    Dans Minecraft, lorsque vous créez un monde, vous pouvez utiliser une graine pour générer un monde aléatoire. Cette graine est un nombre fini qui sert de base à l'algorithme de génération de monde. Si vous utilisez la même graine, vous obtiendrez le même monde.

    Mais pour que cela fonctionne il faut le code source de Minecraft, lui aussi c'est une succession de 0 et de 1, et donc c'est un nombre, lui aussi fini.

    Enfin, lorsque vous jouez, vos actions génèrent de l'information qui influence le monde, et donc la quantité d'information dans le monde croît. C'est pour cela que plus vous jouez, plus la sauvegarde de votre monde devient grande, mais vous pouvez la représenter aussi avec un nombre fini.

Les mémoires des ordinateurs ne sont pas infinies, elles sont limitées par la quantité de transistors qui les composent. Il n'est donc pas possible d'y stocker n'importe quel nombre. $\pi$ ne peut pas être stocké en mémoire, mais une approximation de $\pi$ peut l'être.

Aussi, l'informatique impose certaines limitations sur les nombres que l'on peut manipuler. Les nombres entiers sont les plus simples à manipuler, mais ils sont limités par la taille de la mémoire et la manière dont on les enregistres en mémoire. C'est ce que nous allons voir.

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

L'ennui pour les **variables** c'est que le contenu peut changer et qu'un nombre négatif pourrait très bien devenir positif après un calcul. Il faudrait alors le déplacer d'une région mémoire à une autre. Ce n'est donc pas la meileure méthode.

On pourrait alors renseigner la nature du nombre, c'est à dire son signe avec sa valeur.

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

Il faudrait donc trouver une méthode qui permetterait de conserver la possibilité de faire les opérations directement en binaire. En d'autres termes on aimerait pouvoir calculer en base deux sans se soucier du signe :

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

Ainsi, il est facile d'écrire le complément à neuf d'un nombre en base dix car on s'arrange pour que chaque chiffre composant le nombre on trouve un autre chiffre dont la somme est égale à neuf.

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

Pour réaliser ce complément à deux (complément à un plus un) il y a deux étapes :

1. Calculer le complément à un du nombre d'entrée.
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

### Nombres complexes

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

On note une perte de précision puisqu'il n'est pas possible d'encoder un tel nombre dans seulement 16 bits. L'incrément positif minimal serait : $1 / 2^12 = 0.00024$. Il convient alors d'arrondir le nombre à la troisième décimale soit 3.141.

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

Multiplier ces deux valeurs revient à une multiplication sur 2 fois la taille. Le résultat doit être obtenu sur 32-bits sachant que les nombre **Q** s'additionnent comme **Q4.12** x **Q4.12** donnera **Q8.24**.

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