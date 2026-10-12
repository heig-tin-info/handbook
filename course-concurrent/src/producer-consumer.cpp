#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <semaphore>
#include <cstdlib>
#include <cmath>
#include <condition_variable>

template <int MAX>
class Semaphore {
    std::mutex mtx;
    std::condition_variable cv;
    std::condition_variable cf;
    int count;

public:
    Semaphore(int count = 0) : count(count) {}

    // Proberen
    void release() {
        std::unique_lock<std::mutex> lock(mtx);
        cf.wait(lock, [this] { return count < MAX; });
        ++count;
        cv.notify_one();
    }

    // Verhogen
    void acquire() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this] { return count > 0; });
        --count;
        cf.notify_one();
    }
};

#define MAX 20
static std::vector<int> buffer;
static std::mutex mtx;
static std::counting_semaphore<MAX> sem_empty(MAX);
static std::counting_semaphore<MAX> sem_full(0);

constexpr void acquire(std::counting_semaphore<MAX>& sem, int n) {
    for (int i = 0; i < n; i++) {
        sem.acquire();
    }
}
constexpr void release(std::counting_semaphore<MAX>& sem, int n) {
    for (int i = 0; i < n; i++) {
        sem.release();
    }
}

void consumer(int time, int lot) {
    while (true) {
        acquire(sem_full, lot);
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(time));
            std::lock_guard<std::mutex> lock(mtx);
            std::cout << "Buffer [" << buffer.size() << "/" << MAX << "]" << std::endl;                    
            std::cout << "Consumer: ";
            for (int i = 0; i < lot; i++) {
                int data = buffer.back();
                buffer.pop_back();
                std::cout << " " << data ;
            }
            std::cout << std::endl;
        }
        release(sem_empty, lot);
    }
}

void producer(int time, int lot) {
    auto t0 = std::chrono::system_clock::now();
    while (true) {
        acquire(sem_empty, lot);
        {
            const int data = std::rand() % 100;
            // Wait time is sinuoidal function of time
            const float frequency = 0.5;
            const float amplitude = time / 2;
            auto fluctuations = std::chrono::duration<double>(
                time + amplitude * std::sin(2 * M_PI * frequency * std::chrono::duration<double>(std::chrono::system_clock::now() - t0).count())
            );
            std::cout << "Fluctuations: " << fluctuations.count() << std::endl;
   auto fluctuations_ms = std::chrono::duration_cast<std::chrono::milliseconds>(fluctuations / 1000);

            std::this_thread::sleep_for(fluctuations_ms);
            std::lock_guard<std::mutex> lock(mtx);
            std::cout << "Buffer [" << buffer.size() << "/" << MAX << "]" << std::endl;       
            std::cout << "Producer: ";     
            for (int i = 0; i < lot; i++) {
                buffer.push_back(data);
                std::cout << " " << data;
            }
            std::cout << std::endl;
        }
        release(sem_full, lot);
    }
}

int main(int argc, char*argv[]) {
    int manufacturing_time = atoi(argv[1]);
    int consuming_time = atoi(argv[2]);
    int manufacturing_lot = atoi(argv[3]);
    int consuming_lot = atoi(argv[4]);

    std::thread t1(producer, manufacturing_time, manufacturing_lot);
    std::thread t2(consumer, consuming_time, consuming_lot); 
    t1.join();
    t2.join();
}
