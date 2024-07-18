#pragma once

#include <stddef.h>

typedef struct MaxHeap MaxHeap;

MaxHeap *max_heap_create(size_t element_size,
    int (*compare)(const void *, const void *),
    void (*free_function)(void *));
void max_heap_destroy(MaxHeap *heap);
int max_heap_insert(MaxHeap *heap, void *element);
void *max_heap_extract_max(MaxHeap *heap);
size_t max_heap_size(MaxHeap *heap);