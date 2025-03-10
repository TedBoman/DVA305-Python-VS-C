#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int my_function(int x, int random_value) {
    return x * 2 + random_value;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <n>\n", argv[0]);
        return 1;
    }

    long long n = atoll(argv[1]);

    int result = 0; // Initialize result to 0
    srand(42); // Seed the random number generator

    clock_t start, end;
    start = clock();

    for (long long i = 0; i < n; i++) {
        int random_val = rand() % 100; // Generate a random number
        result = my_function(i, random_val); // Pass random value to function
    }

    end = clock();
    printf("%d\n", result);
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%f\n", cpu_time_used);
    return 0;
}