# Pièges

Ce chapitre traite des pièges les plus courants dans lesquels l'apprenti programmeur ne manquera pas de tomber. Le C est un langage puissant, mais potentiellement dangereux, car il permet d'opérer à très bas niveau, ce qui peut occasionner des bogues retors à l'exécution.

## Préprocesseur

Rappelons-le, les macros sont des simples remplacements de chaînes de caractères intervenant avant la compilation.

### Macro avec paramètre

Le préprocesseur interprète une macro avec paramètres que si la parenthèse ouvrante suit directement et sans espace le nom de la macro. Ainsi considérant cet exemple :

```c
#define f (x) ((x) + 1)

int u = f(1)
```

Le préprocesseur génère ceci et le compilateur retournera une erreur du type `identification x non déclarés`.

```c
int u = (x) ((x) + 1)(1)
```

Observations :

- Ne jamais mettre d'espace entre le nom d'une macro et ses paramètres.
- Être toujours prêt à mettre en doute le code généré par une macro.

### Paramètres de macro non protégés

On ne le répètera jamais assez: une macro est un remplacement de chaîne effectué par le préprocesseur. Donc écrire `#define m(x) x * 2` et `m(2 + 5)` sera remplacé en `2 + 5 * 2`.

Quel sera le problème dans le cas suivant ?

```c
#define ABS(x) x >= 0 ? x: -x

int foo(void) {
    return ABS(5 - 8);
}
```

Plus difficile, quel serait le problème ici :

```c
#define ERROR(str) printf("Erreur: %s\r\n", str); log(str);

if (y < 0)
    ERROR("Zero division");
else
    x = x / y;
```

Observations :

- Toujours protéger les paramètres des macros avec des parenthèses

  ```c
  #define ABS(x) ((x) >= 0 ? (x): -(x))
  ```

- Toujours protéger une macro à plusieurs instructions par une boucle vide :

  ```c
  #define ERROR(str) do { \
      printf("Erreur: %s\r\n", str); \
      log(str); \
  } while (0)
  ```

### Pré/Post incrémentation avec une macro

On pourrait se dire qu'avec toutes les précautions prises, il n'y aura plus d'ennuis possibles. Or, les post/pré incréments peuvent encore poser problème.

```c
#define ABS(x) ((x) >= 0 ? (x) : -(x))

return ABS(x++)
```

On peut constater que x sera post-incrémenté deux fois au lieu d'une :

```c
#define ABS(x) ((x) >= 0 ? (x) : -(x))

return ((x++) >= 0 ? (x++) : -(x++))
```

Observations :

- Éviter l'utilisation de la pre/post incrémentation/décrémentation dans l'appel de macros.

## Erreurs de syntaxe

### Confusion = et ==

L'erreur est si vite commise, mais souvent fatale :

```c
if (c = 'o') {

}
```

L'effet contre-intuitif est que le test retourne toujours VRAI, car `'o' > 0`. Ajoutons que la valeur de `c` est modifié au passage.

Observations :

- Pour éviter toute ambiguïté, éviter les affectations dans les structures conditionnelles.

### Confusion & et &&

Confondre le ET logique et le ET binaire est courant. Dans l'exemple suivant, le `if` n'est jamais exécuté:

```c
int a = 0xA;
int b = 0x5;

if(a & b) {

}
```

### Écriture déroutante

Selon la table de précédences on aura `i--` calculé en premier suivi de `- -j`:

```c
k = i----j;
```

Observations :

- Éviter les formes ambigües d'écriture
- Favoriser la précédence explicite en utilisant des parenthèses
- Séparez vos opérations par des espaces pour plus de lisibilité: `k = i-- - -j`

### Point virgule

L'erreur typique suivante est arrivée à tout programmeur débutant. Le `;` placé après le test `if` agis comme une instruction nulle si bien que la fusée sera lancée à tous les coups :

```c
if (countdown == 0);
  launch_rocket();
```

Le même type d'erreur peut apparaître avec une boucle, ici causant une boucle infinie :

```c
while(i > 0);
{
    i--;
}
```
