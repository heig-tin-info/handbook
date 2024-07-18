#include "queue.h"
#include "stack.h"

#include <stdio.h>
#include <ctype.h>

int main() {
    Stack stack = stack_create();
    Queue output = queue_create();
    Queue input = queue_create();

    // Load expression in input queue
    while (!feof(stdin)) {
        char token;
        scanf("%c", &token);
        if (isspace(token))
            continue;
        queue_push(&input, token);
    }

    // Shunting yard algorithm
    while (!queue_empty(&input)) {
        char token = queue_pop(&input);
        if (isdigit(token))
            queue_push(&output, token);
        else if (token == '(')
            stack_push(&stack, token);
        else if (token == ')') {
            while (stack_top(&stack) != '(')
                queue_push(&output, stack_pop(&stack));
            stack_pop(&stack);
        } else {
            while (!stack_empty(&stack) && stack_top(&stack) != '(')
                queue_push(&output, stack_pop(&stack));
            stack_push(&stack, token);
        }
    }
    while (!stack_empty(&stack))
        queue_push(&output, stack_pop(&stack));

    // Display output queue
    while (!queue_empty(&output))
        printf("%c", queue_pop(&output));
}
