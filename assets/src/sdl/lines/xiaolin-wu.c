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
   Uint8 alpha = fmax(fmin(intensity, 1.0f), 0.0f) * 255;
   SDL_SetRenderDrawColor(renderer, 255, 20, 182, alpha);
   SDL_Rect rect = {x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE};
   SDL_RenderFillRect(renderer, &rect);
}

void swapXY(Point *p) {
   int temp = p->x;
   p->x = p->y;
   p->y = temp;
}

void swapPoints(Point *p0, Point *p1) {
   Point temp = *p0;
   *p0 = *p1;
   *p1 = temp;
}

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

int main(int argc, char *argv[]) {
   SDL_Init(SDL_INIT_VIDEO);
   SDL_Window *window =
       SDL_CreateWindow("Algorithme de Xiaolin Wu", SDL_WINDOWPOS_CENTERED,
                        SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, 0);
   SDL_Renderer *renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

   Point startPoint = {0, 0};
   Point endPoint = {WINDOW_WIDTH / GRID_SIZE - 1,
                     WINDOW_HEIGHT / GRID_SIZE - 1};
   bool running = true;
   bool leftButtonDown = false;
   bool rightButtonDown = false;

   SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
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
      wuLine(startPoint, endPoint, renderer);
      SDL_RenderPresent(renderer);
   }
   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
