int truc()
{
	return 1;
}

int main(int argc, char const *argv[])
{
	(int (*t)(void)) = truc;
	tab2 = map(truc, tab);
	return 0;
}