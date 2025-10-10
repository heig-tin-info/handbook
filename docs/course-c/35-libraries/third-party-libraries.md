# Autres bibliothèques

Les bibliothèques tierces regroupent des modules, des fonctions et des structures de données conçus pour être intégrés dans des projets existants. Elles ajoutent des fonctionnalités spécialisées — communication réseau, traitement d’images, chiffrement — sans qu’il soit nécessaire de tout réimplémenter. Provenant d’éditeurs, de communautés libres ou d’organismes de normalisation, elles constituent un levier majeur pour livrer plus rapidement un logiciel fiable.

## Installation de bibliothèques tierces

Sous Linux, les bibliothèques tierces sont généralement disponibles via le gestionnaire de paquets de la distribution. On recherche d’abord le nom du module, puis on installe le paquet qui fournit **à la fois** la bibliothèque compilée et les fichiers d’en-tête. Pour `curl`, par exemple, on cible le paquet `libcurl4-openssl-dev` ou équivalent : le préfixe `lib` signale qu’il s’agit d’une bibliothèque, tandis que le suffixe `-dev` confirme que les fichiers nécessaires à la compilation sont inclus.

```bash
sudo apt install libcurl4-openssl-dev
```

Sous Windows, l’installation demande davantage de vigilance : il n’existe pas de gestionnaire de paquets universel et chaque bibliothèque propose sa propre procédure. Plusieurs projets — comme [vcpkg](https://github.com/microsoft/vcpkg) ou [MSYS2](https://www.msys2.org/) — facilitent toutefois l’obtention d’archives à jour, accompagnées des fichiers `.lib` et `.dll` indispensables.

### libc (bibliothèque standard du C)

La bibliothèque standard du C, ou *libc*, constitue le socle minimal sur lequel reposent tous les programmes écrits en C. Elle regroupe les fonctions de base du langage : gestion de la mémoire, manipulation des chaînes, entrée/sortie standard, conversions numériques… Sur la plupart des systèmes, elle est livrée avec le compilateur ou le système d’exploitation, mais il reste utile de connaître la version installée et ses éventuelles extensions.

### Glib (bibliothèque de base de GNOME)

*Glib* est une bibliothèque polyvalente, développée dans le cadre du projet GNOME mais largement utilisée ailleurs. Elle propose une panoplie de fonctions pour la gestion de la mémoire, la manipulation des chaînes de caractères et des structures de données avancées (listes, arbres, tables de hachage), ainsi que la gestion des signaux et des threads. Son architecture robuste et son API cohérente en font un choix privilégié pour de nombreux projets libres.

## Sécurité

### OpenSSL

*OpenSSL* est une bibliothèque incontournable dans le domaine de la cryptographie et de la sécurité des communications. Adoptée par une multitude de projets open source et commerciaux, elle fournit les primitives cryptographiques, la gestion des certificats X.509 et les outils nécessaires pour établir des connexions TLS sécurisées. Sa large adoption témoigne de sa robustesse, mais impose de suivre de près les correctifs de sécurité publiés par le projet.

## Bases de données

### SQLite

*SQLite* se distingue par son moteur de base de données relationnelle compact et performant, largement utilisé dans les applications mobiles et embarquées. Malgré sa légèreté, il offre des fonctionnalités avancées telles que le support des transactions ACID, des index, des vues, des déclencheurs et de nombreuses fonctions SQL. Sa distribution sous la forme d’un simple fichier source facilite son intégration dans des projets C ou C++.

## Réseau

### libcurl

*libcurl* est une bibliothèque spécialisée dans le transfert de données sur le réseau. Elle prend en charge une multitude de protocoles (HTTP, HTTPS, FTP, SFTP, MQTT, etc.) et gère de nombreuses options pratiques : authentification, reprise de téléchargement, connexions simultanées. Utilisée aussi bien par des projets libres que par des entreprises, elle constitue une base solide pour toute application qui dialogue avec des services distants.

## Traitement d'images

### OpenCV

*OpenCV* est une bibliothèque de référence pour le traitement d’images et de vidéos. Utilisée dans des applications aussi diverses que la reconnaissance faciale, la détection d’objets ou la vision industrielle, elle prend en charge de nombreux formats (JPEG, PNG, TIFF, BMP) et propose des modules spécialisés pour l’apprentissage automatique ou la calibration de caméras.

### libpng

*libpng* est spécialisée dans la manipulation des images au format PNG. Elle permet de lire, écrire et transformer des images tout en respectant les spécificités du format : transparence, correction gamma, métadonnées. Sa robustesse et sa compatibilité avec les normes en font un choix sûr pour toutes les applications manipulant des fichiers PNG.

### libjpeg

*libjpeg* est la bibliothèque de référence pour le traitement des images JPEG. Elle prend en charge la compression, la décompression et la transformation sans perte de blocs JPEG, avec différents niveaux de qualité. De nombreux visionneurs, navigateurs et outils de conversion s’appuient sur cette implémentation mature.

## Traitement vidéo

### FFmpeg

*FFmpeg* est une suite logicielle puissante dédiée au traitement des flux audio et vidéo. Elle comprend des bibliothèques (libavcodec, libavformat, libswscale…) et des outils en ligne de commande qui prennent en charge une quantité impressionnante de formats (AVI, MP4, WebM, MP3, FLAC). Conversion, transcodage, diffusion en direct ou extraction de pistes audio deviennent accessibles avec quelques appels.

## Gestion des événements

### libevent

*libevent* propose des fonctionnalités avancées pour la gestion des événements asynchrones, élément essentiel des applications réseau performantes. Elle encapsule les multiplexeurs du système (epoll, kqueue, select…) et fournit une API unifiée pour surveiller les sockets, les signaux ou les opérations temporisées, tout en restant légère.

### libuv

*libuv* est une bibliothèque multiplateforme spécialisée dans la gestion des événements asynchrones, popularisée par Node.js. Elle combine un modèle d’exécution basé sur une boucle d’événements avec un pool de threads pour traiter les opérations bloquantes, ce qui garantit des performances élevées sur Windows, Linux et macOS.

## Gestion de la mémoire

### jemalloc

*jemalloc* est réputée pour ses performances en matière de gestion de la mémoire, notamment dans les applications qui allouent massivement de petits blocs. Elle réduit la fragmentation, fournit des statistiques détaillées et propose des profils de mémoire utiles pour le diagnostic. De nombreux systèmes de bases de données et services web l’utilisent en remplacement de l’allocateur par défaut.

## Compression

### zlib

*zlib* est une bibliothèque de compression polyvalente, largement utilisée pour compresser et décompresser des fichiers, flux de données ou archives. Elle implémente les formats DEFLATE, gzip et zlib, offrant un excellent compromis entre vitesse et taux de compression. On la retrouve dans des outils aussi divers que `zip`, `pngcrush` ou `ssh`.

### liblzma

*liblzma* se spécialise dans la compression au format LZMA, réputé pour son taux de compression élevé. Elle est utilisée dans des contextes où l’efficacité du stockage et la réduction de la taille des données sont primordiales, tout en maintenant des performances honorables en décompression. Elle constitue le cœur du format `.xz`.

## Sérialisation

### libyaml

*libyaml* offre des outils robustes pour la sérialisation et la désérialisation de données au format YAML. Utilisée pour manipuler des configurations ou des données structurées, elle gère efficacement les séquences, les scalaires et les paires clé-valeur, tout en validant la conformité aux spécifications officielles.

### libxml2

*libxml2* est une bibliothèque puissante pour le traitement des documents XML. Elle prend en charge les normes associées (XPath, XPointer, XInclude, XML Schema) et propose un validateur, un moteur XSLT ainsi qu’une API DOM/SAX performante. Elle est couramment utilisée pour analyser, valider et générer des documents XML dans des environnements où la conformité aux standards est cruciale.

## Utilitaires

### PCRE (Perl Compatible Regular Expressions)

*PCRE* est la référence pour le traitement des expressions régulières compatibles avec Perl. Elle permet des recherches complexes, des remplacements conditionnels ou la validation de chaînes de texte selon des motifs avancés. Plusieurs langages de script l’utilisent directement comme moteur interne.

### GMP (GNU Multiple Precision Arithmetic Library)

*GMP* est spécialisée dans les calculs arithmétiques à précision arbitraire, indispensables dans des domaines exigeants comme la cryptographie ou les calculs scientifiques. Elle offre des opérations optimisées sur les entiers, rationnels et flottants et s’appuie sur des algorithmes avancés pour exploiter au mieux l’architecture matérielle.

### ncurses

*ncurses* est la bibliothèque de référence pour créer des interfaces utilisateur en mode texte dans un terminal. Elle fournit des primitives pour gérer les fenêtres, les couleurs, les panneaux et la capture des touches de fonction, ce qui permet d’élaborer des interfaces riches malgré un affichage en caractères.

## Bibliothèque C POSIX

Le standard C ne définit que le minimum vital pour garantir la portabilité. Les systèmes compatibles POSIX apportent de nombreuses extensions utiles :

- Communication entre processus (deux programmes qui souhaitent dialoguer)

  - `<sys/socket.h>`
  - `<sys/shm.h>`

- Communication réseau (par exemple sur Internet)

  - `<sys/socket.h>`
  - `<arpa/inet.h>`
  - `<net/if.h>`

- Gestion des tâches

  - `<pthread.h>`

- Traduction de chaînes (par exemple du français vers l’anglais)

  - `<iconv.h>`

- Fonctions avancées de recherche de texte

  - `<regex.h>`

- Journalisation centralisée des messages (notamment d’erreur)

  - `<syslog.h>`

Toutes ces extensions ne sont pas nécessairement disponibles sur votre machine ni sur la cible visée, en particulier pour des applications *bare metal*. Elles dépendent fortement du système d’exploitation, mais POSIX (ISO/IEC 9945) constitue l’effort de normalisation le plus abouti.

La vaste majorité des distributions GNU/Linux et Unix respectent ce standard, sauf lorsqu’on vise une architecture exotique. Sous Windows, le support POSIX reste partiel ; certaines fonctionnalités sont accessibles via des bibliothèques de compatibilité ou des sous-systèmes comme WSL.

L’en-tête `<unistd.h>` représente un bon point d’entrée dans l’API POSIX.

## GNU glibc

La bibliothèque GNU C (*glibc*) est l’implémentation de référence fournie par la plupart des distributions GNU/Linux. Le projet [Gnulib](https://www.gnu.org/software/gnulib/) propose, quant à lui, une collection de modules portables qui complètent la glibc ou servent d’alternative lorsqu’une fonctionnalité fait défaut.

## Bibliothèque C pour Windows

L’[API Windows](https://docs.microsoft.com/en-us/windows/win32/apiindex/windows-api-list) expose les services du système : système de fichiers, registre, impression, interface graphique, console, réseau… L’inclusion de `<windows.h>` donne accès à un large éventail d’en-têtes — certains issus du standard C (`<stdarg.h>`, `<string.h>`), d’autres propres à la plateforme.

`<winreg.h>`

: Accès au registre Windows

`<wincon.h>`

: Accès à la console

La documentation officielle est disponible sur le site de Microsoft, mais elle peut paraître morcelée. Le [Microsoft API and Reference Catalog](https://msdn.microsoft.com/library) est un bon point de départ pour retrouver les pages pertinentes. Gardez cependant à l’esprit les particularités suivantes :

- Officiellement, Windows garantit la compatibilité avec C89 (ANSI C).
- Le support de C99 est partiel et peu documenté ; certains mots-clés ou en-têtes restent absents.
- L’équipe Microsoft privilégie C++ et C#, d’où des zones grises dans la documentation C.
- Les [types standards Windows](https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types) diffèrent de ceux de C99 (par exemple, `LONG32` à la place de `int32_t`).
