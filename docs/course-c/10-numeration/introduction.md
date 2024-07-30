[](){#numeration}

# Numération

La numération désigne le mode de représentation des nombres (p. ex. cardinaux, ordinaux), leur base (système binaire, ternaire, quinaire, décimal ou vicésimal), ainsi que leur codification, IEEE 754, complément à un, complément à deux. Bien comprendre les bases de la numération est important pour l'ingénieur développeur, car il est souvent amené à effectuer des opérations de bas niveau sur les nombres.

Ce chapitre n'est essentiel qu'au programmeur de bas niveau, l'électronicien ou l'informaticien technique. Bien comprendre la numération permet de mieux se représenter la manière dont l'ordinateur traite les données au niveau le plus fondamental: le bit.

## Quantité d'information (bit)

Un **bit** est l'unité d'information fondamentale qui ne peut prendre que deux états : `1` ou `0`. En électronique, cette information peut être stockée dans un élément mémoire par une charge électrique. Dans le monde réel, on peut stocker un bit avec une pièce de monnaie déposée sur le côté pile ou face. L'assemblage de plusieurs bits permet de stocker de l'information plus complexe.

Le bit est l'abréviation de *binary digit* (chiffre binaire) et est central à la théorie de l'information. Le concept a été popularisé par Claude Shannon dans son article fondateur de la théorie de l'information en 1948: *A Mathematical Theory of Communication*. Shannon y introduit le bit comme unité de mesure de l'information.

S'il existe un meuble avec huit casiers assez grands pour une pomme, et que l'on souhaite connaître le nombre de possibilités de rangement, on sait que chaque casier peut contenir une pomme ou aucune. Le nombre de possibilités est alors de $2^8 = 256$. La quantité d'information nécessaire à connaître l'état du meuble est de 8 bits.

On pourrait utiliser ce meuble, et ces pommes pour représenter son âge. Une personne de 42 ans n'aurait pas besoin de 42 pommes, mais seulement de 3. En effet, si on représente l'absence de pomme par `0` et la présence d'une pomme par `1`, on obtient :

```text
0 0 1 0 1 0 1 0
```

Si l'on souhaite représenter l'état d'un meuble beaucoup plus grand, par exemple un meuble de 64 casiers, la quantité d'information représentable est de $2^{64} = 18'446'744'073'709'551'616$, ou 64 bits. Cela permet de représenter le nombre de grains de sable sur Terre, le nombre de secondes dans 584'942 années, ou le nombre de combinaisons possibles pour un mot de passe de 8 caractères.

Les informaticiens ont l'habitude de regrouper les bits par 8 pour former un **octet**. Un octet peut donc représenter $256$ valeurs différentes. Un octet est souvent appelé un **byte** en anglais, mais ce terme est ambigu, car il peut également désigner un groupe de bits de taille variable.

Lorsque vous achetez un disque de stockage pour votre ordinateur, vous pouvez par exemple lire sur l'emballage que le disque a une capacité de 1 To (Téra-octet). Un Téra-octet est égal à $2^{40}$ octets, soit $1'099'511'627'776$ octets. Un octet égant égal à 8 bits, donc un Téra-octet est égal à $8'796'093'022'208$ bits. À titre d'information l'entièreté de Wikipédia en pèse environ 22 Go (Giga-octet). On peut donc dire que notre disque de 1 To permettrait de stocker 45 copies de Wikipédia.

Pour représenter l'état de Wikipédia, il suffirait donc d'avoir $10'225'593'776'312$ pommes et de l'armoire appropriée.

!!! exercise "Pile ou face"

    Lors d'un tir à pile ou face de l'engagement d'un match de football, l'arbitre lance une pièce de monnaie qu'il rattrape et dépose sur l'envers de sa main. Lorsqu'il annonce le résultat de ce tir, quelle quantité d'information transmet-il ?

    ??? solution

        Il transmet un seul 1 bit : équipe A ou pile ou `1`, équipe B ou face ou `0`. Il faut néanmoins encore définir à quoi correspond cette information.

!!! info "Entropie"

    On entends souvent que l'entropie est la mesure du désordre d'un système. En thermodynamique, l'entropie est une mesure de l'énergie non disponible. En informatique, l'entropie est une mesure de l'incertitude d'une information. Plus une information est incertaine, plus elle contient d'entropie. L'entropie est souvent mesurée en bits, et est utilisée en cryptographie pour mesurer la qualité d'un générateur de nombres aléatoires.

    Néanmoins l'entropie peut également être utilisée pour mesurer la quantité d'information transmise par un message. Plus un message est incertain, plus il contient d'entropie. Par exemple, si un message est composé de 8 bits, il contient 8 bits d'entropie. Si le message est composé de 16 bits, il contient 16 bits d'entropie.

## Les préfixes

On l'a vu, le nombre de bits peut être très grand et même divisé par 8 pour obtenir un nombre d'octets, il est difficile avec des nombres simples de représenter ces quantités. C'est pourquoi on utilise des préfixes.

Avec le système international d'unités, on utilise des préfixes pour exprimer des multiples de 10. Par exemple, un kilogramme est égal à 1000 grammes. La tonne est égale à 1000 kilogrammes.

En informatique, comme on utilise un système binaire en puissance de deux, rajouter un bit double la quantité d'information. On utilise donc des préfixes pour exprimer des multiples de 2. Un kilo-octet est égal à 1000 octets $10^3$, mais un kibi-octet est égal à 1024 octets $2^10$. Les préfixes binaires sont définis par l'IEC (International Electrotechnical Commission) et sont les suivants :

=== "Préfixes standards"

    Table: Préfixes standards

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

    Table: Préfixes binaires

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

## Notation positionnelle

La numération est un système de représentation des nombres. La numération décimale est un système de base 10, c'est-à-dire que chaque chiffre peut prendre 10 valeurs différentes : $0, 1, 2, 3, 4, 5, 6, 7, 8, 9$. La position des chiffres dans un nombre décimal indique la puissance de 10 à laquelle il est multiplié. Par exemple, le nombre 123 est égal à :

$$1 \times 10^2 + 2 \times 10^1 + 3 \times 10^0$$

On parle de notation positionnelle, car la position des chiffres est importante. Le chiffre le plus à droite est le chiffre des unités, le chiffre à sa gauche est le chiffre des dizaines, puis des centaines, etc.

En informatique, et particulièrement en binaire on nomme **LSB** (Least Significant Bit) le bit de poids faible et **MSB** (Most Significant Bit) le bit de poids fort. Le bit de poids faible est le bit le plus à droite, et le bit de poids fort est le bit le plus à gauche.

Faits remarquables:

- le **LSB** permet de savoir si le nombre est pair ou impair, si le **LSB** est à `0`, le nombre est pair, et s'il est à `1`, le nombre est impair.
- le **MSB** dans un nombre signé permet de savoir si le nombre est positif ou négatif. Si le **MSB** est à `0`, le nombre est positif, et s'il est à `1`, le nombre est négatif.
