/* ast.h */
#ifndef AST_H
#define AST_H

typedef enum {
    NODE_TYPE_IDENTIFIER,
    NODE_TYPE_CONSTANT,
    NODE_TYPE_STRING,
    NODE_TYPE_BINARY_OP,
    NODE_TYPE_UNARY_OP,
    NODE_TYPE_FUNCTION_CALL,
    NODE_TYPE_STATEMENT,
    // ajoutez d'autres types de nœuds selon vos besoins
} NodeType;

typedef struct ASTNode {
    NodeType type;
    union {
        struct {
            char *name;
        } identifier;
        struct {
            int value;
        } constant;
        struct {
            char *value;
        } string;
        struct {
            struct ASTNode *left;
            struct ASTNode *right;
            char op;
        } binary_op;
        struct {
            struct ASTNode *operand;
            char op;
        } unary_op;
        struct {
            char *name;
            struct ASTNode **args;
            int arg_count;
        } function_call;
        struct {
            struct ASTNode **statements;
            int statement_count;
        } statement;
        // ajoutez d'autres types de nœuds selon vos besoins
    } data;
} ASTNode;

ASTNode *create_identifier_node(char *name);
ASTNode *create_constant_node(int value);
ASTNode *create_string_node(char *value);
ASTNode *create_binary_op_node(char op, ASTNode *left, ASTNode *right);
ASTNode *create_unary_op_node(char op, ASTNode *operand);
ASTNode *create_function_call_node(char *name, ASTNode **args, int arg_count);
ASTNode *create_statement_node(ASTNode **statements, int statement_count);
void print_ast(ASTNode *node);

#endif /* AST_H */
