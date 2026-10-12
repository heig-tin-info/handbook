#include <iostream>
#include <thread>

static int x = 0;

int a() { for(;;) { x = 5; std::cout << x; } }
int b() { for(;;) x = 7; }

int main() {
    std::thread ta(a);
    std::thread tb(b);
    ta.join();
    tb.join();
}
