# GTK

GTK (*Gimp ToolKit*) est une bibliothèque logicielle libre qui permet de créer des interfaces graphiques. Elle est utilisée par de nombreux logiciels, dont le bureau GNOME, GIMP, Inkscape, etc. C'est la bibliothèque graphique la plus utilisée sous Linux.

![Architecture GTK](/assets/images/gtk-stack.drawio)

Elle repose grandement sur GLib, la bibliothèque de base de GNOME, qui fournit des types de données, des macros, des structures et des fonctions de base pour la programmation en C. Avec Glib on peut par exemple simplifier considérablement le développement en C, en fournissant des fonctions pour la gestion de la mémoire, des chaînes de caractères, des listes, des tableaux, des arbres, des files d'attente, des piles, des tables de hachage etc. Voici un exemple simple d'utilisation de GLib :

```c
#include <glib.h>

int main(int argc, char **argv) {
    // Créer et parcourir une liste
    GList *list = NULL;
    list = g_list_append(list, "Hello");
    list = g_list_append(list, "World");
    g_list_foreach(list, (GFunc)g_print, NULL);
    g_list_free(list);

    // Générer un nombre aléatoire
    g_random_int();

    // Simplifier la gestion des chaînes de caractères
    GString *string = g_string_new("Hello");
    g_string_append(string, " World");

    // etc.
}
```

GDK (*Gimp Drawing Kit*) est une bibliothèque qui fournit des fonctions pour la gestion des fenêtres, des événements, des images, des polices de caractères, etc. Elle est utilisée par GTK pour dessiner les éléments graphiques.

GSK (*Gimp Scene Kit*) est une bibliothèque qui fournit des fonctions pour la gestion des animations, des transitions, des effets graphiques, etc. Elle est utilisée par GTK pour animer les éléments graphiques.

Enfin PANGO est une bibliothèque qui fournit des fonctions pour la gestion des polices de caractères, des textes, des langues, etc. Elle est utilisée par GTK pour afficher du texte.

Ces 4 bibliothèques sont les composants principaux de GTK et elles se reposent sur différentes librairies comme CAIRO pour le rendu graphique.

Cairo est une bibliothèque de dessin 2D qui fournit des fonctions pour dessiner des lignes, des courbes, des formes, des images, des textes, etc. Elle est utilisée par GDK pour dessiner les éléments graphiques.

OpenGL et Wayland sont utilisées pour le rendu graphique et l'intégration avec le gestionnaire de fenêtres.

## Glade

Glade est un logiciel graphique qui permet de créer des interfaces graphiques pour GTK de manière interactive. Il permet de dessiner les fenêtres, les boutons, les champs de texte, etc. et de générer le code source correspondant.

Il est très utile pour les débutants qui ne connaissent pas encore bien GTK, car il permet de voir en temps réel le rendu de l'interface graphique et de générer le code source correspondant. Il est également très utile pour les développeurs expérimentés, car il permet de gagner du temps en évitant de devoir écrire le code source à la main.