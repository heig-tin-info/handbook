#include <thread>
#include <iostream>
#include <chrono>
#include <vector>
constexpr size_t alignment_size = SIZE; // Une valeur supposée si non disponible

struct Foo {
    alignas(alignment_size) int x{0};
    alignas(alignment_size) int y{0};
};

void update_foo(Foo& data, int id) {
    for (int i = 0; i < 500000000; ++i) {
        if (i % 2)
            data.x += id;
        else
            data.y += id;
    }
}

int main() {
    Foo x, y;
    std::cerr << sizeof(Foo) << std::endl;
    std::vector<std::thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back(update_foo, std::ref(x), 1);
    }
    auto start1 = std::chrono::high_resolution_clock::now();
    for (auto& thread : threads)
        thread.join();
    auto end1 = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsedTime1 = end1 - start1;

    std::cout << elapsedTime1.count() << std::endl;
}