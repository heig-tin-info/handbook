# Fenêtre graphique

Comme nous l'avons vu, un programme informatique standard dispose de plusieurs flux : un flux d'entrée (`stdin`) et deux flux de sortie (`stdout` et `stderr`). Ces flux sont généralement associés à la console texte, mais ne sont pas directement reliés à une fenêtre graphique permettant des interactions visuelles. Pourtant, de nombreuses applications modernes proposent une interface graphique pour permettre une meilleure interaction avec l'utilisateur.

Sous Windows comme sous Linux, l'interface utilisateur graphique, composée de fenêtres, de menus et d'autres éléments interactifs, est gérée par ce que l'on appelle un *window manager*. Ce gestionnaire de fenêtres est responsable de la création, de la gestion et de la disposition des différentes fenêtres à l'écran. Il agit comme une couche intermédiaire entre le noyau du système d'exploitation et les applications graphiques.

Le *window manager* est un processus distinct qui fonctionne en parallèle de votre programme. Il est donc essentiel, d'une part, qu'il soit déjà lancé avant l'exécution de votre application (ce qui est généralement le cas dans un environnement de bureau standard) et, d'autre part, que votre programme soit capable de communiquer avec ce gestionnaire de manière appropriée. Sous Linux, cette communication se fait le plus souvent par l'intermédiaire le protocole X11 ou plus réemment Wayland, également connu sous le nom de "X Window System". Sous Windows c'est l'API Win32 qui est utilisée mais des alternatives comme GTK ou Qt sont également disponibles via MinGW ou MSYS.

## Le protocole X11

X11 est un protocole réseau qui permet à un programme de dessiner des fenêtres sur l'écran, qu'il soit local ou distant. Il a la particularité d'être indépendant de la machine où l'application s'exécute, permettant ainsi de contrôler graphiquement des applications sur d'autres ordinateurs. Cependant, interagir directement avec X11 est un processus complexe, car cela implique de gérer de nombreux paramètres relatifs aux fenêtres : dimensions, position, gestion des événements, et autres aspects liés à l'interaction utilisateur.

Le protocole X11 est basé sur un modèle client-serveur. Un programme se connecte donc au serveur en utilisant des sockets, typiquement des sockets Unix (*Unix Domain Socket*). Ce socket est un canal de communication avec le serveur dans lequel des ordre du type "dessine-moi un rectangle à telle position" ou "affiche ce texte" sont envoyés. Le serveur X11 est responsable de la gestion des fenêtres, des événements, des polices, des couleurs, etc.

Comme la communication passe par les sockets, il est possible de profiter de l'encapsulation TCP/IP et de dialoguer avec un server distant via internet ou un réseau local. Avant l'avènement WSLg (*Windows Subsystem for Linux GUI*), il était possible d'afficher des fenêtres graphiques Linux en utilisant un serveur X11 installé directement sous Windows comme [VcXsrv](https://sourceforge.net/projects/vcxsrv/). D'ailleurs si vous utilisez Docker, ou que vous vous connectez à un Raspberry Pi, vous pouvez également profiter d'une interface graphique depuis une connection SSH par exemple (via l'option `-X`).

Pour illustrer la complexité de l'usage direct de X11, voici un exemple de programme en C qui ouvre une simple fenêtre de 100 pixels par 100 pixels :

