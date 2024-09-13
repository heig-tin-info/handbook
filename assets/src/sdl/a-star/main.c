#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#define WIDTH 800
#define HEIGHT 400
#define CELL_SIZE 15

typedef struct {
   int x, y;
} Point;

typedef enum CellType {
   CELL_EMPTY,
   CELL_OBSTACLE,
   CELL_OPEN,
   CELL_CLOSE,
   CELL_PATH,
} CellType;

typedef struct {
   Point parent;
   float gCost;
   float hCost;
   CellType type;
} Node;

Node grid[WIDTH / CELL_SIZE][HEIGHT / CELL_SIZE];
Point start, end;
bool hasStart = false, hasEnd = false, obstaclesPlaced = false;

float heuristic(Point a, Point b) {
   return fabsf(a.x - b.x) + fabsf(a.y - b.y);
}

void drawGrid(SDL_Renderer* renderer) {
   SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
   SDL_RenderClear(renderer);
   for (int x = 0; x < WIDTH / CELL_SIZE; ++x) {
      for (int y = 0; y < HEIGHT / CELL_SIZE; ++y) {
         Uint32 color = 0;
         switch (grid[x][y].type) {
            case CELL_OBSTACLE:
               SDL_SetRenderDrawColor(renderer, 0, 0, 0, 128);
               break;
            case CELL_OPEN:
               SDL_SetRenderDrawColor(renderer, 153, 255, 153, 128);
               break;
            case CELL_CLOSE:
               SDL_SetRenderDrawColor(renderer, 204, 255, 204, 128);
               break;
            case CELL_PATH:
               filledCircleColor(renderer, x * CELL_SIZE + CELL_SIZE / 2,
                                 y * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE / 4,
                                 0xff0066cc);
               continue;
            case CELL_EMPTY:
               continue;
         }
         SDL_Rect rect = {x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE};
         SDL_RenderFillRect(renderer, &rect);
      }
   }

   if (hasStart) {
      filledCircleColor(renderer, start.x * CELL_SIZE + CELL_SIZE / 2,
                        start.y * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE / 3,
                        0xFF0066cc);
   }

   if (hasEnd) {
      filledCircleColor(renderer, end.x * CELL_SIZE + CELL_SIZE / 2,
                        end.y * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE / 3,
                        0xFFff6600);
   }

   // Dessine les lignes de la grille en gris
   SDL_SetRenderDrawColor(renderer, 200, 200, 200, 255);
   for (int x = 0; x < WIDTH; x += CELL_SIZE)
      SDL_RenderDrawLine(renderer, x, 0, x, HEIGHT);
   for (int y = 0; y < HEIGHT; y += CELL_SIZE)
      SDL_RenderDrawLine(renderer, 0, y, WIDTH, y);
}

