import ply.yacc as yacc
import lexer
import sys

tokens = lexer.tokens
start = 'program'

def newvar():
    if not hasattr(newvar, 'counter'):
        newvar.counter = 0
    newvar.counter += 1
    s = "%x" + str(newvar.counter)
    #print s
    return s

class Type          :pass
class INT       (Type):pass
class FLOAT     (Type):pass
class VOID      (Type):pass
class ARRAY     (Type):pass

basetype = Type()

vars = {}

# -------------- RULES ----------------

########################### primary_expression ###########################
def p_primary_expression_1(p):
    '''primary_expression : IDENTIFIER'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = p[1]['type']
    if (p[1]['type'] == INT):
        p[0]['code'] = p[0]['reg'] + " = load i32* " + p[1]['reg']


def p_primary_expression_2(p):
    '''primary_expression : CONSTANTI'''

def p_primary_expression_3(p):
    '''primary_expression : CONSTANTF'''

def p_primary_expression_4(p):
    '''primary_expression : '(' expression ')' '''

def p_primary_expression_5(p):
    '''primary_expression : MAP '(' postfix_expression ',' postfix_expression ')' '''

def p_primary_expression_6(p):
    '''primary_expression : REDUCE '(' postfix_expression ',' postfix_expression ')' '''

def p_primary_expression_7(p):
    '''primary_expression : IDENTIFIER '(' ')' '''
    print(p[1])

def p_primary_expression_8(p):
    '''primary_expression : IDENTIFIER '(' argument_expression_list ')' '''
    print(p[1])

def p_primary_expression_9(p):
    '''primary_expression : IDENTIFIER INC_OP'''
    print(p[1])

def p_primary_expression_10(p):
    '''primary_expression : IDENTIFIER DEC_OP'''
    print(p[1])

########################### postfix_expression ###########################
def p_postfix_expression_1(p):
    '''postfix_expression : primary_expression'''

def p_postfix_expression_2(p):
    '''postfix_expression : postfix_expression '[' expression ']' '''

########################### argument_expression_list ###########################
def p_argument_expression_list_1(p):
    '''argument_expression_list : expression'''

def p_argument_expression_list_2(p):
    '''argument_expression_list : argument_expression_list ',' expression'''

########################### unary_expression ###########################
def p_unary_expression_1(p):
    '''unary_expression : postfix_expression'''

def p_unary_expression_2(p):
    '''unary_expression : INC_OP unary_expression'''

def p_unary_expression_3(p):
    '''unary_expression : DEC_OP unary_expression'''

def p_unary_expression_4(p):
    '''unary_expression : unary_operator unary_expression'''

########################### unary_operator ###########################
def p_unary_operator_1(p):
    '''unary_operator : '-' '''

########################### multiplicative_expression ###########################
def p_multiplicative_expression_1(p):
    '''multiplicative_expression : unary_expression'''

def p_multiplicative_expression_2(p):
    '''multiplicative_expression : multiplicative_expression '*' unary_expression'''

def p_multiplicative_expression_3(p):
    '''multiplicative_expression : multiplicative_expression '/' unary_expression'''

########################### additive_expression ###########################
def p_additive_expression_1(p):
    '''additive_expression : multiplicative_expression'''

def p_additive_expression_2(p):
    '''additive_expression : additive_expression '+' multiplicative_expression'''

def p_additive_expression_3(p):
    '''additive_expression : additive_expression '-' multiplicative_expression'''

########################### comparison_expression ###########################
def p_comparison_expression_1(p):
    '''comparison_expression : additive_expression'''
    print p[1]['code']

def p_comparison_expression_2(p):
    '''comparison_expression : additive_expression '<' additive_expression'''

def p_comparison_expression_3(p):
    '''comparison_expression : additive_expression '>' additive_expression'''

def p_comparison_expression_4(p):
    '''comparison_expression : additive_expression LE_OP additive_expression'''

def p_comparison_expression_5(p):
    '''comparison_expression : additive_expression GE_OP additive_expression'''

def p_comparison_expression_6(p):
    '''comparison_expression : additive_expression EQ_OP additive_expression'''

def p_comparison_expression_7(p):
    '''comparison_expression : additive_expression NE_OP additive_expression'''

########################### expression ###########################
def p_expression_1(p):
    '''expression : unary_expression assignment_operator comparison_expression'''

def p_expression_2(p):
    '''expression : comparison_expression'''

########################### assignment_operator ###########################
def p_assignment_operator_1(p):
    '''assignment_operator : '=' '''

def p_assignment_operator_2(p):
    '''assignment_operator : MUL_ASSIGN'''

def p_assignment_operator_3(p):
    '''assignment_operator : ADD_ASSIGN'''

def p_assignment_operator_4(p):
    '''assignment_operator : SUB_ASSIGN'''

########################### declaration ###########################
def p_declaration_1(p):
    '''declaration : type_name declarator_list ';' '''

def p_declaration_2(p):
    '''declaration : EXTERN type_name declarator_list ';' '''

########################### declarator_list ###########################
def p_declarator_list_1(p):
    '''declarator_list : declarator'''

def p_declarator_list_2(p):
    '''declarator_list : declarator_list ',' declarator'''

########################### type_name ###########################
def p_type_name_1(p):
    '''type_name : VOID'''
    global basetype
    basetype = VOID

def p_type_name_2(p):
    '''type_name : INT'''
    global basetype
    basetype = INT

def p_type_name_3(p):
    '''type_name : FLOAT'''
    global basetype
    basetype = FLOAT

########################### declarator ###########################
def p_declarator_1(p):
    '''declarator : IDENTIFIER'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['name'] = p[1]
    p[0]['type'] = basetype
    
    if (basetype == INT):
        p[0]['code'] = p[0]['reg']+" = alloca i32"
    elif (basetype == FLOAT):
        p[0]['code'] = p[0]['reg']+" = alloca float"

