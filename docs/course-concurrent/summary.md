# Résumé

POSIX (Portable Operating System Interface) est une norme qui définit une interface système standard pour les systèmes d'exploitation de type UNIX. Cette norme a été définie par l'IEEE (Institute of Electrical and Electronics Engineers) et l'ISO (International Organization for Standardization). Elle a été inventée en 1988 pour permettre la portabilité des applications entre les systèmes UNIX.

## OS

### Appels Systèmes

- `fork` : Crée un nouveau processus en copiant le processus appelant.
- `clone` : Crée un nouveau processus léger en copiant le processus appelant.
- `exec` : Remplace l'image mémoire du processus appelant par un nouveau programme.
- `wait` : Attend la fin d'un processus.
- `exit` : Termine le processus appelant.
- `open` : Ouvre un fichier.
- `close` : Ferme un fichier.
- `read` : Lit des données depuis un fichier.
- `write` : Ecrit des données dans un fichier.
- `mmap` : Mappe un fichier en mémoire (new, malloc).
- ...

### Processus

Un processus c'est un programme en cours d'exécution. Il possède un espace d'adressage, un identifiant unique (PID), un état (running, waiting, sleeping, zombie), un parent (PPID), des ressources (fichiers ouverts, mémoire allouée, ...).

Pour créer un processus on a vu que l'appel système `fork` permet de dupliquer le processus appelant. Le processus fils hérite de l'espace d'adressage du processus parent. A ce moment là la mémoire est copiée en mode "copy-on-write". Cela signifie que la mémoire n'est pas copiée immédiatement mais seulement lorsqu'elle est modifiée. Et les deux processus sont indépendants. Donc c'est lourd en mémoire.

### Processus légers ou threads

Un processus léger se crée avec l'appel système `clone`. Il est plus léger qu'un processus car il partage le même espace d'adressage que le processus parent. Cela signifie que les threads partagent les mêmes variables globales, les mêmes fichiers ouverts, les mêmes signaux, ... Mais cela peut poser des problèmes de synchronisation: des accès concurrents à des ressources partagées.

### Mécanismes de synchronisation

Pour synchroniser les threads on utilise des primitives de synchronisation. Les plus courantes sont les mutex, les sémaphores et les moniteurs.

La notion de concurrence a été imaginée par Edsger Dijkstra en 1965 pour résoudre les problèmes de synchronisation dans les systèmes d'exploitation. Il était d'origine néerlandaise et a travaillé pour la compagnie Philips.

Il a inventé le concept de sémaphore. Un sémaphore est un objet de synchronisation qui possède un compteur. Il possède deux opérations atomiques: `wait` et `post`. `wait` décrémente le compteur et bloque si le compteur est négatif. `post` incrémente le compteur et réveille un thread en attente si le compteur est négatif.
Historiquement les noms donnés par Dijkstra étaient `P` et `V` pour `Proberen` et `Verhogen` en néerlandais.

Le sémaphore compte des ressources disponibles. Si le sémaphore est à zéro, il n'y a plus de ressources disponibles. Si le sémaphore est à un, il y a une ressource disponible. Si le sémaphore est à deux...

Plus tard sont venu des opérations atomiques dans les processeurs comme le `test-and-set` ou le `compare-and-swap`. Ces opérations permettent de réaliser des primitives de synchronisation plus complexes comme les mutex. Le gros avantage c'est l'absence d'attente active. L'attente active c'est une boucle qui teste une condition en permanence. C'est très gourmand en CPU.

Une opération atomique dans le cadre de l'informatique c'est une opération qui s'exécute en une seule instruction machine. Cela signifie que l'opération est indivisible. C'est soit tout ou rien. C'est soit l'opération s'exécute complètement, soit elle ne s'exécute pas du tout.

#### Mutex

En C++ le mutex est une classe qui permet de protéger des ressources partagées entre plusieurs threads. Il possède deux méthodes: `lock` et `unlock`. `lock` bloque le mutex si il est déjà verrouillé. `unlock` déverrouille le mutex.

```cpp
#include <iostream>
#include <thread>
#include <mutex>

std::mutex mtx;

void func() {
    mtx.lock();
    // Section critique
    std::cout << "Hello" << std::endl;
    mtx.unlock();
}

int main() {
    std::thread t(func);
    t.join();
}
```

On appelle section critique une portion de code qui accède à des ressources partagées. Il est important de protéger cette section critique avec un mutex pour éviter les accès concurrents.

