#include <stdio.h>
#include <string.h>
#include <assert.h>

#define CHARS_IN_ALPHABET 256

/**
 * Rabin-Karp algorithm
 * @param needle Motif à rechercher
 * @param haystack Texte d'entrée
 * @param matches La liste des occurences trouvées
 * @param size La taille du tableau matches
 * @return Le nombre d'occurences trouvées
 */
int search(char needle[], char haystack[], int matches[], size_t size)
{
    const int q = 101; // A prime number
    const int M = strlen(needle);
    const int N = strlen(haystack);

    int h = 1;
    for (int i = 0; i < M - 1; i++)
        h = (h * CHARS_IN_ALPHABET) % q;

    // Compute the hash value of pattern and first
    // window of text
    int p = 0; // Hash value for pattern
    int t = 0; // Hash value for haystack
    for (int i = 0; i < M; i++)
    {
        p = (CHARS_IN_ALPHABET * p + needle[i]) % q;
        t = (CHARS_IN_ALPHABET * t + haystack[i]) % q;
    }

    // Slide the pattern over text one by one
    size_t k = 0;
    for (int i = 0; i <= N - M; i++)
    {
        // Check the hash values of current window of text
        // and pattern. If the hash values match then only
        // check for characters on by one
        if (p == t)
        {
            // Check for characters one by one
            int j = 0;
            while (haystack[i + j] == needle[j] && j < M)
                j++;

            // Save the position found
            if (j == M)
                if (k < size)
                    matches[k++] = i;
                else
                    return k;
        }

        // Calculate hash value for next window of text.
        // Remove leading digit and add trailing digit.
        if (i < (N - M))
        {
            t = (CHARS_IN_ALPHABET *
                (t - haystack[i] * h) + haystack[i + M]) % q;
            t += t < 0 ? q : 0;
        }
    }
    return k;
}

int test_search()
{
    char text[] =
        "Le courage n'est pas l'absence de peur, "
        "mais la capacité de vaincre ce qui fait peur."
        "On ne peut vaincre sa destinée."
        "A vaincre sans barils, on triomphe sans boire.";

    int matches[10];
    int k = search("vaincre", text, matches, sizeof(matches)/sizeof(matches[0]));
    assert(k == 3);
    assert(matches[0] == 61);
    assert(matches[1] == 97);
    assert(matches[2] == 120);
}

int main() {
    test_search();
}
