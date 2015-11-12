// Compile sans erreur : comparaison int, float, int avec float

int main()
{
	int a, b, c, d, e, f;

	int m1;
	float m2;

	m1 = 3;
	m2 = 3.1;

	a = 2 < 3; // 1
	b = 2 > 3; // 0
	c = 2 <= 3; // 1
	d = 2 >= 3; // 0
	e = 2 == 3; // 0
	f = 2 != 3; // 1

	a = 2.1 < 3.1; // 1
	b = 2.1 > 3.1; // 0
	c = 2.1 <= 3.1; // 1
	d = 2.1 >= 3.1; // 0
	e = 2.1 == 3.1; // 0
	f = 2.1 != 3.1; // 1

	a = m1 < m2; // 1
	b = m1 > m2; // 0
	c = m1 <= m2; // 1
	d = m1 >= m2; // 0
	e = m1 == m2; // 0
	f = m1 != m2; // 1

	return 0;
}