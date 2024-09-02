#include <boost/asio.hpp>
#include <boost/asio/thread_pool.hpp>
#include <boost/bind/bind.hpp>
#include <iostream>
#include <mutex>

std::mutex coutMutex;

void printHello(int id)
{
    std::lock_guard<std::mutex> lock(coutMutex);
    std::cout << "Hello from thread " << id << std::endl;
}

int main()
{
    boost::asio::thread_pool pool(4);

    for (int i = 0; i < 8; ++i) {
        boost::asio::post(pool, [i] { printHello(i); });
    }

    pool.join();
}