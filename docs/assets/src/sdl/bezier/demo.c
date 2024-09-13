#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>
#include <math.h>
#include <stdbool.h>

typedef struct {
   float x, y;
} Point;

typedef struct {
   Point p, q, control;
} Segment;

Point bezier(Point p, Point q, Point p2, float t) {
   float it = 1.f - t;
   return (Point){.x = it * it * p.x + 2 * it * t * q.x + t * t * p2.x,
                  .y = it * it * p.y + 2 * it * t * q.y + t * t * p2.y};
}

void drawBezierCurve(SDL_Renderer *renderer, Segment segment) {
   Point prev = segment.p;
   for (float t = 0.0; t <= 1.0; t += 0.05) {
      Point current = bezier(segment.p, segment.control, segment.q, t);
      SDL_RenderDrawLine(renderer, prev.x, prev.y, current.x, current.y);
      prev = current;
   }
}

void drawThickBezier(SDL_Renderer *renderer, Segment segment, int thickness) {
   Sint16 x[3] = {(Sint16)segment.p.x, (Sint16)segment.control.x,
                  (Sint16)segment.q.x};
   Sint16 y[3] = {(Sint16)segment.p.y, (Sint16)segment.control.y,
                  (Sint16)segment.q.y};

   for (int i = -thickness / 2; i <= thickness / 2; i++) {
      for (int j = -thickness / 2; j <= thickness / 2; j++) {
         Sint16 offset_x[3] = {x[0] + i, x[1] + i, x[2] + i};
         Sint16 offset_y[3] = {y[0] + j, y[1] + j, y[2] + j};
         bezierRGBA(renderer, offset_x, offset_y, 3, 5, 0, 0, 0, 200);
      }
   }
}

int main() {
   SDL_Init(SDL_INIT_VIDEO);
   SDL_Window *window =
       SDL_CreateWindow("Bezier Curve", SDL_WINDOWPOS_UNDEFINED,
                        SDL_WINDOWPOS_UNDEFINED, 800, 400, 0);
   SDL_Renderer *renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

   SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "1");

   SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
   Segment segment = {{400, 200}, {400, 200}, {400, 100}};
   bool running = true;
   bool controlClicked = false;

   while (running) {
      SDL_Event event;
      while (SDL_PollEvent(&event)) {
         if (event.type == SDL_QUIT) {
            running = false;
         } else if (event.type == SDL_MOUSEBUTTONDOWN) {
            int mouseX = event.button.x;
            int mouseY = event.button.y;
            if (sqrt((segment.control.x - mouseX) *
                         (segment.control.x - mouseX) +
                     (segment.control.y - mouseY) *
                         (segment.control.y - mouseY)) < 10) {
               controlClicked = true;
            }
         } else if (event.type == SDL_MOUSEBUTTONUP) {
            controlClicked = false;
         } else if (event.type == SDL_MOUSEMOTION) {
            if (controlClicked) {
               segment.control.x = event.motion.x;
               segment.control.y = event.motion.y;
            }
            segment.q.x = event.motion.x;
            segment.q.y = event.motion.y;
         }
      }

      SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
      SDL_RenderClear(renderer);

      SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
      // drawBezierCurve(renderer, segment);
      drawThickBezier(renderer, segment, 2);
      //   SDL_SetRenderDrawColor(renderer, 128, 0, 0, 128);
      //   SDL_RenderDrawLine(renderer, segment.p.x, segment.p.y, segment.q.x,
      //                      segment.q.y);

      SDL_SetRenderDrawColor(renderer, 0, 128, 100, 80);
      SDL_RenderDrawLine(renderer, segment.p.x, segment.p.y, segment.control.x,
                         segment.control.y);
      SDL_RenderDrawLine(renderer, segment.control.x, segment.control.y,
                         segment.q.x, segment.q.y);

      SDL_SetRenderDrawColor(renderer, 100, 0, 100, 100);
      SDL_Rect controlRect = {segment.control.x - 4, segment.control.y - 4, 8,
                              8};
      SDL_RenderFillRect(renderer, &controlRect);

      SDL_RenderPresent(renderer);
   }

   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
