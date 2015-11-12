//Error : missing return value in function 'foo' in foo line 7

int foo(int a)
{
	int b;
	b = a;
}

int main()
{
	int a, b;

	a = 10;
	b = foo(a);

	return 0;
}
