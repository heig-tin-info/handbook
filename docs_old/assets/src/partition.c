#include <stdio.h>

void swap(int *a, int *b) { int tmp = *a; *a = *b; *b = tmp; }

int display(int a[], int low, int high) {
    for (int i = low; i <= high; i++)
        printf("%x ", a[i]);
    printf("\n");
}

int partition (int a[], int low, int high, int pivot)
{
    int i = low;
    for (int j = low; j < high; j++)
        if (a[j] < a[pivot]) {
            swap(&a[i++], &a[j]);
            display(a, low, high);
        }
    swap(&a[i], &a[pivot]);
    display(a, low, high);
    return i;
}

int main() {
    int array[] = {2, 9, 4, 1, 11, 5, 10, 7, 3, 8, 6};
    const int size = sizeof(array) / sizeof(*array);
    partition(array, 0, size - 1, size - 1);
}