En général on utilise pas le `lock`/`unlock` directement mais plutôt un `std::lock_guard` qui est un RAII (Resource Acquisition Is Initialization). C'est une classe qui s'occupe de libérer les ressources automatiquement à la fin du bloc.

```cpp
void func() {
    {
        std::lock_guard<std::mutex> lock(mtx);
        // Section critique
        std::cout << "Hello" << std::endl;
    }
}
```

On peut implémenter très facilement un lock_guard de la manière suivante:

```cpp
struct LockGuard {
    LockGuard(std::mutex &mtx) : mtx(mtx) { mtx.lock(); }
    ~LockGuard() { mtx.unlock(); }
private:
    std::mutex &mtx;
};
```

Aternativement au `lock_guard` on peut utiliser un `std::unique_lock`. La différence c'est qu'un `unique_lock` est un verrou de portée manuelle. Il peut être déverrouillé et verrouillé à nouveau.

```cpp
void func() {
    std::unique_lock<std::mutex> lock(mtx);
    // Section critique
    std::cout << "Hello" << std::endl;
}
```

Le unique_lock sera utilisé par exemple dans les variables conditions.

#### Variable condition

Une variable condition est un objet de synchronisation qui permet de mettre un thread en attente tant qu'une condition n'est pas remplie. Elle utilise un mutex pour protéger la condition et permet de notifier des threads.

Les méthodes les plus courantes sont `wait`, `wait_for`, `wait_until`, `notify_one` et `notify_all`.

```cpp
int beers_in_fridge = 0;
std::mutex mtx;
std::variable_condition cv;

void drinker() {
    while(true) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, []{ return beers_in_fridge > 0; });
        beers_in_fridge--;
    }
}

void gf() {
    while(true) {
        std::unique_lock<std::mutex> lock(mtx);
        beers_in_fridge++;
        cv.notify_one();
    }
}

int main() {
    std::thread t1(drinker);
    std::thread t2(gf);
    t1.join();
    t2.join();
}
```

Dans cet exemple, il y a un problème c'est que la copine (gf) peut mettre une bière dans le frigo alors qu'il est déjà plein. Il faudrait ajouter un sémaphore pour gérer le nombre de bières dans le frigo. Puisqu'un sémaphore est un compteur de ressources.

Mais ici, on est dans un cas de producteur-consommateur. Un producteur met des bières dans le frigo et un consommateur les boit.

#### Producteur-Consommateur

Le problème du producteur-consommateur est un problème classique de synchronisation.

On peut le résoudre de deux manières:

1. Avec deux sémaphores: un pour le producteur et un pour le consommateur.
2. Avec une variable condition.

#### Moniteur

Un moniteur est un objet de synchronisation qui encapsule des données et des opérations sur ces données. Il permet de protéger les données et de synchroniser les threads qui accèdent à ces données.

Concrètement c'est un classe qui contient des données et des méthodes pour accéder à ces données. Les méthodes sont protégées par un mutex pour éviter les accès concurrents.

```cpp
class Fridge {
public:
    void put(int beer) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this]{ return beers.size() < MAX; });
        beers.push_back(beer);
        cv.notify_one();
    }

    int get() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this]{ return beers.size() > 0; });
        int beer = beers.back();
        beers.pop_back();
        cv.notify_one();
        return beer;
    }
private:
    std::vector<int> beers;
    std::mutex mtx;
    std::variable_condition cv;
};
```

Si on veut l'utiliser dans l'exemple précédent on peut faire:

```cpp
void drinker(Fridge &fridge) {
    while(true) { int beer = fridge.get(); }
}

void gf(Fridge &fridge) {
    while(true) { fridge.put(1); }
}

int main() {
    Fridge fridge;
    std::thread t1(drinker, std::ref(fridge));
    std::thread t2(gf, std::ref(fridge));
    t1.join();
    t2.join();
}
```

### Deadlock et starvation

Le deadlock est une situation où deux threads se bloquent mutuellement en attendant une ressource que l'autre thread possède. C'est un problème classique de synchronisation.

Typiquement si la copine (gf) attend que le frigo soit vide pour mettre une bière et que le buveur (drinker) attend que le frigo soit plein pour boire une bière. C'est un deadlock.

