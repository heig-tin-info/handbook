# Intervalles et Vues

Les intervalles et les vues sont des concepts importants en programmation fonctionnelle. Ils permettent de manipuler des collections de données de manière plus expressive et plus efficace.

Le standard C++ 2020 s'est vu étendu avec la bibliothèque `ranges` qui propose des types et des fonctions pour manipuler des intervalles et des vues.

## Vues

Une vue est un objet qui encapsule un intervalle. Elle permet de le manipuler de manière paresseuse, c’est-à-dire que les opérations ne sont effectuées que lorsque cela devient nécessaire.

Traditionnellement un objet itérable en C++ est un objet qui implémente les méthodes `begin()` et `end()`. La méthode `begin()` retourne un itérateur sur le premier élément de la collection et la méthode `end()` retourne un itérateur sur l'élément après le dernier élément de la collection (*passed-the-end*). L'itérateur dispose d'une méthode `operator++` pour avancer à l'élément suivant et d'une méthode `operator*` pour accéder à la valeur de l'élément courant.

Les vues introduisent un nouveau concept d’itérateur : l’itérateur de vue, défini par l’interface `std::ranges::view`, qui propose des méthodes pour manipuler l’intervalle de manière paresseuse.

Il existe plusieurs types de vues dans la bibliothèque `ranges` :

Transformations (`std::ranges::transform_view`)

: Elles permettent de modifier les éléments de l’intervalle en appliquant une fonction de transformation (foncteur) à chaque élément (p. ex. doubler chaque valeur).

Filtrage (`std::ranges::filter_view`)

: Elles filtrent les éléments de l’intervalle en appliquant un prédicat à chacun. Cela réduit généralement la taille de l’intervalle en ne sélectionnant que les éléments qui satisfont la condition (p. ex. conserver uniquement les nombres pairs).

## Algorithmes

La bibliothèque `ranges` est étroitement liée à la bibliothèque `algorithm` qui propose des fonctions pour manipuler des collections de données. Les algorithmes de la bibliothèque `algorithm` ont été étendus pour accepter des vues en plus des intervalles. La fonction `find_if` par exemple peut être utilisée avec une vue pour trouver le premier élément qui satisfait un prédicat.

```cpp
#include <iostream>
#include <vector>
#include <ranges>
#include <algorithm>

using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    auto view = v | views::filter([](int i) { return i % 2 == 0; });

    auto it = find_if(view.begin(), view.end(), [](int i) { return i > 5; });
    if (it != view.end()) {
        cout << *it << endl;
    }

    return 0;
}
```

## Paresse

Les vues sont conçues pour différer l'exécution de toute transformation ou filtrage jusqu'à ce qu'un élément soit effectivement demandé. Cela signifie que chaque opération `operator++` ou `operator*` dans les itérateurs des vues déclenche seulement alors l'application de la transformation ou du filtrage, rendant la vue très efficace en termes de mémoire et de performance.
