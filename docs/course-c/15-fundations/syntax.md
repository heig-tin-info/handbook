---
epigraph:
    text: "Tout devrait être rendu aussi simple que possible, mais pas plus simple."
    source: Albert Einstein
---
# Syntaxe

Ce chapitre traite des éléments constitutifs et fondamentaux du langage C. Il traite des généralités propres au langage, mais aussi des notions élémentaires permettant d'interpréter du code source. Notons que ce chapitre est transversal, à sa première lecture, le profane ne pourra tout comprendre sans savoir lu et maîtrisé les chapitres suivants, néanmoins il retrouvera ici les aspects fondamentaux du langage.

## L'alphabet

[[||alphabet, l']]

Heureusement pour nous occidentaux, l'alphabet de C est composé de 52 caractères latins et de 10 [chiffres indo-arabes](https://fr.wikipedia.org/wiki/Chiffres_arabes) :

```text
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
a b c d e f g h i j k l m n o p q r s t u v w x y z
0 1 2 3 4 5 6 7 8 9
```

Pour comparaison, le système d'écriture coréen ([[Hangul]]) est [[alphasyllabique]], c'est-à-dire que chaque caractère représente une syllabe. Les lettres de base sont composées de 14 consonnes de base et 10 voyelles. Quant aux chiffres, ils sont les mêmes qu'en occident.

```text
g n d r/l m b s ng j ch k t p h
ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ

a ya eo yeo o yo u yu eu i
ㅏ ㅑ ㅓ ㅕ ㅗ ㅛ ㅜ ㅠ ㅡ ㅣ
```

Les Japonais quant à eux utilisent trois systèmes d'écriture, le [[Hiragana]], le [[Katakana]] et le [[Kanji]]. Les deux premiers sont des syllabaires et le dernier est un système d'[[écriture logographique]]. Le Hiragana et Katakana ont tous deux 46 caractères de base. Voici l'exemple du Katakana:

```text
あ (a),  い (i),   う (u),   え (e),  お (o)
か (ka), き (ki),  く (ku),  け (ke), こ (ko)
さ (sa), し (shi), す (su),  せ (se), そ (so)
た (ta), ち (chi), つ (tsu), て (te), と (to)
な (na), に (ni),  ぬ (nu),  ね (ne), の (no)
は (ha), ひ (hi),  ふ (fu),  へ (he), ほ (ho)
ま (ma), み (mi),  む (mu),  め (me), も (mo)
や (ya), ゆ (yu),  よ (yo)
ら (ra), り (ri),  る (ru),  れ (re), ろ (ro)
わ (wa), を (wo)
ん (n)
```

On notera ici que l'alphabet latin est tout particulièrement adapté à la programmation, car, d'une part ce fut le premier alphabet à être utilisé pour l'écriture de programmes informatiques et d'autre part, il reste assez simple pour être utilisé par des machines. On peut noter en outre que les pays qui utilisent leur propre alphabet doivent impérativement apprendre et maîtriser l'alphabet latin pour pouvoir programmer. Ceci implique qu'ils doivent également disposer d'un clavier latin pour pouvoir saisir leur code. Ayez à l'esprit que nous sommes des privilégiés de ne pas devoir jongler avec plusieurs alphabets pour écrire du code...

Outre ces caractères, la séparation des symboles est assurée par [une espace](https://fr.wikipedia.org/wiki/Espace_(typographie)), une tabulation horizontale, une [[tabulation]] verticale, et un caractère de retour à la ligne. Ces caractères ne sont pas imprimables, c'est-à-dire qu'ils ne sont pas directement visibles ni à l'écran ni à l'impression (ni sur le papier d'ailleurs). Microsoft Word et d'autres éditeurs utilisent généralement le [pied-de-mouche](https://fr.wikipedia.org/wiki/Pied-de-mouche) `¶` U+00B6 pour indiquer les fins de paragraphes qui sont également des caractères non imprimables. [[||pied-de-mouche (¶)]] [[||caractère non imprimable]]

La convention est de nommer les caractères non imprimables soit par leur acronyme `LF` pour *Line Feed* ou soit par leur convention C échappée par un *backslash n* `\n`:

Table: Caractères non imprimables

| Acronyme | Échappé | Description            |
| -------- | ------- | ---------------------- |
| LF       | `\n`    | Retour à la ligne      |
| VT       | `\v`    | Tabulation verticale   |
| FF       | `\f`    | Nouvelle page          |
| TAB      | `\t`    | Tabulation horizontale |
| CR       | `\r`    | Retour charriot        |
| SPACE    | `\040`  | Espace                 |
| NUL      | `\0`    | Caractère nul          |

Voici en pratique comment ces caractères peuvent être utilisés :

![Distinction de différents caractères non imprimables](/assets/images/crlf.drawio)

La ponctuation utilise les 29 symboles graphiques suivants :

```text
! # % ^ & * ( _ ) - + = ~ [ ] ' | \ ; : " { } , . < > / ?
```

## La machine à écrire

Peut-être avez-vous déjà été confronté à une machine à écrire mécanique. Elles disposent d'un levier sur la gauche du chariot qui dispose de deux fonctionnalités. D'une part il permet de faire revenir le chariot au début de la ligne, mais également de faire avancer le papier d'une ligne par une rotation du cylindre. C'est ce levier de retour chariot qui a donné son nom au caractère de retour à la ligne `CR` pour *Carriage Return*. Quant au caractère de nouvelle ligne `LF` pour *Line Feed*, il est associé à la rotation du rouleau qui entraîne la feuille de papier.

![Machine à écrire Hermès 3000 hébraïque](/assets/images/hermes-3000.webp){width=50%}

Historiquement il y a donc bien une distinction entre ces deux caractères, mais aujourd'hui, cela n'a plus vraiment de sens. Un autre point que l'on peut relever est que pour souligner un texte, on utilisait le caractère de soulignement ([[tiret bas]], ou *underscore*) `_` pour mettre en emphase du texte déjà écrit. De même pour barrer un texte, on utilisait le caractère `-` pour faire reculer le chariot d'une demi-case et ensuite frapper le même caractère. Enfin, pour ajouter un accent circonflexe, il fallait utiliser la touche `^` pour faire reculer le chariot d'une demi-case et ensuite frapper la lettre à accentuer.

Ces subtilités de la machine à écrire ont été partiellement reprises dans le format [Unicode][unicode]. Aussi pour écrire un accent aigu, il y a aujourd'hui plusieurs façons de le faire.

1. Utiliser le caractère `e` U+0065 suivi du caractère `´` U+0301 aussi appelé *combining acute accent* pour obtenir `é`. U+0301
2. Utiliser le caractère `é` U+00E9 directement. U+0065 U+00E9

Ces héritages historiques font qu'il est difficile aujourd'hui de traiter sans bogue les textes multilingues. Les cas particuliers sont nombreux et bien souvent, les informaticiens utilisent des bibliothèques logicielles pour gérer ces cas particuliers.

Un fait historique intéressant est que les premiers ordinateurs ne disposaient pas d'un clavier ayant tous ces symboles et la commission responsable de standardiser C a intégré au standard les **trigraphes** et plus tard les **digraphes** qui sont des combinaisons de caractères de base qui remplacent les caractères impossibles à saisir directement. Ainsi `<:` est le digraphe de `[` et `??<` est le trigraphe de `{`. Néanmoins vous conviendrez cher lecteur que ces alternatives ne devraient être utilisées que dans des cas extrêmes et justifiables. Par ailleurs, le standard C et C++ songe à les retirer.

Retenez que C peut être un langage extrêmement cryptique tant il est permissif sur sa syntaxe. Il existe d'ailleurs un concours international d'obfuscation, le [The International Obfuscated C Code Contest](https://www.ioccc.org/) qui prime des codes les plus subtils et illisibles comme le code suivant écrit par [Chris Mills](https://www.ioccc.org/2015/mills2/prog.c). Il s'agit d'ailleurs d'un exemple qui compile parfaitement sur la plupart des compilateurs.

```c
    int I=256,l,c, o,O=3; void e(
int L){ o=0; for( l=8; L>>++l&&
16>l;                           o+=l
<<l-                            1) ;
o+=l                     *L-(l<<l-1); { ; }
if (                    pread(3,&L,3,O+o/8)<
2)/*                    */exit(0);  L>>=7&o;
L%=1                     <<l; L>>8?256-L?e(
L-1)                            ,c||
(e(c                            =L),
c=0)                            :( O
+=(-I&7)*l+o+l>>3,I=L):putchar(
    L); }int main(int l,char**o){
                for(
            /*          ////      */
            open(1[o],0); ; e(I++
            ))                    ;}
```

??? info "Exemple grivois"

    Ce code également issu du IOCCC est un exemple pas très gracieux de ce qu'il est possible de faire en C. Il est à noter que ce code compile parfaitement et affiche un message pas très Catholique.

    ```c
    main(i){for(i=160;i--;putchar(i%32?"œ™cæRJ""\\J•äRJ""œ]dä"[i/8]&1<<i%8?42:32:10));}
    ```

## Fin de lignes (EOL)

[[||EOL, fin de ligne]] [[||CR, retour chariot]] [[||LF, nouvelle ligne]]

À l'instar des premières machines à écrire, les [téléscripteurs](https://fr.wikipedia.org/wiki/T%C3%A9l%C3%A9scripteur) possédaient de nombreux caractères de déplacement qui sont depuis tombés en désuétude et prêtent aujourd'hui à confusion même pour le plus aguerri des programmeurs. Maintenant que les ordinateurs possèdent des écrans, la notion originale du terme [retour chariot](https://fr.wikipedia.org/wiki/Retour_chariot) est compromise et comme il y a autant d'avis que d'ingénieurs, les premiers PC [IBM compatibles](https://fr.wikipedia.org/wiki/Compatible_PC) ont choisi qu'une nouvelle ligne dût toujours se composer de deux caractères: un retour chariot (`CR`) et une nouvelle ligne (`LF`) ou en C `\r\n`. Les premiers [Macintosh](https://fr.wikipedia.org/wiki/Macintosh) d'Apple jugeant inutile de gaspiller deux caractères pour chaque nouvelle ligne dans un fichier et ont décidé d'associer le retour chariot et la nouvelle ligne dans le caractère `\r`. Enfin, les ordinateurs UNIX ont eu le même raisonnement, mais ils ont choisi de ne garder que `\n`.

Heureusement, depuis qu'Apple a migré son système sur une base BSD (UNIX) en 2001, les systèmes d'exploitation modernes ont adopté le standard UNIX et il n'y a plus de problème de compatibilité entre les systèmes. En sommes, il existe aujourd'hui deux types de fin de ligne :

- `LF` ou `\n` sur tous les ordinateurs de la planète à l'exception de Windows,
- `CRLF` ou `\r\n` sur les ordinateurs Windows.

Il n'y a pas de consensus établi sur lesquels des deux types de fin de ligne (`EOL`: *End Of Line*) il faut utiliser, faite preuve de bon sens et surtout, soyez cohérent.

## Mots clés

[[||mot clé]]

Le langage de programmation C tel que défini par C17 comporte 44 mots clés :

```c
auto       break      case       char       const
continue   default    do         double     else
enum       extern     float      for        goto
if         inline     int        long       register
restrict   return     short      signed     sizeof
static     struct     switch     typedef    union
unsigned   void       volatile   while      _Alignas
_Alignof   _Atomic    _Bool      _Complex   _Generic
_Imaginary _Noreturn  _Static_assert        _Thread_local
```

[[||_Bool]] [[||_Complex]] [[||_Imaginary]] [[||auto]] [[||break]] [[||case]] [[||char]] [[||const]] [[||continue]] [[||default]] [[||do]] [[||double]] [[||else]] [[||enum]] [[||extern]] [[||float]] [[||for]] [[||goto]] [[||if]] [[||inline]] [[||int]] [[||long]] [[||register]] [[||restrict]] [[||return]] [[||short]] [[||signed]] [[||sizeof]] [[||static]] [[||struct]] [[||switch]] [[||typedef]] [[||union]] [[||unsigned]] [[||void]] [[||volatile]] [[||while]]

Dans ce cours, l'usage des mots clés suivants est découragé, car leur utilisation pourrait prêter à confusion ou mener à des inélégances d'écriture.

```c
_Bool, _imaginary, auto, goto, inline, long, register, restrict, short
```

Il n'y a donc plus que 35 mots clés à connaître pour être un bon développeur C.

Notons que les mots clés `true` et `false` ne sont pas standardisés en C, mais ils le sont en C++. [[||true]] [[||false]]

Ces mots clés font partie intégrante de la [grammaire][grammar] du langage et ne peuvent être utilisés pour identifier des variables, des fonctions ou des étiquettes.

??? info "Nombre de mots clés"

    On peut se demander s'il est préférable pour un langage d'avoir plus ou moins de mots clés. En effet, plus il y a de mots clés, plus il est difficile d'apprendre le langage, mais plus il y a de mots clés, plus il est facile de comprendre le code des autres.

    C'est le même dilemme entre les architectures processeur RISC et CISC. Les architectures RISC ont moins d'instructions, mais elles sont plus complexes à utiliser, tandis que les architectures CISC ont plus d'instructions, mais elles sont plus simples à utiliser.

    Le Perl par exemple n'a environ que 20 mots clés, mais il est réputé pour être un langage difficile à apprendre. Le C++ dans sa version 2020 en a plus de 84.

[](){#identifier}

## Identificateurs

Un identificateur est une séquence de caractères représentant une entité du programme et à laquelle il est possible de se référer. Un identificateur est défini par une grammaire régulière qui peut être exprimée comme suit :

![Grammaire d'un identificateur C](/assets/images/identifier.drawio)

La notation `#!re /[a-z]/` signifie que l'on peut utiliser n'importe quelle lettre minuscule de l'alphabet latin, `#!re /[A-Z]/` pour les lettres majuscules, `#!re /[0-9]/` pour les chiffres et `_` pour le caractère souligné.

En addition de cette grammaire, voici quelques règles :

1. Un identificateur ne peut pas être l'un des mots clés du langage.
2. Les identificateurs sont sensibles à la [casse](https://fr.wikipedia.org/wiki/Casse_(typographie)) (majuscule/minuscule).
3. Le standard C99, se réserve l'usage de tous les identificateurs débutant par `_` suivi d'une lettre majuscule ou un autre *underscore* `_`.
4. Le standard POSIX, se réserve l'usage de tous les identificateurs finissant par `_t`.

!!! tip "Expression régulière"

    Il est possible d'exprimer la syntaxe d'un identificateur à l'aide de l'expression régulière suivante :

    `#!re /^[a-zA-Z_][a-zA-Z0-9_]*$/`

!!! exercise "Validité des identificateurs"

    Pour chacune des suites de caractères ci-dessous, indiquez s'il s'agit d'un identificateur valide et utilisable en C. Justifier votre réponse.

    /// html | div[class='three-column-list']

    - [ ] `2_pi`
    - [x] `x_2`
    - [x] `x___3`
    - [ ] `x 2`
    - [x] `positionRobot`
    - [x] `piece_presente`
    - [x] `_commande_vanne`
    - [ ] `-courant_sortie`
    - [x] `_alarme_`
    - [ ] `panne#2`
    - [ ] `int`
    - [ ] `défaillance`
    - [ ] `f'`
    - [x] `INT`

    ///

    ??? solution

        Une excellente approche serait d'utiliser directement l'expression régulière fournie et d'utiliser l'outil en ligne [regex101.com](https://regex101.com/r/cmxaic/1).

        /// html | div[class='two-column-list']

        1. `2_pi` **invalide**, car commence par un chiffre
        2. `x_2` **valide**
        3. `x___3` **valide**
        4. `x 2` **invalide**, car comporte un espace
        5. `positionRobot` **valide**, notation *camelCase*
        6. `piece_presente` **valide**, notation *snake_case*
        7. `_commande_vanne` **valide**
        8. `-courant_sortie` **invalide**, un identificateur ne peut pas commencer par le signe `-`
        9. `_alarme_` **valide**
        10. `panne#2` **invalide**, le caractère `#` n'est pas autorisé
        11. `int` **invalide**, `int` est un mot réservé du langage
        12. `défaillance` **invalide**, uniquement les caractères imprimable ASCII sont autorisés
        13. `f'` **invalide** l'apostrophe n'est pas autorisée
        14. `INT` **valide**

        ///

Il faut noter que le standard C autorise depuis C11 l'utilisation de caractères Unicode dans les identificateurs, mais cette fonctionnalité est rarement implémentée par les compilateurs. Avec gcc le programme suivant est valide:

```c
#include <stdio.h>

int main() {
    int 💩 = 42;
    printf("Salut %d", 💩);
}
```

## Variables

Une [[variable]] est un [[symbole]] qui associe un nom (**identificateur**) à une **valeur**. Comme son nom l'indique, une variable peut voir son contenu varier au cours du temps.

Une variable est définie par :

- Son **nom** (*name*), c'est-à-dire l'identificateur associé au symbole.
- Son **type** (*type*), qui est la convention d'interprétation du contenu binaire en mémoire.
- Sa **valeur** (*value*), qui est le contenu interprété connaissant son **type**.
- Son **adresse** (*address*) qui est l'emplacement mémoire ou la représentation binaire sera enregistrée.
- Sa **portée** (*scope*) qui est la portion de code où le symbole est défini et accessible.
- Sa **visibilité** (*visibility*) qui ne peut être que *public* en C.

Pour mieux comprendre ce concept fondamental, imaginons la plage de Donnant à Belle-Île-en-Mer. Quelqu'un a écrit sur le sable, bien visible depuis la colline adjacente, le mot `COIN`. L'identificateur c'est `Donnant`, la valeur c'est `COIN`, le type permet de savoir comment interpréter la valeur. Cela peut s'agir d'une pièce de monnaie en anglais, du coin d'une table en français ou du lapin en néerlandais.

L'**adresse** est l'emplacement exact de la plage où le mot a été écrit (47.32638670571° N, 3.2363350691522° W), la portée est la plage de Donnant et la visibilité est la colline adjacente.

On voit que sans connaître le **type** de la variable, il est impossible de savoir comment interpréter sa **valeur**.

![La plage de Donnant](/assets/images/donnant.png)

En pratique l'adresse sera plutôt de la forme `0x7fffbf7f1b4c`, la valeur serait plutôt `0100001101001111010010010100111000000000` et le type serait une chaîne de caractères `char[]`.

!!! info "Variables initialisées"

    Le fait de déclarer des variables dans en langage C implique que le
    logiciel doit réaliser l'initialisation de ces variables au tout début
    de son exécution. De fait, on peut remarquer deux choses. Il y a les
    variables initialisées à la valeur zéro et les variables initialisées à
    des valeurs différentes de zéro. Le compilateur regroupe en mémoire ces
    variables en deux catégories et ajoute un bout de code au début de votre
    application (qui est exécuté avant le `main`).

    Ce code (que l'on n'a pas à écrire) effectue les opérations suivantes :

    - mise à zéro du bloc mémoire contenant les variables ayant été
      déclarées avec une valeur d'initialisation à zéro,
    - recopie d'une zone mémoire contenant les valeurs initiales des
      variables ayant été déclarées avec une valeur d'initialisation
      différente de zéro vers la zone de ces mêmes variables.

    Par ce fait, dès que l'exécution du logiciel est effectuée, on a, lors
    de l'exécution du `main`, des variables correctement initialisées.

### Déclaration

Avant de pouvoir être utilisée, une variable doit être **déclarée** afin que le compilateur puisse réserver un emplacement en mémoire pour stocker sa valeur.

Voici quelques déclarations valides :

```c
char c = '€';
int temperature = 37;
float neptune_stone_height = 376.86;
char message[] = "Jarvis, il faut parfois savoir "
                 "courir avant de savoir marcher.";
```

Il n'est pas nécessaire d'associer une valeur initiale à une variable, une [[déclaration]] peut se faire sans [[initialisation]] comme montré dans l'exemple suivant dans lequel on réserve trois variables `i`, `j`, `k`.

```c
int i, j, k;
```

!!! exercise "Affectation de variables"

    Considérons les déclarations suivantes :

    ```c
    int a, b, c;
    float x;
    ```

    Notez après chaque affectation, le contenu des différentes variables :

    | Ligne | Instruction    | `a` | `b` | `c` | `x` |
    | ----- | -------------- | --- | --- | --- | --- |
    | 1     | `a = 5;`       |     |     |     |     |
    | 2     | `b = c;`       |     |     |     |     |
    | 3     | `c = a;`       |     |     |     |     |
    | 4     | `a = a + 1;`   |     |     |     |     |
    | 5     | `x = a - ++c;` |     |     |     |     |
    | 6     | `b = c = x;`   |     |     |     |     |
    | 7     | `x + 2. = 7.;` |     |     |     |     |

    ??? solution

        | Ligne | Instruction    | `a` | `b` | `c` | `x` |
        | ----- | -------------- | --- | --- | --- | --- |
        | 1     | `a = 5;`       | 5   | ?   | ?   | ?   |
        | 2     | `b = c;`       | 5   | ?   | ?   | ?   |
        | 3     | `c = a;`       | 5   | ?   | 5   | ?   |
        | 4     | `a = a + 1;`   | 6   | ?   | 5   | ?   |
        | 5     | `x = a - ++c;` | 6   | ?   | 6   | 12  |
        | 6     | `b = c = x;`   | 6   | 12  | 12  | 12  |
        | 7     | `x + 2. = 7.;` | -   | -   | -   | -   |

### Convention de nommage

![Différentes casses illustrées](/assets/images/kebab.png)

Il existe autant de conventions de nommage qu'il y a de développeurs, mais un consensus majoritaire, que l'on retrouve dans d'autres langages de programmation dit que :

- la longueur du nom d'une variable est généralement proportionnelle à sa portée et donc il est d'autant plus court que l'utilisation d'une variable est localisée ;
- le nom doit être concis et précis et ne pas laisser place à une quelconque ambiguïté ;
- le nom doit participer à l'autodocumentation du code et permettre à un lecteur de comprendre facilement le programme qu'il lit.

Selon les standards adoptés, chaque société on trouve ceux qui préfèrent nommer les variables en utilisant un *underscore* (`_`) comme séparateur et ceux qui préfèrent nommer une variable en utilisant des majuscules comme séparateurs de mots.

Table: Conventions de nommage

| Convention   | Nom français     | Exemple            |
| ------------ | ---------------- | ------------------ |
| *camelcase*  | Casse de chameau | `userLoginCount`   |
| *snakecase*  | Casse de serpent | `user_login_count` |
| *pascalcase* | Casse de Pascal  | `UserLoginCount`   |
| *kebabcase*  | Casse de kebab   | `user-login-count` |

[[||camelCase]] [[||snake_case]] [[||PascalCase]] [[||kebab-case]]

!!! note

    La casse de kebab n'est pas acceptée par le standard C car les noms formés ne sont pas des identificateurs valides. Néanmoins cette notation est beaucoup utilisée par exemple sur GitHub.

### Variable métasyntaxique

Souvent lors d'exemples donnés en programmation, on utilise des variables génériques dites [métasyntaxiques](https://fr.wikipedia.org/wiki/Variable_m%C3%A9tasyntaxique). En français les valeurs `toto`, `titi`, `tata` et `tutu` sont régulièrement utilisées tandis qu'en anglais
`foo`, `bar`, `baz` et `qux` sont régulièrement utilisés. Les valeurs `spam`, `ham` et `eggs` sont quant à elles souvent utilisée en Python, en référence au sketch [Spam](https://en.wikipedia.org/wiki/Spam_(Monty_Python)) des Monthy Python. [[||Monty Python]] [[||foo]] [[||bar]] [[||baz]] [[||qux]] [[||spam]] [[||ham]] [[||eggs]]

Leur usage est conseillé pour appuyer le cadre générique d'un exemple sans lui donner la consonance d'un problème plus spécifique.

On trouvera une [table](http://www.catb.org/jargon/html/M/metasyntactic-variable.html) des différents noms les plus courants utilisés dans différentes langues.

!!! info "Foo, Bar, Titi et Toto"

    L'origine de `foo` et `bar` remonte à la [deuxième guerre mondiale](https://en.wikipedia.org/wiki/FUBAR) où les militaires américains utilisaient ces termes pour désigner des objets non identifiés.

    Titi et Toto sont des personnages de bande dessinée créés par [Maurice Cuvillier](https://fr.wikipedia.org/wiki/Maurice_Cuvillier) en 1931.

## Les constantes

Une constante par opposition à une variable voit son contenu **fixe** et **immuable**. Il s'agit d'un espace mémoire qui ne peut être modifié après son initialisation. Formellement, une constante se déclare comme une variable, mais préfixée du mot-clé `const`.

```c
const double scale_factor = 12.67;
```

Une [[constante]] est principalement utilisée pour indiquer au développeur que la valeur ne doit pas être modifiée. Le compilateur peut également s'en servir pour mieux optimiser le code et donc améliorer les performances d'exécution.

!!! warning

    Il ne faut pas confondre la **constante** qui est une variable immuable, stockée en mémoire et une **macro** qui appartient au préprocesseur. Sur certaines plateformes, le fichier d'en-tête `math.h` définit par exemple la constante `M_PI` sous forme de macro.

    ```c
    #define M_PI 3.14159265358979323846
    ```

    Cette même constante peut être définie comme une variable constante :

    ```c
    const double pi = 3.14159265358979323846;
    ```

En résumé, les constantes sont utilisées pour:

- Éviter les erreurs de programmation en évitant de modifier une valeur qui ne devrait pas l'être.
- Indiquer au compilateur que la valeur ne changera pas et qu'il peut optimiser le code en conséquence.
- Indiquer au développeur que la valeur ne sera pas modifiée plus tard dans le programme.

## Constantes littérales

Les constantes littérales représentent des **grandeurs scalaires** numériques ou de caractères et initialisées lors de la phase de compilation. [[||constante littérale]]

En effet, lorsque l'on veut saisir un nombre, on ne veut pas que le compilateur la comprenne comme un identificateur, mais bien comme une valeur numérique. C'est d'ailleurs la raison pour laquelle un identificateur ne peut pas commencer par un chiffre.

Les constantes littérales sont généralement identifiées avec des préfixes et des suffixes pour indiquer leur nature. Voici quelques exemples :

```c
6      // Le nombre d'heures sur l'horloge du Palais du Quirinal à Rome
12u    // Grandeur non signée
6l     // Grandeur entière signée codée sur un entier long
42ul   // Grandeur entière non signée codée sur un entier long
010    // Grandeur octale valant 8 en décimal
0xa    // Grandeur hexadécimale valant 10 en décimal
0b111  // Grandeur binaire valant 7 en décimal
1.     // Grandeur réelle exprimée en virgule flottante
'0'    // Grandeur caractère valant 48 en décimal
2e3    // Grandeur réelle exprimée en notation scientifique
```

Nous l'avons vu plus haut, le **type** d'une variable est important pour déterminer comment une valeur est stockée en mémoire.

Comme vu dans le chapitre sur la [numération][numeration], les valeurs numériques peuvent être stockées en mémoire de différentes manières. Ainsi, une valeur `48` peut être stockée sur un octet, un mot de 16 bits, un mot de 32 bits ou un mot de 64 bits. De plus, la valeur peut faire référence au caractère `0` en ASCII, mais aussi au nombre `72` s'il est exprimé en hexadécimal.

On utilisera un préfixe devant un nombre `0x` pour indiquer qu'il est en hexadécimal, `0b` pour indiquer qu'il est en binaire et `0` pour indiquer qu'il est en octal. Sans préfixe il s'agit d'un nombre décimal (base 10). [[||0x]] [[||0b]]

On utilisera un suffixe `u` pour indiquer que le nombre est non signé (n'admettant pas de valeurs négatives) et `l` pour indiquer qu'il est long ou `ll` pour indiquer qu'il est très long.

Quant aux guillemets simples `'`, ils sont utilisés pour délimiter un caractère de la table ASCII.

??? info "Expressions régulières"

    Il est plus facile pour un informaticien de comprendre la syntaxe des constantes littérales en utilisant des expressions régulières. Voici les expressions régulières qui définissent les différentes constantes littérales :

    | Type               | Expression régulière    | Exemple |
    | ------------------ | ----------------------- | ------- |
    | Nombre signé       | `#!re /[1-9][0-9]*/`    | `42`    |
    | Nombre non signé   | `#!re /[1-9][0-9]*u/`   | `42u`   |
    | Nombre hexadécimal | `#!re /0x[0-9a-fA-F]+/` | `0x2a`  |
    | Nombre octal       | `#!re /0[0-7]+/`        | `052`   |

    Vous pouvez essayer de les tester sur [regex101.com](https://regex101.com/).

!!! exercise "Constances littérales"

    Pour les entrées suivantes, indiquez lesquelles sont correctes.

    /// html | div[class='two-column-list']

    - [x] `12.3`
    - [x] `12E03`
    - [x] `12u`
    - [ ] `12.0u`
    - [ ] `1L`
    - [ ] `1.0L`
    - [x] `.9`
    - [x] `9.`
    - [ ] `.`
    - [x] `0x33`
    - [ ] `0xefg`
    - [x] `0xef`
    - [x] `0xeF`
    - [ ] `0x0.2`
    - [x] `09`
    - [x] `02`

    ///

La [[notation scientifique]], aussi appelée [[notation exponentielle]], est une manière d'écrire des nombres très grands ou très petits de manière plus compacte. Par exemple, `1.23e3` est équivalent à `1230.` et `1.23e-3` est équivalent à `0.00123`. Le caractère `e` est utilisé pour indiquer la puissance de 10 par laquelle le nombre doit être multiplié. Il tire probablement son origine du Fortran qui l'utilisait déjà en 1957.

!!! warning "Pas Euler"

    Il ne faut pas confondre l'exponentiation avec le nombre d'Euler (2.71828...) `e` avec la notation scientifique `e` qui est utilisée pour indiquer une puissance de 10.

!!! warning "La notation scientifique est un double"

    En C, la notation scientifique est toujours un nombre en virgule flottante de type `double`. Ainsi, `1e3` est un `double` et non un `int`. Ne prenez donc pas l'habitude d'écrire `int i = 1e3;`, mais plutôt `int i = 1000;`.

## Opérateur d'affectation

Dans les exemples ci-dessus, on utilise l'opérateur d'affectation pour associer une valeur à une variable. Historiquement, et malheureusement, le symbole choisi pour cet opérateur est le signe égal `=` or, l'égalité est une notion mathématique qui n'est en aucun cas reliée à l'affectation. [[||=]]

Pour mieux saisir la nuance, considérons le programme suivant :

```c
a = 42;
a = b;
```

Mathématiquement, la valeur de `b` devrait être égale à 42 ce qui n'est pas le cas en C où il faut lire, séquentiellement l'exécution du code, car oui, C est un langage **impératif**. Ainsi, dans l'ordre, on lit :

1. J'assigne la valeur 42 à la variable symbolisée par `a`
2. Puis, j'assigne la valeur de la variable `b` au contenu de `a`.

Comme on ne connaît pas la valeur de `b`, avec cet exemple, on ne peut pas connaître la valeur de `a`. Certains langages de programmation ont été sensibilisés à l'importance de cette distinction et dans les langages **F#**, **OCaml**, **R** ou **S**, l'opérateur d'affectation est `<-` et une affectation pourrait s'écrire par exemple: `a <- 42` ou `42 -> a`.

En C, l'opérateur d'égalité que nous verrons plus loin s'écrit `==` (deux `=` concaténés). [[||==]]

Remarquez ici que l'opérateur d'affectation de C agit toujours de droite à gauche c'est-à-dire que la valeur à **droite** de l'opérateur est affectée à la variable située à **gauche** de l'opérateur. S'agissant d'un opérateur il est possible de chaîner les opérations, comme on le ferait avec l'opérateur `+` et dans l'exemple suivant il faut lire que `42` est assigné à `c`, que la valeur de `c` est ensuite assigné à `b` et enfin la valeur de `b` est assignée à `a`. Nous verrons plus tard comment l'ordre des opérations et l'associativité de chaque opérateur.

```c
a = b = c = 42;
```

!!! exercise "Affectations simples"

    Donnez les valeurs de `x`, `n`, `p` après l'exécution des instructions ci-dessous :

    ```c
    float x;
    int n, p;

    p = 2;
    x = 15 / p;
    n = x + 0.5;
    ```

    ??? solution

        ```text
        p ≡ 2
        x ≡ 7
        n ≡ 7
        ```

!!! exercise "Trop d'égalités"

    On considère les déclarations suivantes :

    ```c
    int i, j, k;
    ```

    Donnez les valeurs des variables `i`, `j` et `k` après l'exécution de chacune des expressions ci-dessous. Qu'en pensez-vous ?

    ```c
    /* 1 */ i = (k = 2) + (j = 3);
    /* 2 */ i = (k = 2) + (j = 2) + j * 3 + k * 4;
    /* 3 */ i = (i = 3) + (k = 2) + (j = i + 1) + (k = j + 2) + (j = k - 1);
    ```

    ??? solution

        Selon la table de priorité des opérateurs, on note :

        - `()` priorité 1 associativité à droite
        - `*` priorité 3 associativité à gauche
        - `+` priorité 4 associativité à droite
        - `=` priorité 14 associativité à gauche

        En revanche rien n'est dit sur les `point de séquences <https://en.wikipedia.org/wiki/Sequence_point>`__. L'opérateur d'affectation n'est pas un point de séquence, autrement dit le standard C99 (Annexe C) ne définit pas l'ordre dans lequel les assignations sont effectuées.

        Ainsi, seul le premier point possède une solution, les deux autres sont indéterminés

        1. `i = (k = 2) + (j = 3)`

            - `i = 5`
            - `j = 3`
            - `k = 2`

        2. `i = (k = 2) + (j = 2) + j * 3 + k * 4`

            - Résultat indéterminé

        3. `i = (i = 3) + (k = 2) + (j = i + 1) + (k = j + 2) + (j = k - 1)`

            - Résultat indéterminé

## Espaces de noms

En C, il est possible d'utiliser le même identificateur pour autant qu'il n'appartient pas au même espace de nom. Il existe en C plusieurs espaces de noms :

- étiquettes utilisées pour l'instruction `goto`;
- tag de structures, d'énumérations et d'union;
- membres de structures, d'énumérations et d'union;
- identificateurs de variable ou fonctions.

Ces espaces de noms sont indépendants les uns des autres, il est donc possible d'utiliser le même nom sans conflit. Par exemple:

```c
typedef struct x {  // Espace de nom des structures
    int x;  // Membre de la structure point
} x;  // Espace de nom des types

int main() {
    x x = {.x = 42};  // x est une variable de type x
}
```

## Commentaires

Comme en français et ainsi qu'illustré par la figure suivante, il est possible d'annoter un programme avec des **commentaires**. Les commentaires n'ont pas d'incidence sur le fonctionnement d'un programme et ne peuvent être lus que par le développeur qui possède le code source. Par ailleurs, comme nous l'avons vu en [introduction][preproc-intro], le préprocesseur C supprime les commentaires du code source avant la compilation. [[||commentaire]]

![Les carafes dans la Vivonne](/assets/images/vivonne.drawio)

Il existe deux manières d'écrire un commentaire en C, les commentaires de lignes apparus avec le C++ et C99, ainsi que les commentaires de blocs. Les commentaires de blocs sont plus anciens et sont compatibles avec les versions antérieures du langage.

=== "Commentaire de ligne"

    ```c
    // This is a single line comment.
    ```

=== "Commentaire de bloc"

    ```c
    /* This is a
       Multi-line comment */
    ```

Il est important de rappeler que les commentaires sont traités par le préprocesseur, aussi ils n'influencent pas le fonctionnement d'un programme, mais seulement sa lecture. Rappelons qu'un code est plus souvent lu qu'écrit, car on ne l'écrit qu'une seule fois, mais comme tout développement doit être si possible **réutilisable**, il est plus probable qu'il soit lu par d'autres développeurs.

En conséquence, il est important de clarifier toute zone d'ombre lorsque l'on s'éloigne des consensus établis, ou lorsque le code seul n'est pas suffisant pour bien comprendre son fonctionnement.

D'une façon générale, les commentaires servent à expliquer **pourquoi** et non **comment**. Un bon programme devrait pouvoir se passer de commentaires, mais un programme sans commentaires n'est pas nécessairement un bon programme.

!!! note

    Il est préférable d'utiliser le commentaire de ligne dès que possible, car d'une part il y a moins de caractères à écrire, mais surtout les commentaires de blocs ne sont pas imbriquables (*nestable*).

    ```c
    /*
    // Autorisé
    */
    ```

    ```c
    /*
    /* Interdit */
    */
    ```

Les commentaires de blocs peuvent être utilisés pour documenter une fonction ou un bloc de code, mais également pour insérer un commentaire à l'intérieur d'une ligne:

```c
int deep_throught /* Name of the computer */ = 42; // The answer
```

### Commenter du code ?

Lorsque vous développez, vous avez souvent besoin de désactiver des portions de code pour des raisons de débogage ou de test. Il est tentant de commenter ces portions de code plutôt que de les supprimer. Néanmoins une règle à retenir est que l'on ne commente **jamais** des portions de code, et ce pour plusieurs raisons :

1. Les outils de *refactoring* ne pourront pas accéder du code commenté.
2. La syntaxe ne pourra plus être vérifiée par l'IDE.
3. Les outils de gestion de configuration (e.g. Git) devraient être utilisés à cette fin.

Si d'aventure vous souhaitez quand même exclure temporairement du code de la compilation, il est recommandé d'utiliser la directive de préprocesseur suivante, et n'oubliez pas d'expliquer pourquoi vous avez souhaité
désactiver cette portion de code.

```c
#if 0 // TODO: Check if divisor could still be null at this point.
if (divisor == 0) {
    return -1; // Error
}
#endif
```

### Quelques conseils

D'une manière générale l'utilisation des commentaires ne devrait pas être utilisée pour :

- désactiver temporairement une portion de code sans l'effacer ;
- expliquer le **comment** du fonctionnement du code ;
- faire dans le dithyrambique pompeux et notarial, des phrases à rallonge bien trop romanesques ;
- créer de jolies séparations telles que `#!c /*************************/`.

Il n'est pas rare de voir au début d'un fichier un commentaire de la forme suivante :

```c
/**
 * @brief Short description of the translation unit.
 *
 * @author John Doe <john@doe.com>
 * @date 2021-09-01
 * @file main.c
 *
 * Long description of the translation unit.
 *
 * NOTE: Important notes about this code
 * TODO: Things to fix...
 */
```

!!! note end "SSOT"

    Vous verrez souvent, trop souvent le nom de l'auteur et du fichiers dans les en-têtes. Ce n'est pas une bonne pratique si vous utilisez Git, car ces informations sont déjà présentes dans les métadonnées du fichier.

Voici un exemple de ce qu'il ne faut pas faire :

=== "Pas bien"

    ```c
    /*****************************************************
                                               _..._
     _   _    _    ____    _                .'     '.      _
    | \ | |  / \  / ___|  / \              /    .-""-\   _/ \
    |  \| | / _ \ \___ \ / _ \          .-|   /:.   |  |   |
    | |\  |/ ___ \ ___) / ___ \         |  \  |:.   /.-'-./
    |_| \_/_/   \_\____/_/   \_\        | .-'-;:__.'    =/
                                      .'=  *=|NASA _.='
                                     /   _.  |    ;
                                    ;-.-'|    \   |
                                   /   | \    _\  _\
                                   \__/'._;.  ==' ==\
                                            \    \   |
                                     jgs    /    /   /
                                            /-._/-._/
    National Aeronautics and Space          \   `\  \
    Administration.                          `-._/._/

    @file appolo11.c
    @brief Launch control module
    @author Margaret Hamilton
    @date 1969-07-16

    This module is responsible for the launch of the Apollo
    11 mission. It is a critical part of the mission and
    should not be modified.
    *******************************************************/
    ```

=== "Bien"

    ```c
    /**
     * Launch control module.
     *
     * This module is responsible for the launch of the Apollo
     * 11 mission. It is a critical part of the mission and
     * should not be modified.
     */
    ```

Le format des commentaires est par essence libre au développeur, mais il est généralement souhaité que : Les commentaires soient concis et précis et qu'ils soient écrits en anglais.

!!! exercise "Verbosité"

    Comment récririez-vous ce programme?

    ```c
    for (register unsigned int the_element_index = 0;
        the_element_index < number_of_elements; the_element_index += 1)
        array_of_elements[the_element_index] =  the_element_index;
    ```

    ??? solution

        Une règle de programmation: le nom identifieurs doit être proportionnel à leur contexte. Plus le contexte de la variable est réduit, plus le nom peut être court. Le même programme pourrait être écrit comme suit :

        ```c
        for (size_t i; i < nelems; i++)
            elem[i] = i;
        ```

        Un consensus assez bien établi est qu'une variable commençant par `n` peut signifier
        *number of*.
