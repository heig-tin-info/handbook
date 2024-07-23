# Exercices de révision

!!! exercise "Mot du jour"

    Écrire un programme qui retourne un mot parmi une liste de mot, de façon aléatoire.

    ```c
    #include <time.h>
    #include <stdlib.h>

    char *words[] = {"Albédo", "Bigre", "Maringouin", "Pluripotent", "Entrechat",
        "Caracoler" "Palinodie", "Sémillante", "Atavisme", "Cyclothymie",
        "Idiosyncratique", "Entéléchie"};

    #if 0
        srand(time(NULL));   // Initialization, should only be called once.
        size_t r = rand() % sizeof(words) / sizeof(char*); // Generate random value
    #endif
    ```

    ??? solution

        ```c
        #include <time.h>
        #include <stdlib.h>

        char *words[] = {
            "Albédo", "Bigre", "Maringouin", "Pluripotent", "Entrechat",
            "Caracoler" "Palinodie", "Sémillante", "Atavisme", "Cyclothymie",
            "Idiosyncratique", "Entéléchie"};

        int main(void)
        {
            srand(time(NULL));
            puts(words[rand() % (sizeof(words) / sizeof(char*))]);
        }
        ```