[](){#fast-sin}

# Sinus rapide

Dans des architectures sans support pour les nombres réels (virgule flottante), il est courant d'utiliser des approximations polynomiales pour calculer des fonctions mathématiques comme le sinus. Le code fourni implémente une approximation de la fonction sinus en utilisant un polynôme de cinquième ordre en arithmétique en virgule fixe.

Le code suivant est une fonction C qui calcule une approximation du sinus pour un angle donné, représenté en virgule fixe :

```c
/**
 * A 5-order polynomial approximation to sin(x).
 * @param i   angle (with 2^15 units/circle)
 * @return    16 bit fixed point Sine value (4.12) (ie: +4096 = +1 & -4096 = -1)
 *
 * The result is accurate to within +- 1 count. ie: +/-2.44e-4.
 */
int16_t fpsin(int16_t i) {
    // Convert (signed) input to a value between 0 and 8192.
    // (8192 is pi/2, which is the region of the curve fit).
    i <<= 1;
    uint8_t c = i < 0;

    if(i == (i | 0x4000 )) // flip input value to corresponding
       i = (1<<15) - i;    // value in range [0..8192)

    i = (i & 0x7FFF) >> 1;

    /**
     * The following section implements the formula:
     *  y = i * 2^-n * ( A1 - 2^(q-p) * i * 2^-n * i * 2^-n *
     *      [B1 - 2^-r * i * 2^-n * C1 * i] ) * 2^(a-q)
     * Where the constants are defined as follows:
     */
    enum {A1=3370945099UL, B1=2746362156UL, C1=292421UL};
    enum {n=13, p=32, q=31, r=3, a=12};

    uint32_t y = (C1*((uint32_t)i))>>n;
    y = B1 - (((uint32_t)i*y)>>r);
    y = (uint32_t)i * (y>>n);
    y = (uint32_t)i * (y>>n);
    y = A1 - (y>>(p-q));
    y = (uint32_t)i * (y>>n);
    y = (y+(1UL<<(q-a-1)))>>(q-a); // Rounding

    return c ? -y : y;
}
```

Source : [5th Order Polynomial Fixed-Point Sine Approximation](https://www.nullhardware.com/blog/fixed-point-sine-and-cosine-for-embedded-systems/)