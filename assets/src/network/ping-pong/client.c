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

   char buffer[1024] = {0};
   send(sock, ping_msg, strlen(ping_msg), 0);
   printf("Ping sent\n");
   int valread = read(sock, buffer, sizeof(buffer));
   if (valread > 0) printf("Server: %s\n", buffer);

   close(sock);
}