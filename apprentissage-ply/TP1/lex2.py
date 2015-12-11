import ply.lex as lex

reserved_words = (
	'while',
	'print'
)

tokens = (
	'NUMBER',
	'ADD_OP',
	'MUL_OP',
	'ID',
) + tuple(map(lambda s:s.upper(), reserved_words))

t_ADD_OP = r'\+ | -'
t_MUL_OP = r'\* | /'

literals = ['(', ')', '=', '{', '}', ';']

def t_NUMBER(t):
	r'\d+\.?\d*'
	t.value = float(t.value)
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = file(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok:
			break
		print "line %d: %s(%s)" % (tok.lineno, tok.type, tok.value)