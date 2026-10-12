#include "slurp.h"

int main(int argc, char *argv[]) {
   if (argc <= 1) {
      fprintf(stderr, "Usage: %s <file>\n", argv[0]);
      return 1;
   }
   FILE *file = fopen(argv[1], "r");
   if (file == NULL) {
      fprintf(stderr, "Error opening file\n");
      return 1;
   }
   char *data = slurp(file);
   fclose(file);
   printf("%s", data);
}