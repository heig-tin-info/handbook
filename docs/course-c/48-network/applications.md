# Applications réseau

Ce chapitre donne quelques exemples très simples d'applications réseau en C.

## Serveur Web

Le plus simple en C est d'utiliser la bibliothèque [Mongoose](https://github.com/cesanta/mongoose) qui est très légère et utilisable dans des applications embarquées. Elle fonctionne sous Windows, Linux, macOS, Windows, Android et sur différents microcontrôleurs (STM32, NXP, ESP32, NRF52, ...).

Le plus magique c'est que cette bibliothèque est monolithique, c'est-à-dire qu'elle ne dépend d'aucune autre bibliothèque. Il suffit de rajouter les fichiers `mongoose.c` et `mongoose.h` dans votre projet et de les compiler avec votre programme.

L'utilisation est très simple. Le programme d'exemple ci-dessous crée un serveur web qui écoute sur le port 8090. Il répond à quatre requêtes différentes :

- `/` : Retourne `Hello, world!`, c'est la page d'accueil.
- `/source` : Retourne le contenu du dossier `www` situé dans le répertoire courant.
- `/api/time/get` : Retourne l'heure actuelle en JSON, il simule une API.
- `/teapot` : Retourne `I'm a teapot`, c'est une blague.
- Tout autre URI retourne une erreur 500.

```c
#include "mongoose.h"

void ev_handler(struct mg_connection *c, int ev, void *ev_data) {
   if (ev == MG_EV_HTTP_MSG) {
      struct mg_http_message *hm = (struct mg_http_message *)ev_data;
      if (mg_match(hm->uri, mg_str("/"), NULL)) {
         mg_http_reply(c, 200, "Content-Type: text/plain\r\n",
            "Hello, world!\n");
      } else if (mg_match(hm->uri, mg_str("/source"), NULL)) {
         struct mg_http_serve_opts opts = {.root_dir = "./www"};
         mg_http_serve_dir(c, hm, &opts);
      } else if (mg_match(hm->uri, mg_str("/api/time/get"), NULL)) {
         mg_http_reply(c, 200, "Content-Type: application/json\r\n",
            "{%m:%lu}\n", MG_ESC("time"), time(NULL));
      } else if (mg_match(hm->uri, mg_str("/teapot"), NULL)) {
         mg_http_reply(c, 418, "", "I'm a teapot\n");
      } else {
         mg_http_reply(c, 500, "Content-Type: application/json\r\n",
            "{%m:%m}\n", MG_ESC("error"), MG_ESC("Unsupported URI"));
      }
   }
}

int main(void) {
   struct mg_mgr mgr;
   mg_mgr_init(&mgr);
   mg_http_listen(&mgr, "http://0.0.0.0:8090", ev_handler, NULL);
   for (;;) mg_mgr_poll(&mgr, 1000);
}
```

## Requête HTTP

Il est parfois utile pour un programme de récupérer des informations sur un serveur web. Le développeur recherchera une solution impliquant une API simple retournant un contenu JSON. Le JSON est un format de sérialisation de données très populaire, et il est facile à lire et à écrire pour les humains.

Imaginons que vous souhaitez réaliser un programme qui affiche un fait incroyable sur les chats. Heureusement, vous avez à votre disposition l'API [Cat Facts](https://catfact.ninja/). Une requête HTTP GET sera envoyée à l'URL `https://catfact.ninja/fact` pour obtenir un fait aléatoire en JSON.

Voici un exemple de requête :

```http
GET /fact HTTP/1.1
Host: catfact.ninja
```

Et voici un exemple de réponse :

```json
{
    "fact": "The cat who holds the record for the longest non-fatal fall is
    Andy. He fell from the 16th floor of an apartment building
    (about 200 ft/.06 km) and survived.",
    "length": 157
}
```

Il y a plusieurs manières de réaliser ce programme en C tout d'abord sans aucune dépendance. Le protocole HTTP sera émulé en utilisant des sockets et la réponse JSON sera découpée à la main. Notez que ce code n'est pas du tout un bon exemple. Tout d'abord aucune erreur n'est vérifiée, et le code est très fragile. Si la réponse du serveur change, le programme ne fonctionnera plus. Néanmoins l'exercice ici est de comprendre que HTTP n'est qu'un simple protocole texte.

