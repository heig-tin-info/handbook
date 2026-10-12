#include "min-heap.h"

#include <stdio.h>
#include <stdlib.h>

int compare_int(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;
}

void print_int(void *element, FILE *output) {
    fprintf(output, "%d", *(int *)element);
}

int main() {
    MinHeap *heap = min_heap_create(sizeof(int), compare_int, free);
    if (!heap) {
        fprintf(stderr, "Failed to create min heap\n");
        return 1;
    }

    int elements[] = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    for (size_t i = 0; i < sizeof(elements) / sizeof(elements[0]); i++) {
        int *element = malloc(sizeof(int));
        if (!element) {
            fprintf(stderr, "Failed to allocate memory for element\n");
            min_heap_destroy(heap);
            return 1;
        }
        *element = elements[i];
        min_heap_insert(heap, element);
    }

    min_heap_to_mermaid(heap, stdout, print_int);

    while (min_heap_size(heap) > 0) {
        int *element = (int *)min_heap_extract_min(heap);
        printf("Extracted: %d\n", *element);
        free(element); // Libération après extraction
    }

    min_heap_destroy(heap);
    return 0;
}
