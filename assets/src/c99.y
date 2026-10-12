%{
#include "ast.h"
#include <stdio.h>
void yyerror(const char *s);
int yylex(void);
extern int yylineno;
ASTNode *root;
%}

%token IDENTIFIER I_CONSTANT F_CONSTANT STRING_LITERAL FUNC_NAME SIZEOF
%token PTR_OP INC_OP DEC_OP LEFT_OP RIGHT_OP LE_OP GE_OP EQ_OP NE_OP
%token AND_OP OR_OP MUL_ASSIGN DIV_ASSIGN MOD_ASSIGN ADD_ASSIGN
%token SUB_ASSIGN LEFT_ASSIGN RIGHT_ASSIGN AND_ASSIGN
%token XOR_ASSIGN OR_ASSIGN
%token TYPEDEF_NAME ENUMERATION_CONSTANT

%token TYPEDEF EXTERN STATIC AUTO REGISTER INLINE
%token CONST RESTRICT VOLATILE
%token BOOL CHAR SHORT INT LONG SIGNED UNSIGNED FLOAT DOUBLE VOID
%token COMPLEX IMAGINARY
%token STRUCT UNION ENUM ELLIPSIS

%token CASE DEFAULT IF ELSE SWITCH WHILE DO FOR GOTO CONTINUE BREAK RETURN

%token ALIGNAS ALIGNOF ATOMIC GENERIC NORETURN STATIC_ASSERT THREAD_LOCAL

%start translation_unit
%%

primary_expression
    : IDENTIFIER {
        $$ = create_identifier_node($1);
    }
    | constant {
        $$ = $1;
    }
    | string {
        $$ = $1;
    }
    | '(' expression ')' {
        $$ = $2;
    }
    | generic_selection {
        $$ = $1;
    }
    ;

constant
    : I_CONSTANT {
        $$ = create_constant_node($1);
    }
    | F_CONSTANT {
        $$ = create_constant_node($1);
    }
    | ENUMERATION_CONSTANT {
        $$ = create_identifier_node($1);
    }
    ;

string
    : STRING_LITERAL {
        $$ = create_string_node($1);
    }
    | FUNC_NAME {
        $$ = create_string_node($1);
    }
    ;

generic_selection
    : GENERIC '(' assignment_expression ',' generic_assoc_list ')' {
        // Créez le nœud correspondant
    }
    ;

generic_assoc_list
    : generic_association
    | generic_assoc_list ',' generic_association
    ;

generic_association
    : type_name ':' assignment_expression
    | DEFAULT ':' assignment_expression
    ;

postfix_expression
    : primary_expression {
        $$ = $1;
    }
    | postfix_expression '[' expression ']' {
        // Créez le nœud correspondant
    }
    | postfix_expression '(' ')' {
        // Créez le nœud correspondant
    }
    | postfix_expression '(' argument_expression_list ')' {
        // Créez le nœud correspondant
    }
    | postfix_expression '.' IDENTIFIER {
        // Créez le nœud correspondant
    }
    | postfix_expression PTR_OP IDENTIFIER {
        // Créez le nœud correspondant
    }
    | postfix_expression INC_OP {
        $$ = create_unary_op_node(INC_OP, $1);
    }
    | postfix_expression DEC_OP {
        $$ = create_unary_op_node(DEC_OP, $1);
    }
    | '(' type_name ')' '{' initializer_list '}' {
        // Créez le nœud correspondant
    }
    | '(' type_name ')' '{' initializer_list ',' '}' {
        // Créez le nœud correspondant
    }
    ;

argument_expression_list
    : assignment_expression {
        // Créez le nœud correspondant
    }
    | argument_expression_list ',' assignment_expression {
        // Créez le nœud correspondant
    }
    ;

