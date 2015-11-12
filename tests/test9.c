//Compile sans erreur : conditions

int main()
{
	int a;
	float b;

	a = 1;
	b = 2.2;

	if (a<b)
		a = a +1;
	else b = b+1;


	if (a){
		a = a+1;
	}


	if (b){
		b = b+1;
	}


	if (a && b){
		a = a-1;
		b = b-1;
	}
	else {
		a = a+1;
		b = b+1;
	}

	if (a || b)
		a = a-1;
	return 0;
}