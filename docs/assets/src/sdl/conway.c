#include <SDL2/SDL.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 800
#define WIDTH 10

#define ROWS (SCREEN_HEIGHT / WIDTH)
#define COLS (SCREEN_WIDTH / WIDTH)

#define TIME_TO_FADE 5000 // 30 seconds in milliseconds

typedef struct
{
    bool alive;
    Uint32 death_time; // Timestamp when the cell died
} Cell;

// Fonction pour initialiser le tableau avec un petit module en mouvement (glider)
void init_grid(Cell grid[ROWS][COLS])
{
    for (int i = 0; i < ROWS; ++i)
    {
        for (int j = 0; j < COLS; ++j)
        {
            grid[i][j].alive = false;
            grid[i][j].death_time = 0;
        }
    }

    // Ajouter un planeur (glider)
    grid[1][2].alive = true;
    grid[2][3].alive = true;
    grid[3][1].alive = true;
    grid[3][2].alive = true;
    grid[3][3].alive = true;
}

// Fonction pour randomiser la grille
void randomize_grid(Cell grid[ROWS][COLS])
{
    for (int i = 0; i < ROWS; ++i)
    {
        for (int j = 0; j < COLS; ++j)
        {
            grid[i][j].alive = rand() % 2;
            grid[i][j].death_time = grid[i][j].alive ? 0 : SDL_GetTicks();
        }
    }
}

