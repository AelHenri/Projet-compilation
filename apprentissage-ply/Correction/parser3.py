import ply.yacc as yacc
from lex4 import tokens

vars = {}

def p_programme(p):
    '''programme : statement COMA programme 
    | statement '''
    if (len(p) == 2):
        p[0] = p[1]
    else :
        p[0] = p[3]

def p_statement(p):
    ''' statement : affectation 
    | expression'''
    p[0] = p[1]
    
def p_expression_num(p):
    'expression : NUMBER'
    p[0] = p[1]

    
def p_affectation(p):
    '''affectation :  IDENTIFICATEUR EGAL expression '''
    p[0] = p[3]
    vars[p[1]]=p[3]

def p_variable(p):
    """ expression : IDENTIFICATEUR"""
    p[0] = vars[p[1]]
    
operations = {
    '+' : lambda x,y : x+y,
    '-' : lambda x,y : x-y,
    '*' : lambda x,y : x*y,
    '/' : lambda x,y : x/y,
}

operation_minus = {
    '+' : lambda x : x,
    '-' : lambda x : -x,
}

def p_expression_op(p):
    '''expression : expression ADD_OP expression 
    | expression MUL_OP expression'''
    p[0] = operations[p[2]](p[1],p[3])


def p_expression_parenthese(p):
    '''expression : L_PARENTHESE expression R_PARENTHESE'''
    p[0] = p[2]


def p_expression_uminus(p):
    'expression : ADD_OP expression %prec UNARY_MINUS '
    p[0] = operation_minus[p[1]](p[2])

def p_error(p):
    print "Syntax error in line %d" % p.lineno
    yacc.errok()

precedence = (
    ('left', 'EGAL'),
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right','UNARY_MINUS'),
)

yacc.yacc(outputdir = 'generated')

if __name__ == "__main__":
    import sys
    prog = file(sys.argv[1]).read()
    result = yacc.parse(prog)
    print result
