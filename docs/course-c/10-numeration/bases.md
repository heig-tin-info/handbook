---
epigraph:
  text: Il y a 10 types de personnes dans le monde, celles qui comprennent le binaire, et celles qui ne le comprennent pas.
  source: Mème internet
---
# Bases

Une [[base]] désigne la valeur dont les puissances successives interviennent dans l'écriture des nombres dans la numération positionnelle, laquelle est un procédé par lequel l'écriture des nombres est composée de chiffres ou symboles reliés à leur position voisine par un multiplicateur, appelé base du système de numération.

Sans cette connaissance à priori du système de numération utilisé, il vous est impossible d'interpréter les nombres suivants :

```
69128
11027
j4b12
>>!!0
九千十八
九千 零十八
```

En effet, au-delà de l'ordre des symboles (de gauche à droite), la base du système utilisé est cruciale pour interpréter ces nombres. Cette base détermine le nombre de symboles distincts qui peuvent être employés pour chaque position, et par conséquent, elle régit la structure même du nombre. Par exemple, une base dix (décimale) utilise dix symboles (0-9), tandis qu'une base deux (binaire) n'en utilise que deux (0 et 1). Sans cette compréhension, les nombres demeurent incompréhensibles et dépourvus de signification.

!!! exercise "Symboles binaires"

    Dans la notation binaire, composés de 1 et de 0, combien de symboles existent et combien de positions y-a-t-il dans le nombre `11001` ?

    ??? solution

        Le nombre `11001` est composé de 5 positions et de deux symboles possibles par position : `1` et `0`. La quantité d'information est donc e 5 bits.

## Système décimal

Le [[système décimal]] est le système de numération utilisant la base **dix** et le plus utilisé par l'humanité au vingt et unième siècle, ce qui n'a pas toujours été le cas. Par exemple, les anciennes civilisations de Mésopotamie (Sumer ou Babylone) utilisaient un système positionnel de base [[sexagésimale]] (60) toujours utilisé pour la représentation des heures ou des angles, la civilisation maya utilisait un système de base 20 encore ancrée dans la culture française de même que certaines langues celtiques dont il reste aujourd'hui quelques traces en français avec la dénomination *quatre-vingts*.

