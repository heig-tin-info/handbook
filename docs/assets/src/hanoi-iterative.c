#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int n;
    char from;
    char to;
    char aux;
    int stage;
} Frame;

typedef struct {
    Frame *frames;
    int top;
    int max_size;
} Stack;

void init_stack(Stack *stack, int max_size) {
    stack->frames = (Frame *)malloc(max_size * sizeof(Frame));
    stack->top = -1;
    stack->max_size = max_size;
}

void push(Stack *stack, Frame frame) {
    if (stack->top < stack->max_size - 1) {
        stack->frames[++stack->top] = frame;
    }
}

Frame pop(Stack *stack) {
    if (stack->top >= 0) {
        return stack->frames[stack->top--];
    } else {
        Frame empty = {0, '\0', '\0', '\0', 0};
        return empty;
    }
}

int is_empty(Stack *stack) {
    return stack->top == -1;
}

void hanoi_iterative(int n, char from, char to, char aux) {
    Stack stack;
    init_stack(&stack, 100);  // Assuming the stack size to be 100, adjust if needed

    Frame initial_frame = {n, from, to, aux, 0};
    push(&stack, initial_frame);

    while (!is_empty(&stack)) {
        Frame current_frame = pop(&stack);

        switch (current_frame.stage) {
            case 0:
                if (current_frame.n == 1) {
                    printf("Déplacer le disque 1 de %c à %c\n", current_frame.from, current_frame.to);
                } else {
                    current_frame.stage = 1;
                    push(&stack, current_frame);

                    Frame new_frame = {current_frame.n - 1, current_frame.from, current_frame.aux, current_frame.to, 0};
                    push(&stack, new_frame);
                }
                break;

            case 1:
                printf("Déplacer le disque %d de %c à %c\n", current_frame.n, current_frame.from, current_frame.to);

                current_frame.stage = 2;
                push(&stack, current_frame);

                Frame new_frame = {current_frame.n - 1, current_frame.aux, current_frame.to, current_frame.from, 0};
                push(&stack, new_frame);
                break;
        }
    }
    free(stack.frames);
}

int main() {
    int n = 3;
    hanoi_iterative(n, 'A', 'C', 'B');
}
