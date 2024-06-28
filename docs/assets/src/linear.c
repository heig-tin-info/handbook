#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    float x;
    float offset;
    float slope;

    if (argc > 2) {
        offset = atof(argv[1]);
        slope = atof(argv[2]);
    } else {
        float offset_default = 0.;
        printf("Offset? [%f]: ", offset_default);
        if (!scanf("%f", &offset)) {
            offset = offset_default;
        }

        float slope_default = 1.;
        printf("Pente? [%f]: ", slope_default);
        if (!scanf("%f", &slope)) {
            slope = slope_default;
        }
    }

    if (argc == 2 || argc > 3) {
        slope = atof(argv[argc == 2 ? 2: 3]);
    } else {
        float x_default = 0;
        printf("x (abscisse) [%f]:", x_default);
        if (!scanf("%f", &x)) {
            x = x_default;
        }
    }

    printf("%f\n", slope * x + offset);

    return 0;
}
