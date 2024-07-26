[](){ #grammar }

# La grammaire

Dans un langage formel, la grammaire est l'ensemble des règles qui régissent la construction des phrases. Elle est essentielle pour comprendre et produire un texte correctement. En français, la grammaire est complexe et comporte de nombreuses règles et exceptions.

En programmation informatique, la grammaire est également très importante. Elle définit la syntaxe du langage de programmation, c'est-à-dire la manière dont les instructions doivent être écrites pour être comprises par l'ordinateur. Une erreur de syntaxe peut empêcher un programme de fonctionner correctement, voire de compiler.

L'ordinateur ne lit pas une phrase comme vous, elle ne peut pas ignorer les fautes de frappe, les erreurs de syntaxe ou les erreurs d'accord, car le compilateur doit être capable d'interpréter le code source sans aucune ambiguïté.

La grammaire d'un langage de programmation est généralement définie par un document appelé "grammaire formelle". Elle va définir les composants des éléments de votre code. Prenons par exemple le programme suivant :

```c
int main() {
    const int n = 23 + 42;
    for (int j = 0; j < n; ++j) {
        printf("%d ", j);
    }
    return 0;
}
```

On peut hiérarchiser les éléments de ce programme de la manière suivante :

![Abstract Syntax Tree]({assets}/images/parsing.drawio)

La grammaire formelle du langage C est très complexe et comporte de nombreuses règles. Elle est définie par le standard du langage C, qui est un document officiel publié par l'ANSI (American National Standards Institute) et l'ISO (International Organization for Standardization).

??? example "Grammaire BNF du langage C"

    ```bnf
    <translation_unit> ::= {<external_declaration>}*

    <external_declaration> ::= <function_definition>
                            | <declaration>

    <function_definition> ::= {<declaration_specifier>}* <declarator> {<declaration>}* <compound_statement>

    <declaration_specifier> ::= <storage_class_specifier>
                              | <type_specifier>
                              | <type_qualifier>

    <storage_class_specifier> ::= "auto"
                                | "register"
                                | "static"
                                | "extern"
                                | "typedef"

    <type_specifier> ::= "void"
                      | "char"
                      | "short"
                      | "int"
                      | "long"
                      | "float"
                      | "double"
                      | "signed"
                      | "unsigned"
                      | <struct_or_union_specifier>
                      | <enum_specifier>
                      | <typedef_name>

    <struct_or_union_specifier> ::= <struct_or_union> <identifier> { {<struct_declaration>}+ }
                                  | <struct_or_union> { {<struct_declaration>}+ }
                                  | <struct_or_union> <identifier>

    <struct_or_union> ::= "struct"
                        | "union"

    <struct_declaration> ::= {<specifier_qualifier>}* <struct_declarator_list>

    <specifier_qualifier> ::= <type_specifier>
                            | <type_qualifier>

    <struct_declarator_list> ::= <struct_declarator>
                              | <struct_declarator_list> "," <struct_declarator>

    <struct_declarator> ::= <declarator>
                          | <declarator> ":" <constant_expression>
                          | ":" <constant_expression>

    <declarator> ::= {<pointer>}? <direct_declarator>

    <pointer> ::= * {<type_qualifier>}* {<pointer>}?

    <type_qualifier> ::= "const"
                      | "volatile"

    <direct_declarator> ::= <identifier>
                          | ( <declarator> )
                          | <direct_declarator> "[" {<constant_expression>}? "]"
                          | <direct_declarator> "(" <parameter_type_list> ")"
                          | <direct_declarator> "(" {<identifier>}* ")"

    <constant_expression> ::= <conditional_expression>

    <conditional_expression> ::= <logical_or_expression>
                              | <logical_or_expression> "?" <expression> ":" <conditional_expression>

    <logical_or_expression> ::= <logical_and_expression>
                              | <logical_or_expression> "||" <logical_and_expression>

    <logical_and_expression> ::= <inclusive_or_expression>
                              | <logical_and_expression> "&&" <inclusive_or_expression>

    <inclusive_or_expression> ::= <exclusive_or_expression>
                                | <inclusive_or_expression> "|" <exclusive_or_expression>

    <exclusive_or_expression> ::= <and_expression>
                                | <exclusive_or_expression> "^" <and_expression>

    <and_expression> ::= <equality_expression>
                      | <and_expression> "&" <equality_expression>

    <equality_expression> ::= <relational_expression>
                            | <equality_expression> "==" <relational_expression>
                            | <equality_expression> "!=" <relational_expression>

    <relational_expression> ::= <shift_expression>
                              | <relational_expression> "<" <shift_expression>
                              | <relational_expression> ">" <shift_expression>
                              | <relational_expression> "<=" <shift_expression>
                              | <relational_expression> ">=" <shift_expression>

    <shift_expression> ::= <additive_expression>
                        | <shift_expression> "<<" <additive_expression>
                        | <shift_expression> ">>" <additive_expression>

    <additive_expression> ::= <multiplicative_expression>
                            | <additive_expression> "+" <multiplicative_expression>
                            | <additive_expression> "-" <multiplicative_expression>

    <multiplicative_expression> ::= <cast_expression>
                                  | <multiplicative_expression> "*" <cast_expression>
                                  | <multiplicative_expression> "/" <cast_expression>
                                  | <multiplicative_expression> "%" <cast_expression>

    <cast_expression> ::= <unary_expression>
                        | ( <type_name> ) <cast_expression>

    <unary_expression> ::= <postfix_expression>
                        | "++" <unary_expression>
                        | "--" <unary_expression>
                        | <unary_operator> <cast_expression>
                        | "sizeof" <unary_expression>
                        | "sizeof" <type_name>

    <postfix_expression> ::= <primary_expression>
                          | <postfix_expression> "[" <expression> "]"
                          | <postfix_expression> "(" {<assignment_expression>}* ")"
                          | <postfix_expression> "." <identifier>
                          | <postfix_expression> "->" <identifier>
                          | <postfix_expression> "++"
                          | <postfix_expression> "--"

    <primary_expression> ::= <identifier>
                          | <constant>
                          | <string>
                          | ( <expression> )

    <constant> ::= <integer_constant>
                | <character_constant>
                | <floating_constant>
                | <enumeration_constant>

    <expression> ::= <assignment_expression>
                  | <expression> "," <assignment_expression>

    <assignment_expression> ::= <conditional_expression>
                              | <unary_expression> <assignment_operator> <assignment_expression>

    <assignment_operator> ::= "="
                            | "*="
                            | "/="
                            | "%="
                            | "+="
                            | "-="
                            | "<<="
                            | ">>="
                            | "&="
                            | "^="
                            | "|="

    <unary_operator> ::= "&"
                      | "*"
                      | "+"
                      | "-"
                      | "~"
                      | "!"

    <type_name> ::= {<specifier_qualifier>}+ {<abstract_declarator>}?

    <parameter_type_list> ::= <parameter_list>
                            | <parameter_list> , ...

    <parameter_list> ::= <parameter_declaration>
                      | <parameter_list> "," <parameter_declaration>

    <parameter_declaration> ::= {<declaration_specifier>}+ <declarator>
                              | {<declaration_specifier>}+ <abstract_declarator>
                              | {<declaration_specifier>}+

    <abstract_declarator> ::= <pointer>
                            | <pointer> <direct_abstract_declarator>
                            | <direct_abstract_declarator>

    <direct_abstract_declarator> ::=  ( <abstract_declarator> )
                                  | {<direct_abstract_declarator>}? [ {<constant_expression>}? ]
                                  | {<direct_abstract_declarator>}? ( {<parameter_type_list>}? )

    <enum_specifier> ::= "enum" <identifier> { <enumerator_list> }
                      | "enum" { <enumerator_list> }
                      | "enum" <identifier>

    <enumerator_list> ::= <enumerator>
                        | <enumerator_list> "," <enumerator>

    <enumerator> ::= <identifier>
                  | <identifier> "=" <constant_expression>

    <typedef_name> ::= <identifier>

    <declaration> ::=  {<declaration_specifier>}+ {<init_declarator>}* ;

    <init_declarator> ::= <declarator>
                        | <declarator> "=" <initializer>

    <initializer> ::= <assignment_expression>
                    | { <initializer_list> }
                    | { <initializer_list> , }

    <initializer_list> ::= <initializer>
                        | <initializer_list> "," <initializer>

    <compound_statement> ::= { {<declaration>}* {<statement>}* }

    <statement> ::= <labeled_statement>
                  | <expression_statement>
                  | <compound_statement>
                  | <selection_statement>
                  | <iteration_statement>
                  | <jump_statement>

    <labeled_statement> ::= <identifier> : <statement>
                          | "case" <constant_expression> : <statement>
                          | "default" : <statement>

    <expression_statement> ::= {<expression>}? ;

    <selection_statement> ::= "if" ( <expression> ) <statement>
                            | "if" ( <expression> ) <statement> "else" <statement>
                            | "switch" ( <expression> ) <statement>

    <iteration_statement> ::= "while" ( <expression> ) <statement>
                            | "do" <statement> "while" ( <expression> ) ;
                            | "for" ( {<expression>}? ; {<expression>}? ; {<expression>}? ) <statement>

    <jump_statement> ::= "goto" <identifier> ;
                      | "continue" ;
                      | "break" ;
                      | "return" {<expression>}? ;
    ```

Un compilateur va tout d'abord convertir votre code source en un arbre de syntaxe abstraite (AST) qui va représenter la structure de votre programme. C'est grosso modo la figure montrée plus haut.

Ensuite, il va vérifier que cet arbre respecte les règles du standard C. Si ce n'est pas le cas, il va vous renvoyer une erreur de compilation.

Si cela passe à cette étape, il va ensuite pouvoir assembler votre programme en convertissant cette représentation interne en du code assembleur.

Ce dernier peut ensuite être optimisé pour être plus rapide ou plus petit.

La grammaire est donc un élément important de la programmation et elle explique pourquoi un simple `;` manquant peut vous coûter quelques cheveux arrachés.
