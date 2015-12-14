import ply.yacc as yacc
import lexer
import sys

tokens = lexer.tokens
start = 'program'


def newvar():
    # Fonction servant à générer un nouveau registre de la forme %xi, i étant incrémenté à chaque fois
    if not hasattr(newvar, 'counter'):
        newvar.counter = 0
    s = "%x" + str(newvar.counter)
    newvar.counter += 1
    return s

def newlabel():
    # Même chose que pour les registres, mais pour les labels
    if not hasattr(newlabel, 'counter'):
        newlabel.counter = 0
    s = "label" + str(newlabel.counter)
    newlabel.counter += 1
    return s

# Equivalent du enum pour les types
class Type          :pass
class INT       (Type):pass
class FLOAT     (Type):pass
class VOID      (Type):pass
class ARRAY     (Type):pass

# Initialisation de la variable globale pour connaitre le type de l'identifiant suivant
basetype = Type()

# Dictionnaire (équivalent de la hashtable)
# Marche par clé, exemple : vars = {'x' : %x3} : le dictionnaire une entrée, dont la clé est 'x' (nom de la variable en C) et la valeur est %x3 (le nom du registre où est stocké la variable)
# Pour y accéder, on tape vars['x']
vars = {}


def sitofp(reg):
    # Fonction pour écrire le code pour convertir un int en float (marche à peu près, pas beaucoup testé)
    newReg = newvar()
    code = newReg + " = sitofp i32 " + reg +" to float\n"
    return [code, newReg]


# On utilsie aussi des dictionnaires pour chaque règle. p[0] = {} initialise p[0] en un dictionnaire, et le minimum est d'y mettre un code :
# p[0]['code'] = "machin truc"
# Pour les variables, on a les clés 'code', 'reg' qui enregistre le registre où est stocké la variable, et 'type'.
# Dans la première règle en dessous il y a l'entrée 'name', je sais plus exactement pourquoi mais c'est pour enregistrer le nom du registre d'origine (je crois, je reviendrai dessus plus tard).
# -------------- RULES ----------------

########################### primary_expression ###########################
def p_primary_expression_1(p):
    '''primary_expression : IDENTIFIER'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p_id = vars[p[1]]
    p[0]['name'] = p_id['reg']
    if (p_id['type'] == INT):
        p[0]['type'] = INT
        p[0]['code'] = p[0]['reg'] + " = load i32* " + p_id['reg'] + "\n"
    else:
        p[0]['type'] = FLOAT
        p[0]['code'] = p[0]['reg'] + " = load float* " + p_id['reg'] + "\n"

def p_primary_expression_2(p):
    '''primary_expression : CONSTANTI'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = INT
    p[0]['code'] = p[0]['reg'] + " = add i32 0, " + p[1] + "\n"
    p[0]['val'] = p[1]

def p_primary_expression_3(p):
    '''primary_expression : CONSTANTF'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = FLOAT
    p[0]['code'] = p[0]['reg'] + " = fadd float 0.0, " + p[1] + "\n"
    p[0]['val'] = p[1]

def p_primary_expression_4(p):
    '''primary_expression : '(' expression ')' '''
    p[0] = p[2]

def p_primary_expression_5(p):
    '''primary_expression : MAP '(' postfix_expression ',' postfix_expression ')' '''
    p[0] = {'type': INT}

def p_primary_expression_6(p):
    '''primary_expression : REDUCE '(' postfix_expression ',' postfix_expression ')' '''
    p[0] = {'type': INT}

def p_primary_expression_7(p):
    '''primary_expression : IDENTIFIER '(' ')' '''
    p[0] = {'type': INT}

def p_primary_expression_8(p):
    '''primary_expression : IDENTIFIER '(' argument_expression_list ')' '''
    p[0] = {'type': INT}

def p_primary_expression_9(p):
    '''primary_expression : IDENTIFIER INC_OP'''
    p[0] = {'type': INT}

def p_primary_expression_10(p):
    '''primary_expression : IDENTIFIER DEC_OP'''
    p[0] = {'type': INT}

########################### postfix_expression ###########################
def p_postfix_expression_1(p):
    '''postfix_expression : primary_expression'''
    p[0] = p[1]

def p_postfix_expression_2(p):
    '''postfix_expression : postfix_expression '[' expression ']' '''
    p[0] = p[1]

########################### argument_expression_list ###########################
def p_argument_expression_list_1(p):
    '''argument_expression_list : expression'''
    p[0] = p[1]

def p_argument_expression_list_2(p):
    '''argument_expression_list : argument_expression_list ',' expression'''

########################### unary_expression ###########################
def p_unary_expression_1(p):
    '''unary_expression : postfix_expression'''
    p[0] = p[1]

def p_unary_expression_2(p):
    '''unary_expression : INC_OP unary_expression'''
    p[0] = p[2]

def p_unary_expression_3(p):
    '''unary_expression : DEC_OP unary_expression'''
    p[0] = p[2]

def p_unary_expression_4(p):
    '''unary_expression : unary_operator unary_expression'''
    p[0] = {}
    p[0]['var'] = newvar()
    if (p[2]['type'] == INT):
        p[0]['type'] = INT
        p[0]['code'] = p[2]['code'] + " " + p[0]['reg'] + " = sub i32 0, " + p[2]['reg'] + "\n"
    elif (p[2]['type'] == FLOAT):
        p[0]['type'] = FLOAT
        p[0]['code'] = p[2]['code'] + " " + p[0]['reg'] + " = fsub float 0.0, " + p[2]['reg'] + "\n"    

########################### unary_operator ###########################
def p_unary_operator_1(p):
    '''unary_operator : '-' '''

########################### multiplicative_expression ###########################
def p_multiplicative_expression_1(p):
    '''multiplicative_expression : unary_expression'''
    p[0] = p[1]


def p_multiplicative_expression_2(p):
    '''multiplicative_expression : multiplicative_expression '*' unary_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['type'] = INT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = mul i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['type'] = FLOAT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fmul float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == INT and p[3]['type'] == FLOAT):
        p[0]['type'] = FLOAT
        p1 = sitofp(p[1]['reg'])
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p1[0] + p[0]['reg'] + " = fmul float " + p1[1] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

