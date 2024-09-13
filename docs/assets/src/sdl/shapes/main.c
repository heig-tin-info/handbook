#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>
#include <stdbool.h>
#include <stdio.h>

#define S(i) (sin(2 * M_PI / 3 * i))
#define C(i) (cos(2 * M_PI / 3 * i))

int main(int argc, char *argv[]) {
   if (SDL_Init(SDL_INIT_VIDEO) < 0) {
      fprintf(stderr, "Error: SDL Initialization: %s\n", SDL_GetError());
      exit(1);
   }
   SDL_Window *window =
       SDL_CreateWindow("Circles", SDL_WINDOWPOS_CENTERED,
                        SDL_WINDOWPOS_CENTERED, 800, 400, SDL_WINDOW_SHOWN);
   if (!window) {
      fprintf(stderr, "Error: CreateWindow: %s\n", SDL_GetError());
      exit(2);
   }
   SDL_Renderer *r = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
   if (!r) {
      fprintf(stderr, "Error: Renderer: %s\n", SDL_GetError());
      exit(3);
   }
   SDL_SetRenderDrawBlendMode(r, SDL_BLENDMODE_ADD);
   bool running = true;
   while (running) {
      SDL_Event event;
      while (SDL_PollEvent(&event))
         if (event.type == SDL_QUIT) running = false;
      SDL_SetRenderDrawColor(r, 255, 255, 255, 255);
      SDL_RenderClear(r);
      Sint16 cx = 400, cy = 200, d = 50;
      filledCircleRGBA(r, cx + d * C(1), cy + d * S(1), 100, 255, 0, 0, 100);
      filledCircleRGBA(r, cx + d * C(2), cy + d * S(2), 100, 0, 255, 0, 100);
      filledCircleRGBA(r, cx + d * C(3), cy + d * S(3), 100, 0, 0, 255, 100);
      SDL_RenderPresent(r);
   }
   SDL_DestroyRenderer(r);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
