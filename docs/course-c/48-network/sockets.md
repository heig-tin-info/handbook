# Sockets

Un socket (prise en français) est un point de communication entre deux processus sur un réseau. Il permet l'échange de données entre les processus en utilisant majoritairement les protocoles de communication TCP ou UDP.

Hélas, les sockets ne sont pas disponibles dans la bibliothèque standard de C, ils ne sont donc pas standardisés et donc chaque système d'exploitation a sa propre implémentation. Cependant, la plupart des systèmes d'exploitation modernes supportent (avec de légères variations) les sockets BSD (Berkeley Software Distribution).

Un serveur web est un programme qui utilise les sockets TCP pour écouter les connexions entrantes et répondre aux requêtes des clients. Un client web est un programme qui utilise les sockets TCP pour se connecter à un serveur web et envoyer des requêtes. Une base de données MySQL est un programme qui expose un socket TCP pour permettre aux clients de se connecter et d'envoyer des requêtes SQL. De mêmes, Docker expose un socket Unix pour permettre aux clients de se connecter et de contrôler les conteneurs. Les sockets sont partout.

## Fonctionnement des sockets

Les sockets sont une couche d'abstraction de la communication entre deux processus (programmes), que ce soit sur le même appareil ou sur des machines distantes. Le principe de base d'un socket est d'agir comme un canal de communication pour échanger des données binaires. On qualifie souvent un programme de **serveur** s'il écoute les connexions entrantes et de **client** s'il initie une connexion. Une fois la connexion établie, les deux processus peuvent envoyer et recevoir des données de manière bidirectionnelle.

Les sockets sont identifiés par une adresse IP et un numéro de port. L'adresse IP identifie l'appareil sur le réseau et le numéro de port identifie le processus sur l'appareil. L'organisme IANA (*Internet Assigned Numbers Authority*) est responsable du maintien des affectations des numéros de port pour les communications TCP et UDP. On notera que les ports de 0 à 1023 sont réservés pour les services système, les ports de 1024 à 49151 sont réservés pour les applications utilisateur et les ports de 49152 à 65535 sont réservés pour les connexions dynamiques (NAT / PAT / UPnP...).

Le port de loin le plus utilisé est le port 80 pour les connexions HTTP, suivi du port 443 pour les connexions HTTPS. Les ports 20 et 21 étaient utilisés jadis pour les connexions FTP. Les services de messagerie (e-mail) utilisent les ports 25, 465 et 587 etc.

Pour établir un socket, un programme commence par créer un socket avec la fonction `socket()`. C'est là qu'est défini la famille d'adresse (IPv4 ou IPv6), le type de socket (TCP/UDP) et le protocole. Le socket est ensuite lié à une adresse et à un port spécifique. Une fois relié, la fonction `listen()` permet d'écouter sur le socket. Un serveur écoute un socket lorsqu'il attend des connexions entrantes. Une fois une tentative de connexion détectée, la fonction `accept()` est utilisée pour établie la connexion et permettre l'échange de données. Enfin, les fonctions `read()`, `write()` sont utilisées pour échanger des données. Lorsque la communication est terminée, le socket est fermé avec `close()`.

## Types de sockets

Il existe principalement trois catégories de sockets encore utilisées : **AF_INET** utilisé pour les connexions IPv4, **AF_INET6** utilisé pour les connexions IPv6 et **AF_UNIX**  Utilisé pour les connexions Unix. Le préfixe `AF` signifie *Address Family*. Si l'on jète un oeil à `<socket.h>` on peut constater d'autres familles peu intéressantes comme `AF_AX25` utilisé par les radio amateurs, `AF_APPLETALK` utilisé par les réseaux Macintosh entre 1985 et 1995 ou encore `AF_AAL5` utilisé par les réseaux ATM de 1990 à 2000. On constate l'héritage de l'histoire des réseaux dans les sockets.

Une fois la famille choisie, il faut choisir le type de socket. Il existe trois types de sockets principaux : **SOCK_STREAM** pour une connexion TCP, c'est un socket de type flux orienté connexion. Il garantit la livraison des données dans l'ordre et sans perte. **SOCK_DGRAM** pour une connexion UDP. Il ne garantit pas la livraison des données ni l'ordre. Il n'y a pas besoin de connexion préalable. Le type **SOCK_RAW** permet d'accéder directement aux trames réseau au niveau IP, au-dessus de la couche liaison. Utilisé pour implémenter des protocoles réseau au niveau utilisateur ou pour des outils de diagnostic réseau (comme ping, traceroute). Il est généralement utilisé par des programmes ayant des privilèges élevés (root, `sudo`). Les autres types de sockets sont moins utilisés et ne méritent pas d'être mentionnés ici.

