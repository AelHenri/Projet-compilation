// Error : invalid argument type in function map (expected non-void function, array, have function, int)
//		   invalid argument type in function map (expected non-void function, array, have void function, array)


int addOne(int a)
{
	return a+1;
}

void half(int a)
{
	float b;
	b = a;
}

int main(int argc, char const *argv[])
{
	int A[10];
	int B[];
	float C[];
	int i;

	for (i=0; i<10; i=i+1)
		A[i] = i;


	B = map(addOne, 10);
	C = map(half, A);
	
	return 0;
}