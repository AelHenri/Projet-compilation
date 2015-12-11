import ply.lex as lex
import sys

# List of token names.   This is always required
reserved = {
    'do' : 'DO',
    'else' : 'ELSE',
    'float' : 'FLOAT',
    'for' : 'FOR',
    'if' : 'IF',
    'int' : 'INT',
    'return' : 'RETURN',
    'void' : 'VOID',
    'while' : 'WHILE',
    }

tokens =  ['IDENTIFIER', 'CONSTANTI', 'CONSTANTF', 'MAP', 'REDUCE', 'EXTERN',
            # Operators
            'INC_OP', 'DEC_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP',
            'SUB_ASSIGN', 'MUL_ASSIGN', 'ADD_ASSIGN',
            ] + list(reserved.values())

literals = [';', '{', '}', ',', '/', '=', '(', ')', '[', ']', '.', '!', '-',
            '+', '*', '<', '>']

def t_IDENTIFIER(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

t_MAP           = r'map'
t_REDUCE        = r'reduce'
t_EXTERN        = r'extern'

# Operators
t_INC_OP        = r'\+\+'
t_DEC_OP        = r'--'
t_LE_OP         = r'<='
t_GE_OP         = r'>='
t_EQ_OP         = r'=='
t_NE_OP         = r'!='
t_SUB_ASSIGN    = r'-='
t_MUL_ASSIGN    = r'\*='
t_ADD_ASSIGN    = r'\+='

t_CONSTANTI     = r'\d+'
t_CONSTANTF     = r'((\d+)(\.\d+))'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\v\f'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    if len(sys.argv) > 1 :
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            lexer.input(f.read())
            while True:
                tok = lexer.token()
                if not tok:
                    break      # No more input
                print(tok)
    else :
        print("Usage: ./{0} <file.c>".format(sys.argv[0]))
