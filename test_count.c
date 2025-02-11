#include <stdio.h>
#include <time.h>

int main() {
    long long n = 100000000;
    long long result = 0; // Important: Use a result variable

    clock_t start, end;
    start = clock();

    for (long long i = 0; i < n; i++) { // Corrected loop
        result += 1; // Prevent loop optimization
    }

    end = clock();

    // Print the result FIRST
    printf("Result: %lld\n", result);

    // THEN print the time, as the LAST thing
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%f\n", cpu_time_used);
    
    return 0;
}