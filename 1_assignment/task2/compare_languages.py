import subprocess
import time
import matplotlib.pyplot as plt
import os

# Python implementation
def insertion_sort_python(arr):
    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1
        while i >= 0 and arr[i] > key:
            arr[i+1] = arr[i]
            i = i - 1
        arr[i+1] = key

def measure_python(size):
    arr = list(range(size, 0, -1))
    
    start = time.time()
    insertion_sort_python(arr)
    end = time.time()
    
    return end - start

def measure_go(size):
    try:
        result = subprocess.run(
            ['./insertion_sort_go', str(size)],
            capture_output=True,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError) as e:
        print(f"Error running Go program: {e}")
        return None

def compile_go():
    try:
        subprocess.run(
            ['go', 'build', '-o', 'insertion_sort_go', 'insertion_sort.go'],
            check=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return True
    except subprocess.CalledProcessError:
        print("Failed to compile Go program")
        return False

def main():
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("Running performance tests...\n")
    
    # Test with various input sizes
    sizes = [100, 500, 1000, 2000, 3000, 5000, 7000, 10000]
    
    python_times = []
    go_times = []
    
    for size in sizes:
        # Python
        py_time = measure_python(size)
        python_times.append(py_time)
        
        # Go
        go_time = measure_go(size)
        if go_time is not None:
            go_times.append(go_time)
        else:
            go_times.append(0)
    
    # Create comparison plot
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, python_times, 'o-', label='Python', linewidth=2, markersize=8, color='blue')
    plt.plot(sizes, go_times, 's-', label='Go', linewidth=2, markersize=8, color='green')
    plt.xlabel('Input Size (n)', fontsize=11)
    plt.ylabel('Execution Time (seconds)', fontsize=11)
    plt.title('Insertion Sort: Python vs Go Performance', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('language_comparison.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    main()
