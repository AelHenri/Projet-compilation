//Error : missing argument in function 'foo' (expected int, int, have int) in main line 13

int foo(int a, int b)
{
	return 0;
}

int main()
{
	int a, b;

	a = 10;
	b = foo(a);

	return 0;
}
