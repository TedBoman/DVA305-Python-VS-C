#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    long long n = 100000000;
    int *my_array = (int *)malloc(n * sizeof(int));

    clock_t start, end;
    start = clock();

    for (long long i = 0; i < n; i++) {
        my_array[i] = i;
    }
    for (long long i = 0; i < n; i++) {
        my_array[i] *= 2;
    }

    end = clock();

    printf("arr1 = %d\n", my_array[40]);
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%f\n", cpu_time_used);

    free(my_array);
    return 0;
}