# Visual Studio Code

Visual Studio Code est un éditeur de code source développé par Microsoft. Il est gratuit, open-source et multiplateforme. Il est très populaire pour le développement de logiciels, notamment pour les langages de programmation tels que C, C++, Python, Java, etc.

Il s'inscrit dans une très longue liste d'éditeurs de code source. La table suivante présente quelques éditeurs de code source populaires.

Table: Éditeurs de code source populaires

| Éditeur            | Année | Commentaire                                                | Inspiré de   |
| ------------------ | ----- | ---------------------------------------------------------- | ------------ |
| ed                 | 1971  | Éditeur primitif en mode texte défini dans la norme POSIX  | -            |
| Vi                 | 1976  | Éditeur en mode texte défini dans la norme POSIX           | ed           |
| Emacs              | 1976  | Éditeur extensible et personnalisable.                     | TECO         |
| Vim                | 1991  | Amélioration de Vi, très populaire des geek et devloppeurs | Vi           |
| Nano               | 1999  | Éditeur simple et convivial en ligne de commande           | -            |
| Sublime Text       | 2008  | Éditeur propriétaire avec une version gratuite             | Vim          |
| Atom               | 2014  | Éditeur open-source développé par GitHub                   | Sublime Text |
| Visual Studio Code | 2015  | Éditeur open-source développé par Microsoft                | Atom         |

Outre ces éditeurs on peut citer d'autres éditeurs de texte tels que Notepad++, TextPad, UltraEdit, etc. Si vous les utilisez, demandez-vous pourquoi...

## Raccourcis clavier

Parmis les très nombreux raccourcis clavier de Visual Studio Code, vous trouverez ci-dessous une liste des raccourcis les plus utiles.

Table: Raccourcis clavier de Visual Studio Code

| Raccourci       | Description                                                           |
| --------------- | --------------------------------------------------------------------- |
| `Ctrl+P`        | Ouvrir un fichier (*fuzzy search*)                                    |
| `Ctrl+Shift+P`  | Ouvrir la palette de commandes (*fuzzy search*)                       |
| `Ctrl+Shift+N`  | Nouvelle fenêtre                                                      |
| `Ctrl+Shift+F`  | Rechercher dans tous les fichiers                                     |
| `Ctrl+Shift+G`  | Ouvrir le contrôle de code source (pour faire un Git commit)          |
| `Ctrl+Shift+D`  | Ouvrir le contrôle de débogage                                        |
| `Ctrl+Shift+X`  | Ouvrir le gestionnaire d'extensions                                   |
| `Ctrl+Shift+V`  | Ouvrir un aperçu du fichier Markdown                                  |
| `Ctrl+K V`      | Ouvrir un aperçu côte à côte du fichier Markdown                      |
| `Ctrl+K Z`      | Activer/désactiver le mode Zen (plein écran)                          |
| `Ctrl+K S`      | Enregistrer sous...                                                   |
| `Ctrl+K R`      | Ouvrir le dossier du fichier actuel                                   |
| `Ctrl+K Ctrl+O` | Ouvre un dossier                                                      |
| `Ctrl+D`        | Sélectionner le mot suivant (multicurseur) (répéter)                  |
| `Ctrl+U`        | Annuler la dernière sélection                                         |
| `Ctrl+J`        | Ouvrir un terminal intégré                                            |
| `Ctrl+L`        | Sélectionner la ligne entière (répéter)                               |
| `Ctrl+Shift+L`  | Sélectionner toutes les occurrences du mot sélectionné (multicurseur) |
| `Alt+Click`     | Insérer un curseur                                                    |
| `Ctrl+Alt+Up`   | Insérer un curseur au-dessus                                          |

## Installation

Pour installer Visual Studio Code, rendez-vous sur la page [https://code.visualstudio.com/](https://code.visualstudio.com/) et téléchargez la version correspondant à votre système d'exploitation. Une fois téléchargé, installez-le en suivant les instructions.

Alternativement, utilisez `winget` depuis PowerShell :

```powershell
winget install -e --id Microsoft.VisualStudioCode
```

## Extensions

### WSL

Si vous utilisez WSL vous devez installer l'extension `Remote - WSL` pour Visual Studio Code. Cette extension permet d'ouvrir un terminal intégré dans WSL, d'exécuter des commandes dans WSL, de déboguer des programmes dans WSL, etc.

### Remote - SSH

Si vous utilisez SSH pour vous connecter à un serveur distant par exemple vous connecter directement sur votre RaspberryPI, vous devez installer l'extension `Remote - SSH` pour Visual Studio Code. Cette extension permet d'ouvrir un terminal intégré sur un serveur distant, d'exécuter des commandes sur le serveur distant, de déboguer des programmes sur le serveur distant, etc.

### C/C++

Si vous développez en C ou en C++, vous devez installer l'extension `C/C++` pour Visual Studio Code. Cette extension permet d'ajouter des fonctionnalités pour le développement en C et en C++ telles que la coloration syntaxique, l'autocomplétion, la compilation, le débogage, etc.

### Python

Si vous développez en Python, vous devez installer l'extension `Python` pour Visual Studio Code. Cette extension permet d'ajouter des fonctionnalités pour le développement en Python telles que la coloration syntaxique, l'autocomplétion, la compilation, le débogage, etc.

### Configuration pour le debogueur

Visual Studio Code n'a pas la notion de **projet** mais d'espace de travail **workspace**. Un espace de travail est simplement un répertoire. À l'intérieur de ce répertoire, on y trouvera :

```text
.
├── .vscode
│   └── launch.json
└── main.c
```

Visual Studio Code peut en général générer automatiquement le fichier `.vscode/launch.json` qui contient tout ce qu'il faut pour compiler et exécuter le programme :

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "gcc",
      "type": "cppdbg",
      "request": "launch",
      "program": "${fileDirname}\\${fileBasenameNoExtension}.exe",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "gdb",
      "miDebuggerPath":
        "C:\\ProgramData\\chocolatey\\lib\\mingw\\tools\\install\\mingw64\\bin\\gdb.exe",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for gdb",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ],
      "preLaunchTask": "gcc.exe build active file"
    }
  ]
}
```

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "shell",
      "label": "gcc.exe build active file",
      "command":
        "C:\\ProgramData\\chocolatey\\lib\\mingw\\tools\\install\\mingw64\\bin\\gcc.exe",
      "args": [
        "-g",
        "${file}",
        "-o",
        "${fileDirname}\\${fileBasenameNoExtension}.exe"
      ],
      "options": {
        "cwd":
          "C:\\ProgramData\\chocolatey\\lib\\mingw\\tools\\install\\mingw64\\bin"
      },
      "problemMatcher": [
        "$gcc"
      ]
    }
  ]
}
```
