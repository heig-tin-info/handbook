# Moi et mon ordinateur

Vous êtes devant votre ordinateur, vous avez en théorie un clavier devant vous, une souris à droite de votre clavier, et un ou plusieurs écrans devant vous.

Votre ordinateur démarre et vous verrez apparaître très probablement soit :

- Une pomme croquée (Apple)
- Une fenêtre à carreaux (Windows)
- Un manchot Adélie (Linux)

C'est votre système d'exploitation et peu importe lequel vous avez, la bonne nouvelle c'est que vous pourrez écrire vos premiers programmes avec n'importe lequel de ces systèmes d'exploitation.

## Éditeur de code source

Pour écrire un programme, vous aurez besoin d'un *éditeur de code*, c'est un programme qui vous permet d'écrire du texte et de le sauvegarder dans un fichier. Il en existe des centaines !

Si vous prenez une Doloréane munie d'un convecteur temporel, et que vous dépassez les 88 miles à l'heure, vous vous rendre en 1973 et vous pourrez utiliser un éditeur de code qui s'appelle `ed`.

![ED]({assets}/images/ed.jpg)

C'est un éditeur qui a été écrit à l'époque des [télétypes][teletype] et qui, curieusement, est encore intégré au standard POSIX. Il est par conséquent toujours disponible sur nos systèmes d'exploitation modernes. Il faut noter qu'à cette époque il n'y avait pas d'écran, et que l'on utilisait des imprimantes pour afficher le texte. L'éditeur n'est donc pas très interactif, mais il a le mérite d'exister.

En 1991 naît un éditeur de code qui va révolutionner le monde de la programmation, il s'appelle `vim`. C'est un éditeur de code qui est très puissant, mais qui a une courbe d'apprentissage assez velue. Il est toujours très utilisé de nos jours, et il est disponible sur tous les systèmes d'exploitation. Vous seriez surpris de voir le nombre de programmeurs qui l'utilisent encore. C'est un éditeur modal, c'est-à-dire qu'il a plusieurs modes, un mode pour écrire du texte, un mode pour éditer du texte, un mode pour naviguer dans le texte, etc.

Puisque nous nommons Vim, nous devons aussi nommer Emacs. Le rival de Vim. Emacs est un éditeur de code qui est aussi très puissant. Il est aussi très utilisé de nos jours, et il est disponible sur tous les systèmes d'exploitation.

