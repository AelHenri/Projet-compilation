//Error : incompatible types when assigning 'int' to 'int[10]' in main line 15

int foo(int a)
{
	return 0;
}

int main()
{
	int A[10];
	int a;

	a = 10;

	A = foo(a);

	return 0;
}
