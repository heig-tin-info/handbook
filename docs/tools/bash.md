# Bash (Ligne de commande)

La maîtrise de la ligne de commande n'est pas indispensable pour ce cours, mais la compréhension de quelques commandes est utile pour bien comprendre les exemples donnés.

Dans un environnement **POSIX** l'interaction avec le système s'effectue pour la plupart du temps via un terminal. Le programme utilisé pour interagir avec le système d'exploitation est appelé un [interpréteur de commande](https://en.wikipedia.org/wiki/Command-line_interface#Command-line_interpreter). Sous Windows vous utilisez le programme `cmd.exe` ou `PowerShell.exe`. Sous Linux vous utilisez très souvent un dérivé de [Bourne shell](https://en.wikipedia.org/wiki/Bourne_shell) nom éponyme de [Stephen Bourne](https://en.wikipedia.org/wiki/Stephen_R._Bourne) et apparu en 1979. La compatibilité est toujours maintenue aujourd'hui via son successeur [Bash](<https://en.wikipedia.org/wiki/Bash_(Unix_shell)>) dont le nom est un acronyme de *Bourne-again shell*.

Bash est écrit en C et les sources sont naturellement disponibles sur internet. Lorsque vous lancez Bash, vous aurez un simple prompt :

```console
$
```

Ce dernier vous invite à taper une commande laquelle est le plus souvent le nom d'un programme. Voici un exemple :

```console
$ cat foo.txt | hexdump -C -n100
```

## Navigation

Pour naviguer dans l'arborescence, le programme `cd` est utilisé. Il est l'acronyme de *change directory*. Ce programme prend en argument un chemin relatif ou absolu.

```console
$ cd /usr
/usr$ cd bin
/usr/bin$ cd .
/usr/bin$ cd ..
/usr/$ cd /var/tmp
/var/tmp$ cd
~$
```

La dernière commande est singulière : si `cd` est appelé sans argument, il nous ramène dans notre répertoire personnel nommé *home* et abbrégé `~`.

## Affichage

L'affichage du contenu courant de l'arborescence est possible avec le programme `ls` pour *list structure*.

```console
$ ls /usr/bin/as*
/usr/bin/as                 /usr/bin/asciitopgm     /usr/bin/assistant
/usr/bin/asan_symbolize     /usr/bin/aspell         /usr/bin/asy
/usr/bin/asan_symbolize-10  /usr/bin/aspell-import
$ ls -al /usr/bin/as*
-rwxr-xr-x 1 root root  38K 2020-04-20 07:12 /usr/bin/asan_symbolize-10
-rwxr-xr-x 1 root root 9.9K 2016-04-23 13:53 /usr/bin/asciitopgm
-rwxr-xr-x 1 root root 167K 2020-03-22 16:33 /usr/bin/aspell
-rwxr-xr-x 1 root root 2.0K 2020-03-22 16:33 /usr/bin/aspell-import
lrwxrwxrwx 1 root root    9 2020-03-22 16:55 /usr/bin/assistant -> qtchooser
-rwxr-xr-x 1 root root 4.3M 2020-02-10 15:52 /usr/bin/asy
```

On utilise souvent les options `a` (pour *all*) et `l` (pour *long*) permettant d'afficher les résultats avec plus de détails. Dans l'ordre on peut lire les permissions du fichier, le propriétaire, le groupe, la taille du fichier, sa date de dernière modification et enfin son nom.

## Pipe

Le signe pipe `|` permet de rediriger le flux de sortie d'un programme vers le flux d'entrée d'un autre programme et ainsi les exécuter à la chaîne.

% code-block::text
%
% $ echo "Bonjour" | cowsay

Il se peut que vous souhaitiez rediriger la sortie d'erreur vers la sortie standard et ainsi concaténer les deux flux sur l'entrée standard d'un autre programme.

% code-block::text
%
% $ echo "Bonjour" 2>&1 | cowsay
