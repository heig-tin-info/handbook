#include <stdio.h>
#include <stdlib.h>
#include "vector.h"

int main() {
    Vector *vector = vector_create(sizeof(int), NULL);
    if (!vector) {
        fprintf(stderr, "Failed to create vector\n");
        return 1;
    }

    int elements[] = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    for (size_t i = 0; i < sizeof(elements) / sizeof(elements[0]); i++) {
        vector_push_back(vector, &elements[i]);
    }

    // Utilisation de vector_set pour mettre à jour un élément
    int new_value = 42;
    vector_set(vector, 3, &new_value);

    for (size_t i = 0; i < vector_size(vector); i++) {
        int *element = (int *)vector_get(vector, i);
        printf("%d ", *element);
    }
    printf("\n");

    // Utilisation de vector_get_back et vector_get_front
    int *back = (int *)vector_get_back(vector);
    int *front = (int *)vector_get_front(vector);
    if (back && front) {
        printf("Front: %d, Back: %d\n", *front, *back);
    }

    // Utilisation de vector_pop_back
    vector_pop_back(vector);

    for (size_t i = 0; i < vector_size(vector); i++) {
        int *element = (int *)vector_get(vector, i);
        printf("%d ", *element);
    }
    printf("\n");

    vector_destroy(vector);
}
