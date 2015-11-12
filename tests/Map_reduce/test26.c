// Compile sans erreur

int addOne(int a)
{
	return a+1;
}

float half(int a)
{
	float b;
	b = a;

	return a/2.0;
}

int main(int argc, char const *argv[])
{
	int A[10];
	int B[];
	float C[];
	int i;

	for (i=0; i<10; i=i+1)
		A[i] = i;

	B = map(addOne, A);
	C = map(half, A);

	return 0;
}