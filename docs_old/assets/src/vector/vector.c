#include "vector.h"

#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 4

Vector *vector_create(size_t element_size, void (*free_function)(void *)) {
    Vector *vector = (Vector *)malloc(sizeof(Vector));
    if (!vector) return NULL;

    vector->data = malloc(INITIAL_CAPACITY * element_size);
    if (!vector->data) {
        free(vector);
        return NULL;
    }

    vector->size = 0;
    vector->capacity = INITIAL_CAPACITY;
    vector->element_size = element_size;
    vector->free_function = free_function;

    return vector;
}

void vector_destroy(Vector *vector) {
    if (!vector) return;
    if (vector->free_function) {
        for (size_t i = 0; i < vector->size; i++) {
            vector->free_function((char *)vector->data + i * vector->element_size);
        }
    }
    free(vector->data);
    free(vector);
}

int vector_push_back(Vector *vector, const void *element) {
    if (vector->size == vector->capacity) {
        vector->capacity *= 2;
        void *new_data = realloc(vector->data, vector->capacity * vector->element_size);
        if (!new_data) return -1; // realloc failed
        vector->data = new_data;
    }

    memcpy((char *)vector->data + vector->size * vector->element_size, element, vector->element_size);
    vector->size++;
    return 0;
}

void *vector_get(const Vector *vector, size_t index) {
    if (index >= vector->size) return NULL;
    return (char *)vector->data + index * vector->element_size;
}

int vector_set(Vector *vector, size_t index, const void *element) {
    if (index >= vector->size) return -1;

    if (vector->free_function) {
        vector->free_function((char *)vector->data + index * vector->element_size);
    }

    memcpy((char *)vector->data + index * vector->element_size, element, vector->element_size);
    return 0;
}

size_t vector_size(const Vector *vector) {
    return vector->size;
}

int vector_pop_back(Vector *vector) {
    if (vector->size == 0) return -1;

    vector->size--;
    if (vector->free_function) {
        vector->free_function((char *)vector->data + vector->size * vector->element_size);
    }
    return 0;
}

void *vector_get_back(const Vector *vector) {
    if (vector->size == 0) return NULL;
    return (char *)vector->data + (vector->size - 1) * vector->element_size;
}

void *vector_get_front(const Vector *vector) {
    if (vector->size == 0) return NULL;
    return vector->data;
}
