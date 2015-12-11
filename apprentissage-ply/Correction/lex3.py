import ply.lex as lex

tokens = (
    'L_PARENTHESE',
    'R_PARENTHESE',
    'NUMBER',
    'ADD_OP',
    'MUL_OP',
    )

t_L_PARENTHESE = r'\('
t_R_PARENTHESE = r'\)'
t_ADD_OP = r'\+|-'
t_MUL_OP = r'\*|/'


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    print t.value
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print "Illegal character '%s'" % t.value[0]

lex.lex()


if __name__ == "__main__":
    print "coucou \n"
    import sys
    prog = file(sys.argv[1]).read()
    lex.input(prog)
    while 1:
        tok = lex.token()
        if not tok: break
        print "line %d: %s(%s)" % ( tok.lineno,tok.type, tok.value)
        
