#include <boost/thread.hpp>
#include <boost/bind/bind.hpp>
#include <iostream>

void printHello(int id)
{
    std::cout << "Hello from thread " << id << std::endl;
}

int main()
{
    boost::thread_group threadGroup;

    for (int i = 0; i < 5; ++i) {
        threadGroup.create_thread(boost::bind(&printHello, i));
    }

    threadGroup.join_all();
}