// The A* algorithm
void aStar(SDL_Renderer* renderer) {
   Point openList[(WIDTH / CELL_SIZE) * (HEIGHT / CELL_SIZE)];
   int openListSize = 0;

   grid[start.x][start.y].gCost = 0;
   grid[start.x][start.y].hCost = heuristic(start, end);
   openList[openListSize++] = start;
   grid[start.x][start.y].type = CELL_OPEN;

   bool pathFound = false;

   while (openListSize > 0) {
      int lowestFIndex = 0;
      for (int i = 1; i < openListSize; i++) {
         Point p = openList[i];
         Point lowestP = openList[lowestFIndex];
         float fCostP = grid[p.x][p.y].gCost + grid[p.x][p.y].hCost;
         float fCostLowest = grid[lowestP.x][lowestP.y].gCost +
                             grid[lowestP.x][lowestP.y].hCost;
         if (fCostP < fCostLowest) {
            lowestFIndex = i;
         }
      }

      Point current = openList[lowestFIndex];

      if (current.x == end.x && current.y == end.y) {
         pathFound = true;
         break;
      }

      // Remove current from openList
      for (int i = lowestFIndex; i < openListSize - 1; i++) {
         openList[i] = openList[i + 1];
      }
      openListSize--;
      grid[current.x][current.y].type = CELL_CLOSE;

      // Neighbors (4-way movement)
      Point neighbors[4] = {{current.x + 1, current.y},
                            {current.x - 1, current.y},
                            {current.x, current.y + 1},
                            {current.x, current.y - 1}};

      for (int i = 0; i < 4; i++) {
         Point neighbor = neighbors[i];

         // Check bounds
         if (neighbor.x < 0 || neighbor.x >= WIDTH / CELL_SIZE ||
             neighbor.y < 0 || neighbor.y >= HEIGHT / CELL_SIZE)
            continue;
         if (grid[neighbor.x][neighbor.y].type == CELL_OBSTACLE ||
             grid[neighbor.x][neighbor.y].type == CELL_CLOSE)
            continue;

         float tentativeGCost = grid[current.x][current.y].gCost + 1;

         if (grid[neighbor.x][neighbor.y].type != CELL_OPEN ||
             tentativeGCost < grid[neighbor.x][neighbor.y].gCost) {
            grid[neighbor.x][neighbor.y].parent = current;
            grid[neighbor.x][neighbor.y].gCost = tentativeGCost;
            grid[neighbor.x][neighbor.y].hCost = heuristic(neighbor, end);

            if (grid[neighbor.x][neighbor.y].type != CELL_OPEN) {
               openList[openListSize++] = neighbor;
               grid[neighbor.x][neighbor.y].type = CELL_OPEN;
            }
         }
      }

      drawGrid(renderer);
      SDL_RenderPresent(renderer);
      SDL_Delay(10);  // Slow down the algorithm
   }

   // If path is found, trace back
   if (pathFound) {
      Point current = end;
      while (!(current.x == start.x && current.y == start.y)) {
         grid[current.x][current.y].type = CELL_PATH;
         SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
         drawGrid(renderer);
         SDL_RenderPresent(renderer);
         SDL_Delay(30);
         current = grid[current.x][current.y].parent;
      }
   }
}

int main(int argc, char* argv[]) {
   SDL_Init(SDL_INIT_VIDEO);
   SDL_Window* window = SDL_CreateWindow(
       "A* Pathfinding", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
       WIDTH, HEIGHT, SDL_WINDOW_SHOWN);
   SDL_Renderer* renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

   SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
   SDL_bool running = SDL_TRUE;
   SDL_Event event;

   SDL_bool middleButtonHeld = SDL_FALSE;
   while (running) {
      while (SDL_PollEvent(&event)) {
         if (event.type == SDL_QUIT) {
            running = SDL_FALSE;
         } else if (event.type == SDL_MOUSEBUTTONDOWN) {
            int x = event.button.x / CELL_SIZE;
            int y = event.button.y / CELL_SIZE;

            if (event.button.button == SDL_BUTTON_LEFT) {
               start = (Point){x, y};
               hasStart = true;
            } else if (event.button.button == SDL_BUTTON_RIGHT) {
               end = (Point){x, y};
               hasEnd = true;
            } else if (event.button.button == SDL_BUTTON_MIDDLE) {
               grid[x][y].type = CELL_OBSTACLE;
               middleButtonHeld = SDL_TRUE;  // Le bouton du milieu est enfoncé
            }
         } else if (event.type == SDL_MOUSEBUTTONUP) {
            if (event.button.button == SDL_BUTTON_MIDDLE) {
               middleButtonHeld = SDL_FALSE;  // Le bouton du milieu est relâché
            }
         }

         if (middleButtonHeld) {
            int x, y;
            SDL_GetMouseState(&x, &y);
            x /= CELL_SIZE;
            y /= CELL_SIZE;
            if (x >= 0 && x < WIDTH / CELL_SIZE && y >= 0 &&
                y < HEIGHT / CELL_SIZE) {
               grid[x][y].type = CELL_OBSTACLE;
            }
         }
      }

      if (hasStart && hasEnd) {
         aStar(renderer);
         hasStart = false;
         hasEnd = false;
      }

      drawGrid(renderer);
      SDL_RenderPresent(renderer);
      SDL_Delay(10);
   }

   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
