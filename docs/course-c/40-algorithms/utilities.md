# Algorithmes sur chaînes

## Slurp

Il est souvent nécessaire de lire l'intégralité de l'entrée standard dans une chaîne de caractères. Cependant, comme l'entrée standard (`stdin`) n'est pas *seekable*, c'est-à-dire qu'il est impossible de se déplacer librement dans le flux ou d'en déterminer la taille à l'avance, il devient impossible d'allouer précisément la mémoire nécessaire à l'avance. Une stratégie commune consiste à lire le flux par fragments et à utiliser un tableau dynamique, redimensionné de façon progressive (via un facteur de croissance), pour stocker l'intégralité du contenu. C'est précisément l'objectif de la fonction `slurp` présentée ci-dessous. Slurp est un terme argotique qui signifie "aspirer" ou "engloutir" en anglais, c'est également un terme utilisé en informatique pour désigner le fait de lire un fichier en entier, notamment en Perl.

```c title="slurp.h"
--8<-- "docs/assets/src/slurp/slurp.h"
```

```c title="slurp.c"
--8<-- "docs/assets/src/slurp/slurp.c"
```

### Analyse et alternatives possibles

#### Taille prédéterminée

Une première alternative consisterait à allouer un espace mémoire suffisamment grand pour que la probabilité que le fichier excède cette taille soit très faible. Cependant, cette approche est loin d'être robuste. Elle se base sur des hypothèses qui pourraient échouer sur des systèmes avec des contraintes mémoire strictes, ou lorsque la taille du fichier dépasse largement les prévisions. De plus, elle introduit un risque de gaspillage de mémoire si l'estimation dépasse largement la taille réelle du fichier.

#### Utilisation d'un fichier temporaire

Une autre approche consisterait à rediriger le flux non *seekable* vers un fichier temporaire. Une fois que le flux a été entièrement consommé, il serait alors possible de rouvrir ce fichier temporaire et d'en déterminer la taille exacte avec `fseek`. On pourrait ensuite allouer précisément la mémoire requise en une seule opération, charger le fichier en mémoire, puis supprimer le fichier temporaire. Toutefois, cette solution, bien qu'ingénieuse, présente également des inconvénients : elle repose sur le système de fichiers, ce qui ajoute une complexité inutile et la rend sensiblement plus lente que la solution initiale.

#### Analyse de la solution proposée

La solution actuelle a néanmoins des aspects qui méritent d'être discutés. Tout d'abord, la taille du tampon initial est fixée arbitrairement à `256` caractères. Pour de grands fichiers, cette taille modeste entraînera un nombre élevé d'appels systèmes à `read`, ce qui peut affecter les performances globales. Une meilleure approche serait de permettre à l'utilisateur de spécifier la taille initiale du tampon en tant qu'argument optionnel de la fonction, avec une valeur par défaut appropriée si un argument nul ou zéro est fourni.

Par ailleurs, la fonction pourrait échouer dans le cas où le fichier à lire est trop volumineux pour tenir en mémoire. Une amélioration serait de permettre la définition d'une taille maximale à charger en mémoire, transmise en paramètre. Si le fichier dépasse cette limite, la fonction pourrait retourner un pointeur `NULL`, signalant ainsi au programme appelant que le fichier ne peut pas être traité entièrement en mémoire.

Un autre aspect discutable de l'implémentation actuelle réside dans la gestion des erreurs. En cas d'échec d'allocation mémoire (`malloc` ou `realloc`), la fonction appelle `exit()`, ce qui interrompt brutalement l'exécution du programme. Il serait préférable d'adopter une approche plus flexible en retournant un code d'erreur ou un pointeur `NULL`, laissant ainsi le programme appelant décider de la manière de gérer l'erreur. Cela permettrait une meilleure gestion des erreurs au niveau applicatif, notamment dans les cas où une terminaison immédiate du programme n'est pas souhaitable.

Enfin, on notera que l'espace alloué n'est pas réduit à la taille exacte du fichier après lecture. Cela peut entraîner un gaspillage de mémoire si l'algorithme vient de réallouer la mémoire. Une amélioration possible serait de réduire la taille du tampon à la taille exacte du fichier après lecture, en utilisant `realloc` pour libérer l'espace excédentaire.

La solution proposée est fonctionnelle mais perfectible, comme tout code informatique. Gardons à l'esprit ici que l'objectif est de comprendre le concept de l'algorithme et de saisir les principes de base de sa mise en œuvre.

## Split

