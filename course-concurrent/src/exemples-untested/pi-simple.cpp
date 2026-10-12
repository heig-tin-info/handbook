#include <iostream>
#include <omp.h>
#include <string>

using namespace std::string_literals;

double estimate_pi_seq(uint64_t num_steps) {
    auto delta = 1.0 / static_cast<double>(num_steps);
    double pi = 0.0;
    for (uint64_t step = 0; step < num_steps; ++step) {
        auto x = delta * (static_cast<double>(step) + 0.5);
        pi += 4.0 / (1 + x * x);
    }
    return pi * delta;
}

double estimate_pi_par(uint64_t num_steps) {
    auto delta = 1.0 / static_cast<double>(num_steps);
    double pi = 0.0;
#pragma omp parallel for default(none) shared(num_steps, delta) reduction(+:pi)
    for (uint64_t step = 0; step < num_steps; ++step) {
        auto x = delta * (static_cast<double>(step) + 0.5);
        pi += 4.0 / (1 + x * x);
    }
    return pi * delta;
}

int main(int argc, const char **argv) {
    uint64_t num_steps = std::stoull(argv[1]);
    auto calc_pi = [argv](uint64_t num_steps) {
        return "seq"s == argv[2] ? estimate_pi_seq(num_steps) : estimate_pi_par(num_steps);
    };
    auto pi = calc_pi(num_steps);
    std::cout << pi << "\n";
}