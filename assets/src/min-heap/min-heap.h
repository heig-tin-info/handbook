#pragma once

#include <stddef.h>
#include <stdio.h>

typedef struct MinHeap MinHeap;

MinHeap *min_heap_create(size_t element_size,
    int (*compare)(const void *, const void *),
    void (*free_function)(void *));
void min_heap_destroy(MinHeap *heap);
int min_heap_insert(MinHeap *heap, void *element);
void *min_heap_extract_min(MinHeap *heap);
size_t min_heap_size(MinHeap *heap);

void min_heap_to_mermaid(MinHeap *heap, FILE *output);