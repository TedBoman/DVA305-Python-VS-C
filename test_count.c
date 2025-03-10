#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <n>\n", argv[0]);
        return 1;
    }

    long long n = atoll(argv[1]);

    long long result = 0; // Changed to a variable, no pointer needed.
    srand(42);

    // Generate random values beforehand
    int* random_values = (int*)malloc(n * sizeof(int));
    if (random_values == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    for (long long i = 0; i < n; i++) {
        random_values[i] = rand() % 10; // Random numbers between 0 and 9
    }

    clock_t start, end;
    start = clock();

    for (long long i = 0; i < n; i++) {
        result += random_values[i];
    }

    end = clock();

    printf("Result: %lld\n", result);

    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%f\n", cpu_time_used);

    free(random_values); // Free allocated memory
    return 0;
}