## Portabilité

Comme il a été évoqué, les sockets sont une API de bas niveau et ne sont pas standardisés. Chaque système d'exploitation a sa propre implémentation des sockets. Heureusement, pour simplifier la portabilité entre systèmes, il existe des bibliothèques externes qui offrent une abstraction (oui, encore une...) des sockets. La bibliothèque la plus populaire est [libuv](https://github.com/libuv/libuv) qui a été développée initialement pour [Node.js](https://nodejs.org/). Elle est aujourd'hui utilisée par de nombreux projets open-source et est disponible pour la plupart des systèmes d'exploitation.

Lorsque vous développez un programme utilisant des sockets, il n'est pas recommandé d'utiliser directement les appels système, ou les fonctions spécifiques à votre système d'exploitation. Préférez utiliser une bibliothèque externe qui vous simplifiera la vie.

Notons que si vous développez une application graphique avec SDL, GTK, Qt, etc. vous n'aurez pas besoin de gérer les sockets directement. Ces bibliothèques offrent des fonctions pour gérer les connexions réseau de manière plus simple et également portable.

## Création d'un socket

L'exercice du jour est la création de deux programmes : un serveur et un client, pour illustrer l'utilisation des sockets en C. Bien entendu cet exemple sera réalisé sur Linux, sans bibliothèque externe.

Le serveur va écouter les connexions entrantes et le client va se connecter au serveur pour envoyer et recevoir des données. Pour les besoins de l'exemple, le serveur va simplement répondre à `ping` par `pong`.

Voici le serveur :

```c
--8<-- "docs/assets/src/network/ping-pong/server.c"
```

et voici le client :

```c
--8<-- "docs/assets/src/network/ping-pong/client.c"
```

Un descripteur de fichier `server_fd` est créé pour le serveur. Il s'agit d'un vrai *file descriptor* selon le principe de Unix :*everything is a file*. Le socket est créé sur la famille IPv4 en mode TCP (*SOCK_STREAM*). Si le socket ne peut pas être créé, la valeur `-1` est retournée et le programme se termine.

Ensuite une structure `sockaddr_in` est créée pour définir l'adresse et le port du serveur. L'adresse est définie à `INADDR_ANY` pour écouter sur toutes les interfaces réseau. Le port est défini à `8080`. La fonction `bind()` est utilisée pour lier le socket à l'adresse et au port. Si la fonction échoue, le programme se termine. Pour le type et la famille de socket choisie, nous utilisons ici la structure `sockaddr_in` qui est spécifique à IPv4. Elle contiendra l'adresse IP et le port du serveur. le port `8080` utilisé ici sera converti en *big-endian* avec la fonction `htons()` puisque le réseau utilise le *big-endian*, et l'adresse IP est définie à `INADDR_ANY` pour écouter sur toutes les interfaces réseau.

L'étape suivante est de lier le socket à l'adresse avec la fonction `bind()`. Si la fonction échoue, le programme se termine. Si une erreur doit se produire, c'est très souvent le `bind` qui échoue. En effet, il ne peut y avoir qu'un seul programme écoutant sur un port donné. Si un autre programme écoute déjà sur le port 8080, le `bind` échouera avec l'erreur : *Address already in use*. C'est une erreur agaçante parce qu'il faut chercher quel programme écoute sur ce port. La commande `ss -tulnp` permet de lister les programmes écoutant sur les ports TCP.

La fonction `listen()` est ensuite utilisée pour démarrer l'écoute. Cette fonction prend en paramètre le descripteur de fichier du socket et la taille souhaitée de la file d'attente des connexions entrantes. La taille de la file d'attente est fixée à `3` ici, donc trois clients pourraient être en attente de connexion. Si un quatrième client tente de se connecter, il recevra un message d'erreur.

Lorsqu'une demande de connexion est détectée, la fonction `accept()` est utilisée pour accepter la connexion. Cette fonction retourne un nouveau descripteur de fichier `new_socket` qui est utilisé pour envoyer et recevoir des données. La fonction `accept()` est bloquante, c'est-à-dire qu'elle attend qu'une connexion soit établie. Si aucune connexion n'est en attente, le programme est mis en pause jusqu'à ce qu'une connexion soit établie.

