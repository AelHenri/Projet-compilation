%{
    #include <stdio.h> 
    #include "parse.h"
    extern int yylineno;
    int yylex ();
    int yyerror ();

    char* newvar(){
        char *str = NULL;
        static int lastnum = 0;
        lastnum++;
        return str;
    }

%}

%token <string> IDENTIFIER 
%token <n> CONSTANTI 
%token <f> CONSTANTF 
%token MAP REDUCE EXTERN
%token INC_OP DEC_OP LE_OP GE_OP EQ_OP NE_OP
%token SUB_ASSIGN MUL_ASSIGN ADD_ASSIGN
%token TYPE_NAME
%token INT FLOAT VOID
%token IF ELSE WHILE RETURN FOR DO
%type <t> primary_expression postfix_expression unary_expression multiplicative_expression additive_expression declarator

%start program
%union {
  char *string;
  int n;
  float f;
  gen_t t;
}
%%

primary_expression
: IDENTIFIER 
| CONSTANTI  {
    $$.name = newvar(); 
    $$.type = INT_T;
    asprintf(&($$.code),"%s = add i32 0, %d\n", $$.name, $1);
}
| CONSTANTF  {
    $$.name = newvar();
    $$.type = FLOAT_T;
    asprintf(&($$.code),"%s = add i32 0, %d\n", $$.name, $1);
}
| '(' expression ')'
| MAP '(' postfix_expression ',' postfix_expression ')'
| REDUCE '(' postfix_expression ',' postfix_expression ')'
| IDENTIFIER '(' ')'    
| IDENTIFIER '(' argument_expression_list ')'   
| IDENTIFIER INC_OP 
| IDENTIFIER DEC_OP 
;

postfix_expression
: primary_expression
| postfix_expression '[' expression ']'
;

argument_expression_list
: expression
| argument_expression_list ',' expression
;

unary_expression
: postfix_expression
| INC_OP unary_expression
| DEC_OP unary_expression
| unary_operator unary_expression
;

unary_operator
: '-'
;

multiplicative_expression
: unary_expression
| multiplicative_expression '*' unary_expression {
    $$.name = newvar();
    asprintf($$.code, "%s\n%s\n%s = mul i32 %s, %s", $1.code, $3.code, $$.name, $1.name, $3.name);
}
| multiplicative_expression '/' unary_expression {
    $$.name = newvar();
    asprintf($$.code, "%s\n%s\n%s = sdiv i32 %s, %s", $1.code, $3.code, $$.name, $1.name, $3.name);
}
;

additive_expression
: multiplicative_expression
| additive_expression '+' multiplicative_expression {
    $$.name = newvar();
    asprintf($$.code, "%s\n%s\n%s = add i32 %s, %s", $1.code, $3.code, $$.name, $1.name, $3.name);
}
| additive_expression '-' multiplicative_expression {
    $$.name = newvar();
    asprintf($$.code, "%s\n%s\n%s = sub i32 %s, %s", $1.code, $3.code, $$.name, $1.name, $3.name);
}
;

comparison_expression
: additive_expression
| additive_expression '<' additive_expression
| additive_expression '>' additive_expression
| additive_expression LE_OP additive_expression
| additive_expression GE_OP additive_expression
| additive_expression EQ_OP additive_expression
| additive_expression NE_OP additive_expression
;

expression
: unary_expression assignment_operator comparison_expression
| comparison_expression
;

assignment_operator
: '='
| MUL_ASSIGN
| ADD_ASSIGN
| SUB_ASSIGN
;

declaration
: type_name declarator_list ';'
| EXTERN type_name declarator_list ';'
;

declarator_list
: declarator
| declarator_list ',' declarator
;

type_name
: VOID  
| INT   
| FLOAT
;

declarator
: IDENTIFIER 
| '(' declarator ')'
| declarator '[' CONSTANTI ']'
| declarator '[' ']'
| declarator '(' parameter_list ')'
| declarator '(' ')'
;

parameter_list
: parameter_declaration
| parameter_list ',' parameter_declaration
;

parameter_declaration
: type_name declarator
;

statement
: compound_statement
| expression_statement 
| selection_statement
| iteration_statement
| jump_statement
;

compound_statement
: '{' '}'
| '{' statement_list '}'
| '{' declaration_list statement_list '}'
;

declaration_list
: declaration
| declaration_list declaration
;

statement_list
: statement
| statement_list statement
;

expression_statement
: ';'
| expression ';'
;

selection_statement
: IF '(' expression ')' statement
| IF '(' expression ')' statement ELSE statement
| FOR '(' expression_statement expression_statement expression ')' statement
;

iteration_statement
: WHILE '(' expression ')' statement
| DO statement WHILE '(' expression ')'
;

jump_statement
: RETURN ';'
| RETURN expression ';'
;

program
: external_declaration
| program external_declaration
;

external_declaration
: function_definition
| declaration
;

function_definition
: type_name declarator compound_statement
;

%%
#include <stdio.h>
#include <string.h>

extern char yytext[];
extern int column;
extern int yylineno;
extern FILE *yyin;

char *file_name = NULL;

int yyerror (char *s) {
    fflush (stdout);
    fprintf (stderr, "%s:%d:%d: %s\n", file_name, yylineno, column, s);
    return 0;
}


int main (int argc, char *argv[]) {
    FILE *input = NULL;
    if (argc==2) {
	input = fopen (argv[1], "r");
	file_name = strdup (argv[1]);
	if (input) {
	    yyin = input;
	}
	else {
	  fprintf (stderr, "%s: Could not open %s\n", *argv, argv[1]);
	    return 1;
	}
    }
    else {
	fprintf (stderr, "%s: error: no input file\n", *argv);
	return 1;
    }
    yyparse ();
    free (file_name);
    return 0;
}
