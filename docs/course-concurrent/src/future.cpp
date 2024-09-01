#include <future>
#include <iostream>
#include <thread>
#include <vector>

int main()
{
    std::vector<std::future<int>> f;

    /**
     * Solution 1: std::packaged_task
     * std::packaged_task est un moyen de transformer une fonction en une tâche asynchrone.
     * Une fois la tâche créée, on peut récupérer le résultat de la tâche sous forme de future.
     * La tâche doit être exécutée dans un thread.
     */

    // Une fonction doit être empaquetée dans un objet pour être exécutée de manière asynchrone
    std::packaged_task<int()> task([]{ return 7; });

    // Récupère le résultat de la tâche sous forme de future
    f.emplace_back(task.get_future());

    // La tâche doit être exécutée dans un thread
    std::jthread t(std::move(task));

    /**
     * Solution 2: std::async
     * Alternativement, on peut utiliser std::async pour exécuter une fonction de manière asynchrone
     * sans avoir à créer un thread explicitement.
     */
    f.emplace_back(std::async(std::launch::async, []{ return 8; }));

    /**
     * Solution 3: std::promise
     * std::promise est un moyen de communiquer entre un thread et un autre.
     * Un thread peut promettre une valeur future à un autre thread.
     */
    std::promise<int> p;
    f.emplace_back(p.get_future());
    std::thread([&p]{ p.set_value_at_thread_exit(9); }).detach();

    std::cout << "Waiting..." << std::flush;
    for (auto& f : f) f.wait();

    std::cout << "Done!\nResults are: ";
    for (auto& f : f) std::cout << f.get() << ' ';
    std::cout << '\n';
}