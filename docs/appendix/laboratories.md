# Laboratoires

Les laboratoires sont des travaux pratiques permettant à l'étudiant d'attaquer des problèmes de programmation plus difficiles que les exercices faits en classe.

## Protocole

1. Récupérer le référentiel du laboratoire en utilisant GitHub Classroom.
2. Prendre connaissance du cahier des charges.
3. Rédiger le code.
4. Le tester.
5. Rédiger votre rapport de test si demandé.
6. Le soumettre avant la date butoir.

## Évaluation

Une grille d'évaluation est intégrée à tous les laboratoires. Elle prend la forme d'un fichier `criteria.yml` que l'étudiant peut consulter en tout temps.

## Directives

- La recherche sur internet est autorisée et conseillée.
- Le plagiat n'est pas autorisé, et sanctionné si découvert par la note de 1.0.
- Le rendu passé la date butoir est sanctionné à raison de 1 point puis 1/24 de point par heure de retard.

## Format de rendu

- Fin de lignes: `LF` (`'\n'`).
- Encodage: UTF-8 sans BOM.
- Code source respectueux de ISO/IEC 9899:1999.
- Le code doit comporter un exemple d'utilisation et une documentation mise à jour dans `README.md`.
- Lorsqu'un rapport est demandé, vous le placerez dans `REPORT.md`.

## Anatomie d'un travail pratique

Un certain nombre de fichiers vous sont donnés, il est utile de les connaître. Un référentiel sera généralement composé des éléments suivants :

```text
$ tree
.
├── .clang-format
├── .devcontainer
│   ├── Dockerfile
│   └── devcontainer.json
├── .editorconfig
├── .gitattributes
├── .gitignore
├── .vscode
│   ├── launch.json
│   └── tasks.json
├── Makefile
├── README.md
├── assets
│   └── test.txt
├── foo.c
├── foo.h
├── main.c
├── criteria.yml
└── tests
    ├── Makefile
    └── test_foo.c
```

### .clang-format

