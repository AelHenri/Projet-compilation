//Error : invalid argument type in function 'foo' (expected int, have int[10]) in main, line 13;

int foo(int a)
{
	return 0;
}

int main()
{
	int A[10];
	int a;

	a = foo(A);

	return 0;
}
