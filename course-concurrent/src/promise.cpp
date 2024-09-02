#include <chrono>
#include <future>
#include <iostream>
#include <numeric>
#include <vector>
#include <ranges>
#include <thread>
#include <algorithm>

using namespace std;

void accumulate(ranges::range auto range, promise<int> accumulate_promise) {
    int sum = accumulate(range.begin(), range.end(), 0);
    accumulate_promise.set_value(sum); // Notify future
}

void do_work(promise<void> barrier) {
    this_thread::sleep_for(chrono::seconds(1));
    barrier.set_value();
}

int main() {
    vector<int> numbers(6);
    iota(numbers.begin(), numbers.end(), 1);

    promise<int> accumulate_promise;
    future<int> accumulate_future = accumulate_promise.get_future();

    jthread work_thread([&] { accumulate(numbers, move(accumulate_promise)); });

    cout << "result=" << accumulate_future.get() << '\n';

    promise<void> barrier;
    future<void> barrier_future = barrier.get_future();
    jthread new_work_thread([&] { do_work(move(barrier)); });
    barrier_future.wait();
}
