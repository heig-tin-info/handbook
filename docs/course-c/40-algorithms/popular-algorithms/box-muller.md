# Transformation de Box-Muller

La fonction `rand()` de la bibliothèque standard, et plus généralement les [générateurs congruentiels](#lcg) qui se cachent derrière, produisent des nombres **uniformément** répartis : chaque valeur de l'intervalle a la même probabilité de sortir. C'est parfait pour tirer une carte ou mélanger un tableau, mais la nature, elle, n'est pas uniforme. Le bruit d'un capteur, l'erreur d'une mesure, la taille des individus d'une population ou la dispersion des pièces usinées suivent une [loi normale](https://fr.wikipedia.org/wiki/Loi_normale), la fameuse courbe en cloche de Gauss. #[loi normale]

Dès que l'on veut simuler un phénomène physique, ajouter un bruit réaliste à un signal de test, initialiser les poids d'un réseau de neurones ou mener une simulation de [Monte-Carlo](https://fr.wikipedia.org/wiki/M%C3%A9thode_de_Monte-Carlo), on a donc besoin de nombres aléatoires **gaussiens**. La transformation de Box-Muller #[Box-Muller], publiée en 1958 par [George Box](https://fr.wikipedia.org/wiki/George_Box) et Mervin Muller, est la méthode classique pour les fabriquer à partir de deux nombres uniformes. Elle tient en trois lignes, mais ces trois lignes cachent une idée géométrique élégante.

## Le problème

La recette habituelle pour obtenir une loi quelconque à partir d'une loi uniforme s'appelle la **méthode de l'inverse** : si $U$ est uniforme sur $[0, 1]$ et $F$ la fonction de répartition de la loi visée, alors $F^{-1}(U)$ suit cette loi. Pour la loi exponentielle, par exemple, $F(x) = 1 - e^{-\lambda x}$ s'inverse sans difficulté et $-\ln(U) / \lambda$ fait l'affaire.

Pour la loi normale, cette recette tombe à l'eau. Sa fonction de répartition fait intervenir la [fonction d'erreur](https://fr.wikipedia.org/wiki/Fonction_d%27erreur) $\operatorname{erf}$, qui n'a pas d'expression analytique, et encore moins d'inverse. Il faudrait recourir à des approximations numériques coûteuses.

Une autre approche naïve s'appuie sur le théorème central limite : la somme de douze nombres uniformes, moins six, ressemble à une normale centrée réduite. C'est simple mais grossier, la distribution obtenue ne dépasse jamais $\pm 6$ et les queues de la cloche sont mal reproduites, sans compter qu'il faut douze tirages pour une seule valeur.

## L'idée

L'astuce de Box et Muller consiste à ne pas chercher une normale, mais **deux à la fois**. Prenons deux variables normales indépendantes $Z_0$ et $Z_1$ et regardons le point $(Z_0, Z_1)$ dans le plan. Sa densité de probabilité est le produit des deux densités :

$$
f(z_0, z_1) = \frac{1}{2\pi} e^{-z_0^2/2} \, e^{-z_1^2/2} = \frac{1}{2\pi} e^{-(z_0^2 + z_1^2)/2} = \frac{1}{2\pi} e^{-r^2/2}
$$

Elle ne dépend que de la distance $r$ à l'origine, pas de la direction : le nuage de points est **isotrope**, il a la même allure dans toutes les directions. C'est exactement ce que montre la figure ci-dessous, où les histogrammes marginaux sur chaque axe sont tous deux des courbes en cloche.

![Nuage de points gaussien et ses projections](/assets/images/box-muller-cloud.svg){ width=70% }

Or un nuage isotrope se décrit bien mieux en coordonnées polaires qu'en coordonnées cartésiennes :

- L'angle $\theta$ est **uniforme** sur $[0, 2\pi[$, puisqu'aucune direction n'est privilégiée.
- Le rayon $r$ suit une loi dont on peut calculer la fonction de répartition en intégrant la densité sur un disque. On trouve $P(R > r) = e^{-r^2/2}$, autrement dit $R^2$ suit une loi exponentielle de moyenne 2.

Et la loi exponentielle, on sait l'inverser ! Si $U_1$ est uniforme, alors $-2 \ln(U_1)$ est exponentielle de moyenne 2, et par conséquent :

$$
r = \sqrt{-2 \ln U_1} \qquad \theta = 2\pi U_2
$$

Il ne reste plus qu'à revenir en coordonnées cartésiennes pour récupérer les deux normales :

$$
z_0 = r \cos\theta = \sqrt{-2 \ln U_1} \, \cos(2\pi U_2)
\qquad
z_1 = r \sin\theta = \sqrt{-2 \ln U_1} \, \sin(2\pi U_2)
$$

La figure suivante résume les trois étapes. À gauche, les couples $(U_1, U_2)$ remplissent uniformément le carré unité. Au centre, chaque couple est devenu un point $(r, \theta)$ du plan polaire : les petites valeurs de $U_1$, en rouge, sont projetées loin du centre car le logarithme y explose, tandis que les grandes valeurs de $U_1$, en bleu, se regroupent près de l'origine. À droite, la projection de ces points sur l'axe horizontal donne la cloche attendue.

![Les trois étapes de la transformation de Box-Muller](/assets/images/box-muller-steps.svg)

Chaque couple d'uniformes produit ainsi **deux** valeurs normales indépendantes, $z_0$ et $z_1$. Une implémentation soigneuse ne jette pas la seconde : elle la garde en réserve pour l'appel suivant.

## Implémentation en C

Deux précautions s'imposent. D'abord, `rand()` peut retourner zéro, et $\ln(0)$ n'est pas défini : on décale donc le tirage pour obtenir une uniforme sur $]0, 1]$. Ensuite, la seconde valeur est conservée dans une variable statique, ce qui divise par deux le nombre d'appels à `log()`, `sqrt()`, `cos()` et `sin()`.

```c
#include <math.h>
#include <stdlib.h>

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
```

La fonction produit une loi normale **centrée réduite**, de moyenne $0$ et d'écart-type $1$, que l'on note $\mathcal{N}(0, 1)$. Pour obtenir n'importe quelle autre loi normale $\mathcal{N}(\mu, \sigma^2)$, il suffit d'une multiplication et d'une addition :

```c
// Loi normale de moyenne mu et d'écart-type sigma.
double randn_scaled(double mu, double sigma) {
    return mu + sigma * randn();
}
```

Voici par exemple comment simuler un capteur de température qui mesure $20\,°C$ avec un bruit d'écart-type $0.5\,°C$ :

```c
for (int i = 0; i < 10; ++i)
    printf("%.2f\n", randn_scaled(20.0, 0.5));
```

Le programme complet, disponible dans les sources du cours, tire cent mille valeurs et affiche leur histogramme. La moyenne et l'écart-type mesurés collent à la théorie :

```text
moyenne = 0.0001, écart-type = 1.0013
 -3.0 |
 -2.6 | ##
 -2.2 | #####
 -1.8 | ###########
 -1.4 | ###################
 -1.0 | ############################
 -0.6 | ####################################
 -0.2 | #######################################
  0.2 | ####################################
  0.6 | #############################
  1.0 | ###################
  1.4 | ###########
  1.8 | #####
  2.2 | ##
  2.6 |
```

## Variante polaire de Marsaglia

Le cosinus et le sinus sont les opérations les plus chères de la méthode. En 1964, [George Marsaglia](https://fr.wikipedia.org/wiki/George_Marsaglia) a proposé une variante qui s'en passe. Au lieu de tirer un angle, on tire un point $(V_1, V_2)$ uniformément dans le carré $[-1, 1]^2$ et l'on ne le garde que s'il tombe dans le disque unité, c'est-à-dire si $s = V_1^2 + V_2^2 < 1$. Les points conservés sont uniformément répartis dans le disque, donc leur angle est uniforme, et le cosinus et le sinus de cet angle s'obtiennent gratuitement par $V_1 / \sqrt{s}$ et $V_2 / \sqrt{s}$. #[méthode polaire]

![Méthode polaire : rejet des points hors du disque unité](/assets/images/box-muller-polar.svg){ width=50% }

Mieux encore, $s$ est lui-même uniforme sur $]0, 1[$ et peut jouer le rôle de $U_1$. Les formules deviennent :

$$
z_0 = V_1 \sqrt{\frac{-2 \ln s}{s}} \qquad z_1 = V_2 \sqrt{\frac{-2 \ln s}{s}}
$$

Le prix à payer est le rejet : l'aire du disque vaut $\pi / 4 \approx 79\,\%$ de celle du carré, donc un tirage sur cinq environ est perdu et la boucle recommence. En contrepartie, chaque passe ne coûte plus qu'un logarithme et une racine carrée.

```c
double randn_polar(void) {
    static int has_spare = 0;
    static double spare;

    if (has_spare) {
        has_spare = 0;
        return spare;
    }

    double v1, v2, s;
    do {
        v1 = 2.0 * rand() / (double)RAND_MAX - 1.0;
        v2 = 2.0 * rand() / (double)RAND_MAX - 1.0;
        s = v1 * v1 + v2 * v2;
    } while (s >= 1.0 || s == 0.0);

    double factor = sqrt(-2.0 * log(s) / s);
    spare = v2 * factor;
    has_spare = 1;
    return v1 * factor;
}
```

!!! warning "Les pièges"

    1. **Le logarithme de zéro.** Si l'uniforme peut valoir exactement $0$, `log()` retourne moins l'infini et la valeur produite est infinie. Les deux implémentations ci-dessus l'évitent, l'une en décalant le tirage, l'autre en rejetant $s = 0$.
    2. **La qualité du générateur uniforme.** Box-Muller ne fait que transformer : si `rand()` est un mauvais générateur congruentiel, les défauts se retrouvent dans la gaussienne. Avec un `RAND_MAX` de $32767$, la plus petite uniforme vaut $3 \times 10^{-5}$ et le rayon ne dépassera jamais $\sqrt{-2 \ln(3 \times 10^{-5})} \approx 4.6$ : les queues de la distribution sont tronquées.
    3. **Le coût sur un microcontrôleur.** Logarithme, racine carrée et fonctions trigonométriques en virgule flottante sont hors de prix sur un petit processeur. On préférera alors la méthode polaire, une table de valeurs précalculées, ou pour un bruit sans prétention la somme de quelques uniformes évoquée plus haut.
    4. **La variable statique.** La valeur en réserve rend la fonction non réentrante : deux fils d'exécution qui l'appellent simultanément peuvent se la partager par erreur. Dans un contexte concurrent, on retournera les deux valeurs à l'appelant au lieu de les mémoriser.

::: exercise {title="#(ex:box-muller-regle) : La règle des 68-95-99.7"}
Une loi normale a la propriété bien connue qu'environ $68\,\%$ des valeurs tombent à moins d'un écart-type de la moyenne, $95\,\%$ à moins de deux écarts-types et $99.7\,\%$ à moins de trois.

Écrivez un programme qui tire un million de valeurs avec `randn()` et compte la proportion de valeurs dans chacun des trois intervalles $[-1, 1]$, $[-2, 2]$ et $[-3, 3]$. Comparez avec la théorie. Que se passe-t-il si vous remplacez `randn()` par la somme de douze uniformes moins six ?

??? solution

    ```c
    #include <math.h>
    #include <stdio.h>
    #include <stdlib.h>

    double randn(void); // Box-Muller, voir ci-dessus

    int main(void) {
        const int n = 1000000;
        int within[3] = {0, 0, 0};
        for (int i = 0; i < n; ++i) {
            double z = fabs(randn());
            for (int k = 0; k < 3; ++k)
                if (z < k + 1) within[k]++;
        }
        for (int k = 0; k < 3; ++k)
            printf("|z| < %d : %.2f %%\n", k + 1, 100.0 * within[k] / n);
    }
    ```

    On obtient des proportions très proches de $68.27\,\%$, $95.45\,\%$ et $99.73\,\%$. Avec la somme de douze uniformes, les deux premières proportions restent correctes à quelques dixièmes près, mais la troisième est un peu trop élevée : la distribution est bornée à $\pm 6$ et ses queues sont plus minces que celles d'une vraie gaussienne. C'est précisément dans les queues, les événements rares, que l'approximation du théorème central limite montre ses limites.
:::
