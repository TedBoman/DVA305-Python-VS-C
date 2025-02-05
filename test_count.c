#include <stdio.h>
#include <time.h>

int main() {
    long long n = 1000000000;

    clock_t start, end;
    start = clock();

    for (long long i = 0; i < n; i++) {  // Declare i inside the loop or before
        ; // Empty loop
    }

    end = clock();
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%f\n", cpu_time_used);
    return 0;
}