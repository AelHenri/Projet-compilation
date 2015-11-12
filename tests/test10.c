//Compile sans erreur : while

int main()
{
	int a;
	float b;

	a = 1;
	b = 2.2;

	while (a<b);

	while (a<b)
		a = a +1;

	while (a != b)
		a = a+1;

	while (a){
		a = a+1;
	}

	while (b){
		b = b-1;
		a = a +1;
	}

	while (a && b)
		a = a-1;

	while (a || b)
		a = a-1;

	return 0;
}