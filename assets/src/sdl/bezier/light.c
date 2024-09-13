#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>  // Inclure SDL2_gfx
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#define GRIDSTEP 10
#define MAX_POINTS 100
const int WINDOW_WIDTH = 800, WINDOW_HEIGHT = 400;

const SDL_Color GRID_COLOR = {80, 80, 80, 200};
const SDL_Color BACKGROUND_COLOR = {30, 30, 30, 255};
const SDL_Color LINE_COLOR = {255, 0, 128, 255};
const SDL_Color ANCHOR_COLOR = {0, 255, 255, 150};

typedef struct Point {
   float x, y;
} Point;

typedef struct Segment {
   Point p, q;
} Segment;

typedef struct State {
   bool drawing;
   Point start, last, current;
   size_t segment_count;
   Segment segments[MAX_POINTS];
} State;

#define COLORARGS(color) color.r, color.g, color.b, color.a

void clear(SDL_Renderer *renderer) {
   SDL_SetRenderDrawColor(renderer, COLORARGS(BACKGROUND_COLOR));
   SDL_RenderClear(renderer);
}

void drawGrid(SDL_Renderer *renderer) {
   for (int x = 0; x < WINDOW_WIDTH; x += GRIDSTEP) {
      SDL_Color color = GRID_COLOR;
      color.a = x % 100 ? 100 : 200;
      SDL_SetRenderDrawColor(renderer, COLORARGS(color));
      SDL_RenderDrawLine(renderer, x, 0, x, WINDOW_HEIGHT);
   }
   for (int y = 0; y < WINDOW_HEIGHT; y += GRIDSTEP) {
      SDL_Color color = GRID_COLOR;
      color.a = y % 100 ? 100 : 200;
      SDL_SetRenderDrawColor(renderer, COLORARGS(color));
      SDL_RenderDrawLine(renderer, 0, y, WINDOW_WIDTH, y);
   }
}

void drawAnchor(SDL_Renderer *r, Point p, SDL_Color color) {
   const int size = 6, half = size / 2;
   SDL_SetRenderDrawColor(r, COLORARGS(color));
   SDL_RenderFillRect(r, &(SDL_Rect){p.x - half, p.y - half, size, size});
}

void drawSegment(SDL_Renderer *r, Segment s) {
   SDL_SetRenderDrawColor(r, COLORARGS(LINE_COLOR));
   SDL_RenderDrawLine(r, s.p.x, s.p.y, s.q.x, s.q.y);
   drawAnchor(r, s.p, ANCHOR_COLOR);
   drawAnchor(r, s.q, ANCHOR_COLOR);
}

void drawSegments(SDL_Renderer *renderer, Segment *segments, size_t count) {
   for (int i = 0; i < count; i++) drawSegment(renderer, segments[i]);
}

void addSegment(State *state) {
   if (state->segment_count >= MAX_POINTS) {
      fprintf(stderr, "Reached maximum number of points\n");
      return;
   }
   state->segments[state->segment_count++] =
       (Segment){.p = state->last, .q = state->current};
}

void endSegment(State *state) {
   state->drawing = false;
   addSegment(state);
}

bool isClose(Point p, Point q, int threshold) {
   return (fabs(p.x - q.x) < threshold) && (fabs(p.y - q.y) < threshold);
}

bool onStartAnchor(State state) {
   return isClose(state.start, state.current, 10);
}

int main(int argc, char *argv[]) {
   SDL_Init(SDL_INIT_VIDEO);
   SDL_Window *window = SDL_CreateWindow("Polygons", SDL_WINDOWPOS_CENTERED,
                                         SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH,
                                         WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
   SDL_Renderer *renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

   SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
   State state = {0};
   bool running = true;
   while (running) {
      SDL_Event event;
      while (SDL_PollEvent(&event)) {
         if (event.type == SDL_QUIT) {
            running = false;
            continue;
         }
         if (event.type == SDL_MOUSEMOTION) {
            state.current = (Point){event.button.x, event.button.y};
            continue;
         }
         if (event.type == SDL_MOUSEBUTTONDOWN &&
             event.button.button == SDL_BUTTON_LEFT) {
            if (!state.drawing) {
               state.drawing = true;
               state.start = state.current;
            } else if (onStartAnchor(state)) {
               state.current = state.start;
               endSegment(&state);
            } else {
               addSegment(&state);
            }
            state.last = state.current;
         }
      }
      clear(renderer);
      drawGrid(renderer);
      drawSegments(renderer, state.segments, state.segment_count);
      if (state.start.x >= 0 && state.start.y >= 0)
         drawAnchor(renderer, state.start, ANCHOR_COLOR);
      if (state.drawing)
         drawSegment(renderer, (Segment){.p = state.last, .q = state.current});
      SDL_RenderPresent(renderer);
   }
   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
