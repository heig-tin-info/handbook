#include <atomic>
#include <thread>
#include <vector>

#ifndef ITERATIONS
#    define ITERATIONS (1 << 27)
#endif
#ifndef NUM_THREADS
#    define NUM_THREADS 1
#endif

int main() {
    std::atomic<int> counter = 0;
    std::vector<std::jthread> threads;

    for(int i = 0; i < NUM_THREADS; i++) {
        constexpr int n = ITERATIONS / NUM_THREADS;
        threads.emplace_back([&]() {
            for (int i = 0; i < n; i++)
                counter++;
        });
    }
}