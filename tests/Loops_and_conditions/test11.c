//Compile sans erreur : for

int main()
{
	int a, i;
	float b;

	a = 10;
	b = 2.2;
	

	for (i=1; i < a; i = i+1)
	{
		b = b -1;
	}


	for (i=1; i != a; i = i+1)
	{
		b = b -1;
	}	

	for (i=1; i < 20 && i != b; i = i+1)
		a = a+1;
	
	for (;;);

}