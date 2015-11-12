// Compile sans erreur : déclaration float, affectation float, opérations float

int main()
{
	float x;
	float y;
	float z1, z2, z3, z4;

	x = 1.3;
	y = 2.3;

	z1 = x + y;
	z2 = x - y;
	z3 = x / y;
	z4 = x * y;

	x = y + 7.1;
	x = y - 7.1;
	x = y * 7.1;
	x = y / 7.1;
	return 0;
}