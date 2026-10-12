#include "calc.h"

Node* create_number_node(double value) {
    Node* node = malloc(sizeof(Node));
    node->type = NODE_NUMBER;
    node->number = value;
    return node;
}

Node* create_operator_node(char operator, Node* left, Node* right) {
    Node* node = malloc(sizeof(Node));
    node->type = NODE_OPERATOR;
    node->op.operator = operator;
    node->op.left = left;
    node->op.right = right;
    return node;
}

Node* create_function_node(char* function, Node* arg) {
    Node* node = malloc(sizeof(Node));
    node->type = NODE_FUNCTION;
    node->func.function = function;
    node->func.arg = arg;
    return node;
}

void print_node(Node* node) {
    if (node->type == NODE_NUMBER) {
        printf("%f", node->number);
    } else if (node->type == NODE_OPERATOR) {
        printf("(");
        print_node(node->op.left);
        printf(" %c ", node->op.operator);
        print_node(node->op.right);
        printf(")");
    } else if (node->type == NODE_FUNCTION) {
        printf("%s(", node->func.function);
        print_node(node->func.arg);
        printf(")");
    }
}

void free_node(Node* node) {
    if (node->type == NODE_OPERATOR) {
        free_node(node->op.left);
        free_node(node->op.right);
    } else if (node->type == NODE_FUNCTION) {
        free_node(node->func.arg);
    }
    free(node);
}
