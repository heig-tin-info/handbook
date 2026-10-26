// Box-Muller: normal deviates from the uniform rand() of the C library.
// gcc -Wall -O2 -o main main.c -lm && ./main
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Uniforme sur ]0, 1] : jamais zéro, pour que log() soit défini.
static double uniform(void) {
    return (rand() + 1.0) / ((double)RAND_MAX + 1.0);
}

// Retourne un nombre tiré selon N(0, 1).
// Chaque passe de Box-Muller produit deux valeurs indépendantes :
// la seconde est conservée pour l'appel suivant.
double randn(void) {
    static int has_spare = 0;
    static double spare;

    if (has_spare) {
        has_spare = 0;
        return spare;
    }

    double u1 = uniform();
    double u2 = uniform();
    double r = sqrt(-2.0 * log(u1));
    double theta = 2.0 * M_PI * u2;

    spare = r * sin(theta);
    has_spare = 1;
    return r * cos(theta);
}

// Loi normale de moyenne mu et d'écart-type sigma.
double randn_scaled(double mu, double sigma) {
    return mu + sigma * randn();
}

int main(void) {
    srand(time(NULL));

    const int n = 100000;
    double sum = 0.0, sum2 = 0.0;
    int bins[15] = {0};

    for (int i = 0; i < n; ++i) {
        double z = randn();
        sum += z;
        sum2 += z * z;
        int b = (int)floor((z + 3.0) / 0.4); // 15 classes de 0.4 sur [-3, 3]
        if (b >= 0 && b < 15) bins[b]++;
    }

    double mean = sum / n;
    double var = sum2 / n - mean * mean;
    printf("moyenne = %.4f, écart-type = %.4f\n", mean, sqrt(var));

    for (int b = 0; b < 15; ++b) {
        printf("%5.1f | ", -3.0 + b * 0.4);
        for (int k = 0; k < bins[b] / 400; ++k) putchar('#');
        putchar('\n');
    }
}
