#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static size_t get_total_length(const char **strings, size_t count,
                               const char *delimiter) {
   size_t total_length = 0;
   size_t delimiter_length = strlen(delimiter);

   for (size_t i = 0; i < count; i++) {
      total_length += strlen(strings[i]);
      if (i < count - 1) total_length += delimiter_length;
   }
   return total_length + sizeof('\0');
}

char *join(const char **strings, size_t count, const char *delimiter) {
   if (strings == NULL || count == 0) return NULL;

   size_t total_length = get_total_length(strings, count, delimiter);

   char *result = (char *)malloc(total_length);
   if (result == NULL) {
      fprintf(stderr, "Memory allocation failed in %s\n", __func__);
      return NULL;
   }

   result[0] = '\0';
   for (size_t i = 0; i < count; i++) {
      strcat(result, strings[i]);
      if (i < count - 1) strcat(result, delimiter);
   }
   return result;
}

// Exemple d'utilisation de la fonction `join`
int main() {
   const char *strings[] = {"apple", "banana", "orange", "grape"};
   char *result = join(strings, 4, ", ");

   if (result == NULL) fprintf(stderr, "Error joining strings\n");

   printf("%s\n", result);
   free(result);  // Because `join` allocates memory,
                  // it should be freed after use
}