La fonction `read` est similaire à celle utilisée pour lire un fichier. Elle prend en paramètre le descripteur de fichier, un tampon pour stocker les données lues et la taille du tampon. Comme pour les fichiers et l'entrée standard, la fonction est bloquante. Elle attend que des données soient disponibles pour les lire. Si la connexion est fermée par le client, la fonction `read` retourne `0`.

Pourquoi avoir besoin d'un deuxième descripteur de fichier `new_socket` ? Parce que le socket `server_fd` est utilisé pour écouter les connexions entrantes, mais une fois une connexion établie, il faut un nouveau socket pour échanger des données avec le client. C'est le socket `new_socket` qui est utilisé pour envoyer et recevoir des données. Comme analogie `server_fd` est le bureau de réception où les clients arrivent pour se connecter. Il reste ouvert pour accepter de nouveaux clients et `new_socket` est comme la cabine téléphonique où le client et le serveur peuvent échanger des données.

## Exemple portable

Pour un exemple portable, nous allons utiliser la bibliothèque libuv. Cette bibliothèque est basée sur un modèle de programmation asynchrone et événementielle. C'est-à-dire que le programme ne bloque pas lorsqu'il attend une connexion ou des données, mais qu'il fonctionne avec des *callback*. C'est un modèle de programmation très populaire pour les applications réseau et les serveurs web.

Nécessairement l'exemple donné est un peu plus complexe que l'exemple précédent. Il est cependant plus robuste et portable. Voici le serveur :

```c
--8<-- "docs/assets/src/network/ping-pong/server-uv.c"
```

Et voici le client

```c
--8<-- "docs/assets/src/network/ping-pong/client-uv.c"
```

## Erreurs courantes

Les erreurs les plus courantes lors de la création d'un socket sont :

*Address already in use*

: Un autre programme écoute déjà sur le port spécifié. Utilisez la commande `ss -tulnp` pour lister les programmes écoutant sur les ports TCP ou sous Windows `netstat -aon`. Essayez de changer de port.

*Permission denied*

: Vous n'avez pas les droits pour écouter ou sur le port spécifié. Essayez de lancer le programme avec les droits `root` ou `sudo`. Sous Windows, exécutez le programme en tant qu'administrateur et sous Linux, utilisez `sudo`. Il faut savoir que les ports de 0 à 1023 sont réservés pour les services système et nécessitent des privilèges élevés pour être utilisés. Si votre objectif est d'écrire un programme de test, utilisez un port supérieur à 1024. Dans le cas d'un socket Unix, vérifiez que le fichier de socket n'existe pas déjà ou si vous vous connectez dessus, vérifiez que vous avez les droits nécessaires.

*Connection refused*

: Le serveur n'accepte pas la connexion. Cela peut être dû à un pare-feu, à une erreur dans le code du serveur ou à une erreur dans l'adresse IP ou le port du client. Il faut investiguer pour trouver la cause.

Le problème de l'adresse déjà utilisée peut apparaître même si le programme a été arrêté. Cela est dû au fait que le système d'exploitation conserve les sockets en état `TIME_WAIT` pendant un certain temps (entre 30 secondes et 2 minutes) après la fermeture du programme. Cela permet de s'assurer que tous les paquets ont été reçus et envoyés. Si vous avez besoin de réutiliser un port immédiatement après la fermeture du programme, vous pouvez utiliser l'option `SO_REUSEADDR` avec la fonction `setsockopt()` :

```c
int opt = 1;
if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
    perror("setsockopt failed");
    exit(EXIT_FAILURE);
}
```

Une autre solution est de forcer la fermeture du socket immédiatement après la fermeture du programme avec l'option `SO_LINGER` :

```c
struct linger so_linger;
so_linger.l_onoff = 1;   // Activer SO_LINGER
so_linger.l_linger = 0;  // Fermer immédiatement sans délai

if (setsockopt(server_fd, SOL_SOCKET, SO_LINGER, &so_linger, sizeof(so_linger)) < 0) {
    perror("setsockopt failed");
    exit(EXIT_FAILURE);
}
```

Le délai d'attente sous Linux est déterminé par le paramètre `net.ipv4.tcp_fin_timeout` du noyau. Vous pouvez le modifier avec la commande `sysctl -w net.ipv4.tcp_fin_timeout=30` pour le mettre à 30 secondes par exemple. Vous pouvez également le lire avec la commande `sysctl net.ipv4.tcp_fin_timeout`. Sous Ubuntu 24.04, le délai est de 60 secondes par défaut.

La dernière solution est de lister les connexions en état `TIME_WAIT` avec la commande suivante et tuer les connexions qui posent problème :

```bash
ss -o state time-wait '( sport = :8080 )'
```
