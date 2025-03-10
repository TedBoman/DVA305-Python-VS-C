#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <n>\n", argv[0]);
        return 1;
    }

    long long n = atoll(argv[1]);

    double result = 0; // Initialize result to 0. Change to a double.
    srand(time(NULL)); // Seed the random number generator

    clock_t start, end;
    start = clock();

    for (long long i = 0; i < n; i++) {
        result = i * 2 + (double)i / 3 - i % 5; // Incorporate randomness
    }

    end = clock();

    printf("result: %f\n", result); // print result as a float.
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%f\n", cpu_time_used);
    return 0;
}