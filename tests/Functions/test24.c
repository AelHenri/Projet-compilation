//Error : wrong return type in function 'jeanpierre' (expected int, have void) in 'jeanpierre', line 12

void foo(int a)
{
	a = a+1;
}

int jeanpierre()
{
	int a;
	a = 10;
	return foo(a);
}

int main()
{
	int a;
	a = jeanpierre();
	return 0;
}
