# Fenêtre graphique

Comme nous l'avons vu, un programme informatique standard dispose de plusieurs flux : un flux d'entrée (`stdin`) et deux flux de sortie (`stdout` et `stderr`). Ces flux sont généralement associés à la console texte, mais ne sont pas directement reliés à une fenêtre graphique permettant des interactions visuelles. Pourtant, de nombreuses applications modernes nécessitent une interface graphique pour permettre une meilleure interaction avec l'utilisateur.

Sous Windows comme sous Linux, l'interface utilisateur graphique, composée de fenêtres, de menus et d'autres éléments interactifs, est gérée par ce que l'on appelle un *window manager*. Ce gestionnaire de fenêtres est responsable de la création, de la gestion et de la disposition des différentes fenêtres à l'écran. Il agit comme une couche intermédiaire entre le noyau du système d'exploitation et les applications graphiques.

Le *window manager* est un processus distinct qui fonctionne en parallèle de votre programme. Il est donc essentiel, d'une part, qu'il soit déjà lancé avant l'exécution de votre application (ce qui est généralement le cas dans un environnement de bureau standard) et, d'autre part, que votre programme soit capable de communiquer avec ce gestionnaire de manière appropriée. Sous Linux, cette communication se fait via le protocole X11, également connu sous le nom de "X Window System".

## Le protocole X11

X11 est un protocole réseau qui permet à un programme de dessiner des fenêtres sur l'écran, qu'il soit local ou distant. Il a la particularité d'être indépendant de la machine où l'application s'exécute, permettant ainsi de contrôler graphiquement des applications sur d'autres ordinateurs. Cependant, interagir directement avec X11 est un processus complexe, car cela implique de gérer de nombreux paramètres relatifs aux fenêtres : dimensions, position, gestion des événements, et autres aspects liés à l'interaction utilisateur.

Le protocole X11 est basé sur un modèle client-serveur. Un programme se connecte donc au serveur en utilisant des sockets, typiquement des sockets Unix (*Unix Domain Socket*). C'est un canal de communication avec le serveur dans lequel des ordre du type "dessine un rectangle à telle position" ou "affiche ce texte" sont envoyés. Le serveur X11 est responsable de la gestion des fenêtres, des événements, des polices, des couleurs, etc.

Comme la communication passe par les sockets, il est possible de profiter de l'encapsulation TCP/IP et de dialoguer avec un server distant. Avant l'avènement WSLg (*Windows Subsystem for Linux GUI*), il était possible d'afficher des fenêtres graphiques Linux en utilisant un serveur X11 installé directement sous Windows comme [VcXsrv](https://sourceforge.net/projects/vcxsrv/). Notons que si vous utilisez Docker, ou que vous vous connectez à un Raspberry Pi, vous pouvez également véhiculer des fenêtres graphiques depuis une connection SSH par exemple (via l'option `-X`).

Pour illustrer la complexité de l'usage direct de X11, voici un exemple de programme en C qui ouvre une simple fenêtre de 100 pixels par 100 pixels :

```c
#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
   // Open display
   Display *d = XOpenDisplay(NULL);
   if (d == NULL) {
      fprintf(stderr, "Impossible d'ouvrir le display\n");
      exit(1);
   }

   // Create window
   int s = DefaultScreen(d);
   Window w = XCreateSimpleWindow(d, RootWindow(d, s), 10, 10,  // x, y
                                  100, 100,                     // width, height
                                  1,                            // border width
                                  BlackPixel(d, s), WhitePixel(d, s));

   XSelectInput(d, w, ExposureMask | KeyPressMask);  // Select event to watch
   XMapWindow(d, w);                                 // Display the window

   // Event loop
   for (;;) {
      XEvent e;
      XNextEvent(d, &e);
      if (e.type == Expose)
         XFillRectangle(d, w, DefaultGC(d, s), 20, 20, 10, 10);
      if (e.type == KeyPress) break;
   }

   XCloseDisplay(d);  // Close the display
}
```

