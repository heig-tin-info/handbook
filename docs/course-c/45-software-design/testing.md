# Qualité et Testabilité

![Bogue de l'an 2000](/assets/images/y2k-bug.jpg)

Surveiller et assurer la qualité d'un code est primordial dans toute institution et quelques soit le produit. Dans l'industrie automobile par exemple, un bogue qui serait découvert plusieurs années après la commercialisation d'un modèle d'automobile aurait des conséquences catastrophiques.

Voici quelques exemples célèbres de ratés logiciels :

La sonde martienne Mariner

: En 1962, un bogue logiciel a causé l'échec de la mission avec la destruction de la fusée après qu'elle ait divergé de sa trajectoire. Une formule a mal été retranscrite depuis le papier en code exécutable. Des tests suffisants auraient évité cet échec.

Un pipeline soviétique de gaz

: En 1982, un bogue a été introduit dans un ordinateur canadien acheté pour le contrôle d'un pipeline de gaz transsibérien. L'erreur est reportée comme la plus large explosion jamais enregistrée d'origine non nucléaire.

Le générateur de nombre pseudo-aléatoire Kerberos

: Kerberos est un système de sécurité utilisé par Microsoft pour chiffrer les mots de passe des comptes Windows. Une erreur de code lors de la génération d'une [graine aléatoire](https://fr.wikipedia.org/wiki/Graine_al%C3%A9atoire) a permis de façon triviale pendant 8 ans de pénétrer n'importe quel ordinateur utilisant une authentification Kerberos.

La division entière sur Pentium

: En 1993, une erreur sur le silicium des processeurs Pentium, fleuron technologique de l'époque, menait à des erreurs de calcul en virgule flottante. Par exemple la division $4195835.0/3145727.0$ menait à $1.33374$ au lieu de $1.33382$

## SQuaRE

La norme ISO/IEC 25010 (qui remplace ISO/IEC 9126-1) décrit les caractéristiques définissant la qualité d'un logiciel. L'acronyme **SQuaRE** (*Software product Quality Requirements and Evaluation*) définit le standard international. Voici quelques critères d'un code de qualité :

- Maintenabilié
- Modifiabilité
- Testabilité
- Analisabilité
- Stabilité
- Changeabilité
- Réutilisabilité
- Compréhensibilité

## Hacking

### Buffer overflow

L'attaque par buffer overflow est un type d'attaque typique permettant de modifier le comportement d'un programme en exploitant "le jardinage mémoire". Lorsqu'un programme a mal été conçu et que les tests de dépassement n'ont pas été correctement implémentés, il est souvent possible d'accéder à des comportements de programmes imprévus.

Considérons le programme suivant :

```c
#include <stdio.h>
#include <string.h>

int check_password(char *str) {
    if(strcmp(str, "starwars"))
    {
        printf ("Wrong Password \n");
        return 0;
    }

    printf ("Correct Password \n");
    return 1;
}

int main(void)
{
    char buffer[15];
    int is_authorized = 0;

    printf("Password: ");
    gets(buffer);
    is_authorized = check_password(buffer);

    if(is_authorized)
    {
        printf ("Now, you have the root access! \n");
    }
}
```

À priori, c'est un programme tout à fait correct. Si l'utilisateur entre le bon mot de passe, il se voit octroyer des privilèges administrateurs. Testons ce programme :

```console
$ gcc u.c -fno-stack-protector
$ ./a.out
Password: starwars
Correct Password
Now, you have the root access!
```

Très bien, maintenant testons avec un mauvais mot de passe :

```console
$ ./a.out
Password: startrek
Wrong Password
```

Et maintenant, essayons avec un mot de passe magique...

## Tests unitaires

Un test unitaire est une procédure permettant de vérifier le bon fonctionnement d'une unité de code. Une unité de code est la plus petite partie d'un programme qui peut être testée de manière isolée. En C, une unité de code est souvent une fonction.

Lorsque l'on travaille selon la philosophie du TDD (*Test Driven Development*), on commence par écrire les tests unitaires avant d'écrire le code. Voici par exemple un test unitaire pour la résolution d'une équation du second degré :

```c
#include <stdio.h>

bool quadratic_solver(double a, double b, double c, double *x1, double *x2)
{
    double delta = b * b - 4 * a * c;

    if (delta < 0)
        return false;

    *x1 = (-b + sqrt(delta)) / (2 * a);
    *x2 = (-b - sqrt(delta)) / (2 * a);

    return true;
}

void test_quadratic_solver(void)
{
    double x1, x2;

    // Cas 1 : Deux racines réelles et distinctes
    assert(quadratic_solver(1, -3, 2, &x1, &x2) == true);
    assert(fabs(x1 - 2.0) < 1e-6);
    assert(fabs(x2 - 1.0) < 1e-6);

    // Cas 2 : Deux racines réelles et égales
    assert(quadratic_solver(1, -2, 1, &x1, &x2) == true);
    assert(fabs(x1 - 1.0) < 1e-6);
    assert(fabs(x2 - 1.0) < 1e-6);

    // Cas 3 : Racines complexes (pas de solution réelle)
    assert(quadratic_solver(1, 0, 1, &x1, &x2) == false);

    // Cas 4 : a = 0 (ce n'est pas une équation quadratique)
    assert(quadratic_solver(0, 2, 1, &x1, &x2) == false);

    // Cas 5 : Equation triviale (b = 0 et c = 0)
    assert(quadratic_solver(1, 0, 0, &x1, &x2) == true);
    assert(fabs(x1 - 0.0) < 1e-6);
    assert(fabs(x2 - 0.0) < 1e-6);
}
```

En pratique on aimerait lancer les tests unitaires automatiquement à chaque modification du code source. Pour cela, on utilisera des outils d'intégration continue comme Travis CI ou GitHub Actions.

Souvent on utilise des frameworks de tests unitaires pour automatiser les tests. En C, on peut citer [Unity](https://www.throwtheswitch.org/unity).

Reprenons l'exemple précédent avec Unity :

```c
#include "unity.h"
#include "quadratic_solver.h"

#include <stdio.h>

void setUp(void) {}

void tearDown(void) {}

void test_quadratic_solver(void)
{
    double x1, x2;

    // Cas 1 : Deux racines réelles et distinctes
    TEST_ASSERT_TRUE(quadratic_solver(1, -3, 2, &x1, &x2));
    TEST_ASSERT_FLOAT_WITHIN(1e-6, x1, 2.0);
    TEST_ASSERT_FLOAT_WITHIN(1e-6, x2, 1.0);

    // Cas 2 : Deux racines réelles et égales
    TEST_ASSERT_TRUE(quadratic_solver(1, -2, 1, &x1, &x2));
    TEST_ASSERT_FLOAT_WITHIN(1e-6, x1, 1.0);
    TEST_ASSERT_FLOAT_WITHIN(1e-6, x2, 1.0);

    // Cas 3 : Racines complexes (pas de solution réelle)
    TEST_ASSERT_FALSE(quadratic_solver(1, 0, 1, &x1, &x2));

    // Cas 4 : a = 0 (ce n'est pas une équation quadratique)
    TEST_ASSERT_FALSE(quadratic_solver(0, 2, 1, &x1, &x2));

    // Cas 5 : Equation triviale (b = 0 et c = 0)
    TEST_ASSERT_TRUE(quadratic_solver(1, 0, 0, &x1, &x2));
    TEST_ASSERT_FLOAT_WITHIN(1e-6, x1, 0.0);
    TEST_ASSERT_FLOAT_WITHIN(1e-6, x2, 0.0);
}
```

## Tests fonctionnels

Les tests fonctionnels permettent de vérifier le bon fonctionnement d'une application dans son ensemble. Ils sont souvent utilisés pour tester des applications web ou des applications mobiles. Les tests fonctionnels sont souvent automatisés et peuvent être lancés à chaque modification du code source.

Dans le cadre de ce cours on utilise le framework [Baygon](https://heig-tin-info.github.io/baygon/) pour réaliser des tests fonctionnels.

Pour l'utiliser il suffit de créer un fichier `tests.yml` à la racine de votre projet :

```yaml
version: 1
tests:
  - name: Arguments check
    tests:
      - name: No errors if two arguments
        args: [1, 2]
        exit: 0
      - name: Error if less than two arguments
        args: [1]
        exit: 1
  - name: Stdout is the sum of arguments
    args: [1, 2]
    stdout: []
  - name: Version on stderr
    args: ['--version']
    stderr:
      - regex: '\b\d\.\d\.\d\b'
      - contains: 'Version'
```

Il faut ensuite installer Baygon :

```bash
$ pip install baygon
```

Et lancer les tests :

```bash
$ baygon program
```
