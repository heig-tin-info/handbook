# Algorithmes d'infographie

Les algorithmes d'infographie sont des algorithmes utilisés pour générer des images numériques. Ils sont utilisés dans de nombreux domaines, tels que les jeux vidéo, les films d'animation, la réalité virtuelle, etc.

## Bresenham

L'algorithme de Bresenham est une méthode efficace pour tracer des lignes droites sur une grille de pixels en utilisant uniquement des opérations entières. Il est particulièrement adapté aux écrans d'ordinateur où les positions des pixels sont discrètes. L'algorithme détermine quels pixels doivent être allumés pour former la meilleure approximation possible d'une ligne droite entre deux points.

![Algorithme de Bresenham](/assets/images/bressenham.gif)

### Principe de l'algorithme

Considérons le tracé d'une ligne entre deux points:

$$p=(x_0, y_0), q=(x_1, y_1)$

Tel que pour chaque position $x$, la valeur de $y$ qui correspond le mieux à la ligne idéale.

L'algorithme utilise une variable d'erreur pour décider quand incrémenter $y$. Cette variable représente la distance entre la position réelle de la ligne idéale et la position actuelle sur la grille de pixels. L'équation de la variable d'erreur est mise à jour à chaque itération pour refléter cette distance. Cet algorithme est un outil puissant pour le tracé efficace de lignes sur une grille de pixels. En utilisant uniquement des opérations entières, il optimise les performances, ce qui est crucial pour les applications graphiques en temps réel.

```c
void bresenhamLine(Point p, Point q, SDL_Renderer *renderer) {
   int dx = abs(q.x - p.x), dy = abs(q.y - p.y);
   int sx = p.x < q.x ? 1 : -1, sy = p.y < q.y ? 1 : -1;
   int err = dx - dy;

   for (;;) {
      setPixel(renderer, p.x, p.y, 1.0f);
      if (p.x == q.x && p.y == q.y) break;
      int e2 = 2 * err;
      if (e2 > -dy) {
         err -= dy;
         p.x += sx;
      }
      if (e2 < dx) {
         err += dx;
         p.y += sy;
      }
   }
}
```

## Xiaolin Wu

L'algorithme de Xiaolin Wu est une méthode améliorée pour le tracé d'antialiasing de lignes. Il utilise des techniques de subpixel pour rendre les lignes plus lisses et plus précises. L'algorithme de Xiaolin Wu est basé sur l'algorithme de Bresenham, mais il ajoute des étapes supplémentaires pour gérer les valeurs de couleurs partielles des pixels. Il fut publié en 1991 dans le journal Computer Graphics ([An Efficient Antialiasing Technique](https://cgg.mff.cuni.cz/~pepca/ref/WU.pdf)).

![Algorithme de Xiaolin Wu](/assets/images/xiaolin-wu.gif)

```c
void wuLine(Point p0, Point p1, SDL_Renderer *renderer) {
   bool steep = abs(p1.y - p0.y) > abs(p1.x - p0.x);

   if (steep) {
      swapXY(&p0);
      swapXY(&p1);
   }

   if (p0.x > p1.x) swapPoints(&p0, &p1);

   int dx = p1.x - p0.x;
   int dy = p1.y - p0.y;
   float gradient = dx == 0 ? 1 : (float)dy / (float)dx;

   // Première extrémité
   float xEnd = p0.x;
   float yEnd = p0.y + gradient * (xEnd - p0.x);
   float xGap = 1.0f;
   int xPixel1 = (int)xEnd;
   int yPixel1 = (int)yEnd;

   if (steep) {
      setPixel(renderer, yPixel1, xPixel1, (1 - (yEnd - yPixel1)) * xGap);
      setPixel(renderer, yPixel1 + 1, xPixel1, (yEnd - yPixel1) * xGap);
   } else {
      setPixel(renderer, xPixel1, yPixel1, (1 - (yEnd - yPixel1)) * xGap);
      setPixel(renderer, xPixel1, yPixel1 + 1, (yEnd - yPixel1) * xGap);
   }

   float intery = yEnd + gradient;

   // Deuxième extrémité
   xEnd = p1.x;
   yEnd = p1.y + gradient * (xEnd - p1.x);
   xGap = 1.0f;
   int xPixel2 = (int)xEnd;
   int yPixel2 = (int)yEnd;

   if (steep) {
      setPixel(renderer, yPixel2, xPixel2, (1 - (yEnd - yPixel2)) * xGap);
      setPixel(renderer, yPixel2 + 1, xPixel2, (yEnd - yPixel2) * xGap);
   } else {
      setPixel(renderer, xPixel2, yPixel2, (1 - (yEnd - yPixel2)) * xGap);
      setPixel(renderer, xPixel2, yPixel2 + 1, (yEnd - yPixel2) * xGap);
   }

   // Tracer les pixels entre les deux extrémités
   if (steep) {
      for (int x = xPixel1 + 1; x < xPixel2; ++x) {
         setPixel(renderer, (int)intery, x, (1 - (intery - (int)intery)));
         setPixel(renderer, (int)intery + 1, x, intery - (int)intery);
         intery += gradient;
      }
   } else {
      for (int x = xPixel1 + 1; x < xPixel2; ++x) {
         setPixel(renderer, x, (int)intery, (1 - (intery - (int)intery)));
         setPixel(renderer, x, (int)intery + 1, intery - (int)intery);
         intery += gradient;
      }
   }
}
```

## Courbes de Bézier

Les courbes de Bézier sont des courbes mathématiques utilisées pour représenter des formes lisses et régulières. Elles sont largement utilisées en infographie pour le tracé de courbes.

![Courbes de Bézier](/assets/images/bezier.gif)

Le calcul de Bézier est donné par l'algorithme suivant :

```c
Point bezier(Point p, Point c, Point q, float t) {
   const float it = 1.f - t;
   return (Point){.x = it * it * p.x + 2 * it * t * c.x + t * t * q.x,
                  .y = it * it * p.y + 2 * it * t * c.y + t * t * q.y};
}
```

Le point $p$ est le point de départ de la courbe, le point $q$ est le point d'arrivée et le point $c$ est le point de contrôle. La valeur de $t$ varie de 0 à 1 pour déterminer la position le long de la courbe.

En pratique, la valeur $t$ est incrémentée à chaque itération pour tracer des tronçons de la courbe par des segments de droite.

```c
void drawBezierCurve(SDL_Renderer *renderer, Point p, Point q, Point c) {
   const float precision = 0.01;
   Point prev = p;
   for (float t = 0.0; t <= 1.0; t += precision) {
      Point current = bezier(p, c, q, t);
      draw_line(prev, current);
      prev = current;
   }
}
```

## Floyd-Steinberg
