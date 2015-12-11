import AST
from AST import addToClass

operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
}

vars = {}

@addToClass(AST.ProgramNode)
def execute(self):
	for c in self.children:
		c.execute()

@addToClass(AST.TokenNode)
def execute(self):
	if isinstance(self.tok, str):
		

if __name__ == "__main__":
	from parser1 import parse
	import sys

	prog = file(sys.argv[1]).read()
	ast = parse(prog)

	ast.execute()
