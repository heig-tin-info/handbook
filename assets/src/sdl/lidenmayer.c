#include <SDL2/SDL.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h> // Pour getopt

#define SCREEN_WIDTH 500
#define SCREEN_HEIGHT 500

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct lsystem
{
    char axiom[128];
    char rule[128];
    unsigned int iterations;
    double angle;
    double length;
} Lsystem;

// Fonction pour générer la chaîne L-System
void generate(Lsystem sys, char *output, size_t size)
{
    char *temp = malloc(size);
    if (temp == NULL)
        exit(1);
    strcpy(output, sys.axiom);
    for (int i = 0; i < sys.iterations; ++i)
    {
        strcpy(temp, output);
        output[0] = '\0';
        for (char *p = temp; *p != '\0'; p++)
        {
            if (*p >= 'A' && *p <= 'Z')
            {
                strncat(output, sys.rule, size - strlen(output) - 1);
            }
            else
            {
                strncat(output, (char[]){*p, '\0'}, size - strlen(output) - 1);
            }
        }
    }
    free(temp);
}

// Fonction pour dessiner le L-System avec SDL
void draw(SDL_Renderer *renderer, const char *instructions, Lsystem sys)
{
    double x = SCREEN_WIDTH / 2;
    double y = SCREEN_HEIGHT;
    double direction = -M_PI / 2;
    double stack[1024];
    int stack_ptr = 0;
    int depth = 0;

    SDL_SetRenderDrawColor(renderer, 31, 36, 48, 255);
    SDL_RenderClear(renderer);

    for (const char *p = instructions; *p != '\0'; p++)
    {
        switch (*p)
        {
        case 'F':
        {
            // Change color based on depth (realism: darker for trunk, lighter for branches)
            if (depth < 2)
            {
                SDL_SetRenderDrawColor(renderer, 139, 69, 19, 255); // Trunk: Brown
            }
            else if (depth < 4)
            {
                SDL_SetRenderDrawColor(renderer, 34, 139, 34, 255); // Branches: Green
            }
            else
            {
                SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255); // Leaves: Light Green
            }
            double new_x = x + cos(direction) * sys.length;
            double new_y = y + sin(direction) * sys.length;
            SDL_RenderDrawLine(renderer, (int)x, (int)y, (int)new_x, (int)new_y);
            x = new_x;
            y = new_y;
            break;
        }
        case '+':
            direction += sys.angle * M_PI / 180;
            break;
        case '-':
            direction -= sys.angle * M_PI / 180;
            break;
        case '[':
            stack[stack_ptr++] = x;
            stack[stack_ptr++] = y;
            stack[stack_ptr++] = direction;
            depth++;
            break;
        case ']':
            direction = stack[--stack_ptr];
            y = stack[--stack_ptr];
            x = stack[--stack_ptr];
            depth--;
            break;
        }
    }
    SDL_RenderPresent(renderer);
}

int main(int argc, char *argv[])
{
    Lsystem system = {
        .axiom = "F",
        .rule = "FF-[-F+F+F]+[+F-FF-FF]",
        .iterations = 4,
        .angle = 22,
        .length = 6};

    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *window = SDL_CreateWindow("L-System SDL Example",
                                          SDL_WINDOWPOS_UNDEFINED,
                                          SDL_WINDOWPOS_UNDEFINED,
                                          SCREEN_WIDTH, SCREEN_HEIGHT,
                                          SDL_WINDOW_SHOWN);

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    char instructions[100000];
    generate(system, instructions, sizeof(instructions));
    draw(renderer, instructions, system);

    int quit = 0;
    SDL_Event event;
    while (!quit)
    {
        while (SDL_PollEvent(&event))
            if (event.type == SDL_QUIT)
                quit = 1;
        SDL_Delay(1000 / 60);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}
