#include <stdio.h>
#include <stdlib.h>

int recurse(int n, int stack_size)
{
    char array[1024*1024] = {0};
    printf("used stack: %d kiB\n", stack_size / 1024);
    if (n == 0) return 0;
    return recurse(n - 1, stack_size + sizeof(array));
}

int main(int argc, char* argv[])
{
    recurse(atoi(argv[1]), 0);
}