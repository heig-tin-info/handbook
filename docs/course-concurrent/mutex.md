# Exclusion Mutuelle

Les exclusions mutuelles sont un concept fondamental en programmation concurrente et parallèle. L'idée est de garantir que certaines parties du code ne sont pas exécutées simultanément par plusieurs threads, afin d'éviter des conditions de concurrence et des résultats imprévisibles.

Les *race conditions* ou en français *conditions de course* sont des situations où le résultat d'une opération dépend de l'ordre d'exécution des threads, ce qui peut conduire à des résultats incorrects ou incohérents. Les exclusions mutuelles permettent de protéger les **sections critiques** du code pour éviter ces problèmes.

En C++, les exclusions mutuelles sont souvent mises en œuvre à l'aide de verrous (locks) fournis par la bibliothèque standard. Ces verrous sont des objets qui peuvent être verrouillés (locked) par un thread pour empêcher d'autres threads d'accéder à une section critique, puis déverrouillés (unlocked) pour permettre à d'autres threads d'accéder à cette section.

En principe les vérrous sont utilisés pour :

- Protéger les données partagées entre plusieurs threads
- Protéger les ressources partagées entre plusieurs threads (fichiers, sockets, etc.)
- Synchroniser l'accès à des sections critiques du code
- Synchroniser la communication entre threads
- Synchroniser la terminaison de threads
- etc.

## Histoire

Le concept d'exclusion mutuelle a été introduit par Edsger Dijkstra en 1965. Il a inventé le terme "exclusion mutuelle" pour décrire une propriété souhaitable des systèmes informatiques, à savoir que deux processus ne peuvent pas être simultanément dans une section critique. Dijkstra a également inventé l'algorithme du "banquier" pour éviter les interblocages dans les systèmes informatiques.

Dans son article (Solution of a Problem in Concurrent Programming Control)[https://www.cs.utexas.edu/users/EWD/ewd01xx/EWD123.PDF], Dijkstra a introduit le concept de sémaphores, qui sont des variables entières utilisées pour la synchronisation entre processus ou threads. Les sémaphores peuvent être utilisés pour implémenter l'exclusion mutuelle, ainsi que d'autres formes de synchronisation.

Dekker a introduit un autre algorithme pour l'exclusion mutuelle entre deux processus en 1968. Cet algorithme est similaire à l'algorithme de Peterson, mais utilise des variables supplémentaires pour éviter les problèmes de synchronisation.

Peterson a introduit un algorithme pour l'exclusion mutuelle entre deux processus en 1981. Cet algorithme est souvent utilisé pour illustrer les concepts d'exclusion mutuelle et de synchronisation dans les cours d'informatique.

À cette époque les processeurs multi-cœurs n'existaient pas, et les systèmes informatiques étaient généralement des systèmes à un seul processeur. Les problèmes de synchronisation et d'exclusion mutuelle étaient donc moins complexes que dans les systèmes modernes. Un processeur moderne dispose de plusieurs cœurs, et chaque cœur peut exécuter plusieurs threads simultanément. La synchronisation et l'exclusion mutuelle sont donc des problèmes plus complexes dans les systèmes modernes.

## Exemple du compteur partagé

Considérons un exemple simple où deux threads partagent un compteur. Chaque thread incrémente le compteur 1000000 fois. Si les threads ne sont pas synchronisés, le résultat final dépendra de l'ordre d'exécution des threads.

En effet, si les deux threads tentent d'incrémenter le compteur simultanément, le résultat final sera imprévisible car l'exécution des instructions n'est pas **atomique**. Le processeur va devoir décomposer l'opération d'incrémentation en plusieurs étapes:

1. Charger la valeur actuelle du compteur depuis la mémoire dans un registre
2. Incrémenter la valeur dans le registre
3. Écrire la nouvelle valeur du registre dans la mémoire

Si un autre thread modifie la valeur du compteur entre ces étapes, le résultat final sera incorrect.

Pour éviter cela, nous devons synchroniser l'accès au compteur pour que les threads ne puissent pas l'incrémenter simultanément. La partie d'incrémentation est nommée **section critique**.

```cpp
// counter.cpp
#include <iostream>
#include <thread>
#include <vector>

size_t counter = 0;

class Worker {
public:
    Worker(size_t max_iterations = 1000000) : max_iterations(max_iterations) {}
    const size_t max_iterations;
    void operator() () {
        for (size_t i = 0; i < max_iterations; ++i)
        { // section critique
            ++counter;
        }
    }
};

int main() {
    const int num_threads = std::thread::hardware_concurrency();

    std::vector<std::jthread> threads;
    Worker worker;
    for (int i = 0; i < num_threads; ++i)
        threads.emplace_back(std::jthread(worker));

    for (auto& t : threads) t.join();

    std::cout << "Number of threads: " << num_threads << std::endl;
    std::cout << "Expected Counter: " << worker.max_iterations * num_threads << std::endl;
    std::cout << "Actual Counter: " << counter << std::endl;
}
```

## Verrous Mutex

En C++, les verrous sont généralement implémentés à l'aide de la classe `std::mutex` de la bibliothèque standard. Un verrou de type `std::mutex` peut être verrouillé à l'aide de la méthode `lock()` et déverrouillé à l'aide de la méthode `unlock()`.

## Exemple simple

```cpp
#include <iostream>
#include <thread>

static int x = 0;

int a() { for(;;) { x = 5; std::cout << x; } }
int b() { for(;;) x = 7; }

int main() {
    std::thread ta(a);
    std::thread tb(b);
    ta.join();
    tb.join();
}
```

```bash
$ g++ sync.cpp
$ timeout 10s ./a.out
$ grep -o 7 data | wc -l
$ wc -c < data
```

On peut voir qu'il y a environ 1 change sur 10000 d'avoir un 7.

## Autre Exemple

Dans cet exemple, nous avons deux threads `a` et `b` qui partagent une variable globale `x`. Le thread `a` affecte la valeur `5` à `x` et l'affiche, tandis que le thread `b` affecte la valeur `7` à `x`. Les threads s'exécutent indépendamment et peuvent modifier `x` simultanément, ce qui peut entraîner des résultats imprévisibles.

```cpp
#include <iostream>
#include <thread>

static int x = 0;

int a() { for(;;) { x = 5; std::cout << x; } }
int b() { for(;;) x = 7; }

int main() {
    std::thread ta(a);
    std::thread tb(b);
    ta.join();
    tb.join();
}
```

> Exercice: Testez quelle est la probablilité d'avoir un 7 dans la sortie.

Pour cela faite tourner le programme en redirigeant la sortie standard vers un fichier, puis comptez le nombre de 7 dans le fichier. Exécutez le programme pendant 5 secondes avec la commande `timeout`.

Attention, le fichier peut être très volumineux, la commande grep pour chercher les 7 peut être utilisée comme suit:

```bash
$ timeout 5s ./a.out > data
$ grep -o 5 data | wc -l
$ grep -o 7 data | wc -l
```