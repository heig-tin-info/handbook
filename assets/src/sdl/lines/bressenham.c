#include <SDL2/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#define WINDOW_WIDTH 800
#define WINDOW_HEIGHT 400
#define GRID_SIZE 10

typedef struct {
   int x;
   int y;
} Point;

void drawGrid(SDL_Renderer *renderer) {
   SDL_SetRenderDrawColor(renderer, 200, 200, 200, 255);
   for (int x = 0; x <= WINDOW_WIDTH; x += GRID_SIZE)
      SDL_RenderDrawLine(renderer, x, 0, x, WINDOW_HEIGHT);
   for (int y = 0; y <= WINDOW_HEIGHT; y += GRID_SIZE)
      SDL_RenderDrawLine(renderer, 0, y, WINDOW_WIDTH, y);
}

Point getGridPosition(int x, int y) {
   return (Point){.x = x / GRID_SIZE, .y = y / GRID_SIZE};
}

void setPixel(SDL_Renderer *renderer, int x, int y, float intensity) {
   Uint8 color = fmax(fmin(intensity, 1.0f), 0.0f) * 255;
   SDL_SetRenderDrawColor(renderer, color, 0, color, 255);
   SDL_Rect rect = {x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE};
   SDL_RenderFillRect(renderer, &rect);
}

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

int main(int argc, char *argv[]) {
   SDL_Init(SDL_INIT_VIDEO);
   SDL_Window *window =
       SDL_CreateWindow("Algorithme de Bresenham", SDL_WINDOWPOS_CENTERED,
                        SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, 0);
   SDL_Renderer *renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

   Point startPoint = {0, 0};
   Point endPoint = {WINDOW_WIDTH / GRID_SIZE - 1,
                     WINDOW_HEIGHT / GRID_SIZE - 1};
   bool running = true;
   bool leftButtonDown = false;
   bool rightButtonDown = false;

   while (running) {
      SDL_Event event;
      while (SDL_PollEvent(&event)) {
         switch (event.type) {
            case SDL_QUIT:
               running = false;
               break;
            case SDL_MOUSEBUTTONDOWN:
               if (event.button.button == SDL_BUTTON_LEFT)
                  leftButtonDown = true;
               else if (event.button.button == SDL_BUTTON_RIGHT)
                  rightButtonDown = true;
               break;
            case SDL_MOUSEBUTTONUP:
               if (event.button.button == SDL_BUTTON_LEFT)
                  leftButtonDown = false;
               else if (event.button.button == SDL_BUTTON_RIGHT)
                  rightButtonDown = false;
               break;
            case SDL_MOUSEMOTION:
               if (leftButtonDown || rightButtonDown) {
                  int x, y;
                  SDL_GetMouseState(&x, &y);
                  Point gridPos = getGridPosition(x, y);
                  if (leftButtonDown)
                     startPoint = gridPos;
                  else if (rightButtonDown)
                     endPoint = gridPos;
               }
               break;
            default:
               break;
         }
      }
      SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
      SDL_RenderClear(renderer);
      drawGrid(renderer);
      bresenhamLine(startPoint, endPoint, renderer);
      SDL_RenderPresent(renderer);
   }
   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
