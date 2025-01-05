# Élision de copie

Une des optimisations les plus importantes en C++ est l'**Élision de copie** (*copy elision*).

## RVO

En C++ un concept essentiel est le **Return Value Optimization** (RVO). Il s'agit d'une optimisation du compilateur qui permet d'éviter des copies inutiles lors du retour d'une valeur.

Prenons l'exemple du programme suivant. En C, la fonction `createHeavy` devra copier la structure `Heavy` sur la pile lors du retour de la fonction. En C++, le compilateur peut optimiser cette copie en partant du principe qu'il peut retarder la construction de l'objet `h` jusqu'à son utilisation.

```cpp
struct Heavy {
    int data[1000];
};

#ifndef __cplusplus
typedef struct Heavy Heavy;
#endif

Heavy createHeavy() {
    Heavy h;
    // Initialisation de h
    return h;
}

int main() {
    Heavy h = createHeavy();
}
```

Le RVO introdui en C++
