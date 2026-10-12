// 10 threads, wait 1s
// Display their ID on stdout
// Protect stdout with mutex
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <chrono>


int func(int id) {
    static std::mutex mtx;
    for(;;) {
#if 0
        mtx.lock();
        std::cout << id << ": " << std::this_thread::get_id() << std::endl;
        mtx.unlock();
#else 
        {
            std::lock_guard g(mtx);
            std::cout << id << ": " << std::this_thread::get_id() << std::endl;
        }
#endif 
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

int main() {
    std::vector<std::jthread> threads;
    for (int i = 0; i < 10; i++) threads.emplace_back(func, i + 1);

    //for (auto &thread : threads) thread.join();
}