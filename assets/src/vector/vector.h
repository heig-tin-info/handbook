#pragma once

#include <stddef.h>

typedef struct {
    void *data;
    size_t size;
    size_t capacity;
    size_t element_size;
    void (*free_function)(void *);
} Vector;

Vector *vector_create(size_t element_size, void (*free_function)(void *));
void vector_destroy(Vector *vector);

int vector_push_back(Vector *vector, const void *element);
void *vector_get(const Vector *vector, size_t index);
int vector_set(Vector *vector, size_t index, const void *element);
size_t vector_size(const Vector *vector);
int vector_pop_back(Vector *vector);
void *vector_get_back(const Vector *vector);
void *vector_get_front(const Vector *vector);
