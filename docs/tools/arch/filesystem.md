# Système de fichier

![Fourmi portant des données](/assets/images/ant.png)

Un *système de fichier* est une structure de données qui permet de stocker des fichiers et des répertoires sur un support de stockage. Les systèmes de fichiers sont utilisés pour organiser les données sur les disques durs, les clés USB, les cartes mémoire, etc.

Nous savons maintenant que les données informatiques sont stockées sous forme binaire. Sur une clé USB ou un disque dur, c'est pareil. On aura des 0 et des 1 stockés à perte de vue sur le silicium. Si votre disque dur de 1 Tio est la surface de la terre, sans les océans et d'environ $148.9$ millions de $\text{km}^2$. Notre disque contient $2^{40}$ octets, soit $2^{43}$ bits :

$$
N_{bits} = 8'796'093'022'208
$$

Cela revient à stocker environ 16 bits par millimètre carré. Une fourmi aurait sur son dos 2 à 3 octets de données. Imaginez vous un instant prendre l'avion, le train, revêtir votre tenue d'explorateur pour chercher les fourmis qui portent les données que vous cherchez ?

Oui ce n'est pas très réaliste, et le calcul que nous avons fourni est très simplifié. Mais cela permet de comprendre que les données stockées doivent être organisées car elles ne sont pas accessibles immédiatement. Pour un disque dur, la tête de lecture doit parcourir le disque pour atteindre les données. Sur une clé USB, la mémoire doit être configurée pour accéder une région précise.

Nous avons donc besoin d'une carte pour savoir où sont stockées les données. C'est le rôle du système de fichier. Il permet de stocker les fichiers, les organiser en dossiers. N'importe qui n'aura pas accès à toutes les données, il faut les droits d'accès. Et les données peuvent être corrompues, détruites par des [rayonnements cosmiques](https://fr.wikipedia.org/wiki/Rayonnement_cosmique). Il faut aussi gérer les erreurs.

Le premier système de fichier a été inventé par IBM en 1956 pour le disque dur IBM 305 RAMAC. Il s'appelait le *système de fichier à index*. Il a été inventé par Hans Peter Luhn. Il permettait de stocker 5 Mo de données sur un disque de 24 pouces. Depuis

## FAT et les autres

Le système de fichier FAT (File Allocation Table) est un système de fichier simple et robuste. Il a été inventé par Microsoft en 1977 pour le système d'exploitation MS-DOS. Il est toujours utilisé aujourd'hui pour les clés USB, les cartes mémoire, etc. C'est très certainement celui-ci qu'un ingénieur embarqué utiliserait sur une carte SD interfacée avec un microcontrôleur.

L'API de FAT, c'est-à-dire les fonctions primitives pour contrôler le système de fichier contient par exemple les fonctions suivantes :

- `fopen` : Ouvrir un fichier à partir d'un chemin
- `fread` : Lire de données depuis un fichier ouvert
- `fseek` : Se déplacer dans un fichier ouvert
- `fsize` : Obtenir la taille d'un fichier
- `fopendir` : Ouvrir un répertoire
- `frename` : Renommer un fichier
- `fmkdir` : Créer un répertoire
- ...

Les systèmes de fichiers les plus utilisés aujourd'hui sont :

Table: Quelques systèmes de fichiers

| Système de fichier | Année | Utilisation              |
| :----------------- | :---- | :----------------------- |
| FAT                | 1977  | Clés USB, cartes mémoire |
| FAT32              | 1996  | Disques durs             |
| NTFS               | 1993  | Windows                  |
| ext4               | 2006  | Linux                    |
| APFS               | 2017  | macOS                    |
| Btrfs              | 2009  | Linux                    |
| ZFS                | 2005  | Solaris, FreeBSD         |

## Organisation

Un système de fichier comporte en général :

- Des répertoires (des dossiers) qui contiennent des fichiers ou d'autres répertoires.
- Des fichiers qui contiennent des données.

Les répertoires sont organisés en arborescence de manière hiérarchique. Si vous avez dans votre maison, dans votre cuisine, dans votre frigo, au second rayonnage, sur la droite, une pomme. Vous pourriez écrire :

```
maison -> cuisine -> frigo -> rayonnage2 -> droite -> pomme
```

