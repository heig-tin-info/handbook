#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX 1000

int main(int argc, char *argv[]) {
   if (argc != 2) return -1;
   int n = atoi(argv[1]);
   if (n > MAX) return -2;
   bool primes[MAX];

   // Considère tous les nombres comme premiers
   for (int i = 0; i <= n; i++) primes[i] = true;

   // Ératosthène sieve algorithm
   primes[0] = primes[1] = false;  // 0 et 1 are not prime numbers
   for (int p = 2; p <= sqrt(n); p++)
      if (primes[p])
         for (int i = p * p; i <= n; i += p) primes[i] = false;

   // Display prime numbers
   for (int i = 2; i <= n; i++)
      if (primes[i]) printf("%d ", i);
   printf("\n");
}
