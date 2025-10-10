---
epigraph:
  text: L'informatique ne concerne pas plus les ordinateurs que l'astronomie ne concerne les télescopes... La science ne concerne pas les outils. Elle concerne la manière dont nous les utilisons et ce que nous découvrons en les utilisant.
  source: Edsger W. Dijkstra
---
[](){#numeration}

# L'information

L'information constitue le cœur battant de l'informatique : les ordinateurs la stockent, la transmettent, la traitent et la transforment en permanence. Comprendre comment elle est représentée et manipulée s'avère essentiel pour toute personne qui développe des logiciels. Nous verrons qu'elle désigne à la fois un message et les symboles mobilisés pour l'exprimer.

## Quantité d'information (bit)

Un **bit** est l'unité d'information fondamentale qui ne peut prendre que deux états : `1` ou `0`. En électronique, cette information peut être stockée dans un élément mémoire par une charge électrique. Dans le monde réel, on peut stocker un bit avec une pièce de monnaie déposée sur le côté pile ou face. La combinaison de plusieurs bits permet de former des messages plus complexes.

Le bit est l'abréviation de *binary digit* ([[chiffre]] binaire) et occupe une place centrale dans la théorie de l'information. Ce concept a été popularisé par [[Claude Shannon]] dans son article fondateur de 1948, *A Mathematical Theory of Communication*, où il introduit le bit comme unité fondamentale de mesure.

Imaginons un meuble doté de huit casiers assez grands pour accueillir une pomme. Chaque casier peut contenir soit une pomme, soit n'être pas rempli. Le nombre de configurations possibles est alors de $2^8 = 256$. Le chiffre $2$ correspond aux deux états disponibles pour chaque casier (pomme ou absence de pomme) et $8$ au nombre total de casiers. La quantité d'information nécessaire pour connaître l'état du meuble est donc de 8 bits.

Ce meuble et ces pommes pourraient tout aussi bien servir à représenter un âge. Une personne de 42 ans n'aurait pas besoin de 42 pommes, mais seulement de trois. En effet, si l'on associe l'absence de pomme à `0` et la présence d'une pomme à `1`, on peut représenter 42 ans ainsi :

```text
0 0 1 0 1 0 1 0
```

De façon analogue, si l'on souhaite représenter l'état d'un meuble beaucoup plus grand, par exemple un meuble de 64 casiers, la quantité d'information représentable serait de :

$$2^{64} = 18'446'744'073'709'551'616$$

soit 64 bits. Un tel volume suffit à coder le nombre estimé de grains de sable sur Terre, le nombre de secondes contenues dans 584'942 années ou encore l'ensemble des combinaisons possibles pour un mot de passe de 8 caractères. À l'inverse, si l'on admet qu'une personne peut vivre au maximum 127 ans, 7 bits suffisent à représenter son âge. Avec 64 pommes au plus, on peut donc représenter l'âge d'environ neuf personnes.

Ce nombre, peu importe la manière dont il est interprété, représente une certaine quantité d'information qui peut s'exprimer par la formule générale suivante :

$$I = \log_2(N)$$

où $I$ est la quantité d'information en bits, et $N$ est le nombre de possibilités.

Les informaticiens ont l'habitude d'agencer les bits par groupe de 8 pour former ce que l'on appelle un **octet**. Un [[octet]] peut donc représenter $256$ valeurs différentes. Un octet est souvent appelé un **byte** en anglais, mais ce terme reste ambigu, car il peut également désigner un groupe de bits de taille variable. Historiquement les ordinateurs ont utilisé des bytes de 6, 7, ou 8 bits, mais aujourd'hui l'octet est équivalent au *byte*.

Lorsque vous achetez un disque de stockage pour votre ordinateur, vous pouvez par exemple lire sur l'emballage que l'unité de stockage dispose d'une capacité de 1 Tio (Tébi-octet). Un Tébi-octet est égal à $2^{40}$ octets, soit $1'099'511'627'776$ octets. Un octet étant égal à 8 bits, donc un tébi (millier de milliards) d'octet est égal à $8'796'093'022'208$ bits. À titre d'information l'entièreté d'encyclopédie libre Wikipédia en pèse environ 22 Go (Giga-octet). On peut affirmer que notre disque de 1 Tio, acheté environ 50 dollars, permettrait de stocker 45 copies de Wikipédia.

Pour représenter l'état de Wikipédia, il suffirait donc d'avoir $10'225'593'776'312$ pommes et bien entendu, l'armoire idoine.

!!! exercise "Pile ou face"

    Lors d'un tir à pile ou face de l'engagement d'un match de football, l'arbitre lance une pièce de monnaie qu'il rattrape et dépose sur l'envers de sa main. Lorsqu'il annonce le résultat de ce tir, quelle quantité d'information transmet-il ?

    ??? solution

        Il transmet un seul bit d'information : équipe A (pile, `1`) ou équipe B (face, `0`). Il faut toutefois préciser préalablement à quoi correspondent ces deux valeurs.

!!! info "Entropie"

    On entend souvent que l'[[entropie]] mesure le désordre d'un système. En thermodynamique, elle correspond à l'énergie non disponible ; en informatique, elle quantifie l'incertitude d'une information. Plus une information est incertaine, plus elle contient d'entropie. Cette grandeur, fréquemment mesurée en bits, est notamment utilisée en cryptographie pour évaluer la qualité d'un générateur de nombres aléatoires.

    Néanmoins l'entropie peut également être utilisée pour mesurer la quantité d'information transmise par un message. Plus un message est incertain, plus il contient d'entropie. Par exemple, si un message est composé de 8 bits, il contient 8 bits d'entropie. Si le message est composé de 16 bits, il contient 16 bits d'entropie.

## Les préfixes

Comme évoqué, le nombre de bits peut croître très rapidement, même après division par 8 pour obtenir un nombre d'octets. Il devient alors difficile de manipuler ces valeurs et, surtout, de se les représenter mentalement. Pour y remédier, nous recourons à des préfixes. Un agriculteur évoque des tonnes de blé ou des hectares de terres ; une informaticienne ou un informaticien parle de *giga* de mémoire, de *méga* de données ou de *kilo* bits par seconde pour un débit de connexion.

Dans le système international d'unités, nous utilisons couramment des préfixes pour exprimer des multiples de dix. Par exemple, un kilogramme équivaut à 1000 grammes, une tonne à 1000 kilogrammes et un hectare à 10'000 mètres carrés.

En informatique, où l'unité fondamentale d'information suit un système binaire, chaque bit ajouté double la quantité représentable. On privilégie donc des préfixes correspondant à des puissances de deux. Par définition, un kilo-octet vaut 1000 octets ($10^3$), tandis qu'un kibi-octet en compte 1024 ($2^{10}$). Les [[préfixes binaires]] sont normalisés et définis par l'IEC (International Electrotechnical Commission). Voici un tableau des préfixes les plus courants :

=== "Préfixes standards"

    Table: Préfixes standards

    | Préfixe | Symbole | $10^n$    |
    | ------- | ------- | --------- |
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
    | ------- | ------- | --------- |
    | Kibi    | Ki      | $2^{10}$  |
    | Mébi    | Mi      | $2^{20}$  |
    | Gibi    | Gi      | $2^{30}$  |
    | Tébi    | Ti      | $2^{40}$  |
    | Pébi    | Pi      | $2^{50}$  |
    | Exbi    | Ei      | $2^{60}$  |
    | Zebi    | Zi      | $2^{70}$  |
    | Yobi    | Yi      | $2^{80}$  |

!!! info

    Les préfixes binaires restent méconnus et peu utilisés. Les disques durs sont souvent vendus en Go (Giga-octets) alors que les systèmes d'exploitation les affichent en Gio (Gibi-octets). Il est donc important de bien comprendre la différence entre ces deux unités et de les utiliser correctement pour éviter toute confusion.

## Notation positionnelle

La numération est la science de la représentation des nombres. La numération décimale est un système de [[base 10]], c'est-à-dire que chaque chiffre peut prendre dix valeurs différentes : $0, 1, 2, 3, 4, 5, 6, 7, 8, 9$. La position des chiffres dans un nombre décimal indique la puissance de 10 par laquelle il est multiplié. Par exemple, le nombre 123 est égal à :

$$1 \times 10^2 + 2 \times 10^1 + 3 \times 10^0$$

On parle ici de notation positionnelle, car la place de chaque chiffre compte, comme pour nos pommes dans leurs casiers. Le chiffre le plus à droite désigne les unités, celui immédiatement à gauche les dizaines, puis viennent les centaines, etc. Cette idée peut sembler triviale tant notre civilisation y est familière depuis des siècles. Pourtant, les systèmes de numération les plus anciens, comme ceux basés sur les os d'Ishango (datant d'environ 20'000 ans avant notre ère), ne l'utilisaient pas. Ils se contentaient souvent de marquer des quantités sans tirer parti de la position.

La véritable apparition de la notation positionnelle est attribuée aux mathématiciens indiens, autour du $5^e$ siècle de notre ère. Le système de numération indien utilisait dix symboles ($0$ à $9$), et la position de chaque chiffre dans un nombre indiquait sa valeur multiplicative par une puissance de dix. Ce système a été révolutionnaire, car il simplifiait grandement les calculs, rendant les opérations arithmétiques plus efficaces.

Ce système indien a ensuite été transmis aux savant·es arabes, qui l'ont adopté, perfectionné puis diffusé en Europe au cours du Moyen Âge. C'est ce système, connu aujourd'hui sous le nom de « système décimal » ou « système indo-arabe », qui fonde la notation positionnelle universellement employée.

Le choix du nombre de symboles reste bien entendu arbitraire. On pourrait en utiliser deux, trois ou cinquante, pourvu que leur position indique la valeur multiplicative par une puissance correspondant à ce nombre de symboles. Ce principe définit ce que nous appelons la **base** d'un système de numération.

En informatique, nous utilisons deux symboles et donc une base de deux, appelée base binaire. En binaire, on nomme **LSB** ([[Least Significant Bit]]) le bit de poids faible et **MSB** ([[Most Significant Bit]]) le bit de poids fort. Le bit de poids faible est le plus à droite et le bit de poids fort le plus à gauche. Il est remarquable de noter que le **LSB** permet de savoir si le nombre est pair ou impair : si le **LSB** vaut `0`, le nombre est pair, et s'il vaut `1`, il est impair :

```c
bool is_even(int n) {
    return (n & 1) == 0;
}
```

Le **MSB**, quant à lui, indique si un nombre signé représenté en complément à deux est positif ou négatif. Si le **MSB** vaut `0`, le nombre est positif ; s'il vaut `1`, il est négatif (on privilégiera toutefois l'expression `n < 0` pour effectuer ce test).

