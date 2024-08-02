%{
#include "calc.h"
#include "calc.tab.h"
%}

%%

[0-9]+(\.[0-9]+)? {
    yylval.number = atof(yytext);
    return NUMBER;
}

"sin" {
    yylval.function = "sin";
    return FUNCTION;
}

"cos" {
    yylval.function = "cos";
    return FUNCTION;
}

"sqrt" {
    yylval.function = "sqrt";
    return FUNCTION;
}

"(" { return '('; }
")" { return ')'; }
"+" { return '+'; }
"-" { return '-'; }
"*" { return '*'; }
"/" { return '/'; }
[ \t\n] ;
. { yyerror("Unknown character"); }

%%

int yywrap() {
    return 1;
}