C'est aussi le cas dans le dilemme des philosophes. Chaque philosophe a besoin de deux fourchettes pour manger. Si chaque philosophe prend une fourchette et attend que l'autre fourchette soit libre, il y a un deadlock: y'a cinq philosophes, une fouchette à gauche et une fourchette à droite, la table est ronde. Donc on a 5 fourchettes et 5 philosophes ce qui ne permet pas que tout le monde mange en même temps.

En théorie de programmation concurrente ce problème des philosphophe peut être décrit comme ayant un cycle dans le graphe des ressources. Chaque philosophe est un noeud et chaque fourchette est une arête. Si on a un cycle dans le graphe, il y a un deadlock.

La starvation (famine) est une situation où un thread n'arrive pas à accéder à une ressource partagée à cause de l'ordonnancement du système. C'est un problème de synchronisation.

Un exmple de famine serait si le buveur (drinker) boit toutes les bières et que la copine (gf) ne peut jamais mettre de bière dans le frigo. C'est une famine.

### Termes de programmation concurrente

- *Section Critique*: Une portion de code qui accède à des ressources partagées, dans laquelle un seul thread doit s'exécuter à la fois sinon il y a risque de corruption des données.
- *Deadlock*: Situation où deux threads se bloquent mutuellement en attendant une ressource que l'autre thread possède.
- *Starvation*: Situation où un thread n'arrive pas à accéder à une ressource partagée à cause de l'ordonnancement du système
- *Condition de course*: Situation où le résultat d'une opération dépend de l'ordre d'exécution des threads.

## Mémoire Cache

La mémoire cache est une mémoire rapide située entre le processeur et la mémoire principale. Elle permet d'accélérer l'accès aux données en stockant les données les plus fréquemment utilisées par le processeur.

Les problèmes typiques que l'on rencontre en programmation concurrente sont :

- *Cache Miss*: Situation où une donnée n'est pas présente dans le cache et doit être chargée depuis la mémoire principale.
- *False Sharing*: Situation où deux threads accèdent à des données qui sont stockées dans la même ligne de cache, ce qui entraîne des accès mémoire inutiles.
- *True Sharing*: Situation où deux threads accèdent à des données qui sont stockées dans la même ligne de cache, mais où les données sont réellement partagées entre les threads.

Pour résoudre ces problèmes on va s'assurer que l'alignement mémoire que l'on utilise dans nos thread ne crée pas de situation de false sharing. On peut aussi utiliser des attributs de compilation pour forcer l'alignement mémoire.

## Programmation Asynchrone

La programmation asynchrone est un style de programmation qui permet d'exécuter des tâches de manière concurrente sans bloquer le thread principal. Cela permet d'améliorer les performances en évitant les attentes inutiles.

En C++ on peut utiliser les threads, les promesses et les tâches pour réaliser de la programmation asynchrone.

- `std::async` : Exécute une fonction de manière asynchrone et renvoie un `std::future` qui permet de récupérer le résultat de la fonction.
- `std::promise` : Permet de communiquer entre deux threads en envoyant une valeur d'un thread à un autre.
- `std::future` : Permet de récupérer le résultat d'une fonction asynchrone.

## Programmation Parallèle

La programmation parallèle est un style de programmation qui permet d'exécuter des tâches de manière concurrente sur plusieurs processeurs ou cœurs de processeur. Cela permet d'améliorer les performances en répartissant la charge de calcul sur plusieurs unités de calcul.

En C++ on va souvent utiliser `std::hardware_concurrency` pour connaître le nombre de coeurs disponibles sur la machine. Pourquoi on va créer uniquement le nombre de thread qui correspond au nombre de coeurs ? Parce que si on crée plus de threads que de coeurs, on va créer des threads qui vont se partager le temps de calcul des coeurs. On va perdre beaucoup de temps dans les changements de contexte.

En pratique il est rare d'utiliser directement les thread pour paralléliser des tâches. On va plutôt utiliser des librairies comme OpenMP ou des frameworks comme Qt.

Avec OpenMP on peut paralléliser des boucles for, des sections de code ou des tâches. C'est très simple à utiliser et très efficace.

```cpp
#include <iostream>
#include <omp.h>

int main() {
    #pragma omp parallel for
    for(int i = 0; i < 10; i++) {
        std::cout << i << std::endl;
    }
}
```

Alternativement, on peut confier l'exécution de certain problèmes paralleles à des GPU. Les GPU sont des unités de calcul massivement parallèles qui permettent d'accélérer les calculs en parallélisant les tâches.