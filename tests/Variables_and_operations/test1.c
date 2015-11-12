// Compile sans erreur : déclaration int, affectation int, opérations int

int main()
{
	int x;
	int y;
	int z1, z2, z3, z4, z5;

	x = 1;
	y = 2;

	z1 = x + y;
	z2 = x - y;
	z3 = x / y;
	z4 = x * y;
	z5 = x % y;

	x = y + 7;
	x = y - 7;
	x = y * 7;
	x = y / 7;
	x = y % 7;
	return 0;
}