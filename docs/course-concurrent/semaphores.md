# Semaphore

Le semaphore a été introduit par Edsger Dijkstra en 1965. Il s'agit d'une variable entière non négative qui peut être utilisée pour synchroniser l'accès à une ressource partagée. Un sémaphore est un objet de synchronisation qui permet à plusieurs threads d'accéder à une ressource partagée en même temps.

Historiquement, puisque Dijkstra était Néerlandais, il a choisi comme noms de signaux :

- `P` pour "Proberen" (essayer en néerlandais)
- `V` pour "Verhogen" (augmenter en néerlandais)

Un sémaphore était vu comme la brique de base pour la synchronisation de threads. Il est toujours utilisé dans les systèmes d'exploitation modernes pour implémenter des mécanismes de synchronisation tels que les mutex, les moniteurs, les barrières, etc.

Néanmoins, on peut émuler un sémaphore avec un mutex et une variable condition. C'est ce que fait la classe `std::counting_semaphore` de la bibliothèque standard C++20. Voici comment on peut émuler un sémaphore avec un mutex et une variable condition :

```cpp
#include <mutex>
#include <condition_variable>

class Semaphore {
    std::mutex mtx;
    std::condition_variable cv;
    int count;

public:
    Semaphore(int count = 0) : count(count) {}

    // Proberen
    void notify() {
        std::unique_lock<std::mutex> lock(mtx);
        ++count;
        cv.notify_one();
    }

    // Verhogen
    void wait() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this] { return count > 0; });
        --count;
    }
};
```

Dans cet exemple, la méthode `notify` incrémente le compteur du sémaphore et notifie un thread en attente. La méthode `wait` attend que le compteur soit supérieur à zéro, puis le décrémente.

Il est parfois utile pour compter des ressources de fournir aux méthodes `notify` et `wait` un argument `n` pour incrémenter ou décrémenter le compteur de `n` unités. Cela permet de libérer ou d'acquérir plusieurs ressources en une seule opération. Par exemple, si `n` est égal à 3, cela signifie que trois ressources sont libérées ou acquises en une seule opération.

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

Le problème du producteur et du consommateur est un problème classique de synchronisation de threads. Il s'agit de synchroniser un ou plusieurs threads producteurs qui produisent des données et un ou plusieurs threads consommateurs qui consomment ces données.

Le problème du producteur et du consommateur peut être résolu à l'aide de deux sémaphores :

- Un sémaphore `empty` pour compter le nombre d'emplacements vides dans le tampon
- Un sémaphore `full` pour compter le nombre d'emplacements pleins dans le tampon