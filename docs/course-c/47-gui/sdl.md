# SDL

SDL (*Simple DirectMedia Layer*) est une bibliothèque multiplateforme qui permet de créer des applications graphiques. Elle est utilisée dans de nombreux jeux vidéo et applications multimédia. Elle est écrite en C, mais des bindings existent pour de nombreux langages, dont Python ou C++.

La biblithèque a été créée en 1998 par Sam Lantinga, un développeur alors employé par Loki Software, une société spécialisée dans le portage de jeux vidéo sur Linux. À l’époque, il était difficile pour les développeurs de créer des jeux multiplateformes, car chaque système d'exploitation (Windows, Linux, macOS) utilisait des bibliothèques et des API différentes pour gérer les graphismes, le son et les entrées. SDL a été développée pour offrir une interface unique et simple permettant d'accéder à ces fonctionnalités sur plusieurs plateformes, facilitant ainsi le développement de jeux et d'applications multimédias multiplateformes.

On peut citer quelques projets qui utilisent SDL.

- [The Battle for Wesnoth](https://www.wesnoth.org/)
- [Faster Than Light](https://subsetgames.com/ftl.html)
- [Doom 3](https://github.com/id-Software/DOOM-3)
- [ScummVM](https://www.scummvm.org/)

La plupart de ces projets sont développés en C++ car le C n'est pas un langage très adapté pour le développement d'applications complexes et graphiques.

La bibliothèque est plus qu'une simple abstraction des fonctionnalités graphiques des systèmes d'exploitation. Elle offre également des fonctionnalités notament :

- Gestion des fenêtres
- Gestion des événements (clavier, souris, joystick)
- Gestion du son
- Multi-threading
- Timers
- Accélération 2D
- Support 3D (Vulkan, Metal, OpenGL)

La bibliothèque est plus complète que GLFW et est bien adaptée à des projets complexes en C.

## Premiers pas

Pour installer SDL sur votre système, vous pouvez utiliser le gestionnaire de paquets de votre distribution. Sous Ubuntu :

```bash
sudo apt install libsdl2-dev "libsdl2-*"
```

Une extension de SDL nommée GFX est également disponible. Elle ajoute des fonctionnalités graphiques supplémentaires comme des fonctions de dessin de primitives (lignes, rectangles, cercles, etc.).

```bash
--8<-- "docs/assets/src/sdl/shapes/main.c"
```

![Intersections de cercles](/assets/images/circles.png)


## Polygones

Voici un exemple d'un programme de dessin de polygones en utilisant SDL.

![Programme de dessin de polygones](/assets/images/polygons.png)

```c
--8<-- "docs/assets/src/sdl/bezier/light.c"
```