Ce fichier est au format [YAML](https://fr.wikipedia.org/wiki/YAML) et contient des directives pour formater votre code automatiquement soit à partir de VsCode si vous avez installé l'extension [Clang-Format](https://marketplace.visualstudio.com/items?itemName=xaver.clang-format) et l'exécutable `clang-format` (`sudo apt install -y clang-format`). [Clang-format](https://clang.llvm.org/docs/ClangFormat.html) est un utilitaire de la suite LLVM, proposant Clang un compilateur alternatif à GCC.

On voit que le texte passé sur `stdin` (jusqu'à EOF) est ensuite formaté proprement :

```console
$ clang-format --style=mozilla <<EOF
#include <stdio.h>
int
main
()
{printf("hello, world\n");}
EOF
#include <stdio.h>
int
main()
{
printf("hello, world\n");
}
```

Par défaut `clang-format` utilise le fichier de configuration nommé `.clang-format` qu'il trouve.

Vous pouvez générer votre propre configuration facilement depuis un configurateur tel que [clang-format configurator](https://zed0.co.uk/clang-format-configurator/).

### .editor_config

Ce fichier au format YAML permet de spécifier des recommandations pour l'édition de fichiers sources. Vous pouvez y spécifier le type de fin de lignes **CR** ou **CRLF**, le type d'indentation (espaces ou tabulations) et le type d'encodage (ASCII ou UTF-8) pour chaque type de fichiers. [EditorConfig](https://editorconfig.org/) est aujourd'hui supporté par la plupart des éditeurs de textes qui cherchent automatiquement un fichier de configuration nommé `.editor_config`.

Dans Visual Studio Code, il faut installer l'extension [EditorConfig for VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig) pour bénéficier de ce fichier.

Pour les travaux pratiques, on se contente de spécifier les directives suivantes :

```yaml
root = true

[*]
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4
charset = utf-8

[*.{json,yaml}]
indent_style = space
indent_size = 2

[Makefile]
indent_style = tab

[*.{cmd,bat}]
end_of_line = crlf
```

### .gitattributes

Ce fichier permet à Git de résoudre certains problèmes dans l'édition de fichiers sous Windows ou POSIX lorsque le type de fichiers n'a pas le bon format. On se contente de définir quelle sera la fin de ligne standard pour certains types de fichiers :

% code::text
%
% * text=auto eol=lf
% *.{cmd,[cC][mM][dD]} text eol=crlf
% *.{bat,[bB][aA][tT]} text eol=crlf

### .gitignore

Ce fichier de configuration permet à Git d'ignorer par défaut certains fichiers et ainsi éviter qu'ils ne soient ajoutés par erreur au référentiel. Ici, on souhaite éviter d'ajouter les fichiers objets `.o` et les exécutables `*.out` :

% code::text
%
% *.out
% *.o
% *.d
% *.so
% *.lib

### .vscode/launch.json

Ce fichier permet à Visual Studio Code de savoir comment exécuter le programme en mode débogue. Il est au format JSON. Les lignes importantes sont `program` qui contient le nom de l'exécutable à lancer `args` qui spécifie les arguments passés à ce programme et `MiMode` qui est le nom du débogueur que vous utiliserez. Par défaut nous utilisons GDB.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Main",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/a.out",
            "args": ["--foobar", "filename", "<<<", "hello, world"],
            "stopAtEntry": true,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "Build Main"
        }
    ]
}
```

### .vscode/tasks.json

Ce fichier contient les directives de compilation utilisées par Visual Studio Code lors de l'exécution de la tâche *build* accessible par la touche `<F5>`. On y voit que la commande exécutée est `make`. Donc la manière dont l'exécutable est généré dépend d'un `Makefile`.

% code::json
%
% {
%     "version": "2.0.0",
%     "tasks": [
%         {
%             "label": "Build Main",
%             "type": "shell",
%             "command": "make",
%             "group": {
%                 "kind": "build",
%                 "isDefault": true
%             }
%         },
%         {
%             "label": "Clean",
%             "type": "shell",
%             "command": "make clean"
%         }
%     ]
% }

### Makefile

Ce fichier contient les directives nécessaires au programme `make` pour générer votre exécutable. Vous pouvez vous inspirer de ce `Makefile` générique, mais n'oubliez pas que la tabulation dans un Makefile doit être le caractère tabulation (pas des espaces). Si vous avez l'extension EditorConfig installée pour votre éditeur vous pouvez reformater le fichier avant de l'enregistrer.

```make
CSRCS=$(wildcard *.c)
COBJS=$(patsubst %.c,%.o,$(CSRCS))
EXEC?=a.out

CFLAGS=-std=c99 -g -Wall -pedantic
LDFLAGS=-lm

all: $(EXEC)

-include $(COBJS:.o=.d)