Un besoin assez courant concernant les chaînes de caractères est de les diviser en sous-chaînes en fonction d'un délimiteur. Prenons l'exemple d'un fichier `CSV` (Comma-Separated Values) où les champs sont séparés par des virgules ou point virgules. Pour chaque ligne, l'objectif est de parcourir la chaîne à la recherche du délimiteur et de copier le champ dans un tableau. Pour conserver un code générique, l'opération de stockage des champs peut être confiée à une fonction de type `callback`, qui sera appelée pour chaque champ trouvé.

Pour l'implémentation il est possible de profiter de la fonction `strtok` de la bibliothèque standard C, qui permet de découper une chaîne en fonction d'un délimiteur. Cependant, `strtok` est une fonction *stateful*, c'est-à-dire qu'elle conserve l'état interne entre les appels. On préfèrera donc utiliser une version sécurisée *thread-safe* de cette fonction, `strtok_s`, qui prend en paramètre un pointeur vers un pointeur de chaîne de caractères. Cela permet de découper une chaîne en plusieurs sous-chaînes sans interférer avec d'autres appels à la fonction. Voici une implémentation possible de la fonction `split` :

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef void (*FieldCallback)(const char *field);

void split(const char *str, const char *delim, FieldCallback callback) {
    if (str == NULL || delim == NULL || callback == NULL) {
        fprintf(stderr, "Invalid argument(s) passed to split.\n");
        return;
    }

    // Copies str to avoid modifying the original. strtok is destructive, as
    // it adds null terminators to the original string.
    char *strCopy = strdup(str);
    if (strCopy == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return;
    }

    char *saveptr;
    char *token = strtok_r(strCopy, delim, &saveptr);
    while (token != NULL) {
        callback(token);
        token = strtok_r(NULL, delim, &saveptr);
    }
    free(strCopy);
}

void printField(const char *field) { printf("%s\n", field); }

int main() {
    const char *csvLine = "apple,banana,orange,grape";
    split(csvLine, ",", printField);
}
```

Dans le cas ou la chaîne originale est non constante, et qu'elle peut être modifiée sans risque, il n'est pas nécessaire de copier la chaîne avant de l'envoyer à `strtok_r` et le code de split peut être simplifié.

Notez également que si la fonction `callback` utilise un mécanisme de `longjmp` pour sortir de la fonction, le `free(strCopy)` pourrait ne jamais être appelé, ce qui entraînerait une fuite de mémoire.

## Join

L'opération de jointure est l'opération inverse de `split`. Elle consiste à concaténer plusieurs chaînes de caractères en une seule, en les séparant par un délimiteur. Cette opération est couramment utilisée pour générer des chaînes de requêtes SQL, des URL, des chaînes de formatage, etc. Voici une implémentation possible de la fonction `join` en utilisant la bibliothèque standard C :

```c
--8<-- "docs/assets/src/join/main.c"
```

## Trim

La fonction `trim` permet de supprimer les espaces en début et en fin de chaîne. Cette opération est couramment utilisée pour nettoyer les chaînes de caractères avant de les traiter. Voici une implémentation possible de la fonction `trim`.

La fonction modifie la chaîne en place en déplacant les caractères non blancs vers le début de la chaîne, puis en ajoutant un caractère nul à la fin de la chaîne.

```c
#include <stdio.h>
#include <ctype.h>

void trim(char *str) {
    if (str == NULL) {
        fprintf(stderr, "Invalid argument passed to trim.\n");
        return;
    }

    // Identify the start of the string
    char *start = str;
    while (*start != '\0' && isspace(*start)) start++;

    // Shift the string to the left
    char *end = start;
    while (*end != '\0') *(str++) = *(end++);
    *str = '\0';

    // Remove trailing whitespaces
    if (str > start) {
        str--;
        while (str >= start && isspace(*str)) *(str--) = '\0';
    }
}
```

Notons que cette implémentation n'est pas nécessairement optimale car elle parcours la chaîne de caractères. Dans le cas où il est possible de modifier le pointeur de la chaîne, il est possible de grandement simplifier l'algorithme en déplaçant directement le pointeur de début et en rajoutant une sentinelle à la fin de la chaîne.

## Chomp

La fonction `chomp` permet de supprimer le caractère de fin de ligne d'une chaîne de caractères. Ce caractère est généralement un retour à la ligne (`\n`) ou un retour chariot (`\r`). Le terme vient de l'action de "manger" le caractère de fin de ligne, il a été popularisé par le langage de programmation Perl qui dispose d'une fonction `chomp` pour effectuer cette opération.

Voici une implémentation possible de la fonction `chomp` :

```c
#include <stdio.h>
#include <string.h>

