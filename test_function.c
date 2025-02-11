#include <stdio.h>
#include <time.h>

int my_function(int x) {
    return x * 2;
}

int main() {
    long long n = 100000000;
    int result = 0;

    clock_t start, end;
    start = clock();

    for (long long i = 0; i < n; i++) {
        result = my_function(i);
    }

    end = clock();
    printf("%d\n", result);
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%f\n", cpu_time_used);
    return 0;
}