def p_declarator_2(p):
    '''declarator : '(' declarator ')' '''
    p[0] = p[2]

def p_declarator_3(p):
    '''declarator : declarator '[' CONSTANTI ']' '''

def p_declarator_4(p):
    '''declarator : declarator '[' ']' '''

def p_declarator_5(p):
    '''declarator : declarator '(' parameter_list ')' '''

def p_declarator_6(p):
    '''declarator : declarator '(' ')' '''

########################### parameter_list ###########################
def p_parameter_list_1(p):
    '''parameter_list : parameter_declaration'''

def p_parameter_list_2(p):
    '''parameter_list : parameter_list ',' parameter_declaration'''

########################### parameter_declaration ###########################
def p_parameter_declaration_1(p):
    '''parameter_declaration : type_name declarator'''

########################### statement ###########################
def p_statement_1(p):
    '''statement : compound_statement'''

def p_statement_2(p):
    '''statement : expression_statement'''

def p_statement_3(p):
    '''statement : selection_statement'''

def p_statement_4(p):
    '''statement : iteration_statement'''

def p_statement_5(p):
    '''statement : jump_statement'''

########################### compound_statement ###########################
def p_compound_statement_1(p):
    '''compound_statement : '{' '}' '''

def p_compound_statement_2(p):
    '''compound_statement : '{' statement_list '}' '''

def p_compound_statement_3(p):
    '''compound_statement : '{' declaration_list statement_list '}' '''

########################### declaration_list ###########################
def p_declaration_list_1(p):
    '''declaration_list : declaration'''

def p_declaration_list_2(p):
    '''declaration_list : declaration_list declaration'''

########################### statement_list ###########################
def p_statement_list_1(p):
    '''statement_list : statement'''

def p_statement_list_2(p):
    '''statement_list : statement_list statement'''

########################### expression_statement ###########################
def p_expression_statement_1(p):
    '''expression_statement : ';' '''

def p_expression_statement_2(p):
    '''expression_statement : expression ';' '''

########################### selection_statement ###########################
def p_selection_statement_1(p):
    '''selection_statement : IF '(' expression ')' statement'''

def p_selection_statement_2(p):
    '''selection_statement : IF '(' expression ')' statement ELSE statement'''

def p_selection_statement_3(p):
    '''selection_statement : FOR '(' expression_statement expression_statement expression ')' statement'''

########################### iteration_statement ###########################
def p_iteration_statement_1(p):
    '''iteration_statement : WHILE '(' expression ')' statement'''

def p_iteration_statement_2(p):
    '''iteration_statement : DO statement WHILE '(' expression ')' ';' '''

########################### jump_statement ###########################
def p_jump_statement_1(p):
    '''jump_statement : RETURN ';' '''

def p_jump_statement_2(p):
    '''jump_statement : RETURN expression ';' '''

########################### program ###########################
def p_program_1(p):
    '''program : external_declaration'''

def p_program_2(p):
    '''program : program external_declaration'''

########################### external_declaration ###########################
def p_external_declaration_1(p):
    '''external_declaration : function_definition'''

def p_external_declaration_2(p):
    '''external_declaration : declaration'''

########################### function_definition ###########################
def p_function_definition_1(p):
    '''function_definition : type_name declarator compound_statement'''

def p_error(p):
    print("Syntax error in input! {0}".format(p))

if __name__ == '__main__':
    parser = yacc.yacc()
    if len(sys.argv) > 1 :
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            parser.parse(f.read())
    else :
        print("Usage: ./{0} <file.c>".format(sys.argv[0]))