Pour compiler et exécuter ce programme vous aurez besoin de la bibliothèque X11. Sous Ubuntu, vous pouvez l'installer avec la commande suivante :

```bash
sudo apt-get install libx11-dev
```

Ensuite, vous pouvez compiler le programme avec la commande suivante :

```bash
gcc window.c -lX11
```

Ce code ouvre une fenêtre minimaliste, mais il est évident qu'implémenter des interfaces graphiques sophistiquées en utilisant uniquement X11 est un travail considérable. La gestion manuelle des événements, des composants graphiques et des interactions utilisateurs devient rapidement fastidieuse.

D'autre part ce protocol n'est pas portable, il est spécifique à Linux et n'est pas disponible sur d'autres systèmes d'exploitation. Sous Windows à partir de Windows 11 et avec WSL2, il est possible d'utiliser X11 pour afficher des fenêtres graphiques et de tester ce programme.

## Wayland

Wayland est un protocole graphique plus récent que X11, conçu pour remplacer ce dernier en tant que gestionnaire de fenêtres par défaut sous Linux. Wayland est plus moderne, plus sécurisé et plus performant que X11, mais il est également plus restrictif en termes de fonctionnalités. Wayland est conçu pour être plus simple et plus sécurisé que X11, en limitant l'accès des applications aux ressources système et en isolant les processus les uns des autres.

## L'API Win32

Sous Windows, l'équivalent de X11 est l'API Win32, qui permet de créer des applications graphiques pour le système d'exploitation de Microsoft. L'API Win32 est une interface de programmation d'applications (API) basée sur des messages, qui permet de créer des fenêtres, des contrôles, des menus, et d'autres éléments d'interface utilisateur. L'API Win32 est plus complexe que X11, mais elle offre des fonctionnalités plus avancées et une meilleure intégration avec le système d'exploitation. Voici à titre d'exemple le même programme que précédemment, mais cette fois-ci en utilisant l'API Win32 :

```c
#include <windows.h>

LRESULT CALLBACK WindowProcedure(HWND hwnd, UINT msg, WPARAM wParam,
                                 LPARAM lParam) {
   switch (msg) {
      case WM_DESTROY:
         PostQuitMessage(0);
         break;
      default:
         return DefWindowProc(hwnd, msg, wParam, lParam);
   }
   return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                   LPSTR lpCmdLine, int nCmdShow) {
   // Définition de la classe de fenêtre
   WNDCLASS wc = {0};
   wc.lpfnWndProc = WindowProcedure;  // Fonction callback pour les messages
   wc.hInstance = hInstance;
   wc.lpszClassName = "MaFenetreClass";

   if (!RegisterClass(&wc)) {
      return -1;
   }

   // Création de la fenêtre
   HWND hwnd = CreateWindowEx(0, "MaFenetreClass", "Ma Fenetre",
                              WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
                              100, 100, NULL, NULL, hInstance, NULL);

   if (hwnd == NULL) {
      return -1;
   }

   ShowWindow(hwnd, nCmdShow);
   UpdateWindow(hwnd);

   // Event loop
   MSG msg = {0};
   while (GetMessage(&msg, NULL, 0, 0)) {
      TranslateMessage(&msg);
      DispatchMessage(&msg);
   }

   return msg.wParam;
}
```

Pour compiler ce programme, vous pouvez utiliser le compilateur MinGW (Minimalist GNU for Windows) qui fournit les outils nécessaires pour compiler des programmes C sous Windows. Vous pouvez installer MinGW via le gestionnaire de paquets MSYS2, qui fournit un environnement de développement similaire à celui de Linux.

```bash
gcc window.c -lgdi32
```

Alternativement, vous pouvez utiliser l'environnement officiel de développement de Microsoft, Visual Studio, qui fournit un ensemble complet d'outils pour le développement d'applications Windows mais son installation est plus lourde et dépasse le cadre de ce cours.

## Pipeline graphique

