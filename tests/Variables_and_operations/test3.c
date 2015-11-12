// Compile sans erreur : affectation de float dans int et int dans float, opérations int et float

int main()
{
	int x, a, b;
	float y, c, d;
	
	y = 3.2;
	x = y; // x = 3
	y = x; // y = 3.0

	a = 3;
	c = 6.7;

	b = a + c; // b = 9
	d = a + c; // d = 9.7

	b = a - c; // b = -3
	d = a - c; // d = -3.7

	b = a / c; // b = 0
	d = a / c; // d = 0.44776119403

	b = a * c; // b = 20
	d = a * c; // d = 20.1

	return 0;
}