# OpenGL

## Versions

On distingues plusieurs versions d'OpenGL :

OpenGL 1.0 : Première version d'OpenGL sortie en 1992.
OpenGL 2.0 : Version sortie en 2004 qui introduit les shaders.
OpenGL 3.0 : Version sortie en 2008 qui introduit les shaders de géométrie.
OpenGL 4.0 : Version sortie en 2010 qui introduit les shaders de tessellation.
OpenGL 4.3 : Version sortie en 2012 qui introduit les shaders de calcul.
OpenGL 4.6 : Version sortie en 2017 qui introduit les shaders de tâches.

OpenGL ES 2.0 : Version d'OpenGL pour les systèmes embarqués.
Vulkan : API graphique bas niveau qui succède à OpenGL.

Wayland : Protocole de communication entre le serveur et les clients.
X11 : Protocole de communication entre le serveur et les clients.

## Fonctionnement

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

Une fois les primitives assemblées, les sommets sont traités par le *vertex shader*. Le *vertex shader* est un petit programme écrit en langage de shader (comme [GLSL](https://fr.wikipedia.org/wiki/OpenGL_Shading_Language) pour OpenGL ou HLSL pour DirectX sous Windows) qui s'exécute sur chaque sommet de la primitive. Le GLSL est un langage très proche du C mais beaucoup plus limité. En revanche il est capable de tirer parti des capacités de calcul parallèle des cartes graphiques et donc d'être très performant pour certaines opérations.

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

[OpenGL](https://fr.wikipedia.org/wiki/OpenGL), ou *Open Graphics Library*, est une API graphique multiplateforme utilisée principalement pour le rendu 2D et 3D dans des applications interactives. Elle est très répandue dans l'industrie des jeux vidéo, la visualisation scientifique, la modélisation 3D, et les simulations interactives. Conçue à l'origine pour permettre l'accélération graphique en temps réel via des cartes graphiques, OpenGL a marqué une révolution en facilitant le développement d'applications graphiques de haute performance tout en masquant les détails spécifiques au matériel.

OpenGL a été initialement développé par [Silicon Graphics, Inc.](https://fr.wikipedia.org/wiki/Silicon_Graphics) (SGI) en 1992. À l'époque, SGI dominait le marché des stations de travail graphiques de haute performance, utilisées dans des domaines comme la modélisation 3D et la simulation scientifique. SGI voulait une API standardisée qui permettrait aux développeurs de concevoir des applications indépendantes des spécificités matérielles des différentes cartes graphiques, tout en tirant parti de l'accélération matérielle.

Le but d'OpenGL était de fournir une interface simple et uniforme qui fonctionne sur divers systèmes d'exploitation (Windows, Linux, macOS) et plateformes matérielles, permettant ainsi une portabilité accrue des applications graphiques. Depuis, OpenGL a évolué au fil des années, en intégrant de nombreuses fonctionnalités graphiques modernes, comme les shaders et les buffers de trames.

Bien que d'autres API graphiques comme DirectX (pour Windows) ou Direct3D (pour les jeux vidéo) soient également très populaires, OpenGL reste une API de choix pour de nombreux développeurs en raison de sa portabilité, de sa flexibilité et de sa compatibilité avec un large éventail de matériels.

Néanmoins, certaines limitations ont conduit le Khronos Group qui gère OpenGL a développé [Vulkan](https://fr.wikipedia.org/wiki/Vulkan_(API)), une nouvelle API graphique et de calcul, publiée en 2016. Vulkan est considéré comme le successeur d'OpenGL et offre de nombreuses améliorations qui répondent aux besoins modernes des développeurs de jeux et d’applications graphiques.

Les jeux vidéos modernes comme FarCry, The Witcher 3, Red Dead Redemption 2, ou encore Cyberpunk 2077 utilisent des moteurs graphiques basés sur les API Vulkan ou DirectX 12 pour tirer parti des performances des cartes graphiques récentes.

En 2024, sur Windows, DirectX est l'API dominante. Néanmoins avec la technologie [DXVK](https://github.com/doitsujin/dxvk) qui est une couche de traduction permettant à des applications Vulkan de fonctionner avec DirectX 12.

### Principe de fonctionnement

OpenGL et Vulkan fonctionnent sur le principe de la programmation par états. Cela signifie que l'application configure l'état de l'API graphique en définissant des paramètres comme la couleur, la texture, la lumière, la perspective, etc. Une fois l'état configuré, l'application envoie des commandes graphiques à l'API pour dessiner des objets géométriques, des textures, des effets visuels, etc.

Ces API offrent une abstraction du matériel graphique sous-jacent, permettant aux développeurs de concevoir des applications graphiques sans se soucier des détails spécifiques à la carte graphique. En effet, une carte graphique contient des milliers de cœurs de calcul qui peuvent être programmés pour effectuer des calculs parallèles. Heureusement pour les développeurs, OpenGL et Vulkan fournissent des interfaces de haut niveau pour exploiter ces capacités de calcul sans avoir à gérer les détails complexes du matériel.

L'abstraction consiste principalement à ce que l'on nomme le *pipeline* graphique. Le pipeline graphique est une séquence d'étapes qui transforme les données géométriques en pixels affichés à l'écran. Ces étapes incluent la transformation des coordonnées, l'application des textures, l'éclairage, la perspective, et bien d'autres. Chaque étape du pipeline est configurable par l'application, permettant ainsi de personnaliser le rendu graphique en fonction des besoins.

### Carte graphique


### Pipeline

Le pipeline graphique d'OpenGL et de Vulkan est composé de plusieurs étapes, chacune effectuant une transformation spécifique sur les données graphiques. Voici les étapes principales du pipeline graphique :


## Double Buffer

OpenGL utilise un double buffer pour afficher les images. Le double buffer est composé de deux buffers : un buffer de dessin et un buffer d'affichage. Le buffer de dessin est utilisé pour dessiner les images et le buffer d'affichage est utilisé pour afficher les images. Lorsque l'image est dessinée dans le buffer de dessin, elle est ensuite copiée dans le buffer d'affichage. Cela permet d'éviter les problèmes de scintillement. C'est une pratique très courante dans les applications graphiques.

## Vsync

La synchronisation verticale (Vsync) est une technique qui permet de synchroniser le taux de rafraîchissement de l'écran avec le taux de rafraîchissement de l'application. Cela permet d'éviter les problèmes de déchirure d'écran. La synchronisation verticale est généralement activée par défaut dans les applications graphiques.

## GFLW

La bibliothèque GLFW est une bibliothèque C qui permet de créer des fenêtres avec OpenGL. Elle est compatible avec OpenGL ES et Vulkan. Elle est utilisée pour créer des fenêtres et gérer les événements de fenêtre. On pourrait très bien utiliser GTK néanmoins GLFW est plus simple et plus adapté à OpenGL.

Pour installer GLFW sur Ubuntu, il suffit d'installer la biblothèque avec les fichiers d'en-tête :

```bash
sudo apt install libglfw3-dev
```

Pour compiler un programme avec GLFW, il est nécessaire de lier la bibliothèque avec le programme. Pour cela, il suffit d'ajouter l'option `-lglfw` à la commande de compilation.

Un programme simple qui crée une fenêtre avec GLFW :

```c
#include <GLFW/glfw3.h>

int main() {
   if (!glfwInit()) return -1;
   GLFWwindow* window = glfwCreateWindow(800, 400, "Window", NULL, NULL);
   if (!window) {
      glfwTerminate();
      return -2;
   }
   glfwMakeContextCurrent(window);
   while (!glfwWindowShouldClose(window)) {
      glfwSwapBuffers(window);
      glfwPollEvents();
   }
}
```

On observe que la bibliothèque est tout d'abord initialisée avec la fonction `glfwInit()`. Ensuite, une fenêtre est créée avec un titre. Les deux derniers paramètres laissés à `NULL` sont des pointeurs sur le moniteur sur laquelle la fenêtre est affichée `GLFWmonitor` et la fenêtre du parent `GLFWwindow` utilisée dans le cas d'une application multi-fenêtres. Dans notre cas on laisse ces paramètres à `NULL` car nous n'avons pas besoin de ces fonctionnalités.

Si la fenêtre n'a pas pu être créée, le programme se termine. Sinon, la fenêtre est affichée avec la fonction `glfwMakeContextCurrent(window)`.

Enfin, une boucle est créée pour afficher la fenêtre tant que l'utilisateur ne la ferme pas. La fonction `glfwSwapBuffers(window)` permet de copier le contenu du buffer de dessin dans le buffer d'affichage. La fonction `glfwPollEvents()` permet de gérer les événements de fenêtre.

Le grand avantage de ce programme est qu'il est portable. Il fonctionne sur Windows, Linux et MacOS.

GLFW permet également de gérer les joystick et gamepads, les évènements du clavier ou de la souris ainsi que le curseurs de la souris. Cela permet de créer des applications graphiques interactives sans nécessité d'avoir recours à d'autres bibliothèques.

Nous n'approfonfirons pas plus GLFW dans ce cours néanmoins, vous avez toujours la possibilité de consulter la documentation officielle de GLFW qui est très complète.

## GLEW

La bibliothèque GLEW (*OpenGL Extension Wrangler Library*) est une bibliothèque qui facilite le chargement des extensions OpenGL. OpenGL a un ensemble de fonctionnalités qui peut varier selon le matériel graphique et le système d'exploitation, et GLEW est utilisé pour accéder à ces fonctionnalités de manière portable. En sommes, la bibliothèque permet de charger dynamiquement des fonctions OpenGL qui ne sont pas directement accessibles par le système, surtout pour les versions modernes d'OpenGL.

Pour disposer d'un contexte OpenGL utilsable nous devons compléter notre programme précédent avec GLEW. D'abord des messages d'erreurs plus explicites sont affichés en cas d'erreur. Certains paramètres sont ajoutés pour activer l'anticrénelage et spécifier la version d'OpenGL que nous voulons utiliser.

Dans la boucle principale, la touche echape permet maintenant de quitter le programme.

```c
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <stdbool.h>
#include <stdio.h>

int main() {
   if (!glfwInit()) {
      fprintf(stderr, "Failed to initialize GLFW\n");
      return -1;
   }
   glfwWindowHint(GLFW_SAMPLES, 4);                // 4x antialiasing
   glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);  // We want OpenGL 3.3
   glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
   glfwWindowHint(GLFW_OPENGL_PROFILE,
                  GLFW_OPENGL_CORE_PROFILE);  // We don't want the old OpenGL

   // Open a window and create its OpenGL context
   GLFWwindow* window = glfwCreateWindow(800, 400, "OpenGL", NULL, NULL);
   if (window == NULL) {
      fprintf(stderr, "Error: Failed to open GLFW window.\n");
      glfwTerminate();
      return -1;
   }
   glfwMakeContextCurrent(window);
   if (glewInit() != GLEW_OK) {
      fprintf(stderr, "Error: Failed to initialize GLEW\n");
      return -1;
   }
   glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
   do {
      glClear(GL_COLOR_BUFFER_BIT);

      // ...

      glfwSwapBuffers(window);
      glfwPollEvents();
   } while (glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS &&
            glfwWindowShouldClose(window) == 0);
}
```

## GLUT

GLUT (*OpenGL Utility Toolkit*) est une bibliothèque qui facilite la création de fenêtres OpenGL. Elle est plus ancienne que GLFW et elle est moins utilisée. GLUT est une bibliothèque portable qui permet de créer des fenêtres OpenGL sur Windows, Linux et MacOS. Elle permet également de gérer les événements de fenêtre, les événements de clavier et de souris, et les événements de redimensionnement de fenêtre. Préférez GLFW à GLUT pour vos projets OpenGL.

[](){#opengl-coordinates}

## Coordonnées

Le système de coordonnées d'OpenGL est un peu particulier. L'origine du système de coordonnées est au centre de la fenêtre. Les coordonnées x et y vont de -1 à 1. Les coordonnées z vont de -1 à 1. Les coordonnées x et y sont en 2D et la coordonnée z est en 3D.

On notera qu'il n'y a pas de notion de pixels dans le système de coordonnées d'OpenGL car les coordonnées sont normalisées et représentée par un flottant 32-bit. Nous verrons que pour dessiner des formes géométriques, la projection doit être ajustée car si la fenêtre n'est pas carrée, les formes géométriques seront déformées.

Le $x$ positif est à droite, le $y$ positif est en haut et le $z$ positif est vers l'observateur. C'est la règle de la main droite issue de la physique où l'axe $z$ est la direction du pouce, l'axe $x$ est l'index et l'axe $y$ est le majeur.

Si nous souhaitons dessiner un triangle isocèle centré dans l'espace, nous devons définir les coordonnées des sommets du triangle.

```c
static const GLfloat verticles[] = {
   -1.0f, -1.0f, 0.0f, // Bottom left
   1.0f,  -1.0f, 0.0f, // Bottom right
   0.0f,  1.0f,  0.0f, // Top
};
```

## Vertex

Un vertex est un sommet dans l'espace 3D. Un vertex est défini par ses coordonnées $x$, $y$ et $z$ mais il peut également avoir d'autres attributs comme la couleur, la normale, la texture, etc. La normale est un vecteur perpendiculaire à la surface du sommet, c'est une information importante pour les calculs d'éclairage. En effet, une surface va refléter la lumière différemment selon l'angle d'incidence de la lumière. OpenGL est assez flexible
pour définir les attributs d'un vertex.

Définissons les primitives de base d'un vertex. Il peut contenir un point :

```c
typedef union Point2D {
   struct {
      GLfloat x;
      GLfloat y;
   };
   GLfloat data[2];
} Point2D;

typedef union Point3D {
   struct {
      GLfloat x;
      GLfloat y;
      GLfloat z;
   };
   GLfloat data[3];
} Point3D;
```

Il peut contenir une normale qui est un vecteur. Formellement un vecteur n'est pas un point mais il peut être représenté par un point :

```c
typedef Point3D Vector3D;
```

Il peut contenir une couleur. En OpenGL une couleur peut être représentée par un vecteur de trois composantes rouge, vert et bleu, ou par un vecteur de quatre composantes rouge, vert, bleu et alpha pour gérer la transparence :

```c
typedef union ColorRGB {
   struct {
      GLfloat r;
      GLfloat g;
      GLfloat b;
   };
   GLfloat data[3];
} ColorRGB;

typedef union ColorRGBA {
   struct {
      GLfloat r;
      GLfloat g;
      GLfloat b;
      GLfloat a;
   };
   GLfloat data[4];
} ColorRGBA;
```

Enfin, on peut imaginer différents types de vertex:

```c
typedef union VertexA {
   struct {
      Point3D position;
      ColorRGB color;
      Vector3D normal;
      Point2D texture_coordinates;
   };
   GLfloat data[11];
} VertexA;

typedef union VertexB {
   struct {
      Point2D position;
   };
   GLfloat data[2];
} VertexB;

typedef union VertexC {
   struct {
      ColorRGBA color;
      Vector3D normal;
      Point3D position;
   };
   GLfloat data[10];
} VertexC;
```

Une chose est sûre, un vertex est un tableau de flottants 32-bits et il est rarement seul. Il est souvent regroupé dans un tableau de vertex pour former un objet géométrique.

Comme l'ordre des attributs d'un vertex configurable, il est nécessaire d'informer OpenGL de la manière dont les attributs sont structurés. Pour configurer notre `VertexC` nous utiliserons par exemple :

```c
// Position
glEnableVertexAttribArray(0);
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(VertexC),
    (GLvoid*)(6 * sizeof(GLfloat)));

// Color
glEnableVertexAttribArray(1);
glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, sizeof(VertexC),
    (GLvoid*)(0 * sizeof(GLfloat)));

// Normal
glEnableVertexAttribArray(2);
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sizeof(VertexC),
    (GLvoid*)(3 * sizeof(GLfloat)));
```

Chaque vertex à donc 3 attributs : la position, la couleur et la normale. L'attribut 0 est la couleur, l'attribut 1 est la normale et l'attribut 2 est la position. J'ai volontairement inversé l'ordre des attributs pour montrer qu'il n'a pas d'importance, vous faites comme vous voulez.

Le dernier argument de `glVertexAttribPointer` peut paraitre étrange. Pourquoi ne s'agit-il pas d'un `uintptr_t` mais d'un `GLvoid*` ? C'est une question de compatibilité avec les anciennes versions d'OpenGL. `GLvoid*` est un pointeur générique qui peut pointer sur n'importe quel type de données. C'est en réalité un `void*` en C. Néanmoins, ce n'est pas vraiment un pointeur non plus car il ne peut pas être déréférencé. Il y a parfois des questions d'héritage dans les API ou cette dernière à évoluée mais que pour des raisons de compatibilité, certaines décisions historiques sont conservées.

## VBO

Un VBO (*Vertex Buffer Object*) est un espace mémoire qui peut être utilisé pour stocker des données de sommets. C'est en général cet objet qui est partagé entre le CPU et le GPU. Évidemment plus le buffer est grand plus le temps de transfert peut être long, surtout si l'opération est répétée à chaque image.

Avant de pouvoir utiliser un tel buffer il faut en faire la requête à OpenGL. Dans l'exemple suivant on demande à OpenGL de nous allouer un seul buffer :

```c
Gluint vbo = 0;
glGenBuffers(1, &vbo);
```

La variable `vbo` contiendra l'identifiant du buffer alloué par OpenGL. Une fois alloué il sera important plus tard d'utiliser `glDeleteBuffers(1, &vbo)` pour libérer la mémoire allouée dynamiquement.

Afin d'éviter de passer l'identifiant du `vbo` à toutes les fonctions OpenGL, qui traitent les buffers, la stratégie adoptée est de lier le buffer à un contexte OpenGL. Cela se fait avec la fonction `glBindBuffer` :

```c
glBindBuffer(GL_ARRAY_BUFFER, vbo);
```

Ici on indique que le `vbo` créé sera utilisé pour stocker des `GL_ARRAY_BUFFER`, c'est-à-dire des données de sommets, et que ce `vbo` sera désormais le buffer actif pour toutes les fonctions du type `glBufferData`, `glBufferSubData`, `glMapBuffer`, etc. Et ce jusqu'à ce qu'un autre buffer soit lié ou que le buffer soit supprimé.

[Plus haut][opengl-coordinates], nous avions défini les coordonnées d'un triangle en 3 dimensions. Il est maintenant temps de les envoyer à la carte graphique. Pour cela nous utilisons la fonction `glBufferData` après que le buffer ait été lié au contexte :

```c
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
```

La constante `GL_STATIC_DRAW` indique à OpenGL que les données ne changeront pas souvent. Il existe d'autres constantes pour indiquer à OpenGL que les données seront modifiées fréquemment ou rarement. Cela permet à OpenGL d'optimiser le stockage des données en mémoire.

## VAO

Nous avons vu plus haut qu'un vertex peut être plus ou moins complexe en fonction des attributs qu'il contient. Un VAO (*Vertex Array Object*) est un tableau qui stocke l'état des attributs de vertex. Nous avons vu également que ces attributs doivent être configurés pour être utilisés par OpenGL. C'est le rôle du VAO de stocker cette configuration.

De la même manière que pour le VBO, on demande à OpenGL de nous allouer un VAO, puis on le lie au contexte actif. Ensuite on peut configurer les attributs du vertex et les lier au VBO.

```c
Gluint vao = 0;
glGenVertexArrays(1, &vao);
glBindVertexArray(vao);
```

Comme notre triangle ne contient qu'une position en 3D, nous devons configurer l'attribut 0 pour qu'il pointe vers la position du vertex.

```c
glEnableVertexAttribArray(0);
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
    3 * sizeof(GLfloat), (GLvoid*)0);
```

Ici on indique à OpenGL que l'attribut 0 est un vecteur de 3 flottants, que les données sont de type `GL_FLOAT`, que les données ne sont pas normalisées, que chaque vertex est séparé de 3 flottants et que le premier vertex commence à l'indice 0.

## Shader

Un shader est un programme qui s'exécute sur la carte graphique. Il est écrit en langage GLSL (*OpenGL Shading Language*) pour OpenGL ou en HLSL (*High-Level Shading Language*) pour DirectX. Comme pour un programme en C, un shader doit être compilé avant d'être exécuté mais contrairement à un programme en C il sera compilé à chaque exécution du programme. Cela permet de s'adapter à la configuration matérielle de la carte graphique car l'architecture des cartes graphiques peut varier d'un PC à l'autre.

Le GLSL est très similaire au C du point de vue de la syntaxe mais il est beaucoup plus limité. Il n'y a pas de pointeurs, pas de structures, pas de fonctions récursives, pas de boucles infinies, pas de gestion de la mémoire, etc. En effet, les processeurs graphiques sont des processeurs spécialisés qui n'ont pas besoin de ces fonctionnalités. Ils sont très simples mais très nombreux.

Dans une carte graphique de type GTX 3090 sortie en 2020 et capable de faire tourner un jeu comme Cyberpunk 2077 en 4K, il y a 82 *streaming multiprocessors* ou **SMs**. Chaque SM contient 128 CUDA cores et donc la carte graphique contient 10496 CUDA cores. Chaque CUDA core peut exécuter différent type de shaders : vertex, tessellation, geometry, fragment, etc. En outre, cette carte graphique tourne à 1.7 GHz, c'est à dire que chaque CUDA core peut exécuter 1.7 milliard d'instructions par seconde.

En d'autres termes, un shader GLSL de 10 instructions qui sera exécuté pour chaque pixel d'un écran de 3840x2160 pixels sera exécuté en :

$$
\frac{x \times y}{\text{cores}} \times \text{instructions} \times \frac{1}{\text{freq}}
\frac{3840 \times 2160}{10496} \times 10 \times \frac{1}{1.7 \times 10^9} = 4\mu s
$$

Le premier shader du *pipeline* graphique est le vertex shader. Il est exécuté pour chaque vertex d'un objet géométrique. Il sera utilisé pour transformer les coordonnées des sommets du modèle en coordonnées de l'écran car rappelez-vous que les coordonnées des sommets sont normalisées.

Un shader de manière générique possède des entrées et des sorties. Les entrées sont les données que le shader reçoit et les sorties sont les données que le shader transmera à l'étape suivante du *pipeline* graphique. En plus des entrées et des sorties, un shader peut avoir des *uniformes*. Une *uniforme* est une variable du programme principal qui est constante pour tous les vertex ou tous les fragments au même instant de rendu. Une uniforme est typiquement utilisée pour passer des matrices de transformation (rotation, translation, échelle).

Il faut également noter que le langage GLSL possède des types un peu différents de C. Il existe des types de base comme `int`, `float`, `vec2`, `vec3`, `vec4`, `mat2`, `mat3`, `mat4`, etc. Il existe également des types de structures et des types de tableaux. Un `vec3` est un vecteur de 3 flottants, un `mat4` est une matrice de 4x4 flottants.

Enfin, le langage GLSL à beaucoup évolué depuis sa première version en 2004. La manière de transmettre les entrées et les sorties d'un shader a beaucoup changé. Il est maintenant possible de déclarer les entrées et les sorties d'un shader avec des mots-clés comme `in`, `out`, `uniform`, `layout`, etc.

Le vertex shader le plus typique que l'on puisse écrire est le suivant :

```c
#version 330 core

layout(location = 0) in vec3 position;

void main() {
   gl_Position = vec4(position, 1.0);
}
```

Ce shader prend en entrée un vecteur de 3 flottants `position` issue de l'attribut 0 du vertex. Il transforme ce vecteur en un vecteur de 4 flottants `gl_Position` qui est la position du vertex dans l'espace de l'écran. La quatrième coordonnée est liée à l'utlisation de coordonnées homogènes dans les transformations grpahiques en 3D. Cette quatrième coordonnée nommée `w` a un rôle crucial dans les transformations géométriques. En mathématiques et en infographie, les coordonnées homogènes permettent d'utiliser des transformations affines (comme la translation, la rotation, l'échelle) et des transformations projectives (comme la projection en perspective) de manière plus simple et uniforme. Lors d'une transformation projective, la quatrième coordonnée est utilisée pour déterminer la profondeur du vertex dans l'espace 3D. Elle permet de simuler l'effet de rapetissement des objets éloignés dans une scène 3D. Pour une scène en 2D ou une scène en 3D sans perspective, la quatrième coordonnée est égale à `1.0f`.

Le deuxième type de shader dont nous aurons besoin est nommé *fragment shader*. Un fragment est un élément de base d'un objet géométrique qui contient une information de couleur mais aussi de la position sur l'écran, la coordonnée d'une texture, des valeurs d'interpolation ou même une information de profondeur en $z$. Chaque fragment représente une peitite portion d'une primitive (triangle, carré, cercle, etc.) souvent associée à un pixel de l'écran. Le fragment shader le plus simple que l'on puisse écrire est le suivant :

```c
#version 330 core

out vec4 FragColor;

void main() {
   FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
```

Pour chaque fragment, on retourne la couleur $[1.0, 1.0, 1.0, 1.0]$ qui est le blanc. Donc chaque pixel contenu dans la primitive dessinée sera blanc. Il conviendra d'avoir du noir pour la couleur de fond de la fenêtre pour voir notre triangle.

Maintenant que nous avons nos deux shaders, il est temps de les compiler et de les lier à un programme OpenGL. Un programme OpenGL est un ensemble de shaders qui sont liés ensemble pour former un programme graphique. Un programme graphique est un ensemble de shaders qui sont exécutés à chaque image pour dessiner des primitives.

Si nous reprenons notre triangle précédent, le vertex shader transformera les coordonnées du triangle en coordonnées de l'écran sans les déformer et le fragment shader colorera chaque pixel du triangle en blanc.

Tout d'abord chaque shader est stocké sous forme d'une chaîne de caractères, puis chaque shader est compilé et enfin les shaders sont liés ensemble pour former un programme graphique :

```c
const char* vertexShaderSource =
    "#version 330 core\n"
    "layout (location = 0) in vec3 position;\n"
    "void main() {\n"
    "    gl_Position = vec4(position, 1.0);\n"
    "}\n";

const char* fragmentShaderSource =
    "#version 330 core\n"
    "out vec4 FragColor;\n"
    "void main() { FragColor = vec4(1.0, 1.0, 1.0, 1.0); }\n";

GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
glCompileShader(vertexShader);

GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
glCompileShader(fragmentShader);

GLuint shaderProgram = glCreateProgram();
glAttachShader(shaderProgram, vertexShader);
glAttachShader(shaderProgram, fragmentShader);
glLinkProgram(shaderProgram);
glUseProgram(shaderProgram);

glDeleteShader(vertexShader);
glDeleteShader(fragmentShader);
```

Notez que cette méthode est très basique et ne gère pas les erreurs de compilation ou de liaison des shaders, nous verrons plus tard un exemple plus complet.

## Rendu

Si vous êtes arrivé jusqu'ici, vous avez compris que nous utilisons `GLFW` pour créer une fenêtre graphique et `GLEW` pour charger les extensions OpenGL. Nous avons compris la notion de double buffer et de coordonnées normalisées avec la règle de la main droite. Les notions de VBO et de VAO n'ont plus de secret pour vous et vous avez compris l'utilité d'un vertex shader et d'un fragment shader.

Il est temps de dessiner notre triangle.

```c
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <stdbool.h>
#include <stdio.h>

static const GLfloat vertices[] = {
    -1.0f, -1.0f, 0.0f,  // Bottom left
    1.0f,  -1.0f, 0.0f,  // Bottom right
    0.0f,  1.0f,  0.0f,  // Top
};

const char* vertexShaderSource =
    "#version 330 core\n"
    "layout (location = 0) in vec3 position;\n"
    "void main() {\n"
    "    gl_Position = vec4(position, 1.0);\n"
    "}\n";

const char* fragmentShaderSource =
    "#version 330 core\n"
    "out vec4 FragColor;\n"
    "void main() { FragColor = vec4(1.0, 1.0, 1.0, 1.0); }\n";

int main() {
   // Initialise GLFW
   if (!glfwInit()) {
      fprintf(stderr, "Failed to initialize GLFW\n");
      return -1;
   }
   glfwWindowHint(GLFW_SAMPLES, 4);                // 4x antialiasing
   glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);  // We want OpenGL 3.3
   glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
   glfwWindowHint(GLFW_OPENGL_PROFILE,
                  GLFW_OPENGL_CORE_PROFILE);  // We don't want the old OpenGL

   // Open a window and create its OpenGL context
   GLFWwindow* window =
       glfwCreateWindow(800, 400, "White Triangle", NULL, NULL);
   if (window == NULL) {
      fprintf(stderr, "Error: Failed to open GLFW window.\n");
      glfwTerminate();
      return -1;
   }
   glfwMakeContextCurrent(window);
   if (glewInit() != GLEW_OK) {
      fprintf(stderr, "Error: Failed to initialize GLEW\n");
      return -1;
   }
   glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);

   // Compile and link shaders
   unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
   glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
   glCompileShader(vertexShader);

   unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
   glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
   glCompileShader(fragmentShader);

   unsigned int shaderProgram = glCreateProgram();
   glAttachShader(shaderProgram, vertexShader);
   glAttachShader(shaderProgram, fragmentShader);
   glLinkProgram(shaderProgram);
   glUseProgram(shaderProgram);

   glDeleteShader(vertexShader);
   glDeleteShader(fragmentShader);

   // Setup VAO/VBO
   unsigned int VBO = 0, VAO = 0;
   glGenVertexArrays(1, &VAO);
   glGenBuffers(1, &VBO);
   glBindVertexArray(VAO);

   glBindBuffer(GL_ARRAY_BUFFER, VBO);
   glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

   glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
   glEnableVertexAttribArray(0);

   //  Main loop
   do {
      glClear(GL_COLOR_BUFFER_BIT);
      glDrawArrays(GL_TRIANGLES, 0, 3);
      glfwSwapBuffers(window);
      glfwPollEvents();
   } while (glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS &&
            glfwWindowShouldClose(window) == 0);
}
```

Après compilation avec la commande suivante, on obtient un triangle blanc comme illustré ci-dessous

```bash
gcc -o triangle triangle.c -lglfw -lGLEW -lGL -lm
```

![Triangle Blanc](/assets/images/triangle1.png)

## Matrices

Le risque avec l'OpenGL bas niveau c'est qu'à un moment donné on se retrouve à devoir gérer des matrices de transformation et donc de faire des maths. Si nous voulons rendre notre exemple plus interfactif, nous pourrions par exemple ajouter une rotation au triangle, d'abord dans le plan $xy$ puis plus tard en 3D.

Pour mémoire, en mathémathique, un vecteur est une matrice de $n \times 1$ soit avec une seule colonne, tandiqu'un point est une matrice de $1 \times n$ soit avec une seule ligne. La matrice qui n'a pas d'effet sur un vecteur est la matrice identité. La matrice identité est une matrice carrée de taille $n \times n$ avec des $1$ sur la diagonale principale et des $0$ ailleurs. La matrice identité est notée $I_n$. En 3D nous avons donc:

$$
I_3 = \begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

Une matrice de rotation en 3D est une matrice qui permet de faire tourner un vecteur autour d'un axe. Il existe trois types de rotation en 3D : la rotation autour de l'axe $x$, la rotation autour de l'axe $y$ et la rotation autour de l'axe $z$. La rotation autour de l'axe $x$ est donnée par la matrice :

$$
R_x(\theta) = \begin{bmatrix}
1 & 0 & 0 \\
0 & \cos(\theta) & -\sin(\theta) \\
0 & \sin(\theta) & \cos(\theta)
\end{bmatrix}
$$

Ces deux matrices sont des matrices 3x3. Dans OpenGL on utilise des coordonnées homogènes pour les transformations géométriques. Une matrice de transformation homogène est une matrice 4x4 qui permet de faire des transformations affines et projectives en 3D. La matrice de rotation peut être réécrite de la forme :

$$
R_x(\theta) = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & \cos(\theta) & -\sin(\theta) & 0 \\
0 & \sin(\theta) & \cos(\theta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

On peut facilement calculer une matrice de rotation en implémentant une fonction en C :

```c
void identityMatrix(GLfloat matrix[16]) {
   for (int i = 0; i < 16; i++) matrix[i] = 0;
   matrix[0] = 1;
   matrix[5] = 1;
   matrix[10] = 1;
   matrix[15] = 1;
}

void rotationMatrix(GLfloat matrix[16], GLfloat angle, GLfloat x, GLfloat y, GLfloat z) {
   GLfloat c = cos(angle);
   GLfloat s = sin(angle);
   GLfloat t = 1 - c;
   matrix[0] = x * x * t + c;
   matrix[1] = x * y * t - z * s;
   matrix[2] = x * z * t + y * s;
   matrix[3] = 0;
   matrix[4] = y * x * t + z * s;
   matrix[5] = y * y * t + c;
   matrix[6] = y * z * t - x * s;
   matrix[7] = 0;
   matrix[8] = x * z * t - y * s;
   matrix[9] = y * z * t + x * s;
   matrix[10] = z * z * t + c;
   matrix[11] = 0;
   matrix[12] = 0;
   matrix[13] = 0;
   matrix[14] = 0;
   matrix[15] = 1;
}
```

Une manière plus simple est de faire appel à une bibliothèque de mathématiques comme `CGLM` que vous pouvez installer avec la commande suivante :

```bash
sudo apt-get install libcglm-dev
```

### Model View Projection

La matrice de transformation homogène la plus courante est la matrice de transformation *Model View Projection* ou *MVP*. La matrice *Model* est la matrice qui transforme les coordonnées du modèle en coordonnées du monde. La matrice *View* est la matrice qui transforme les coordonnées du monde en coordonnées de la caméra. La matrice *Projection* est la matrice qui transforme les coordonnées de la caméra en coordonnées de l'écran.

Souvenez-vous dans Futurama lorsque Cubert Farnsworth réalise comment fonctionne les moteurs du vaisseau spatial de son père. Il dit :

> I understand how the engines work now. It came to me in a dream. The engines don't move the ship at all. The ship stays where it is and the engines move the universe around it.

En français

> J'ai compris comment fonctionnent les moteurs maintenant. C'est venu à moi dans un rêve. Les moteurs ne déplacent pas le vaisseau du tout. Le vaisseau reste où il est et les moteurs déplacent l'univers autour de lui.

En OpenGL il n'y pas de caméra qui se déplace, de longueur focale ou de distance de vue. C'est l'univers qui se déplace autour de la caméra. Cette dernière reste fixe avec ses coordonnées $(0, 0, 0)$ et son orientation $(0, 0, -1)$.

## Transformation

Ce n'est pas très joli d'avoir chaque sommet du triangle collé au bord de la fenêtre. Nous allons donc déplacer le triangle au centre de la fenêtre. Pour cela nous allons utiliser une matrice de transformation. On peut définir par exemple que le triangle fera 70% de la hauteur de la fenêtre et son rapport largeur/hauteur sera de 1.0. Vous l'avez compris on utilisera une matrice de transformation homogène qui sera appliquée par le *vertex shader* à chaque sommet du triangle.

Un autre problème est que les dimensions de la fenêtre *viewport* peuvent changer si l'utilisateur décide de la redimensionner. Or, comme les coordonnées des sommets du triangle sont normalisées, dans le cas d'une fenêtre deux fois plus large que haute. $1.0$ en $x$ sera deux fois plus grand que $1.0$ en $y$.

Pour éviter cela, une manière est d'utiliser une matrice de projection  orthographique homogène définie comme :

$$
\begin{bmatrix}
\frac{2}{width} & 0 & 0 & 0 \\
0 & \frac{2}{height} & 0 & 0 \\
0 & 0 & -1 & 0 \\
-1 & -1 & 0 & 1
\end{bmatrix}
$$

Pour se faire on aura besoin de modifier le *vertex shader* pour qu'il prenne en compte une matrice de transformation :

```c
const char* vertexShaderSource =
    "#version 330 core\n"
    "layout (location = 0) in vec3 position;\n"
    "uniform mat4 model;\n"
    "void main() {\n"
    "    gl_Position = model * vec4(position, 1.0);\n"
    "}\n";
```