$(EXEC): $(COBJS)
    $(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
    $(CC) -c $(CFLAGS) -o $@ $< -MMD -MF $(@:.o=.d)

clean:
    $(RM) $(EXEC) *.o a.out $(COBJS:.o=.d)

.PHONY: all prof clean
```

En substance, ce fichier contient des règles, des dépendances et des recettes de fabrication. Les règles de base sont `all` et `clean`. La règle `all` dépend de la règle `$(EXEC)` qui est une variable qui contient le nom de l'exécutable, ici `a.out`. Vous pouvez spécifier le nom de l'exécutable souhaité à la ligne `EXEC=mon_executable`. La règle `$(EXEC)` dépend de `$(COBJS)` qui sont la liste des objets C, à savoir tous les fichiers `.c` dont l'extension est remplacée par `.o`. Une règle générique permet ensuite de générer tous les fichiers objets nécessaires à partir du fichier C correspondant : `%.o: %.c`. Enfin, en compilation séparée, l'exécutable est créé en assemblant tous les fichiers objets.

Pas de panique, il vous suffit de savoir exécuter `make all` ou `make clean` pour vous en sortir.

### README.md

Il s'agit de la documentation principale de votre référentiel. Elle contient la donnée du travail pratique en format Markdown. Ce fichier est également utilisé par défaut dans GitHub. Il contient notamment le titre du laboratoire, la durée, le délai de rendu et le format individuel ou de groupe :

% code::markdown
%
% # Laboratoire <!-- omit in toc -->
%
% - **Durée**: 2 périodes + environ 3h à la maison
% - **Date de rendu**: dimanche avant minuit
% - **Format**: travail individuel
%
% ...

### criteria.yml

Ce fichier contient les directives d'évaluation du travail pratique. Il est au format YAML. Pour chaque point évalué une description est donnée avec la clé `description` et un nombre de points est spécifié. Une exigence peut avoir soit un nombre de points positifs soit négatifs. Les points négatifs agissent comme une pénalité. Ce choix d'avoir des points et des pénalités permet de ne pas diluer les exigences au travers d'autres critères importants, mais normalement respectés des étudiants.

Des points bonus sont donnés si le programme dispose d'une aide et d'une version et si la fonctionnalité du programme est étendue.

% code::yaml
%
% # Critères d'évaluation du travail pratique
% %YAML 1.2
% ---
% tests:
%     build:
%         description: Le programme compile sans erreurs ni warning
%         points: 0/-4
%         test: test_build
%     unit-testing:
%         function_foo:
%         points: 0/10
%         test: test_foo
%         function_bar:
%         points: 0/10
%         test: test_bar
%     functional-testing:
%         arguments:
%         description: La lecture des arguments fonctionne comme demandé
%         points: 0/7
%         test: test_arguments
%         output-display:
%         description: Affichage sur stdout/stderr comme spécifié
%         points: 0/3
%         test: test_output
%         errors:
%         description: Le programme affiche des erreurs si rencontrées
%         points: 0/2
%         test: test_errors
% report:
%     introduction:
%         description: Le rapport de test contient une introduction
%         points: 0/2
%     conclusion:
%         description: Le rapport de test contient une conclusion
%         points: 0/2
%     analysis:
%         description: Le rapport de test contient une analyse du comportement
%         points: 0/3
% code:
%     specifications:
%         prototypes:
%             description: Les prototypes des fonctions demandées sont respectés
%             points: 0/3
%         main:
%             description: Le programme principal est minimaliste
%             points: 0/3
%         algorithm:
%             description: L'algorithme de encode/decode est bien pensé
%             points: 0/5
%     comments:
%         header:
%         description: Un en-tête programme est clairement défini
%         points: 0/2
%         purpose:
%         description: Les commentaires sont pertinents
%         points: 0/-2
%         commented-code:
%         description: Du code est commenté
%         points: 0/-2
%     variables:
%         naming:
%         description: Le noms des variables est minimaliste et explicite
%         points: 0/2
%         scope:
%         description: La portée des variables est réduite au minimum
%         points: 0/2
%         type:
%         description: Le type des variables est approprié
%         points: 0/2
%     functions:
%         length:
%         description: La longueur des fonctions est raisonnable
%         points: 0/-4
%     control-flow:
%         description: Les structures de contrôle sont appropriées
%         points: 0/4
%     overall:
%         dry:
%         description: Pas de répétition dans le code
%         points: 0/-5
%         kiss:
%         description: Le code est minimaliste et simple
%         points: 0/-5
%         ssot:
%         description: Pas de répétition d'information
%         points: 0/-5
%         indentation:
%         description: L'indentation du code est cohérente
%         points: 0/-5
% bonus:
%     help:
%         description: Le programme dispose d'une aide
%         bonus: 0/1
%         test: test_help
%     version:
%         description: La version du programme peut être affichée
%         bonus: 0/1
%         test: test_version
%     extension:
%         description: La fonctionnalité du programme est étendue
%         bonus: 0/3
%     english:
%         description: Usage de l'anglais
%         bonus: 0/1

Ce fichier est utilisé par des tests automatique pour faciliter la correction du travail pratique.