Mais la pomme est un fruit, comment le savoir avec seulement un nom. C'est peut-être une pomme de terre, une pomme de pin ou une pomme de douche. Généralement, on ajoute une extension, c'est un suffixe qui permet de savoir de quel type de fichier il s'agit. Par exemple, `.txt` pour un fichier texte, `.jpg` pour une image, `.c` pour un fichier source en langage C, etc.

Enfin, utiliser `->` pour indiquer la hiérarchie n'est pas pratique. Tous les systèmes de fichiers du monde utilisent le *slash* `/` pour séparer les répertoires. Tous... sauf un qui résiste encore et toujours à l'envahisseur. Sur Windows, la convention est différente, et c'est le *backslash* qui est utilisé `\`. C'est une source de confusion pour les développeurs qui doivent écrire des programmes compatibles avec les deux systèmes d'exploitation.

Reprenons. Notre pomme serait un fruit, une image de fruit. On indiquerait alors son chemin complet :

```
/maison/cuisine/frigo/rayonnage2/droite/pomme.jpg
```

Tiens ? Pourquoi un `slash` au début ? C'est pour indiquer le répertoire racine : le répertoire d'origine, le point de départ de l'arborescence. Évidemment si vous vous trouvez déjà dans la cuisine, vous n'avez pas besoin de préciser `/maison/cuisine`. Vous pouvez simplement écrire : `frigo/rayonnage2/droite/pomme.jpg`. Donc un chemin peut, ou non avoir un `slash` au début. On dit qu'il est **absolu** ou **relatif**.

!!! note "Windows"

    Sur Windows, le répertoire racine est `C:\` pour le disque dur principal. Donc un chemin absolu sur Windows ressemblerait à :

    ```txt
    C:\maison\cuisine\frigo\rayonnage2\droite\pomme.jpg
    ```

    L'usage de `C` est historique. À l'origine il n'y avait pas de disques durs mais des disquettes. Ceux qui avaient la chance d'avoir un lecteur de disquette avaient un unique lecteur `A`. Ceux qui voulaient faire des copies de disquettes devaient en avoir un deuxième, c'était le lecteur `B`. En général, le disque dur était le troisième lecteur, le lecteur `C`. Et depuis Windows 95, c'est resté comme ça.

## Navigation

Nous savons qu'un chemin est une suite de répertoires séparés par des slashes mais ce que nous ne savons pas c'est où on se trouve. Lorsque vous ouvrez un terminal, ou une application vous êtes dans un répertoire, c'est le répertoire courant, ou le répertoire de travail (*working directory*). Pour savoir où vous trouvez vous pouvez ouvrir un terminal et taper :

=== "POSIX"

    ```bash
    $ pwd
    /home/username
    ```

=== "Windows"

    ```cmd
    > cd
    C:\Users\username
    ```

Mais si je suis dans la maison et que je veux aller dans le jardin ? Je ne vais pas indiquer le chemin complet :

```bash
/universe/
    galaxy/
        solar-system/
            earth/
                europe/
                    switzerland/
                        vaud/
                            yverdon-les-bains/
                                maison/
                                    jardin
