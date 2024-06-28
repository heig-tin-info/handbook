# Généralités du langage

Ce chapitre traite des éléments constitutifs et fondamentaux du langage C. Il traite des généralités propres au langage, mais aussi des notions élémentaires permettant d'interpréter du code source.

Notons que ce chapitre est transversal, à la sa première lecture, le profane ne pourra tout comprendre sans savoir lu et maîtrisé les chapitres suivants, néanmoins il retrouvera ici les aspects fondamentaux du langage.

```{index} alphabet
```

## L'alphabet

```{index} Chiffres arabes
```

Fort heureusement pour nous occidentaux, l'alphabet de C est composé des 52 caractères latins et de 10 [chiffres indo-arabes](https://fr.wikipedia.org/wiki/Chiffres_arabes) :

```text
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
a b c d e f g h i j k l m n o p q r s t u v w x y z
0 1 2 3 4 5 6 7 8 9
```

La séparation des symboles est assurée par [une espace](<https://fr.wikipedia.org/wiki/Espace_(typographie)>), une tabulation horizontale, une tabulation verticale, et un caractère de retour à la ligne. Ces caractères ne sont pas imprimables, c'est-à-dire qu'ils ne sont pas directement visibles ni à l'écran ni à l'impression. Microsoft Word et d'autres éditeurs utilisent généralement le [pied-de-mouche](https://fr.wikipedia.org/wiki/Pied-de-mouche) `¶` pour indiquer les fins de paragraphes qui sont également des caractères non imprimables.

On nomme les caractères non imprimables soit par leur acronyme `LF` pour *Line Feed* ou soit par leur convention C échappée par un *backslash* `\n`:

```{index} LF, VT, FF, TAB, CR
```

```text
LF    \n   Line feed (retour à la ligne)
VT    \v   Vertical tab
FF    \f   New page
TAB   \t   Horizontal tab
CR    \r   Carriage return (retour charriot)
SPACE \040 Space
```

La ponctuation utilise les 29 symboles graphiques suivants :

```text
! # % ^ & * ( _ ) - + = ~ [ ] ' | \ ; : " { } , . < > / ?
```

```{index} trigraphes, digraphes
```

Un fait historique intéressant est que les premiers ordinateurs ne disposaient pas d'un clavier ayant tous ces symboles et la commission responsable de standardiser C a intégré au standard les **trigraphes** et plus tard les **digraphes** qui sont des combinaisons de caractères de base qui remplacent les caractères impossibles à saisir directement. Ainsi `<:` est le digraphe de `[` et `??<` est le trigraphe de `{`. Néanmoins vous conviendrez cher lecteur que ces alternatives ne devraient être utilisées que dans des cas extrêmes et justifiables.

Retenez que C peut être un langage extrêmement cryptique tant il est permissif sur sa syntaxe. Il existe d'ailleurs un concours international d'obfuscation, le [The International Obfuscated C Code Contest](https://www.ioccc.org/) qui prime des codes les plus subtils et illisibles comme le code suivant écrit par [Chris Mills](https://www.ioccc.org/2015/mills2). Il s'agit d'ailleurs d'un exemple qui compile parfaitement sur la plupart des compilateurs.

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

```{index} EOL
```

## Fin de lignes (EOL)

```{index} téléscripteurs
```

À l'instar des premières machines à écrire, les [téléscripteurs](https://fr.wikipedia.org/wiki/T%C3%A9l%C3%A9scripteur) possédaient de nombreux caractères de déplacement qui sont depuis tombés en désuétude et prêtent aujourd'hui à confusion même pour le plus aguerri des programmeurs. Maintenant que les ordinateurs possèdent des écrans, la notion originale du terme [retour chariot](https://fr.wikipedia.org/wiki/Retour_chariot) est compromise et comme il y a autant d'avis que d'ingénieurs, les premiers PC [IBM compatibles](https://fr.wikipedia.org/wiki/Compatible_PC) ont choisi qu'une nouvelle ligne dût toujours se composer de deux caractères: un retour chariot (`CR`) et une nouvelle ligne (`LF`) ou en C `\r\n`. Les premiers [Macintosh](https://fr.wikipedia.org/wiki/Macintosh) d'Apple jugeant inutile de gaspiller deux caractères pour chaque nouvelle ligne dans un fichier et ont décidé d'associer le retour chariot et la nouvelle ligne dans le caractère `\r`. Enfin, les ordinateurs UNIX ont eu le même raisonnement, mais ils ont choisi de ne garder que `\n`.

Fort heureusement depuis que Apple a migré son système sur une base [BSD](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution) (UNIX), il n'existe aujourd'hui plus que deux standards de retour à la ligne :

- `LF` ou `\n` sur les ordinateurs POSIX comme Linux, Unix ou macOS
- `CRLF` ou `\r\n` sur les ordinateurs Windows.

Il n'y a pas de consensus établi sur lesquels des deux types de fin de ligne (`EOL`: *End Of Line*) il faut utiliser, faite preuve de bon sens et surtout, soyez cohérent.

:::{figure} ../../assets/figures/dist/encoding/crlf.*
Distinction de différents caractères non imprimables
:::

## Mots clés

Le langage de programmation C tel que défini par C11 comporte environ 37 mots clés :

```{index} auto, do, goto, return, typedef, _Complex , break, double, if, short, union, _Imaginary , case, else, inline, signed, unsigned , char, enum, int, sizeof, void , const, extern, long, static, volatile , continue, float, register, struct, while , default, for, restrict, switch, _Bool
```

```{eval-rst}
.. hlist::
    :columns: 4

    - ``_Bool``
    - ``_Complex``
    - ``_Imaginary``
    - ``auto``
    - ``break``
    - ``case``
    - ``char``
    - ``const``
    - ``continue``
    - ``default``
    - ``do``
    - ``double``
    - ``else``
    - ``enum``
    - ``extern``
    - ``float``
    - ``for``
    - ``goto``
    - ``if``
    - ``inline``
    - ``int``
    - ``long``
    - ``register``
    - ``restrict``
    - ``return``
    - ``short``
    - ``signed``
    - ``sizeof``
    - ``static``
    - ``struct``
    - ``switch``
    - ``typedef``
    - ``union``
    - ``unsigned``
    - ``void``
    - ``volatile``
    - ``while``
```

Dans ce cours l'usage des mots clés suivants est découragé, car leur utilisation pourrait prêter à confusion ou mener à des inélégances d'écriture.

```{eval-rst}
.. hlist::
    :columns: 4

    - ``_Bool``
    - ``_imaginary``
    - ``auto``
    - ``goto``
    - ``inline``
    - ``long``
    - ``register``
    - ``restrict``
    - ``short``

```

Notons que les mots clés `true` et `false` décrits à la {numref}`booleans` ne sont pas standardisés en C, mais ils le sont en C++.

(identifiers)=

## Identificateurs

```{index} identificateur
```

Un identificateur est une séquence de caractères représentant une entité du programme et à laquelle il est possible de se référer. Un identificateur est défini par :

:::{figure} ../../assets/figures/dist/grammar/identifier.*
Grammaire d'un identificateur C
:::

En addition de ceci, voici quelques règles :

```{index} casse
```

- Un identificateur ne peut pas être l'un des mots clés du langage.
- Les identificateurs sont sensibles à la [casse](<https://fr.wikipedia.org/wiki/Casse_(typographie)>).
- Le standard C99, se réserve l'usage de tous les identificateurs débutant par `_` suivi d'une lettre majuscule ou un autre *underscore* `_`.
- Le standard [POSIX](https://fr.wikipedia.org/wiki/POSIX), se réserve l'usage de tous les identificateurs finissant par `_t`.

:::{hint}
Expression régulière

Il est possible d'exprimer la syntaxe d'un identificateur à l'aide de l'expression régulière suivante :

```text
^[a-zA-Z_][a-zA-Z0-9_]*$
```
:::

```{eval-rst}
.. exercise:: Validité des identificateurs

    Pour chacune des suites de caractères ci-dessous, indiquez s'il s'agit d'un identificateur valide et utilisable en C. Justifier votre réponse.

    .. hlist::
        :columns: 2

        #. ``2_pi``
        #. ``x_2``
        #. ``x___3``
        #. ``x 2``
        #. ``positionRobot``
        #. ``piece_presente``
        #. ``_commande_vanne``
        #. ``-courant_sortie``
        #. ``_alarme_``
        #. ``panne#2``
        #. ``int``
        #. ``défaillance``
        #. ``f'``
        #. ``INT``

    .. solution::

        Une excellente approche serait d'utiliser directement l'expression régulière fournie et d'utiliser l'outil en ligne `regex101.com <https://regex101.com/r/cmxaic/1>`__.

        .. hlist::
            :columns: 2

            #. ``2_pi`` **invalide**, car commence par un chiffre
            #. ``x_2`` **valide**
            #. ``x___3`` **valide**
            #. ``x 2`` **invalide**, car comporte un espace
            #. ``positionRobot`` **valide**, notation *camelCase*
            #. ``piece_presente`` **valide**, notation *snake_case*
            #. ``_commande_vanne`` **valide**
            #. ``-courant_sortie`` **invalide**, un identificateur ne peut pas commencer par le signe ``-``
            #. ``_alarme_`` **valide**
            #. ``panne#2`` **invalide**, le caractère ``#`` n'est pas autorisé
            #. ``int`` **invalide**, ``int`` est un mot réservé du langage
            #. ``défaillance`` **invalide**, uniquement les caractères imprimable ASCII sont autorisés
            #. ``f'`` **invalide** l'apostrophe n'est pas autorisée
            #. ``INT`` **valide**
```

```{index} variable
```

## Variables

Une variable est un symbole qui associe un nom **identificateur** à une **valeur**. Comme son nom l'indique, une variable peut voir son contenu varier au cours du temps.

Une variable est définie par :

```{index} visibilité, type, valeur, portée
```

- Son **nom** (*name*), c'est-à-dire l'identificateur associé au symbole.
- Son **type** (*type*), qui est la convention d'interprétation du contenu binaire en mémoire.
- Sa **valeur** (*value*), qui est le contenu interprété connaissant son type.
- Son **adresse** (*address*) qui est l'emplacement mémoire ou la représentation binaire sera enregistrée
- Sa **portée** (*scope*) qui est la portion de code ou le symbole est défini et accessible.
- Sa **visibilité** (*visibility*) qui ne peut être que *public* en C.

```{index} déclaration
```

### Déclaration

Avant de pouvoir être utilisée, une variable doit être déclarée afin que le compilateur puisse réserver un emplacement en mémoire pour stocker sa valeur. Voici quelques déclarations valides en C :

```c
char c = '€';
int temperature = 37;
float neptune_stone_height = 376.86;
char message[] = "Jarvis, il faut parfois savoir "
    "courir avant de savoir marcher.";
```

Il n'est pas nécessaire d'associer une valeur initiale à une variable, une déclaration peut se faire sans initialisation comme montré dans l'exemple suivant dans lequel on réserver trois variables `i`, `j`, `k`.

```c
int i, j, k;
```

```{eval-rst}
.. exercise:: Affectation de variables

    Considérons les déclarations suivantes :

    .. code-block:: c

        int a, b, c;
        float x;

    Notez après chaque affectation, le contenu des différentes variables :

    =====  ================  =====  =====  =====  =====
    Ligne  Instruction       ``a``  ``b``  ``c``  ``x``
    =====  ================  =====  =====  =====  =====
    1      ``a = 5;``
    2      ``b = c;``
    3      ``c = a;``
    4      ``a = a + 1;``
    5      ``x = a - ++c;``
    6      ``b = c = x;``
    7      ``x + 2. = 7.;``
    =====  ================  =====  =====  =====  =====

    .. solution::

        =====  ================  =====  =====  =====  =====
        Ligne  Instruction       ``a``  ``b``  ``c``  ``x``
        =====  ================  =====  =====  =====  =====
        1      ``a = 5;``            5      ?      ?      ?
        2      ``b = c;``            5      ?      ?      ?
        3      ``c = a;``            5      ?      5      ?
        4      ``a = a + 1;``        6      ?      5      ?
        5      ``x = a - ++c;``      6      ?      6     12
        6      ``b = c = x;``        6     12     12     12
        7      ``x + 2. = 7.;``      -      -      -      -
        =====  ================  =====  =====  =====  =====
```

### Convention de nommage

Il existe autant de conventions de nommage qu'il y a de développeurs, mais un consensus majoritaire, que l'on retrouve dans d'autres langages de programmation exprime que :

- La longueur du nom d'une variable est généralement proportionnelle à sa portée et donc il est d'autant plus court que l'utilisation d'une variable est localisée.
- Le nom doit être concis et précis et ne pas laisser place à une quelconque ambiguïté.
- Le nom doit participer à l'autodocumentation du code et permettre à un lecteur de comprendre facilement le programme qu'il lit.

Selon les standards adoptés chaque société on trouve ceux qui préfèrent nommer les variables en utilisant un *underscore* (`_`) comme séparateur et ceux qui préfèrent nommer une variable en utilisant des majuscules comme séparateurs de mots.

```{eval-rst}
.. table:: Conventions de nommage

    +--------------+------------------+----------------------+
    | Convention   | Nom français     | Exemple              |
    +==============+==================+======================+
    | *camelcase*  | Casse de chameau | ``userLoginCount``   |
    +--------------+------------------+----------------------+
    | *snakecase*  | Casse de serpent | ``user_login_count`` |
    +--------------+------------------+----------------------+
    | *pascalcase* | Casse de Pascal  | ``UserLoginCount``   |
    +--------------+------------------+----------------------+
    | *kebabcase*  | Casse de kebab   | ``user-login-count`` |
    +--------------+------------------+----------------------+
```

### Variable métasyntaxiques

Souvent lors d'exemples donnés en programmation on utilise des variables génériques dites [métasyntaxiques](https://fr.wikipedia.org/wiki/Variable_m%C3%A9tasyntaxique). En français les valeurs `toto`, `titi`, `tata` et `tutu` sont régulièrement utilisées tandis qu'en anglais
`foo`, `bar`, `baz` et `qux` sont régulièrement utilisés. Les valeurs `spam`, `ham` et `eggs` sont quant à elles souvent utilisée en Python, en référence au sketch [Spam](<https://en.wikipedia.org/wiki/Spam_(Monty_Python)>) des Monthy Python.

Leur usage est conseillé pour appuyer le cadre générique d'un exemple sans lui donner la consonance d'un problème plus spécifique.

On trouvera une [table](http://www.catb.org/jargon/html/M/metasyntactic-variable.html) des différents noms les plus courants utilisés dans différentes langues.

## Les constantes

Une constante par opposition à une variable voit son contenu fixe et immuable.

Formellement, une constante se déclare comme une variable, mais préfixée du mot-clé `const`.

```c
const double scale_factor = 12.67;
```

:::{note}
Il ne faut pas confondre la **constante** qui est une variable immuable, stockée en mémoire et une **macro** qui appartient au préprocesseur. Le fichier d'en-tête `math.h` définit par exemple la constante `M_PI` sous forme de macro.

```c
#define M_PI 3.14159265358979323846
```
:::

## Constantes littérales

Les constantes littérales représentent des grandeurs scalaires numériques ou de caractères et initialisées lors de la phase de compilation.

```c
6      // Grandeur valant le nombre d'heures sur l'horloge du Palais du Quirinal à Rome
12u    // Grandeur non signée
6l     // Grandeur entière signée codée sur un entier long
42ul   // Grandeur entière non signée codée sur un entier long
010    // Grandeur octale valant 8 en décimal
0xa    // Grandeur hexadécimale valant 10 en décimal
0b111  // Grandeur binaire valant 7 en décimal
33.    // Grandeur réelle exprimée en virgule flottante
'0'    // Grandeur caractère valant 48 en décimal
```

```{eval-rst}
.. exercise:: Constances littérales

    Pour les entrées suivantes, indiquez lesquelles sont correctes.

    .. hlist::
        :columns: 2

        #. ``12.3``
        #. ``12E03``
        #. ``12u``
        #. ``12.0u``
        #. ``1L``
        #. ``1.0L``
        #. ``.9``
        #. ``9.``
        #. ``.``
        #. ``0x33``
        #. ``0xefg``
        #. ``0xef``
        #. ``0xeF``
        #. ``0x0.2``
        #. ``09``
        #. ``02``
```

## Opérateur d'affectation

Dans les exemples ci-dessus, on utilise l'opérateur d'affectation pour associer une valeur à une variable.

Historiquement, et fort malheureusement, le symbole choisi pour cet opérateur est le signe égal `=` or, l'égalité est une notion mathématique qui n'est en aucun cas reliée à l'affectation.

Pour mieux saisir la nuance, considérons le programme suivant :

```c
a = 42;
a = b;
```

Mathématiquement, la valeur de `b` devrait être égale à 42 ce qui n'est pas le cas en C où il faut lire, séquentiellement l'exécution du code, car oui, C est un langage impératif (c.f. {numref}`paradigms`). Ainsi, dans l'ordre on lit :

1. J'assigne la valeur 42 à la variable symbolisée par `a`
2. Puis, j'assigne la valeur de la variable `b` au contenu de `a`.

Comme on ne connaît pas la valeur de `b`, avec cet exemple, on ne peut pas connaître la valeur de `a`.

Certains langages de programmation ont été sensibilisés à l'importance de cette distinction et dans les langages **F#**, **OCaml**, **R** ou **S**, l'opérateur d'affectation est `<-` et une affectation pourrait s'écrire par exemple: `a <- 42` ou `42 -> a`.

En C, l'opérateur d'égalité que nous verrons plus loin s'écrit `==` (deux `=` concaténés).

Remarquez ici que l'opérateur d'affectation de C agit toujours de droite à gauche c'est-à-dire que la valeur à **droite** de l'opérateur est affectée à la variable située à **gauche** de l'opérateur.

S'agissant d'un opérateur il est possible de chaîner les opérations, comme on le ferait avec l'opérateur `+` et dans l'exemple suivant il faut lire que `42` est assigné à `c`, que la valeur de `c` est ensuite assigné à `b` et enfin la valeur de `b` est assignée à `a`.

```c
a = b = c = 42;
```

Nous verrons {numref}`precedence` que l'associativité de chaque opérateur détermine s'il agit de gauche à droite ou de droite à gauche.

```{eval-rst}
.. exercise:: Affectations simples

    Donnez les valeurs de ``x``, ``n``, ``p`` après l'exécution des instructions ci-dessous :

    .. code-block:: c

        float x;
        int n, p;

        p = 2;
        x = 15 / p;
        n = x + 0.5;

    .. solution::

        .. code-block:: text

            p ≡ 2
            x ≡ 7
            n ≡ 7
```

```{eval-rst}
.. exercise:: Trop d'égalités

    On considère les déclarations suivantes :

    .. code-block:: c

        int i, j, k;

    Donnez les valeurs des variables ``i``, ``j`` et ``k`` après l'exécution de chacune des expressions ci-dessous. Qu'en pensez-vous ?

    .. code-block:: c

        /* 1 */ i = (k = 2) + (j = 3);
        /* 2 */ i = (k = 2) + (j = 2) + j * 3 + k * 4;
        /* 3 */ i = (i = 3) + (k = 2) + (j = i + 1) + (k = j + 2) + (j = k - 1);

    .. solution::

        Selon la table de priorité des opérateurs, on note :

        - ``()`` priorité 1 associativité à droite
        - ``*`` priorité 3 associativité à gauche
        - ``+`` priorité 4 associativité à droite
        - ``=`` priorité 14 associativité à gauche

        En revanche rien n'est dit sur les `point de séquences <https://en.wikipedia.org/wiki/Sequence_point>`__. L'opérateur d'affectation n'est pas un point de séquence, autrement dit le standard C99 (Annexe C) ne définit pas l'ordre dans lequel les assignations sont effectuées.

        Ainsi, seul le premier point possède une solution, les deux autres sont indéterminés

        #. ``i = (k = 2) + (j = 3)``

            - ``i = 5``
            - ``j = 3``
            - ``k = 2``
        #. ``i = (k = 2) + (j = 2) + j * 3 + k * 4``

            - Résultat indéterminé
        #. ``i = (i = 3) + (k = 2) + (j = i + 1) + (k = j + 2) + (j = k - 1)``

            - Résultat indéterminé

```

## Commentaires

Comme en français et ainsi qu'illustré par la {numref}`proust`, il est possible d'annoter un programme avec des **commentaires**. Les commentaires n'ont pas d'incidence sur le fonctionnement d'un programme et ne peuvent être lu que par le développeur qui possède le code source.

(proust)=

:::{figure} ../../assets/images/proust.*
Les carafes dans la Vivonne
:::

Il existe deux manière d'écrire un commentaire en C :

- Les commentaires de lignes (depuis C99)

  ```c
  // This is a single line comment.
  ```

- Les commentaires de blocs

  ```c
  /* This is a
     Multi-line comment */
  ```

Les commentaires sont parsés par le préprocesseur, aussi ils n'influencent pas le fonctionnement d'un programme, mais seulement sa lecture. Rappelons qu'un code est plus souvent lu qu'écrit, car on ne l'écrit qu'une seule fois, mais comme tout développement doit être si possible **réutilisable**,
il est plus probable qu'il soit lu part d'autres développeurs.

En conséquence, il est important de clarifier toute zone d'ombre lorsque l'on s'éloigne des consensus établis, ou lorsque le code seul n'est pas suffisant pour bien comprendre son fonctionnement.

D'une façon générale, les commentaires servent à expliquer **pourquoi** et non **comment**. Un bon programme devrait pouvoir se passer de commentaires, mais un programme sans commentaires n'est pas
nécessairement un bon programme.

Notons que l'on ne commente jamais des portions de code, et ce pour plusieurs raisons :

1. Les outils de *refactoring* ne pourront pas accéder du code commenté
2. La syntaxe ne pourra plus être vérifiée par l'IDE
3. Les outils de gestion de configuration (e.g. Git) devraient être utilisés à cette fin

Si d'aventure vous souhaitez exclure temporairement du code de la compilation, utilisez la directive de préprocesseur suivante, et n'oubliez pas d'expliquer pourquoi vous avez souhaité
désactiver cette portion de code.

```c
#if 0 // TODO: Check if divisor could still be null at this point.
if (divisor == 0) {
    return -1; // Error
}
#endif
```

D'une manière générale l'utilisation des commentaires ne devrait pas être utilisée pour :

- Désactiver temporairement une portion de code sans l'effacer.
- Expliquer le **comment** du fonctionnement du code.
- Faire dans le dithyrambique pompeux et notarial, des phrases à rallonge bien trop romanesques.
- Créer de jolies séparations telles que `/*************************/`.

Exemple d'entête de fichier :

```c
/**
 * Short description of the translation unit.
 *
 * Author: John Doe <john@doe.com>
 *
 * Long description of the translation unit.
 *
 * NOTE: Important notes about this code
 */
```

Le format des commentaires est par essence libre au développeur, mais il est généralement souhaité que :

- Les commentaires soient concis et précis.
- Les commentaires soient écrits en anglais.

```{eval-rst}
.. exercise:: Verbosité

    Comment récririez-vous ce programme?

    .. code-block:: c

        for (register unsigned int the_element_index = 0; the_element_index < number_of_elements; the_element_index += 1)
            array_of_elements[the_element_index] =  the_element_index;

    .. solution::

        Une règle de programmation: le nom identifieurs doit être proportionnel à leur contexte. Plus le contexte de la variable est réduit, plus le nom peut être court. Le même programme pourrait être écrit comme suit :

        .. code-block:: c

            for (size_t i; i < nelems; i++)
                elem[i] = i;

        Un consensus assez bien établi est qu'une variable commençant par ``n`` peut signifier
        *number of*.
```