Quelque soit la bibliothèque graphique utilisée, la programmation graphique suit un *pipeline* bien défini. Le pipeline graphique est un ensemble d'étapes qui transforment les données géométriques en pixels affichés à l'écran. Ces étapes incluent la transformation des coordonnées, l'application des textures, l'éclairage, la perspective, et bien d'autres. Chaque étape du pipeline est configurable par l'application, permettant ainsi de personnaliser le rendu graphique en fonction des besoins.

Tout contenu qui implique du rendu graphique accéléré (comme le dessin de formes, d'images ou de scènes 3D) passe par le pipeline graphique. Les bibliothèques graphiques de haut niveau, comme GTK ou Qt, SDL ou Allegro, abstraient généralement le pipeline graphique pour simplifier le développement d'interfaces graphiques.

Le pipeline graphique permet d'écrire dans un *framebuffer*, une zone de mémoire qui stocke les pixels de l'image à afficher. Le framebuffer est ensuite affiché à l'écran par le *window manager* ou le système d'exploitation. Le framebuffer est une abstraction de la mémoire vidéo de la carte graphique qui est généralement organisé en trois canaux de couleur (rouge, vert, bleu) pour chaque pixel, ainsi que des canaux supplémentaires pour la transparence (alpha) et la profondeur (z-buffer).

Les différentes étapes du pipeline graphique sont les suivantes.

### Vertex

La première étape du pipeline graphique est la transformation des coordonnées des sommets des objets géométriques en coordonnées de l'écran. Cette étape est appelée *vertex processing* et consiste à appliquer des transformations géométriques (comme la translation, la rotation, l'échelle) aux sommets des objets. Les coordonnées des sommets sont généralement définies dans un espace 3D, mais elles doivent être transformées en coordonnées 2D pour l'affichage à l'écran.

Imaginons que l'on souhaite dessiner une pyramide en 3D. Chaque sommet de la pyramide est défini par ses coordonnées (x, y, z) dans l'espace 3D. Les données sont écrites dans un *buffer* de sommets comme dans l'exemple suivant:

```c
struct Vertex { float x, y, z; }[] = {
   {0.0f, 1.0f, 0.0f},   // Sommet 0
   {-1.0f, -1.0f, 1.0f}, // Sommet 1
   {1.0f, -1.0f, 1.0f},  // Sommet 2
   {1.0f, -1.0f, -1.0f}, // Sommet 3
   {-1.0f, -1.0f, -1.0f} // Sommet 4
};
```

Un *vertex* (sommet) peut alternativement contenir des informations supplémentaires comme la couleur, la texture ou la normale. Cette dernière est une information importante pour le calcul de l'éclairage.

Dans une carte graphique toute forme géométrique est définie par des sommets, lesquels forment des triangles. Les triangles sont les formes les plus simples à dessiner et sont utilisés pour représenter des surfaces planes. Il faut deux triangles pour dessiner un rectangle, trois pour un quadrilatère, et un certain nombre pour dessiner un cercle. Il est intéressant de noter qu'une carte graphique n'est pas capable de dessiner des cercles à partir de coordonnées simples, ces derniers seront toujours appriximés par des triangles.

### Assemblage des primitives

Les sommets seuls ne forment pas encore une géométrie complète. Ils doivent être assemblés en primitives (triangles, lignes, points). L'assemblage des primitives consiste à prendre des groupes de sommets et à les combiner pour former des triangles ou d'autres formes géométriques. La primitive la plus courante est le triangle, c'est d'ailleurs celle que nous avons utilisée pour définir la pyramide précédente. Néanmoins il existe d'autres primitives comme le point, la ligne, le triangle strip, le triangle fan, etc. Les deux dernières primitives sont utilisées pour optimiser le nombre de sommets à envoyer à la carte graphique, certains sommets peuvent être partagés entre plusieurs triangles.


### Traitement des sommets

