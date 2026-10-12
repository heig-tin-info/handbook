#include <SDL2/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 400
#define TIME_TO_FADE_MS 5000
#define CELL_WIDTH 10
#define RULE_CONWAY "B3/S23"
#define RULE_MAZE "B3/S12345"

#define ROWS (SCREEN_HEIGHT / CELL_WIDTH)
#define COLS (SCREEN_WIDTH / CELL_WIDTH)

int glider[][2] = {{1, 2}, {2, 3}, {3, 1}, {3, 2}, {3, 3}};

int gosper_glider_gun[][2] = {
    {0, 24}, {1, 22}, {1, 24}, {2, 12}, {2, 13}, {2, 20}, {2, 21}, {2, 34},
    {2, 35}, {3, 11}, {3, 15}, {3, 20}, {3, 21}, {3, 34}, {3, 35}, {4, 0},
    {4, 1},  {4, 10}, {4, 16}, {4, 20}, {4, 21}, {5, 0},  {5, 1},  {5, 10},
    {5, 14}, {5, 16}, {5, 17}, {5, 22}, {5, 24}, {6, 10}, {6, 16}, {6, 24},
    {7, 11}, {7, 15}, {8, 12}, {8, 13}};

typedef struct {
   bool alive;
   Uint32 death_time;  // Timestamp when the cell died
} Cell;

void insert_shape(Cell grid[ROWS][COLS], int shape[][2], int shape_size, int x,
                  int y) {
   for (int i = 0; i < shape_size; ++i) {
      int nx = shape[i][0] + x;
      int ny = shape[i][1] + y;
      if (nx >= 0 && nx < ROWS && ny >= 0 && ny < COLS) {
         grid[nx][ny].alive = true;
         grid[nx][ny].death_time = 0;
      }
   }
}

void init_grid(Cell grid[ROWS][COLS]) {
   for (int i = 0; i < ROWS; ++i) {
      for (int j = 0; j < COLS; ++j) {
         grid[i][j].alive = false;
         grid[i][j].death_time = 0;
      }
   }
}

// Fonction pour randomiser la grille
void randomize_grid(Cell grid[ROWS][COLS]) {
   for (int i = 0; i < ROWS; ++i) {
      for (int j = 0; j < COLS; ++j) {
         grid[i][j].alive = rand() % 2;
         grid[i][j].death_time = grid[i][j].alive ? 0 : SDL_GetTicks();
      }
   }
}

int inArray(int arr[], int value) {
   for (int i = 0; arr[i] != 0; i++) {
      if (arr[i] == value) {
         return 1;  // Trouvé
      }
   }
   return 0;  // Non trouvé
}

// Convertir HSV en RGB (avec interpolation sur le hue)
void HSVtoRGB(double hue, double saturation, double value, Uint8* r, Uint8* g,
              Uint8* b) {
   int h = (int)(hue * 6);
   double f = hue * 6 - h;
   double p = value * (1 - saturation);
   double q = value * (1 - f * saturation);
   double t = value * (1 - (1 - f) * saturation);

   switch (h % 6) {
      case 0:
         *r = (Uint8)(value * 255);
         *g = (Uint8)(t * 255);
         *b = (Uint8)(p * 255);
         break;
      case 1:
         *r = (Uint8)(q * 255);
         *g = (Uint8)(value * 255);
         *b = (Uint8)(p * 255);
         break;
      case 2:
         *r = (Uint8)(p * 255);
         *g = (Uint8)(value * 255);
         *b = (Uint8)(t * 255);
         break;
      case 3:
         *r = (Uint8)(p * 255);
         *g = (Uint8)(q * 255);
         *b = (Uint8)(value * 255);
         break;
      case 4:
         *r = (Uint8)(t * 255);
         *g = (Uint8)(p * 255);
         *b = (Uint8)(value * 255);
         break;
      case 5:
         *r = (Uint8)(value * 255);
         *g = (Uint8)(p * 255);
         *b = (Uint8)(q * 255);
         break;
   }
}

void parseRules(const char* ruleString, int born[], int survive[]) {
   int bIndex = 0, sIndex = 0;
   int i = 0;

   // Parcours de la chaîne de caractères
   while (ruleString[i] != '\0') {
      if (ruleString[i] == 'B') {
         i++;  // Passer le 'B'
         while (ruleString[i] >= '0' && ruleString[i] <= '9') {
            born[bIndex++] = ruleString[i++] - '0';
         }
         born[bIndex] = 0;  // Terminer par 0
      } else if (ruleString[i] == 'S') {
         i++;  // Passer le 'S'
         while (ruleString[i] >= '0' && ruleString[i] <= '9') {
            survive[sIndex++] = ruleString[i++] - '0';
         }
         survive[sIndex] = 0;  // Terminer par 0
      } else {
         i++;  // Passer les autres caractères (séparateurs ou caractères
               // inattendus)
      }
   }
}

