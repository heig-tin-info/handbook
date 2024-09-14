[](){#fast-sin}

# Sinus rapide

Dans des architectures sans support pour les nombres réels (comme les processeurs ne supportant pas les opérations en virgule flottante IEEE 754), il est courant d'utiliser des approximations polynomiales pour calculer des fonctions mathématiques comme le sinus. Calculer un sinus n'est pas une simple opération, comme l'addition ou la multiplication, et il n'existe pas d'algorithme trivial pour obtenir une valeur exacte.

Les processeurs modernes, lorsqu'ils calculent le sinus, utilisent souvent des **tables de valeurs prédéfinies** (appelées tables de sinus) stockées en mémoire. Ces tables contiennent des valeurs pré-calculées du sinus pour différents angles, généralement entre 0 et $\pi/2$. Lorsqu'un sinus doit être calculé, le processeur se base sur la valeur dans la table la plus proche de l'angle donné, puis utilise une interpolation souvent linéaire pour obtenir un résultat plus précis. Cette méthode permet d'économiser du temps de calcul au prix d'une petite perte de précision. Voici une manière de faire :

$$
\sin(\theta) \approx \sin(\theta_1) + \frac{\sin(\theta) - \sin(\theta_1)}{\theta_2 - \theta_1} \times (\sin(\theta_2) - \sin(\theta_1))
$$

où $\sin(\theta_1)$ et $\sin(\theta_2)$ sont les valeurs de sinus les plus proches de $\theta$ dans la table, $\theta$ est l'angle pour lequel le sinus doit être calculé. La recherche dans la table peut être simplement une table de hachage pour un accès en $O(1)$.

```c
#include <stdio.h>

#define TABLE_SIZE 1024

double sin_table[TABLE_SIZE];

// Computed on a powerful machine (with floating point support)
void init_sin_table() {
    for (int i = 0; i < TABLE_SIZE; ++i)
        sin_table[i] = sin((double)i / TABLE_SIZE * M_PI / 2);
}

double sin_fast(double angle) {
    double x = angle / (M_PI / 2) * TABLE_SIZE;
    int i = (int)x;
    double frac = x - i;
    return sin_table[i] + frac * (sin_table[i + 1] - sin_table[i]);
}
```

Dans une architecture légère qui ne dispose pas de support pour les nombres en virgule flottante, on utilise plutôt des **approximations en virgule fixe**. Ces approximations polynomiales, comme le développement de Taylor, permettent de calculer des sinus avec une précision acceptable, tout en restant dans le domaine des entiers.

### Approximation du cinquième ordre

Ce qui suit est grandement inspiré du travail d'Andrew Steadman et son article [5th Order Polynomial Fixed-Point Sine Approximation](https://www.nullhardware.com/blog/fixed-point-sine-and-cosine-for-embedded-systems/) publié en 2018 lui même inspiré d'un autre travail seulement disponible sur le [web archive](https://web.archive.org/web/20190119030856/https://www.coranac.com/2009/07/sines/).

Le domaine du sinus est infini mais il est possible de le réduire à l'intervalle ci-dessous car toutes les autres sorties pouvant être obtenues en utilisant les propriétés de symétrie du sinus.

$$
x \in [0, \frac{\pi}{2}]
$$

D'autre part, le sinus est une fonction impaire, c'est-à-dire que $\sin(-x) = -\sin(x)$. Cette propriété induit lors d'une décomposition en série de Fourier que les coefficients de la série de Fourier pour les termes pairs sont nuls. Cela signifie que le sinus peut être approximé par un polynôme de degré impair. On peut donc tenter d'approximer un sinus par un polynôme de degré 5 en ayant seulement 3 coefficients à calculer. D'autre part, afin de faciliter les calculs, on peut réduire l'intervalle de calcul à $[0, 1]$ en posant que :

$$
x = z\frac{\pi}{2}
$$

Le polynôme de degré 5 peut être exprimé de la manière suivante :

$$
\sin(z) \approx S_5 = cz - bz^3 + az^5
$$


Pour résoudre cette équation à trois inconnues, on peut utiliser les propriétés du sinus et de ses dérivées. On peut poser que :

$$
S_5(z) = az^5 - bz^3 + cz
S_5'(z) = a5z^4 - b3z^2 + c
$$

On peut noter quelques conditions aux bords:

- $S_5(1) = 1$ qui est équivalent à $\sin(\frac{\pi}{2}) = 1$
- $S_5'(1) = 0$ Et la pente est nulle
- $S_5'(0) = \frac{\pi}{2}$ car la pente est maximale en 0

Ce qui nous permet de poser :

$$
1 = a - b + c
0 = 5a - 3b + 5c
\frac{\pi}{2} = a
$$

Le système peut être résolu en utilisant une méthode de résolution de système d'équations linéaires. On obtient les coefficients suivants :

$$
a = \frac{\pi}{2}
b = \pi-\frac{5}{2}
c = \frac{\pi}{2}-\frac{3}{2}
$$

Que l'on peut réécrire :

$$
a = \frac{\pi}{2}
b = 2a-\frac{5}{2}
c = a-\frac{3}{2}
$$

On peut alors calculer le sinus en utilisant ces coefficients. En outre, lorsqu'on cherche à approximer une fonction, l'une des façons de s'assurer que l'approximation est correcte sur une certaine plage est de minimiser l'erreur moyenne entre la fonction approximée et la vraie fonction. Cela signifie que, sur un intervalle donné, la somme des erreurs (en moyenne) doit être la plus proche possible de zéro. Cette approche permet de redistribuer les erreurs uniformément plutôt que de les concentrer sur certains points.

L'erreur moyenne pour une fonction est souvent calculée en prenant l'intégrale de la différence entre la fonction approximée etla vraie fonction sur l'intervalle donné. ici $[0, 1]$. En d'autres termes, si $f(x)$ est la fonction que l'on souhaite approximer et $p(x)$ est l'approximation polynomiale, l'erreur moyenne est donnée par :

$$
\int_0^1 [f(x)-p(x)]dx
$$

Appliqué à notre cas de figure, c'est à dire le sinus et une approximation polynomiale de degré $n$, on obtient :

$$
\int_0^1 \sum_n a_nx^ndx=\int_0^1 \sin(x\cdot\pi/2)dx=\frac{2}{\pi}
$$

Ceci nous permet d'obtenir des coefficients alternatifs pour l'approximation du sinus :

$$
a = 4(\frac{3}{\pi}-\frac{9}{16})
b = 2a-\frac{5}{2}
c = a-\frac{3}{2}
$$

Sur une architecture en virgule fixe comme un microcontrôleur MSP430 16-bit, on peut par exemple utiliser un entier de 16-bit pour représenter un angle. Ce dernier peut être exprimé en radians en complément à deux et en format Q15.1. Cela signifie que la partie entière représente les radians et la partie fractionnaire représente les décimales. Par exemple, 1.0 en Q15.1 est représenté par 0x8000. En termes binaire notre équation devra être multipliée par $2^{15}$ pour obtenir un résultat correct. On peut rendre générique cette définition en déclarant $a$ l'exponent de la puissance de 2 à appliquer. Notre équation complète est donc :

$$
sin_5(x) = 2^a\left(az - bz^3 + cz^5\right)
$$

Or, l'équation doit pouvoir être réécrite seulement en terme de multiplications d'entiers et de décalages. Comme $z\in[0, 1]$, on peut écrire $z$ comme $y/2^a$ avec $y\in[0, 2^a]$. On peut alors réécrire l'équation en s'affranchissant des puissances:

$$
\begin{aligned}
sin_5(x) &= 2^a\left(az - bz^3 + cz^5\right)\\
&= z\left(a-z^2\left[b-z^2c\right]\right)2^a\\
&= \frac{y}{2^n}\left(a-\frac{y^2}{2^{2n}}\left[b-\frac{y^2}{2^{2n}}c\right]\right)2^a\\
&= y2^{-n}\left(a-\frac{y^2}{2^{2n}}\left[b-\frac{y^2}{2^{2n}}c\right]\right)2^a\\
&= y\left(a-\frac{y^2}{2^{2n}}\left[b-\frac{y^2}{2^{2n}}c\right]\right)2^{a-n}\\
\end{aligned}
$$

Afin de maximiser la précision, on a besoin que nos multiplications occupent le plus de bits possibles pour le type choisi. À cette fin, on peut introduire des facteurs d'échelle $2^p$, $2^q$ et $2^r$ sachant qu'ils s'annuleront et n'affecterons pas le résultat final. On peut alors réécrire l'équation en introduisant ces facteurs d'échelle :

$$
\begin{aligned}
= y2^{p-n}\left(a-y2^{-n}y{2^-n}\left[b-2^{-r}y2^{-2n}2^rcy\right]\right)2^{a}\\
= y2^{p-n}\left(a-2^{-p}y2^{-n}y{2^-n}\left[2^Pb-2^{-r}y2^{-2n}2^{r+p}cy\right]\right)2^{a}\\
= y2^{-n}\left(2^qa-2^{q-p}y2^{-n}\left[2^Pb-2^{-r}y2^{-n}2^{r+p-n}cy\right]\right)2^{a-q}\\
\end{aligned}
$$

En redéfinissant les constantes $A$, $B$ et $C$ comme suit :

$$
A = 2^qa
B = 2^Pb
C = 2^{r+p-n}c
$$

On obtient l'équation finale :

$$
= y2^{-n}\left(A-2^{q-p}y2^{-n}y2^{-n}\left[B-2^{-r}y2^{-n}Cy\right]\right)2^{a-q}
$$

On peut maintenant essayer de maximiser chaque multiplication en travaillant depuis l'intérieur de l'équation en direction de l'extérieur de façon à ce que le produit soit exactement 32-bit. On peut également ajuster l'échelle du résultat en virgule fixe pour obtenir une précision maximale. Le résultat final est :

```c
a = 12;
n = 13;
p = 32;
q = 31;
r = 3;

A = 3370945099;
B = 2746362156;
C = 292421;
```

Enfin, on peut implémenter cette approximation en C :

```c
#include <stdio.h>
#include <stdint.h>
#include <math.h>

int16_t fpsin(int16_t i) {
   i <<= 1;
   uint8_t c = i < 0;

   if (i == (i | 0x4000)) i = (1 << 15) - i;
   i = (i & 0x7FFF) >> 1;

   enum { A1 = 3370945099UL, B1 = 2746362156UL, C1 = 292421UL };
   enum { n = 13, p = 32, q = 31, r = 3, a = 12 };

   uint32_t y = (C1 * ((uint32_t)i)) >> n;
   y = B1 - (((uint32_t)i * y) >> r);
   y = (uint32_t)i * (y >> n);
   y = (uint32_t)i * (y >> n);
   y = A1 - (y >> (p - q));
   y = (uint32_t)i * (y >> n);
   y = (y + (1UL << (q - a - 1))) >> (q - a);

   return c ? -y : y;
}

int main() {
    // Quelques angles : (0, pi/2, pi, 3pi/2, 2pi)
    const int16_t angles[] = {0, 16384, 32768, 49152, 65536};

    printf("Angle (deg)\tFixed-Point Sin\tStandard Sin\tError\n");
    for (int i = 0; i < 5; ++i) {
        int16_t angle = angles[i];
        double radians = (double)angle / 65536.0 * M_PI;

        int16_t fpsin_result = fpsin(angle);
        double sin_result = sin(radians);
        double sin_fixed_point = sin_result * 4096.0;
        double error = fpsin_result - sin_fixed_point;

        printf("%d\t\t%d\t\t%.2f\t\t%.2f\n", (int)(radians * 180.0 / M_PI),
            fpsin_result, sin_fixed_point, error);
    }
}
```

### Démonstration graphique avec SDL

Voici un exemple qui utilise SDL pour afficher un graphe montrant le sinus en virgule fixe et l'erreur par rapport à la fonction sinus standard.

```c
#include <SDL2/SDL.h>
#include <math.h>

#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 480

void draw_graph(SDL_Renderer *renderer) {
    // Dessine le sinus en virgule fixe et la version standard
    for (int x = 0; x < SCREEN_WIDTH; x++) {
        // Mappe x à un angle (entre 0 et 2pi)
        double angle = (double)x / SCREEN_WIDTH * 2.0 * M_PI;
        int y_fixed = (int)((fpsin((int16_t)(angle * 65536.0 / (2.0 * M_PI))) / 4096.0) * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 2);
        int y_standard = (int)((sin(angle) * SCREEN_HEIGHT / 2) + SCREEN_HEIGHT / 2);

        // Sinus standard en rouge
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
        SDL_RenderDrawPoint(renderer, x, y_standard);

        // Sinus en virgule fixe en vert
        SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255);
        SDL_RenderDrawPoint(renderer, x, y_fixed);

        // Erreur en bleu
        int error = y_fixed - y_standard;
        SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
        SDL_RenderDrawPoint(renderer, x, SCREEN_HEIGHT / 2 - error);
    }
}

int main(int argc, char *argv[]) {
    SDL_Window *window = NULL;
    SDL_Renderer *renderer = NULL;

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    window = SDL_CreateWindow("Sinus Approximation", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_RenderClear(renderer);

    draw_graph(renderer);
    SDL_RenderPresent(renderer);

    SDL_Event e;
    int quit = 0;
    while (!quit) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                quit = 1;
            }
        }
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
```

---

Ce programme C dessine les courbes de la fonction sinus en virgule fixe et de la fonction sinus standard en utilisant SDL. La courbe rouge représente la version standard, la courbe verte l'approximation en virgule fixe, et la courbe bleue montre l'erreur.