# Racine carrée inverse rapide

![Quake III Arena](/assets/images/quake-iii-arena.jpg)

Cet algorithme a été développé chez Silicon Graphics au début des années 90. Il a été utilisé dans des jeux vidéos comme [Quake III Arena](https://fr.wikipedia.org/wiki/Quake_III_Arena) pour améliorer la performance du calcul des angles d'incidence dans la réflexion des lumières et est attribué à John Carmack, un des fondateurs de [id Software](https://fr.wikipedia.org/wiki/Id_Software), qui a publié le code source de Quake III Arena en 2005.

Il est utilisé pour les vecteurs normaux dans les calculs de réflexion de la lumière.

![Réflexion de la lumière](/assets/images/vector-field.svg)

```c
float Q_rsqrt(float number)
{
    const float threehalfs = 1.5F;

    float x2 = number * 0.5F;
    float y = number;
    long i = *(long *) &y; // Evil floating point bit level hacking
    i = 0x5f3759df - (i >> 1); // What the fuck?
    y = *(float *) &i;
    y = y * (threehalfs - (x2 * y * y)); // 1st iteration
#if BETTER
    y = y * (threehalfs - (x2 * y * y)); // 2nd iteration
#endif
    return y;
}
```

Cet algorithme de [racine carrée inverse rapide](https://fr.wikipedia.org/wiki/Racine_carr%C3%A9e_inverse_rapide) utilise une constante magique `0x5f3759df`. L'implémentation proposée ci-dessus est extraite du code source du jeu Quake III arena ([q_math.c](https://github.com/id-Software/Quake-III-Arena/blob/dbe4ddb10315479fc00086f08e25d968b4b43c49/code/game/q_math.c#L552)) disponible sur GitHub.

Ce n'est pas un algorithme très académique, il s'agit d'un [kludge](https://fr.wikipedia.org/wiki/Kludge), une solution irrespectueuse des règles de l'art de la programmation, car la valeur `y` est transtypée en un `long` (`i = *(long *)&y`. C'est cette astuce qui permet de tirer avantage que les valeurs en virgule flottantes sont exprimées en puissances de 2.
