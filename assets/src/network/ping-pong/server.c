#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define PORT 8080

int main() {
   int server_fd;
   if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
      perror("socket failed");
      exit(EXIT_FAILURE);
   }

   struct sockaddr_in address = {.sin_family = AF_INET,
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

   while (1) {
      int new_socket;
      if ((new_socket = accept(server_fd, (struct sockaddr *)&address,
                               (socklen_t *)&addrlen)) < 0) {
         perror("accept");
         exit(EXIT_FAILURE);
      }

      char buffer[1024] = {0};
      char *response = "pong";
      read(new_socket, buffer, 1024);
      printf("Received: %s\n", buffer);
      send(new_socket, response, strlen(response), 0);
      printf("Response sent\n");

      close(new_socket);
   }
}