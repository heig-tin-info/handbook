---
epigraph:
    quote: "Well-typed programs don’t go wrong."
    source: Robin Milner
---
# Types de données

Inhérent au fonctionnement interne d’un ordinateur, un langage de programmation opère à un certain degré d’abstraction par rapport au mode de stockage des données dans la mémoire. De la même façon qu’il est impossible, dans la vie quotidienne, de rendre la monnaie à une fraction de centime près, un ordinateur ne peut enregistrer des informations numériques avec une précision infinie. Ce principe est intrinsèque aux limites matérielles et au modèle mathématique des nombres. [[||type]]

Les langages de programmation se divisent ainsi en deux grandes catégories : ceux que l’on qualifie de **typés**, où le programmeur a la charge explicite de définir la manière dont les données seront stockées, et ceux dits **non typés**, où ce choix est géré implicitement. Chaque approche présente des avantages et des inconvénients. Reprenons l’exemple du rendu de monnaie : s’il était possible d’enregistrer des montants avec une précision supérieure à celle des pièces en circulation, disons à la fraction de centime, cela poserait problème pour qu’un caissier puisse rendre la monnaie correctement. Dans de telles situations, un langage **typé** s’avère plus adapté, car il permet de fixer des bornes pertinentes à la précision des données. C, en ce sens, est un langage fortement typé, ce qui convient particulièrement à la manipulation rigoureuse des données financières, entre autres.

Il convient de noter que les types de données ne se limitent pas aux seules informations numériques. On trouve des types plus élaborés, capables de représenter des caractères individuels comme `A` ou `B`, ou même des structures plus complexes. Ce chapitre a pour vocation de familiariser le lecteur avec les différents types de données disponibles en C et leur utilisation optimale.

!!! note "Standard ISO 80000-2"

    Les ingénieurs ont une prédilection marquée pour les standards, et cela d'autant plus lorsqu’ils sont de portée internationale. Pour prévenir des erreurs aussi regrettables que le crash d'une fusée dû à une incompréhension entre deux ingénieurs de nations différentes, il existe des normes telles que l'[[ISO 80000-2]], qui définit avec rigueur ce que l'on entend par un entier (incluant ou non le zéro), la nature des nombres réels, et bien d'autres concepts mathématiques fondamentaux. Il va sans dire que les compilateurs, lorsqu’ils sont correctement conçus, s'efforcent de respecter ces normes internationales au plus près. Et vous, en tant que développeur, faites-vous de même ?

## Stockage et interprétation

Ancrez-vous ça bien dans la cabosse : un ordinateur ne peut stocker l'information que sous forme binaire et il ne peut manipuler ces informations que par paquets d'octets.

Un ordinateur 64-bits manipulera avec aisance des paquets de 64-bits, mais plus difficilement des paquets de 32-bits. Un microcontrôleur 8-bit devra quant à lui faire plusieurs manipulations pour lire une donnée 32-bits. Il est donc important par souci d'efficacité d'utiliser la taille appropriée à la quantité d'information que l'on souhaite stocker.

Quant à la représentation, considérons le paquet de 32-bit suivant, êtes-vous à même d'en donner une signification?

```text
01000000 01001001 00001111 11011011
```

Il y a une infinité d'interprétations possibles, mais voici quelques pistes les plus probables:

1. 4 caractères de 8-bits : `01000000` `@`, `01001001` `I`, `00001111` `\x0f` et `11011011` `Û`.
2. 4 nombres de 8-bits: `64`, `73`, `15`, `219`.
3. Deux nombres de 16-bits `18752` et `56079`.
4. Un seul nombre de 32-bit `3675212096`.
5. Peut-être le nombre `-40331460896358400.000000` lu en *little endian*.
6. Ou encore `3.141592` lu en *big endian*.

Qu'en pensez-vous ?

Lorsque l'on souhaite programmer à bas niveau, vous voyez que la notion de type de donnée est essentielle, car en dehors d'une interprétation subjective: "c'est forcément PI la bonne réponse", rien ne permet à l'ordinateur d'interpréter convenablement l'information enregistrée en mémoire. Le typage permet de résoudre toute ambiguïté.

À titre d'exemple, le programme suivant reprend notre question précédente et affiche les différentes interprétations possibles selon différents types de données du langage C. Vous n'avez pas encore vu tous les éléments pour comprendre ce programme, mais vous pouvez déjà en deviner le sens et surtout vous pouvez déjà essayer de l'exécuter pour voir si vos hypothèses étaient correctes.

```c
int main() {
    union {
        uint8_t u8[4];
        uint16_t u16[2];
        uint32_t u32;
        float f32;
    } u = { 0b01000000, 0b01001001, 0b00001111, 0b11011011 };

    printf("'%c', '%c', '%c', '%c'\n", u.u8[0], u.u8[1], u.u8[2], u.u8[3]);
    printf("%hhu, %hhu, %hhu, %hhu\n", u.u8[0], u.u8[1], u.u8[2], u.u8[3]);
    printf("%hu, %hu\n", u.u16[0], u.u16[1]);
    printf("%u\n", u.u32);
    printf("%f\n", u.f32);
    u.u32 = (
        ((u.u32 >> 24) & 0xff) | // move byte 3 to byte 0
        ((u.u32 << 8) & 0xff0000) | // move byte 1 to byte 2
        ((u.u32 >> 8) & 0xff00) | // move byte 2 to byte 1
        ((u.u32 << 24) & 0xff000000) // byte 0 to byte 3
    );
    printf("%f\n", u.f32);
}
```

