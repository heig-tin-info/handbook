#pragma once

typedef struct StackNode {
    char data;
    struct StackNode *next;
} StackNode;

typedef struct {
    StackNode *top;
} Stack;

Stack stack_create();
void stack_push(Stack *stack, char value);
char stack_pop(Stack *stack);
char stack_top(Stack *stack);
int stack_empty(Stack *stack);
