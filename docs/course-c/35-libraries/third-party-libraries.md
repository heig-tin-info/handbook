# Autres bibliothèques

Les bibliothèques tierces constituent des ensembles cohérents de fonctions et de types de données, conçus pour être intégrés dans des programmes informatiques. Leur objectif est d'étendre les fonctionnalités d'un projet sans nécessiter la réécriture de code existant. Provenant généralement de développeurs ou d'organisations externes, ces bibliothèques permettent de gagner en efficacité tout en garantissant la robustesse et la maintenance du code.

## Installation de bibliothèques tierces

Sous Linux, les bibliothèques tierces sont généralement disponibles via les gestionnaires de paquets de la distribution. Il suffit de rechercher le nom de la bibliothèque et de l'installer à l'aide de la commande appropriée. Par exemple, pour installer la bibliothèque `curl` il faut ajouter le préfixe `lib` et le suffixe `-dev` . Le prefixe indique qu'il s'agit d'une bibliothèque et le suffixe indique qu'il s'agit de la version de développement incluant les fichiers d'en-tête nécessaires pour la compilation.

```bash
sudo apt-get install libcurl-dev
```

Sous Windows, l'installation de bibliothèques tierces peut être plus complexe, car il n'existe pas de gestionnaire de paquets standardisé. Il est souvent nécessaire de télécharger les fichiers d'installation depuis le site officiel de la bibliothèque et de suivre les instructions spécifiques à chaque bibliothèque.

### libc (Bibliothèque standard du C)

La bibliothèque standard du C, ou *libc*, est essentielle à tout programme écrit en C. Elle regroupe les fonctions de base du langage, telles que la gestion de la mémoire, les opérations sur les chaînes de caractères, ou encore les entrées/sorties. Généralement incluse dans l'environnement de développement, elle est fournie par le système d'exploitation ou le compilateur et représente un pilier fondamental de l'écosystème C.

### Glib (Bibliothèque de base de GNOME)

*Glib* est une bibliothèque polyvalente, développée dans le cadre du projet GNOME, mais largement utilisée au-delà. Elle propose une panoplie de fonctions pour la gestion de la mémoire, la manipulation des chaînes de caractères, des structures de données avancées telles que les listes, arbres, tables de hachage, ainsi que la gestion des signaux et des threads. Son architecture robuste en fait un choix privilégié pour de nombreux projets open source en quête de fiabilité.

## Sécurité

### OpenSSL

*OpenSSL* est une bibliothèque incontournable dans le domaine de la cryptographie et de la sécurité des communications. Adoptée par une multitude de projets, tant open source que commerciaux, elle propose des outils performants pour la gestion des certificats SSL, le chiffrement des données, ainsi que la vérification des signatures numériques. Sa large adoption témoigne de sa fiabilité et de sa capacité à sécuriser les échanges en ligne.

## Bases de données

### SQLite

*SQLite* se distingue par son moteur de base de données relationnelle compact et performant, largement utilisé dans les applications mobiles et web. Malgré sa légèreté, il offre des fonctionnalités avancées telles que la prise en charge des transactions ACID, des index, des vues, des déclencheurs, et des fonctions SQL sophistiquées. Sa simplicité d'intégration et son efficacité en font un choix privilégié pour le stockage des données dans des environnements variés.

## Réseau

### Libcurl

*Libcurl* est une bibliothèque spécialisée dans le transfert de données sur le réseau. Elle prend en charge une multitude de protocoles, dont HTTP, HTTPS, FTP, SFTP, et bien d'autres encore. Utilisée tant par des projets open source que par des entreprises, elle est indispensable pour toute application nécessitant des transferts de fichiers ou la communication avec des serveurs distants via des protocoles sécurisés ou non.

## Traitement d'images

### OpenCV

*OpenCV* est une bibliothèque de référence dans le domaine du traitement d'images et de vidéos. Utilisée pour des applications aussi diverses que la reconnaissance faciale, la détection d'objets ou la vision par ordinateur, elle supporte une vaste gamme de formats d'images tels que JPEG, PNG, TIFF, et BMP. Sa richesse fonctionnelle la rend incontournable pour les projets nécessitant une manipulation avancée des images.

