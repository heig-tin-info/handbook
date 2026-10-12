%{
#include "c99.tab.h"
extern int yylineno;
void yyerror(const char *s);
%}

%%
"/*"                                    { comment(); }
"//".*                                  { /* consume //-comment */ }

"auto"                                  { printf("Token: AUTO\n"); return(AUTO); }
"break"                                 { printf("Token: BREAK\n"); return(BREAK); }
"case"                                  { printf("Token: CASE\n"); return(CASE); }
"char"                                  { printf("Token: CHAR\n"); return(CHAR); }
"const"                                 { printf("Token: CONST\n"); return(CONST); }
"continue"                              { printf("Token: CONTINUE\n"); return(CONTINUE); }
"default"                               { printf("Token: DEFAULT\n"); return(DEFAULT); }
"do"                                    { printf("Token: DO\n"); return(DO); }
"double"                                { printf("Token: DOUBLE\n"); return(DOUBLE); }
"else"                                  { printf("Token: ELSE\n"); return(ELSE); }
"enum"                                  { printf("Token: ENUM\n"); return(ENUM); }
"extern"                                { printf("Token: EXTERN\n"); return(EXTERN); }
"float"                                 { printf("Token: FLOAT\n"); return(FLOAT); }
"for"                                   { printf("Token: FOR\n"); return(FOR); }
"goto"                                  { printf("Token: GOTO\n"); return(GOTO); }
"if"                                    { printf("Token: IF\n"); return(IF); }
"inline"                                { printf("Token: INLINE\n"); return(INLINE); }
"int"                                   { printf("Token: INT\n"); return(INT); }
"long"                                  { printf("Token: LONG\n"); return(LONG); }
"register"                              { printf("Token: REGISTER\n"); return(REGISTER); }
"restrict"                              { printf("Token: RESTRICT\n"); return(RESTRICT); }
"return"                                { printf("Token: RETURN\n"); return(RETURN); }
"short"                                 { printf("Token: SHORT\n"); return(SHORT); }
"signed"                                { printf("Token: SIGNED\n"); return(SIGNED); }
"sizeof"                                { printf("Token: SIZEOF\n"); return(SIZEOF); }
"static"                                { printf("Token: STATIC\n"); return(STATIC); }
"struct"                                { printf("Token: STRUCT\n"); return(STRUCT); }
"switch"                                { printf("Token: SWITCH\n"); return(SWITCH); }
"typedef"                               { printf("Token: TYPEDEF\n"); return(TYPEDEF); }
"union"                                 { printf("Token: UNION\n"); return(UNION); }
"unsigned"                              { printf("Token: UNSIGNED\n"); return(UNSIGNED); }
"void"                                  { printf("Token: VOID\n"); return(VOID); }
"volatile"                              { printf("Token: VOLATILE\n"); return(VOLATILE); }
"while"                                 { printf("Token: WHILE\n"); return(WHILE); }
"_Alignas"                              { printf("Token: ALIGNAS\n"); return ALIGNAS; }
"_Alignof"                              { printf("Token: ALIGNOF\n"); return ALIGNOF; }
"_Atomic"                               { printf("Token: ATOMIC\n"); return ATOMIC; }
"_Bool"                                 { printf("Token: BOOL\n"); return BOOL; }
"_Complex"                              { printf("Token: COMPLEX\n"); return COMPLEX; }
"_Generic"                              { printf("Token: GENERIC\n"); return GENERIC; }
"_Imaginary"                            { printf("Token: IMAGINARY\n"); return IMAGINARY; }
"_Noreturn"                             { printf("Token: NORETURN\n"); return NORETURN; }
"_Static_assert"                        { printf("Token: STATIC_ASSERT\n"); return STATIC_ASSERT; }
"_Thread_local"                         { printf("Token: THREAD_LOCAL\n"); return THREAD_LOCAL; }
"__func__"                              { printf("Token: FUNC_NAME\n"); return FUNC_NAME; }

{L}{A}*                                 { printf("Token: IDENTIFIER (%s)\n", yytext); return check_type(); }

