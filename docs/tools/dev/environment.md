# L'environnement de travail

Vous êtes étudiante ou étudiant et vous êtes perdus avec l'utilisation de Python, LaTeX, Git, etc., sous Windows, Linux ou encore Docker Ce document est fait pour vous. Il vous guidera dans l'installation et l'utilisation de ces outils. L'objectif est de comprendre les avantages et les inconvénients de chaque outil et de vous permettre de les utiliser de manière efficace.

## Préambule

Les applications utilisées typiquement par un ingénieur aujourd'hui sont Python, Git, GCC, LaTeX ou même Docker. Ces applications ont un point commun, c'est qu'elles ont d'abord été écrites pour un environnement **POSIX** (Unix).

**POSIX** est une norme internationale (IEEE 1003) qui définit l'interface de programmation d'un système d'exploitation. Elle est basée sur UNIX. Elle est utilisée pour les systèmes d'exploitation de type UNIX. Windows n'est pas un système qui respecte cette norme, ce qui complique l'utilisation de ces applications.

Afin de pouvoir porter Python ou Git sous Windows, il a fallu ajouter une couche d'abstraction pour rendre compatible le monde Linux avec le monde Windows. Historiquement le projet [Cygwin](https://fr.wikipedia.org/wiki/Cygwin) né en 1995 a été le premier à proposer une telle couche. Il s'agissait d'un environnement POSIX pour Windows muni d'un terminal, d'un gestionnaire de paquets et d'une bibliothèque d'émulation POSIX. Les outils en ligne de commande type `ls`, `cat` ou même `grep` étaient proposés. Néanmoins, Cygwin n'était pas parfait, il nécessitait son propre environnement de travail et n'était pas bien intégré à Windows. Le projet MSYS a été créé en 2003 pour pallier à ces problèmes. Il s'agissait d'une couche d'abstraction POSIX pour Windows qui se voulait plus légère. Au lieu de compiler des applications Linux qui devaient impérativement être lancées sous Cygwin, MSYS intégrait la couche d'abstraction dans les applications elles-mêmes, ces dernières étaient compilées en `.exe` et pouvaient être lancées directement depuis l'explorateur Windows. MSYS a été un franc succès et a été intégré dans le projet [MinGW](https://fr.wikipedia.org/wiki/MinGW) (Minimalist GNU for Windows) qui est un portage de GCC pour Windows.

Lorsque vous installez `Git` sous Windows et que vous visitez l'emplacement d'installation (`C:\Program Files\Git`), vous verrez des dossiers aux noms compatibles `POSIX` comme `bin`, `etc`, `lib`, `usr`, etc. Le dossier `bin` qui contient les exécutables contient `bash` qui n'est rien d'autre que le terminal utilisé sous Linux. La raison est que `Git` ou même `Python` sont des outils avant tout développés pour les environnements Unix/Linux.

Le choix de l'environnement de travail est donc compliqué. Faut-il travailler sous Windows avec les limitations que le portage des applications Linux implique ou faut-il travailler sous Linux directement ? Un ingénieur reste  aujourd'hui attaché au monde Windows car il dépend de logiciels comme `SolidWorks` ou `Altium Designer` qui ne sont pas disponibles sous Linux. Il est donc nécessaire de trouver un compromis.

En 2016, Microsoft a annoncé le support de Linux dans Windows 10. Il s'agissait d'une couche d'abstraction qui permettait de faire tourner des applications Linux directement sous Windows. Cette couche d'abstraction s'appelle [Windows Subsystem for Linux](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) (WSL). Elle est basée sur une technologie de virtualisation de conteneurs. WSL a été un franc succès et il a très vite été adopté par les développeurs Web. Il fut de surcroît proposé comme une alternative à Cygwin et MSYS.

WSL a été amélioré au fil des années et en 2019, Microsoft a annoncé WSL 2. WSL 2 est basé sur une technologie de virtualisation de type 2 (hyperviseur) et non plus de type 1 (noyau Linux). WSL 2 est donc plus performant que WSL 1. Il est possible de faire tourner un serveur web ou même un serveur de base de données directement sous WSL 2. WSL 2 est maintenant une alternative crédible à Linux.

Il rend possible de travailler sous Windows et de faire tourner des applications Linux directement sous Windows.

Le choix donné aux ingénieurs est donc :

1. **Choix facile, mais source d'incohérences**: Travailler exclusivement sous Windows et installer `Python`, `Git`, `LaTeX` sous Windows. L'inconvénient est que chacune de ses applications ne profite pas d'une unité de travail commune. À force d'installer des applications, vous aurez dans votre système plusieurs installations de Python, plusieurs exécutables Git ce qui peut vite devenir compliqué à gérer.
2. **Choix plus difficile, mais offrant davantage de flexibilité**: Travailler sous WSL 2 et de faire tourner `Python`, `Git`, `LaTeX` sous Linux. L'avantage est que vous aurez une unité de travail commune. Vous pourrez installer des applications Linux directement depuis le gestionnaire de paquets de votre distribution Linux. Néanmoins vous devrez vous familiariser avec la ligne de commande Linux.

## Le terminal

Historiquement sous Windows, le terminal était une application graphique appelée `cmd`. Elle n'a pas évolué depuis Windows NT. Son interface est limitée à un nombre fini de caractères par ligne et ne supportait que quelques couleurs. Elle ne supportait pas les caractères Unicode et ne supportait pas les raccourcis clavier comme `Ctrl+C` ou `Ctrl+V`.

Heureusement Windows a évolué et propose PowerShell. PowerShell est un terminal plus moderne qui supporte les couleurs, les raccourcis clavier, les caractères Unicode, etc. PowerShell est un terminal plus puissant que `cmd`.

L'interface du terminal était également rudimentaire (pas d'onglets, pas de séparateurs, etc.). Heureusement Windows propose depuis 2019 [Windows Terminal](https://en.wikipedia.org/wiki/Windows_Terminal). Windows Terminal est un terminal moderne multionglets qui supporte plusieurs terminaux (cmd, PowerShell, WSL, etc.). S'il n'est pas installé, vous pouvez le faire via le [Microsoft Store](https://www.microsoft.com/fr-ch/p/windows-terminal/9n0dx20hk701).

![Interface de cmd.exe dans Windows Terminal](/assets/images/cmd.png)

![Interface de PowerShell dans Windows Terminal](/assets/images/powershell.png)

![Interface de Ubuntu dans Windows Terminal](/assets/images/bash.png)

## Variables d'environnement

Que vous soyez sous POSIX ou Windows, votre système d'exploitation dispose de variables d'environnement. Il s'agit de variables qui sont accessibles par toutes les applications. Elles sont utilisées pour stocker des informations comme le chemin d'accès à un exécutable, le nom de l'utilisateur, le répertoire de travail, etc.

La variable la plus importante est `PATH`. Elle contient une liste de chemins d'accès aux exécutables. Lorsque vous tapez une commande dans un terminal, le système d'exploitation parcourt les chemins d'accès de la variable `PATH` pour trouver l'exécutable correspondant à la commande. Si vous avez installé Python, Git, LaTeX, etc., dans des répertoires différents, il est nécessaire de les ajouter à la variable `PATH`. Parfois les installateurs le font automatiquement, parfois non. Il est donc nécessaire de vérifier manuellement.

Une variable d'environnement n'est propagée à un processus que si ce dernier est lancé après la modification de la variable. Si vous modifiez la variable, `PATH` les processus déjà lancés ne verront pas la modification. Il est nécessaire de fermer le terminal et de le rouvrir (relancer Visual Studio Code, votre terminal, etc.).

Parfois si vous installez plusieurs versions d'un même logiciel comme `Python` vous pourriez avoir plusieurs variables d'environnement qui pointent vers des versions différentes de Python. C'est une source de confusion et c'est un problème fréquent sous Windows. Vous pouvez vérifier quel est le chemin d'accès à un exécutable avec la commande `where` sous Windows et `which` sous Linux.

=== "Linux/WSL/MacOS"

    ```bash
    $ which python
    /usr/bin/python
    ```

=== "Windows CMD"

    ```cmd
    PS C:\> where python
    C:\Python39\python.exe
    ```

=== "PowerShell"

    ```powershell
    PS C:\> Get-Command python
    ```

### LaTeX

Sous Linux/WSL, le plus simple est d'installer LaTeX avec le gestionnaire de paquets de votre distribution Linux. Ouvrez un terminal et tapez la commande suivante :

```bash
sudo apt install texlive-full latexmk
```

Sous Windows c'est plus compliqué. Il existe plusieurs distributions LaTeX pour Windows. La plus courante est [MiKTeX](https://miktex.org). Téléchargez l'installateur et suivez les instructions.

## Commandes principales

### GCC

| Commande | Description                 |
| -------- | --------------------------- |
| `gcc`    | Compilateur C               |
| `g++`    | Compilateur C++             |
| `make`   | Gestionnaire de compilation |

Pour compiler un programme :

=== "C"

    ```bash
    gcc -o hello hello.c
    ```

=== "C++"

    ```bash
    g++ -o hello hello.cpp
    ```

=== "Plusieurs fichiers C"

    ```bash
    gcc -o hello main.c functions.c
    ```

=== "Compilation séparée"

    ```bash
    gcc -c functions.c
    gcc -c main.c
    gcc -o hello main.o functions.o
    ```

### Linux/WSL

| Commande | Description                                        |
| -------- | -------------------------------------------------- |
| `ls`     | Liste les fichiers du répertoire courant           |
| `cd`     | Change de répertoire                               |
| `pwd`    | Affiche le répertoire courant                      |
| `cat`    | Affiche le contenu d'un fichier                    |
| `less`   | Affiche le contenu d'un fichier page par page      |
| `grep`   | Recherche une chaîne de caractères dans un fichier |
| `find`   | Recherche un fichier dans un répertoire            |
| `man`    | Affiche le manuel d'une commande                   |
| `which`  | Affiche le chemin d'accès à un exécutable          |

#### Afficher les fichiers du répertoire courant

```bash
ls -al # Par noms
ls -lt # Par date de modification
ls -lh # En format lisible
```

### Python

| Commande      | Description                       |
| ------------- | --------------------------------- |
| `python`      | Lance l'interpréteur Python       |
| `pip`         | Gestionnaire de paquets Python    |
| `ipython`     | Lance l'interpréteur IPython      |
| `jupyter lab` | Lance l'environnement Jupyter Lab |

### LaTeX

| Commande           | Description               |
| ------------------ | ------------------------- |
| `latexmk -xelatex` | Compile un document LaTeX |
