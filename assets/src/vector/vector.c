#include "vector.h"

#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 4

Vector *vector_create(size_t element_size, void (*free_function)(void *)) {
    Vector *vector = (Vector *)malloc(sizeof(Vector));
    if (!vector) return NULL;

    vector->data = (void **)malloc(INITIAL_CAPACITY * sizeof(void *));
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
    if (vector) {
        if (vector->free_function) {
            for (size_t i = 0; i < vector->size; i++) {
                vector->free_function(vector->data[i]);
            }
        }
        free(vector->data);
        free(vector);
    }
}

int vector_push_back(Vector *vector, void *element) {
    if (vector->size == vector->capacity) {
        vector->capacity *= 2;
        void **new_data = (void **)realloc(vector->data, vector->capacity * sizeof(void *));
        if (!new_data) return -1; // realloc failed
        vector->data = new_data;
    }

    vector->data[vector->size] = malloc(vector->element_size);
    if (!vector->data[vector->size]) return -1; // malloc failed

    memcpy(vector->data[vector->size], element, vector->element_size);
    vector->size++;
    return 0;
}

void *vector_get(Vector *vector, size_t index) {
    if (index >= vector->size) return NULL;
    return vector->data[index];
}

int vector_set(Vector *vector, size_t index, void *element) {
    if (index >= vector->size) return -1;

    if (vector->free_function) {
        vector->free_function(vector->data[index]);
    }

    memcpy(vector->data[index], element, vector->element_size);
    return 0;
}

size_t vector_size(Vector *vector) {
    return vector->size;
}