// Fonction pour dessiner la grille
void draw_grid(SDL_Renderer* renderer, Cell grid[ROWS][COLS], int cell_size,
               bool history_mode, Uint32 current_time) {
   for (int i = 0; i < ROWS; ++i) {
      for (int j = 0; j < COLS; ++j) {
         SDL_Rect cell = {j * cell_size, i * cell_size, cell_size, cell_size};

         if (grid[i][j].alive) {
            SDL_SetRenderDrawColor(renderer, 0, 0, 0,
                                   255);  // Noir pour les cellules vivantes
            SDL_RenderFillRect(renderer, &cell);
         } else if (history_mode && grid[i][j].death_time > 0) {
            // Calculer le temps écoulé depuis la mort de la cellule
            Uint32 time_since_death = current_time - grid[i][j].death_time;
            if (time_since_death < TIME_TO_FADE_MS) {
               // Déterminer la couleur en fonction du temps écoulé
               double ratio = (double)time_since_death / TIME_TO_FADE_MS;

               // Commencer par un bleu très clair et passer à blanc
               double hue = ratio;  // Bleu en HSV
               double saturation = (1.0 - ratio) / 5.0;
               ;
               double value = 1.0;  // Toujours à pleine intensité

               Uint8 r, g, b;
               HSVtoRGB(hue, saturation, value, &r, &g, &b);

               SDL_SetRenderDrawColor(renderer, r, g, b, 255);
               SDL_RenderFillRect(renderer, &cell);
            }
         }

         // Toujours dessiner la grille par-dessus
         SDL_SetRenderDrawColor(renderer, 200, 200, 200,
                                255);  // Gris clair pour les bordures
         SDL_RenderDrawRect(renderer, &cell);
      }
   }
}

// Fonction pour compter les voisins vivants d'une cellule
int count_neighbors(Cell grid[ROWS][COLS], int x, int y) {
   int count = 0;
   for (int i = -1; i <= 1; ++i) {
      for (int j = -1; j <= 1; ++j) {
         if (i == 0 && j == 0) continue;  // Ignore la cellule elle-même
         int nx = x + i;
         int ny = y + j;
         if (nx >= 0 && nx < ROWS && ny >= 0 && ny < COLS &&
             grid[nx][ny].alive) {
            count++;
         }
      }
   }
   return count;
}

// Fonction pour mettre à jour la grille selon les règles du jeu de la vie
void update_grid(Cell grid[ROWS][COLS], char* rule, Uint32 current_time) {
   Cell new_grid[ROWS][COLS];

   int born[9] = {0};
   int survive[9] = {0};
   parseRules(rule, born, survive);

   for (int i = 0; i < ROWS; ++i) {
      for (int j = 0; j < COLS; ++j) {
         int neighbors = count_neighbors(grid, i, j);
         new_grid[i][j].alive = grid[i][j].alive;
         new_grid[i][j].death_time = grid[i][j].death_time;

         if (grid[i][j].alive) {
            if (inArray(survive, neighbors)) {
               new_grid[i][j].alive = true;
            } else {
               new_grid[i][j].alive = false;
               new_grid[i][j].death_time = current_time;
            }
         } else {
            if (inArray(born, neighbors)) {
               new_grid[i][j].alive = true;
               new_grid[i][j].death_time = 0;
            }
         }
      }
   }

   for (int i = 0; i < ROWS; ++i)
      for (int j = 0; j < COLS; ++j) grid[i][j] = new_grid[i][j];
}

void toggle_cell(Cell grid[ROWS][COLS], int x, int y, int cell_size,
                 Uint32 current_time) {
   int i = y / cell_size, j = x / cell_size;
   if (i >= 0 && i < ROWS && j >= 0 && j < COLS) {
      grid[i][j].alive = !grid[i][j].alive;
      grid[i][j].death_time = grid[i][j].alive ? 0 : current_time;
   }
}

int main(int argc, char* argv[]) {
   SDL_Init(SDL_INIT_VIDEO);
   srand(time(NULL));

   SDL_Window* window = SDL_CreateWindow(
       "Game of Life", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
       SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);

   SDL_Renderer* renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

   Cell grid[ROWS][COLS];
   init_grid(grid);
   insert_shape(grid, gosper_glider_gun,
                sizeof(gosper_glider_gun) / sizeof(gosper_glider_gun[0]), 10,
                10);

   SDL_Event event;

   int quit = 0;
   int cell_size = CELL_WIDTH;
   int delay = 100;
   bool running = false;
   bool history_mode = false;

   while (!quit) {
      Uint32 current_time = SDL_GetTicks();

      while (SDL_PollEvent(&event)) {
         if (event.type == SDL_QUIT) {
            quit = 1;
         } else if (event.type == SDL_MOUSEBUTTONDOWN &&
                    event.button.button == SDL_BUTTON_LEFT) {
            toggle_cell(grid, event.button.x, event.button.y, cell_size,
                        current_time);
         } else if (event.type == SDL_KEYDOWN) {
            if (event.key.keysym.sym == SDLK_SPACE) {
               running = !running;
            } else if (event.key.keysym.sym == SDLK_LEFT) {
               if (delay < 1000) delay += 10;
            } else if (event.key.keysym.sym == SDLK_RIGHT) {
               if (delay > 10) delay -= 10;
            } else if (event.key.keysym.sym == SDLK_h) {
               history_mode = !history_mode;  // Basculer le mode historique
            } else if (event.key.keysym.sym == SDLK_r) {
               randomize_grid(grid);
            }
         }
      }

      int width, height;
      SDL_GetWindowSize(window, &width, &height);
      cell_size = width / COLS;

      if (running) update_grid(grid, RULE_CONWAY, current_time);

      SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
      SDL_RenderClear(renderer);
      draw_grid(renderer, grid, cell_size, history_mode, current_time);

      SDL_RenderPresent(renderer);
      SDL_Delay(delay);
   }

   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
