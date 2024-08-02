%{
#include "calc.h"

int yylex(void);
void yyerror(const char *s);
%}

%union {
    double number;
    Node* node;
    char* function;
}

%token <number> NUMBER
%token <function> FUNCTION
%left '+' '-'
%left '*' '/'
%type <node> expression term factor

%%

expression
    : term { $$ = $1; }
    | expression '+' term { $$ = create_operator_node('+', $1, $3); }
    | expression '-' term { $$ = create_operator_node('-', $1, $3); }
    ;

term
    : factor { $$ = $1; }
    | term '*' factor { $$ = create_operator_node('*', $1, $3); }
    | term '/' factor { $$ = create_operator_node('/', $1, $3); }
    ;

factor
    : NUMBER { $$ = create_number_node($1); }
    | '(' expression ')' { $$ = $2; }
    | FUNCTION '(' expression ')' { $$ = create_function_node($1, $3); }
    ;

%%

int main() {
    printf("Enter an expression: ");
    if (yyparse() == 0) {
        printf("Parsed successfully\n");
    } else {
        printf("Failed to parse\n");
    }
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
