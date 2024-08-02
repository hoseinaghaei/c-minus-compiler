/*===== Sample 8 =====*/
int sum(int b[], int arrsize){
	int s;
	int i;
	s = 0;
        for (i=0; i< arrsize; i=i+1){
		s = s + b[i];
	}
	return s;
}

int fib(int n){
	int fib1;
	int fib2;
	int j;
	int res;
	fib1 = 1;
	fib2 = 2;
        for (j=0; j< (n+1); j=j+1){
		res = fib1 + fib2;
		output(res);
		fib1 = fib2;
		fib2 = res;
	}
	return res;
}

void main(void){
	int a[9];
	int j;
        for (j=0; j< 9; j=j+1){
		a[j] = j + 1;
	}
	output(sum(a,9));
	output(fib(3));
}
