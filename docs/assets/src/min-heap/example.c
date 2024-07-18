#include "min-heap.h"

#include <stdio.h>

int compare_int(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;
}

int main() {
    MinHeap *heap = min_heap_create(sizeof(int), compare_int, NULL);
    if (!heap) {
        fprintf(stderr, "Failed to create min heap\n");
        return 1;
    }

    int elements[] = {1,2,3,4,5,6,7,8,9,10};
    for (size_t i = 0; i < sizeof(elements) / sizeof(elements[0]); i++) {
        min_heap_insert(heap, &elements[i]);
    }

    min_heap_to_mermaid(heap, stdout);

    min_heap_destroy(heap);
}