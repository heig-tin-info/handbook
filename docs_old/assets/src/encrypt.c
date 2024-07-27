#include <caesar.h>
#include <stdio.h>

#define KEY 13

int main(int argc, char *argv[])
{
    for (int i = 1; i < argc; i++)
    {
        caesar(argv[i], KEY);
        printf("%s\n", argv[i]);
    }
}