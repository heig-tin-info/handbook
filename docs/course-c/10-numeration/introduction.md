---
epigraph:
  text: L'informatique ne concerne pas plus les ordinateurs que l'astronomie ne concerne les télescopes... La science ne concerne pas les outils. Elle concerne la manière dont nous les utilisons et ce que nous découvrons en les utilisant.
  source: Edsger W. Dijkstra
---
[](){#numeration}

# L'information

La [[numération]] désigne le mode de représentation des nombres (p. ex. cardinaux, ordinaux), leur base (système binaire, ternaire, quinaire, décimal ou vicésimal), ainsi que leur codification, IEEE 754, [[complément à un]], [[complément à deux]]. Bien comprendre les bases de la numération est important pour l'ingénieur développeur, car il est souvent amené à effectuer des opérations de bas niveau sur les nombres.

Ce chapitre n'est essentiel qu'au programmeur de bas niveau, l'électronicien ou l'informaticien technique. Bien comprendre la numération permet de mieux se représenter la manière dont l'ordinateur traite les données au niveau le plus fondamental: le [[bit|bit|bit, le]].

## Quantité d'information (bit)

Un **bit** est l'unité d'information fondamentale qui ne peut prendre que deux états : `1` ou `0`. En électronique, cette information peut être stockée dans un élément mémoire par une charge électrique. Dans le monde réel, on peut stocker un bit avec une pièce de monnaie déposée sur le côté pile ou face. L'assemblage de plusieurs bits permet de stocker de l'information plus complexe.

Le bit est l'abréviation de *binary digit* ([[chiffre]] binaire) et est central à la théorie de l'information. Le concept a été popularisé par [[Claude Shannon]] dans son article fondateur de la théorie de l'information en 1948: *A Mathematical Theory of Communication*. Shannon y introduit le bit comme unité de mesure de l'information.

S'il existe un meuble avec huit casiers assez grands pour une pomme, et que l'on souhaite connaître le nombre de possibilités de rangement, on sait que chaque casier peut contenir soit une pomme, soit oaucune. Le nombre de possibilités est alors de $2^8 = 256$. La quantité d'information nécessaire à connaître l'état du meuble est de 8 bits.

On pourrait utiliser ce meuble, et ces pommes pour représenter son âge. Une personne de 42 ans n'aurait pas besoin de 42 pommes, mais seulement de 3. En effet, si on représente l'absence de pomme par `0` et la présence d'une pomme par `1`, on obtient :

```text
0 0 1 0 1 0 1 0
```

Si l'on souhaite représenter l'état d'un meuble beaucoup plus grand, par exemple un meuble de 64 casiers, la quantité d'information représentable est de :

$$2^{64} = 18'446'744'073'709'551'616$$

ou 64 bits. Cela permet de représenter le nombre de grains de sable sur Terre, le nombre de secondes dans 584'942 années, ou le nombre de combinaisons possibles pour un mot de passe de 8 caractères.

La quantité d'information peut s'exprimer par la formule suivante :

$$I = \log_2(N)$$

où $I$ est la quantité d'information en bits, et $N$ est le nombre de possibilités.

Les informaticiens ont l'habitude de regrouper les bits par 8 pour former un **octet**. Un [[octet]] peut donc représenter $256$ valeurs différentes. Un octet est souvent appelé un **byte** en anglais, mais ce terme est ambigu, car il peut également désigner un groupe de bits de taille variable.

Lorsque vous achetez un disque de stockage pour votre ordinateur, vous pouvez par exemple lire sur l'emballage que le disque a une capacité de 1 To (Téra-octet). Un Téra-octet est égal à $2^{40}$ octets, soit $1'099'511'627'776$ octets. Un octet égant égal à 8 bits, donc un Téra-octet est égal à $8'796'093'022'208$ bits. À titre d'information l'entièreté de Wikipédia en pèse environ 22 Go (Giga-octet). On peut donc dire que notre disque de 1 To permettrait de stocker 45 copies de Wikipédia.

Pour représenter l'état de Wikipédia, il suffirait donc d'avoir $10'225'593'776'312$ pommes et de l'armoire appropriée.

!!! exercise "Pile ou face"

    Lors d'un tir à pile ou face de l'engagement d'un match de football, l'arbitre lance une pièce de monnaie qu'il rattrape et dépose sur l'envers de sa main. Lorsqu'il annonce le résultat de ce tir, quelle quantité d'information transmet-il ?

    ??? solution

        Il transmet un seul 1 bit d'information : équipe A ou pile ou `1`, équipe B ou face ou `0`. Il faut néanmoins encore définir à quoi correspond cette information.

!!! info "Entropie"

    On entends souvent que l'[[entropie]] est la mesure du désordre d'un système. En thermodynamique, l'entropie est une mesure de l'énergie non disponible. En informatique, l'entropie est une mesure de l'incertitude d'une information. Plus une information est incertaine, plus elle contient d'entropie. L'entropie est souvent mesurée en bits, et est utilisée en cryptographie pour mesurer la qualité d'un générateur de nombres aléatoires.

    Néanmoins l'entropie peut également être utilisée pour mesurer la quantité d'information transmise par un message. Plus un message est incertain, plus il contient d'entropie. Par exemple, si un message est composé de 8 bits, il contient 8 bits d'entropie. Si le message est composé de 16 bits, il contient 16 bits d'entropie.

## Les préfixes

On l'a vu, le nombre de bits peut être très grand et même divisé par 8 pour obtenir un nombre d'octets, il est difficile avec des nombres simples de représenter ces quantités. C'est pourquoi on utilise des préfixes.

Avec le système international d'unités, on utilise des préfixes pour exprimer des multiples de 10. Par exemple, un kilogramme est égal à 1000 grammes. La tonne est égale à 1000 kilogrammes.

En informatique, comme on utilise un système binaire en puissance de deux, rajouter un bit double la quantité d'information. On utilise donc des préfixes pour exprimer des multiples de 2. Un kilo-octet est égal à 1000 octets $10^3$, mais un kibi-octet est égal à 1024 octets $2^10$. Les [[préfixes binaires]] sont définis par l'IEC (International Electrotechnical Commission) et sont les suivants :

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

    Les préfixes binaires sont méconnus et peu utilisés par le marketing. Les disques durs sont souvent vendus en Go (Giga-octets) alors que les systèmes d'exploitation les affichent en Gio (Gibi-octets). Il est donc important de bien comprendre la différence entre ces deux unités.

## Notation positionnelle

La numération est un système de représentation des nombres. La numération décimale est un système de [[base 10]], c'est-à-dire que chaque chiffre peut prendre 10 valeurs différentes : $0, 1, 2, 3, 4, 5, 6, 7, 8, 9$. La position des chiffres dans un nombre décimal indique la puissance de 10 à laquelle il est multiplié. Par exemple, le nombre 123 est égal à :

$$1 \times 10^2 + 2 \times 10^1 + 3 \times 10^0$$

On parle de notation positionnelle, car la position des chiffres est importante. Le chiffre le plus à droite est le chiffre des unités, le chiffre à sa gauche est le chiffre des dizaines, puis des centaines, etc. Cela semble pour vous et moi une évidence et notre civilisation y est familiarisée depuis des siècles. Les systèmes de numération les plus anciens, comme ceux basés sur les os d'Ishango (datant d'environ 20'000 ans avant notre ère), n'utilisaient pas ce concept. Ces systèmes se contentaient souvent de représenter des quantités par des marques ou des symboles sans utiliser la position pour indiquer des valeurs différentes.

La véritable apparition de la notation positionnelle est attribuée aux mathématiciens indiens, autour du 5^e siècle de notre ère. Le système de numération indien utilisait dix symboles (0-9), et la position de chaque chiffre dans un nombre indiquait sa valeur multiplicative par une puissance de dix. Ce système a été révolutionnaire car il simplifiait grandement les calculs, rendant les opérations arithmétiques plus efficaces.

Ce système indien a ensuite été transmis aux Arabes, qui l'ont adopté et perfectionné avant de le diffuser en Europe au cours du Moyen Âge. C'est ce système, connu aujourd'hui sous le nom de "système décimal" ou "système indo-arabe", qui est à la base de la notation positionnelle utilisée universellement de nos jours.

En informatique, c'est naturellement cette notation qui est utilisée. En binaire on nomme **LSB** ([[Least Significant Bit]]) le bit de poids faible et **MSB** ([[Most Significant Bit]]) le bit de poids fort. Le bit de poids faible est le bit le plus à droite, et le bit de poids fort est le bit le plus à gauche.

Il est remarquable de noter que le **LSB** permet de savoir si le nombre est pair ou impair, si le **LSB** est à `0`, le nombre est pair, et s'il est à `1`, le nombre est impair :

```c
bool is_even(int n) {
    return n & 1 == 0;
}
```

Le **MSB** quant à lui permet de savoir si le nombre est positif ou négatif dans un nombre signé utilisant le comlément à deux. Si le **MSB** est à `0`, le nombre est positif, et s'il est à `1`, le nombre est négatif (on préfèrera plutôt utiliser `n < 0` pour vérifier si un nombre est négatif).

```c
bool is_negative(int32_t n) {
    return n & 0x80000000 == 0x80000000;
}
```

!!! exercise "Nature de ces nombres ?"

    Pour les nombres suivants stockés sur 8-bit, pouvez-vous dire s'ils sont pairs ou impairs, positifs ou négatifs ?

    1. `0b01100000` est {{pair}} et de signe {{positif}}
    2. `0b00001001` est {{impair}} et de signe {{positif}}
    3. `0b10000000` est {{pair}} et de signe {{négatif}}
    4. `0b11011011` est {{impair}} et de signe {{négatif}}

## Codification des nombres en informatique

On a vu plus haut que les nombres en informatiques sont stockés sous forme de bits agencés en octets et dont l'ordre est important. Cette méthode permet de représenter les nombres entiers positifs mais pour représenter les nombres négatifs ou les nombres à virgule, il faut utiliser des méthodes de codification spécifiques.

On utilise la norme IEEE 754 pour représenter les nombres à virgule et le complément à deux pour représenter les nombres négatifs. Ces deux méthodes sont essentielles pour comprendre comment les nombres sont stockés en mémoire et comment les opérations arithmétiques sont effectuées. Nous allons les étudier en détail dans les sections suivantes.

Voici une version enrichie et plus précise de votre texte, intégrant des exemples concrets de vitesse de communication et de quantité d'informations transmises :

## Transmission de l'information

Il est fondamental de comprendre que le stockage de l'information n'acquiert toute sa valeur que lorsque cette information peut être efficacement transmise et reçue. Ce processus ne se limite pas à la simple conservation des données : le protocole d'encodage joue un rôle tout aussi crucial. L'histoire regorge d'exemples où les vestiges des civilisations passées nous ont transmis des messages énigmatiques, dont le déchiffrement reste incertain. Parmi ces exemples, on peut citer les hiéroglyphes égyptiens, les tablettes cunéiformes sumériennes ou encore les manuscrits de la mer Morte, qui ont été partiellement révélés grâce aux travaux érudits de Jean-François Champollion sur la pierre de Rosette, d'Henry Rawlinson sur l'inscription de Behistun, ou encore de William F. Albright sur les manuscrits de Qumrân. Toutefois, il subsiste des écritures anciennes qui demeurent hermétiques, comme l'écriture rongorongo de l'île de Pâques. Les khipus, ces cordes nouées par les Incas, constituent un autre exemple fascinant d'un système d'encodage dont le secret nous échappe encore.

L'évolution des moyens de communication nous permet aujourd'hui de transmettre des informations sur des distances inimaginables à une vitesse vertigineuse. Par exemple, la transmission d'un signal entre la Terre et Mars, à une distance moyenne d'environ 225 millions de kilomètres, prend environ 12,5 minutes. Cette durée, bien que rapide à l'échelle cosmique, impose des contraintes significatives pour les missions spatiales, obligeant à une planification méticuleuse et à une anticipation des échanges. Un autre exemple marquant est la communication avec la sonde Voyager 1, située actuellement à plus de 23 milliards de kilomètres de la Terre. Les signaux radio, voyageant à la vitesse de la lumière, mettent plus de 21 heures pour atteindre notre planète, illustrant les défis de la transmission à travers les vastes étendues de l'espace.

En ce qui concerne la quantité d'informations, l'expérience internationale de mesure utilisant des radiotélescopes, telle que l'observation des trous noirs via l'Event Horizon Telescope (EHT), a généré des volumes de données si immenses qu'il a été plus rapide de transporter les disques durs contenant des pétaoctets d'informations par avion que de les transmettre via les réseaux de communication. Cette réalité témoigne des limites actuelles des infrastructures de télécommunication face à l'immensité des données générées par les sciences modernes.

Ainsi, la transmission de l'information est un enjeu majeur, non seulement dans sa capacité à franchir les distances, mais aussi dans son aptitude à préserver et à interpréter les données codées, que ce soit à travers le temps ou l'espace.

Voici une version révisée de votre chapitre en tenant compte des informations correctes concernant le projet en Arctique :

## Pérennité de l'information

La pérennité de l'information représente un défi tout aussi crucial que sa transmission. En effet, les supports physiques sur lesquels nous conservons nos données sont souvent fragiles et périssables. Le papier, qui a servi de base à la transmission du savoir pendant des siècles, s'use et se dégrade au fil du temps, même lorsqu'il est conservé dans des conditions optimales. Les bandes magnétiques, autrefois utilisées pour stocker de grandes quantités de données numériques, ont une durée de vie limitée, avec une détérioration progressive de l'information qu'elles contiennent. De même, les CD et les DVD, longtemps perçus comme des solutions de stockage robustes, ont montré leurs limites : leur surface peut se corroder, entraînant une perte irrémédiable des données.

Consciente de ces limitations, l'humanité a entrepris de consolider ses connaissances en les stockant dans des endroits spécialement conçus pour résister à l'épreuve du temps. Un des projets les plus ambitieux en la matière est l'[Arctic World Archive (AWA)](https://en.wikipedia.org/wiki/Arctic_World_Archive), situé dans l'archipel de Svalbard, en Norvège, à proximité du **Global Seed Vault**. L'Arctic World Archive, ouvert en 2017, est une installation sécurisée dans une ancienne mine de charbon, enfouie sous des centaines de mètres de pergélisol. Ce projet vise à préserver les données numériques pour des siècles, voire des millénaires, en utilisant une technologie de stockage sur **PiqlFilm**, un film photosensible spécialement conçu pour garantir la durabilité des informations sans nécessiter d'électricité ou de maintenance continue.

Des institutions du monde entier, telles que les Archives nationales du Brésil, l'Agence spatiale européenne (ESA) et même GitHub, y ont déjà déposé des données importantes. Par exemple, GitHub a archivé 21 téraoctets de données provenant de l'ensemble des dépôts publics actifs de la plateforme, garantissant ainsi la pérennité de précieuses ressources en code source pour les générations futures (voir [GitHub Archive Program](https://archiveprogram.github.com/)).

Ainsi, Svalbard, avec l'Arctic World Archive, s'affirme comme un bastion de la conservation des connaissances numériques, soulignant l'importance de la préservation des données dans un monde où la technologie évolue rapidement, mais où la fiabilité des supports de stockage demeure un enjeu majeur.