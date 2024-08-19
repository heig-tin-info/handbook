# Unions

Une [union](https://en.wikipedia.org/wiki/Union_type) est une variable qui peut avoir plusieurs représentations d'un même contenu mémoire. Rappelez-vous, nous nous demandions quelle était l'interprétation d'un contenu mémoire donné. Il est possible en C d'avoir toutes les interprétations à la fois :

```c
#include <stdint.h>
#include <stdio.h>

union Mixed
{
    int32_t signed32;
    uint32_t unsigned32;
    int8_t signed8[4];
    int16_t signed16[2];
    float float32;
};

int main(void) {
    union Mixed m = {
        .signed8 = {0b11011011, 0b0100100, 0b01001001, 0b01000000}
    };

    printf(
        "int32_t\t%d\n"
        "uint32_t\t%u\n"
        "char\t%c, %c, %c, %c\n"
        "short\t%hu, %hu\n"
        "float\t%f\n",
        m.signed32,
        m.unsigned32,
        m.signed8[0], m.signed8[1], m.signed8[2], m.signed8[3],
        m.signed16[0], m.signed16[1],
        m.float32
    );
}
```

Les unions sont très utilisées en combinaison avec des champs de bits. Pour reprendre l'exemple du champ de bit évoqué plus haut, on peut souhaiter accéder au registre soit sous la forme d'un entier 16-bits soit via chacun de ses bits indépendamment.

```c
union i2cmdr {
    struct {
        int  bc  :3;
        bool fdf :1;
        bool stb :1;
        bool irs :1;
        bool dlb :1;
        bool rm  :1;
        bool xa  :1;
        bool trx :1;
        bool mst :1;
        bool stp :1;
        bool _reserved :1;
        bool stt  :1;
        bool free :1;
        bool nackmod :1;
    } bits;
    uint16_t all;
};
```