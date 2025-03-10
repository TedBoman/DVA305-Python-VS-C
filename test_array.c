#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <n>\n", argv[0]);
        return 1;
    }

    // Convert command line argument to long long
    long long n = atoll(argv[1]);
    
    int *my_array = (int *)malloc(n * sizeof(int));
    if (my_array == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }

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