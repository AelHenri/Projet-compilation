//Erreur : invalid operands to binary operation && (expected int int, have float float) in main, line 18
//		   invalid operands to binary operation || (expected int int, have float float)	in main, line 19

int main()
{
	int a, b, c;
	float e, f, g;

	a = 0;
	b = 1;

	e = 0.0;
	f = 1.0;

	c = a && b;
	c = a || b;

	g = e && f;
	g = e || f;

}