import time
import subprocess
import platform
import matplotlib.pyplot as plt

def compile_c_code(filename, output_name):
    compiler = "gcc"  # Default compiler
    if platform.system() == "Windows":
        compiler = "gcc"  # Or "cl" if you're using Visual Studio's compiler
    try:
        subprocess.run([compiler, filename, "-o", output_name, "-O0"], check=True) #check=True raises an exception if the compilation fails
        return True
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")
        return False

def test_count_python(n):
    start_time = time.perf_counter()
    for i in range(n):
        pass
    end_time = time.perf_counter()
    return end_time - start_time

def test_arithmetic_python(n):
    start_time = time.perf_counter()
    result = 0
    for i in range(n):
        result += i * 2 + i / 3 - i % 5
    end_time = time.perf_counter()
    return end_time - start_time

def test_array_python(n):
    start_time = time.perf_counter()
    my_list = list(range(n))
    for i in range(n):
        my_list[i] *= 2
    end_time = time.perf_counter()
    return end_time - start_time

def test_function_python(n):
    def my_function(x):
        return x * 2
    start_time = time.perf_counter()
    for i in range(n):
        my_function(i)
    end_time = time.perf_counter()
    return end_time - start_time

def test_c(n, filename, num_runs=5):
    output_name = filename[:-2] if filename.endswith(".c") else filename
    if platform.system() == "Windows":
      output_name += ".exe"
    if not compile_c_code(filename, output_name):
        return None

    times = []
    for _ in range(num_runs):
        try:
            # Run the C program and capture output
            if platform.system() == "Windows":
                result = subprocess.run([output_name], capture_output=True, text=True, check=True)
            else:
                result = subprocess.run(["./" + output_name], capture_output=True, text=True, check=True)

            # Split the output into lines
            output_lines = result.stdout.strip().split('\n')

            # Find the last line that can be converted to a float (the time)
            c_time = None
            for line in reversed(output_lines):
                try:
                    c_time = float(line)
                    break  # Exit loop once a valid float is found
                except ValueError:
                    continue  # Ignore lines that are not floats

            if c_time is not None:
                times.append(c_time)
            else:
                print(f"C program did not return a valid float. Output: {result.stdout}")
                return None  # No valid time found


        except subprocess.CalledProcessError as e:
            print(f"C execution failed: {e}")
            return None

    if not times:
        return None

    return sum(times) / len(times)

def main():
    n = 100000000  # Number of iterations
    num_runs = 1  # Number of times to run each test.  Increased for more stable results.

    tests = [
        {"name": "count", "python_func": test_count_python, "c_file": "test_count.c"},
        {"name": "arithmetic", "python_func": test_arithmetic_python, "c_file": "test_arithmetic.c"},
        {"name": "array", "python_func": test_array_python, "c_file": "test_array.c"},
        {"name": "function", "python_func": test_function_python, "c_file": "test_function.c"},
    ]

    test_names = []
    python_times = []
    c_times = []

    for test in tests:
        test_names.append(test["name"])

        python_runs = []
        for _ in range(num_runs):
            python_runs.append(test["python_func"](n))
        python_time_avg = sum(python_runs) / len(python_runs)
        python_times.append(python_time_avg)

        c_time_avg = test_c(n, test["c_file"], num_runs)  # Use num_runs here

        if c_time_avg is not None:
            c_times.append(c_time_avg)
        else:
            c_times.append(0)  # Append 0 if C test failed

        # Print results for this test
        print(f"--- {test['name'].upper()} TEST ---")
        print(f"Python time (average of {num_runs}): {python_time_avg:.4f} seconds")
        if c_time_avg is not None:
            print(f"C time (average of {num_runs}): {c_time_avg:.4f} seconds")
            if c_time_avg != 0:
                print(f"C is {python_time_avg / c_time_avg:.2f}x faster than Python")
            else:
                print("C time is zero")
        else:
            print("C test failed.")
        print("-" * 20)

    # Create the bar chart
    width = 0.35
    x = list(range(len(test_names)))

    fig, ax = plt.subplots()
    ax.bar([i - width/2 for i in x], python_times, width, label="Python")
    ax.bar([i + width/2 for i in x], c_times, width, label="C")

    ax.set_ylabel("Average Execution Time (seconds)")
    ax.set_title("Python vs. C Execution Time Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(test_names)
    ax.legend()

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()