# Test

La directive include peut prendre deux formes, l'inclusion locale et l'inclusion globale. Il s'agit d'ailleurs de l'une des questions les plus posées (c.f. [cette question](https://stackoverflow.com/questions/21593/what-is-the-difference-between-include-filename-and-include-filename).).

`#!c \#include <filename>`

: Le préprocesseur va chercher le chemin du fichier à inclure dans les chemins de l'implémentation.

`#!c \#include "filename"`

: Le préprocesseur cherche le chemin du fichier à partir du chemin courant et les chemins donnés par les des directives `-I`.
