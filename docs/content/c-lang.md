# Langage C

Le langage C est un des premiers langages de programmation de haut niveau. Il est très proche de l'assembleur, le langage de bas niveau des processeurs, et permet de programmer des applications très performantes. Il est utilisé dans de nombreux domaines de l'informatique, de l'embarqué à la programmation système en passant par les applications de bureau.

Même s'il est très ancien, il continue d'être utilisé et enseigné, car il est très efficace et permet de comprendre les bases de la programmation.

## Historique { data-search-keyword="thompson"}

Le langage de programmation **C** est la suite naturelle du langage **B** créé dans la toute fin des années soixante par un grand pionnier de l'informatique moderne: [Ken Thompson](https://fr.wikipedia.org/wiki/Ken_Thompson).

Le langage C a été inventé en 1972 par [Brian Kernighan](https://fr.wikipedia.org/wiki/Brian_Kernighan) et [Dennis Ritchie](https://fr.wikipedia.org/wiki/Dennis_Ritchie). Ils sont aussi les concepteurs du système d'exploitation [UNIX](https://fr.wikipedia.org/wiki/Unix) et ont créé ce nouveau langage pour faciliter leurs travaux de développement logiciel. La saga continue avec [Bjarne Stroustrup](https://fr.wikipedia.org/wiki/Bjarne_Stroustrup) qui décide d'étendre C en apportant une saveur nouvelle: la programmation orientée objet (OOP), qui fera l'objet d'un cours à part entière. Ce C amélioré voit le jour en 1985.

Il faut attendre 1989 pour que le langage C fasse l'objet d'une normalisation par l'ANSI (*American National Standards Institute*). L'année suivante le comité ISO (*International Organization for Standardization*) ratifie le standard *ISO/IEC 9899:1990* communément appelé **C90**. Dès lors, le langage C est devenu un standard international et devient le langage dominant dans le monde de l'informatique.

Les années se succèdent et le standard évolue pour soit corriger certaines de ses faiblesses soit pour apporter de nouvelles fonctionnalités.

Cinquante ans plus tard, C est toujours l'un des langages de programmation les plus utilisés par les ingénieurs, car il allie une bonne vision de haut niveau tout en permettant des manipulations de très bas niveau, de fait il est un langage de choix pour les applications embarquées à microcontrôleurs, ou lorsque l'optimisation du code est nécessaire pour obtenir de bonnes performances tels que les noyaux des systèmes d'exploitation comme le noyau Linux (Kernel) ou le noyau Windows.

Il faut retenir que **C** est un langage simple et efficace. Votre machine à café, votre voiture, vos écouteurs Bluetooth ont très probablement été programmés en C.

![Les pères fondateurs du C](../assets/images/thompson-kernighan-ritchie.webp)

## Standardisation

Le langage C possède un grand historique, et il a fallu attendre près de 20 ans après sa création pour voir apparaître la première standardisation internationale.

Le standard le plus couramment utilisé en 2024 est encore [C99](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf). C11 le remplace peu à peu dans l'industrie mais la saga continue avec C17, C18 et C23 qui sont des évolutions.

Table: Normes internationales du language C

| Notation courte | Standard international                                       | Date |
| --------------- | ------------------------------------------------------------ | ---- |
| C               | n/a                                                          | 1972 |
| K&R C           | n/a                                                          | 1978 |
| C89 (ANSI C)    | ANSI X3.159-1989                                             | 1989 |
| C90             | [ISO/IEC 9899:1990](https://www.iso.org/standard/17782.html) | 1990 |
| C99             | [ISO/IEC 9899:1999](https://www.iso.org/standard/29237.html) | 1999 |
| C11             | [ISO/IEC 9899:2011](https://www.iso.org/standard/57853.html) | 2011 |
| C17/C18         | [ISO/IEC 9899:2018](https://www.iso.org/standard/74528.html) | 2018 |
| C23             | [ISO/IEC 9899:2023](https://www.iso.org/standard/82075.html) | 2023 |

En substance, **C18** n'apporte pas de nouvelles fonctionnalités au langage, mais vise à clarifier de nombreuses zones d'ombres laissées par **C11**.

**C11** apporte peu de grands changements fondamentaux pour le développement sur microcontrôleur.

!!! info

    Vous entendrez ou lirez souvent des références à **ANSI C** ou **K&R**, préférez plutôt une compatibilité avec **C99** au minimum.

Le standard est lourd, difficile à lire et avec 552 pages pour **C99**, vous n'aurez probablement jamais le moindre plaisir à y plonger les yeux qui se rempliront de larmes à chaque lecture.

Armez-vous de mouchoirs car l'investissement est pourtant parfois nécessaire pour comprendre certaines subtilités du langage qui sont rarement expliquées dans les livres. Pourquoi diable écrire un livre qui détaille l'implémentation C alors qu'il existe déjà ?

Vous vous demandez probablement pourquoi l'industrie a-t-elle autant de retard sur le dernier standard. Lorsque qu'Apple annonce sa dernière mouture d'iOS, chacun s'empresse de l'installer. En revanche, dans le milieu industriel, les machines et les processus sont réglées par des validations strictes qui décrivent les standards utilisés. Migrer vers un standard plus récent est une aventure. Il faut mettre à jour le code, faire des tests, encore et tests, et toujours plus de tests pour s'assurer que la fusée qu'on enverra sur Mars n'aura pas d'issue fatale. Ces validations sont longues et fastidieuses autant administrativement que techniquement. Ce qui est long est cher et bien souvent, les entreprises préfèrent rester fidèle à un ancien standard.

!!! exercise

    Ouvrez le standard [C99](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf) et cherchez la valeur maximale possible de la constante `ULLONG_MAX`. Que vaut-elle ?

    ??? solution

        Au paragraphe §5.2.4.2.1-1 on peut lire que `ULLONG_MAX` est encodé sur 64-bits et donc que sa valeur est $2^{64}-1$ donc `18'446'744'073'709'551'615`.

## Le C et les autres langages de programmation

Si ce cours ce concentre sur le C, ce n'est pas le seul langage de programmation et surtout ce n'est certainement pas le seul que vous apprendrez.

| Langage de programmation | Année | Utilisation               |
| ------------------------ | ----- | ------------------------- |
| Fortran                  | 1957  | Calcul scientifique       |
| Lisp                     | 1958  | Intelligence artificielle |
| Cobol                    | 1959  | Finance, banque           |
| Basic                    | 1964  | Enseignement              |
| Pascal                   | 1970  | Enseignement              |
| C                        | 1972  | Systèmes embarqués        |
| C++                      | 1985  | Applications lourdes      |
| Perl                     | 1987  | Scripts                   |
| Python                   | 1991  | Ingénierie, sciences      |
| Ruby                     | 1995  | Scripts, Web              |
| Java                     | 1995  | Applications lourdes      |
| PHP                      | 1995  | Web                       |
| C#                       | 2000  | Applications graphiques   |
| Go                       | 2009  | Systèmes distribués       |
| Rust                     | 2010  | Systèmes embarqués        |
| Swift                    | 2014  | Applications mobiles      |
| Zig                      | 2016  | Systèmes embarqués        |

L'index [TIOBE](https://www.tiobe.com/tiobe-index/) est un bon indicateur de la popularité des langages de programmation. Il est mis à jour chaque mois et permet de suivre l'évolution de la popularité des langages de programmation.

En 2024, le top 10 des langages de programmation les plus populaires est le suivant :

1. Python
2. C++
3. C
4. Java
5. C#
6. JavaScript
7. Go
8. SQL
9. Visual Basic
10. Fortran

Python est un langage de très haut niveau, simple a apprendre mais éloigné du matériel. C++ est un langage de programmation orientée objet, très puissant, mais complexe à apprendre. C est un excellent compromis entre les deux, il est simple, mais permet de comprendre les bases de la programmation et de la manipulation du matériel. C'est pour cela que ce cours est basé sur le langage C.

## Environnement de développement

Un développeur logiciel passe son temps devant son écran à étudier, et écrire du code et bien qu'il pourrait utiliser un éditeur de texte tel que Microsoft Word ou Notepad, il préfèrera des outils apportant davantage d'interactivité et d'aide au développement. Les éditeurs de texte orienté programmation disposent d'outils puissances de complétion automatique de code et de coloration syntaxique. La touche `Tab` devient alors un allié précieux pour écrire du code rapidement.

Un autre composant essentiel de l'environnement de développement est le **compilateur**. Il s'agit généralement d'un ensemble de programmes qui permettent de convertir le **code** écrit en un programme exécutable. Ce programme peut-être par la suite intégré dans un *smartphone*, dans un système embarqué sur un satellite, sur des cartes de prototypage comme un Raspberry PI, ou encore sur un ordinateur personnel.

L'ensemble des outils nécessaire à créer un produit logiciel est appelé chaîne de compilation, plus communément appelée **toolchain**.

Un environnement de développement intégré, ou [IDE](https://fr.wikipedia.org/wiki/Environnement_de_d%C3%A9veloppement) pour *Integrated development environment* comporte généralement un éditeur de code ainsi que la [toolchain](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_compilation) associée.

![Représentation graphique des notions de compilateur, IDE, toolchain...](../assets/images/toolchain.drawio)

À titre d'exemple on peut citer quelques outils bien connus des développeurs. Choisissez celui que vous pensez être le plus adapté à vos besoins, consultez l'internet, trouvez votre optimal :

[Microsoft Visual Studio](https://visualstudio.microsoft.com/)

: Un **IDE** très puissant disponible sous Microsoft Windows exclusivement. Il supporte de nombreux langages de programmation comme C, C++, C# ou Python.


[Code::Blocks](http://www.codeblocks.org/)

: Un **IDE** libre et multi-plate-forme pour C et C++, une solution simple pour développer rapidement.


[Visual Studio Code](https://code.visualstudio.com/)

: Un **éditeur de code** *open-source* multi-plates-formes disponible sur Windows, macOS et Linux. Souvent abrégé *VsCode*.


[GCC](https://gcc.gnu.org/)

: Un **compilateur** *open-source* utilisé sous Linux et macOS.

[CLANG](https://clang.llvm.org/)

: Un **compilateur** *open-source* gagnant en popularité, une alternative à GCC.


[Vim](https://www.vim.org/)

: Un **éditeur de code** *open-source* multi-usage à la courbe d'apprentissage très raide et installé par défaut sur la plupart des distributions Unix/Linux. Il est l'évolution de *ed*, puis *ex* puis *vi* puis *vim*.


[Ed](<https://en.wikipedia.org/wiki/Ed_(text_editor)>)

: Prononcé "hidi", il s'agit du tout premier éditeur de texte développé en 1969 faisant partie des trois premiers éléments du système UNIX: l'assembleur, l'éditeur et le *shell*. Il n'est pas interactif, il n'a pas de coloration syntaxique, il est absolument obscur dans son fonctionnement, mais bientôt 50 ans après, il fait toujours partie de la norme POSIX et donc disponible sur tout système compatible. Bref, ne l'utilisez pas...

Le résultat de l'étude annuelle de [Stackoverflow](https://survey.stackoverflow.co/2023/#overview) donne une idée de la popularité des éditeurs et IDE les plus utilisés par les développeurs :

1. Visual Studio Code (73.3%)
2. Visual Studio (28.4%)
3. IntelliJ IDEA (26.8%)
4. Notepad++ (24.5%)
5. Vim (22.3%)

!!! exercise Eclipse

    Un ami vous parle d'un outil utilisé pour le développement logiciel nommé **Eclipse**. De quel type d'outil s'agit-il ?

    ??? solution

        [Eclipse](https://www.eclipse.org/ide/) est un IDE. Il n'intègre donc pas de chaîne de compilation et donc aucun compilateur.

??? exercise

    Combien y a-t-il eu de questions posées en C sur le site Stack Overflow?

    ??? solution

        Il suffit pour cela de se rendre sur le site de `Stackoverflow <https://stackoverflow.com/tags/c>`__ et d'accéder à la liste des tags. En 2019/07 il y eut 307'669 questions posées.

        Seriez-vous capable de répondre à une question posée?

## Programmation texte structurée

Le C comme la plupart des langages de programmation utilise du texte structuré, c'est-à-dire que le langage peut être défini par un **vocabulaire**, une **grammaire** et se compose d'un **alphabet**.

À l'inverse des [langages naturels](https://en.wikipedia.org/wiki/Natural_language) comme le Français, un langage de programmation est un [langage formel](https://fr.wikipedia.org/wiki/Langage_formel) et se veut exact dans sa grammaire et son vocabulaire, il n'y a pas de cas particuliers ni d'ambiguïtés possibles dans l'écriture.

Les **compilateurs** sont ainsi construits autour d'une grammaire du langage qui est réduite au minimum par souci d'économie de mémoire, pour taire les ambiguïtés et accroître la productivité du développeur.

L'exemple suivant est un [pseudo-code](https://fr.wikipedia.org/wiki/Pseudo-code) utilisant une grammaire simple :

```text
POUR CHAQUE oeuf DANS le panier :
    jaune, blanc 🠔 CASSER(oeuf)
    omelette 🠔 MELANGER(jaune, blanc)
    omelette_cuite 🠔 CUIRE(omelette)

SERVIR(omelette_cuite)
```

La structure de la phrase permettant de traiter tous les éléments d'un ensemble d'éléments peut alors s'écrire :

```text
POUR CHAQUE <> DANS <>:
    <>
```

Où les `<>` sont des marques substitutives ([placeholder](https://fr.wikipedia.org/wiki/Marque_substitutive)) qui seront remplacées par le développeur par ce qui convient.

Les grammaires des langages de programmation sont souvent formalisées à l'aide d'un métalangage, c'est-à-dire un langage qui permet de décrire un langage. La grammaire du langage C utilisé dans ce cours peut ainsi s'exprimer en utilisant la forme Backus-Naur ou **BNF** disponible en annexe.

## Les paradigmes de programmation

Chaque langage de programmation que ce soit C, C++, Python, ADA, COBOL et Lisp sont d'une manière générale assez proche les uns des autres. Nous citions par exemple le langage B, précurseur du C (c.f. {numref}`thompson`). Ces deux langages, et bien que leurs syntaxes soient différentes, ils demeurent assez proches, comme l'espagnol et l'italien qui partagent des racines latines. En programmation on dit que ces langages partagent le même [paradigme de programmation](<https://fr.wikipedia.org/wiki/Paradigme_(programmation)>).

Certains paradigmes sont plus adaptés que d'autres à la résolution de certains problèmes et de nombreux langages de programmation sont dit **multi-paradigmes**, c'est-à-dire qu'ils supportent différents paradigmes.

Nous citions plus haut le C++ qui permet la programmation orientée objet, laquelle est un paradigme de programmation qui n'existe pas en C.

Ce qu'il est essentiel de retenir c'est qu'un langage de programmation peut aisément être substitué par un autre pour autant qu'ils s'appuient sur les mêmes paradigmes.

Le langage C répond aux paradigmes suivants :

- [Impératif](https://fr.wikipedia.org/wiki/Programmation_imp%C3%A9rative): programmation en séquences de commandes
- [Structuré](https://fr.wikipedia.org/wiki/Programmation_structur%C3%A9e): programmation impérative avec des structures de contrôle imbriquées
- [Procédural](https://fr.wikipedia.org/wiki/Programmation_proc%C3%A9durale): programmation impérative avec appels de procédures

Le C++ quant à lui apporte les paradigmes suivants à C :

- [Fonctionnel](https://fr.wikipedia.org/wiki/Programmation_fonctionnelle)
- [Orienté objet](https://fr.wikipedia.org/wiki/Programmation_orient%C3%A9e_objet)

Des langages de plus haut niveau comme Python ou C# apportent davantage de paradigmes comme la [programmation réflective](<https://fr.wikipedia.org/wiki/R%C3%A9flexion_(informatique)>).


## Cycle de développement

Le cycle de développement logiciel comprend la suite des étapes menant de l'étude et l'analyse d'un problème jusqu'à la réalisation d'un programme informatique exécutable. Dans l'industrie, il existe de nombreux modèles comme le [Cycle en V](https://fr.wikipedia.org/wiki/Cycle_en_V) ou le [modèle en cascade](https://fr.wikipedia.org/wiki/Mod%C3%A8le_en_cascade). Quel que soit le modèle utilisé, il comprendra les étapes suivantes :

1. **Étude** et analyse du problème
2. Écriture d'un **cahier des charges** (spécifications)
3. Écriture de **tests** à réaliser pour tester le fonctionnement du programme
4. **Conception** d'un algorithme
5. **Transcription** de cet algorithme en utilisant le langage C
6. **Compilation** du code et génération d'un exécutable
7. **Test** de fonctionnement
8. **Vérification** que le cahier des charges est respecté
9. **Livraison** du programme

Mis à part la dernière étape où il n'y a pas de retour en arrière possible, les autres étapes sont **itératives**. Il est très rare d'écrire un programme juste du premier coup. Durant tout le cycle de développement logiciel, des itérations successives sont faites pour permettre d'optimiser le programme, de résoudre des bogues, d'affiner les spécifications, d'écrire davantage de tests pour renforcer l'assurance d'un bon fonctionnement du programme et éviter une coulée de lave [](){#code_smell}.

Le modèle en cascade suivant résume le cycle de développement d'un programme. Il s'agit d'un modèle simple, mais qu'il faut garder à l'esprit que ce soit pour le développement d'un produit logiciel que durant les travaux pratiques liés à ce cours.

![Modèle en cascade](../assets/images/waterfall.drawio)

## Cycle de compilation

Le langage C à une particularité que d'autres langages n'ont pas, c'est-à-dire qu'il comporte une double grammaire. Le processus de compilation s'effectue donc en deux passes.

1. Préprocesseur
2. Compilation du code

Vient ensuite la phase d'édition des liens ou *linkage* lors de laquelle l'exécutable binaire est créé.

![Cycle de compilation illustré](../assets/images/build-cycle.drawio)

Voyons plus en détail chacune de ces étapes.

### Préprocesseur (*pre-processing*)

La phase de *preprocessing* permet de générer un fichier intermédiaire en langage C dans lequel toutes les instructions nécessaires à la phase suivante sont présentes. Le *preprocessing* réalise :

- Le remplacement des définitions par leurs valeurs (`#define`),
- Le remplacement des fichiers inclus par leurs contenus (`#include`),
- La conservation ou la suppression des zones de compilation conditionnelles (`#if/#ifdef/#elif/#else/#endif`).
- La suppression des commentaires (`/* ... */`, `// ...`)

Avec `gcc` il est possible de demander que l'exécution du préprocesseur en utilisant l'option `-E`.

![Processus de prépressing](../assets/images/preprocessing.drawio)

### Compilation (*build*)

La phase de compilation consiste en une analyse syntaxique du fichier à compiler puis en sa traduction en langage assembleur pour le processeur cible. Le fichier généré est un fichier binaire (extension `.o` ou `.obj`) qui sera utilisé pour la phase suivante. Lors de la *compilation*, des erreurs peuvent survenir et empêcher le déroulement complet de la génération de l'exécutable final. Là encore, la correction des erreurs passe toujours par un examen minutieux des messages d'erreur, en commençant toujours par le premier.

Avec `gcc` il est possible de ne demander que l'assemblage d'un code avec l'option `-S`.

![Assemblage d'un programme C pré-processé en assembleur](../assets/images/assembly.drawio)


![Traduction d'un programme C pré-processé en objet binaire](../assets/images/build.drawio)


### Édition de liens (*link*)

La phase d'édition de liens permet de rassembler le fichier binaire issu de la compilation et les autres fichiers binaires nécessaires au programme pour former un exécutable complet. Les autres fichiers binaires sont appelés des **librairies**. Elles peuvent appartenir au système (installée avec l'environnement de développement) ou provenir d'autres applications avec lesquelles votre programme doit interagir. Lors de l'édition de liens, des erreurs peuvent survenir et empêcher le
déroulement complet de génération de l'exécutable final. Là encore, la correction des erreurs passe toujours par un examen minutieux des messages d'erreur, en commençant toujours par le premier.

![Édition des liens de plusieurs objets](../assets/images/link.drawio)


## Hello World!

Il est traditionnellement coutume depuis la publication en 1978 du livre [The C Programming Language](https://en.wikipedia.org/wiki/The_C_Programming_Language) de reprendre l'exemple de Brian Kernighan comme premier programme.

```c title="hello.c"
--8<-- "docs/assets/src/hello.c"
```

Ce programme est composé de deux parties. L'inclusion de la *library* standard d'entrées sorties (*STandarD Inputs Outputs*) qui définit la fonction `printf`, et le programme principal nommé `main`. Tout ce qui se situe à l'intérieur des accolades `{ }` appartient au programme `main`.

L'ensemble que définit `main` et ses accolades est appelé une fonction, et la tâche de cette fonction est ici d'appeler une autre fonction `printf` dont le nom vient de *print formatted*.

L'appel de `printf` prend en **paramètre** le texte `Hello world!\n` dont le `\n` représente un retour à la ligne.

Une fois le code écrit, il faut le compiler. Pour bien comprendre ce que l'on fait, utilisons la ligne de commande ; plus tard, l'IDE se chargera de l'opération automatiquement.

Une console lancée ressemble à ceci, c'est intimidant si l'on n’en a pas l'habitude, mais vraiment puissant.

```bash
$
```

La première étape est de s'assurer que le fichier `test.c` contient bien notre programme. Pour ce faire on utilise un autre programme [cat](<https://fr.wikipedia.org/wiki/Cat_(Unix)>) qui ne fait rien d'autre que lire le fichier passé en argument et de l'afficher sur la console :

[](){#hello-world}

```bash
$ cat hello.c
#include <stdio.h>

int main(void)
{
    printf("hello, world\n");
    return 0;
}
```

À présent on peut utiliser notre compilateur par défaut: `cc` pour *C Compiler*. Ce compilateur prend en argument un fichier C et sans autre option, il génèrera un fichier [a.out](https://fr.wikipedia.org/wiki/A.out) pour *assembler output*. C'est un fichier exécutable que l'on peut donc exécuter.

```bash
$ gcc hello.c
```

Il ne s'est rien passé, c'est une bonne nouvelle. La philosophie Unix est qu'un programme soit le plus discret possible, comme tout s'est bien passé, inutile d'informer l'utilisateur.


On s'attend donc à trouver dans le répertoire courant, notre fichier source ainsi que le résultat de la compilation. Utilisons le programme [ls](https://fr.wikipedia.org/wiki/Ls) pour le vérifier

```bash
$ ls
hello.c       a.out
```

Très bien ! À présent, exécutons le programme en prenant soin de préfixer le nom par `./` car étant un programme local `a.out` ne peut pas être accédé directement. Imaginons qu'un fourbe hacker ait décidé de créer dans ce répertoire un programme nommé `ls` qui efface toutes vos données. La ligne de commande ci-dessus aurait eu un effet désastreux. Pour remédier à ce problème de sécurité, tout programme local doit être explicitement nommé.

```console
$ ./a.out
hello, world
```

Félicitations, le programme s'est exécuté.

Pouvons-nous en savoir plus sur ce programme ? On pourrait s'intéresser à la date de création de ce programme ainsi qu'à sa taille sur le disque. Une fois de plus `ls` nous sera utile, mais cette fois-ci avec l'option `l`:

```console
$ ls -l a.out
-rwxr-xr-- 1 ycr iai 8.2K Jul 24 09:50 a.out*
```

Décortiquons tout cela :

```console
-             Il s'agit d'un fichier
rwx           Lisible (r), Éditable (w) et Exécutable (x) par le propriétaire
r-x           Lisible (r) et Exécutable (x) par le groupe
r--           Lisible (r) par les autres utilisateurs
1             Nombre de liens matériels pour ce fichier
ycr           Nom du propriétaire
iai           Nom du groupe
8.2K          Taille du fichier, soit 8200 bytes soit 65'600 bits
Jul 24 09:50  Date de création du fichier
a.out         Nom du fichier
```

## Exercices de Révision

!!! exercise "Auteurs"

    Qui a inventé le C ?

    - [x] Ken Thompson
    - [ ] Brian Kernighan
    - [ ] Bjarne Stroustrup
    - [ ] Linus Torvalds
    - [x] Dennis Ritchie
    - [ ] Guido van Rossum

!!! exercise "Standardisation"

    Quel est le standard C à utiliser dans l'industrie en 2024 et pourquoi ?

    - [ ] C89
    - [ ] C99
    - [ ] C11
    - [x] C17
    - [ ] C23

    !!! solution

        Le standard industriel, malgré que nous soyons en 2024 est toujours
        **ISO/IEC 9899:2017**, car peu de changements majeurs ont été apportés
        au langage depuis et les entreprises préfèrent migrer sur C++ plutôt
        que d'adopter un standard plus récent qui n'apporte que peu de changements.

!!! exercise "Paradigmes"

    Quels est le paradigme de programmation supportés par C ?

    - [ ] Fonctionnel
    - [ ] Orienté objet
    - [ ] Réflectif
    - [x] Impératif
    - [ ] Déclaratif

    !!! solution

        C supporte les paradigmes impératifs, structurés et procédural.

!!! exercise "Langage impératif"

    Pourriez-vous définir ce qu'est la programmation impérative ?

    ??? solution

        La programmation impérative consiste en des séquences de commandes ordonnées.
        C'est-à-dire que les séquences sont exécutées dans un ordre définis les unes à la suite d’autres.

!!! exercise "Coulée de lave"

    Qu'est-ce qu'une coulée de lave en informatique ?

    ??? solution

        Lorsqu'un code immature est mis en production, l'industriel qui le publie risque un retour de flamme dû aux bogues et mécontentement des clients. Afin d'éviter une *coulée de lave*
        il est important qu'un programme soit testé et soumis à une équipe de *beta-testing* qui
        s'assure qu'outre le respect des spécifications initiales, le programme soit utilisable
        facilement par le public cible. Il s'agit aussi d'étudier l'ergonomie du programme.

        Un programme peut respecter le cahier des charges, être convenablement testé, fonctionner parfaitement, mais être difficile à l'utilisation, car certaines fonctionnalités sont peu ou pas documentées. La surcharge du service de support par des clients perdus peut également être assimilée à une coulée de lave.

!!! exercise "Cat"

    Qu'est-ce que `cat`?

    - [ ] Un programme de chat
    - [ ] Un programme de compilation
    - [x] Un programme d'affichage de fichiers
    - [ ] Un programme de copie de fichiers
    - [ ] Un programme de recherche de fichiers

    !!! solution

        `cat` est un programme normalisé POSIX prenant en entrée un fichier et l'affichant à l'écran. Il est utilisé notamment dans cet ouvrage pour montrer que le contenu du fichier `hello.c` est bel et bien celui attendu.
