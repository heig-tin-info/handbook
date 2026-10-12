#include <iostream>
#include <vector>
#include <thread>
#include <chrono>

#define VECTOR_SIZE 10'000'000  // Taille du vecteur
#define CACHE_LINE_SIZE 178    // Taille de la ligne de cache
#define NUM_THREADS std::thread::hardware_concurrency()

std::vector<int> largeVector(VECTOR_SIZE);

void processBlocks(int startBlock, int endBlock) {
    for (int block = startBlock; block < endBlock; block++) {
        for (int i = block * CACHE_LINE_SIZE; i < (block + 1) * CACHE_LINE_SIZE; i++) {
            largeVector[i]++;
        }
    }
}

int main() {
    // Initialisation du vecteur
    for (int i = 0; i < VECTOR_SIZE; i++) {
        largeVector[i] = 0;
    }

    // Mesure des performances avec False Sharing
    auto start1 = std::chrono::high_resolution_clock::now();

    for (size_t i = 0; i < 100; i++) {
        std::vector<std::thread> threads;
        for (size_t j = 0; j < NUM_THREADS; j++) {
            threads.push_back(std::thread(processBlocks, j, j + VECTOR_SIZE / (CACHE_LINE_SIZE * NUM_THREADS)));
        }
        for (auto& thread : threads) {
            thread.join();
        }
    }

    auto end1 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsedTime1 = end1 - start1;

    // Mesure des performances sans False Sharing (avec un bloc sur deux ignoré)
    auto start2 = std::chrono::high_resolution_clock::now();

    for (size_t i = 0; i < 100; i++) {
        std::vector<std::thread> threads;
        for (size_t j = 0; j < NUM_THREADS; j++) {
            if (j % 2 == 0) {
                threads.push_back(std::thread(processBlocks, j, j + VECTOR_SIZE / (CACHE_LINE_SIZE * NUM_THREADS)));
            }
        }
        for (auto& thread : threads) {
            thread.join();
        }
    }

    auto end2 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsedTime2 = end2 - start2;

    // Affichage des performances
    std::cout << "Temps d'exécution avec False Sharing : " << elapsedTime1.count() << " secondes" << std::endl;
    std::cout << "Temps d'exécution sans False Sharing : " << elapsedTime2.count() << " secondes" << std::endl;
}
