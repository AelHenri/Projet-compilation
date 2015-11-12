//Compile sans erreur : do..while

int main()
{
	int a;
	float b;

	a = 1;
	b = 2.2;

	do
		a = a +1;
	while (a<b);

	do
		a = a+1;
	while (a != b);

	do {
		a = a+1;
	}
	while (a);

	do {	
		b = b-1;
		a = a +1;
	}
	while (b);

	do
		a = a-1;
	while (a && b);

	do
		a = a-1;
	while (a || b);

	do; while(1);

	return 0;
}