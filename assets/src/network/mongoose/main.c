#include "mongoose.h"

void ev_handler(struct mg_connection *c, int ev, void *ev_data) {
   if (ev == MG_EV_HTTP_MSG) {
      struct mg_http_message *hm = (struct mg_http_message *)ev_data;
      if (mg_match(hm->uri, mg_str("/"), NULL)) {
         mg_http_reply(c, 200, "", "Hello, world!\n");
      } else if (mg_match(hm->uri, mg_str("/source"), NULL)) {
         struct mg_http_serve_opts opts = {.root_dir = "./www"};
         mg_http_serve_dir(c, hm, &opts);
      } else if (mg_match(hm->uri, mg_str("/api/time/get"), NULL)) {
         mg_http_reply(c, 200, "", "{%m:%lu}\n", MG_ESC("time"), time(NULL));
      } else if (mg_match(hm->uri, mg_str("/teapot"), NULL)) {
         mg_http_reply(c, 418, "", "I'm a teapot\n");
      } else {
         mg_http_reply(c, 500, "", "{%m:%m}\n", MG_ESC("error"),
                       MG_ESC("Unsupported URI"));
      }
   }
}

int main(void) {
   struct mg_mgr mgr;
   mg_mgr_init(&mgr);
   mg_http_listen(&mgr, "http://0.0.0.0:8090", ev_handler, NULL);
   for (;;) mg_mgr_poll(&mgr, 1000);
}