unary_expression
    : postfix_expression {
        $$ = $1;
    }
    | INC_OP unary_expression {
        $$ = create_unary_op_node(INC_OP, $2);
    }
    | DEC_OP unary_expression {
        $$ = create_unary_op_node(DEC_OP, $2);
    }
    | unary_operator cast_expression {
        $$ = create_unary_op_node($1, $2);
    }
    | SIZEOF unary_expression {
        // Créez le nœud correspondant
    }
    | SIZEOF '(' type_name ')' {
        // Créez le nœud correspondant
    }
    | ALIGNOF '(' type_name ')' {
        // Créez le nœud correspondant
    }
    ;

unary_operator
    : '&' {
        $$ = '&';
    }
    | '*' {
        $$ = '*';
    }
    | '+' {
        $$ = '+';
    }
    | '-' {
        $$ = '-';
    }
    | '~' {
        $$ = '~';
    }
    | '!' {
        $$ = '!';
    }
    ;

cast_expression
    : unary_expression {
        $$ = $1;
    }
    | '(' type_name ')' cast_expression {
        // Créez le nœud correspondant
    }
    ;

multiplicative_expression
    : cast_expression {
        $$ = $1;
    }
    | multiplicative_expression '*' cast_expression {
        $$ = create_binary_op_node('*', $1, $3);
    }
    | multiplicative_expression '/' cast_expression {
        $$ = create_binary_op_node('/', $1, $3);
    }
    | multiplicative_expression '%' cast_expression {
        $$ = create_binary_op_node('%', $1, $3);
    }
    ;

additive_expression
    : multiplicative_expression {
        $$ = $1;
    }
    | additive_expression '+' multiplicative_expression {
        $$ = create_binary_op_node('+', $1, $3);
    }
    | additive_expression '-' multiplicative_expression {
        $$ = create_binary_op_node('-', $1, $3);
    }
    ;

shift_expression
    : additive_expression {
        $$ = $1;
    }
    | shift_expression LEFT_OP additive_expression {
        // Créez le nœud correspondant
    }
    | shift_expression RIGHT_OP additive_expression {
        // Créez le nœud correspondant
    }
    ;

relational_expression
    : shift_expression {
        $$ = $1;
    }
    | relational_expression '<' shift_expression {
        // Créez le nœud correspondant
    }
    | relational_expression '>' shift_expression {
        // Créez le nœud correspondant
    }
    | relational_expression LE_OP shift_expression {
        // Créez le nœud correspondant
    }
    | relational_expression GE_OP shift_expression {
        // Créez le nœud correspondant
    }
    ;

equality_expression
    : relational_expression {
        $$ = $1;
    }
    | equality_expression EQ_OP relational_expression {
        // Créez le nœud correspondant
    }
    | equality_expression NE_OP relational_expression {
        // Créez le nœud correspondant
    }
    ;

and_expression
    : equality_expression {
        $$ = $1;
    }
    | and_expression '&' equality_expression {
        // Créez le nœud correspondant
    }
    ;

exclusive_or_expression
    : and_expression {
        $$ = $1;
    }
    | exclusive_or_expression '^' and_expression {
        // Créez le nœud correspondant
    }
    ;

inclusive_or_expression
    : exclusive_or_expression {
        $$ = $1;
    }
    | inclusive_or_expression '|' exclusive_or_expression {
        // Créez le nœud correspondant
    }
    ;

logical_and_expression
    : inclusive_or_expression {
        $$ = $1;
    }
    | logical_and_expression AND_OP inclusive_or_expression {
        // Créez le nœud correspondant
    }
    ;

logical_or_expression
    : logical_and_expression {
        $$ = $1;
    }
    | logical_or_expression OR_OP logical_and_expression {
        // Créez le nœud correspondant
    }
    ;

conditional_expression
    : logical_or_expression {
        $$ = $1;
    }
    | logical_or_expression '?' expression ':' conditional_expression {
        // Créez le nœud correspondant
    }
    ;

assignment_expression
    : conditional_expression {
        $$ = $1;
    }
    | unary_expression assignment_operator assignment_expression {
        // Créez le nœud correspondant
    }
    ;

