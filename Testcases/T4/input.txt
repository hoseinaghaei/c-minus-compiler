/*===  Sample 4  === */
void printArray(int A[], int size)
{
    int i;
    for (i=0; i<size; i=i+1){
        output(A[i]);
    }
}

void main(void)
{
    int arr[10];
    int arrsize;
    int i;
    int j;
    arrsize = 10;
    for (i=0; i< arrsize; i=i+1){
        arr[i] = -2;
        for (j=0; j< i; j=j+1){
            arr[i] = arr[i] * (0-2);
        }
    }

    printArray(arr, arrsize);
}