```

Je ne peux pas non plus utiliser le chemin relatif `jardin` car le jardin n'est pas dans la maison. Ni d'ailleurs `/jardin` car celui-ci n'est pas à la racine de l'univers. On voit qu'il est essentiel d'introduire une notion de parenté ; ce que je souhaite faire c'est remonter d'un niveau pour aller dans le jardin.

Il existe un fichier spécial qui permet de remonter d'un niveau c'est le fichier `..`.

Et si je suis dans le jardin et que j'aimerais tondre la pelouse. J'aimerais appeler le programme `tondre` en lui donnant le chemin jusque là où je me trouve. Je pourrais écrire : `../jardin` mais c'est redondant, et cela implique de connaître le nom de là ou je me trouve. Il existe pour cela un deuxième fichier spécial qui permet de désigner le répertoire courant, c'est le fichier `.`.

Enfin, si je souhaite me déplacer dans l'arborescence, je peux utiliser la commande `cd` pour *change directory*. Ce programme prend en argument un chemin absolu ou relatif.

## Commandes utiles

=== "POSIX"

    | Commande | Description                       | Exemple                                             |
    | -------- | --------------------------------- | --------------------------------------------------- |
    | `pwd`    | Affiche le répertoire courant     | `/home/username`                                    |
    | `cd`     | Change de répertoire              | `cd /home/username`                                 |
    | `ls`     | Liste les fichiers et répertoires | `ls`                                                |
    | `mkdir`  | Crée un répertoire                | `mkdir -p /home/username`                           |
    | `rmdir`  | Supprime un répertoire            | `rmdir /home/username`                              |
    | `touch`  | Crée un fichier vide              | `touch /home/username/file.txt`                     |
    | `rm`     | Supprime un fichier               | `rm /home/username/file.txt`                        |
    | `mv`     | Déplace un fichier                | `mv /home/username/file.txt /home/username/backup/` |
    | `cp`     | Copie un fichier                  | `cp /home/username/file.txt /home/username/backup/` |

=== "Windows CMD"

    | Commande | Description                       | Exemple                                                     |
    | -------- | --------------------------------- | ----------------------------------------------------------- |
    | `cd`     | Affiche le répertoire courant     | `cd`                                                        |
    | `cd`     | Change de répertoire              | `cd C:\Users\username`                                      |
    | `dir`    | Liste les fichiers et répertoires | `dir`                                                       |
    | `mkdir`  | Crée un répertoire                | `mkdir C:\Users\username\backup`                            |
    | `rmdir`  | Supprime un répertoire            | `rmdir C:\Users\username\backup`                            |
    | `echo`   | Crée un fichier vide              | `echo. > C:\Users\username\file.txt`                        |
    | `del`    | Supprime un fichier               | `del C:\Users\username\file.txt`                            |
    | `move`   | Déplace un fichier                | `move C:\Users\username\file.txt C:\Users\username\backup\` |
    | `copy`   | Copie un fichier                  | `copy C:\Users\username\file.txt C:\Users\username\backup\` |

=== "Windows PowerShell"

    | Commande | Description                       | Exemple                                                   |
    | -------- | --------------------------------- | --------------------------------------------------------- |
    | `pwd`    | Affiche le répertoire courant     | `pwd`                                                     |
    | `cd`     | Change de répertoire              | `cd C:\Users\username`                                    |
    | `ls`     | Liste les fichiers et répertoires | `ls`                                                      |
    | `mkdir`  | Crée un répertoire                | `mkdir C:\Users\username\backup`                          |
    | `rmdir`  | Supprime un répertoire            | `rmdir C:\Users\username\backup`                          |
    | `echo`   | Crée un fichier vide              | `echo. > C:\Users\username\file.txt`                      |
    | `rm`     | Supprime un fichier               | `rm C:\Users\username\file.txt`                           |
    | `mv`     | Déplace un fichier                | `mv C:\Users\username\file.txt C:\Users\username\backup\` |
    | `cp`     | Copie un fichier                  | `cp C:\Users\username\file.txt C:\Users\username\backup\` |

!!! note "Windows"

    On voit que Microsoft a appris de ses erreurs et a introduit `pwd` et `ls` dans PowerShell. C'est une bonne chose car ces commandes sont très utiles. PowerShell est un shell plus moderne que CMD et plus puissant. Il est basé sur le framework .NET et permet d'interagir avec des objets .NET.

!!! warning

    Les commandes `rm`, `mv`, `cp` sont très dangereuses. Elles peuvent détruire des données. Il est important de faire attention à ce que vous faites. Il est recommandé de faire des sauvegardes régulières de vos données.

## Permissions

Les systèmes de fichiers modernes permettent de définir des permissions sur les fichiers et les répertoires. Ces permissions permettent de contrôler qui peut lire, écrire ou exécuter un fichier. Les permissions sont définies pour trois catégories d'utilisateurs :

- Le propriétaire du fichier
- Le groupe auquel appartient le fichier
- Les autres utilisateurs

Les permissions sont définies pour trois actions :

- Lire le fichier
- Écrire dans le fichier
- Exécuter le fichier

Les permissions sont représentées par des lettres :

- `r` pour lire
- `w` pour écrire
- `x` pour exécuter

Les permissions sont affichées par la commande `ls -l` dans POSIX. Sous Windows ce n'est pas aussi simple. Les permissions sont affichées par la commande `icacls` mais le format est différent.

!!! note "NTFS"

    Le système de fichier NTFS (New Technology File System) de Microsoft permet de définir des permissions très fines sur les fichiers et les répertoires. Il permet de définir des permissions pour des utilisateurs individuels ou des groupes d'utilisateurs. Il permet aussi de chiffrer les données pour les protéger contre les accès non autorisés.

    Les commandes sont donc beaucoup plus complexes et ne se réduisent pas aux permissions que l'on explique ici.

    Cette granularité est très utile dans un environnement professionnel où les données sont sensibles mais cela peut être un cauchemar pour les administrateurs système et surtout cela rend le système plus lent car il doit vérifier toutes les permissions à chaque accès disque.

Pour changer une permission, on utilise la commande `chmod` dans POSIX. Sous Windows il est préférable de passer par l'interface graphique.

Table: Commandes utiles pour les permissions

| Description                             | Exemple              |
| :-------------------------------------- | :------------------- |
| Ajouter l'exécution sur un fichier      | `$ chmod +x program` |
| Retirer l'exécution sur un fichier      | `$ chmod -x program` |
| Ajouter l'écriture pour le groupe       | `$ chmod g+w file`   |
| Retirer l'écriture pour les autres      | `$ chmod o-w file`   |
| Ajouter la lecture pour tous            | `$ chmod a+r file`   |
| Retirer tous les droits pour les autres | `$ chmod o-rwx file` |
| Changer les permissions pour tous       | `$ chmod 777 file`   |

!!! note "Représentation octale"

    Dans un environnement POSIX, on peut représenter les permissions avec des chiffres. Chaque permission est représentée par un bit :

    - `r` : 4
    - `w` : 2
    - `x` : 1

    On additionne les bits pour obtenir la permission :

    - `rwx` : 7
    - `rw-` : 6
    - `r-x` : 5

    Chaque chiffre représente dans l'ordre le propriétaire, le groupe et les autres. Ainsi la permission du fichier `~/.ssh/id_rsa` est `400` ce qui signifie que le propriétaire a le droit de lire le fichier mais ni d'écrire ni d'exécuter. Le groupe et les autres n'ont aucun droit. C'est normal c'est la clé privée SSH, elle ne doit être lue que par le propriétaire.

## Propriétaire et groupe

Chaque fichier a un propriétaire et un groupe. Le propriétaire est l'utilisateur qui a créé le fichier. Le groupe est le groupe auquel appartient le fichier. Les utilisateurs peuvent appartenir à plusieurs groupes. Les groupes permettent de définir des permissions pour plusieurs utilisateurs. Par exemple, un groupe `admin` pourrait avoir des droits d'écriture sur un répertoire.

Pour changer le propriétaire d'un fichier, on utilise la commande `chown` dans POSIX. Sous Windows, il est préférable de passer par l'interface graphique.

Table: Commandes utiles pour les propriétaires et les groupes

| Description                          | Exemple                        |
| :----------------------------------- | :----------------------------- |
| Changer le propriétaire d'un fichier | `$ chown username file`        |
| Changer le groupe d'un fichier       | `$ chgrp group file`           |
| Ajouter un utilisateur à un groupe   | `$ usermod -aG group username` |
| Retirer un utilisateur d'un groupe   | `$ gpasswd -d username group`  |
| Créer un groupe                      | `$ groupadd group`             |
| Supprimer un groupe                  | `$ groupdel group`             |
| Lister les groupes d'un utilisateur  | `$ groups username`            |

## ACL (Access Control List)

Les systèmes de fichiers modernes permettent de définir des ACL (Access Control List) sur les fichiers et les répertoires. Les ACL permettent de définir des permissions plus fines que les permissions POSIX. Les ACL permettent de définir des permissions pour des utilisateurs individuels ou des groupes d'utilisateurs. Les ACL sont plus complexes à gérer que les permissions POSIX mais elles permettent de définir des permissions plus précises.

En général, les ACL sont gérées par des outils graphiques ou des commandes spécifiques. Les ACL sont stockées dans les métadonnées des fichiers et des répertoires. Les ACL sont utilisées dans les environnements professionnels où les données sont sensibles et où il est nécessaire de définir des permissions très précises. Cela permet de se rapprocher de systèmes de fichiers comme NTFS de Microsoft.

Sur votre ordinateur ou dans votre carrière professionnelle vous n'aurez très certainement jamais besoin de gérer des ACL. C'est un sujet complexe et réservé aux administrateurs système. Mais pour les plus curieux voici quelques exemples:

| Description                      | Exemple                            |
| :------------------------------- | :--------------------------------- |
| Afficher les ACL d'un fichier    | `$ getfacl file`                   |
| Modifier les ACL d'un fichier    | `$ setfacl -m u:username:rwx file` |
| Supprimer les ACL d'un fichier   | `$ setfacl -b file`                |
| Copier les ACL d'un fichier      | `$ getfacl file1                   | setfacl --set-file=- file2` |
| Sauvegarder les ACL d'un fichier | `$ getfacl file > file.acl`        |
| Restaurer les ACL d'un fichier   | `$ setfacl --restore=file.acl`     |

## Manipulation bas niveau

Une question que l'on peut se poser est s'il est possible d'accéder aux données brutes d'un disque dur (les 1 et les 0) : la réponse est oui. Il est possible d'accéder aux données brutes d'un disque dur en utilisant des outils spécifiques. Ces outils permettent de lire et d'écrire des données directement sur le disque dur sans passer par le système de fichiers.

La commande `dd` dans POSIX permet de lire et d'écrire des données brutes sur un disque dur. Cette commande est très puissante et **très dangereuse**. Elle permet de lire et d'écrire des données directement sur le disque dur. Il est très facile de détruire des données avec cette commande.

On peut utiliser des fichiers spéciaux comme `/dev/zero` ou `/dev/random` pour générer des fichiers de données.

Par exemple créer un fichier de 1 Mio rempli de zéros :

```bash
$ dd if=/dev/zero of=file bs=1M count=1
```

Ou créer un fichier de 100 bytes rempli de données aléatoires :

```bash
$ dd if=/dev/random of=file bs=100 count=1
```

On peut aussi lire des données brutes sur un disque dur. Par exemple lire les 100 premiers bytes d'un disque dur :

```bash
$ dd if=/dev/sda of=file bs=100 count=1
```

## Arborescence POSIX

L'arborescence POSIX est une convention pour organiser les fichiers et les répertoires sur un système de fichiers. L'arborescence POSIX est utilisée par la plupart des systèmes d'exploitation basés sur UNIX. L'arborescence POSIX est organisée de la manière suivante :

- `/` : Le répertoire racine
- `/bin` : Les programmes de base
- `/boot` : Les fichiers de démarrage
- `/dev` : Les fichiers de périphériques
- `/etc` : Les fichiers de configuration
- `/home` : Les répertoires des utilisateurs
- `/lib` : Les bibliothèques partagées
- `/media` : Les points de montage des périphériques amovibles
- `/mnt` : Les points de montage des périphériques
- `/opt` : Les logiciels optionnels
- `/proc` : Les informations sur les processus
- `/root` : Le répertoire de l'administrateur
- `/tmp` : Les fichiers temporaires
- `/usr` : Les programmes et les fichiers partagés
- `/var` : Les fichiers variables
- `/srv` : Les données des services
- `/sys` : Les informations sur le noyau

!!! note "Windows"

    Malheureusement Windows n'a pas vraiment de convention rigide pour l'organisation des fichiers et des répertoires. Chaque programme peut décider où il veut stocker ses fichiers de configuration, ses fichiers de données, etc. Cela rend la maintenance et la sauvegarde des données plus difficile. On peut néanmoins retrouver quelques répertoires communs :

    - `C:\Program Files` : Les programmes installés
    - `C:\Program Files (x86)` : Les programmes 32 bits installés sur un système 64 bits
    - `C:\Users` : Les répertoires des utilisateurs
    - `C:\Windows` : Les fichiers du système d'exploitation
    - `C:\Windows\System32` : Les fichiers du système d'exploitation 64 bits
    - `C:\Windows\SysWOW64` : Les fichiers du système d'exploitation 32 bits sur un système 64 bits
    - `C:\Temp` : Les fichiers temporaires
    - `C:\Users\username\AppData` : Les fichiers de configuration des programmes
    - `C:\Users\username\Documents` : Les documents de l'utilisateur
    - `C:\Users\username\Downloads` : Les fichiers téléchargés