### LibPNG

*LibPNG* est spécialisée dans la manipulation des images au format PNG. Elle permet de lire, écrire et modifier des images tout en gérant les spécificités de ce format, telles que la transparence ou la compression. Sa robustesse et sa compatibilité avec les normes en font un choix solide pour toute application manipulant des images PNG.

### LibJPEG

*LibJPEG* est la bibliothèque de référence pour le traitement des images JPEG. Elle prend en charge des opérations complexes telles que la compression, la décompression, et la manipulation d'images avec différents niveaux de qualité. Sa large adoption témoigne de son efficacité dans la gestion de ce format d'image très répandu.

## Traitement vidéo

### FFmpeg

*FFmpeg* est une bibliothèque puissante dédiée au traitement des fichiers vidéo et audio. Elle supporte un large éventail de formats tels que AVI, MP4, MOV, et MP3, et permet de réaliser des opérations complexes comme la conversion, le transcodage, ou encore la diffusion en direct. Sa polyvalence en fait un outil de choix pour les professionnels et les amateurs du multimédia.

## Gestion des événements

### Libevent

*Libevent* propose des fonctionnalités avancées pour la gestion des événements asynchrones, une composante essentielle des applications réseau performantes. Elle permet de gérer efficacement les connexions réseau, les entrées/sorties, et d'autres événements système critiques, garantissant ainsi une réactivité optimale.

### Libuv

*Libuv* est une autre bibliothèque spécialisée dans la gestion des événements asynchrones, souvent utilisée en conjonction avec Node.js. Elle se distingue par sa capacité à gérer les connexions réseau et les entrées/sorties de manière non bloquante, assurant des performances élevées dans les applications nécessitant une gestion efficace de nombreux événements simultanés.

## Gestion de la mémoire

### Jemalloc

*Jemalloc* est réputée pour ses performances en matière de gestion de la mémoire, notamment dans les applications où la gestion efficace des allocations est cruciale. Elle propose des fonctionnalités avancées comme la fragmentation réduite, les statistiques de mémoire détaillées, et les profils de mémoire, ce qui en fait un choix privilégié pour les systèmes à haute performance.

## Compression

### Zlib

*Zlib* est une bibliothèque de compression polyvalente, largement utilisée pour compresser et décompresser des fichiers, flux de données ou archives. Elle implémente les algorithmes DEFLATE, GZIP et ZLIB, offrant un excellent compromis entre vitesse et taux de compression.

### LibLZMA

*LibLZMA* se spécialise dans la compression au format LZMA, réputé pour son taux de compression élevé. Elle est utilisée dans des contextes où l'efficacité du stockage et la réduction de la taille des données sont primordiales, tout en maintenant des performances élevées en matière de décompression.

## Sérialisation

### LibYAML

*LibYAML* offre des outils robustes pour la sérialisation et la désérialisation de données au format YAML. Utilisée pour manipuler des configurations ou des données structurées, elle gère efficacement les différents éléments de ce format, tels que les séquences, les scalaires, et les paires clé-valeur.

### LibXML2

*LibXML2* est une bibliothèque puissante pour le traitement des documents XML, supportant les normes et standards associés comme XSLT, XPath, ou XML Schema. Elle est couramment utilisée pour l'analyse, la validation et la génération de documents XML dans des environnements où la précision et la conformité aux standards sont cruciales.

## Utilitaires

### PCRE (Perl Compatible Regular Expressions)

*PCRE* est la référence pour le traitement des expressions régulières compatibles avec Perl. Elle est utilisée pour effectuer des recherches complexes, des remplacements, ou pour valider des chaînes de texte selon des motifs avancés, offrant ainsi une flexibilité inégalée dans la manipulation de texte.

### GMP (GNU Multiple Precision Arithmetic Library)

*GMP* est spécialisée dans les calculs arithmétiques à précision arbitraire, indispensable dans des domaines exigeants comme la cryptographie ou les calculs scientifiques. Elle permet des opérations sur des entiers, rationnels et flottants avec une précision que les bibliothèques standards ne peuvent atteindre.

