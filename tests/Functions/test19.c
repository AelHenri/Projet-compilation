//Compile sans erreur

int foo(int a)
{
	return a+1;
}

int main()
{
	int a,b;

	a = 5;
	b = foo(a);
	return 0;
}