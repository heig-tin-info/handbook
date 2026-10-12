#include <iostream>
#include <vector>
#include <chrono>
const int N = 10'000;
int main() {
    std::vector<std::vector<int>> matrix(N, std::vector<int>(N, 0));

    for (size_t i = 0; i < N; i++)
        for (size_t j = 0; j < N; j++)
            matrix[i][j] = i * N + j;

    auto start = std::chrono::high_resolution_clock::now();
    long long sum = 0;
    for (size_t i = 0; i < N; i++)
        for (size_t j = 0; j < N; j++)
#ifdef LINE
            sum += matrix[i][j];
#else
            sum += matrix[j][i];
#endif
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> time = end - start;
    std::cout << "Somme en ligne : " << sum << "\n";
    std::cout << "Temps d'accès: " << time.count() << " s" << std::endl;
}