### ncurses

*ncurses* est la bibliothèque par excellence pour la création d'interfaces utilisateur en mode texte dans les environnements de terminal. Elle propose des outils pour gérer les fenêtres, les couleurs, les panneaux, ainsi que des fonctionnalités avancées comme la capture des touches de fonction et de contrôle.

## POSIX C Library

Le standard C ne définit que le minimum vital et qui est valable sur toutes les architectures pour autant que la *toolchain* soit compatible **C99**. Il existe néanmoins toute une collection d'autres fonctions manquantes :

- La communication entre les processus (deux programmes qui souhaitent communiquer entre eux)

  - `<sys/socket.h>`
  - `<sharedmemory.h>`

- La communication sur le réseau e.g. internet

  - `<sys/socket.h>`
  - `<arpa/inet.h>`
  - `<net/if.h>`

- Les tâches

  - `<thread.h>`

- Les traductions de chaînes p.ex. français vers anglais

  - `<iconv.h>`

- Les fonctions avancées de recherche de texte

  - `<regex.h>`

- Le log centralisé des messages (d'erreur)

  - `<syslog.h>`

Toutes ces bibliothèques additionnelles ne sont pas nécessairement disponibles sur votre ordinateur ou pour le système cible, surtout si vous convoitez une application *bare-metal*. Elles dépendent grandement du système d'exploitation utilisé, mais une tentative de normalisation existe et se nomme [POSIX](https://en.wikipedia.org/wiki/POSIX) (ISO/IEC 9945).

Généralement la vaste majorité des distributions Linux et Unix sont compatibles avec le standard POSIX et les bibliothèques ci-dessus seront disponibles à moins que vous ne visiez une architecture différente de celle sur laquelle s'exécute votre compilateur.

Le support POSIX sous Windows (Win32) n'est malheureusement que partiel et il n'est pas standardisé.

Un point d'entrée de l'API POSIX est la bibliothèque `<unistd.h>`.

## GNU GLIBC

La [[bibliothèque]] portable [GNULIB](https://www.gnu.org/software/gnulib/) est la bibliothèque standard référencée sous Linux par `libc6`.

## Windows C library

La bibliothèque [[Windows]] [Windoes API](https://docs.microsoft.com/en-us/windows/win32/apiindex/windows-api-list) offre une interface au système de fichier, au registre Windows, aux imprimantes, à l'interface de fenêtrage, à la console et au réseau.

L'accès à cet [[API]] est offert par un unique point d'entrée `windows.h` qui regroupe certains en-têtes standards (`<stdarg.h>`, `<string.h>`, ...), mais pas tous (😔) ainsi que les en-têtes spécifiques à Windows tels que :

`<winreg.h>`

: Pour l'accès au registre Windows

`<wincon.h>`

: L'accès à la console

La documentation est disponible en ligne depuis le site de Microsoft, mais n'est malheureusement pas complète et souvent il est difficile de savoir sur quel site trouver la bonne version de la bonne documentation. Par exemple, il n'y a aucune documentation claire de `LSTATUS` pour la fonction [RegCreateKeyExW](https://docs.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regcreatekeyexw) permettant de créer une entrée dans la base de registre.

Un bon point d'entrée est le [Microsoft API and reference catalog](https://msdn.microsoft.com/library).

Quelques observations :

- Officiellement Windows est compatible avec C89 (ANSI C) (c.f. [C Language Reference](https://docs.microsoft.com/en-us/cpp/c-language/c-language-reference?view=vs-2019))
- L'API Windows n'est pas officiellement compatible avec C99, mais elle s'en approche, il n'y pas ou peu de documents expliquant les différences.
- Microsoft n'a aucune priorité pour développer son support C, il se focalise davantage sur C++ et C#, c'est pourquoi certains éléments du langage ne sont pas ou peu documentés.
- Les [types standards Windows](https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types) différent de ceux proposés par C99. Par exemple, `LONG32` remplace `int32_t`.
