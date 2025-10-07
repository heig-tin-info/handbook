# Exponentiation rapide

Cet algorithme permet de calculer rapidement des puissances entières ($a^n$). La méthode naïve consiste à calculer les puissances avec une boucle :

```c
long long pow_naive(long long a, long long n) {
    long long res = 1;
    for (long long i = 0; i < n; ++i) {
        res *= a;
    }
    return res;
}
```

La complexité de cet algorithme est $O(n)$. Il est possible de faire mieux en $O(\log n)$.

```c
long long bin_pow(long long a, long long b) {
    if (b == 0) return 1;
    long long res = bin_pow(a, b / 2);
    return res * res * (b % 2 ? a : 1);
}
```

Comme évoqué plus haut, un algorithme récursif est souvent moins performant que sa variante itérative. Voici l'implémentation itérative :

```c
long long bin_pow(long long a, long long b) {
    long long res = 1;
    while (b > 0) {
        if (b & 1) res = res * a;
        a *= a;
        b /= 2;
    }
    return res;
}
```
