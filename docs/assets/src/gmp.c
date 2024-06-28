#include <gmp.h>
#include <stdio.h>

int main(void)
{
    unsigned int radix = 10;
    char a[] = "19810983098510928501928599999999999990";

    mpz_t n;

    mpz_init(n);
    mpz_set_ui(n, 0);

    mpz_set_str(n, a, radix);

    mpz_out_str(stdout, radix, n);
    putchar('\n');

    mpz_add_ui(n, n, 12); // Addition

    mpz_out_str(stdout, radix, n);
    putchar('\n');

    mpz_mul(n, n, n); // Square

    mpz_out_str(stdout, radix, n);
    putchar('\n');

    mpz_clear(n);
}