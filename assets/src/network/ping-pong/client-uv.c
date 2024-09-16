#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uv.h>

#define PORT 8080

uv_loop_t *loop;
uv_tcp_t socket_client;
uv_connect_t connect_req;

void alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf) {
   buf->base = (char *)malloc(suggested_size);
   buf->len = suggested_size;
}

void on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf) {
   if (nread > 0) {
      printf("Server: %s\n", buf->base);
   } else if (nread < 0) {
      fprintf(stderr, "Read error: %s\n", uv_err_name(nread));
      uv_close((uv_handle_t *)client, NULL);
   }

   free(buf->base);
}

void on_write(uv_write_t *req, int status) {
   if (status) fprintf(stderr, "Write error: %s\n", uv_strerror(status));
   printf("Ping sent to server\n");
   uv_read_start((uv_stream_t *)req->handle, alloc_buffer, on_read);
   free(req);
}

void on_connect(uv_connect_t *req, int status) {
   if (status < 0) {
      fprintf(stderr, "Connection error: %s\n", uv_strerror(status));
      return;
   }
   printf("Connected to server\n");

   uv_write_t *write_req = (uv_write_t *)malloc(sizeof(uv_write_t));
   const char *ping_msg = "ping";
   uv_buf_t buffer = uv_buf_init((char *)ping_msg, strlen(ping_msg));
   uv_write(write_req, req->handle, &buffer, 1, on_write);
}

int main() {
   loop = uv_default_loop();
   uv_tcp_init(loop, &socket_client);
   struct sockaddr_in dest;
   uv_ip4_addr("127.0.0.1", PORT, &dest);
   uv_tcp_connect(&connect_req, &socket_client, (const struct sockaddr *)&dest,
                  on_connect);
   return uv_run(loop, UV_RUN_DEFAULT);  // Boucle d'événements
}
