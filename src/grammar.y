%{
    #include <stdio.h>
    #include "hachage.h"
    extern int yylineno;
    int yylex ();
    int yyerror ();

    char *newvar() {
        static int i=0;
        char *s;
        asprintf(&s,"%%x%d",i++);
        return s;
    }
    gen_t EMPTY= {"", INT_T, "" };
    enum base basetype;
%}

%token <string> IDENTIFIER
%token <f> CONSTANTF 
%token <n> CONSTANTI 
%token MAP REDUCE EXTERN DO
%token INC_OP DEC_OP LE_OP GE_OP EQ_OP NE_OP
%token SUB_ASSIGN MUL_ASSIGN ADD_ASSIGN
%token TYPE_NAME
%token INT FLOAT VOID
%token IF ELSE WHILE RETURN FOR
%type <g> primary_expression postfix_expression unary_expression multiplicative_expression additive_expression
%type <g> declarator
%start program
%union {
  char *string;
  int n;
  float f;
  gen_t g;
}
%%

primary_expression
: IDENTIFIER {
    gen_t g = findtab($1);
    char *n = newvar();
    if (g.type == INT_T){
        $$.type = INT_T;
        asprintf(&($$.code), "%s = load i32* %s\n",n,g.var);
    }
    else {
        $$.type = FLOAT_T;
        asprintf(&($$.code), "%s = load float* %s\n",n,g.var);
    }

} 
| CONSTANTI { 
    $$.var=newvar(); 
    $$.type=INT_T;
    asprintf(&($$.code), "%s = add i32 0, %d\n", $$.var,$1);
}
| CONSTANTF { 
    $$.var=newvar(); 
    $$.type=FLOAT_T;
    asprintf(&($$.code), "%s = fadd float 0, %f\n", $$.var,$1);
}
| '(' expression ')' { $$ = EMPTY; } 
| MAP '(' postfix_expression ',' postfix_expression ')' { $$ = EMPTY; } 
| REDUCE '(' postfix_expression ',' postfix_expression ')' { $$ = EMPTY; } 
| IDENTIFIER '(' ')' { $$ = EMPTY; } 
| IDENTIFIER '(' argument_expression_list ')' { $$ = EMPTY; } 
| IDENTIFIER INC_OP  { $$ = EMPTY; } 
     | IDENTIFIER DEC_OP { $$ = EMPTY; }  
;

postfix_expression
  : primary_expression { $$ = $1; }
   | postfix_expression '[' expression ']' { $$ = $1; }
;

argument_expression_list
: expression
| argument_expression_list ',' expression
;

unary_expression
  : postfix_expression { $$ = $1; }
   | INC_OP unary_expression { $$ = $2; }
   | DEC_OP unary_expression { $$ = $2; }
   | unary_operator unary_expression {   $$.var = newvar(); 
  if ($2.type==INT_T) {
  $$.type=INT_T;
    asprintf(&($$.code), "%s %s = sub i32 0, %s\n", $2.code, $$.var,$2.var);
 } else {
  $$.type=FLOAT_T;
    asprintf(&($$.code), "%s %s = fsub float 0, %s\n", $2.code, $$.var,$2.var);
 } }
;

unary_operator
: '-'
;

multiplicative_expression
: unary_expression { $$ = $1; } 
| multiplicative_expression '*' unary_expression { 
  $$.var = newvar(); 
  if ($1.type==INT_T && $3.type==INT_T) {
  $$.type=INT_T;
    asprintf(&($$.code), "%s%s%s = mul i32 %s, %s\n", $1.code, $3.code,$$.var,$1.var,$3.var);
 } else {
  $$.type=FLOAT_T;
    asprintf(&($$.code), "%s%s%s = fmul float %s, %s\n", $1.code, $3.code,$$.var,$1.var,$3.var);
 } }
| multiplicative_expression '/' unary_expression { 
  $$.var = newvar(); 
  if ($1.type==INT_T && $3.type==INT_T) {
  $$.type=INT_T;
    asprintf(&($$.code), "%s%s%s = sdiv i32 %s, %s\n", $1.code, $3.code,$$.var,$1.var,$3.var);
 } else {
  $$.type=FLOAT_T;
    asprintf(&($$.code), "%s%s%s = fdiv float %s, %s\n", $1.code, $3.code,$$.var,$1.var,$3.var);
 } }
;

additive_expression
  : multiplicative_expression { $$ = $1; } 
     | additive_expression '+' multiplicative_expression { 
  $$.var = newvar(); 
  if ($1.type==INT_T && $3.type==INT_T) {
  $$.type=INT_T;
    asprintf(&($$.code), "%s%s%s = add i32 %s, %s\n", $1.code, $3.code,$$.var,$1.var,$3.var);
 } else {
  $$.type=FLOAT_T;
    asprintf(&($$.code), "%s%s%s = fadd float %s, %s\n", $1.code, $3.code,$$.var,$1.var,$3.var);
 } 
 }
| additive_expression '-' multiplicative_expression { 
  $$.var = newvar(); 
  if ($1.type==INT_T && $3.type==INT_T) {
    asprintf(&($$.code), "%s%s%s = sub i32 %s, %s\n", $1.code, $3.code,$$.var,$1.var,$3.var);
 } else {
    asprintf(&($$.code), "%s%s%s = fsub float %s, %s\n", $1.code, $3.code,$$.var,$1.var,$3.var);
 } }
;

comparison_expression
  : additive_expression { printf("%s\n",$1.code); }
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
  : VOID { basetype = VOID_T; }
   | INT { basetype = INT_T; }
   | FLOAT { basetype = FLOAT_T; }
;

declarator
  : IDENTIFIER {
    $$.code = newvar();
    addtab($1, basetype, $$.var);
    if (basetype == INT_T) {
        asprintf(&($$.code), "%s = alloca i32", $$.var);
    }
    else {
        asprintf(&($$.code), "%s = alloca float", $$.var);
    }
  }           
   | '(' declarator ')' { $$ = $2; }   
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
    init();
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