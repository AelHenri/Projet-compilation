// Compile sans erreur

int addInt(int a, int b)
{
	return a+b;
}

float multFloat(float a, float b)
{
	return a*b;
}

int main(int argc, char const *argv[])
{
	int A[10];
	float B[10];
	int i, a, b;

	for (i=0; i<10; i=i+1)
	{
		A[i] = i;
		B[i] = i + 0.6;
	}

	a = reduce(addInt, A);
	b = reduce(multFloat, B);

	return 0;
}