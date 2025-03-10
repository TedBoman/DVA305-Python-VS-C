import random
import time
import subprocess
import platform
import matplotlib.pyplot as plt
import array

def compile_c_code(filename, output_name):
    compiler = "gcc"  # Default compiler
    if platform.system() == "Windows":
        compiler = "gcc"
    try:
        subprocess.run([compiler, filename, "-o", output_name, "-O3", "-std=c17"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")
        return False

def test_count_python(n):
    random_values = [random.randint(0, 9) for _ in range(n)] #Generate the random numbers before the timer.
    start_time = time.perf_counter()
    result = 0
    for i in range(n):
        result = i + random_values[i]
    end_time = time.perf_counter()
    print(f"Python count result (prevent optimization): {result}")
    return end_time - start_time

def test_arithmetic_python(n):
    start_time = time.perf_counter()
    result = 0
    for i in range(n):
        result += i * 2 + i / 3 - i % 5
    end_time = time.perf_counter()
    print(f"Python arithmetic result (prevent optimization): {result}")
    return end_time - start_time

def test_array_python(n):
    start_time = time.perf_counter()
    my_array = array.array('i', range(n))  # Create an array of integers
    for i in range(n):
        my_array[i] *= 2
    end_time = time.perf_counter()
    print(f"Python array result (prevent optimization): {my_array[n-1]}")
    return end_time - start_time

def test_function_python(n):
    random_values = [random.randint(0, 9) for _ in range(n)] #Generate the random numbers before the timer.
    def my_function(x, random_val):
        return x * 2 + random_val

    start_time = time.perf_counter()
    result = 0
    for i in range(n):
        result += my_function(i, random_values[i])
    end_time = time.perf_counter()
    print(f"Python function result (prevent optimization): {result}")
    return end_time - start_time

def test_c(n, c_file, num_runs):
    try:
        times = []
        for _ in range(num_runs):
            # Run with timeout to prevent hanging
            try:
                result = subprocess.run([f'./{c_file.replace(".c", "")}', str(n)], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=30)  # 30 second timeout
                if result.returncode == 0:
                    # Get the last line which contains the time
                    time_str = result.stdout.strip().split('\n')[-1]
                    times.append(float(time_str))
                else:
                    print(f"C program failed with error: {result.stderr}")
                    return None
            except subprocess.TimeoutExpired:
                print(f"C program timed out with n={n}")
                return None
        return sum(times) / len(times) if times else None
    except Exception as e:
        print(f"Error running C test: {e}")
        return None

def run_performance_tests(iterations_list, size_range, tests):
    """
    Run performance tests with different iterations and array sizes.
    
    Args:
        iterations_list (list): List of number of iterations [1, 10, 100]
        size_range (list): List of powers for array sizes from 2^18 to 2^27
        tests (list): List of test configurations
    """
    results = {
        'python': {},
        'c': {}
    }
    
    # Compile all C programs first
    for test in tests:
        output_name = test["c_file"].replace(".c", "")
        if not compile_c_code(test["c_file"], output_name):
            print(f"Failed to compile {test['c_file']}. Skipping C tests for {test['name']}")
            return None
    
    # Run tests for each iteration count
    for num_runs in iterations_list:
        results['python'][num_runs] = {}
        results['c'][num_runs] = {}
        
        # Test different array sizes
        for power in size_range:
            n = 2 ** power
            print(f"\nTesting with n={n:,} and {num_runs} iteration(s)")
            
            results['python'][num_runs][power] = []
            results['c'][num_runs][power] = []
            
            for test in tests:
                # Run Python tests
                python_runs = []
                for _ in range(num_runs):
                    python_runs.append(test["python_func"](n))
                python_time_avg = sum(python_runs) / len(python_runs)
                
                # Run C tests
                c_time_avg = test_c(n, test["c_file"], num_runs)
                if c_time_avg is None:
                    c_time_avg = 0
                
                # Store results
                results['python'][num_runs][power].append(python_time_avg)
                results['c'][num_runs][power].append(c_time_avg)
                
                # Print individual test results
                print(f"\n--- {test['name'].upper()} TEST ---")
                print(f"Python time (average of {num_runs}): {python_time_avg:.4f} seconds")
                print(f"C time (average of {num_runs}): {c_time_avg:.4f} seconds")
                if c_time_avg > 0:
                    print(f"C is {python_time_avg / c_time_avg:.2f}x faster than Python")
    
    return results

def plot_results(results, iterations_list, size_range, tests):
    """
    Create plots for the test results.
    """
    test_names = [test["name"] for test in tests]
    
    # Create a plot for each iteration count
    for num_runs in iterations_list:
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Performance Comparison with {num_runs} iteration(s)')
        
        for idx, test_name in enumerate(test_names):
            row = idx // 2
            col = idx % 2
            
            # Prepare data for plotting
            sizes = [2**power for power in size_range]
            python_times = [results['python'][num_runs][power][idx] for power in size_range]
            c_times = [results['c'][num_runs][power][idx] for power in size_range]
            
            # Create plot
            ax = axs[row, col]
            ax.plot(sizes, python_times, 'b-', label='Python')
            ax.plot(sizes, c_times, 'r-', label='C')
            ax.set_title(f'{test_name.capitalize()} Test')
            ax.set_xlabel('Array Size (N)')
            ax.set_ylabel('Execution Time (seconds)')
            ax.set_xscale('log', base=2)
            ax.set_yscale('log')
            ax.grid(True)
            ax.legend()
        
        plt.tight_layout()
        plt.show()

def save_results_to_file(results, iterations_list, size_range, tests, filename="results.txt"):
    """
    Save the test results to a file in a structured format.
    """
    test_names = [test["name"] for test in tests]
    
    with open(filename, "w") as f:
        for num_runs in iterations_list:
            f.write(f"\n\nResults with {num_runs} iteration(s):\n")
            for power in size_range:
                n = 2 ** power
                f.write(f"\nArray size (N): {n:,}\n")
                for idx, test_name in enumerate(test_names):
                    python_time = results['python'][num_runs][power][idx]
                    c_time = results['c'][num_runs][power][idx]
                    f.write(f"  {test_name.capitalize()} Test:\n")
                    f.write(f"    Python time: {python_time:.4f} seconds\n")
                    f.write(f"    C time: {c_time:.4f} seconds\n")
                    if c_time > 0:
                        f.write(f"    C is {python_time / c_time:.2f}x faster than Python\n")


def main():
    # Define tests
    tests = [
        {"name": "count", "python_func": test_count_python, "c_file": "test_count.c"},
        {"name": "arithmetic", "python_func": test_arithmetic_python, "c_file": "test_arithmetic.c"},
        {"name": "array", "python_func": test_array_python, "c_file": "test_array.c"},
        {"name": "function", "python_func": test_function_python, "c_file": "test_function.c"},
    ]
    random.seed(42)
    
    # Test parameters
    iterations_list = [10]
    size_range = range(18, 28)  # 2^18 to 2^27
    
    # Run all tests
    results = run_performance_tests(iterations_list, size_range, tests)
    
    if results is not None:
        save_results_to_file(results, iterations_list, size_range, tests)
        # Plot results
        plot_results(results, iterations_list, size_range, tests)
    else:
        print("Testing failed due to compilation errors")

if __name__ == "__main__":
    main()