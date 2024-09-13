#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>  // Inclure SDL2_gfx
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#define GRIDSTEP 10
#define MAX_POINTS 100
const int WINDOW_WIDTH = 800, WINDOW_HEIGHT = 400;

const SDL_Color GRID_COLOR = {100, 100, 100, 255};
const SDL_Color BACKGROUND_COLOR = {40, 40, 40, 255};
const SDL_Color LINE_COLOR = {255, 0, 128, 255};
const SDL_Color ANCHOR_COLOR = {0, 255, 255, 255};
const SDL_Color BEZIER_ANCHOR_COLOR = {255, 255, 0, 255};

typedef struct Point {
   float x, y;
} Point;

typedef struct Segment {
   Point p0, p1, control;
   bool isBezier;
} Segment;

typedef struct State {
   bool drawing;
   bool isBezierMode;
   Point start;    // Start of polyline
   Point last;     // Last point of polyline
   Point current;  // Current point of polyline
   Point control;  // Bezier control point

   size_t segment_count;
   Segment segments[MAX_POINTS];
   size_t paths_count;
   size_t paths[MAX_POINTS];
} State;

#define COLORARGS(color) color.r, color.g, color.b, color.a

void clear(SDL_Renderer *renderer) {
   SDL_SetRenderDrawColor(renderer, COLORARGS(BACKGROUND_COLOR));
   SDL_RenderClear(renderer);
}

void drawGrid(SDL_Renderer *renderer) {
   for (int x = 0; x < WINDOW_WIDTH; x += GRIDSTEP) {
      SDL_Color color = GRID_COLOR;
      color.a = x % 100 ? 100 : 255;
      SDL_SetRenderDrawColor(renderer, COLORARGS(color));
      SDL_RenderDrawLine(renderer, x, 0, x, WINDOW_HEIGHT);
   }
   for (int y = 0; y < WINDOW_HEIGHT; y += GRIDSTEP) {
      SDL_Color color = GRID_COLOR;
      color.a = y % 100 ? 100 : 255;
      SDL_SetRenderDrawColor(renderer, COLORARGS(color));
      SDL_RenderDrawLine(renderer, 0, y, WINDOW_WIDTH, y);
   }
}

void drawAnchor(SDL_Renderer *renderer, Point p, SDL_Color color) {
   const int size = 6;
   SDL_SetRenderDrawColor(renderer, COLORARGS(color));
   SDL_RenderFillRect(renderer,
                      &(SDL_Rect){p.x - size / 2, p.y - size / 2, size, size});
}

Point bezier(Point p0, Point p1, Point p2, float t) {
   const float it = 1.f - t;
   return (Point){.x = it * it * p0.x + 2 * it * t * p1.x + t * t * p2.x,
                  .y = it * it * p0.y + 2 * it * t * p1.y + t * t * p2.y};
}

Point get_bezier_control_point(Segment s, Point p) {
   Point control;
   if (s.isBezier) {
      float dx = s.p1.x - s.control.x, dy = s.p1.y - s.control.y;
      control.x = s.p1.x + dx / 2;
      control.y = s.p1.y + dy / 2;
   } else {
      float dx = s.p1.x - s.p0.x, dy = s.p1.y - s.p0.y;
      float perp_dx = -dy, perp_dy = dx;
      control.x = p.x + perp_dx / 2;
      control.y = p.y + perp_dy / 2;
   }
   return control;
}

Point set_bezier_control_point(State *s) {
   if (s->segment_count > 0)
      s->control = get_bezier_control_point(s->segments[s->segment_count - 1],
                                            s->current);
   return s->control;
}

void drawBezierCurve(SDL_Renderer *renderer, Segment segment) {
   Point prev = segment.p0;
   for (float t = 0.0; t <= 1.0; t += 0.01) {
      Point current = bezier(segment.p0, segment.control, segment.p1, t);
      SDL_RenderDrawLine(renderer, prev.x, prev.y, current.x, current.y);
      prev = current;
   }
}

void drawSegment(SDL_Renderer *renderer, Segment s) {
   SDL_SetRenderDrawColor(renderer, COLORARGS(LINE_COLOR));
   if (s.isBezier) {
      drawBezierCurve(renderer, s);
      drawAnchor(renderer, s.control, BEZIER_ANCHOR_COLOR);
   } else {
      SDL_RenderDrawLine(renderer, s.p0.x, s.p0.y, s.p1.x, s.p1.y);
   }
   drawAnchor(renderer, s.p0, ANCHOR_COLOR);
   drawAnchor(renderer, s.p1, ANCHOR_COLOR);
}

bool isClosePQ(Point p, Point q, int threshold) {
   return (fabs(p.x - q.x) < threshold) && (fabs(p.y - q.y) < threshold);
}

