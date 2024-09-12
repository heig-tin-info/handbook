# Sockets

Un socket (prise en français) est un point de communication entre deux processus sur un réseau. Il permet l'échange de données entre les processus en utilisant des protocoles de communication tels que TCP ou UDP.

Hélas, les sockets ne sont pas disponibles dans la bibliothèque standard de C, ils ne sont donc pas standardisés et donc chaque système d'exploitation a sa propre implémentation. Cependant, la plupart des systèmes d'exploitation modernes supportent les sockets BSD (Berkeley Software Distribution) qui sont largement utilisés.

## Création d'un socket

Nous allons créer deux programmes, un serveur et un client, pour illustrer l'utilisation des sockets en C. Le serveur va écouter les connexions entrantes et le client va se connecter au serveur pour envoyer et recevoir des données. Pour les besoins de l'exemple, le serveur va simplement répondre à `ping` par `pong`.

Voici le serveur :

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 8080

int main() {
    int server_fd;
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in address = {
        .sin_family = AF_INET,
        .sin_addr.s_addr = INADDR_ANY,
        .sin_port = htons(PORT)};
    const int addrlen = sizeof(address);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    int new_socket;
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("accept");
        exit(EXIT_FAILURE);
    }

    char buffer[1024] = {0};
    char *response = "pong";
    read(new_socket, buffer, 1024);
    printf("Received: %s\n", buffer);
    send(new_socket, response, strlen(response), 0);
    printf("Response sent\n");
}
```

et voici le client :

```c
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define PORT 8080
int main() {
   int sock = 0;
   if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
      printf("Socket creation error\n");
      return -1;
   }

   struct sockaddr_in serv_addr;
   serv_addr.sin_family = AF_INET;
   serv_addr.sin_port = htons(PORT);

   if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
      printf("Invalid address / Address not supported\n");
      return -1;
   }

   if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
      printf("Connection failed\n");
      return -1;
   }

   const char *ping_msg = "ping";
   while (1) {
      char buffer[1024] = {0};
      send(sock, ping_msg, strlen(ping_msg), 0);
      printf("Ping sent\n");
      int valread = read(sock, buffer, sizeof(buffer));
      if (valread > 0) printf("Server: %s\n", buffer);
      sleep(1);
   }
   close(sock);
}
```

## Modèle de Berkeley

Le modèle de Berkeley est un modèle de programmation pour les sockets qui a été introduit dans les années 1980 par l'Université de Berkeley. Il est largement utilisé dans les systèmes Unix et Linux. Le principe est de traiter les sockets comme des fichiers, en utilisant les appels système `open`, `read`, `write` et `close`.

## Types de sockets

Il existe trois catégories de sockets :

- **AF_INET** : Utilisé pour les connexions IPv4.
- **AF_INET6** : Utilisé pour les connexions IPv6.
- **AF_UNIX** : Utilisé pour les connexions Unix.

Il existe trois types de sockets principaux :

- **SOCK_STREAM** : Utilisé pour les connexions TCP, garantit la livraison des données dans l'ordre et sans perte.
- **SOCK_DGRAM** : Utilisé pour les connexions UDP, ne garantit pas la livraison des données ni l'ordre.
- **SOCK_RAW** : Utilisé pour les sockets bruts, permet d'accéder directement aux trames réseau.


Les sockets Unix (`AF_UNIX`) sont utilisés pour les communications inter-processus sur un même système. Ils sont similaires aux sockets TCP/IP mais utilisent des fichiers pour la communication. C'est par exemple le cas des sockets utilisés par le serveur X pour communiquer avec les clients graphiques.

Sous Windows les sockets sont implémentés différemment, il est recommandé d'utiliser la bibliothèque Winsock pour les applications Windows.