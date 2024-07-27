#include <stdlib.h>
#include <stdbool.h>

void swap(char* a, char* b)
{
    char old_a = a;
    a = b;
    b = old_a;
}

void reverse(char* str, size_t length)
{
    for (size_t start = 0, end = length - 1; start < end; start++, end--)
    {
        swap(str + start, str + end);
    }
}

void my_itoa(int num, char* str)
{
    const unsigned int base = 10;
    bool is_negative = false;
    size_t i = 0;

    if (num == 0) {
        str[i++] = '0';
        str[i] = '\0';
        return;
    }

    if (num < 0) {
        is_negative = true;
        num = -num;
    }

    while (num != 0) {
        int rem = num % 10;
        str[i++] = rem + '0';
        num /= base;
    }

    if (is_negative)
        str[i++] = '-';

    str[i] = '\0';

    reverse(str, i);
}