```c
bool is_negative(int32_t n) {
    return (n & 0x80000000) == 0x80000000;
}
```

!!! exercise "Nature de ces nombres ?"

    Pour les nombres suivants stockés sur 8-bit, pouvez-vous dire s'ils sont pairs ou impairs, positifs ou négatifs ?

    1. `0b01100000` est {{pair}} et de signe {{positif}}
    2. `0b00001001` est {{impair}} et de signe {{positif}}
    3. `0b10000000` est {{pair}} et de signe {{négatif}}
    4. `0b11011011` est {{impair}} et de signe {{négatif}}

## Codification de l'information

Nous avons vu plus haut que les nombres sont stockés sous forme de bits agencés en octets dont l'ordre importe. Cette méthode suffit pour représenter des entiers positifs, mais les nombres négatifs ou à virgule nécessitent des codifications particulières.

La norme *IEEE 754* sert à représenter les nombres à virgule flottante, tandis que le *complément à deux* code les nombres négatifs. Nous y reviendrons plus tard, car ces deux méthodes sont essentielles pour comprendre comment les valeurs sont stockées en mémoire et comment les opérations arithmétiques sont effectuées. Par ailleurs, une succession de bits peut représenter bien plus que des nombres : du texte, des images ou des programmes. *In fine*, tout est stocké sous forme de bits, et c'est leur interprétation qui permet d'en extraire un contenu utile.