// Convertir HSV en RGB (avec interpolation sur le hue)
void HSVtoRGB(double hue, double saturation, double value, Uint8 *r, Uint8 *g, Uint8 *b)
{
    int h = (int)(hue * 6);
    double f = hue * 6 - h;
    double p = value * (1 - saturation);
    double q = value * (1 - f * saturation);
    double t = value * (1 - (1 - f) * saturation);

    switch (h % 6)
    {
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

// Fonction pour dessiner la grille
void draw_grid(SDL_Renderer *renderer, Cell grid[ROWS][COLS], int cell_size, bool history_mode, Uint32 current_time)
{
    for (int i = 0; i < ROWS; ++i)
    {
        for (int j = 0; j < COLS; ++j)
        {
            SDL_Rect cell = {j * cell_size, i * cell_size, cell_size, cell_size};

            if (grid[i][j].alive)
            {
                SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Noir pour les cellules vivantes
                SDL_RenderFillRect(renderer, &cell);
            }
            else if (history_mode && grid[i][j].death_time > 0)
            {
                // Calculer le temps écoulé depuis la mort de la cellule
                Uint32 time_since_death = current_time - grid[i][j].death_time;
                if (time_since_death < TIME_TO_FADE)
                {
                    // Déterminer la couleur en fonction du temps écoulé
                    double ratio = (double)time_since_death / TIME_TO_FADE;

                    // Commencer par un bleu très clair et passer à blanc
                    double hue = ratio; // Bleu en HSV
                    double saturation = (1.0 - ratio) / 5.0;
                    ;
                    double value = 1.0; // Toujours à pleine intensité

                    Uint8 r, g, b;
                    HSVtoRGB(hue, saturation, value, &r, &g, &b);

                    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
                    SDL_RenderFillRect(renderer, &cell);
                }
            }

            // Toujours dessiner la grille par-dessus
            SDL_SetRenderDrawColor(renderer, 200, 200, 200, 255); // Gris clair pour les bordures
            SDL_RenderDrawRect(renderer, &cell);
        }
    }
}

// Fonction pour compter les voisins vivants d'une cellule
int count_neighbors(Cell grid[ROWS][COLS], int x, int y)
{
    int count = 0;
    for (int i = -1; i <= 1; ++i)
    {
        for (int j = -1; j <= 1; ++j)
        {
            if (i == 0 && j == 0)
                continue; // Ignore la cellule elle-même
            int nx = x + i;
            int ny = y + j;
            if (nx >= 0 && nx < ROWS && ny >= 0 && ny < COLS && grid[nx][ny].alive)
            {
                count++;
            }
        }
    }
    return count;
}

// Fonction pour mettre à jour la grille selon les règles du jeu de la vie
void update_grid(Cell grid[ROWS][COLS], Uint32 current_time)
{
    Cell new_grid[ROWS][COLS];

    for (int i = 0; i < ROWS; ++i)
    {
        for (int j = 0; j < COLS; ++j)
        {
            int neighbors = count_neighbors(grid, i, j);
            new_grid[i][j].alive = grid[i][j].alive;
            new_grid[i][j].death_time = grid[i][j].death_time;

            if (grid[i][j].alive)
            {
                // Cellule vivante
                if (neighbors == 2 || neighbors == 3)
                {
                    new_grid[i][j].alive = true;
                }
                else
                {
                    new_grid[i][j].alive = false;
                    new_grid[i][j].death_time = current_time;
                }
            }
            else
            {
                // Cellule morte
                if (neighbors == 3)
                {
                    new_grid[i][j].alive = true;
                    new_grid[i][j].death_time = 0; // Reset death time as it's alive now
                }
            }
        }
    }

    // Copier le nouveau tableau dans l'ancien
    for (int i = 0; i < ROWS; ++i)
    {
        for (int j = 0; j < COLS; ++j)
        {
            grid[i][j] = new_grid[i][j];
        }
    }
}

// Fonction pour inverser l'état d'une cellule avec un clic de souris
void toggle_cell(Cell grid[ROWS][COLS], int x, int y, int cell_size, Uint32 current_time)
{
    int i = y / cell_size;
    int j = x / cell_size;

    if (i >= 0 && i < ROWS && j >= 0 && j < COLS)
    {
        grid[i][j].alive = !grid[i][j].alive;
        if (!grid[i][j].alive)
        {
            grid[i][j].death_time = current_time;
        }
        else
        {
            grid[i][j].death_time = 0; // Reset death time as it's alive now
        }
    }
}

int main(int argc, char *argv[])
{
    SDL_Init(SDL_INIT_VIDEO);
    srand(time(NULL));

    SDL_Window *window = SDL_CreateWindow("Game of Life",
                                          SDL_WINDOWPOS_UNDEFINED,
                                          SDL_WINDOWPOS_UNDEFINED,
                                          SCREEN_WIDTH, SCREEN_HEIGHT,
                                          SDL_WINDOW_SHOWN);

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    Cell grid[ROWS][COLS];
    init_grid(grid);

    int quit = 0;
    SDL_Event event;
    int cell_size = WIDTH;
    bool running = false;      // Pour gérer l'état de lecture/pause
    int delay = 100;           // Délai pour visualiser les étapes (vitesse)
    bool history_mode = false; // Mode historique activé/désactivé

    while (!quit)
    {
        Uint32 current_time = SDL_GetTicks();

        while (SDL_PollEvent(&event))
        {
            if (event.type == SDL_QUIT)
            {
                quit = 1;
            }
            else if (event.type == SDL_MOUSEBUTTONDOWN && event.button.button == SDL_BUTTON_LEFT)
            {
                toggle_cell(grid, event.button.x, event.button.y, cell_size, current_time);
            }
            else if (event.type == SDL_KEYDOWN)
            {
                if (event.key.keysym.sym == SDLK_SPACE)
                {
                    running = !running; // Basculer entre lecture/pause
                }
                else if (event.key.keysym.sym == SDLK_LEFT)
                {
                    if (delay < 1000)
                    {
                        delay += 10; // Diminuer la vitesse
                    }
                }
                else if (event.key.keysym.sym == SDLK_RIGHT)
                {
                    if (delay > 10)
                    {
                        delay -= 10; // Augmenter la vitesse
                    }
                }
                else if (event.key.keysym.sym == SDLK_h)
                {
                    history_mode = !history_mode; // Basculer le mode historique
                }
                else if (event.key.keysym.sym == SDLK_r)
                {
                    randomize_grid(grid); // Randomiser la grille
                }
            }
        }

        // Ajuster la taille des cellules pour s'adapter à la largeur de la fenêtre
        int width, height;
        SDL_GetWindowSize(window, &width, &height);
        cell_size = width / COLS;

        if (running)
        {
            update_grid(grid, current_time);
        }

        // Mettre à jour et dessiner la grille
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Blanc pour le fond
        SDL_RenderClear(renderer);
        draw_grid(renderer, grid, cell_size, history_mode, current_time);

        SDL_RenderPresent(renderer);
        SDL_Delay(delay); // Délai pour visualiser les étapes
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}