[]{#endianess}

## Boutisme

![Boutisme par J. J. Grandville (1838)](/assets/images/endian.jpg){width=70%}

La hantise de l’ingénieur bas-niveau, c’est le concept de **boutisme**, ou *endianess* en anglais. Ce terme, popularisé par l’informaticien Danny Cohen, fait référence au livre *Les Voyages de Gulliver* de Jonathan Swift. Dans cette satire, les habitants de Lilliput se divisent en deux factions : ceux qui mangent leurs œufs à la coque en commençant par le petit bout (les *Little Endians*) et ceux qui préfèrent le gros bout (les *Big Endians*), engendrant un conflit absurde. [[||endianess]] [[||Gulliver, les voyages de]] [[||boutisme]]

En informatique, cette question, loin d’être triviale, persiste dans le monde des microprocesseurs. Certains fonctionnent en **big endian**, où les octets sont stockés en mémoire du plus significatif au moins significatif, tandis que d'autres adoptent le format **little endian**, inversant cet ordre. Imaginons qu’une donnée soit enregistrée en mémoire ainsi :

```text
[0x40, 0x49, 0x0F, 0xDB]
```

Doit-on lire ces octets de gauche à droite (comme en *big endian*) ou de droite à gauche (comme en *little endian*) ? Ce problème, bien qu’il semble anodin, devient crucial dans des contextes internationaux. Si ce texte était écrit en arabe, une langue lue de droite à gauche, votre perception pourrait être différente.

Prenons un exemple plus concret. Un microcontrôleur *big endian* 8 bits envoie via Bluetooth la valeur `1'111'704'645` – représentant, par exemple, le nombre de photons détectés par un capteur optique. Il transmet les octets suivants : `0x42, 0x43, 0x44, 0x45`. Cependant, l’ordinateur qui reçoit ces données en mode *little endian* interprète cette séquence comme `1'162'101'570`. Ce décalage dans la lecture est un problème courant auquel les ingénieurs en électronique se heurtent fréquemment dans leur carrière.

Le **boutisme** intervient donc dans la manière de stocker et transmettre des données, chaque approche ayant ses avantages et inconvénients. Personnellement, en matière d’œufs, je préfère le *gros boutisme* : je trouve qu’il est plus pratique de manger un œuf à la coque en le commençant par le gros bout. En informatique, cependant, les arguments des deux camps se valent, et les choix dépendent souvent des exigences du système.

Pour mieux illustrer ce concept, prenons un exemple en base 10, plus accessible. Imaginez que je doive transmettre un nombre, comme `532`, par un tuyau dans lequel une seule boule peut passer à la fois, chaque boule représentant un chiffre. Dois-je envoyer la boule marquée `5`, puis `3`, puis `2` ? Ou devrais-je commencer par la boule marquée `2` et terminer par celle portant le `5` ? Dans notre culture, nous lisons de gauche à droite, mais lorsque les données sont stockées dans un nombre fixe de bits, comme c’est le cas en informatique, les deux méthodes se justifient.

Par exemple, si je vous transmets le nombre `7` et vous dis qu'il est inférieur à 10, en *big endian*, vous devrez attendre deux boules supplémentaires (0, 0, 7), tandis qu’en *little endian*, vous saurez immédiatement que c'est `7` (7, 0, 0). C’est cette raison de simplicité dans la gestion des petites valeurs qui a largement contribué à la popularité du *little endian* dans les systèmes modernes.

Techniquement parlant, voici la représentation en mémoire de trois entiers 32 bits :

```text
16909060, 42, 10000
01 02 03 04  00 00 00 2a  00 00 27 10 (big endian)
04 03 02 01  2a 00 00 00  10 27 00 00 (little endian)
```

Ainsi, le **boutisme** n'est pas qu'un détail technique : c'est une question cruciale pour l'interopérabilité des systèmes numériques.

!!! warning "Organisation par type"

    Selon le boutisme, ce n'est pas toute l'information qui est inversée, mais l'ordre des octets au sein de chaque nombre.

!!! note "Réseau informatique"

    Le réseau informatique comme les protocoles TCP/IP, UDP, Wi-Fi utilisent le *network byte order* qui impose le *big endian* pour l'envoi des données. Cela remonte aux premières normes dont l'idée était d'adopter une convention unique et standardisée à une époque ou les ordinateurs *big endian* étaient majoritaires. Or aujourd'hui la très vaste majorité des ordinateurs sont en *little endian* et donc les données transmises et réceptionnées doivent être converties. C'est le rôle de la fonction `htonl` (*host to network long*) qui convertit un entier 32 bits en *big endian* ou `ntohl` (*network to host long*) qui fait l'opération inverse.

    Pour vous lecteurs, cela n'a pas de grande importance, car nous n'allons pas approfondir le fonctionnement du réseau informatique dans cet ouvrage.

## Les nombres entiers

Les **nombres entiers** que nous avons définis plus tôt peuvent être négatifs, nuls ou positifs. En C, il existe plusieurs types de données pour les représenter, chacun ayant ses propres caractéristiques.

### Les entiers naturels

En informatique, les entiers naturels de l'ensemble $\mathbb{N}$ sont **non signés**, et peuvent prendre des valeurs comprises entre $0$ et $2^N-1$ où $N$ correspond au nombre de bits avec lesquels la valeur numérique sera stockée en mémoire. Il faut naturellement que l'ordinateur sur lequel s'exécute le programme soit capable de supporter le nombre de bits demandé par le programmeur. En C, on nomme ce type de donnée `unsigned int`, `int` étant le dénominatif du latin *integer* signifiant "entier".

Voici quelques exemples des valeurs minimales et maximales possibles selon le nombre de bits utilisés pour coder l'information numérique :

Table: Stockage d'un entier non signé sur différentes profondeurs

| Profondeur | Minimum | Maximum                                   |
| ---------- | ------- | ----------------------------------------- |
| 8 bits     | 0       | 255 ($2^8 - 1$)                           |
| 16 bits    | 0       | 65'535 ($2^{16} - 1$)                     |
| 32 bits    | 0       | 4'294'967'295 ($2^{32} - 1$)              |
| 64 bits    | 0       | 18'446'744'073'709'551'616 ($2^{64} - 1$) |

Notez l'importance du $-1$ dans la définition du maximum, car la valeur minimum $0$ fait partie de l'information même si elle représente une quantité nulle. Il y a donc 256 valeurs possibles pour un nombre entier non signé 8-bits, bien que la valeur maximale ne soit que de 255.

### Les entiers bornés signés

Les entiers signés peuvent être **négatifs**, **nuls** ou **positifs** et peuvent prendre des valeurs comprises entre $-2^{N-1}$ et $+2^{N-1}-1$ où $N$ correspond au nombre de bits avec lesquels la valeur numérique sera stockée en mémoire. Notez l'asymétrie entre la borne positive et négative.

Comme ils sont signés (*signed* en anglais), il est par conséquent correct d'écrire `signed int` bien que le préfixe `signed` soit optionnel, car le standard définit qu'un entier est par défaut signé. La raison à cela relève plus du lourd historique de C qu'à des préceptes logiques et rationnels.

Voici quelques exemples de valeurs minimales et maximales selon le nombre de bits utilisés pour coder l'information :

Table: Stockage d'un entier signé sur différentes profondeurs

| Profondeur | Minimum                    | Maximum                    |
| ---------- | -------------------------- | -------------------------- |
| 8 bits     | -128                       | +127                       |
| 16 bits    | -32'768                    | +32'767                    |
| 32 bits    | -2'147'483'648             | +2'147'483'647             |
| 64 bits    | -9'223'372'036'854'775'808 | +9'223'372'036'854'775'807 |

En mémoire, ces nombres sont stockés en utilisant le [complément à deux][twos_complement] que nous avons déjà évoqué.

### Les entiers bornés

Comme nous l'avons vu, les degrés de liberté pour définir un entier sont :

- Signé ou non signé
- Nombre de bits avec lesquels l'information est stockée en mémoire

À l'origine le standard C restait flou quant au nombre de bits utilisés pour chacun des types et aucune réelle cohérence n'existait pour la construction d'un type. Le modificateur `signed` était optionnel, le préfixe `long` ne pouvait s'appliquer qu'au type `int` et `long` et la confusion entre `long` (préfixe) et `long` (type) restait possible. En fait, la plupart des développeurs s'y perdaient et s'y perd toujours ce qui menait à des problèmes de compatibilités des programmes entre eux.

#### Types standards

La construction d'un type entier C peut être résumée par la figure suivante :

![Entiers standardisés](/assets/images/ansi-integers.drawio)

Le préfixe `signed` est implicite, mais il est possible de l'utiliser pour plus de clarté. En pratique il sera rarement utilisé. De même, lorsque `short`, `long` ou `long long` est utilsé, le suffixe `int` est implicite.

Les types suivants sont donc des synonymes:

```c
// Entier signé
signed int, int, signed

// Entier non signé
unsigned int, unsigned

// Entier court signé
signed short int, short, signed short

// Entier court non signé
unsigned short int, unsigned short

// Entier long signé
signed long int, long, long int, signed long

// Entier très long signé
signed long long int, long long, signed long long
```

En revanche `char` est un type à part entière signé par défaut qui n'aura pas de suffixe `int`, mais il est possible de le déclarer `unsigned char`.

Ci-dessous la table des entiers standards en C. Le format est celui utilisé par la fonction `printf` de la bibliothèque standard C.

Table: Table des types entiers en C

| Type                            | Signe      | Profondeur       | Format |
| ------------------------------- | ---------- | ---------------- | ------ |
| `char`, `signed char`           | *signed*   | au moins 8 bits  | `%c`   |
| `unsigned char`                 | *unsigned* | au moins 8 bits  | `%uc`  |
| `short`, `short int`, ...       | *signed*   | au moins 16 bits | `%hi`  |
| `unsigned short`, ...           | *unsigned* | au moins 16 bits | `%hu`  |
| `unsigned`, `unsigned int`      | *unsigned* | au moins 32 bits | `%u`   |
| `int`, `signed`, `signed int`   | *signed*   | au moins 32 bits | `%d`   |
| `unsigned`, `unsigned int`, ... | *unsigned* | au moins 32 bits | `%u`   |
| `long`, `long int`, ...         | *signed*   | au moins 32 bits | `%li`  |
| `unsigned long`, ..             | *unsigned* | au moins 32 bits | `%lu`  |
| `long long`, ...                | *signed*   | au moins 64 bits | `%lli` |
| `unsigned long long`, ...       | *unsigned* | au moins 64 bits | `%llu` |

Avec l'avènement de **C99**, une meilleure cohésion des types a été proposée dans le fichier d'en-tête `stdint.h`. Cette bibliothèque standard offre les types suivants :

![Flux de construction d'un entier standardisé](/assets/images/c99-integers.drawio)

[]{#reformed-types}

### Nouveaux types standard

Avec l'avènement de **C99**, une meilleure cohésion des types a été proposée dans le fichier d'en-tête `stdint.h`. Cette bibliothèque standard offre les types suivants. Comme nous l'avons vu, la taille des types historiques n'est pas précisément définie par le standard. On sait qu'un `int` contient **au moins** 16-bits, mais il peut, selon l'architecture, et aussi le modèle de donnée, prendre n'importe quelle valeur supérieure. Ceci pose des problèmes de portabilité possibles si le développeur n'est pas suffisamment consciencieux et qu'il ne s'appuie pas sur une batterie de tests automatisés. En conséquence, il est recommandé d'utiliser les types de `<stdint.h>` lorsque la taille du type doit être garantie.

Attention cependant à noter que garantir un type à taille fixe n'est pas toujours la meilleure solution. En effet, si vous avez besoin d'un entier de 32-bits, il est préférable d'utiliser `int` qui sera adapté à l'architecture matérielle. Si vous utilisez `int32_t` vous risquez de perdre en performance si l'architecture matérielle est capable de traiter des entiers 64-bits de manière plus efficace. Voici les types à taille fixe de `<stdint.h>` :

Table: Entiers standard défini par stdint

| Type       | Signe    | Profondeur | Format |
| ---------- | -------- | ---------- | ------ |
| `uint8_t`  | unsigned | 8 bits     | `%c`   |
| `int8_t`   | signed   | 8 bits     | `%c`   |
| `uint16_t` | unsigned | 16 bits    | `%hu`  |
| `int16_t`  | signed   | 16 bits    | `%hi`  |
| `uint32_t` | unsigned | 32 bits    | `%u`   |
| `int32_t`  | signed   | 32 bits    | `%d`   |
| `uint64_t` | unsigned | 64 bits    | `%llu` |
| `int64_t`  | signed   | 64 bits    | `%lli` |

À ces types s'ajoutent les types **rapides** (*fast*) et **minimums** (*least*). Un type nommé `uint_least32_t` garanti l'utilisation du type de donnée utilisant le moins de mémoire et garantissant une profondeur d'au minimum 32 bits. Les types rapides, moins utilisés, vont automatiquement choisir le type adapté le plus rapide à l'exécution. Par exemple, si l'architecture matérielle permet un calcul natif sur 48-bits, elle sera privilégiée par rapport au type 32-bits.

!!! exercise "Débordement"

    Quel sera le contenu de `j` après l'exécution de l'instruction suivante :

    ```c
    uint16_t j = 1024 * 64;
    ```

    - [ ] 0
    - [x] 1
    - [ ] 64
    - [ ] 1024
    - [ ] 65536

[]{#datamodel}

## Modèle de donnée

Comme nous l'avons évoqué plus haut, la taille des entiers `short`, `int`, ... n'est pas précisément définie par le standard. On sait qu'un `int` contient **au moins** 16-bits, mais il peut, selon l'architecture, et aussi le modèle de donnée, prendre n'importe quelle valeur supérieure.

Admettons que ce développeur sans scrupule développe un programme complexe sur sa machine 64-bits en utilisant un `int` comme valeur de comptage allant au-delà de dix milliards. Après tests, son programme fonctionne sur sa machine, ainsi que celle de son collègue. Mais lorsqu'il livre le programme à son client, le processus crash. En effet, la taille du `int` sur l'ordinateur du client est de 32-bits. Comment peut-on s'affranchir de ce type de problème ?

La première solution est de toujours utiliser les types proposés par `<stdint.h>` lorsque la taille du type nécessaire est supérieure à la valeur garantie. L'autre solution est de se fier au modèle de données. Le modèle de données est une convention qui définit la taille des types de données de base. Il est déterminé par l'architecture matérielle et le système d'exploitation. Voici un tableau résumant les modèles de données les plus courants :

Table: Modèle de données

| Modèle     | short | int | long | long long | size_t | Système d'exploitation                                                      |
| ---------- | ----- | --- | ---- | --------- | ------ | --------------------------------------------------------------------------- |
| **LP32**   | 16    | 16  | 32   |           | 32     | Windows 16-bits, Apple Macintosh                                            |
| **ILP32**  | 16    | 32  | 32   | 64        | 32     | Windows x86, Linux 32-bits                                                  |
| **LLP64**  | 16    | 32  | 32   | 64        | 64     | [Microsoft Windows](https://en.wikipedia.org/wiki/Microsoft_Windows) x86-64 |
| **LP64**   | 16    | 32  | 64   | 64        | 64     | Unix, Linux, macOS                                                          |
| **ILP64**  | 16    | 64  | 64   | 64        | 64     | [HAL](https://en.wikipedia.org/wiki/HAL_Computer_Systems) (SPARC)           |
| **SILP64** | 64    | 64  | 64   | 64        | 64     | [UNICOS](https://en.wikipedia.org/wiki/UNICOS) (Super ordinateur)           |

[[||LP32]] [[||ILP32]] [[||LLP64]] [[||LP64]] [[||ILP64]] [[||SILP64]]

Table: Taille usuelle des types de base

| Type        | Taille                               | Windows | Linux |
| ----------- | ------------------------------------ | ------- | ----- |
| char        | habituellement 8 bits                | 1       | 1     |
| short       | au moins 16 bits                     | 2       | 2     |
| int         | taille naturelle pour l'architecture | 4       | 4     |
| long        | au moins 32 bits                     | 4       | 8     |
| long long   | au moins 64 bits                     | 8       | 8     |
| float       | normalement 32 bits                  | 4       | 4     |
| double      | normalement 64 bits                  | 8       | 8     |
| long double | au moins 63 bits                     | 8       | 16    |

Les troisième et quatrième colonnes représentent la taille des types de base sur des machines modernes 64-bits. On notera que la taille des types `long` et `long double` varie selon l'architecture matérielle et le système d'exploitation. On voit donc que selon le modèle les types n'ont pas la même taille et donc que la portabilité des programmes est un enjeu majeur. Aussi, pour s'assurer qu'un type est de la taille souhaitée, il est recommandé d'utiliser les [nouveaux types standards][reformed-types] de `<stdint.h>`. Ainsi pour s'assurer qu'un type soit **au moins** de 32-bits, on utilisera `uint_least32_t`.

## Les caractères

Les caractères, ceux que vous voyez dans cet ouvrage, sont généralement représentés par des grandeurs exprimées sur 1 octet (8-bits):

```text
97 ≡ 0b1100001 ≡ 'a'
```

Un caractère du clavier enregistré en mémoire c'est donc un nombre entier de 8-bits. En C, le type de donnée `char` est utilisé pour stocker un caractère.

Mais comment un ordinateur sait-il que `97` correspond à `a` ? C'est là que la notion d'encodage entre en jeu.

### La table ASCII

Historiquement, alors que les informations dans un ordinateur ne sont que des 1 et des 0, il a fallu établir une correspondance entre une grandeur binaire et le caractère associé. Chaque constructeur d'ordinateur avait sa propre table de correspondance. On peut naïvement penser qu'il serait simple de faire concorder les lettres `A` à `Z` avec les valeurs 1 à 26, puis de même pour les minuscules, les chiffres et les caractères spéciaux mais pourquoi dans cet ordre ? Et tous ces caractères invisibles comme le retour chariot, le saut de ligne, la tabulation, l'espace, etc. ?

En 1963 l'ASA (*American Standards Association*) aujourd'hui **ANSI** propose un premier standard qui ne définissait alors que 63 caractères imprimables. Comme la mémoire à cette époque était très chère, un caractère n'était codé que sur 7 bits. En effet, l'œuvre de la recherche du temps perdu de Marcel Proust - 7 tomes - pour 3000 pages et quelques 10.45 millions de signes demanderait 9.96 MiB de mémoire de stockage avec 8 bits et seulement contre 8.72 MiB sur 7 bits, soit 12% d'économie : une aubaine !

La première table [[ASCII]] définissant 128 caractères est donnée par la figure suivante : [[||ANSI]]

![Table ASCII ASA X3.4 établie en 1963](/assets/images/ascii-1963.drawio)

En 1986, la table ASCII a été étendue pour couvrir les caractères majuscules et minuscules. Cette réforme est donnée par la figure suivante. Il s'agit de la table ASCII standard actuelle.

![Table ANSI INCITS 4-1986 (standard actuel)](/assets/images/ascii.drawio)

!!! info "Majuscules et Minuscules"

    Notez que dans la table ASCII, les lettres majuscules et minuscules sont séparées par une valeur de 32. Ainsi pour convertir une lettre majuscule en minuscule, il suffit d'ajouter 32 à sa valeur. Par exemple `A` vaut `65` et `a` vaut `97`. Inversement, pour convertir une lettre minuscule en majuscule, il suffit de soustraire 32 à sa valeur. La valeur 65 peut s'exprimer comme $2^6 + 1$ et la valeur 97 comme $2^6 + 2^5 + 1$. Ainsi, en utilisant les décalages de bits, on peut écrire :

    ```c
    printf("a = %c", 1<<6 + 1);        // Affiche a
    printf("A = %c", 1<<6 + 1<<5 + 1); // Affiche A
    ```

    Pour convertir une valeur majuscule en minuscule, il suffit d'activer le 5ème bit (en comptant à partir de 0) :

    ```c
    char letter = 'p';
    letter |= 1 << 5; // active le cinquième bit
    printf("%c\n", letter); // Affiche P
    ```

Ainsi qu'évoqué plusieurs fois dans cet ouvrage, chaque pays et chaque langue utilise ses propres caractères et il a fallu trouver un moyen de satisfaire tout le monde. Il a été alors convenu d'encoder les caractères sur 8-bits au lieu de 7 et de profiter des 128 nouvelles positions offertes pour ajouter les caractères manquants telles que les caractères accentués, le signe euro, la livre sterling et d'autres. Le standard **ISO/IEC 8859** aussi appelé standard *Latin* définit 16 tables d'extension selon les besoins des pays. Les plus courantes en Europe occidentale sont les tables **ISO-8859-1** ou (**latin1**) et **ISO-8859-15** (**latin9**). Voici la table d'extension de l'[[ISO-8859-1]] et de l'[[ISO-8859-15]] :

![Table d'extension ISO-8859-1 (haut) et ISO-8859-15 (bas)](/assets/images/latin1.drawio)

Ce standard a généré durant des décennies de grandes frustrations et de profondes incompréhensions chez les développeurs et utilisateurs d'ordinateur. Ne vous est-il jamais arrivé d'ouvrir un fichier texte et de ne plus voir les accents convenablement ? C'est un problème typique d'encodage.

Pour tenter de remédier à ce standard incompatible entre les pays, Microsoft a proposé un standard nommé [Windows-1252](https://fr.wikipedia.org/wiki/Windows-1252) s'inspirant de [ISO-8859-1](https://fr.wikipedia.org/wiki/ISO/CEI_8859-1). En voulant rassembler en proposant un standard plus général, Microsoft n'a contribué qu'à proposer un standard supplémentaire venant s'inscrire dans une liste déjà trop longue. Et l'histoire n'est pas terminée...

C'est pourquoi, en 1991, l'**ISO** a proposé un standard universel nommé **Unicode** qui est capable d'encoder tous les caractères de toutes les langues du monde.

[]{#encodingunicode}

### Unicode

Avec l'arrivée d'internet et les échanges entre les Arabes (عَرَب), les Coréens (한국어), les Japonais qui possèdent deux alphabets ainsi que des caractères chinois (日本語), sans oublier l'ourdou (پاکِستان) pakistanais et tous ceux que l'on ne mentionnera pas, il a fallu bien plus que 256 caractères et quelques tables de correspondance. Ce présent ouvrage, ne pourrait d'ailleurs par être écrit sans avoir pu résoudre, au préalable, ces problèmes d'encodage; la preuve étant, vous parvenez à voir ces caractères qui ne vous sont pas familiers.

Un fabuleux consensus planétaire a été atteint en 2008 avec l'adoption majoritaire du standard **Unicode** (*Universal Coded Character Set*) et son encodage **UTF-8** (*Unicode Transformation Format*). Ce standard est capable d'encoder tous les caractères de toutes les langues du monde. Il est utilisé par la plupart des systèmes d'exploitation, des navigateurs web et des applications informatiques. Il est capable d'encoder 1'112'064 caractères en utilisant de 1 à 4 octets. La figure suivante montre la tendance de l'adoption de 2001 à 2012. Cette tendance est accessible [ici](https://googleblog.blogspot.com/2012/02/unicode-over-60-percent-of-web.html).

Figure: Tendances sur l'encodage des pages web en faveur de UTF-8 dès 2001, données collectées par Google et Erik van der Poel

![Utiliation de l'UTF-8 dès 2001](/assets/images/unicode-trends.drawio)

[Ken Thompson](https://fr.wikipedia.org/wiki/Ken_Thompson), dont nous avons déjà parlé en introduction, []{#thompson} est à l'origine de ce standard. Par exemple le *devanagari* caractère `ह` utilisé en Sanskrit possède la dénomination Unicode U+0939 et s'encode sur 3 octets: `0xE0 0xA4 0xB9`

En programmation C, un caractère `char` ne peut exprimer sans ambigüité que les 128 caractères de la table ASCII standard et selon les conventions locales, les 128 caractères d'extension. C'est-à-dire que vous ne pouvez pas exprimer un caractère Unicode en utilisant un `char`. Pour cela, il faudra utiliser un tableau de caractères `char` ou un tableau de caractères `wchar_t` qui est capable de stocker un caractère Unicode, mais nous verrons cela plus tard. [[||wchar]] [[||unicode]] [[||utf8]] [[||Ken Thompson]]

Ce nouveau standard devait résoudre de nombreux problème techniques. Le premier étant la rétro-compatibilité avec l'ASCII. La première excellente idée fut de calquer les 128 premiers caractères Unicode à la table ASCII. Ainsi, un texte ASCII est aussi un texte Unicode. Rappelez-vous la première table n'utilisant que 7 bits, le huitième bit était toujours à 0, et ce fut une idée brillante de s'approprier ce huitième bit pour définir des caractères supplémentaires. Mais comment faire pour caser les 1'112'064 caractères dans seulement 128 valeurs supplémentaires ?

Unicode définit plusieurs encodages dont les plus courants sont **UTF-8**, **UTF-16** et **UTF-32**. Le plus utilisé, et de loin est **UTF-8** qui est un encodage à **longueur variable**. Le premier octet, s'il ne s'agit pas d'un caractère ASCII (0xxxxxxx), indique le nombre d'octets utilisés pour encoder le caractère. Par exemple, si le premier octet commence par `110xxxxx`, cela signifie que le caractère est encodé sur 2 octets. Si le premier octet commence par `1110xxxx`, cela signifie que le caractère est encodé sur 3 octets. Si le premier octet commence par `11110xxx`, cela signifie que le caractère est encodé sur 4 octets. Les bits `x` sont utilisés pour coder la valeur du caractère.

Figure: Table de correspondance du nombre d'octets d'une séquence UTF-8 selon le premier octet

![Nombre d'octets en UTF-8](/assets/images/unicode-table.drawio)

Table: Longueur des séquences Unicode

| Longueur | Octet 1  | Octets suivants                              | Plage Unicode      |
| -------- | -------- | -------------------------------------------- | ------------------ |
| 1        | 0xxxxxxx |                                              | U+0000 à U+007F    |
| 2        | 110xxxxx | 10xxxxxx                                     | U+0080 à U+07FF    |
| 3        | 1110xxxx | 10xxxxxx 10xxxxxx                            | U+0800 à U+FFFF    |
| 4        | 11110xxx | 10xxxxxx 10xxxxxx 10xxxxxx                   | U+10000 à U+10FFFF |
| 5        | 111110xx | 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx          | Non utilisé        |
| 6        | 1111110x | 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx | Non utilisé        |

Originellement quant il a été inventé par Ken Thompson et Rob Pike en 1992, l'encodage UTF-8 pouvait utiliser jusqu'à 6 octets pour encoder un caractère. Mais comme le standard Unicode n'utilise que les plages U+0000 à U+10FFFF, les séquences de 5 et 6 octets ne sont plus utilisées.

Il est intéressant de constater que les séquence débutant par `0xC0xx` ou `0xC1xx` ne sont pas valides car elles permetteraient de représenter des caractères ASCII en utilisant 2 octets. De même, les séquences débutant par `0xF5xx` à `0xF7xx` ne sont pas valides car elles permettraient de représenter des caractères au-delà de U+10FFFF.

Il existe en effet une règle stricte d'encodage qui interdit les séquences surlongues (*overlong encoding*), c'est-à-dire l'utilisation de plusieurs octets pour encoder un caractère qui pourrait être représenté avec moins d'octets. Par exemple, le caractère ASCII `A` (U+0041) doit être encodé en UTF-8 avec un seul octet `0x41` et non pas avec deux octets `0xC1 0x81`. Voici l'exemple illustré :

```text
A        01   00 0001  (0x41 en ASCII)
  110x xxxx 10xx xxxx  (2 octets)
  1100 0001 1000 0001  (C1 81 en UTF-8)  <- Overlong encoding (interdit)
```

C'est pour cette raison que parfois si un texte écrit en Latin1 est ouvert en UTF-8, des caractères inconnus peuvent apparaître (�) car ces séquences sont invalides.

Notons que l'encodage à décidé de réserver deux bits pour les séquences suivantes. D'une part le huitième bit de chaque octet suivi d'un `0` (`10xxxxxx`). L'intérêt est de pouvoir immédiatement reconnaître toute séquence UTF-8, mais surtout de faciliter la recherche de la fin d'une séquence. En effet, si l'on rencontre un octet commençant par `0` ou `11`, on sait que l'on est au début d'une nouvelle séquence.

Parlons de diacritiques (accents). En Unicode, un caractère accentué peut être représenté de deux manières différentes. Soit par un caractère unique, soit par une combinaison d'un caractère de base et d'un ou plusieurs caractères diacritiques. Par exemple, le caractère `é` peut être représenté par le code Unicode U+00E9 (caractère composé) ou par la combinaison du caractère `e` (U+0065) suivi du caractère diacritique `´` (U+0301), forme décomposée. Cette flexibilité permet de représenter des caractères accentués de manière plus cohérente, mais elle peut aussi poser des problèmes lors de la comparaison de chaînes de caractères. Pour ce faire il existe des algorithmes de normalisation Unicode qui permettent de convertir les chaînes de caractères en une forme standardisée comme la forme NFC (Normalization Form C), NFD (Normalization Form D), NFKC (Normalization Form KC) et NFKD (Normalization Form KD).

NFC

:   Composée : les caractères sont combinés en un seul caractère lorsqu'une telle combinaison existe.

NFD

:   Décomposée : les caractères sont séparés en leurs composants de base.

NFKC

:   Composée compatible : similaire à NFC, mais applique des transformations de compatibilité.

NFKD

:   Décomposée compatible : similaire à NFD, mais applique des transformations de compatibilité.

Cette superposition possible de caractère est très utile pour les langues comme le coréen qui utilise le mécanisme des superpositions pour former les syllabes. Par exemple, la syllabe 한 (han) peut être décomposée en trois caractères Unicode : ㅎ en haut à gauche (U+1112), ㅏ à droite (U+1161) et ㄴ en bas (U+11AB). Elle s'écrira donc en UTF-8 avec la séquence d'octets suivante :

```text
E1 84 92  E1 85 A1  E1 86 AB
```

Notons que c'est La forme composée (NFC) de 한 est U+D55C qui utilisée dans la plupart des textes coréens. La forme décomposée (NFD) U+1112 U+1161 U+11AB est quant à elle rarement utilisée.

C'est au travail des moteurs de rendus comme [HarfBuzz](https://harfbuzz.github.io/) ou [Uniscribe](https://learn.microsoft.com/en-us/windows/win32/intl/uniscribe) que nous devons la capacité d'afficher correctement ces caractères complexes.

Le problème principal d'unicode est la navigation et le calcul de la longueur d'une chaîne de caractères. En effet, un texte encodé en ASCII ou en Latin1 peut être parcouru octet par octet. Un texte de 1000 signes occupe 1000 octets et il est possible d'accéder directement au 500ème caractère en se déplaçant de 500 octets depuis le début du texte `text[500]`. En UTF-8, un texte de 1000 signes peut occuper entre 1000 et 4000 octets. Il est donc impossible d'accéder directement au 500ème caractère sans parcourir la chaîne depuis le début et en comptant les caractères rencontrés. Les éditeurs qui permettent de naviguer rapidement dans un texte utilisent des index pour accélérer la recherche. Une approche alternative est d'encoder les textes en UTF-32 où chaque caractère est codé sur 4 octets.

En C moderne (C20 ou C23), il est possible d'écrire des chaînes de caractères Unicode en utilisant le préfixe `u8` pour UTF-8, `u` pour UTF-16 et `U` pour UTF-32. Par exemple :

```c
char *utf8_string = u8"Bonjour, 世界"; // Chaîne UTF-8
char16_t *utf16_string = u"Bonjour, 世界"; // Chaîne UTF-16
char32_t *utf32_string = U"Bonjour, 世界"; // Chaîne UTF-32
```

Le calcul de la longueur d'une chaîne de caractères peut être effectué en utilisant la fonction `strlen` pour les chaînes UTF-8, mais pour les chaînes UTF-16 et UTF-32, il est nécessaire d'utiliser des fonctions spécifiques comme `u16_strlen` et `u32_strlen` respectivement.

### Les emojis

Les [[emojis]] sont des caractères spéciaux qui ont été introduits en 2010 par le standard Unicode 6.0. Ils sont donc codés sur 4 octets et permettent de représenter des émotions, des objets, des animaux, des symboles ou des étrons (💩).

Les émoticônes que vous pouvez envoyer à votre grand-mère via WhatsApp sont donc des caractères Unicode et non des images. Si vous dites à votre grand-maman que vous l'aimez en lui envoyant un cœur, elle recevra le caractère U+2764 qui est le caractère `❤`. Mais les navigateurs web et les applications informatiques remplacent à la volée ces caractères par des images.

Ceci est vrai, mais encore faut-il que la police d'écriture utilisée par votre chère grand-maman soit capable d'afficher ce caractère. Si ce n'est pas le cas, elle verra probablement le caractère � qui est un caractère de remplacement très disgracieux et qui ne démontre pas tout l'amour que vous lui portez.

### Les boxchars

Les **boxchars** sont des caractères spéciaux utilisés pour dessiner des boîtes, des cadres et des lignes dans les interfaces en mode texte. Ils font partie de la table ASCII étendue et sont souvent utilisés dans les applications en ligne de commande pour améliorer l'apparence visuelle :

```text
┌───────────────┐
│   Boxchars    │
├───────────────┤
│ ─ │ │ ┌ ┐ └ ┘ │
│ ├ ┤ ┬ ┴ ┼     │
└───────────────┘
```

Avec Unicode, il existe une vaste gamme de boxchars qui permettent de créer des interfaces utilisateur plus complexes et esthétiques. Voici quelques exemples courants de boxchars Unicode :

```text
U+2500 ─  (ligne horizontale)
U+2502 │  (ligne verticale)
U+250C ┌  (coin supérieur gauche)
U+2510 ┐  (coin supérieur droit)
U+2514 └  (coin inférieur gauche)
U+2518 ┘  (coin inférieur droit)
U+251C ├  (jonction gauche)
U+2524 ┤  (jonction droite)
U+252C ┬  (jonction haut)
U+2534 ┴  (jonction bas)
U+253C ┼  (jonction croisée)
```

## Chaîne de caractères

Une **chaîne de caractères** est simplement la suite contiguë de plusieurs caractères dans une zone mémoire donnée. Afin de savoir lorsque cette chaîne se termine, le standard impose que le dernier caractère d'une chaîne soit `NUL` ou `\0`. On appelle ce caractère le caractère de fin de chaîne. Il s'agit d'une [[sentinelle]].

!!! example "Les légumes et les choux"

    Imaginez que l'on vous demande de vous placer dans un champ et de déterrer n'importe quel légume sauf un chou. Votre algorithme est :

    ```mermaid
    %% Algorithme de déterrage de légumes
    flowchart LR
        start(Début) --> pick[Déterrer]
        pick --> if{Choux?}
        if --Non--> step[Avancer de 1 pas]
        step --> pick
        if --Oui--> stop(Fin)
    ```

    Si vous trouvez un chou, vous savez que vous êtes arrivés au bout du champ. Le chou fait office de sentinelle.

    Sans sentinelle, vous êtes obligé de connaître à l'avance le nombre de pas à faire pour arriver au bout du champ. Vous devez donc stocker en mémoire cette information additionnelle ce qui n'est pas pratique.

La chaîne de caractère `Hello` sera en mémoire stockée en utilisant les codes ASCII suivants.

```c
char string[] = "Hello";
```

```
  H   E   L   L   O  \0
┌───┬───┬───┬───┬───┬───┐
│ 72│101│108│108│111│ 0 │
└───┴───┴───┴───┴───┴───┘

 0x00  0b01001000
 0x01  0b01100101
 0x02  0b01101100
 0x03  0b01101100
 0x04  0b01101111
 0x05  0b00000000
```

On utilise le caractère nul `\0` pour plusieurs raisons:

1. Il est facilement reconnaissable.
2. Dans un test il vaut `false`.
3. Il n'est pas imprimable.

!!! warning

    Ne pas confondre le caractère nul `\0` avec le caractère `0`. Le premier est un caractère de fin de chaîne, le second est un caractère numérique qui vaut `0x30`. Le caractère nul est la valeur `0` selon la table ASCII.

## Booléens

Un [booléen](https://fr.wikipedia.org/wiki/Bool%C3%A9en) est un type de donnée à deux états consensuellement nommés *vrai* (`true`) et *faux* (`false`) et destinés à représenter les états en logique booléenne (Nom venant de [George Boole,](https://fr.wikipedia.org/wiki/George_Boole) fondateur de l'algèbre éponyme). [[||booléen]] [[||George Boole]] [[||Boole, George]] [[||true]] [[||false]]

La convention est d'utiliser `1` pour mémoriser un état vrai, et `0` pour un état faux, c'est d'ailleurs de cette manière que les booléens sont encodés en C.

Les **booléens** ont été introduits formellement en C avec **C99** et nécessitent l'inclusion du fichier d'en-tête `<stdbool.h>`. Avant cela le type booléen était `_Bool` et définir les états vrais et faux était à la charge du développeur. [[||<stdbool.h>]]

```c
#include <stdbool.h>

bool is_enabled = false;
bool has_tail = true;
```

Afin de faciliter la lecture du code, il est courant de préfixer les variables booléennes avec les préfixes `is_` ou `has_`. À titre d'exemple, si l'on souhaite stocker le genre d'un individu (mâle, ou femelle), on pourrait utiliser la variable `is_male`.

Bien qu'un booléen puisse être stocké sur un seul bit, en pratique, il est stocké sur un octet, voire même sur un mot de 32 ou 64 bits. Cela est dû à la manière dont les processeurs manipulent les données en mémoire. Sur une architecture LP64, un booléen sera stocké sur 8 octets. Les valeurs `true` et `false` vaudront donc :

```
00 00 00 00 00 00 00 00   false
00 00 00 00 00 00 00 01   true
```

Néanmoins, il est possible d'utiliser le type `char` pour stocker un booléen. On peut également utiliser de l'arithmétique binaire pour stocker 8 booléens sur un `uint8_t`. Voici un exemple de stockage de 8 booléens sur un `uint8_t` :

```c
#include <stdint.h>

uint8_t flags = 0b00000000;

int main (void) {
    flags |= 1 << 3; // Mettre le quatrième bit à 1
    flags &= ~(1 << 3); // Mettre le quatrième bit à 0
}
```

## Énumérations

Une énumération est un type de donnée un peu particulier qui permet de définir un ensemble de valeurs possibles associées à des noms symboliques. Ce style d'écriture permet de définir un type de données contenant un
nombre fini de valeurs. Ces valeurs sont nommées textuellement et
définies numériquement dans le type énuméré.

```c
enum ColorCode {
    COLOR_BLACK, // Vaut zéro par défaut
    COLOR_BROWN,
    COLOR_RED,
    COLOR_ORANGE,
    COLOR_YELLOW,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_PURPLE,
    COLOR_GRAY,
    COLOR_WHITE
};
```

Le type d'une énumération est apparenté à un entier `int`. Sans précision, la première valeur vaut 0, la suivante 1, etc. Il est néanmoins possible de forcer les valeurs de la manière suivante : [[||enum]]

```c
typedef enum country_codes {
    CODE_SWITZERLAND=41,
    CODE_BELGIUM=32,
    CODE_FRANCE, // Sera 33...
    CODE_SPAIN,  // Sera 34...
    CODE_US=1
} CountryCodes;
```

Pour ne pas confondre un type énuméré avec une variable, on utilise souvent la convention d'une notation en capitales. Pour éviter d’éventuelles collisions avec d'autres types, un préfixe est souvent ajouté ce qu'on appelle un **espace de nommage**.

L'utilisation d'un type énuméré peut être la suivante :

```c
void call(enum country_codes code) {
    switch(code) {
    case CODE_SWITZERLAND :
        printf("Calling Switzerland, please wait...\n");
        break;
    case CODE_BELGIUM :
        printf("Calling Belgium, please wait...\n");
        break;
    case CODE_FRANCE :
        printf("Calling France, please wait...\n");
        break;
    default :
        printf("No calls to this country are allowed yet!\n");
    }
}
```

## Type incomplet

En C, un [[type incomplet]] est un type de données dont la taille n'est pas encore complètement définie au moment de sa déclaration. En d'autres termes, le compilateur sait qu'un type existe, mais ne connaît pas encore la totalité des détails nécessaires pour allouer de la mémoire ou effectuer certaines opérations sur ce type. Un type incomplet peut apparaître dans le cas des structures ou des tableaux, notamment pour l'abstraction de données. Certains types comme `void` sont également incomplets.

### VLQ

Dans certains systèmes, on peut stocker des nombres entiers à taille variable. C'est-à-dire que l'on s'arrange pour réserver un bit supplémentaire dans le nombre pour indiquer si le nombre se poursuit sur un autre octet. C'est le cas des nombres entiers VLQ utilisés dans le protocole [[MIDI]]

On peut stocker un nombre [[VLQ]] en mémoire, mais on ne sait pas de combien d'octets on aura besoin. On peut donc définir un type incomplet pour ce type de donnée, mais nous aurons besoin de notions que nous n'avons pas encore vues pour le manipuler, les structures et les unions.

### Type vide (*void*)

Le type `void` est particulier. Il s'agit d'un type dit **incomplet**, car la taille de l'objet qu'il représente en mémoire n'est pas connue. Il est utilisé comme type de retour pour les fonctions qui ne retournent rien : [[||void]]

```c
void shout() {
    printf("Hey!\n");
}
```

Il peut être également utilisé comme type générique comme la fonction de copie mémoire `memcpy` [[||memcpy]] :

```c
void *memcpy(void * restrict dest, const void * restrict src, size_t n);
```

Le mot clé `void` ne peut être utilisé que dans les contextes suivants :

- Comme paramètre unique d'une fonction, indiquant que cette fonction n'a pas de paramètres `int main(void)`
- Comme type de retour pour une fonction indiquant que cette fonction ne retourne rien `void display(char c)`
- Comme pointeur dont le type de destination n'est pas spécifié `void* ptr`

## Transtypage

### Promotion implicite

Généralement le type `int` est de la même largeur que le bus mémoire de donnée d'un ordinateur. [[||promotion]] C'est-à-dire que c'est souvent, le type le plus optimisé pour véhiculer de l'information au sein du processeur. Les *registres* du processeur, autrement dit ses casiers mémoires, sont au moins assez grand pour  contenir un `int`.

Aussi, la plupart des types de taille inférieure à `int` sont automatiquement et implicitement promus en `int`. Le résultat de `a + b` lorsque `a` et `b` sont des `char` sera automatiquement un `int`.

Table: Promotion numérique

| Type source | Type cible |
| ----------- | ---------- |
| char        | int        |
| short       | int        |
| int         | long       |
| long        | float      |
| float       | double     |

Notez qu'il n'y a pas de promotion numérique vers le type *short*. On
passe directement à un type *int*.

!!! exercise "Promotion numérique"

    Représentez les promotions numériques qui surviennent lors de l'évaluation des expressions ci-dessous :

    ```c
    char c;
    short sh;
    int i;
    float f;
    double d;
    ```

    <div class="two-column-list" markdown>

    1. `c * sh - f / i + d;`
    2. `c * (sh – f) / i + d;`
    3. `c * sh - f - i + d;`
    4. `c + sh * f / i + d;`

    </div>

!!! exercise "Expressions mixtes"

    Soit les instructions suivantes :

    ```c
    int n = 10;
    int p = 7;
    float x = 2.5;
    ```

    Donnez le type et la valeur des expressions suivantes :

    <div class="two-column-list" markdown>

    1. `x + n % p`
    2. `x + p / n`
    3. `(x + p) / n`
    4. `.5 * n`
    5. `.5 * (float)n`
    6. `(int).5 * n`
    7. `(n + 1) / n`
    8. `(n + 1.0) / n`

    </div>

### Promotion explicite

Il est possible de forcer la promotion d'un type vers un autre en utilisant un transtypage explicite. Par exemple, pour forcer la promotion d'un `int` vers un `double` :

```c
int n = 10;
double x = (double)n;
```

Le changement de type forcé ([[transtypage]]) entre des variables de
différents types engendre des effets de bord qu'il faut connaître. Lors
d'un changement de type vers un type dont le pouvoir de représentation
est plus important, il n'y a pas de problème. À l'inverse, on peut
rencontrer des erreurs sur la précision ou une modification radicale de
la valeur représentée !

#### Transtypage d'un entier en flottant

Par exemple, la conversion d'un nombre flottant (*double* ou *float*) en entier (signé) doit être étudiée pour éviter tout problème. Le type entier doit être
capable de recevoir la valeur (attention aux valeurs maxi).

```c
double d=3.9;
long l=(long)d; // valeur : 3 => perte de précision
```

A l'exécution, la valeur de $l$ sera la partie entière de
$d$. Il n'y a pas d'arrondi.

```c
double d=0x12345678;
short sh=(short)d; // valeur : 0x5678 => changement de valeur
```

La variable sh (*short* sur 16 bit) ne peut contenir la valeur réelle.
Lors du transtypage, il y a modification de la valeur ce qui conduit à
des erreurs de calculs par la suite.

```c
double d=-123;
unsigned short sh=(unsigned short)d; // valeur : 65413 => changement de valeur
```

L'utilisation d'un type non signé pour convertir un nombre réel conduit
également à une modification de la valeur numérique.

#### Transtypage d'un double en float

La conversion d'un nombre réel de type *double* en réel de type *float*
pose un problème de précision de calcul.

```c
double d=0.1111111111111111;
float f=(float)d; // valeur : 0.1111111119389533 => perte de précision
```

À l'exécution, il y a une perte de précision lors de la conversion, ce
qui peut, lors d'un calcul itératif induire des erreurs de calcul.

!!! exercise "Conversion de types"

    On considère les déclarations suivantes :

    ```c
    float x;
    short i;
    unsigned short j;
    long k;
    unsigned long l;
    ```

    Identifiez les expressions ci-dessous dont le résultat n'est pas mathématiquement correct.

    ```c
    x = 1e6;
    i = x;
    j = -20;
    k = x;
    l = k;
    k = -20;
    l = k;
    ```

    ??? solution

        ```c
        x = 1e6;
        i = x;    // Incorrect, i peut-être limité à -32767..+32767 (C99 §5.2.4.2.1)
        j = -20;  // Incorrect, valeur signée dans un conteneur non signé
        k = x;
        l = k;
        k = -20;
        l = k;    // Incorrect, valeur signée dans un conteneur non signé
        ```

!!! exercise "Un casting explicite"

    Que valent les valeurs de `p`, `x` et `n`:

    ```c
    float x;
    int n, p;

    p = 2;
    x = (float)15 / p;
    n = x + 1.1;
    ```

    ??? solution

        ```text
        p ≡ 2
        x = 7.5
        n = 8
        ```

!!! exercise "Opérateurs de relation et opérateurs logiques"

    Soit les déclarations suivantes :

    ```c
    float x, y;
    bool condition;
    ```

    Réécrire l'expression ci-dessous en mettant des parenthèses montrant l'ordre des opérations :

    ```c
    condition = x >= 0 && x <= 20 && y > x || y == 50 && x == 2 || y == 60;
    ```

    Donner la valeur de `condition` évaluée avec les valeurs suivantes de `x` et `y`:

    <div class="two-column-list" markdown>

    1. `x = -1.0; y = 60.;`
    2. `x = 0; y = 1.;`
    3. `x = 19.0; y = 1.0;`
    4. `x = 0.0; y = 50.0;`
    5. `x = 2.0; y = 50.0;`
    6. `x = -10.0; y = 60.0;`

    </div>

    ??? solution

        ```c
        condition = (
            (x >= 0) && (x <= 20) && (y > x))
            ||
            ((y == 50) && (x == 2))
            ||
            (y == 60)
        );
        ```

        <div class="two-column-list" markdown>

        1. `true`
        2. `true`
        3. `false`
        4. `true`
        5. `true`
        6. `true`

        </div>

!!! exercise "Casse-tête"

    Vous participez à une revue de code et tombez sur quelques perles laissées par quelques collègues. Comment proposeriez-vous de corriger ces écritures ? Le code est écrit pour un modèle de donnée **LLP64**.

    Pour chaque exemple, donner la valeur des variables après exécution du code.

    1. &#32;

        ```c
        unsigned short i = 32767;
        i++;
        ```

    1. &#32;

        ```c
        short i = 32767;
        i++;
        ```

    1. &#32;

        ```c
        short i = 0;
        i = i--;
        i = --i;
        i = i--;
        ```

## Exercices de révision

!!! exercise "Évaluation d'expressions"

    Considérons les déclarations suivantes :

    ```c
    char c = 3;
    short s = 7;
    int i = 3;
    long l = 4;
    float f = 3.3;
    double d = 7.7;
    ```

    Que vaut le type et la valeur des expressions suivantes ?

    <div class="two-column-list" markdown>

    1. `c / 2`
    2. `sh + c / 10`
    3. `lg + i / 2.0`
    4. `d + f`
    5. `(int)d + f`
    6. `(int)d + lg`
    7. `c << 2`
    8. `sh & 0xF0`
    9. `sh && 0xF0`
    10. `sh == i + lg`
    11. `d + f == sh + lg`

    </div>

!!! exercise "Précision des flottants"

    Que vaut `x`?

    ```c
    float x = 10000000. + 0.1;
    ```

    ??? solution

        Le format float est stocké sur 32-bits avec 23-bits de mantisse et 8-bits d'exposants. Sa précision est donc limitée à environ 6 décimales. Pour représenter 10'000'000.1 il faut plus que 6 décimales et l'addition est donc caduc :

        ```c
        #include <stdio.h>

        int main(void) {
            float x = 10000000. + 0.1;
            printf("%f\n", x);
        }
        ```

        ```bash
        $ ./a.out
        10000000.000000
        ```

!!! exercise "Type de donnée idoine"

    Pour chaque entrée suivante, indiquez le nom et le type des variables que vous utiliseriez pour représenter les données dans ce programme :

    1. Gestion d'un parking: nombre de voitures présente
    2. Station météo
        a. Température moyenne de la journée
        b. Nombre de valeurs utilisées pour la moyenne
    3. Montant disponible sur un compte en banque
    4. Programme de calcul de d'énergie produite dans une centrale nucléaire
    5. Programme de conversion décimal, hexadécimal, binaire
    6. Produit scalaire de deux vecteurs plans
    7. Nombre d'impulsions reçues par un capteur de position incrémental

!!! exercise "Construction d'expressions"

    On considère un disque, divisé en 12 secteurs angulaires égaux, numérotés de 0
    à 11. On mesure l’angle de rotation du disque en degrés, sous la forme d’un
    nombre entier non signé. Une flèche fixe désigne un secteur. Entre 0 et 29 °, le
    secteur désigné est le n° 0, entre 30 ° et 59 °, c’est le secteur 1, ...

    Donnez une expression arithmétique permettant, en fonction d’un angle donné,
    d’indiquer quel est le secteur du disque se trouve devant la flèche. Note :
    l’angle de rotation peut être supérieur à 360 °. Vérifiez cette expression avec
    les angles de 0, 15, 29, 30, 59, 60, 360, 389, 390 degrés.

    Écrivez un programme demandant l’angle et affichant le numéro de secteur
    correspondant.

!!! exercise "Somme des entiers"

    Il est prouvé mathématiquement que la somme des entiers strictement positifs pris dans l'ordre croissant peut être exprimée comme :

    $$
    \sum_{k=1}^n k = \frac{n(n+1)}{2}
    $$

    சீனிவாச இராமானுஜன், un grand mathématicien ([Srinivasa Ramanujan](https://fr.wikipedia.org/wiki/Srinivasa_Ramanujan)) à démontré que ce la somme à l'infini donne :

    $$
    \sum_{k=1}^{\inf} k = -\frac{1}{12}
    $$

    Vous ne le croyez pas et décider d'utiliser le superordinateur [Pensées Profondes](https://fr.wikipedia.org/wiki/La_grande_question_sur_la_vie,_l%27univers_et_le_reste) pour faire ce calcul. Comme vous n'avez pas accès à cet ordinateur pour l'instant (et probablement vos enfants n'auront pas accès à cet ordinateur non plus), écrivez un programme simple pour tester votre algorithme et prenant en paramètre la valeur `n` à laquelle s'arrêter.

    Tester ensuite votre programme avec des valeurs de plus en plus grandes et analyser les performances avec le programme `time`:

    ```console
    $ time ./a.out 1000000000
    500000000500000000

    real    0m0.180s
    user    0m0.172s
    sys     0m0.016s
    ```

    À partir de quelle valeur, le temps de calcul devient significativement palpable ?

    ??? solution

        ```c
        #include <stdio.h>
        #include <stdlib.h>

        int main(int argc, char *argv[]) {
            long long n = atoi(argv[1]);
            long long sum = 0;
            for(size_t i = 0; i < n; i++, sum += i);
            printf("%lld\n", sum);
        }
        ```

!!! exercise "Système de vision industriel"

    La société japonaise Nakainœil développe des systèmes de vision industriels pour l'inspection de pièces dans une ligne d'assemblage. Le programme du système de vision comporte les variables internes suivantes :

    ```c
    uint32_t inspected_parts, bad_parts;
    float percentage_good_parts;
    ```

    À un moment du programme, on peut lire :

    ```c
    percentage_good_parts = (inspected_parts - bad_parts) / inspected_parts;
    ```

    Sachant que `inspected_parts = 2000` et `bad_parts = 200`:

    1. Quel résultat le développeur s'attend-il à obtenir ?
    2. Qu'obtient-il en pratique ?
    3. Pourquoi ?
    4. Corrigez les éventuelles erreurs.

    ??? solution

        1. Le développeur s'attend à obtenir le pourcentage de bonnes pièces avec plusieurs décimales après la virgule.
        2. En pratique, il obtient un entier, c'est-à-dire toujours 0.
        3. La promotion implicite des entiers peut être découpée comme suit :

            ```c
            (uint32_t)numerator = (uint32_t)inspected_parts - (uint32_t)bad_parts;
            (uint32_t)percentage = (uint32_t)numerator / (uint32_t)inspected_parts;
            (float)percentage_good_parts = (uint32_t)percentage;
            ```

        La division est donc appliquée à des entiers et non des flottants.

        4. Une possible correction consiste à forcer le type d'un des membres de la division :

            ```c
            percentage_good_parts = (float)(inspected_parts - bad_parts) / inspected_parts;
            ```

!!! exercise "Missile Patriot"

    Durant la guerre du Golfe le 25 février 1991, une batterie de missile américaine à Dharan en Arabie saoudite à échoué à intercepter un missile irakien Scud. Cet échec tua 28 soldats américains et en blessa 100 autres. L'erreur sera imputée à un problème de type de donnée sera longuement discutée dans le rapport **GAO/OMTEC-92-26** du commandement général.

    Un registre 24-bit est utilisé pour le stockage du temps écoulé depuis le démarrage du logiciel de contrôle indiquant le temps en dixième de secondes. Dès lors il a fallait multiplier ce temps par 1/10 pour obtenir le temps en seconde. La valeur 1/10 était tronquée à la 24^e décimale après la virgule. Des erreurs d'arrondi sont apparue menant à un décalage de près de 1 seconde après 100 heures de fonction. Or, cette erreur d'une seconde s'est traduite par 600 mètres d'erreur lors de la tentative d'interception.

    Le stockage de la valeur 0.1 est donné par :

    $$
    0.1_{10} \approx \lfloor 0.1_{10}\cdot 2^{23} \rfloor = 11001100110011001100_{2} \approx 0.09999990463256836
    $$

    Un registre contient donc le nombre d'heures écoulées exprimées en dixième de seconde soit pour 100 heures :

    $$
    100 \cdot 60 \cdot 60 \cdot 10 = 3'600'000
    $$

    En termes de virgule fixe, la première valeur est exprimée en Q1.23 tandis que la seconde en Q0.24. Multiplier les deux valeurs entre elles donne `Q1.23 x Q0.24 = Q1.47` le résultat est donc exprimé sur 48 bits. Il faut donc diviser le résultat du calcul par :math:`2^{47}` pour obtenir le nombre de secondes écoulées depuis le début la mise sous tension du système.

    Quel est l'erreur en seconde cumulée sur les 100 heures de fonctionnement ?

!!! exercise "Expressions arithmétiques entières"

    Donnez la valeur des expressions ci-dessous :

    ```text
    25 + 10 + 7 - 3
    5 / 2
    24 + 5 / 2
    (24 + 5) / 2
    25 / 5 / 2
    25 / (5 / 2)
    72 % 5 - 5
    72 / 5 - 5
    8 % 3
    -8 % 3
    8 % -3
    -8 % -3
    ```