def p_multiplicative_expression_3(p):
    '''multiplicative_expression : multiplicative_expression '/' unary_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['type'] = INT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = sdiv i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['type'] = FLOAT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fdiv float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

def p_multiplicative_expression_4(p):
    '''multiplicative_expression : multiplicative_expression '%' unary_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['type'] = INT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = srem i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['type'] = FLOAT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = frem float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

########################### additive_expression ###########################
def p_additive_expression_1(p):
    '''additive_expression : multiplicative_expression'''
    p[0] = p[1]

def p_additive_expression_2(p):
    '''additive_expression : additive_expression '+' multiplicative_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['type'] = INT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = add i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['type'] = FLOAT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fadd float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

def p_additive_expression_3(p):
    '''additive_expression : additive_expression '-' multiplicative_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['type'] = INT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = sub i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['type'] = FLOAT
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fsub float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

########################### comparison_expression ###########################
def p_comparison_expression_1(p):
    '''comparison_expression : additive_expression'''
    p[0] = p[1]

def p_comparison_expression_2(p):
    '''comparison_expression : additive_expression '<' additive_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = INT
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = icmp slt i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fcmp olt float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

def p_comparison_expression_3(p):
    '''comparison_expression : additive_expression '>' additive_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = INT
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = icmp sgt i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fcmp ogt float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

def p_comparison_expression_4(p):
    '''comparison_expression : additive_expression LE_OP additive_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = INT
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = icmp use i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fcmp ole float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

def p_comparison_expression_5(p):
    '''comparison_expression : additive_expression GE_OP additive_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = INT
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = icmp sge i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fcmp oge float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

