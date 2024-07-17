# Python

![Un python informaticien](../assets/images/python.png)

## Introduction

Python est un langage de programmation comme le C mais il est plus haut niveau. Cela signifie que Python est plus facile à apprendre et à utiliser que le C. Python est un langage interprété, ce qui signifie que le code source est exécuté directement par un interpréteur sans nécessairement passer par une étape de compilation.

C'est un langage très populaire pour l'enseignement de la programmation et pour la science des données. Python est utilisé dans de nombreux domaines, tels que l'intelligence artificielle, l'apprentissage automatique, l'analyse de données, la programmation web, la programmation système, etc.

## Installation de Python

Sous Linux/WSL, l'installation de Python est très simple. Ouvrez un terminal et tapez la commande suivante :

=== "Ubuntu"

    ```bash
    sudo apt install python3
    ```

=== "MacOS"

    ```bash
    brew install python3
    ```

=== "Windows"

    ```powershell
    winget install -e --id Python.Python.3.12
    ```

    Sous Windows, vous devez choisir la version de Python que vous souhaitez installer. Il est recommandé d'installer la version `3.12` de Python. Utilisez le gestionnaire de paquets `winget` pour installer Python.

## Configuration des variables d'enviroonement

Selon la méthode utilisée pour installer Python, il est possible que les variables d'environnement ne soient pas configurées automatiquement. Il y a deux entrées à configurer dans la variable `PATH` :

1. Le chemin vers l'exécutable Python. Sous Linux/WSL, le chemin sera déjà configuré (`/usr/bin`). Sous Windows, le chemin diffère selon les époques, les installateurs et les versions.
2. Le chemin vers les paquets locaux installés avec `pip`.

Pour configurer sous Linux/WSL le chemin vers les paquets locaux installés avec `pip`, ouvrez un terminal et tapez la commande suivante :

=== "Linux/WSL"

    ```bash
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> ~/.bashrc
    source ~/.bashrc
    ```

=== "Windows"

    Sous Windows, c'est plus compliqué. Selon l'installation de Python vous devez identifier le chemin vers le dossier `Scripts` qui contient les exécutables Python installés avec `pip`.

    Les conventions évoluent avec le temps. Voici un chemin possible :

    ```text
    C:\Users\username\AppData\Local\Programs\Python\Python3x\Scripts
    ```

## Installation des paquets principaux

Installons les paquets les plus couramment utilisés avec Python. Ouvrez un terminal et tapez les commandes suivantes :

```bash
pip install ipython numpy matplotlib pandas jupyterlab black flake8
```

## Environnement virtuel

Lorsque vous installez des paquets avec PIP, un système complexe de gestion de dépendences est mis en place. Par exemple si vous installez `numpy`, `matplotlib` sera installé automatiquement. Chaque paquet dépend d'autres paquets.

Il n'est pas rare d'avoir des conflits entre les versions des paquets. Par exemple, si vous avez un projet qui utilise `numpy` en version `1.20` et un autre projet qui utilise `numpy` en version `1.21`, vous aurez des problèmes.

Pour éviter ces problèmes, il est recommandé d'utiliser un environnement virtuel.

Un environnement virtuel est un dossier local au projet sur lequel vous travaillez qui contient une installation de Python, un gestionnaire de paquets PIP et un ensemble de paquets. Chaque environnement virtuel est indépendant des autres. Vous pouvez avoir autant d'environnements virtuels que vous le souhaitez.

La gestion d'environnement virtuels à beaucoup évolué avec les versions de Python. Il existe plusieurs outils que l'on peut confondre:

- `venv` est un module de la bibliothèque standard de Python depuis la version 3.3 qui permet de créer des environnements virtuels. Il est recommandé d'utiliser `venv` pour les projets personnels.
- `virtualenv` est un outil plus ancien disponible pour Python 2 et 3. Il n'est pas recommandé de l'utiliser.
- `poetry` est un outil externe. Utile pour tester des projets sur différentes versions de Python; facilite la migration entre les versions.

Pour créer un environnement virtuel avec `venv`, ouvrez un terminal et tapez les commandes suivantes :

=== "Linux/WSL"

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

=== "Windows"

    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate
    ```
