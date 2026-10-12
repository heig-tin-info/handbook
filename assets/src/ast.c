/* ast.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

ASTNode *create_identifier_node(char *name) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_TYPE_IDENTIFIER;
    node->data.identifier.name = strdup(name);
    return node;
}

ASTNode *create_constant_node(int value) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_TYPE_CONSTANT;
    node->data.constant.value = value;
    return node;
}

ASTNode *create_string_node(char *value) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_TYPE_STRING;
    node->data.string.value = strdup(value);
    return node;
}

ASTNode *create_binary_op_node(char op, ASTNode *left, ASTNode *right) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_TYPE_BINARY_OP;
    node->data.binary_op.op = op;
    node->data.binary_op.left = left;
    node->data.binary_op.right = right;
    return node;
}

ASTNode *create_unary_op_node(char op, ASTNode *operand) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_TYPE_UNARY_OP;
    node->data.unary_op.op = op;
    node->data.unary_op.operand = operand;
    return node;
}

ASTNode *create_function_call_node(char *name, ASTNode **args, int arg_count) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_TYPE_FUNCTION_CALL;
    node->data.function_call.name = strdup(name);
    node->data.function_call.args = args;
    node->data.function_call.arg_count = arg_count;
    return node;
}

ASTNode *create_statement_node(ASTNode **statements, int statement_count) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_TYPE_STATEMENT;
    node->data.statement.statements = statements;
    node->data.statement.statement_count = statement_count;
    return node;
}

void print_ast(ASTNode *node) {
    if (!node) return;
    switch (node->type) {
        case NODE_TYPE_IDENTIFIER:
            printf("Identifier: %s\n", node->data.identifier.name);
            break;
        case NODE_TYPE_CONSTANT:
            printf("Constant: %d\n", node->data.constant.value);
            break;
        case NODE_TYPE_STRING:
            printf("String: %s\n", node->data.string.value);
            break;
        case NODE_TYPE_BINARY_OP:
            printf("Binary Operation: %c\n", node->data.binary_op.op);
            print_ast(node->data.binary_op.left);
            print_ast(node->data.binary_op.right);
            break;
        case NODE_TYPE_UNARY_OP:
            printf("Unary Operation: %c\n", node->data.unary_op.op);
            print_ast(node->data.unary_op.operand);
            break;
        case NODE_TYPE_FUNCTION_CALL:
            printf("Function Call: %s\n", node->data.function_call.name);
            for (int i = 0; i < node->data.function_call.arg_count; i++) {
                print_ast(node->data.function_call.args[i]);
            }
            break;
        case NODE_TYPE_STATEMENT:
            printf("Statement:\n");
            for (int i = 0; i < node->data.statement.statement_count; i++) {
                print_ast(node->data.statement.statements[i]);
            }
            break;
        // ajoutez d'autres types de nœuds selon vos besoins
    }
}
