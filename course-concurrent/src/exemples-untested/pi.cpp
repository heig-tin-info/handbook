#include <iostream>
#include <chrono>
#include <numeric>
#include <vector>
#include <omp.h>


double estimate_pi_false_share(uint64_t num_steps) {
    auto max_threads = omp_get_max_threads();
    auto delta = 1.0 / static_cast<double>(num_steps);
    std::vector<double> partial_sum(max_threads, 0.0);
    int num_threads;
#ifdef OMP
#pragma omp parallel default(none) shared(num_steps, delta, max_threads, num_threads, partial_sum)
#endif
    {
        if (omp_get_thread_num() == 0) num_threads = omp_get_num_threads();
        auto local_sum = 0.0;
        for (uint64_t step = omp_get_thread_num(); step < num_steps; step += omp_get_num_threads()) {
            auto x = delta * (static_cast<double>(step) + 0.5);
#ifdef TRUE_SHARE
            local_sum += 4.0 / (1 + x * x);
#else
            partial_sum[omp_get_thread_num()] += 4.0 / (1 + x * x);
#endif
        }
#ifdef TRUE_SHARE
        partial_sum[omp_get_thread_num()] = local_sum;
#endif
    }
    std::cout << "Number of threads: " << num_threads << std::endl;
    return std::accumulate(std::begin(partial_sum), std::begin(partial_sum) + num_threads, 0.0) * delta;
}

int main() {
    auto num_steps = 1'000'000'000;
    auto start = std::chrono::high_resolution_clock::now();
    auto pi = estimate_pi_false_share(num_steps);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Pi: " << pi << "\n";
    std::cout << "Time: " << elapsed.count() << " s" << std::endl;
}