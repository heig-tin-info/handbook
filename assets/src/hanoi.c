#include <stdio.h>

void hanoi(int n, char from, char to, char aux) {
    if (n == 1) {
        printf("Déplacer le disque 1 de %c à %c\n", from, to);
        return;
    }
    hanoi(n - 1, from, aux, to);
    printf("Déplacer le disque %d de %c à %c\n", n, from, to);
    hanoi(n - 1, aux, to, from);
}

int main() {
    int n = 3;
    hanoi(n, 'A', 'C', 'B');
}