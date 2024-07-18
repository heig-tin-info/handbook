#include "min-heap.h"
#include "vector.h"

#include <stdlib.h>
#include <stdio.h>

struct MinHeap {
    Vector *vector;
    int (*compare)(const void *, const void *);
};

static void swap(void **a, void **b) {
    void *temp = *a;
    *a = *b;
    *b = temp;
}

static void heapify_up(MinHeap *heap, size_t index) {
    if (index == 0) return;

    size_t parent_index = (index - 1) / 2;
    if (heap->compare(vector_get(heap->vector, index), vector_get(heap->vector, parent_index)) < 0) {
        swap(&heap->vector->data[index], &heap->vector->data[parent_index]);
        heapify_up(heap, parent_index);
    }
}

static void heapify_down(MinHeap *heap, size_t index) {
    size_t left_child = 2 * index + 1;
    size_t right_child = 2 * index + 2;
    size_t smallest = index;

    if (left_child < vector_size(heap->vector) &&
        heap->compare(vector_get(heap->vector, left_child), vector_get(heap->vector, smallest)) < 0) {
        smallest = left_child;
    }
    if (right_child < vector_size(heap->vector) &&
        heap->compare(vector_get(heap->vector, right_child), vector_get(heap->vector, smallest)) < 0) {
        smallest = right_child;
    }
    if (smallest != index) {
        swap(&heap->vector->data[index], &heap->vector->data[smallest]);
        heapify_down(heap, smallest);
    }
}

MinHeap *min_heap_create(size_t element_size, int (*compare)(const void *, const void *), void (*free_function)(void *)) {
    MinHeap *heap = (MinHeap *)malloc(sizeof(MinHeap));
    if (!heap) return NULL;

    heap->vector = vector_create(element_size, free_function);
    if (!heap->vector) {
        free(heap);
        return NULL;
    }

    heap->compare = compare;
    return heap;
}

void min_heap_destroy(MinHeap *heap) {
    if (heap) {
        vector_destroy(heap->vector);
        free(heap);
    }
}

int min_heap_insert(MinHeap *heap, void *element) {
    if (vector_push_back(heap->vector, element) != 0) return -1;
    heapify_up(heap, vector_size(heap->vector) - 1);
    return 0;
}

void *min_heap_extract_min(MinHeap *heap) {
    if (vector_size(heap->vector) == 0) return NULL;

    void *min_element = vector_get(heap->vector, 0);
    void *last_element = vector_get(heap->vector, vector_size(heap->vector) - 1);
    vector_set(heap->vector, 0, last_element);
    heap->vector->size--; // Adjust size without deallocating the last element

    heapify_down(heap, 0);
    return min_element;
}

size_t min_heap_size(MinHeap *heap) {
    return vector_size(heap->vector);
}

void min_heap_to_mermaid(MinHeap *heap, FILE *output) {
    fprintf(output, "graph TD\n");
    for (size_t i = 0; i < vector_size(heap->vector); i++) {
        fprintf(output, "  %zu((%d))\n", i, *(int *)vector_get(heap->vector, i));
        if (i > 0) {
            size_t parent = (i - 1) / 2;
            fprintf(output, "  %zu --> %zu\n", parent, i);
        }
    }
}