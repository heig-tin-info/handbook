# Qualité et Testabilité

![Bug de l'an 2000](../assets/figures/y2k-bug.webp)

Surveiller et assurer la qualité d'un code est primordial dans toute institution et quelques soit le produit. Dans l'industrie automobile par exemple, un bogue qui serait découvert plusieurs années après la commercialisation d'un modèle d'automobile aurait des conséquences catastrophiques.

Voici quelques exemples célèbres de ratés logiciels :

La sonde martienne Mariner

: En 1962, un bogue logiciel a causé l'échec de la mission avec la destruction de la fusée après qu'elle ait divergé de sa trajectoire. Une formule a mal été retranscrite depuis le papier en code exécutable. Des tests suffisants auraient évité cet échec.

Un pipeline soviétique de gaz

: En 1982, un bug a été introduit dans un ordinateur canadien acheté pour le contrôle d'un pipeline de gaz transsibérien. L'erreur est reportée comme la plus large explosion jamais enregistrée d'origine non nucléaire.

Le générateur de nombre pseudo-aléatoire Kerberos

: Kerberos est un système de sécurité utilisé par Microsoft pour chiffrer les mots de passe des comptes Windows. Une erreur de code lors de la génération d'une [graine aléatoire](https://fr.wikipedia.org/wiki/Graine_al%C3%A9atoire) a permis de façon triviale pendant 8 ans de pénétrer n'importe quel ordinateur utilisant une authentification Kerberos.

La division entière sur Pentium

: En 1993, une erreur sur le silicium des processeurs Pentium, fleuron technologique de l'époque, menait à des erreurs de calcul en virgule flottante. Par exemple la division $4195835.0/3145727.0$ menait à $1.33374$ au lieu de $1.33382$

## SQuaRE

La norme ISO/IEC 25010 (qui remplace ISO/IEC 9126-1) décrit les caractéristiques définissant la qualité d'un logiciel. L'acronyme **SQuaRE** (*Software product Quality Requirements and Evaluation*) défini le standard international. Voici quelques critères d'un code de qualité :

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

## Tests fonctionnels

## Framework de tests

Unity