```c
#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
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
   XEvent e;
   do {
      XNextEvent(d, &e);
      if (e.type == Expose)
         XFillRectangle(d, w, DefaultGC(d, s), 20, 20, 10, 10);
   } while (e.type != KeyPress);

   XCloseDisplay(d);
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

Le programme ainsi généré ouvre une fenêtre minimaliste, mais il est évident qu'implémenter des interfaces graphiques sophistiquées en utilisant uniquement X11 est un travail considérable. La gestion manuelle des événements, des composants graphiques et des interactions utilisateurs devient rapidement fastidieuse. D'autre part ce protocol n'est pas portable, il est spécifique à Linux et n'est pas disponible sur d'autres systèmes d'exploitation.

### Wayland

Wayland est un protocole graphique plus récent que X11, conçu pour remplacer ce dernier en tant que gestionnaire de fenêtres par défaut sous Linux. Wayland est plus moderne, plus sécurisé et plus performant que X11, mais il est également plus restrictif en termes de fonctionnalités. Wayland est conçu pour être plus simple en limitant l'accès des applications aux ressources système et en isolant les processus les uns des autres.

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

Alternativement, vous pouvez utiliser l'environnement officiel de développement de Microsoft Visual Studio, qui fournit un ensemble complet d'outils pour le développement d'applications Windows mais son installation est plus lourde et dépasse le cadre de ce cours.

## GTK

![GUI avec GTK](/assets/images/gui.png)

## Rendu logiciel ou matériel

Les premiers ordinateurs personnels, comme le [Macintosh](wiki:macintosh) d'Apple ou l'Amiga d'Atari, utilisaient un rendu graphique purement logiciel. Cela signifie que le processeur central (CPU) était responsable de dessiner les pixels à l'écran, en calculant les couleurs, les textures, les ombres, et autres effets visuels. Historiquement avant les systèmes d'exploitation multitâches, pour afficher un pixel à l'écran, il suffisait ou presque d'écrire une valeur dans la mémoire vidéo.

Depuis ces ages immémoriaux, les systèmes d'exploitations sont devenus beaucoup plus restrictifs et n'autorisent plus l'accès direct à la mémoire vidéo. D'ailleurs les cartes graphiques modernes fonctionnent très différemment. Néanmoins beaucoup de bibliothèques graphiques de haut niveau comme GTK, Qt, SDL ou Allegro peuvent encore utiliser un rendu logiciel pour dessiner certains éléments graphiques à l'écran. Plutôt qu'accéder à la mémoire vidéo ces bibliothèques utilisent un *framebuffer*. Il s'agit d'une zone de mémoire correspondant à l'intérieur de la fenêtre graphique où les pixels sont dessinés. Une fois que le dessin est terminé, le contenu du *framebuffer* est copié dans la mémoire vidéo par le *window manager*.

Le rendu matériel par opposition n'est pas géré par le CPU mais par la carte graphique. Si vous étiez paysan au moyen-âge pour planter une carottes, vous retroussiez vos manches, preniez votre bêche et en avant la besogne. Vous auriez été dans le champ (mémoire vidéo) pour y planter (allumer) une carotte (pixel). Une carte graphique c'est des milliers de processeurs, c'est une entreprise colossale plus proche des 12 travaux d'Asterix que de la culture ancestrale de la carotte. Coordonner les bonnes personne pour qu'elles aille pour vous planter une carotte à l'endroit souhaité c'est forcément plus compliqué. Le rendu matériel c'est ordonner à la carte graphique de planter les carottes à votre place. Pendant ce temps vous pouvez faire autre chose. C'est plus rapide, plus efficace, mais forcément plus complexe.

Le rendu matériel est particulièrement plus efficace lorsque des effets graphiques sont utilisés (animations 3D, effets d'ombres ou de flous, etc.). L'exemple suivant utlise le rendu matériel pour animer une théière en 3D :

```c
#include <GL/glut.h>
#include <math.h>

float angle = 0.0f;

void display() {
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
   glLoadIdentity();
   gluLookAt(1.0f, 2.0f, 5.0f,   // Position de la caméra
             0.0f, 0.0f, 0.0f,   // Point de mire
             0.0f, 1.0f, 0.0f);  // Vecteur "up"

   glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat[]){1.0f, 1.0f, 1.0f, 0.0f});
   glRotatef(angle, 0.0f, 1.0f, 0.0f);  // Rotation autour de l'axe Y
   glColor3f(0.8f, 0.2f, 0.2f);
   glutSolidTeapot(1.0);
   glutSwapBuffers();
}

void reshape(int width, int height) {
   if (height == 0) height = 1;
   glViewport(0, 0, width, height);
   glMatrixMode(GL_PROJECTION);
   glLoadIdentity();
   gluPerspective(45.0f, (float)width / (float)height, 1.0f, 100.0f);
   glMatrixMode(GL_MODELVIEW);
}

void initOpenGL() {
   glEnable(GL_DEPTH_TEST);
   glEnable(GL_LIGHTING);
   glEnable(GL_LIGHT0);
   glShadeModel(GL_SMOOTH);
   glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
}

void update(int value) {
   if ((angle += 2.0f) > 360) angle -= 360;
   glutPostRedisplay();
   glutTimerFunc(16 /* ms */, update, 0);
}

