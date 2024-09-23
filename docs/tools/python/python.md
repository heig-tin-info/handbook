# Python

![Un python informaticien](/assets/images/python.png)

## Introduction

Python est un langage de programmation comme le C mais il est plus haut niveau. Cela signifie d'une que Python est plus facile à apprendre et à utiliser que le C. Python est un langage interprété, car le code source est exécuté directement par un interpréteur sans nécessairement passer par une étape de compilation.

C'est un langage très populaire pour l'enseignement de la programmation et pour la science des données. Python est utilisé dans de nombreux domaines, tels que l'intelligence artificielle, l'apprentissage automatique, l'analyse de données, la programmation web, la programmation système, etc.

Guido van Rossum a créé Python en 1991. Il en a été le [BDFL](https://fr.wikipedia.org/wiki/Benevolent_dictator_for_life) (dictateur bienveillant à vie) jusqu'en 2018 où il a décidé de se retirer de la direction du projet en raison de désaccords avec la communauté Python. Cette date marque un tournant dans l'histoire de Python qui devient un langage communautaire avec ses avantages et ses inconvénients. L'avantage est que Python est beaucoup plus dynamique et innovant. L'inconvénient est qu'il change rapidement et que les versions ne sont pas toujours compatibles entre elles.

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

## Configuration des variables d'environnement

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

Lorsque vous installez des paquets avec PIP, un système complexe de gestion de dépendances est mis en place. Par exemple, si vous installez `numpy`, `matplotlib` sera installé automatiquement. Chaque paquet dépend d'autres paquets.

Il n'est pas rare d'avoir des conflits entre les versions des paquets. Par exemple, si vous avez un projet qui utilise `numpy` en version `1.20` et un autre projet qui utilise `numpy` en version `1.21`, vous aurez des problèmes.

Pour éviter ces problèmes, il est recommandé d'utiliser un environnement virtuel.

Un environnement virtuel est un dossier local au projet sur lequel vous travaillez qui contient une installation de Python, un gestionnaire de paquets PIP et un ensemble de paquets. Chaque environnement virtuel est indépendant des autres. Vous pouvez avoir autant d'environnements virtuels que vous le souhaitez.

La gestion d'environnement virtuel a beaucoup évolué avec les versions de Python. Il existe plusieurs outils que l'on peut confondre:

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

## Poetry

Poetry est un outil de gestion de dépendances pour Python. Il permet de gérer les dépendances de votre projet, de créer des environnements virtuels, de gérer les versions de Python, de publier des paquets sur PyPI, etc.

Il est une excellente alternative à `venv` et `pip` car en plus de gérer les dépandances, il peut gérer différentes versions de Python.

Si vous voulez créer un projet Python avec Poetry, ouvrez un terminal et tapez les commandes suivantes :

```bash
mkdir myproject
cd myproject
poetry init
```

Ensuite pour ajouter des dépendances à votre projet, utilisez `poetry add` :

```bash
poetry add numpy matplotlib pandas
```

Il est également possible d'ajouter des paquets de développement avec `poetry add --dev` :

```bash
poetry add --group dev black flake8
```

Ces commandes vont créer un fichier de configuration nommé `pyproject.toml` qui contient toutes les informations sur votre projet et ses dépendances. L'avantage est qu'en mettant ce fichier sous Git, lorsque vous clonez votre projet sur une autre machine, il suffit de taper `poetry install` pour installer toutes les dépendances.

Par défaut poetry ne crée pas d'enviroonement virtuel. Pour activer l'environnement virtuel, tapez la commande suivante :

```bash
poetry shell
```

Alternativement si l'objectif est simplement d'exécuter une commande dans l'environnement virtuel, utilisez `poetry run` :

```bash
poetry run python main.py
```

## Pipx

`pipx` est un outil qui permet d'installer des paquets Python en dehors de l'environnement virtuel. Cela permet d'installer des paquets Python comme des exécutables. Par exemple, si vous voulez installer `black` ou `flake8` pour formater votre code, vous pouvez les installer avec `pipx` :

```bash
pipx install black
```

Par défaut à partir de Ubuntu 24.04, `pip` n'est plus conseillé pour installer des paquets Python. Le PEP 668 ayant été accepé, la notion de [Externally Managed Environment](https://packaging.python.org/en/latest/specifications/externally-managed-environments/#externally-managed-environments) a été introduite.

Il y a plusieurs méthodes pour installer des paquets dans une distributions Linux :

1. `pip install ...`
2. `apt install python3-...`

La première méthode est la plus courante mais elle peut créer des problèmes de compatibilité entre les paquets. Comme ces derniers sont installés pour l'utilisateur courant, une version plus récente de `numpy` ne serait possiblement pas compatible avec un paquet Ubuntu qui dépendrait d'une version plus ancienne de `numpy`.

Il est préférable alors d'utiliser la version `apt` autant que possible.

Alternativement, pour les outils en ligne de commande, il est possible d'utiliser `pipx` qui installe les paquets dans un environnement virtuel et crée des liens symboliques vers les exécutables dans le répertoire `~/.local/bin`.

## Analyse syntaxique et formatage

Il y a plétore d'outils pour analyser la syntaxe et formater le code Python. Les paquets `flake8`, `pylint`, `isort`, `bandit` ont été très populaires mais il est aujourd'hui recommandé d'utiliser:

1. `black` pour le formatage du code
2. `ruff` pour l'analyse syntaxique
3. `mypy` pour le typage statique