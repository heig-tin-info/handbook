#include <stdio.h>
#include <stdlib.h>

char *slurp(FILE *file) {
   size_t size = 256;
   size_t len = 0;
   char *input = (char *)malloc(size);

   if (input == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      exit(1);
   }

   size_t bytesRead;
   while ((bytesRead = fread(input + len, 1, size - len - 1, file)) > 0) {
      len += bytesRead;
      if (len + 1 >= size) {
         size *= 2;
         char *newInput = (char *)realloc(input, size);
         if (newInput == NULL) {
            free(input);
            fprintf(stderr, "Memory reallocation failed\n");
            exit(1);
         }
         input = newInput;
      }
   }

   if (ferror(file)) {
      free(input);
      fprintf(stderr, "Error reading file\n");
      exit(1);
   }

   input[len] = '\0';
   return input;
}