L'exemple suivant montre l'écriture de 1506 en écriture [hiéroglyphique](https://fr.wikipedia.org/wiki/%C3%89criture_hi%C3%A9roglyphique_%C3%A9gyptienne) de :

$$ 1000+100+100+100+100+100+1+1+1+1+1+1$$

Il s'agit d'une numération additive.

![1506 en écriture hiéroglyphique](../../assets/images/hieroglyph.drawio)

Notre système de représentation des nombres décimaux est le système de numération [[indo-arabe]] qui emploie une notation positionnelle et dix chiffres (ou symboles) allant de zéro à neuf et un nombre peut se décomposer en puissances successives :

$$
1506_{10} = 1 \cdot 10^{3} + 5 \cdot 10^{2} + 0 \cdot 10^{1} + 6 \cdot 10^{0}
$$

Nous l'avons vu au chapitre précédent, la base dix n'est pas utilisée dans les ordinateurs, car elle nécessite la manipulation de dix états, ce qui est difficile avec les systèmes logiques à deux états; le stockage d'un bit en mémoire étant généralement assuré par des transistors.

!!! exercise "Deux mains"

    Un dessin représentant deux mains humaines (composées chacune de cinq doigts) est utilisé pour représenter un chiffre. Les doigts peuvent être soit levés, soit baissés mais un seul doigt peut être levé. Quelle est la base utilisée ?

    ??? solution

        Deux mains de cinq doigts forment une paire composée de 10 doigts. Il existe donc dix possibilités, la base est donc décimale : 10.

        Si plusieurs doigts peuvent être levés à la fois, il faut réduire le système à l'unité de base "le doigt" pouvant prendre deux états : levé ou baissé. Avec dix doigts (dix positions) et 2 symboles par doigts, un ombre binaire est ainsi représenté.

## Système binaire

Le [[système binaire]] est similaire au système décimal, mais utilise la base deux. Les symboles utilisés pour exprimer ces deux états possibles sont d'ailleurs empruntés au système indo-arabe :

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

Un nombre binaire peut être également décomposé en puissances successives :

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

## Système octal

Inventé par [Charles XII de Suède](https://fr.wikipedia.org/wiki/Charles_XII) , le système de numération octal utilise 8 symboles empruntés au système indo-arabe. Ce système pourrait avoir été utilisé par l'homme en comptant soit les jointures des phalanges proximales (trous entre les doigts), ou les doigts différents des pouces.

```text
0 1 2 3 4 5 6 7
```

Notons que l'utilisation des 8 premiers symboles du système indo-arabe est une convention d'usage bien pratique, car tout humain occidental est familier de ces symboles. L'inconvénient est qu'un nombre écrit en octal pourrait être confondu avec un nombre écrit en décimal. Comme pour le système décimal, un nombre octal peut également être décomposé en puissances successives :

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

## Système hexadécimal

Ce système de numération positionnel en base 16 est le plus utilisé en informatique pour exprimer des grandeurs binaires. Il utilise les dix symboles du système indo-arabe, plus les lettres de A à F. Il n'y a pas de réel consensus quant à la casse des lettres qui peuvent être soit majuscules ou minuscules. Veillez néanmoins à respecter une certaine cohérence, ne mélangez pas les casses (majuscules/minuscules) dans un même projet.

```text
0 1 2 3 4 5 6 7 8 9 A B C D E F
```

Comme pour les autres bases, l'écriture peut également être décomposée en puissances successives :

$$
1AC7_{16} = (1 \cdot 16^{3} + 10 \cdot 16^{2} + 12 \cdot 16^{1} + 7 \cdot 16^{0})_{10} = 41415_{10}
$$

La notation hexadécimale est très pratique en électronique et en informatique, car chaque chiffre hexadécimal représente un quadruplet de bits, soit deux caractères hexadécimaux par octet :

```text
0101'1110'0001₂ = 5E1₁₆
```

Tout ingénieur devrait connaître par cœur la correspondance hexadécimale de tous les quadruplets aussi bien que ses tables de multiplication (qu'il connaît d'ailleurs parfaitement, n'est-ce pas ?). La table suivante vous aidera à convertir rapidement un nombre hexadécimal en décimal :

Table: Correspondance binaire, octale, hexadécimale

| Binaire  | Hexadécimal | Octal | Décimal |
| -------- | ----------- | ----- | ------- |
| `0b0000` | `0x0`       | `00`  | `0`     |
| `0b0001` | `0x1`       | `01`  | `1`     |
| `0b0010` | `0x2`       | `02`  | `2`     |
| `0b0011` | `0x3`       | `03`  | `3`     |
| `0b0100` | `0x4`       | `04`  | `4`     |
| `0b0101` | `0x5`       | `05`  | `5`     |
| `0b0110` | `0x6`       | `06`  | `6`     |
| `0b0111` | `0x7`       | `07`  | `7`     |
| `0b1000` | `0x8`       | `10`  | `8`     |
| `0b1001` | `0x9`       | `11`  | `0`     |
| `0b1010` | `0xA`       | `12`  | `10`    |
| `0b1011` | `0xB`       | `13`  | `11`    |
| `0b1100` | `0xC`       | `14`  | `12`    |
| `0b1101` | `0xD`       | `15`  | `13`    |
| `0b1110` | `0xE`       | `16`  | `14`    |
| `0b1111` | `0xF`       | `17`  | `15`    |


Le fichier `albatros.txt` (rédigé avec `ed`, [rappelez-vous][ed]) contient un extrait du poème de Baudelaire. Un ingénieur en proie à un bogue lié à de l'encodage de caractère cherche à le résoudre et utilise le programme `hexdump`
pour lister le contenu hexadécimal de son fichier. Il obtient la sortie suivante sur son terminal :

```text
$ hexdump -C albatros.txt
0000  53 6f 75 76 65 6e 74 2c  20 70 6f 75 72 20 73 27  |Souvent, pour s'|
0010  61 6d 75 73 65 72 2c 20  6c 65 73 20 68 6f 6d 6d  |amuser, les homm|
0020  65 73 20 64 27 c3 a9 71  75 69 70 61 67 65 0d 0a  |es d'..quipage..|
0030  50 72 65 6e 6e 65 6e 74  20 64 65 73 20 61 6c 62  |Prennent des alb|
0040  61 74 72 6f 73 2c 20 76  61 73 74 65 73 20 6f 69  |atros, vastes oi|
0050  73 65 61 75 78 20 64 65  73 20 6d 65 72 73 2c 0d  |seaux des mers,.|
0060  0a 51 75 69 20 73 75 69  76 65 6e 74 2c 20 69 6e  |.Qui suivent, in|
0070  64 6f 6c 65 6e 74 73 20  63 6f 6d 70 61 67 6e 6f  |dolents compagno|
0080  6e 73 20 64 65 20 76 6f  79 61 67 65 2c 0d 0a 4c  |ns de voyage,..L|
0090  65 20 6e 61 76 69 72 65  20 67 6c 69 73 73 61 6e  |e navire glissan|
00a0  74 20 73 75 72 20 6c 65  73 20 67 6f 75 66 66 72  |t sur les gouffr|
00b0  65 73 20 61 6d 65 72 73  2e 0d 0a 0d 0a 2e 2e 2e  |es amers........|
00c0  0d 0a 0d 0a 43 65 20 76  6f 79 61 67 65 75 72 20  |....Ce voyageur |
00d0  61 69 6c 65 cc 81 2c 20  63 6f 6d 6d 65 20 69 6c  |aile.., comme il|
00e0  20 65 73 74 20 67 61 75  63 68 65 20 65 74 20 76  | est gauche et v|
00f0  65 75 6c 65 e2 80 af 21  0d 0a 4c 75 69 2c 20 6e  |eule...!..Lui, n|
0100  61 67 75 c3 a8 72 65 20  73 69 20 62 65 61 75 2c  |agu..re si beau,|
0110  20 71 75 27 69 6c 20 65  73 74 20 63 6f 6d 69 71  | qu'il est comiq|
0120  75 65 20 65 74 20 6c 61  69 64 e2 80 af 21 0d 0a  |ue et laid...!..|
0130  4c 27 75 6e 20 61 67 61  63 65 20 73 6f 6e 20 62  |L'un agace son b|
0140  65 63 20 61 76 65 63 20  75 6e 20 62 72 c3 bb 6c  |ec avec un br..l|
0150  65 2d 67 75 65 75 6c 65  2c 0d 0a 4c 27 61 75 74  |e-gueule,..L'aut|
0160  72 65 20 6d 69 6d 65 2c  20 65 6e 20 62 6f 69 74  |re mime, en boit|
0170  61 6e 74 2c 20 6c 27 69  6e 66 69 72 6d 65 20 71  |ant, l'infirme q|
0180  75 69 20 76 6f 6c 61 69  74 e2 80 af 21           |ui volait...!|
018d
```

Il lit à gauche sur la première colonne l'offset mémoire de chaque ligne, au milieu le contenu hexadécimal, chaque caractère encodé sur 8 bits étant symbolisés par deux caractères hexadécimaux, et à droite le texte où chaque caractère non imprimable est remplacé par un point. On observe notamment ici que :

- `é` de *équipage* est encodé avec `\xc3\xa9` ce qui est le caractère Unicode U+0065
- `é` de *ailé* est encodé avec `e\xcc\x81`, soit le caractère e suivi du diacritique `´` U+0301
- Une espace fine insécable `\xe2\x80\xaf` est utilisée avant les `!`, ce qui est le caractère Unicode U+202F, conformément à la recommandation de l'Académie française.

Ce fichier est donc encodé en UTF-8 quant au bogue de notre ami ingénieur, il concerne très probablement les deux manières distinctes utilisées pour encoder le `é`. La saisie du poème manque donc de cohérence et le diable est dans les détails.

Par cet exercice, on observe néanmoins l'élégance de l'encodage hexadécimal qui permet de visualiser facilement, par groupe de 8 bits, le contenu du fichier, ce qui aurait été beaucoup moins évident en binaire.

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

        ```text
        0xaaaa    ≡ 43690
        0b1100101 ≡   101
        0x1010    ≡  4112
        129       ≡   129 (n'est-ce pas ?)
        0216      ≡   142
        ```

!!! exercise "Albatros"

    Tentez de récupérer vous même le poème l'[Albatros](/assets/src/albatros.txt) de Baudelaire et d'afficher le même résultat que ci-dessus depuis un terminal de commande Linux.

    ```bash
    $ wget https://.../albatros.txt
    $ hexdump -C albatros.txt
    ```

    Si vous n'avez pas les outils `wget` ou `hexdump`, tentez de les installer ia la commande `apt-get install wget hexdump` sous Ubuntu.

## Conversions de bases

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

Ainsi, la valeur `AP7` exprimée en [[base tritrigesimale]] (base 33) et utilisée pour représenter les plaques des véhicules à Hong Kong peut se convertir en décimales après avoir pris connaissance de la correspondance d'un symbole tritrigesimal vers le système décimal :

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

    ![Les Shadocks](../../assets/images/shadocks.drawio)

    Les [[Shadocks||Shadocks, les]] ne connaissent que quatre mots: `GA`, `BU`, `ZO`, `MEU`. La vidéo éducative [comment compter comme les Shadocks](https://www.youtube.com/watch?v=lP9PaDs2xgQ) en explique le principe. Ils utilisent par conséquent une base quaternaire.

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

        Notons que depuis un terminal Python vous pouvez simplement utiliser:

        ```python
        int("12030", 4)
        ```

## Autres bases

Une autre base couramment utilisée est la [base64](https://fr.wikipedia.org/wiki/Base64), qui utilise les 26 lettres de l'alphabet latin (majuscules et minuscules), les 10 chiffres et deux symboles additionnels. Cette base est souvent utilisée pour encoder des données binaires en ASCII, par exemple pour les pièces jointes des courriels.

Elle n'est pas à proprement parler une base fondamentale, mais plutôt une méthode de codage qui utilise 64 caractères imprimables. [[||base64]]

On peut transmettre de l'information en binaire, mais cela implique de pouvoir gérer un contenu arbitraire qui n'est pas toujours évident dans des environnements prévus pour des caractères imprimables. On pourrait se dire qu'on utilise la représentation ASCII des caractères, mais de nombreux caractères ne sont pas imprimables. La base64 est une solution élégante pour encoder des données binaires en ASCII.

Prenons l'exemple de la phrase suivante:

```text
La fleur en bouquet fâne... et jamais ne renait !
```

Si l'on affiche le contenu hexadécimal de cette phrase, on obtient :

```bash
$ echo -ne 'La fleur en bouquet fâne... et jamais ne renait !'  | hexdump -C
0000  4c 61 20 66 6c 65 75 72  20 65 6e 20 62 6f 75 71  |La fleur en bouq|
0010  75 65 74 20 66 c3 a2 6e  65 2e 2e 2e 20 65 74 20  |uet f..ne... et |
0020  6a 61 6d 61 69 73 20 6e  65 20 72 65 6e 61 69 74  |jamais ne renait|
0030  20 21                                             | !|
0032
```

En [[base64]], le message est découpé en mot de 6 bits, soit 64 valeurs possibles. Chaque mot de 6 bits est ensuite converti en un caractère [[ASCII]] avec la table de codage suivante:

```text
0  000000 A    17 010001 R    34 100010 i    51 110011 z
1  000001 B    18 010010 S    35 100011 j    52 110100 0
2  000010 C    19 010011 T    36 100100 k    53 110101 1
3  000011 D    20 010100 U    37 100101 l    54 110110 2
4  000100 E    21 010101 V    38 100110 m    55 110111 3
5  000101 F    22 010110 W    39 100111 n    56 111000 4
6  000110 G    23 010111 X    40 101000 o    57 111001 5
7  000111 H    24 011000 Y    41 101001 p    58 111010 6
8  001000 I    25 011001 Z    42 101010 q    59 111011 7
9  001001 J    26 011010 a    43 101011 r    60 111100 8
10 001010 K    27 011011 b    44 101100 s    61 111101 9
11 001011 L    28 011100 c    45 101101 t    62 111110 +
12 001100 M    29 011101 d    46 101110 u    63 111111 /
13 001101 N    30 011110 e    47 101111 v
14 001110 O    31 011111 f    48 110000 w    (complément) =
15 001111 P    32 100000 g    49 110001 x
16 010000 Q    33 100001 h    50 110010 y
```

Ainsi le message commence par `4c612` ou en binaire `01001100 01100001 0010`. Découpé en paquet de 6 bits
`010011 000110 000100 10`, on utilise selon la table de codage `TGE`. Comme il s'agit d'un encodage courant,
il existe des outils pour le faire automatiquement:

```bash
echo -ne 'La fleur en bouquet fâne... et jamais ne renait !' | base64
TGEgZmxldXIgZW4gYm91cXVldCBmw6JuZS4uLiBldCBqYW1haXMgbmUgcmVuYWl0ICE=
```

Si le message n'est pas un multiple de $4\times 6$ bits, il est complété avec des zéros et le caractère `=` est ajouté à la fin du message pour indiquer le nombre de zéros ajoutés. Notre message à une longueur de 50 caractères, ou bien 400 bits, qui n'est pas divisible par 24. On complète donc avec `=`.

```bash
echo -ne 'La fleur en bouquet fâne... et jamais ne renait'  | wc -c
50
```
