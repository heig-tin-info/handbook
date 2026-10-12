#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

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
