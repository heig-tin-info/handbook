#include <stdio.h>

int main(void)
{
    int t1 = 0, t2 = 1;
    int n, next_term;
    printf("Enter the number of terms: ");
    scanf("%d", &n);
    printf("Fibonacci Series: ");
    for (size_t i = 1; i <= n; ++i)
    {
        printf("%d, ", t1);
        next_term = t1 + t2;
        t1 = t2;
        t2 = next_term;
    }
    printf("\n");
}