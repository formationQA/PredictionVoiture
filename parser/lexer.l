%{
#include "parser.tab.h"
#include <string.h>
%}

%%

[ \t\r\n]+              ;
"true"                  { return TRUE; }
"false"                 { return FALSE; }
"null"                  { return NULLVALUE; }
\"([^\"\\]|\\.)*\"      { yylval.str = strdup(yytext); return STRING; }
-?[0-9]+(\.[0-9]+)?     { yylval.num = atof(yytext); return NUMBER; }
"{"                     { return LBRACE; }
"}"                     { return RBRACE; }
"["                     { return LBRACKET; }
"]"                     { return RBRACKET; }
":"                     { return COLON; }
","                     { return COMMA; }

.                       { return yytext[0]; }

%%

int yywrap(void) {
    return 1;
}
