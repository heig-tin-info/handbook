# Élision de copie

L’**élision de copie** (*copy elision*) fait partie des optimisations les plus bénéfiques en C++. Elle permet d’éviter la création de copies temporaires coûteuses en laissant le compilateur construire l’objet directement à son emplacement définitif.

## RVO

Le **Return Value Optimization** (RVO) illustre ce principe. Lorsqu’une fonction retourne un objet par valeur, le compilateur est autorisé à construire cet objet directement dans la zone mémoire du résultat, sans passer par un intermédiaire.

Considérons le programme suivant. En C, la fonction `createHeavy` copie la structure `Heavy` sur la pile au moment du retour. En C++, le compilateur peut retarder la construction jusqu’au point d’utilisation et supprimer cette copie inutile.

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

Dans cet exemple, le compilateur construit directement `h` dans la zone mémoire de `main`, comme si l’objet n’avait jamais existé dans `createHeavy`. L’optimisation réduit les copies coûteuses et rend le code plus efficace sans intervention du développeur.
