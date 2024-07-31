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

![Exemple d'arbre syntaxique (AST)]({assets}/images/parsing.drawio)

La grammaire formelle du langage C est très complexe et comporte de nombreuses règles. Elle est définie par le standard du langage C, qui est un document officiel publié par l'ANSI (American National Standards Institute) et l'ISO (International Organization for Standardization).

Une grammaire formelle est souvent écrite en utilisant une notation appelée "Backus-Naur Form" (BNF). Cette notation est très précise et permet de décrire de manière formelle la syntaxe d'un langage de programmation. Pour le C voici un extrait de la grammaire utilisée par le compilateur :

```text
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
```

Ce que l'on observe par exemple c'est que la grammaire du C est récursive. Cela signifie que l'on peut définir un élément en fonction de lui-même. Par exemple, un `declarator` peut contenir un `pointer` qui peut lui-même contenir un `pointer`.

Comment est-ce que cela fonctionne derrière les coulisses ?

Le compilateur va tout d'abord convertir votre code source en un arbre de syntaxe abstraite (AST) qui va représenter la structure de votre programme (c'est grosso modo la figure montrée plus haut). Ensuite, il va vérifier que cet arbre respecte les règles du standard C. Si ce n'est pas le cas, il va vous renvoyer une erreur de compilation. Si cela passe à cette étape, il va ensuite pouvoir assembler votre programme en convertissant cette représentation interne en du code assembleur. Ce dernier peut ensuite être optimisé pour être plus rapide ou plus petit.

La grammaire est donc un élément important de la programmation et elle explique pourquoi un simple `;` manquant peut vous coûter quelques cheveux arrachés car l'analyseur syntaxique ne sait pas comment découper votre code en phrases.

Pour les curieux, vous pouvez consulter la grammaire complète du C dans le standard du langage C (ISO/IEC 9899:2018) dans l'annexe A.

## Définir mon propre langage

Imaginons que l'on souaite réaliser notre propre langage formel, par exemple pour analyser une expression mathématique de la forme

```c
3 + 4 * 5 + ( sin(3.14) + sqrt(2) / 8 )
```

On pourrait définir une grammaire formelle pour ce langage de la manière suivante :

```text
<expression> ::= <term> { "+" <term> | "-" <term> }*

<term> ::= <factor> { "*" <factor> | "/" <factor> }*

<factor> ::= <number> | "(" <expression> ")" | <function> "(" <expression> ")"

<number> ::= [0-9]+("."[0-9]*)?
<function> ::= "sin" | "cos" | "sqrt"
```

Des outils comme `lex` et `yacc` permettent de générer un analyseur lexical et un analyseur syntaxique utilisables en C à partir de cette grammaire. Ces outils sont très puissants et sont utilisés dans de nombreuses bibliothèques et logiciels pour analyser des fichiers de configuration ou des syntaxes spécifiques.