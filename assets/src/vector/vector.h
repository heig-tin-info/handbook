#pragma once

#include <stddef.h>

typedef struct {
    void **data;
    size_t size;
    size_t capacity;
    size_t element_size;
    void (*free_function)(void *);
} Vector;

Vector *vector_create(size_t element_size, void (*free_function)(void *));
void vector_destroy(Vector *vector);

int vector_push_back(Vector *vector, void *element);
void *vector_get(Vector *vector, size_t index);
int vector_set(Vector *vector, size_t index, void *element);
size_t vector_size(Vector *vector);
