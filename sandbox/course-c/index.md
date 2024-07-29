# Bases

```c
0 1 2 3 4 5 6 7 8 9
```

Une base désigne la valeur dont les puissances successives interviennent dans l'écriture des nombres dans la numération positionnelle, laquelle est un procédé par lequel l'écriture des nombres est composée de chiffres ou symboles reliés à leur position voisine par un multiplicateur, appelé base du système de numération.

Sans cette connaissance à priori du système de numération utilisé, il vous est impossible d'interpréter ces nombres :

```
69128
11027
j4b12
>>!!0
九千十八
九千 零十八
```

```c
0 1 2 3 4 5 6 7 8 9
```

Outre la position des symboles (l'ordre dans lequel ils apparaissent de gauche à droite) la base du système de numération utilisé est essentielle pour décoder ces nombres. Cette base définit combien de symboles différents possibles peuvent être utilisés pour coder une position.

!!! exercise "Symboles binaires"

    Dans la notation binaire, composés de 1 et de 0, combien de symboles existent et combien de positions y-a-t-il dans le nombre `11001` ?

    ??? solution

        Le nombre `11001` est composé de 5 positions et de deux symboles possibles par position : `1` et `0`. La quantité d'information est donc e 5 bits.

```c
0 1 2 3 4 5 6 7 8 9
```

## Système décimal

Le système décimal est le système de numération utilisant la base **dix** et le plus utilisé par les humains au vingt et unième siècle, ce qui n'a pas toujours été le cas. Par exemple, les anciennes civilisations de Mésopotamie (Sumer ou Babylone) utilisaient un système positionnel de base sexagésimale (60), la civilisation maya utilisait un système de base 20 de même que certaines langues celtiques dont il reste aujourd'hui quelques traces en français avec la dénomination *quatre-vingts*.

L'exemple suivant montre l'écriture de 1506 en écriture hiéroglyphique `(1000+100+100+100+100+100+1+1+1+1+1+1)`. Il s'agit d'une numération additive.


Notre système de représentation des nombres décimaux est le système de numération indo-arabe qui emploie une notation positionnelle et dix chiffres (ou symboles) allant de zéro à neuf :

```c
0 1 2 3 4 5 6 7 8 9
```