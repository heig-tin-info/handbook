# Générateur congruentiel linéaire

Le générateur congruentiel linéaire (GCL ou LCG) est un algorithme simple pour générer des nombres pseudo-aléatoires. Il est défini par la relation de récurrence suivante :

$$
X_{n+1} = (a \cdot X_n + c) \mod m
$$

où :

$X_n$

: est la séquence de nombres pseudo-aléatoires

$a$

: est le multiplicateur

$c$

: est l'incrément

$m$

: est le modulo

Les informaticiens ont remarqué que ce générateur fonctionne bien pour certaines valeurs de $a$, $c$ et $m$. Par exemple, si $m = 2^k$, le générateur est dit à "congruence binaire". Si $c = 0$, le générateur est dit "multiplicatif".

En C c'est un générateur congruentiel linéaire qui est utilisé pour la fonction `rand()`. Voici une implémentation de ce générateur :

```c
#include <stdio.h>
#include <stdlib.h>

static uint32_t seed = 0;

void srand(uint32_t s) {
    seed = s;
}

uint32_t rand() {
    const uint32_t a = 1103515245;
    const uint32_t c = 12345;
    const uint32_t m = 1ULL << 31;
    seed = (a * seed + c) % m;
    return seed;
}
```

La valeur statique `seed` permet de conserver l'état du générateur entre les appels à la fonction `rand()`. Si elle n'est pas initialisée, le générateur retournera toujours la même séquence de nombres pseudo-aléatoires. La fonction `srand()` permet donc d'initialiser la graine du générateur.

En pratique, on utilise `srand()` avec comme valeur d'initialisation le temps courant en secondes pour obtenir une séquence de nombres pseudo-aléatoires différente à chaque exécution du programme :

```c
#include <time.h>

int main() {
    srand(time(NULL));
    for (int i = 0; i < 10; ++i) {
        printf("%d\n", rand());
    }
}
```

Néanmoins, si vous relancez votre programme durant la même seconde, vous obtiendrez la même séquence de nombres pseudo-aléatoires. Pour obtenir une séquence différente à chaque exécution, vous pouvez inclure le PID du processus :

```c
#include <unistd.h>
#include <time.h>

int main() {
    srand(time(NULL) ^ getpid());
    for (int i = 0; i < 10; ++i) {
        printf("%d\n", rand());
    }
}
```

## LCG et le standard C

Curieusement, la norme ISO/IEC 9899:2018 §7.22.2.1 ne stipule pas que `rand()` doit être implémenté selon un générateur congruentiel linéaire. Cependant, la plupart des implémentations de la fonction `rand()` continuent d'utiliser un LCG. Ainsi, la `libc` de GNU utilise bien ce mécanisme rudimentaire de génération de nombres pseudo-aléatoires alors qu'il existe depuis 2014 un appel système `getrandom()` qui permet de générer des nombres aléatoires de manière sécurisée.

```c
#include <sys/random.h>

ssize_t getrandom(void *buf, size_t buflen, unsigned int flags);
```

## Valeurs remarquables

Voici quelques valeurs de $a$, $c$ et $m$ qui donnent de bons résultats :

| Source               | $m$      | $a$                   | $c$                   |
| -------------------- | -------- | --------------------- | --------------------- |
| ANSI C               | $2^{31}$ | $1103515245$          | $12345$               |
| Borland C            | $2^{32}$ | $22695477$            | $1$                   |
| MMIX de Donald Knuth | $2^{64}$ | $6364136223846793005$ | $1442695040888963407$ |
| Java                 | $2^{48}$ | $25214903917$         | $11$                  |
