# Sémaphores

Le sémaphore a été introduit par Edsger Dijkstra en 1965. Il s'agit d'une variable entière non négative utilisée pour synchroniser l'accès à une ressource partagée. Ce mécanisme de synchronisation permet de contrôler l'accès concurrent à une ressource afin d'éviter les conflits.

Historiquement, puisque Dijkstra était néerlandais, il a choisi comme noms de signaux :

- `P` pour « Proberen » (essayer en néerlandais) ;
- `V` pour « Verhogen » (augmenter en néerlandais).

Le sémaphore est longtemps resté la brique de base pour la synchronisation des threads. Il demeure utilisé dans les systèmes d'exploitation modernes pour implémenter des mécanismes tels que les mutex, les moniteurs, les barrières, etc.

Néanmoins, on peut émuler un sémaphore à l'aide d'un mutex et d'une variable de condition. C'est d'ailleurs l'approche retenue par la classe `std::counting_semaphore` de la bibliothèque standard C++20. Voici un exemple d'implémentation :

```cpp
#include <mutex>
#include <condition_variable>

class Semaphore {
    std::mutex mtx;
    std::condition_variable cv;
    int count;

public:
    Semaphore(int count = 0) : count(count) {}

    // Verhogen
    void notify() {
        std::unique_lock<std::mutex> lock(mtx);
        ++count;
        cv.notify_one();
    }

    // Proberen
    void wait() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this] { return count > 0; });
        --count;
    }
};
```

Dans cet exemple, la méthode `notify` incrémente le compteur du sémaphore et réveille un thread en attente. La méthode `wait` patiente jusqu'à ce que le compteur soit strictement positif, puis le décrémente.

Il est parfois utile, pour compter des ressources, de fournir aux méthodes `notify` et `wait` un argument `n` afin d'incrémenter ou décrémenter le compteur de `n` unités. Cela permet de libérer ou d'acquérir plusieurs ressources en une seule opération. Par exemple, si `n` vaut 3, trois ressources sont libérées ou acquises simultanément.

```cpp
#include <mutex>
#include <condition_variable>

class Semaphore {
    std::mutex mtx;
    std::condition_variable cv;
    int count;

public:
    Semaphore(int count = 0) : count(count) {}

    void notify(int n = 1) {
        std::unique_lock<std::mutex> lock(mtx);
        count += n;
        cv.notify_all();
    }

    void wait(int n = 1) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this, n] { return count >= n; });
        count -= n;
    }
};
```

## Problème du producteur et du consommateur

Le problème du producteur et du consommateur est un classique de la synchronisation de threads. Il s'agit d'orchestrer un ou plusieurs threads producteurs qui génèrent des données et un ou plusieurs threads consommateurs qui les traitent.

Une solution simple s'appuie sur deux sémaphores :

- un sémaphore `empty` qui compte le nombre d'emplacements vides dans le tampon ;
- un sémaphore `full` qui comptabilise les emplacements déjà remplis.

En combinant ces deux compteurs avec un mutex pour protéger la structure de données partagée, on garantit que les producteurs n'écrivent que dans des cases libres et que les consommateurs ne lisent que des éléments valides.
