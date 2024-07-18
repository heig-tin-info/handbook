#include <stdio.h>
#include <string.h>

#define BAND_SIZE 1000

int main() {
    char tape[BAND_SIZE] = {0};
    int head = BAND_SIZE / 2; // Position au milieu de la bande

    scanf("%s", tape + head); // Saisie du nombre d'entrée

    // Algorithme d'addition
    char c = tape[head];
    while (c == '0' || c == '1')
        c = tape[++head];
    c =  tape[--head];
    while (c == '1') {
        tape[head--] = '0';
        c = tape[head];
    }
    tape[head] = '1';

    // Recherche de la position du premier symbole non nul
    while (tape[head]) head--;
    head++;
    printf("%s\n", tape + head);
}