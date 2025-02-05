import time
import subprocess
import platform
import matplotlib.pyplot as plt

def compile_c_code(filename, output_name):
    compiler = "gcc"  # Default compiler
    if platform.system() == "Windows":
        compiler = "gcc"  # Or "cl" if you're using Visual Studio's compiler
        output_name += ".exe" #add .exe extension to the output file
    try:
        subprocess.run([compiler, filename, "-o", output_name], check=True) #check=True raises an exception if the compilation fails
        return True
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")
        return False

def test_count_python(n):
    start_time = time.time()
    for i in range(n):
        pass
    end_time = time.time()
    return end_time - start_time

def test_arithmetic_python(n):
    start_time = time.time()
    result = 0
    for i in range(n):
        result += i * 2 + i / 3 - i % 5
    end_time = time.time()
    return end_time - start_time

def test_array_python(n):
    start_time = time.time()
    my_list = list(range(n))
    for i in range(n):
        my_list[i] *= 2
    end_time = time.time()
    return end_time - start_time

def test_function_python(n):
    def my_function(x):
        return x * 2
    start_time = time.time()
    for i in range(n):
        my_function(i)
    end_time = time.time()
    return end_time - start_time

def test_c(n, filename, num_runs=5):  # Added num_runs parameter
    output_name = filename[:-2] if filename.endswith(".c") else filename
    if not compile_c_code(filename, output_name):
        return None

    times = []
    for _ in range(num_runs):
        start_time = time.time() #time the whole execution
        try:
            subprocess.run(["./" + output_name], capture_output=True, check=True, text=True)
            output = subprocess.run(["./" + output_name], capture_output=True, check=True, text=True)
            c_time = float(output.stdout)
            times.append(c_time)
        except subprocess.CalledProcessError as e:
            print(f"C execution failed: {e}")
            return None
        end_time = time.time()

    return sum(times) / len(times)  # Return the average time

def main():
    n = 100000000  # Number of iterations
    num_runs = 1  # Number of times to run each test

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
        python_time_avg = sum(python_runs) / len(python_runs)  # Calculate average HERE
        python_times.append(python_time_avg)

        c_runs = []
        for _ in range(num_runs):
            c_runs.append(test_c(n, test["c_file"], 1))  # Run C test once per loop
        c_time_avg = sum(c_runs) / len(c_runs)  # Calculate average HERE
        c_times.append(c_time_avg)

        # Print results for this test
        print(f"--- {test['name'].upper()} TEST ---")
        print(f"Python time (average of {num_runs}): {python_time_avg:.4f} seconds")
        print(f"C time (average of {num_runs}): {c_time_avg:.4f} seconds")
        if c_time_avg!= 0:  # Avoid division by zero
            print(f"C is {python_time_avg / c_time_avg:.2f}x faster than Python")
        else:
            print("C time is zero")
        print("-" * 20)

    # Create the bar chart (this part is now correct)
    width = 0.35  # Width of the bars
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