void fillClosedPolygon(SDL_Renderer *renderer, State *state) {
   for (size_t i = 0; i < state->paths_count; i++) {
      size_t start_idx = (i == 0) ? 0 : state->paths[i - 1];
      size_t end_idx = state->paths[i] - 1;
      Point start_point = state->segments[start_idx].p0;
      Point end_point = state->segments[end_idx].p1;
      if (isClosePQ(start_point, end_point, 5)) {
         Sint16 vx[MAX_POINTS], vy[MAX_POINTS];
         int n_points = 0;
         for (size_t j = start_idx; j <= end_idx; j++) {
            vx[n_points] = state->segments[j].p0.x;
            vy[n_points] = state->segments[j].p0.y;
            n_points++;
         }
         filledPolygonRGBA(renderer, vx, vy, n_points, 255, 0, 128, 26);
      }
   }
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
       (Segment){.p0 = state->last,
                 .p1 = state->current,
                 .isBezier = state->isBezierMode,
                 .control = state->control};
}

void endSegment(State *state) {
   state->drawing = false;
   addSegment(state);
   state->paths[state->paths_count++] = state->segment_count;
}

bool onStartAnchor(State state) {
   if (state.start.x < 0 || state.start.y < 0) return false;
   return isClosePQ(state.start, state.current, 10);
}

#define EVENT_MOUSE_LEFT_CLICK(event) \
   (event.type == SDL_MOUSEBUTTONDOWN && event.button.button == SDL_BUTTON_LEFT)

#define EVENT_MOUSE_MOVED(event) (event.type == SDL_MOUSEMOTION)

#define EVENT_MOUSE_LEFT_RELEASE(event) \
   (event.type == SDL_MOUSEBUTTONUP && event.button.button == SDL_BUTTON_LEFT)

#define EVENT_DELETE(event)                                                 \
   (event.type == SDL_KEYDOWN && (event.key.keysym.sym == SDLK_BACKSPACE || \
                                  event.key.keysym.sym == SDLK_DELETE))

#define EVENT_FINISH(event)                                               \
   ((event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_RETURN) || \
    (event.type == SDL_MOUSEBUTTONDOWN && event.button.clicks == 2))

#define EVENT_QUIT(event)     \
   (event.type == SDL_QUIT || \
    (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE))

int main(int argc, char *argv[]) {
   if (SDL_Init(SDL_INIT_VIDEO) < 0) {
      fprintf(stderr, "Error: SDL Initialization: %s\n", SDL_GetError());
      exit(1);
   }

   SDL_Window *window = SDL_CreateWindow("Bezier", SDL_WINDOWPOS_CENTERED,
                                         SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH,
                                         WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
   if (!window) {
      fprintf(stderr, "Error: CreateWindow: %s\n", SDL_GetError());
      exit(2);
   }

   SDL_Renderer *renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
   if (!renderer) {
      fprintf(stderr, "Error: Renderer: %s\n", SDL_GetError());
      exit(3);
   }

   SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
   State state = {.drawing = false, .start = {-1, -1}, .current = {-1, -1}};

   bool running = true;
   while (running) {
      SDL_Event event;
      while (SDL_PollEvent(&event)) {
         if (EVENT_QUIT(event)) {
            running = false;
            continue;
         }
         if (EVENT_MOUSE_MOVED(event)) {
            state.current = (Point){event.button.x, event.button.y};
            state.isBezierMode |= event.motion.state & SDL_BUTTON_LMASK;

            if (state.isBezierMode) {
               state.control = set_bezier_control_point(&state);
            }
            continue;
         }
         if (EVENT_FINISH(event)) {
            endSegment(&state);
            continue;
         }
         if (EVENT_DELETE(event) && state.drawing && state.segment_count > 0) {
            state.last = state.segments[state.segment_count - 1].p0;
            state.segment_count--;
            continue;
         }
         if (EVENT_MOUSE_LEFT_CLICK(event)) {
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
            state.isBezierMode = false;
         }
         if (EVENT_MOUSE_LEFT_RELEASE(event) && state.isBezierMode) {
            endSegment(&state);
         }
      }

      clear(renderer);
      drawGrid(renderer);
      fillClosedPolygon(renderer, &state);
      drawSegments(renderer, state.segments, state.segment_count);
      if (state.start.x >= 0 && state.start.y >= 0) {
         drawAnchor(renderer, state.start, ANCHOR_COLOR);
      }
      if (state.drawing) {
         drawSegment(renderer, (Segment){.p0 = state.last,
                                         .p1 = state.current,
                                         .isBezier = state.isBezierMode,
                                         .control = state.control});
      }
      SDL_RenderPresent(renderer);
   }
   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