def p_comparison_expression_6(p):
    '''comparison_expression : additive_expression EQ_OP additive_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = INT
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = icmp eq i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fcmp oeq float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

def p_comparison_expression_7(p):
    '''comparison_expression : additive_expression NE_OP additive_expression'''
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = INT
    if (p[1]['type'] == INT and p[3]['type'] == INT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = icmp ne i32 " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    elif (p[1]['type'] == FLOAT and p[3]['type'] == FLOAT):
        p[0]['code'] = p[1]['code'] + p[3]['code'] + p[0]['reg'] + " = fcmp one float " + p[1]['reg'] + ", " + p[3]['reg'] + "\n"
    else:
        p_error("Not yet valid operation between float and int =P")

########################### expression ###########################
def p_expression_1(p):
    '''expression : unary_expression assignment_operator comparison_expression'''
    p[0] = {}
    if p[3]['type'] == INT:
        p[0]['type'] = INT
        p[0]['code'] = p[3]['code'] + "store i32 " + p[3]['reg'] + ", i32* " + p[1]['name'] + "\n"
    elif p[3]['type'] == FLOAT:
        p[0]['type'] = FLOAT
        if (p[1]['type'] == INT):
            newReg = newvar()
            p1 = sitofp(p[1]['reg'])
            p[0]['code'] = p[3]['code'] + p1[0] + "store float " + p[3]['reg'] + ", float* " + p1[1] + "\n" + newReg + "= load float* " + p1[1] + "\n"
        else:
            p[0]['code'] = p[3]['code'] + "store float " + p[3]['reg'] + ", float* " + p[1]['name'] + "\n" + p[1]['code']

def p_expression_2(p):
    '''expression : comparison_expression'''
    p[0] = p[1]

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
    p[0] = p[2]

def p_declaration_2(p):
    '''declaration : EXTERN type_name declarator_list ';' '''

########################### declarator_list ###########################
def p_declarator_list_1(p):
    '''declarator_list : declarator'''
    p[0] = p[1]

def p_declarator_list_2(p):
    '''declarator_list : declarator_list ',' declarator'''
    p[0] = {}
    p[0]['code'] = p[1]['code'] + p[3]['code']

########################### type_name ###########################
def p_type_name_1(p):
    '''type_name : VOID'''
    global basetype
    basetype = VOID
    p[0] = {}
    p[0]['type'] = VOID

def p_type_name_2(p):
    '''type_name : INT'''
    global basetype
    basetype = INT
    p[0] = {}
    p[0]['type'] = INT

def p_type_name_3(p):
    '''type_name : FLOAT'''
    global basetype
    basetype = FLOAT
    p[0] = {}
    p[0]['type'] = FLOAT

########################### declarator ###########################
def p_declarator_1(p):
    '''declarator : IDENTIFIER'''
    global basetype
    p[0] = {}
    p[0]['reg'] = newvar()
    p[0]['type'] = basetype
    p[0]['name'] = p[1]
    if (basetype == INT):
        p[0]['code'] = p[0]['reg']+" = alloca i32\n"
    else:
        p[0]['code'] = p[0]['reg']+" = alloca float\n"

    vars[p[1]] = p[0]

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
    p[0] = p[1]

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
    p[0] = p[1]

def p_statement_2(p):
    '''statement : expression_statement'''
    p[0] = p[1]

def p_statement_3(p):
    '''statement : selection_statement'''
    p[0] = p[1]

def p_statement_4(p):
    '''statement : iteration_statement'''
    p[0] = p[1]

def p_statement_5(p):
    '''statement : jump_statement'''
    p[0] = p[1]

########################### compound_statement ###########################
def p_compound_statement_1(p):
    '''compound_statement : '{' '}' '''
    p[0] = {}
    #p[0]['code'] = "{\n\n}"

def p_compound_statement_2(p):
    '''compound_statement : '{' statement_list '}' '''
    p[0] = p[2]
    #p[0]['code'] = "{\n" + p[2]['code'] + "\n}"

def p_compound_statement_3(p):
    '''compound_statement : '{' declaration_list statement_list '}' '''
    p[0] = {}
    p[0]['code'] = p[2]['code'] + p[3]['code']
    #p[0]['code'] = "{\n" + p[2]['code'] + p[3]['code'] + "\n}"


########################### declaration_list ###########################
def p_declaration_list_1(p):
    '''declaration_list : declaration'''
    p[0] = p[1]

def p_declaration_list_2(p):
    '''declaration_list : declaration_list declaration'''
    p[0] = {}
    p[0]['code'] = p[1]['code'] + p[2]['code']

########################### statement_list ###########################
def p_statement_list_1(p):
    '''statement_list : statement'''
    p[0] = p[1]

def p_statement_list_2(p):
    '''statement_list : statement_list statement'''
    p[0] = {}
    p[0]['code'] = p[1]['code'] + p[2]['code']

########################### expression_statement ###########################
def p_expression_statement_1(p):
    '''expression_statement : ';' '''
    p[0] = {}
    p[0]['code'] = "\n"

def p_expression_statement_2(p):
    '''expression_statement : expression ';' '''
    p[0] = p[1]

########################### selection_statement ###########################
def p_selection_statement_1(p):
    '''selection_statement : IF '(' expression ')' statement'''
    p[0] = {}
    trueLabel = newlabel()
    endLabel = newlabel()
    p[0]['code'] = p[3]['code'] + "br i1 " + p[3]['reg'] + ", label %" + trueLabel + ", label %" + endLabel + "\n" + trueLabel + ":\n" + p[5]['code'] + "br label %" + endLabel + "\n" + endLabel + ":\n"

def p_selection_statement_2(p):
    '''selection_statement : IF '(' expression ')' statement ELSE statement'''
    p[0] = {}
    trueLabel = newlabel()
    falseLabel = newlabel()
    endLabel = newlabel()
    p[0]['code'] = p[3]['code'] + "br i1 " + p[3]['reg'] + ", label %" + trueLabel + ", label %" + falseLabel + "\n" + trueLabel + ":\n" + p[5]['code'] + "br label %" + endLabel + "\n" + falseLabel + ":\n" + p[7]['code'] + "br label %" + endLabel + "\n" + endLabel + ":\n"

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
    p[0] = {}
    p[0]['code'] = "ret i1 0"

def p_jump_statement_2(p):
    '''jump_statement : RETURN expression ';' '''
    p[0] = {}
    if (p[2]['type'] == INT):
        p[0]['code'] = p[2]['code'] + "ret i32 " + p[2]['reg']


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
    p[0] = {}
    if p[1]['type'] == INT:
        p[0]['type'] = p[1]['type']
        p[0]['code'] = "define i32 @" + p[2]['name'] + "() {\n" + p[3]['code'] + "\n}"
    print p[0]['code']

def p_error(p):
    print "Error line " + str(p.lineno) + ":" + str(p)

if __name__ == '__main__':
    parser = yacc.yacc()
    if len(sys.argv) > 1 :
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            parser.parse(f.read())
    else :
        print("Usage: ./{0} <file.c>".format(sys.argv[0]))
