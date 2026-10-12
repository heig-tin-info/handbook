#ifndef CALC_H
#define CALC_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Définition des types de nœuds de l'arbre syntaxique
typedef enum { NODE_NUMBER, NODE_OPERATOR, NODE_FUNCTION } NodeType;

typedef struct Node {
    NodeType type;
    union {
        double number;
        struct {
            char operator;
            struct Node* left;
            struct Node* right;
        } op;
        struct {
            char* function;
            struct Node* arg;
        } func;
    };
} Node;

Node* create_number_node(double value);
Node* create_operator_node(char operator, Node* left, Node* right);
Node* create_function_node(char* function, Node* arg);
void print_node(Node* node);
void free_node(Node* node);

#endif