![Guerre d'éditeurs]({assets}/images/vim-vs-emacs.png)

Nous ferons l'impasse sur d'autres éditeurs qui ont été populaires en leurs temps, mais qui sont technologiquement dépassés : TextPad, UltraEdit, Sublime Text, Atom, NotePad++... Le grand gagnant de ces dernières années est Visual Studio Code, un éditeur de code qui est très puissant, qui est très utilisé de nos jours, et qui est disponible sur tous les systèmes d'exploitation.

Le résultat de l'étude annuelle 2023 de [Stackoverflow](https://survey.stackoverflow.co/2023/#overview) donne une idée de la popularité des éditeurs et IDE les plus utilisés par les développeurs :

```mermaid
pie
    "Visual Studio Code" : 73.3
    "Visual Studio" : 28.4
    "IntelliJ IDEA" : 26.8
    "Notepad++": 24.5
    "Vim": 22.3
    "Emacs": 4.69
    "Eclipse": 9.9
    "Nano": 8.98
```

### Fonctionnalités attendues

Coloration Synatxique (*syntax highlighting*)

: L'éditeur de code colore les mots-clés du langage de programmation que vous utilisez. Cela permet de mieux visualiser la structure du code.

Correspondance des parenthèses (*brace matching*)

: L'éditeur de code vous permet de voir la correspondance des parenthèses, accolades, crochets, etc. Cela permet de voir en un tournemain si vous avez oublié une parenthèse.

Indentation automatique (*auto-indent*)

: L'éditeur de code vous permet d'indenter automatiquement votre code. Cela permet de voir la structure du code. Il est consensuellement admis qu' une région de code sélectionnée peut être indentée avec ++tab++ et désindentée avec ++shift+tab++.

Repli de code (*code folding*)

: L'éditeur de code vous permet de replier le code. En cliquant sur une petite flèche à gauche du code, vous pouvez replier le code pour ne voir que les en-têtes des fonctions, des boucles, des conditions, etc.

Structure du code (*outline*)

: L'éditeur de code vous permet de voir dans une fenêtre séparée les éléments de votre code. Cela permet de naviguer rapidement dans votre code.

Navigation hiérarchique (*go to definition*)

: L'éditeur de code vous permet de naviguer rapidement dans votre code. En cliquant sur un mot-clé, vous pouvez vous rendre à la définition de ce mot-clé. Habituellement ++alt+arrow-left++ vous permet de revenir en arrière là où vous étiez.

Expressions régulières (*regular expressions*)

: L'éditeur de code vous permet de rechercher ou remplacer des éléments en utilisant des expressions régulières. Par exemple si vous voulez inverser l'ordre des mots écrits `M. Yves Chevallier` par `M. Chevallier Yves`, vous pouvez utiliser l'expression régulière `/(M.|Mme.)\s+([^ ]+)\s+([^ ]+)/` et la remplacer par `$1 $3 $2`.

Multicurseurs (*multi-cursor*)

: L'éditeur de code vous permet de placer plusieurs curseurs dans votre code. Cela permet de modifier plusieurs lignes en même temps.

Complétion automatique (*auto-completion*)

: L'éditeur de code vous permet de compléter automatiquement le code en utilisant la touche ++tab++. Il utilise une technologie nommée *IntelliSense* qui, en ayant connaissance des mots-clés du langage de programmation et de ce que vous avez déjà écrit, vous propose les possibilités de complétion.

Intelligence artificielle (*AI*)

: L'éditeur de code vous permet de compléter automatiquement le code en utilisant une intelligence artificielle.

Gestion d'extensions (*extensions*)

: L'éditeur de code vous permet d'ajouter des extensions permettant d'ajouter des fonctionnalités à votre éditeur de code.

Intégration du terminal (*terminal integration*)

: L'éditeur de code vous permet d'intégrer un terminal (TTY) dans votre éditeur de code pour lancer directement des commandes.

Intégration de Git (*git integration*)

: L'éditeur de code vous permet d'intégrer Git dans votre éditeur de code pour gérer les versions de votre code.

## Compilateur

Un **compilateur** est un programme qui permet de transformer un programme écrit dans un langage de programmation en un programme exécutable. Il existe de nombreux compilateurs, et chaque langage de programmation a son propre compilateur.

En C, les compilateurs les plus populaires et qui respectent les normes sont GCC et CLANG.

[GCC](https://gcc.gnu.org/)

: Un **compilateur** *open-source* utilisé sous Linux et macOS. Il est sous licence GPL.

[CLANG](https://clang.llvm.org/)

: Un **compilateur** *open-source* gagnant en popularité, une alternative à GCC. Il est sous licence Apache et utilise la bibliothèque LLVM.

## IDE

Un **IDE** est un *Integrated Development Environment*, c'est un environnement de développement intégré. C'est un programme qui vous permet d'écrire du code, de le compiler, de le déboguer, de le tester, de le déployer, etc.

Tous les éditeurs ne sont pas des IDE, mais tous les IDE sont des éditeurs. En fin de compte, un IDE est un éditeur qui a des fonctionnalités supplémentaires telles que:

- Un compilateur
- Un débogueur
- Gestion de paramètres par projet
- Gestion de dépendances logicielles
- ...


Un autre composant essentiel de l'environnement de développement est le **compilateur**. Il s'agit généralement d'un ensemble de programmes qui permettent de convertir le **code** écrit en un programme exécutable. Ce programme peut-être par la suite intégré dans un *smartphone*, dans un système embarqué sur un satellite, sur des cartes de prototypage comme un Raspberry PI, ou encore sur un ordinateur personnel.

L'ensemble des outils nécessaire à créer un produit logiciel est appelé chaîne de compilation, plus communément appelée [toolchain](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_compilation).

![Représentation graphique des notions de compilateur, IDE, toolchain...]({assets}/images/toolchain.drawio)


!!! exercise Eclipse

    Un ami vous parle d'un outil utilisé pour le développement logiciel nommé **Eclipse**. De quel type d'outil s'agit-il ?

    ??? solution

        [Eclipse](https://www.eclipse.org/ide/) est un IDE. Il n'intègre donc pas de chaîne de compilation et donc aucun compilateur.

??? exercise

    Combien y a-t-il eu de questions posées en C sur le site Stack Overflow?

    ??? solution

        Il suffit pour cela de se rendre sur le site de `Stackoverflow <https://stackoverflow.com/tags/c>`__ et d'accéder à la liste des tags. En 2019/07 il y eut 307'669 questions posées.

        Seriez-vous capable de répondre à une question posée?
