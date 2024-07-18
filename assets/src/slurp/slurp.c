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

    while (!feof(stdin)) {
        if (len + 128 >= size) {
            size *= 2;
            input = (char *)realloc(input, size);
            if (input == NULL) {
                fprintf(stderr, "Memory reallocation failed\n");
                exit(1);
            }
        }
        len += fread(input + len, 1, size - len - 1, stdin);
    }
    input[len] = '\0';
    return input;
}