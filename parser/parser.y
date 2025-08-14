%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);
%}

%union {
    char *str;
    double num;
}

%token STRING NUMBER TRUE FALSE NULLVALUE
%token LBRACE RBRACE LBRACKET RBRACKET COLON COMMA

%type <str> STRING
%type <num> NUMBER

%%

json:
    array
;

array:
    LBRACKET elements RBRACKET
;

elements:
    object
    | object COMMA elements
;

object:
    LBRACE key_value_pairs RBRACE
;

key_value_pairs:
    key_value
;

key_value:
    STRING COLON value COMMA
    STRING COLON value COMMA
    STRING COLON value COMMA
    STRING COLON value COMMA
    STRING COLON value COMMA
    STRING COLON value COMMA
    STRING COLON value
;

value:
    STRING
    | NUMBER
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erreur: %s\n", s);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <fichier.json>\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f) {
        perror("Erreur ouverture fichier");
        return 1;
    }

    extern FILE *yyin;
    yyin = f;

    return yyparse();
}
