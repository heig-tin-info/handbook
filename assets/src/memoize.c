#include <stdio.h>
#include <stdbool.h>

#define SIZE 1000

bool cache_input[SIZE] = { false };
int cache_output[SIZE];

int memoize(int input, int output) {
    cache_input[input % SIZE] = true;
    cache_output[input % SIZE] = output;
    return output;
}

bool memoize_has(int input) {
    return cache_input[input % SIZE];
}

int memoize_get(int input) {
    return cache_output[input % SIZE];
}

int fib(int n)
{
    if (memoize_has(n)) return memoize_get(n);
    if (n < 2) return 1;
    return memoize(n, fib(n - 1) + fib(n - 2));
}

int main() {
    for (int i = 0; i < 40; i++) {
        printf("%d\n", fib(i));
    }
}