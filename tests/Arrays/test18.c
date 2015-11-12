//Error :   incompatible types when assigning 'int[100]' to 'int[200]' in main line 14 
//			incompatible types when assigning 'int[]' to 'int[100]' in main line 15
//			incompatible types when assigning 'int' to 'int[]' in main line 17

int main()
{
	int A[];
	int B[100];
	int C[200];
	int a;

	a = 20;

	C = B;
 	B = A;

 	A = a;

 	return 0;
}