import ply.yacc as yacc
from lex2 import tokens
import AST

operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
}

precedence = (
	('left', 'ADD_OP'),
	('left', 'MUL_OP'),
)

vars = {}

def p_program(p):
	'''program : statement
			| statement ';' program '''
	if len(p) == 2:
		p[0] = AST.ProgramNode(p[1])
	else:
		p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_statement_1(p):
	''' statement : assignment'''
	p[0] = p[1]

def p_statement_2(p):
	''' statement : structure'''
	p[0] = p[1]

def p_statement_3(p):
	''' statement : PRINT expression '''
	p[0] = AST.PrintNode(p[2])

def p_structure(p):
	''' structure : WHILE expression '{' program '}' '''
	p[0] = AST.WhileNode([p[2], p[4]])

def p_assignment(p):
	''' assignment : ID '=' expression '''
	p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])

def p_expression_num(p):
	'''expression : NUMBER'''
	p[0] = AST.TokenNode(p[1])

def p_expression_id(p):
	''' expression : ID '''
	p[0] = AST.TokenNode(p[1])

def p_expression_par(p):
	'''expression : '(' expression ')' '''
	p[0] = p[2]

def p_expression_op(p):
	'''expression : expression ADD_OP expression
			| expression MUL_OP expression'''
	p[0] = AST.OpNode(p[2], [p[1], p[3]])



def p_error(p):
	print "Syntax error in line %d" % p.lineno
	yacc.errok()

def parse(program):
	return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
	import sys
	import os

	prog = file(sys.argv[1]).read()
	result = yacc.parse(prog)

	graph = result.makegraphicaltree()
	name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
	graph.write_pdf(name)

	print "wrote ast to", name

	print result