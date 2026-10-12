#include "stack.h"

#include <stdlib.h>

Stack stack_create() {
    Stack stack;
    stack.top = NULL;
    return stack;
}

void stack_push(Stack *stack, char value) {
    StackNode *newNode = (StackNode *)malloc(sizeof(StackNode));
    newNode->data = value;
    newNode->next = stack->top;
    stack->top = newNode;
}

char stack_pop(Stack *stack) {
    if (stack->top == NULL)
        return '\0';
    StackNode *node = stack->top;
    char value = node->data;
    stack->top = node->next;
    free(node);
    return value;
}

char stack_top(Stack *stack) {
    if (stack->top == NULL)
        return '\0';
    return stack->top->data;
}

int stack_empty(Stack *stack) {
    return stack->top == NULL;
}