Une fois les primitives assemblées, les sommets sont traités par le *vertex shader*. Le *vertex shader* est un petit programme écrit en langage de shader (comme [GLSL](wiki:glsl) pour OpenGL ou HLSL pour DirectX sous Windows) qui s'exécute sur chaque sommet de la primitive. Le GLSL est un langage très proche du C mais beaucoup plus limité. En revanche il est capable de tirer parti des capacités de calcul parallèle des cartes graphiques et donc d'être très performant pour certaines opérations.

Le *vertex shader* est responsable de la transformation des coordonnées des sommets, de l'application des textures, de l'éclairage, et d'autres opérations géométriques.

Par exemple, notre pyramide devra être orientée dans l'espace 3D. Selon la position de la caméra, la pyramide devra être tournée, déplacée, et éventuellement éclairée. Par l'application de matrices de transformation (translation, rotation, mise à l'échelle) le *vertex shader* permet de passer de coordonnées locales aux coordonnées de l'espace de la caméra, puis aux coordonnées de l'écran.

Selon l'éclairage de la scène, le *vertex shader* peut également calculer la couleur de chaque sommet en fonction de la position de la lumière. Cette couleur est ensuite interpolée entre les sommets pour obtenir une couleur lisse sur toute la surface du triangle.

Enfin le *vertex shader* peut également calculer les coordonnées de texture pour chaque sommet. Une texture est une image (comme une photo ou une illustration) qui est appliquée à la surface d'un objet pour lui donner un aspect réaliste.

Dans notre exemple, imagions que notre pyramide est celle de Kheops, de Khéphren ou de Mykérinos et que notre caméra est un drone qui survole le Caire. Il est 17h, le soleil est bas sur l'horizon et éclaire la pyramide.

![Pyramide depuis le Caire](/assets/images/caire.png)

(donner un exemple concret avec les données de la caméra, de la lumière et une texture de brique, une transformation de perspective de la lentille de la caméra, let normales des faces pour le calcul de l'éclairage. Donner un exemple en GLSL du vertex shader pour la pyramide.)

### Tessellation

La tessellation est une étape optionnelle du pipeline graphique qui permet de subdiviser les primitives en triangles plus petits. Cette technique est utilisée pour augmenter la densité de triangles dans les zones de la scène qui nécessitent plus de détails, comme les courbes ou les surfaces complexes. La tessellation est particulièrement utile pour le rendu de surfaces lisses et organiques, comme les visages humains ou les paysages naturels.

### Géométrie

L'étape de géométrie est une autre étape optionnelle du pipeline graphique qui permet de générer de nouveaux sommets à partir des sommets d'entrée. Cette étape est utile pour ajouter des détails supplémentaires à la géométrie, comme des arêtes supplémentaires, des plis ou des déformations. La géométrie est souvent utilisée pour générer des ombres, des reflets ou des effets spéciaux dans les jeux vidéo et les applications graphiques.

Par exemple si vous souhaitez dessiner 1000 triangles à l'écran, chacun avec une orientation différente, il n'est pas nécessaire de spécifier les 3000 sommets correspondants. Il suffit de donner les centres des triangles et les orientations. Le *geometry shader* se chargera de générer les sommets correspondants. Voici un exemple ci-dessous de code GLSL pour un *geometry shader* qui génère des triangles à partir de points. Le programme `main` sera appelé par la carte graphique pour chaque point du buffer d'entrée, il s'executera donc en parallèle pour chaque point. Un `vec4` est un vecteur de 4 composantes, ici les coordonnées $x$, $y$, $z$ et $w$. Le $w$ est une composante supplémentaire dont nous n'avons pas besoin ici.

```c
#version 330 core

layout (points) in;
layout (triangle_strip, max_vertices = 3) out;

void main() {
   gl_Position = gl_in[0].gl_Position + vec4(-0.1, -0.1, 0.0, 0.0);
   EmitVertex();

   gl_Position = gl_in[0].gl_Position + vec4(0.1, -0.1, 0.0, 0.0);
   EmitVertex();

   gl_Position = gl_in[0].gl_Position + vec4(0.0, 0.1, 0.0, 0.0);
   EmitVertex();

   EndPrimitive();
}
```

### Clipping

L'étape de clipping consiste à éliminer les parties de la géométrie qui ne sont pas visibles à l'écran. Cette étape est nécessaire pour éviter de dessiner des objets qui sont en dehors du champ de vision de la caméra. Le clipping est généralement effectué en coordonnées d'écran, après la projection des sommets en 2D. Le *frustrum* est une forme tronquée qui représente le champ de vision de la caméra. Les parties de la géométrie qui se trouvent en dehors du *frustrum* sont éliminées.

Cette étape n'a pas besoin d'être gérée manuellement par le développeur, elle est généralement effectuée par le matériel graphique de manière transparente.

### Rasterisation

La rasterisation est l'étape du pipeline graphique qui transforme les primitives géométriques en pixels à afficher à l'écran. Cette étape consiste à déterminer quels pixels sont couverts par les primitives et à calculer la couleur de chaque pixel en fonction de la couleur des sommets. La rasterisation est une opération complexe qui nécessite de calculer l'intersection des primitives avec les pixels de l'écran et d'appliquer des algorithmes de remplissage pour déterminer la couleur de chaque pixel.

Par exemple à partir des sommets de notre pyramide, la rasterisation va calculer les pixels couverts par les triangles formés par les sommets de façon à remplir les faces de la pyramide. Les pixels couverts par les triangles sont ensuite colorés en fonction de la couleur des sommets et de l'éclairage de la scène.

On dit que les primitives sont *rasterisées* lorsqu'elles sont transformées en *fragments*. Un fragment est un pixel potentiel qui doit être coloré.

### Fragment

À cette étape du pipeline graphique, nos sommets ont été convertis en des milliers de fragments. Chaque fragment correspond à un pixel de l'écran et doit être coloré. Le *fragment shader* est un autre programme écrit en langage de shader (GLSL) qui s'exécute sur chaque fragment de la primitive.

Le *fragment shader* est responsable de calculer la couleur finale de chaque pixel en fonction de la couleur des sommets, de la texture, de l'éclairage, et d'autres paramètres. Le programme retourne une couleur pour chaque fragment.

(donner un exemple concret avec les données de la caméra, de la lumière, une texture de brique, les normales des faces pour le calcul de l'éclairage. Donner un exemple en GLSL du fragment shader pour la pyramide.)


### Test de profondeur

Une fois les fragments calculés, ils subissent une série de tests pour déterminer s'ils doivent être affichés à l'écran. Le test de profondeur est un test qui compare la profondeur de chaque fragment avec la profondeur des fragments déjà affichés à l'écran. Si le fragment est plus proche de la caméra que les fragments déjà affichés, il est affiché à l'écran. Sinon, il est rejeté. Ce test est appelé le *Z-Test*.

Il existe également le *Stencil Test* qui permet de définir une zone de l'écran où les fragments peuvent être affichés. Cela permet de créer des effets spéciaux comme des ombres, des reflets, ou des effets de transparence.

Enfin le *Blending* permet de mélanger le fragment avec les fragments déjà affichés à l'écran. Cela permet de créer des effets de transparence, de luminosité, ou de flou.

### Écriture dans le framebuffer

Une fois que tous les tests et calculs ont été effectués, les fragments restants sont convertis en pixels et écrits dans le framebuffer (la mémoire vidéo). Le framebuffer contient les pixels qui seront envoyés à l’écran pour être affichés.


## OpenGL et Vulkan

[OpenGL](wiki:opengl), ou *Open Graphics Library*, est une API graphique multiplateforme utilisée principalement pour le rendu 2D et 3D dans des applications interactives. Elle est très répandue dans l'industrie des jeux vidéo, la visualisation scientifique, la modélisation 3D, et les simulations interactives. Conçue à l'origine pour permettre l'accélération graphique en temps réel via des cartes graphiques, OpenGL a marqué une révolution en facilitant le développement d'applications graphiques de haute performance tout en masquant les détails spécifiques au matériel.

OpenGL a été initialement développé par [Silicon Graphics, Inc.](wiki:silicon graphics) (SGI) en 1992. À l'époque, SGI dominait le marché des stations de travail graphiques de haute performance, utilisées dans des domaines comme la modélisation 3D et la simulation scientifique. SGI voulait une API standardisée qui permettrait aux développeurs de concevoir des applications indépendantes des spécificités matérielles des différentes cartes graphiques, tout en tirant parti de l'accélération matérielle.

Le but d'OpenGL était de fournir une interface simple et uniforme qui fonctionne sur divers systèmes d'exploitation (Windows, Linux, macOS) et plateformes matérielles, permettant ainsi une portabilité accrue des applications graphiques. Depuis, OpenGL a évolué au fil des années, en intégrant de nombreuses fonctionnalités graphiques modernes, comme les shaders et les buffers de trames.

Bien que d'autres API graphiques comme DirectX (pour Windows) ou Direct3D (pour les jeux vidéo) soient également très populaires, OpenGL reste une API de choix pour de nombreux développeurs en raison de sa portabilité, de sa flexibilité et de sa compatibilité avec un large éventail de matériels.

Néanmoins, certaines limitations ont conduit le Khronos Group qui gère OpenGL a développé [Vulkan](wiki:vulkan), une nouvelle API graphique et de calcul, publiée en 2016. Vulkan est considéré comme le successeur d'OpenGL et offre de nombreuses améliorations qui répondent aux besoins modernes des développeurs de jeux et d’applications graphiques.

Les jeux vidéos modernes comme FarCry, The Witcher 3, Red Dead Redemption 2, ou encore Cyberpunk 2077 utilisent des moteurs graphiques basés sur les API Vulkan ou DirectX 12 pour tirer parti des performances des cartes graphiques récentes.

En 2024, sur Windows, DirectX est l'API dominante. Néanmoins avec la technologie [DXVK](wiki:dxvk) qui est une couche de traduction permettant à des applications Vulkan de fonctionner avec DirectX 12.

### Principe de fonctionnement

OpenGL et Vulkan fonctionnent sur le principe de la programmation par états. Cela signifie que l'application configure l'état de l'API graphique en définissant des paramètres comme la couleur, la texture, la lumière, la perspective, etc. Une fois l'état configuré, l'application envoie des commandes graphiques à l'API pour dessiner des objets géométriques, des textures, des effets visuels, etc.

Ces API offrent une abstraction du matériel graphique sous-jacent, permettant aux développeurs de concevoir des applications graphiques sans se soucier des détails spécifiques à la carte graphique. En effet, une carte graphique contient des milliers de cœurs de calcul qui peuvent être programmés pour effectuer des calculs parallèles. Heureusement pour les développeurs, OpenGL et Vulkan fournissent des interfaces de haut niveau pour exploiter ces capacités de calcul sans avoir à gérer les détails complexes du matériel.

L'abstraction consiste principalement à ce que l'on nomme le *pipeline* graphique. Le pipeline graphique est une séquence d'étapes qui transforme les données géométriques en pixels affichés à l'écran. Ces étapes incluent la transformation des coordonnées, l'application des textures, l'éclairage, la perspective, et bien d'autres. Chaque étape du pipeline est configurable par l'application, permettant ainsi de personnaliser le rendu graphique en fonction des besoins.

### Carte graphique


### Pipeline

Le pipeline graphique d'OpenGL et de Vulkan est composé de plusieurs étapes, chacune effectuant une transformation spécifique sur les données graphiques. Voici les étapes principales du pipeline graphique :

## Bibliothèques graphiques de haut niveau

Pour faciliter le développement d'interfaces graphiques, des bibliothèques de plus haut niveau ont été créées. Celles-ci encapsulent les détails complexes du protocole X11 et fournissent des composants graphiques prêts à l'emploi, comme des boutons, des champs de texte, des boîtes de dialogue, et bien plus.

Sous Linux, l'une des bibliothèques graphiques les plus populaires est **GTK** (GIMP Toolkit). GTK est une bibliothèque open source écrite en C, largement utilisée pour développer des interfaces graphiques multiplateformes. Elle est notamment à la base de l'environnement de bureau GNOME et est utilisée dans des logiciels libres majeurs tels que GIMP et Inkscape.

GTK simplifie énormément la création d'interfaces graphiques grâce à une large gamme de widgets prêts à l'emploi et à une gestion intégrée des événements utilisateurs (comme les clics de souris ou les frappes clavier). Par exemple, créer une fenêtre avec des boutons, des listes déroulantes, ou des champs de texte est beaucoup plus simple et rapide qu'avec X11 pur.

```c
#include <gtk/gtk.h>

static void on_activate(GtkApplication *app, gpointer user_data) {
   GtkWidget *window = gtk_application_window_new(app);
   gtk_window_set_title(GTK_WINDOW(window), "Exemple GTK4");
   gtk_window_set_default_size(GTK_WINDOW(window), 100, 100);
   gtk_window_present(GTK_WINDOW(window));
}

int main(int argc, char **argv) {
   GtkApplication *app =
       gtk_application_new("org.gtk.example", G_APPLICATION_DEFAULT_FLAGS);
   g_signal_connect(app, "activate", G_CALLBACK(on_activate), NULL);
   int status = g_application_run(G_APPLICATION(app), argc, argv);
   g_object_unref(app);

   return status;
}
```

Cet exemple montre à quel point GTK rend les choses plus simples : une seule fonction pour ouvrir une fenêtre avec des paramètres de base.

## Autres bibliothèques graphiques

Selon les besoins de votre application, d'autres bibliothèques graphiques peuvent être plus adaptées. Par exemple, **Qt** est une bibliothèque graphique populaire pour le développement d'applications multiplateformes, notamment en C++. Il s'agit davantage d'un framework complet et des outils tiers pour le design interactif d'interfaces graphiques. De base QT (prononcé *cute*) est un framework objet, il n'est donc pas très adapté à la programmation en C.

Les bibliothèques les plus utilisées pour la programmation graphique en C sont les suivantes :

- SDL (Simple DirectMedia Layer)
- Allegro

## Principe de fonctionnement

La plupart des bibliothèques graphiques de haut niveau reposent sur les mêmes principes de base pour créer des interfaces graphiques interactives :

1. Initialisation : la bibliothèque est initialisée et les ressources nécessaires sont allouées.
2. Création de la fenêtre : une fenêtre graphique est créée avec les dimensions et les paramètres souhaités.
3. Création des composants graphiques : des widgets (boutons, champs de texte, etc.) sont ajoutés à la fenêtre.
4. Une boucle principale est lancée pour gérer les événements utilisateur (clics de souris, frappes clavier, etc.) et mettre à jour l'affichage en conséquence. Les évènements arrivent dans une file d'attente et sont traités un par un. L'écran est rafraîchi à chaque itération de la boucle pour afficher les changements.
5. Libération des ressources : une fois l'application terminée, les ressources allouées sont libérées et la fenêtre est fermée.

Lorsque différentes fenêtres sont nécessaires, le programme peut créer des contextes isolés comme des *threads* pour gérer les événements de chaque fenêtre. Cela permet de garder l'interface utilisateur réactive même si une fenêtre est bloquée par une opération longue.

## Allegro

[Allegro](https://liballeg.org/) est une bibliothèque graphique multiplateforme qui fournit des fonctionnalités pour la création de jeux vidéo et d'applications multimédia. Elle est plus orientée vers les jeux vidéo que les interfaces graphiques traditionnelles, mais elle peut être utilisée pour des applications plus générales. Allegro fournit des fonctionnalités pour la création de fenêtres, la gestion des événements utilisateur, le rendu graphique, la lecture de sons et de musiques, et bien plus encore. Elle est écrite en C et est compatible avec de nombreux systèmes d'exploitation, y compris Windows, Linux, macOS, iOS et Android et elle est utilisable sur de nombreux langages de programmation, dont le C.

Voici un exemple simple d'utilisation d'Allegro pour créer une fenêtre graphique avec un cercle rouge qui rebondit sur les bords de la fenêtre :

![Balle qui rebondit](/assets/images/allegro-ball.png)

```c
#include <allegro5/allegro.h>
#include <allegro5/allegro_image.h>
#include <allegro5/allegro_primitives.h>
#include <stdio.h>

const float FPS = 60.0;
const int SCREEN_W = 640;
const int SCREEN_H = 480;
const int BALL_SIZE = 20;

int main(int argc, char **argv) {
   float ball_x = SCREEN_W / 2.0 - BALL_SIZE / 2.0;
   float ball_y = SCREEN_H / 2.0 - BALL_SIZE / 2.0;
   float ball_dx = -4.0, ball_dy = 4.0;

   if (!al_init()) {
      fprintf(stderr, "Erreur d'initialisation d'Allegro.\n");
      return -1;
   }

   al_init_primitives_addon();
   al_install_keyboard();

   ALLEGRO_TIMER *timer = al_create_timer(1.0 / FPS);
   if (!timer) {
      fprintf(stderr, "Erreur de création du timer.\n");
      return -1;
   }

   ALLEGRO_DISPLAY *display = al_create_display(SCREEN_W, SCREEN_H);
   if (!display) {
      fprintf(stderr, "Erreur de création de la fenêtre.\n");
      al_destroy_timer(timer);
      return -1;
   }

   ALLEGRO_EVENT_QUEUE *event_queue = al_create_event_queue();
   if (!event_queue) {
      fprintf(stderr, "Erreur de création de la file d'événements.\n");
      al_destroy_display(display);
      al_destroy_timer(timer);
      return -1;
   }

   al_register_event_source(event_queue, al_get_display_event_source(display));
   al_register_event_source(event_queue, al_get_timer_event_source(timer));
   al_register_event_source(event_queue, al_get_keyboard_event_source());

   al_start_timer(timer);

   bool redraw = true;
   for (;;) {
      ALLEGRO_EVENT ev;
      al_wait_for_event(event_queue, &ev);

      if (ev.type == ALLEGRO_EVENT_TIMER) {
         // Move
         ball_x += ball_dx;
         ball_y += ball_dy;
         // Bounce
         if (ball_x <= 0 || ball_x >= SCREEN_W - BALL_SIZE) ball_dx = -ball_dx;
         if (ball_y <= 0 || ball_y >= SCREEN_H - BALL_SIZE) ball_dy = -ball_dy;
         redraw = true;
      } else if (ev.type == ALLEGRO_EVENT_DISPLAY_CLOSE)
         break;

      if (redraw && al_is_event_queue_empty(event_queue)) {
         redraw = false;
         al_clear_to_color(al_map_rgb(0, 0, 0));
         al_draw_filled_circle(ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2,
                               BALL_SIZE / 2, al_map_rgb(255, 0, 0));
         al_flip_display();  // Refresh
      }
   }

   // Free resources
   al_destroy_timer(timer);
   al_destroy_display(display);
   al_destroy_event_queue(event_queue);
}
```

## Conclusion

En résumé, bien que X11 soit le fondement de l'affichage graphique sous Linux, son utilisation directe est rarement nécessaire pour les développeurs modernes. Des bibliothèques comme GTK permettent de se concentrer sur la logique de l'application et l'expérience utilisateur, tout en masquant les détails techniques sous-jacents. Il est recommandé d'utiliser ces outils de plus haut niveau pour créer des interfaces graphiques complètes, flexibles et ergonomiques.