assignment_operator
    : '=' {
        $$ = '=';
    }
    | MUL_ASSIGN {
        $$ = MUL_ASSIGN;
    }
    | DIV_ASSIGN {
        $$ = DIV_ASSIGN;
    }
    | MOD_ASSIGN {
        $$ = MOD_ASSIGN;
    }
    | ADD_ASSIGN {
        $$ = ADD_ASSIGN;
    }
    | SUB_ASSIGN {
        $$ = SUB_ASSIGN;
    }
    | LEFT_ASSIGN {
        $$ = LEFT_ASSIGN;
    }
    | RIGHT_ASSIGN {
        $$ = RIGHT_ASSIGN;
    }
    | AND_ASSIGN {
        $$ = AND_ASSIGN;
    }
    | XOR_ASSIGN {
        $$ = XOR_ASSIGN;
    }
    | OR_ASSIGN {
        $$ = OR_ASSIGN;
    }
    ;

expression
    : assignment_expression {
        $$ = $1;
    }
    | expression ',' assignment_expression {
        // Créez le nœud correspondant
    }
    ;

constant_expression
    : conditional_expression {
        $$ = $1;
    }
    ;

declaration
    : declaration_specifiers ';' {
        // Créez le nœud correspondant
    }
    | declaration_specifiers init_declarator_list ';' {
        // Créez le nœud correspondant
    }
    | static_assert_declaration {
        // Créez le nœud correspondant
    }
    ;

declaration_specifiers
    : storage_class_specifier declaration_specifiers {
        // Créez le nœud correspondant
    }
    | storage_class_specifier {
        // Créez le nœud correspondant
    }
    | type_specifier declaration_specifiers {
        // Créez le nœud correspondant
    }
    | type_specifier {
        // Créez le nœud correspondant
    }
    | type_qualifier declaration_specifiers {
        // Créez le nœud correspondant
    }
    | type_qualifier {
        // Créez le nœud correspondant
    }
    | function_specifier declaration_specifiers {
        // Créez le nœud correspondant
    }
    | function_specifier {
        // Créez le nœud correspondant
    }
    | alignment_specifier declaration_specifiers {
        // Créez le nœud correspondant
    }
    | alignment_specifier {
        // Créez le nœud correspondant
    }
    ;

init_declarator_list
    : init_declarator {
        // Créez le nœud correspondant
    }
    | init_declarator_list ',' init_declarator {
        // Créez le nœud correspondant
    }
    ;

init_declarator
    : declarator '=' initializer {
        // Créez le nœud correspondant
    }
    | declarator {
        // Créez le nœud correspondant
    }
    ;

storage_class_specifier
    : TYPEDEF {
        // Créez le nœud correspondant
    }
    | EXTERN {
        // Créez le nœud correspondant
    }
    | STATIC {
        // Créez le nœud correspondant
    }
    | THREAD_LOCAL {
        // Créez le nœud correspondant
    }
    | AUTO {
        // Créez le nœud correspondant
    }
    | REGISTER {
        // Créez le nœud correspondant
    }
    ;

type_specifier
    : VOID {
        // Créez le nœud correspondant
    }
    | CHAR {
        // Créez le nœud correspondant
    }
    | SHORT {
        // Créez le nœud correspondant
    }
    | INT {
        // Créez le nœud correspondant
    }
    | LONG {
        // Créez le nœud correspondant
    }
    | FLOAT {
        // Créez le nœud correspondant
    }
    | DOUBLE {
        // Créez le nœud correspondant
    }
    | SIGNED {
        // Créez le nœud correspondant
    }
    | UNSIGNED {
        // Créez le nœud correspondant
    }
    | BOOL {
        // Créez le nœud correspondant
    }
    | COMPLEX {
        // Créez le nœud correspondant
    }
    | IMAGINARY {
        // Créez le nœud correspondant
    }
    | atomic_type_specifier {
        // Créez le nœud correspondant
    }
    | struct_or_union_specifier {
        // Créez le nœud correspondant
    }
    | enum_specifier {
        // Créez le nœud correspondant
    }
    | TYPEDEF_NAME {
        // Créez le nœud correspondant
    }
    ;

