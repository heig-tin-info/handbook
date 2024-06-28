# Environnement de développement

Si ce n'est pas déjà le cas, vous devriez disposer sur votre ordinateur d'un environnement de développement. Pour ce cours, vous êtes libre d'utiliser l'outil qui vous semble le plus pertinent, mais il propose d'utiliser un environnement POSIX qui est aujourd'hui le standard le plus établi et le plus largement utilisé, des téléphones portables aux serveurs informatiques, aux MacBook et aux fusées spatiales. L'autre consensus, également largement utilisé est Windows.

Pour disposer d'un environnement POSIX sous Windows, il existe 3 solutions :

[MinGW](http://www.mingw.org/)

: Un environnement POSIX GNU pour Windows. La solution la plus facile.

[WSL2](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux)

: L'acronyme de *Windows Subsystem for Linux*, c'est une distribution Ubuntu pour Windows 10. La meilleure solution si vous voulez vous confronter à la ligne de commande et mieux comprendre le fonctionnement de Linux.

[Docker](https://docker.com)

: Un système de containers permettant d'émuler un environnement POSIX isolé sans pour autant devoir installer des tas d'applications.

Pour installer le plus facilement votre environnement de développement, je vous recommande [Chocolatey](https://chocolatey.org/), un gestionnaire de paquets pour Windows. Une fois l'outil installé, vous pouvez installer les paquets suivants :

```console
C:\> choco install gcc
C:\> choco install vscode
C:\> choco install docker
C:\> choco install git.install
C:\> choco install microsoft-windows-terminal
C:\> choco install python3
```

Ensuite vous pouvez exécuter `Git Bash` depuis le menu Démarrer et disposer d'une console comme si vous étiez sous Linux ou MacOSx.
