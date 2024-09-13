#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

#define MAX_POINTS 100

typedef struct {
   float x, y;
} Point;

Point points[MAX_POINTS];
int point_count = 0;

SDL_Color colors[MAX_POINTS];

SDL_Color get_color() {
   int r = rand() % 120 + 100;
   int g = rand() % 120 + 100;
   int b = rand() % 120 + 100;
   return (SDL_Color){r, g, b, 255};
}
float distance(Point p1, Point p2) {
   return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y));
}

void draw_voronoi(SDL_Renderer *renderer, int width, int height) {
   for (int y = 0; y < height; y++) {
      for (int x = 0; x < width; x++) {
         Point current_point = {x, y};
         int closest_point = 0;
         float min_dist = distance(current_point, points[0]);
         for (int i = 1; i < point_count; i++) {
            float dist = distance(current_point, points[i]);
            if (dist < min_dist) {
               min_dist = dist;
               closest_point = i;
            }
         }
         SDL_SetRenderDrawColor(
             renderer, colors[closest_point].r, colors[closest_point].g,
             colors[closest_point].b, colors[closest_point].a);
         SDL_RenderDrawPoint(renderer, x, y);
      }
   }
}

int main() {
   SDL_Init(SDL_INIT_VIDEO);
   SDL_Window *window =
       SDL_CreateWindow("Diagramme de Voronoi", SDL_WINDOWPOS_UNDEFINED,
                        SDL_WINDOWPOS_UNDEFINED, 800, 400, 0);
   SDL_Renderer *renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
   SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);

   bool running = true;
   bool voronoi_needs_update = true;

   while (running) {
      SDL_Event event;
      while (SDL_PollEvent(&event)) {
         if (event.type == SDL_QUIT) {
            running = false;
         } else if (event.type == SDL_MOUSEBUTTONDOWN &&
                    point_count < MAX_POINTS) {
            points[point_count].x = event.button.x;
            points[point_count].y = event.button.y;
            colors[point_count] = get_color();
            point_count++;
            voronoi_needs_update = true;
         }
      }

      if (voronoi_needs_update) {
         SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
         SDL_RenderClear(renderer);
         draw_voronoi(renderer, 800, 400);
         for (int i = 0; i < point_count; i++)
            filledCircleRGBA(renderer, points[i].x, points[i].y, 3, 0, 0, 0,
                             255);
         SDL_RenderPresent(renderer);
         voronoi_needs_update = false;
      }
   }
   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