struct_or_union_specifier
    : struct_or_union '{' struct_declaration_list '}' {
        // Créez le nœud correspondant
    }
    | struct_or_union IDENTIFIER '{' struct_declaration_list '}' {
        // Créez le nœud correspondant
    }
    | struct_or_union IDENTIFIER {
        // Créez le nœud correspondant
    }
    ;

struct_or_union
    : STRUCT {
        // Créez le nœud correspondant
    }
    | UNION {
        // Créez le nœud correspondant
    }
    ;

struct_declaration_list
    : struct_declaration {
        // Créez le nœud correspondant
    }
    | struct_declaration_list struct_declaration {
        // Créez le nœud correspondant
    }
    ;

struct_declaration
    : specifier_qualifier_list ';' {
        // Créez le nœud correspondant
    }
    | specifier_qualifier_list struct_declarator_list ';' {
        // Créez le nœud correspondant
    }
    | static_assert_declaration {
        // Créez le nœud correspondant
    }
    ;

specifier_qualifier_list
    : type_specifier specifier_qualifier_list {
        // Créez le nœud correspondant
    }
    | type_specifier {
        // Créez le nœud correspondant
    }
    | type_qualifier specifier_qualifier_list {
        // Créez le nœud correspondant
    }
    | type_qualifier {
        // Créez le nœud correspondant
    }
    ;

struct_declarator_list
    : struct_declarator {
        // Créez le nœud correspondant
    }
    | struct_declarator_list ',' struct_declarator {
        // Créez le nœud correspondant
    }
    ;

struct_declarator
    : ':' constant_expression {
        // Créez le nœud correspondant
    }
    | declarator ':' constant_expression {
        // Créez le nœud correspondant
    }
    | declarator {
        // Créez le nœud correspondant
    }
    ;

enum_specifier
    : ENUM '{' enumerator_list '}' {
        // Créez le nœud correspondant
    }
    | ENUM '{' enumerator_list ',' '}' {
        // Créez le nœud correspondant
    }
    | ENUM IDENTIFIER '{' enumerator_list '}' {
        // Créez le nœud correspondant
    }
    | ENUM IDENTIFIER '{' enumerator_list ',' '}' {
        // Créez le nœud correspondant
    }
    | ENUM IDENTIFIER {
        // Créez le nœud correspondant
    }
    ;

enumerator_list
    : enumerator {
        // Créez le nœud correspondant
    }
    | enumerator_list ',' enumerator {
        // Créez le nœud correspondant
    }
    ;

enumerator
    : enumeration_constant '=' constant_expression {
        // Créez le nœud correspondant
    }
    | enumeration_constant {
        // Créez le nœud correspondant
    }
    ;

atomic_type_specifier
    : ATOMIC '(' type_name ')' {
        // Créez le nœud correspondant
    }
    ;

type_qualifier
    : CONST {
        // Créez le nœud correspondant
    }
    | RESTRICT {
        // Créez le nœud correspondant
    }
    | VOLATILE {
        // Créez le nœud correspondant
    }
    | ATOMIC {
        // Créez le nœud correspondant
    }
    ;

function_specifier
    : INLINE {
        // Créez le nœud correspondant
    }
    | NORETURN {
        // Créez le nœud correspondant
    }
    ;

alignment_specifier
    : ALIGNAS '(' type_name ')' {
        // Créez le nœud correspondant
    }
    | ALIGNAS '(' constant_expression ')' {
        // Créez le nœud correspondant
    }
    ;

declarator
    : pointer direct_declarator {
        // Créez le nœud correspondant
    }
    | direct_declarator {
        // Créez le nœud correspondant
    }
    ;

direct_declarator
    : IDENTIFIER {
        $$ = create_identifier_node($1);
    }
    | '(' declarator ')' {
        $$ = $2;
    }
    | direct_declarator '[' ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '[' '*' ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '[' STATIC type_qualifier_list assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '[' STATIC assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '[' type_qualifier_list '*' ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '[' type_qualifier_list STATIC assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '[' type_qualifier_list assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '[' type_qualifier_list ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '[' assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_declarator '(' parameter_type_list ')' {
        // Créez le nœud correspondant
    }
    | direct_declarator '(' ')' {
        // Créez le nœud correspondant
    }
    | direct_declarator '(' identifier_list ')' {
        // Créez le nœud correspondant
    }
    ;

