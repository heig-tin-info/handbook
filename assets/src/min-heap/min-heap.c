#include <stdlib.h>
#include <string.h>
#include "min-heap.h"

static void swap(void **a, void **b) {
    void *temp = *a;
    *a = *b;
    *b = temp;
}

static void heapify_down(MinHeap *heap, size_t index) {
    size_t smallest = index;
    size_t left = 2 * index + 1;
    size_t right = 2 * index + 2;

    if (left < heap->size && heap->compare(heap->data[left], heap->data[smallest]) < 0) {
        smallest = left;
    }
    if (right < heap->size && heap->compare(heap->data[right], heap->data[smallest]) < 0) {
        smallest = right;
    }
    if (smallest != index) {
        swap(&heap->data[index], &heap->data[smallest]);
        heapify_down(heap, smallest);
    }
}

static void heapify_up(MinHeap *heap, size_t index) {
    if (index && heap->compare(heap->data[index], heap->data[(index - 1) / 2]) < 0) {
        swap(&heap->data[index], &heap->data[(index - 1) / 2]);
        heapify_up(heap, (index - 1) / 2);
    }
}

MinHeap *min_heap_create(size_t capacity, int (*compare)(const void *, const void *)) {
    MinHeap *heap = (MinHeap *)malloc(sizeof(MinHeap));
    if (!heap) return NULL;

    heap->data = (void **)malloc(sizeof(void *) * capacity);
    if (!heap->data) {
        free(heap);
        return NULL;
    }

    heap->capacity = capacity;
    heap->size = 0;
    heap->compare = compare;

    return heap;
}

void min_heap_insert(MinHeap *heap, void *item) {
    if (heap->size == heap->capacity) {
        heap->capacity *= 2;
        heap->data = (void **)realloc(heap->data, sizeof(void *) * heap->capacity);
    }

    heap->data[heap->size] = item;
    heapify_up(heap, heap->size);
    heap->size++;
}

void *min_heap_extract_min(MinHeap *heap) {
    if (heap->size == 0) return NULL;

    void *min = heap->data[0];
    heap->data[0] = heap->data[--heap->size];
    heapify_down(heap, 0);

    return min;
}

void min_heap_free(MinHeap *heap) {
    free(heap->data);
    free(heap);
}
