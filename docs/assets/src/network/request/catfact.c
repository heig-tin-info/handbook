#include <curl/curl.h>
#include <json-c/json.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct response {
   char *memory;
   size_t size;
};

static size_t write_callback(void *data, size_t size, size_t nmemb,
                             void *userp) {
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