```c
#define BUFFER_SIZE 4096

int main() {
   char *request =
       "GET /fact HTTP/1.1\r\n"
       "Host: catfact.ninja\r\n"
       "Connection: close\r\n"
       "\r\n";

   struct addrinfo hints = {0}, *res;
   hints.ai_family = AF_UNSPEC;  // Allow IPv4 or IPv6
   hints.ai_socktype = SOCK_STREAM;
   getaddrinfo("catfact.ninja", "80", &hints, &res);

   int sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
   connect(sockfd, res->ai_addr, res->ai_addrlen);
   freeaddrinfo(res);
   send(sockfd, request, strlen(request), 0);

   char buffer[BUFFER_SIZE];
   int bytes_received = recv(sockfd, buffer, BUFFER_SIZE - 1, 0);
   if (bytes_received < 0) perror("Erreur lors de la réception de la réponse");
   close(sockfd);

   printf("Réponse reçue : %.*s\n", bytes_received, buffer);

   char *json_start = strstr(buffer, "\r\n\r\n");
   if (json_start) {
      json_start += 4;
      char *fact_start = strstr(json_start, "\"fact\":\"");
      if (fact_start) {
         fact_start += 8;
         char *fact_end = strchr(fact_start, '"');
         if (fact_end) {
            *fact_end = '\0';
            printf("%s\n", fact_start);
         }
      }
   } else {
      printf("Réponse HTTP invalide ou absence de JSON.\n");
   }
}
```

Hélas, si ce code fonctionnait bien il y a quelques années, la réponse que l'on obtient est la suivante :

```
Réponse reçue : HTTP/1.1 301 Moved Permanently
Server: nginx/1.24.0
Date: Mon, 16 Sep 2024 12:58:04 GMT
Content-Type: text/html
Content-Length: 169
Connection: close
Location: https://catfact.ninja/fact

<html>
<head><title>301 Moved Permanently</title></head>
<body>
<center><h1>301 Moved Permanently</h1></center>
<hr><center>nginx/1.24.0</center>
</body>
</html>
```

Le code de réponse est `301` parce que le site a été déplacé vers un nouvel emplacement et cet emplacement est `https://catfact.ninja/fact`. Notez la présence du `s` à http. Cela signifie que le serveur utilise le protocole HTTPS et non HTTP. Sans bibliothèque supplémentaire, il est impossible de réaliser une requête HTTPS car cela nécessite une couche de chiffrement et des certificats.

Voyons voir comment faire la même chose convenablement, en utilisant les bonnes dépendances. Nous aurons besoin de quelques bibliothèques :

```bash
sudo apt install libcurl4-openssl-dev libjson-c-dev
```

Voici le code C. La bibliothèque `libcurl` est utilisée pour effectuer la requête HTTP(S) et la bibliothèque `libjson-c` est utilisée pour analyser la réponse JSON :

```c
#include <curl/curl.h>
#include <json-c/json.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct response { char *memory; size_t size; };

static size_t write_callback(void *data, size_t size, size_t nmemb, void *userp) {
   size_t realsize = size * nmemb;
   struct response *mem = (struct response *)userp;
   char *ptr = realloc(mem->memory, mem->size + realsize + 1);
   if (ptr == NULL) {
      printf("Not enough memory (realloc failed)\n");
      return 0;
   }
   mem->memory = ptr;
   memcpy(&(mem->memory[mem->size]), data, realsize);
   mem->size += realsize;
   mem->memory[mem->size] = '\0';
   return realsize;
}

int main() {
   struct response chunk = {.memory = malloc(1), .size = 0};

   curl_global_init(CURL_GLOBAL_DEFAULT);
   CURL *curl = curl_easy_init();
   if (!curl) {
      fprintf(stderr, "Erreur cURL: impossible d'initialiser\n");
      return 1;
   }

   curl_easy_setopt(curl, CURLOPT_URL, "https://catfact.ninja/fact");
   curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
   curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);
   CURLcode res = curl_easy_perform(curl);

   if (res != CURLE_OK) {
      fprintf(stderr, "Erreur cURL: %s\n", curl_easy_strerror(res));
      return 1;
   }

   struct json_object *parsed_json = json_tokener_parse(chunk.memory);
   struct json_object *fact;
   json_object_object_get_ex(parsed_json, "fact", &fact);
   printf("%s\n", json_object_get_string(fact));
   json_object_put(parsed_json);

   curl_easy_cleanup(curl);
   free(chunk.memory);
   curl_global_cleanup();
}
```

N'oubliez pas lors de la compilation de rajouter les bibliothèques:

```bash
gcc catfact.c -lcurl -ljson-c
```