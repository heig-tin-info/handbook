#include "max-heap.h"
#include "vector.h"

#include <stdlib.h>

struct MaxHeap {
    Vector *vector;
    int (*compare)(const void *, const void *);
};

static void swap(void **a, void **b) {
    void *temp = *a;
    *a = *b;
    *b = temp;
}

static void heapify_up(MaxHeap *heap, size_t index) {
    if (index == 0) return;

    size_t parent_index = (index - 1) / 2;
    if (heap->compare(vector_get(heap->vector, index), vector_get(heap->vector, parent_index)) > 0) {
        swap(&heap->vector->data[index], &heap->vector->data[parent_index]);
        heapify_up(heap, parent_index);
    }
}

static void heapify_down(MaxHeap *heap, size_t index) {
    size_t left_child = 2 * index + 1;
    size_t right_child = 2 * index + 2;
    size_t largest = index;

    if (left_child < vector_size(heap->vector) &&
        heap->compare(vector_get(heap->vector, left_child), vector_get(heap->vector, largest)) > 0) {
        largest = left_child;
    }
    if (right_child < vector_size(heap->vector) &&
        heap->compare(vector_get(heap->vector, right_child), vector_get(heap->vector, largest)) > 0) {
        largest = right_child;
    }
    if (largest != index) {
        swap(&heap->vector->data[index], &heap->vector->data[largest]);
        heapify_down(heap, largest);
    }
}

MaxHeap *max_heap_create(size_t element_size, int (*compare)(const void *, const void *), void (*free_function)(void *)) {
    MaxHeap *heap = (MaxHeap *)malloc(sizeof(MaxHeap));
    if (!heap) return NULL;

    heap->vector = vector_create(element_size, free_function);
    if (!heap->vector) {
        free(heap);
        return NULL;
    }

    heap->compare = compare;
    return heap;
}

void max_heap_destroy(MaxHeap *heap) {
    if (heap) {
        vector_destroy(heap->vector);
        free(heap);
    }
}

int max_heap_insert(MaxHeap *heap, void *element) {
    if (vector_push_back(heap->vector, element) != 0) return -1;
    heapify_up(heap, vector_size(heap->vector) - 1);
    return 0;
}

void *max_heap_extract_max(MaxHeap *heap) {
    if (vector_size(heap->vector) == 0) return NULL;

    void *max_element = vector_get(heap->vector, 0);
    void *last_element = vector_get(heap->vector, vector_size(heap->vector) - 1);
    vector_set(heap->vector, 0, last_element);
    heap->vector->size--; // Adjust size without deallocating the last element

    heapify_down(heap, 0);
    return max_element;
}

size_t max_heap_size(MaxHeap *heap) {
    return vector_size(heap->vector);
}
