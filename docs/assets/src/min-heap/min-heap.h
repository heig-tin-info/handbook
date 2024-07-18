#pragma once

#include <stddef.h>

typedef struct {
    void **data;
    size_t capacity;
    size_t size;
    int (*compare)(const void *, const void *);
} MinHeap;

MinHeap *min_heap_create(size_t capacity, int (*compare)(const void *, const void *));
void min_heap_insert(MinHeap *heap, void *item);
void *min_heap_extract_min(MinHeap *heap);
void min_heap_free(MinHeap *heap);
