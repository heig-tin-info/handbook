#pragma once

#include <stddef.h>

typedef struct {
    void **data;
    size_t capacity;
    size_t size;
    int (*compare)(const void *, const void *);
} MaxHeap;

MaxHeap *max_heap_create(size_t capacity, int (*compare)(const void *, const void *));
void max_heap_insert(MaxHeap *heap, void *item);
void *max_heap_extract_max(MaxHeap *heap);
void max_heap_free(MaxHeap *heap);