pointer
    : '*' type_qualifier_list pointer {
        // Créez le nœud correspondant
    }
    | '*' type_qualifier_list {
        // Créez le nœud correspondant
    }
    | '*' pointer {
        // Créez le nœud correspondant
    }
    | '*' {
        // Créez le nœud correspondant
    }
    ;

type_qualifier_list
    : type_qualifier {
        // Créez le nœud correspondant
    }
    | type_qualifier_list type_qualifier {
        // Créez le nœud correspondant
    }
    ;

parameter_type_list
    : parameter_list ',' ELLIPSIS {
        // Créez le nœud correspondant
    }
    | parameter_list {
        // Créez le nœud correspondant
    }
    ;

parameter_list
    : parameter_declaration {
        // Créez le nœud correspondant
    }
    | parameter_list ',' parameter_declaration {
        // Créez le nœud correspondant
    }
    ;

parameter_declaration
    : declaration_specifiers declarator {
        // Créez le nœud correspondant
    }
    | declaration_specifiers abstract_declarator {
        // Créez le nœud correspondant
    }
    | declaration_specifiers {
        // Créez le nœud correspondant
    }
    ;

identifier_list
    : IDENTIFIER {
        $$ = create_identifier_node($1);
    }
    | identifier_list ',' IDENTIFIER {
        // Créez le nœud correspondant
    }
    ;

type_name
    : specifier_qualifier_list abstract_declarator {
        // Créez le nœud correspondant
    }
    | specifier_qualifier_list {
        // Créez le nœud correspondant
    }
    ;

