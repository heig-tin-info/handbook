#include <SDL2/SDL.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 400

typedef struct Node {
   int id;
   double x, y;
   struct Node *left, *right;
} Node;

typedef struct SearchArea {
   double x, y, radius;
} SearchArea;

typedef struct {
   Node* node;       // Pointeur vers le nœud le plus proche trouvé
   double distance;  // Distance du point à ce nœud
} ClosestNode;

void fill_circle(SDL_Renderer* renderer, int cx, int cy, int radius) {
   for (int w = 0; w < radius * 2; w++) {
      for (int h = 0; h < radius * 2; h++) {
         int dx = radius - w;
         int dy = radius - h;
         if ((dx * dx + dy * dy) <= (radius * radius))
            SDL_RenderDrawPoint(renderer, cx + dx, cy + dy);
      }
   }
}

Node* insert(Node* root, Node* new_node, int depth) {
   if (root == NULL) return new_node;

   int cd = depth % 2;

   if ((cd == 0 && new_node->x < root->x) || (cd == 1 && new_node->y < root->y))
      root->left = insert(root->left, new_node, depth + 1);
   else
      root->right = insert(root->right, new_node, depth + 1);

   return root;
}

void draw_tree(SDL_Renderer* r, Node* root, int depth, int minX, int maxX,
               int minY, int maxY) {
   if (root == NULL) return;
   if (depth % 2 == 0) {
      SDL_SetRenderDrawColor(r, 255, 0, 0, 255);
      SDL_RenderDrawLine(r, (int)root->x, minY, (int)root->x, maxY);
      draw_tree(r, root->left, depth + 1, minX, (int)root->x, minY, maxY);
      draw_tree(r, root->right, depth + 1, (int)root->x, maxX, minY, maxY);
   } else {
      SDL_SetRenderDrawColor(r, 0, 255, 0, 255);
      SDL_RenderDrawLine(r, minX, (int)root->y, maxX, (int)root->y);
      draw_tree(r, root->left, depth + 1, minX, maxX, minY, (int)root->y);
      draw_tree(r, root->right, depth + 1, minX, maxX, (int)root->y, maxY);
   }

   SDL_SetRenderDrawColor(r, 0, 0, 0, 255);
   fill_circle(r, (int)root->x, (int)root->y, 3);
}

void draw_search_area(SDL_Renderer* renderer, SearchArea* area) {
   SDL_SetRenderDrawColor(renderer, 10, 30, 255, 60);
   fill_circle(renderer, (int)area->x, (int)area->y, (int)area->radius);
}

double distance(Node* node, SearchArea* area) {
   return sqrt((node->x - area->x) * (node->x - area->x) +
               (node->y - area->y) * (node->y - area->y));
}

double squared_distance(double x1, double y1, double x2, double y2) {
   return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
}

void radius_search(Node* root, SDL_Renderer* renderer, SearchArea* area,
                   int depth) {
   if (root == NULL) return;

   if (distance(root, area) <= area->radius) {
      SDL_SetRenderDrawColor(renderer, 0, 0, 255, 60);
      fill_circle(renderer, (int)root->x, (int)root->y, 8);
   }

   int cd = depth % 2;

   if ((cd == 0 && area->x - area->radius < root->x) ||
       (cd == 1 && area->y - area->radius < root->y)) {
      radius_search(root->left, renderer, area, depth + 1);
   }

   if ((cd == 0 && area->x + area->radius >= root->x) ||
       (cd == 1 && area->y + area->radius >= root->y)) {
      radius_search(root->right, renderer, area, depth + 1);
   }
}

void search_closest(Node* root, double x, double y, int depth,
                    ClosestNode* closest) {
   if (root == NULL) return;

   double d = squared_distance(root->x, root->y, x, y);
   if (d < closest->distance) {
      closest->node = root;
      closest->distance = d;
   }

   int cd = depth % 2;

   // Quelle sous-arborescence est la plus proche ?
   Node* nearer_subtree = NULL;
   Node* farther_subtree = NULL;
   if ((cd == 0 && x < root->x) || (cd == 1 && y < root->y)) {
      nearer_subtree = root->left;
      farther_subtree = root->right;
   } else {
      nearer_subtree = root->right;
      farther_subtree = root->left;
   }

   // Rechercher d'abord dans la sous-arborescence la plus proche
   search_closest(nearer_subtree, x, y, depth + 1, closest);

   // Vérifier si nous devons explorer la sous-arborescence plus éloignée
   double dist_to_plane = (cd == 0) ? (x - root->x) : (y - root->y);
   if (dist_to_plane * dist_to_plane < closest->distance)
      search_closest(farther_subtree, x, y, depth + 1, closest);
}

ClosestNode find_closest(Node* root, double x, double y) {
   ClosestNode closest;
   closest.node = NULL;
   closest.distance = DBL_MAX;

   search_closest(root, x, y, 0, &closest);
   return closest;
}

void handle_events(SDL_Event* event, Node** root, SearchArea* area,
                   int* running) {
   if (event->type == SDL_QUIT) {
      *running = 0;
   } else if (event->type == SDL_MOUSEBUTTONDOWN) {
      int x = event->button.x;
      int y = event->button.y;
      if (event->button.button == SDL_BUTTON_LEFT) {
         Node* new_node = (Node*)malloc(sizeof(Node));
         new_node->x = x;
         new_node->y = y;
         new_node->left = new_node->right = NULL;
         *root = insert(*root, new_node, 0);
      } else if (event->button.button == SDL_BUTTON_RIGHT) {
         // Implement deletion logic here if desired
      } else if (event->button.button == SDL_BUTTON_MIDDLE) {
         area->x = x;
         area->y = y;
      }
   } else if (event->type == SDL_MOUSEWHEEL) {
      if (event->wheel.y > 0) {
         area->radius += 2;
      } else if (event->wheel.y < 0) {
         area->radius -= 2;
         if (area->radius < 2) area->radius = 2;
      }
   }
}

int main(int argc, char* argv[]) {
   if (SDL_Init(SDL_INIT_VIDEO) < 0) {
      printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
      return 1;
   }

   SDL_Window* window = SDL_CreateWindow(
       "K-D Tree Visualization", SDL_WINDOWPOS_UNDEFINED,
       SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
   if (window == NULL) {
      printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
      return 1;
   }

   SDL_Renderer* renderer =
       SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
   if (renderer == NULL) {
      printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
      return 1;
   }

   Node* root = NULL;

   SearchArea search_area = {32, 23, 37.5};

   int running = 1;
   SDL_Event event;

   SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);

   while (running) {
      while (SDL_PollEvent(&event) != 0)
         handle_events(&event, &root, &search_area, &running);

      SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
      SDL_RenderClear(renderer);
      draw_tree(renderer, root, 0, 0, SCREEN_WIDTH, 0, SCREEN_HEIGHT);
      draw_search_area(renderer, &search_area);
      radius_search(root, renderer, &search_area, 0);
      ClosestNode closest = find_closest(root, search_area.x, search_area.y);
      if (closest.node != NULL) {
         SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
         fill_circle(renderer, (int)closest.node->x, (int)closest.node->y, 8);
      }
      SDL_RenderPresent(renderer);
   }
   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();
}
