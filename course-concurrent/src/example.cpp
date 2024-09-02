#include <iostream>
#include <unistd.h>
#include <mutex>

#include "thread-pool.hpp"

std::mutex coutMutex;

int main()
{
    ThreadPool pool(4);

    for (int i = 0; i < 8; ++i) {
        pool.enqueue(0, [i]() {
            std::lock_guard<std::mutex> lock(coutMutex);
            std::cout << "Hello from thread " << i << std::endl;
        });
    }
}