## Transmission de l'information

Il est fondamental de comprendre que le stockage de l'information n'acquiert sa pleine valeur que lorsqu'elle peut être efficacement transmise et reçue. Ce processus ne se limite pas à la conservation des données : le protocole d'encodage joue un rôle tout aussi crucial. L'histoire regorge d'exemples où les vestiges des civilisations passées nous ont transmis des messages énigmatiques dont le [[déchiffrement]] reste incertain. Citons les hiéroglyphes égyptiens, les tablettes cunéiformes sumériennes ou encore les manuscrits de la mer Morte, partiellement révélés grâce aux travaux érudits de Jean-François Champollion sur la pierre de Rosette, d'Henry Rawlinson sur l'inscription de Behistun ou de William F. Albright sur les manuscrits de Qumrân. Toutefois, certaines écritures anciennes demeurent hermétiques, comme l'écriture [[rongorongo]] de l'île de Pâques. Les [[khipus]], ces cordes nouées par les Incas, offrent un autre exemple fascinant d'un système d'encodage dont le secret nous échappe encore.

L'évolution des moyens de communication nous permet aujourd'hui de transmettre des informations sur des distances inimaginables à des vitesses vertigineuses. Par exemple, la transmission d'un signal entre la Terre et Mars, à une distance moyenne d'environ 225 millions de kilomètres, prend environ 12,5 minutes. Cette durée, bien que rapide à l'échelle cosmique, impose des contraintes significatives pour les missions spatiales, obligeant à une planification méticuleuse et à une anticipation des échanges. Un autre exemple marquant est la communication avec la sonde Voyager 1, située actuellement à plus de 23 milliards de kilomètres de la Terre. Les signaux radio, voyageant à la vitesse de la lumière, mettent plus de 21 heures pour atteindre notre planète, illustrant les défis de la transmission à travers les vastes étendues de l'espace.

