#include <SDL2/SDL.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>

#define WIDTH 800
#define HEIGHT 400

int16_t fpsin(int16_t i) {
   i <<= 1;
   uint8_t c = i < 0;

   if (i == (i | 0x4000)) i = (1 << 15) - i;
   i = (i & 0x7FFF) >> 1;

   enum { A1 = 3370945099UL, B1 = 2746362156UL, C1 = 292421UL };
   enum { n = 13, p = 32, q = 31, r = 3, a = 12 };

   uint32_t y = (C1 * ((uint32_t)i)) >> n;
   y = B1 - (((uint32_t)i * y) >> r);
   y = (uint32_t)i * (y >> n);
   y = (uint32_t)i * (y >> n);
   y = A1 - (y >> (p - q));
   y = (uint32_t)i * (y >> n);
   y = (y + (1UL << (q - a - 1))) >> (q - a);

   return c ? -y : y;
}

void draw_graph(SDL_Renderer *renderer) {
   for (int x = 0; x < WIDTH; x++) {
      // Mappe x à un angle (entre 0 et 2pi)
      double angle = (double)x / WIDTH * 2.0 * M_PI;
      int16_t angle_fixed = (int16_t)(angle * 32768.0 / (2.0 * M_PI));
      int16_t y_fixed = (fpsin(angle_fixed) / 4096.0) * HEIGHT / 2 + HEIGHT / 2;
      int y_standard = (int)((sin(angle) * HEIGHT / 2) + HEIGHT / 2);

      // Sinus standard en rouge
      SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
      SDL_RenderDrawPoint(renderer, x, y_standard);

      // Sinus en virgule fixe en vert
      SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255);
      SDL_RenderDrawPoint(renderer, x, y_fixed);

      // Erreur en bleu
      int error =
          (sin(angle) - ((double)fpsin(angle_fixed) / 4096.0)) * 80000.0;
      SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
      SDL_RenderDrawPoint(renderer, x, HEIGHT / 2 - error);
   }
}

int main(int argc, char *argv[]) {
   SDL_Window *window = NULL;
   SDL_Renderer *renderer = NULL;

   if (SDL_Init(SDL_INIT_VIDEO) < 0) {
      printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
      return 1;
   }

   window = SDL_CreateWindow("Sinus Approximation", SDL_WINDOWPOS_UNDEFINED,
                             SDL_WINDOWPOS_UNDEFINED, WIDTH, HEIGHT,
                             SDL_WINDOW_SHOWN);
   renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

   SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
   SDL_RenderClear(renderer);

   draw_graph(renderer);
   SDL_RenderPresent(renderer);

   SDL_Event e;
   int quit = 0;
   while (!quit) {
      while (SDL_PollEvent(&e) != 0) {
         if (e.type == SDL_QUIT) {
            quit = 1;
         }
      }
   }

   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}