abstract_declarator
    : pointer direct_abstract_declarator {
        // Créez le nœud correspondant
    }
    | pointer {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator {
        // Créez le nœud correspondant
    }
    ;

direct_abstract_declarator
    : '(' abstract_declarator ')' {
        // Créez le nœud correspondant
    }
    | '[' ']' {
        // Créez le nœud correspondant
    }
    | '[' '*' ']' {
        // Créez le nœud correspondant
    }
    | '[' STATIC type_qualifier_list assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | '[' STATIC assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | '[' type_qualifier_list STATIC assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | '[' type_qualifier_list assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | '[' type_qualifier_list ']' {
        // Créez le nœud correspondant
    }
    | '[' assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '[' ']' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '[' '*' ']' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '[' STATIC type_qualifier_list assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '[' STATIC assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '[' type_qualifier_list assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '[' type_qualifier_list STATIC assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '[' type_qualifier_list ']' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '[' assignment_expression ']' {
        // Créez le nœud correspondant
    }
    | '(' ')' {
        // Créez le nœud correspondant
    }
    | '(' parameter_type_list ')' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '(' ')' {
        // Créez le nœud correspondant
    }
    | direct_abstract_declarator '(' parameter_type_list ')' {
        // Créez le nœud correspondant
    }
    ;

initializer
    : '{' initializer_list '}' {
        // Créez le nœud correspondant
    }
    | '{' initializer_list ',' '}' {
        // Créez le nœud correspondant
    }
    | assignment_expression {
        // Créez le nœud correspondant
    }
    ;

initializer_list
    : designation initializer {
        // Créez le nœud correspondant
    }
    | initializer {
        // Créez le nœud correspondant
    }
    | initializer_list ',' designation initializer {
        // Créez le nœud correspondant
    }
    | initializer_list ',' initializer {
        // Créez le nœud correspondant
    }
    ;

designation
    : designator_list '=' {
        // Créez le nœud correspondant
    }
    ;

designator_list
    : designator {
        // Créez le nœud correspondant
    }
    | designator_list designator {
        // Créez le nœud correspondant
    }
    ;

designator
    : '[' constant_expression ']' {
        // Créez le nœud correspondant
    }
    | '.' IDENTIFIER {
        // Créez le nœud correspondant
    }
    ;

static_assert_declaration
    : STATIC_ASSERT '(' constant_expression ',' STRING_LITERAL ')' ';' {
        // Créez le nœud correspondant
    }
    ;

statement
    : labeled_statement {
        // Créez le nœud correspondant
    }
    | compound_statement {
        // Créez le nœud correspondant
    }
    | expression_statement {
        // Créez le nœud correspondant
    }
    | selection_statement {
        // Créez le nœud correspondant
    }
    | iteration_statement {
        // Créez le nœud correspondant
    }
    | jump_statement {
        // Créez le nœud correspondant
    }
    ;

labeled_statement
    : IDENTIFIER ':' statement {
        // Créez le nœud correspondant
    }
    | CASE constant_expression ':' statement {
        // Créez le nœud correspondant
    }
    | DEFAULT ':' statement {
        // Créez le nœud correspondant
    }
    ;

compound_statement
    : '{' '}' {
        // Créez le nœud correspondant
    }
    | '{' block_item_list '}' {
        // Créez le nœud correspondant
    }
    ;

block_item_list
    : block_item {
        // Créez le nœud correspondant
    }
    | block_item_list block_item {
        // Créez le nœud correspondant
    }
    ;

block_item
    : declaration {
        // Créez le nœud correspondant
    }
    | statement {
        // Créez le nœud correspondant
    }
    ;

expression_statement
    : ';' {
        // Créez le nœud correspondant
    }
    | expression ';' {
        // Créez le nœud correspondant
    }
    ;

selection_statement
    : IF '(' expression ')' statement ELSE statement {
        // Créez le nœud correspondant
    }
    | IF '(' expression ')' statement {
        // Créez le nœud correspondant
    }
    | SWITCH '(' expression ')' statement {
        // Créez le nœud correspondant
    }
    ;

iteration_statement
    : WHILE '(' expression ')' statement {
        // Créez le nœud correspondant
    }
    | DO statement WHILE '(' expression ')' ';' {
        // Créez le nœud correspondant
    }
    | FOR '(' expression_statement expression_statement ')' statement {
        // Créez le nœud correspondant
    }
    | FOR '(' expression_statement expression_statement expression ')' statement {
        // Créez le nœud correspondant
    }
    | FOR '(' declaration expression_statement ')' statement {
        // Créez le nœud correspondant
    }
    | FOR '(' declaration expression_statement expression ')' statement {
        // Créez le nœud correspondant
    }
    ;

jump_statement
    : GOTO IDENTIFIER ';' {
        // Créez le nœud correspondant
    }
    | CONTINUE ';' {
        // Créez le nœud correspondant
    }
    | BREAK ';' {
        // Créez le nœud correspondant
    }
    | RETURN ';' {
        // Créez le nœud correspondant
    }
    | RETURN expression ';' {
        // Créez le nœud correspondant
    }
    ;

translation_unit
    : external_declaration {
        root = $1;
    }
    | translation_unit external_declaration {
        // Créez le nœud correspondant
    }
    ;

external_declaration
    : function_definition {
        // Créez le nœud correspondant
    }
    | declaration {
        // Créez le nœud correspondant
    }
    ;

function_definition
    : declaration_specifiers declarator declaration_list compound_statement {
        // Créez le nœud correspondant
    }
    | declaration_specifiers declarator compound_statement {
        // Créez le nœud correspondant
    }
    ;

declaration_list
    : declaration {
        // Créez le nœud correspondant
    }
    | declaration_list declaration {
        // Créez le nœud correspondant
    }
    ;

%%
#include <stdio.h>

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s at line %d\n", s, yylineno);
}

int yylex(void);

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            fprintf(stderr, "Could not open file %s\n", argv[1]);
            return 1;
        }
        yyin = file;
    }
    yyparse();
    if (root) {
        print_ast(root);
    }
    return 0;
}
