# Windows

## MSVC (Microsoft Visual C++)

[MSVC](https://fr.wikipedia.org/wiki/Microsoft_Visual_C%2B%2B) est le compilateur C++ de Microsoft. Il est inclus dans [Visual Studio](https://fr.wikipedia.org/wiki/Microsoft_Visual_Studio) et est souvent utilisé pour compiler des programmes Windows. Historiquement, MSVC a toujours été un peu en retrait par rapport au support des standards modernes du langage C, notamment C99, C11, C18 et maintenant C23. Alors que le compilateur suit de très près les standards C++, il ne supporte pas aussi bien les évolutions du langage C.

Pour installer MSVC, vous devez télécharger [Visual Studio](https://visualstudio.microsoft.com/fr/) depuis le site web de Microsoft. L'installation de Visual Studio est assez lourde, car elle installe de nombreux composants qui ne sont pas nécessaires pour la compilation de programmes C/C++.

## MSYS2

[MSYS2](https://www.msys2.org/) est un environnement de développement qui fournit un shell Unix-like et des outils GNU pour Windows. Il est basé sur Cygwin et utilise le gestionnaire de paquets [Pacman](https://wiki.archlinux.org/title/Pacman) de [Arch Linux](https://fr.wikipedia.org/wiki/Arch_Linux).

MSYS2 est un excellent choix pour compiler des programmes en C/C++ qui peuvent être exécutés nativement sous Windows. Le compilateur [MinGW-w64](https://fr.wikipedia.org/wiki/MinGW) est une variante de GCC qui permet de compiler des binaires au format PE (Portable Executable) pour Windows.

L'installation de MSYS2 est assez simple. Une approche consiste à télécharger l'exécutables d'installation depuis le site web de MSYS2 et à l'exécuter. Ma préférence va pour `winget` disponible nativement sur Windows 10/11.

```cmd
winget install -e --id MSYS2.MSYS2
```

Une fois installé, vous pouvez ouvrir le programme `MSYS2 MINGW64` qui tourne dans un terminal `mintty` un peu archaïque. Il est préférable d'utiliser Windows Terminal. Pour ce faire il faut configurer un profil pour MSYS2.

1. Ouvrir Windows Terminal
2. Utiliser ++Ctrl+Shift+,++ pour ouvrir le fichier de configuration JSON
3. Allez à la section `"profiles"` et ajouter un nouvel élément pour MSYS2:

    ```json
    {
        "colorScheme": "Campbell",
        "commandline": "\"C:\\\\msys64\\\\usr\\\\bin\\\\bash.exe\" --login -i -c \"cd ~ && /usr/bin/env MSYSTEM=MINGW64 bash\"\r",
        "guid": "{cffe7ad8-1ccd-43ea-99d9-d3dff62b8a02}",
        "hidden": false,
        "icon": "C:\\msys64\\mingw64.ico",
        "name": "MinGW",
        "startingDirectory": "~"
    }
    ```

4. Attention à bien adapter le chemin et veillez à ce que le fichier JSON soit bien formé, c'est à dire que les virgules soient bien placées.
5. Sauvegarder le fichier JSON et fermer Windows Terminal
6. Ouvrir Windows Terminal et sélectionner le profil MinGW dans le menu déroulant.

Le terminal que vous avez est très similaire à celui de WSL. L'installation de paquets est sensiblement différente de celle de `apt` ou `yum`. Pour installer un paquet, il suffit de lancer la commande `pacman -S nom-du-paquet`. Par exemple, pour installer `git`, il suffit de lancer la commande suivante:

```bash
pacman -S git
```

Pour rechercher un paquet, vous pouvez utiliser la commande `pacman -Ss nom-du-paquet`.

Afin de pouvoir récupérer des projets GitHub avec votre clé SSH, vous devez soit:

1. Générer une nouvelle clé SSH pour MSYS2 et l'ajouter à votre compte GitHub.
2. Utiliser la clé SSH existante en la copiant dans le dossier `~/.ssh` de MSYS2.

La première option est préférable. Pour générer une nouvelle clé SSH, vous pouvez utiliser les commande suivantes.

```bash
ssh-keygen
cat ~/.ssh/id_rsa.pub
```