{HP}{H}+{IS}?                           { printf("Token: I_CONSTANT\n"); return I_CONSTANT; }
{NZ}{D}*{IS}?                           { printf("Token: I_CONSTANT\n"); return I_CONSTANT; }
"0"{O}*{IS}?                            { printf("Token: I_CONSTANT\n"); return I_CONSTANT; }
{CP}?"'"([^'\\\n]|{ES})+"'"             { printf("Token: I_CONSTANT\n"); return I_CONSTANT; }

{D}+{E}{FS}?                            { printf("Token: F_CONSTANT\n"); return F_CONSTANT; }
{D}*"."{D}+{E}?{FS}?                    { printf("Token: F_CONSTANT\n"); return F_CONSTANT; }
{D}+"."{E}?{FS}?                        { printf("Token: F_CONSTANT\n"); return F_CONSTANT; }
{HP}{H}+{P}{FS}?                        { printf("Token: F_CONSTANT\n"); return F_CONSTANT; }
{HP}{H}*"."{H}+{P}{FS}?                 { printf("Token: F_CONSTANT\n"); return F_CONSTANT; }
{HP}{H}+"."{P}{FS}?                     { printf("Token: F_CONSTANT\n"); return F_CONSTANT; }

({SP}?\"([^"\\\n]|{ES})*\"{WS}*)+       { printf("Token: STRING_LITERAL\n"); return STRING_LITERAL; }

"..."                                   { printf("Token: ELLIPSIS\n"); return ELLIPSIS; }
">>="                                   { printf("Token: RIGHT_ASSIGN\n"); return RIGHT_ASSIGN; }
"<<="                                   { printf("Token: LEFT_ASSIGN\n"); return LEFT_ASSIGN; }
"+="                                    { printf("Token: ADD_ASSIGN\n"); return ADD_ASSIGN; }
"-="                                    { printf("Token: SUB_ASSIGN\n"); return SUB_ASSIGN; }
"*="                                    { printf("Token: MUL_ASSIGN\n"); return MUL_ASSIGN; }
"/="                                    { printf("Token: DIV_ASSIGN\n"); return DIV_ASSIGN; }
"%="                                    { printf("Token: MOD_ASSIGN\n"); return MOD_ASSIGN; }
"&="                                    { printf("Token: AND_ASSIGN\n"); return AND_ASSIGN; }
"^="                                    { printf("Token: XOR_ASSIGN\n"); return XOR_ASSIGN; }
"|="                                    { printf("Token: OR_ASSIGN\n"); return OR_ASSIGN; }
">>"                                    { printf("Token: RIGHT_OP\n"); return RIGHT_OP; }
"<<"                                    { printf("Token: LEFT_OP\n"); return LEFT_OP; }
"++"                                    { printf("Token: INC_OP\n"); return INC_OP; }
"--"                                    { printf("Token: DEC_OP\n"); return DEC_OP; }
"->"                                    { printf("Token: PTR_OP\n"); return PTR_OP; }
"&&"                                    { printf("Token: AND_OP\n"); return AND_OP; }
"||"                                    { printf("Token: OR_OP\n"); return OR_OP; }
"<="                                    { printf("Token: LE_OP\n"); return LE_OP; }
">="                                    { printf("Token: GE_OP\n"); return GE_OP; }
"=="                                    { printf("Token: EQ_OP\n"); return EQ_OP; }
"!="                                    { printf("Token: NE_OP\n"); return NE_OP; }
";"                                     { printf("Token: ';'\n"); return ';'; }
("{"|"<%")                              { printf("Token: '{'\n"); return '{'; }
("}"|"%>")                              { printf("Token: '}'\n"); return '}'; }
","                                     { printf("Token: ','\n"); return ','; }
":"                                     { printf("Token: ':'\n"); return ':'; }
"="                                     { printf("Token: '='\n"); return '='; }
"("                                     { printf("Token: '('\n"); return '('; }
")"                                     { printf("Token: ')'\n"); return ')'; }
("["|"<:")                              { printf("Token: '['\n"); return '['; }
("]"|":>")                              { printf("Token: ']'\n"); return ']'; }
"."                                     { printf("Token: '.'\n"); return '.'; }
"&"                                     { printf("Token: '&'\n"); return '&'; }
"!"                                     { printf("Token: '!'\n"); return '!'; }
"~"                                     { printf("Token: '~'\n"); return '~'; }
"-"                                     { printf("Token: '-'\n"); return '-'; }
"+"                                     { printf("Token: '+'\n"); return '+'; }
"*"                                     { printf("Token: '*'\n"); return '*'; }
"/"                                     { printf("Token: '/'\n"); return '/'; }
"%"                                     { printf("Token: '%'\n"); return '%'; }
"<"                                     { printf("Token: '<'\n"); return '<'; }
">"                                     { printf("Token: '>'\n"); return '>'; }
"^"                                     { printf("Token: '^'\n"); return '^'; }
"|"                                     { printf("Token: '|'\n"); return '|'; }
"?"                                     { printf("Token: '?'\n"); return '?'; }

{WS}+                                   { /* ignore whitespace */ }
.                                       { /* discard bad characters */ }

%%

int yywrap(void)        /* called at end of input */
{
    return 1;           /* terminate now */
}

static void comment(void)
{
    int c;

    while ((c = input()) != 0)
        if (c == '*')
        {
            while ((c = input()) == '*')
                ;

            if (c == '/')
                return;

            if (c == 0)
                break;
        }
    yyerror("unterminated comment");
}

static int check_type(void)
{
    switch (sym_type(yytext))
    {
    case TYPEDEF_NAME:                /* previously defined */
        return TYPEDEF_NAME;
    case ENUMERATION_CONSTANT:        /* previously defined */
        return ENUMERATION_CONSTANT;
    default:                          /* includes undefined */
        return IDENTIFIER;
    }
}