Pour ce qui est de la quantité d'informations, l'expérience internationale de mesure utilisant des radiotélescopes, telle que l'observation des trous noirs via l'Event Horizon Telescope (EHT), a généré des volumes de données si immenses qu'il fut plus rapide de transporter les disques durs contenant des pétaoctets d'informations par avion que de les transmettre via les réseaux de communication. Cette réalité témoigne des limites actuelles des infrastructures face à l'immensité des données produites par les sciences modernes. La transmission de l'information est donc un enjeu majeur, non seulement pour franchir les distances, mais aussi pour préserver et interpréter les données codées, à travers le temps comme à travers l'espace.

## Pérennité de l'information

La pérennité de l'information représente un défi tout aussi crucial que sa transmission. En effet, les supports physiques sur lesquels nous conservons nos données sont souvent fragiles et périssables. Le papier, qui a servi de base à la transmission du savoir pendant des siècles, s'use et se dégrade au fil du temps, même lorsqu'il est conservé dans des conditions optimales. Les bandes magnétiques, autrefois utilisées pour stocker de grandes quantités de données numériques, ont une durée de vie limitée, avec une détérioration progressive de l'information qu'elles contiennent. De même, les CD et les DVD, longtemps perçus comme des solutions de stockage robustes, ont montré leurs limites : leur surface peut se corroder, entraînant une perte irrémédiable des données.

![Arctic World Archive](/assets/images/arctic-world-archive.png)

Consciente de ces limitations, l'humanité a entrepris de consolider ses connaissances en les stockant dans des endroits spécialement conçus pour résister à l'épreuve du temps. Un des projets les plus ambitieux en la matière est l'Arctic World Archive (AWA), situé dans l'archipel de Svalbard, en Norvège, à proximité du **Global Seed Vault**. L'Arctic World Archive, ouvert en 2017, est une installation sécurisée dans une ancienne mine de charbon, enfouie sous des centaines de mètres de pergélisol. Ce projet vise à préserver les données numériques pour des siècles, voire des millénaires, en utilisant une technologie de stockage sur **PiqlFilm**, un film photosensible spécialement conçu pour garantir la durabilité des informations sans nécessiter d'électricité ou de maintenance continue.

Des institutions du monde entier, telles que les Archives nationales du Brésil, l'Agence spatiale européenne (ESA) et même GitHub, y ont déjà déposé des données importantes. GitHub, par exemple, y a archivé 21 téraoctets de données provenant de l'ensemble des dépôts publics actifs de la plateforme, garantissant ainsi la pérennité de précieuses ressources en code source pour les générations futures (voir [GitHub Archive Program](https://archiveprogram.github.com/)). Ainsi, Svalbard, avec l'Arctic World Archive, s'affirme comme un bastion de la conservation des connaissances numériques, soulignant l'importance de préserver les données dans un monde où la technologie évolue rapidement, mais où la fiabilité des supports de stockage demeure un enjeu majeur.
