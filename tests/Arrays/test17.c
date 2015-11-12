//Compile sans erreur

int main()
{
	int A[];
	int B[100];
	int C[200];

	int a, b ,c, i;

	a = 5;
	B[1] = a;

	b = A[1];

	for (c=0;c<200;c=c+1)
	{
		C[c] = a ;
	}

	B = C;
	A = B;

	for (i=0;i<200;i=i+1)
	{
		A[i] = a ;
	}

	return 0;

}