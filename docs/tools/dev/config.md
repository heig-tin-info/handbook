# Fichiers de configuration

## Introduction

Dans un projet, vous aurez très souvent un tas de fichiers de configuration. Ils commencent généralement par un point (`.`) pour les cacher dans le répertoire. C'est la manière dont les fichiers sont cachés dans les systèmes de fichiers Unix.

## Fichiers populaires

### .clang-format

Ce fichier est au format YAML et contient des directives pour formater votre code automatiquement soit à partir de VsCode si vous avez installé l'extension [Clang-Format](https://marketplace.visualstudio.com/items?itemName=xaver.clang-format) et l'exécutable `clang-format` (`sudo apt install -y clang-format`). [Clang-format](https://clang.llvm.org/docs/ClangFormat.html) est un utilitaire de la suite LLVM, proposant Clang un compilateur alternatif à GCC.

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

```text
* text=auto eol=lf
*.{cmd,[cC][mM][dD]} text eol=crlf
*.{bat,[bB][aA][tT]} text eol=crlf
```

### .gitignore

Ce fichier de configuration permet à Git d'ignorer par défaut certains fichiers et ainsi éviter qu'ils ne soient ajoutés par erreur au référentiel. Ici, on souhaite éviter d'ajouter les fichiers objets `.o` et les exécutables `*.out` :

```text
*.out
*.o
*.d
*.so
*.lib
```

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

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Build Main",
            "type": "shell",
            "command": "make",
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "Clean",
            "type": "shell",
            "command": "make clean"
        }
    ]
}
```