void chomp(char *str) {
    if (str == NULL) {
        fprintf(stderr, "Invalid argument passed to chomp.\n");
        return;
    }

    size_t len = strlen(str);
    if (len > 0 && (str[len - 1] == '\n' || str[len - 1] == '\r')) {
        str[len - 1] = '\0';
    }
}
```

## Reverse

La fonction `reverse` permet d'inverser une chaîne de caractères. Cette opération est couramment utilisée pour inverser le contenu d'une chaîne, par exemple pour afficher un texte à l'envers. Néanmoins notons que ce n'est pas une opération triviale en C.

Sans informations supplémentaires sur la chaîne de caractère, il n'est pas possible de savoir si elle contient des caractères multioctets (UTF-8, UTF-16, etc.) ou des caractères de contrôle. Dans le cas de caractères multioctets, il est nécessaire de traiter la chaîne de caractères en tant que séquence de caractères UTF-32 et non pas en tant que séquence d'octets. D'autre pas si la chaîne de caractères contient des caractères de contrôle comme `\r\n` il ne suffit pas d'inverser les deux caractères car `\n\r` n'est pas nécessairement reconnu par votre système.

### Implémentation ASCII

Voyons tout d'abord le cas trivial où la chaîne de caractères ne contient que des caractères ASCII :

```c
#include <stdio.h>

void swap(char *a, char *b) {
    char tmp = *a;
    *a = *b;
    *b = tmp;
}

void reverse(char *str) {
    if (str == NULL) {
        fprintf(stderr, "Invalid argument passed to reverse.\n");
        return;
    }

    char *start = str, *end = str;
    while (*end != '\0') end++;
    end--;

    while (start < end) swap(start++, end--);
}
```

[](){#utf8-reverse}

### Implémentation UTF-8

Dans cette implémentation plus compliquée, il est nécessaire de convertir les caractères UTF-8 multioctets en caractères UTF-32 pour pouvoir les inverser correctement. Voici un exemple d'implémentation de la fonction `reverse` pour les chaînes de caractères UTF-8. Elle utilise les fonctions `mbrtoc32` et `c32rtomb` de la bibliothèque standard C pour la conversion entre UTF-8 et UTF-32:

```c
#include <locale.h>
#include <stdio.h>
#include <stdlib.h>  // Pour MB_CUR_MAX
#include <string.h>
#include <uchar.h>

int main() {
   setlocale(LC_ALL, "");  // Initialiser la locale pour UTF-8

   char utf8_str[] = "Salut Γιώργος, comment ça va ? As-tu reçu mon 📧 ?";
   size_t utf8_len = strlen(utf8_str);

   // Convertir UTF-8 en UTF-32
   char32_t utf32_str[utf8_len];
   size_t utf32_len = 0;
   {
      mbstate_t state = {0};
      size_t ret;
      const char *p = utf8_str;
      while (*p != '\0') {
         size_t ret = mbrtoc32(&utf32_str[utf32_len], p, MB_CUR_MAX, &state);
         if (ret == (size_t)-1) {
            perror("Erreur de conversion UTF-8 vers UTF-32");
            return 1;
         } else if (ret == (size_t)-2) {
            // Séquence multioctet incomplète, passer à l'octet suivant
            break;
         } else if (ret == 0) {
            // Fin de la chaîne UTF-8 atteinte
            break;
         }
         p += ret;
         utf32_len++;
      }
   }

   // Inverser la chaîne UTF-32
   for (size_t i = 0, j = utf32_len - 1; i < j; i++, j--) {
      char32_t tmp = utf32_str[i];
      utf32_str[i] = utf32_str[j];
      utf32_str[j] = tmp;
   }

   // Conversion inverse UTF-32 vers UTF-8
   {
      mbstate_t state = {0};
      char *utf8_ptr = utf8_str;
      const char32_t *utf32_ptr = utf32_str;
      size_t utf8_total_len = 0;
      size_t ret;
      while (utf32_len--) {
         ret = c32rtomb(utf8_ptr, *utf32_ptr++, &state);
         if (ret == (size_t)-1) {
            perror("Erreur de conversion UTF-32 vers UTF-8");
            return 1;
         }
         utf8_ptr += ret;  // Avancer dans le buffer UTF-8
         utf8_total_len += ret;
      }
      utf8_str[utf8_total_len] = '\0';
   }

   printf("%s\n", utf8_str);
}
```
