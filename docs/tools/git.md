# Git

![Fanart Git](/assets/images/git-wallhaven.png)

## Introduction

[Git](https://git-scm.com/) est un outil de gestion de versions. Il a été inventé par [Linus Torvalds](https://en.wikipedia.org/wiki/Linus_Torvalds) en 2005 pour gérer le développement du noyau Linux qui contient des millions de lignes de code devant être modifiées par des centaines de milliers de développeurs. Git a été conçu pour être rapide, efficace et pour gérer des projets de toutes tailles. Il est aujourd'hui le système de gestion de version le plus utilisé au monde.

Git est la suite logique des outils comme `CVS` ou [Subversion](https://subversion.apache.org/) qui étaient utilisés pour gérer des projets de développement de logiciels.

Git est avant tout un outil en ligne de commande. Son utilisation passe par la commande `git` suivi d'une sous-commande (`clone`, `pull`, `push`, `commit`, etc.). Il est possible de l'utiliser avec une interface graphique mais l'interface en ligne de commande est plus puissante, plus rapide et plus flexible.

Un dépôt (référentiel) Git est un dossier qui contient un dossier caché `.git`. Ce dossier contient l'historique des modifications du projet. Ne supprimez pas ce dossier, vous perdriez l'historique de votre projet. Lorsque vous faites des *commit* (sauvegarde incrémentationnelle), Git enregistre les modifications dans ce dossier caché et lorsque vous faites un *push* (envoi des modifications sur un serveur distant), Git envoie les modifications à un serveur distant (GitHub, GitLab, Bitbucket, etc.).

Par conséquent, l'utilisation de Git est intrincèquement liée à l'utilisation d'un serveur distant. Il est possible de travailler en local mais l'intérêt de Git est de pouvoir travailler en équipe. Il est possible de travailler sur une branche (version parallèle du projet) et de fusionner les modifications avec la branche principale (master).

Ceci implique de comprendre comment Git communique avec un serveur distant. Notons qu'il est possible de travailler avec plusieurs serveurs distants. Ils se configure avec la commande `git remote`. Deux protocoles de communication existent : `SSH ` et `HTTPS`. Le protocole `SSH` est plus sécurisé que `HTTPS` mais nécessite l'échange de clés cryptographiques. Le protocole `HTTPS` est plus simple à mettre en place mais demande un mot de passe ou un jeton d'authentification à chaque communication avec le serveur distant. La solution recommandée est d'utiliser `SSH`.

## Installation de Git

=== "Linux"

    Sous Linux, et particulièrement Ubuntu, Git est probablement déjà installé par défaut. Si ce n'est pas le cas, avec Ubuntu ouvrez un terminal Bash et tapez la commande suivante :

    ```bash
    sudo apt install git
    ```

    > [!NOTE]
    > Selon la distribution Linux que vous utilisez, les gestionnaires de paquets n'ont pas le même nom. Sous Fedora, le gestionnaire de paquets est `dnf` et sous Arch Linux, le gestionnaire de paquets est `pacman`. Néanmoins la commande reste très similaire.

=== "Windows"

    Pour installer Git sous Windows, le plus simple est d'utiliser le nouveau gestionnaire de paquet de Windows appelé `winget`. Ouvrez un terminal `PowerShell` et tapez la commande suivante issue de [Winget Git/Git](https://winget.run/pkg/Git/Git)

    ```powershell
    winget install -e --id Git.Git
    ```

=== "MacOS"

    Sous MacOS, Git est probablement déjà installé. Si ce n'est pas le cas, vous pouvez installer Git avec [Homebrew](https://brew.sh) en tapant la commande suivante dans un terminal :

    ```bash
    brew install git
    ```

## Configuration de Git

### Utilisateur et adresse e-mail

La première chose à faire après avoir installé Git est de le configurer. Ouvrez un terminal et tapez les commandes suivantes en veillant bien à remplacer `John Doe` par votre nom et `john.doe@acme.com` par votre adresse e-mail.

```bash
git config --global user.name "John Doe"
git config --global user.email john.doe@acme.com
```

Ces informations sont utilisées pour chaque *commit* que vous ferez. Elles sont importantes car elles permettent de savoir qui a fait une modification dans le projet. Ne vous trompez pas dans votre nom ou votre adresse e-mail, il est difficile de changer ces informations une fois qu'elles ont été enregistrées dans un *commit*, et surtout si elle ont été envoyées sur un serveur distant.

### Méthode de fusion (*merge*)

Lorsque vous utilisez la commande `git pull` pour récupérer les modifications d'un serveur distant, Git peut être amené à fusionner des modifications. Il est possible de choisir la méthode de fusion. Les deux méthodes les plus courantes sont `merge` et `rebase`. La méthode `merge` est la méthode par défaut. La méthode `rebase` est plus avancée et est utilisée pour réécrire l'historique du projet. Elle est plus propre mais elle peut être source de problèmes si elle est mal utilisée. Git s'attend à que vous configuriez laquelle des deux méthodes vous préférez. Vous pouvez le faire avec la commande suivante :

Pour le rebase :

```bash
git config --global pull.rebase true
```

Pour le merge :

```bash
git config --global pull.rebase false
```

!!! note

    La méthode `rebase` est plus propre mais elle peut être source de problèmes si elle est mal utilisée. Elle est recommandée pour les projets personnels mais pas pour les projets en équipe. En cas de doute privilégiez la méthode `merge`.

### Affichage de l'historique des commits (*log*)

Lorsque vous utilisez la commande `git log` pour afficher l'historique des *commits*, Git affiche les *commits* dans un format compact. Il est possible de personnaliser l'affichage de l'historique des *commits*. Vous pouvez le faire avec la commande suivante :

```bash
git config --global alias.lg "log -n30 --boundary --graph --pretty=format:'%C(bold blue)%h%C(bold green)%<|(20)% ar%C(reset)%C(white)% s %C(dim white)-% an%C(reset)%C(auto)% d%C(bold red)% N' --abbrev-commit --date=relative"
```

Dès lors vous utiliserez le raccourcis `lg` pour afficher l'historique des *commits* (`git lg`).

Pour afficher la date en format ISO 8601, vous pouvez utiliser la commande suivante :

```bash
git config --global alias.lga "log -n30 --boundary --graph --pretty=format:'%C(bold blue)%h%C(bold green)%<|(20)% ai%C(reset)%C(white)% s %C(dim white)-% an%C(reset)%C(auto)% d%C(bold red)' --abbrev-commit --date=iso"
```

### Configuration SSH

Comme nous l'avons vu, Git peut communiquer avec un serveur distant en utilisant le protocole `SSH`. Pour cela, il est nécessaire de configurer une clé cryptographique.

La première chose à faire est de vérifier si vous avez déjà une clé SSH. Ouvrez un terminal et tapez la commande suivante :

```bash
$ ls -al ~/.ssh/*.pub
-rw-r--r-- 1 ycr ycr 393 2023-09-06 08:38 /home/ycr/.ssh/id_rsa.pub
```

Le fichier `id_rsa.pub` est votre clé publique. Si vous ne voyez pas ce fichier, c'est que vous n'avez pas de clé SSH. Vous pouvez en générer une avec la commande suivante :

```bash
ssh-keygen
```

Sous Windows, la commande est la même mais vous devez lancer `Git Bash` pour l'exécuter. Vous pouvez lancer `Git Bash` en tapant `Git Bash` dans le menu de recherche de Windows.

### Configuration de GitHub

Si vous utilisez GitHub, il est nécessaire de configurer votre clé SSH dans votre compte GitHub. Pour cela, ouvrez un terminal et tapez la commande suivante :

```bash
$ cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+yNp7af6zI8NINIFX1aRj+nzKksZ6XzBSkgA/
iuPpYIGz5SSZOkwkvN0DnX8J42DcuEK/mnu3+f9Wh746823gxhXqt+7Wv9z9DJ9O9qrsYlnxIMip
oqepE/Xt+jE5Yv8ullIdsvZdzY611R5DFwrVswslz9OdmpH6nWCmnY/cGZva79ngdcvJLKFk++fl
+Be1xshWt24svawRH7Fdxn8VyUKmP2Twy6iMo3MT9xGe5leV1CiTXfkzLYntNV50/dtzQN+pwcwR
BdXBP9FdO9+IzieY6bUGttT6t2VcWoK6jFF+i94Chl/FeGvRU1X/QzSP3SYT2biNRNmznSIa2VD
ycr@heig-vd
```

Copiez la clé publique et collez-la dans votre compte GitHub. Pour cela, ouvrez votre navigateur et allez sur [GitHub](https://github.com). Connectez-vous à votre compte et cliquez sur votre photo de profil en haut à droite. Cliquez sur `Settings` puis sur `SSH and GPG keys`. Cliquez sur `New SSH key` et collez votre clé publique dans le champ `Key`. Donnez un nom à votre clé et cliquez sur `Add SSH key`.

## Commandes utiles

| Commande                   | Description                                                |
| -------------------------- | ---------------------------------------------------------- |
| `git init`                 | Initialise un dépôt Git dans le répertoire courant         |
| `git clone <address>`      | Clone un dépôt distant dans le répertoire courant          |
| `git status`               | Affiche l'état du dépôt                                    |
| `git add <file>`           | Ajoute des fichiers à l'index                              |
| `git commit -am "message"` | Enregistre les modifications dans l'historique du dépôt    |
| `git pull`                 | Récupère les modifications du serveur distant              |
| `git push`                 | Envoie les modifications sur le serveur distant            |
| `git log`                  | Affiche l'historique des *commits*                         |
| `git lg`                   | Affiche l'historique des *commits* de manière plus lisible |
