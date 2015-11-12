// Error : invalid argument type in function reduce (expected non-void binary function, array, have non-void unary function, array) in main; line 25
//			invalid argument type in function map (expected non-void binary function, array, have void function, array)

int addOne(int a)
{
	return a+1;
}

void multFloat(float a, float b)
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

	a = reduce(addOne, A);
	b = reduce(multFloat, B);

	return 0;
}