#include <stdlib.h>
#include <stdio.h>

/**
 * Merges two subarrays of `arr`.
 * @return arr[l..m] + arr[m+1..r]
 */
void merge(int arr[], int l, int m, int r)
{
    const int n1 = m - l + 1;
    const int n2 = r - m;

    int L[n1], R[n2];

    // Copy data to temp arrays L[] and R[]
    for (size_t i = 0; i < n1; i++)
        L[i] = arr[l + i];

    for (size_t j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    // Merge the temp arrays back into arr[l..r]
    size_t i = 0; // Initial index of first subarray
    size_t j = 0; // Initial index of second subarray
    size_t k = l; // Initial index of merged subarray

    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j])
        {
            arr[k] = L[i];
            i++;
        }
        else
        {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of L[], if there are any
    while (i < n1)
    {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of R[], if there are any
    while (j < n2)
    {
        arr[k] = R[j];
        j++;
        k++;
    }
}

// l is for left index and r is right index of the sub-array of arr to be sorted.
void merge_sort(int arr[], int l, int r)
{
    if (l < r)
    {
        size_t m = l + (r - l) / 2;

        // Sort first and second halves
        merge_sort(arr, l, m);
        merge_sort(arr, m + 1, r);

        merge(arr, l, m, r);
    }
}

void print_array(int arr[], int size)
{
    for (size_t i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main(void)
{
    int arr[] = {12, 11, 13, 5, 6, 7};
    int arr_size = sizeof(arr) / sizeof(arr[0]);

    printf("Given array is \n");
    print_array(arr, arr_size);

    merge_sort(arr, 0, arr_size - 1);

    printf("\nSorted array is \n");
    print_array(arr, arr_size);
    return 0;
}