int main(int argc, char** argv) {
   glutInit(&argc, argv);
   glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
   glutInitWindowSize(800, 400);
   glutCreateWindow("Animated Teapot with Shadows");
   initOpenGL();
   glutDisplayFunc(display);
   glutReshapeFunc(reshape);
   glutTimerFunc(16, update, 0);
   glutMainLoop();
}
```

![Théière en 3D](/assets/images/teapot.png)

La bibliothèque Cairo est un exemple de bibliothèque de rendu 2D qui peut fonctionner en mode logiciel ou matériel. Cairo est utilisé par GTK pour le rendu graphique de ses composants. Il est également utilisé par d'autres applications comme Inkscape, Firefox, et WebKit. Voici l'exemple d'un programme qui trace une ligne noir sous la souris :

```c
#include <gtk/gtk.h>

#define WIDTH 800
#define HEIGHT 400

gboolean on_draw_event(GtkWidget *widget, cairo_t *cr, gpointer user_data) {
   cairo_set_source_rgb(cr, 1.0, 1.0, 1.0);  // White
   cairo_paint(cr);
   return FALSE;
}

gboolean on_mouse_move(GtkWidget *widget, GdkEventMotion *event, gpointer d) {
   static int last_x = -1, last_y = -1;
   cairo_t *cr = gdk_cairo_create(gtk_widget_get_window(widget));
   int x = (int)event->x, y = (int)event->y;
   if (last_x != -1 && last_y != -1) {
      cairo_set_source_rgb(cr, 0.0, 0.0, 0.0);
      cairo_move_to(cr, last_x, last_y);
      cairo_line_to(cr, x, y);
      cairo_stroke(cr);
   }
   last_x = x;
   last_y = y;
   cairo_destroy(cr);
   return TRUE;  // Stop event propagation
}

int main(int argc, char *argv[]) {
   gtk_init(&argc, &argv);
   GtkWidget *w = gtk_window_new(GTK_WINDOW_TOPLEVEL);

   gtk_window_set_title(GTK_WINDOW(w), "Frame Buffer Example");
   gtk_window_set_default_size(GTK_WINDOW(w), WIDTH, HEIGHT);

   GdkWindow *gdk_window = gtk_widget_get_window(w);
   GdkDisplay *display = gdk_window_get_display(gdk_window);
   GdkCursor *cursor = gdk_cursor_new_for_display(display, GDK_ARROW);
   gdk_window_set_cursor(gdk_window, cursor);
   g_object_unref(cursor);

   g_signal_connect(w, "destroy", G_CALLBACK(gtk_main_quit), NULL);
   g_signal_connect(w, "draw", G_CALLBACK(on_draw_event), NULL);
   g_signal_connect(w, "motion-notify-event", G_CALLBACK(on_mouse_move), NULL);
   gtk_widget_add_events(w, GDK_POINTER_MOTION_MASK);
   gtk_widget_show_all(w);
   gtk_main();
}
```

Pour compiler ce programme vous aurez besoin de la bibliothèque GTK. Or cette biblothèque a de nombreuses dépendances (pango, glib, harfbuzz, freetype, libpng, webp, at...). Pkg-config se révèle très utile pour récupérer les flags de compilation et de liens. Voici comment compiler ce programme:

```bash
gcc `pkg-config --cflags gtk+-3.0` x.c `pkg-config --libs gtk+-3.0`
```

Rien de sorcier, les backticks permettent d'exécuter des sous commandes. On exécute donc `pkg-config` deux fois. Une pour récupérer les drapeaux de compilation et l'autre pour récupérer les bibliothèques à lier. On aurait bien entendu pu le faire à la main, mais vous conviendrez que c'est plus simple avec pkg-config.

```bash
gcc -I/usr/include/gtk-3.0 -I/usr/include/pango-1.0 -I/usr/include/glib-2.0
-I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/harfbuzz
-I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/libmount
-I/usr/include/blkid -I/usr/include/fribidi -I/usr/include/cairo
-I/usr/include/pixman-1 -I/usr/include/gdk-pixbuf-2.0
-I/usr/include/x86_64-linux-gnu -I/usr/include/webp -I/usr/include/gio-unix-2.0
-I/usr/include/atk-1.0 -I/usr/include/at-spi2-atk/2.0 -I/usr/include/at-spi-2.0
-I/usr/include/dbus-1.0 -I/usr/lib/x86_64-linux-gnu/dbus-1.0/include -pthread
x.c -lgtk-3 -lgdk-3 -lz -lpangocairo-1.0 -lpango-1.0 -lharfbuzz -latk-1.0
-lcairo-gobject -lcairo -lgdk_pixbuf-2.0 -lgio-2.0 -lgobject-2.0 -lglib-2.0
```

![Hello tracé avec la souris](/assets/images/framebuffer.png)


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

![Balle qui rebondit](/assets/images/bouncing-ball.gif)

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
