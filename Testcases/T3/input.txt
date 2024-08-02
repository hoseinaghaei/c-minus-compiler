/*==== Sample T3 ====*/
void main(void) {
	int arr[10];
	int var1;
	int var2;
	var1 = 1;
	arr[0] = var1 = var2 = 8;
	output(var1);
	output(arr[0]);
	arr[5] = var2 = 12;
	output(var1);
	output(var2);
	output(arr[5]);
}
