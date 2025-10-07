[](){#fast-sin}

# Sinus rapide

Dans des architectures sans support pour les nombres réels (comme les processeurs ne supportant pas les opérations en virgule flottante IEEE 754), il est courant d'utiliser des approximations polynomiales pour calculer des fonctions mathématiques comme le sinus. Calculer un sinus n'est pas une simple opération, comme l'addition ou la multiplication, et il n'existe pas d'algorithme trivial pour obtenir une valeur exacte.

Les processeurs modernes, lorsqu'ils calculent le sinus, utilisent souvent des **tables de valeurs prédéfinies** (appelées tables de sinus) stockées en mémoire. Ces tables contiennent des valeurs pré-calculées du sinus pour différents angles, généralement entre 0 et $\pi/2$. Lorsqu'un sinus doit être calculé, le processeur se base sur la valeur dans la table la plus proche de l'angle donné, puis utilise une interpolation souvent linéaire pour obtenir un résultat plus précis. Cette méthode permet d'économiser du temps de calcul au prix d'une petite perte de précision. Voici une manière de faire :

$$
\sin(\theta) \approx \sin(\theta_1) + \frac{\theta - \theta_1}{\theta_2 - \theta_1} \times (\sin(\theta_2) - \sin(\theta_1))
$$

où $\sin(\theta_1)$ et $\sin(\theta_2)$ sont les valeurs de sinus les plus proches de $\theta$ dans la table, $\theta$ est l'angle pour lequel le sinus doit être calculé. La recherche dans la table peut être simplement une table de hachage pour un accès en $O(1)$. La table serait pré-calculée et stockée sous forme d'un tableau.

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

L'objectif pédagogique est de montrer que les mathématiques peuvent être très utiles dans l'élaboration d'un algorithme. Nous allons voir comment approximer un sinus en utilisant un polynôme de degré 5 en utilisant les technologies suivantes:

- **Systèmes d'équations linéaires** pour résoudre les coefficients du polynôme;
- **Calcul intégral** pour minimiser l'erreur moyenne (moindre carrés);
- **Virgule fixe** pour représenter les nombres en mémoire.

Le domaine du sinus est infini mais il est possible de le réduire à l'intervalle ci-dessous car toutes les autres sorties peuvent être obtenues en utilisant les propriétés de symétrie du sinus. En effet il suffit du dessin du quart de sinus pour obtenir le sinus complet.

$$
x \in [0, \frac{\pi}{2}]
$$

D'autre part, le sinus est une fonction impaire, c'est-à-dire que $\sin(-x) = -\sin(x)$. Cette propriété induit, par exemple lors d'une décomposition en série de Fourier, que les coefficients de la série pour les termes pairs sont nuls. Cela signifie aussi que le sinus peut être approximé par un polynôme de degré impair. On peut donc tenter d'approximer un sinus par un polynôme de degré 5 en ayant seulement 3 coefficients à calculer. D'autre part, afin de faciliter les calculs et la représentation en virgule fixe on peut réduire l'intervalle de calcul à $[0, 1]$ en posant que :

$$
z = \frac{2x}{\pi}
$$

Le polynôme de degré 5 peut être exprimé de la manière suivante :

$$
\sin(z) \approx S_5(z) = cz - bz^**3** + az^5
$$

Pour trouver les coefficients de ce polynôme, on peut utiliser les propriétés du sinus et de ses dérivées. Nous allons donc raisonner sur ces deux fonctions :

$$
\begin{cases}
S_5(z) = az^5 - bz^3 + cz \\
S_5'(z) = 5az^4 - 3bz^2 + c
\end{cases}
$$

On peut noter quelques conditions aux bords de l'intervalle $[0, 1]$ :

- $S_5(1) = 1$ qui est équivalent à $\sin(\frac{\pi}{2}) = 1$;
- $S_5'(1) = 0$ car la pente est nulle en son sommet;
- $S_5'(0) = \frac{\pi}{2}$ car la pente est maximale en 0.

Ces conditions nous permettent d'obtenir trois équations linéaires qu'il est trivial de résoudre :

$$
\begin{cases}
1 = a - b + c \\
0 = 5a - 3b + 5c \\
\frac{\pi}{2} = a
\end{cases}
$$

Ce qui nous donne les coefficients suivants :

$$
a = \frac{\pi}{2},\quad
b = \pi-\frac{5}{2},\quad
c = \frac{\pi}{2}-\frac{3}{2}
$$

Que l'on peut simplifier en fonction de $a$ :

$$
a = \frac{\pi}{2},\quad
b = 2a-\frac{5}{2},\quad
c = a-\frac{3}{2}
$$

Cette solution triviale n'est généralement pas optimale car un critère fondamental n'a pas été respecté, celui de minimiser l'erreur moyenne avec le sacrifice potentiel de la précision des valeurs extrêmes. Une approche plus rigoureuse consiste donc minimiser l'erreur moyenne sur l'intervalle $[0, 1]$. On utilise pour ce faire la méthode des **moindre carrés** qui consiste à minimiser l'erreur quadratique est la somme des carrés des différences entre la fonction cible \( \sin\left(\frac{\pi}{2}x\right) \) et l'approximation polynomiale \( p(x) \). Pour ce faire, on calcule l'intégrale suivante :

\[
E(a, b, c) = \int_0^1 \left( \sin\left(\frac{\pi}{2}x\right) - (az^5 - bz^3 + cz) \right)^2 dx
\]

Pour minimiser l'erreur nous avons besoin de trouver les coefficients $a$, $b$ et $c$ qui minimisent cette intégrale. Cela revient à résoudre en prenant les dérivées partielles de l'erreur quadratique $E(a, b, c)$ par rapport à $a$, $b$ et $c$. Cela nous donne trois équations :

\[
\begin{cases}
    \frac{\partial E}{\partial a} = 0 \\
    \frac{\partial E}{\partial b} = 0 \\
    \frac{\partial E}{\partial c} = 0
\end{cases}
\]

Ces trois équations sont indépendantes, ce qui signifie qu'il est possible de résoudre ce système.

Pratiquement on aura plutôt recours à une résolution numérique par exemple avec Python :

```python
import numpy as np
from scipy.integrate import quad
from scipy.linalg import solve


def sin_pi_over_2(x):
    return np.sin(np.pi * x / 2)


def z_power_n(n, x):
    return x**n


integrals_matrix = np.zeros((3, 3))
for i, n1 in enumerate([5, 3, 1]):
    for j, n2 in enumerate([5, 3, 1]):
        integrals_matrix[i, j] = quad(lambda x: z_power_n(n1 + n2, x), 0, 1)[0]

integrals_rhs = np.zeros(3)
for i, n in enumerate([5, 3, 1]):
    integrals_rhs[i] = quad(lambda x: sin_pi_over_2(x) * z_power_n(n, x), 0, 1)[0]

a, b, c = solve(integrals_matrix, integrals_rhs)
print(a, b, c)
```

Ce qui nous donnes les coefficients suivants :

$$
a = 1.5704372550337553, \quad
b = 0.6427098943803898, \quad
c = 0.07243339903924052
$$

Une autre approche (j'ai toujours pas compris) est la suivante :

$$
a = 4(\frac{3}{\pi}-\frac{9}{16}), \quad
b = 2a-\frac{5}{2}, \quad
c = a-\frac{3}{2}
$$

Sur une architecture en virgule fixe comme un microcontrôleur MSP430 16-bit, on peut par exemple utiliser un entier de 16-bit pour représenter un angle. Ce dernier peut être exprimé en radians en complément à deux et en format Q15.1. Cela signifie que la partie entière représente les radians et la partie fractionnaire représente les décimales. Par exemple, 1.0 en Q15.1 est représenté par 0x8000. En termes binaire notre équation devra être multipliée par $2^{15}$ pour obtenir un résultat correct. On peut rendre générique cette définition en déclarant $o$ l'exponent de la puissance de 2 à appliquer. Notre équation complète est donc :

$$
fpsin_5(x) = \left. 2^o\left(az - bz^3 + cz^5\right)\right|_{z = \frac{2x}{\pi}}
$$

Or, l'équation doit pouvoir être réécrite seulement en termes de multiplications d'entiers, d'additions et de décalages. En outre, il est essentiel de factoriser au maximum l'équation pour éviter tout calcul redondant. On commence par factoriser l'équation:

$$
fpsin_5(x) = \left. z2^o\left(a - z^2\left(b + cz^2\right)\right)\right|_{z = \frac{2x}{\pi}}
$$

Comme $z\in[0, 1]$ n'est pas représentable par un entier, on peut réécrire $z$ comme $y/2^o$ avec $y\in[0, 2^o]$ et où $o$ est le nombre de bits de la partie fractionnaire du domaine d'entrée. On obtient alors :

$$
fpsin_5(x) = \left. \left[\frac{y}{2^n}\right]2^o\left(a - \left[\frac{y}{2^n}\right]^2\left(b + c\left[\frac{y}{2^n}\right]^2\right)\right)\right|_{z = \frac{2x}{\pi}}
$$

Après simplification on obtient :

$$
fpsin_5(x) = \left. y2^{o-n}\Big(a-y2^{-n}y2^{-n}\left(b-y2^{-2n}cy\right)\Big)\right|_{z = \frac{2x}{\pi}}
$$

Lors d'une multiplication en virgule fixe, on s'intéresse à la partie haute de la multiplication. En effet, pour un produit standard de deux entiers 8-bits, le résultat est un entier 16-bits. C'est d'ailleurs la raison pour laquelle les ALU offrent un registre de résultat deux fois plus grand que les registres d'entrée. Néanmoins, ce sont les 8-bits de poids faible qui sont conservés car si la multiplication n'a pas de dépassement, le résultat tiendra dans les 8-bits de poids faible. On supprime donc les 8-bit de pods fort. Or, dans un calcul en virgule fixe, la logique est différente. Un nombre en Q1.7 peut exprimer des grandeurs entre -1 et 1 avec une précision de 1/128. En multipliant deux nombre en Q1.7, on obtient un résultat en Q2.14. Or, dans ce résultat 16-bit, l'octet de poid faible ne contient que les chiffres après la virgule et none la partie intéressante du calcul.
On peut donc supprimer cet octet de poids faible et ne conserver que les 8-bits de poids fort formant un nombre en Q2.6. En C standard, il n'est pas possible d'ordonner au compilateur de choisir le mot de poids fort ou faible. En assembleur en revanche de nombreux processeurs offrent cette possibilités. Un ADSP-218x par exemple offre des instructions de multiplication en virgule fixe avec un mot de résultat de 32-bits. On peut alors choisir de conserver le mot de poids fort ou faible.

Une méthode pour maximiser la précision des calculs est d'ajouter des facteurs d'échelle. Par exemple, le coefficient $a$ vaut environ $1.57$ ce qui représente pour la partie entière 1 bit. Avec une ALU d'une profondeur $m$: 32-bits, on peut se permettre de décaler à gauche ce nombre tel que l'équation suivante est satisfaite :

$$
\text{sign}(a)\cdot\lceil |\log_2(a)| \rceil + k <= m
$$

où $k$ est le décalage en bits.

Si l'on ajoute un facteur d'échelle, il doit nécessairement être compensé dans l'équation. Commenconç



en virgule fixe on a intérêt à le multiplier

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



from sympy import symbols, Eq, solve, pi

a, b, c = symbols('a b c')

solution = solve([
    Eq(a - b + c, 1),
    Eq(a - 3*b + 5*c, 0),
    Eq(a/2 - b/4 + c/6, 2/pi)
], (a, b, c))

solution