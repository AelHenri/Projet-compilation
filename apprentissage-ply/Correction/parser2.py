import ply.yacc as yacc
from lex3 import tokens

def p_expression_num(p):
    'expression : NUMBER'
    p[0] = p[1]


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
