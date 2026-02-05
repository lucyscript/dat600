import math
import matplotlib.pyplot as plt
import sys

# Increase recursion limit for quicksort worst case
sys.setrecursionlimit(10000)

# Global counters for operations
operation_count = 0

# Insertion-sort with operation counting
def insertion_sort(arr):
    global operation_count
    operation_count = 0
    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1
        while i >= 0 and arr[i] > key:
            operation_count += 1  # comparison
            arr[i+1] = arr[i]
            i = i - 1
        if i >= 0:
            operation_count += 1  # final comparison that failed
        arr[i+1] = key
    return operation_count


# Merge-sort with operation counting
def merge_sort(arr, p, r):
    global operation_count
    if p < r:
        q = math.floor((p+r) / 2)
        merge_sort(arr, p, q)
        merge_sort(arr, q+1, r)
        merge(arr, p, q, r)

def merge(arr, p, q, r):
    global operation_count
    n1, n2 = q - p + 1, r - q
    left_arr, right_arr = [0] * (n1 + 1), [0] * (n2 + 1)
    for i in range(1, n1 + 1):
        left_arr[i] = arr[p + i - 1]
    for j in range(1, n2 + 1):
        right_arr[j] = arr[q + j]
    i, j = 1, 1
    for k in range(p, r + 1):
        operation_count += 1  # comparison
        if i <= n1 and (j > n2 or left_arr[i] <= right_arr[j]):
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1

def merge_sort_wrapper(arr):
    global operation_count
    operation_count = 0
    merge_sort(arr, 0, len(arr) - 1)
    return operation_count


# Heap-sort with operation counting
def left(i):
    return 2 * i + 1

def right(i):
    return 2 * i + 2

def max_heapify(arr, i, heap_size):
    global operation_count
    l = left(i)
    r = right(i)
    operation_count += 1  # comparison with left child
    if l < heap_size and arr[l] > arr[i]:
        largest = l
    else:
        largest = i
    operation_count += 1  # comparison with right child
    if r < heap_size and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, largest, heap_size)

def build_max_heap(arr):
    heap_size = len(arr)
    for i in range(math.floor(len(arr) / 2) - 1, -1, -1):
        max_heapify(arr, i, heap_size)

def heap_sort(arr):
    global operation_count
    operation_count = 0
    build_max_heap(arr)
    heap_size = len(arr)
    for i in range(len(arr) - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heap_size -= 1
        max_heapify(arr, 0, heap_size)
    return operation_count


# Quicksort with operation counting
def partition(arr, p, r):
    global operation_count
    x = arr[r]
    i = p - 1
    for j in range(p, r):
        operation_count += 1  # comparison
        if arr[j] <= x:
            i += 1
            arr[j], arr[i] = arr[i], arr[j]
    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    return i + 1

def quicksort(arr, p, r):
    global operation_count
    if p < r:
        q = partition(arr, p, r)
        quicksort(arr, p, q - 1)
        quicksort(arr, q + 1, r)

def quicksort_wrapper(arr):
    global operation_count
    operation_count = 0
    quicksort(arr, 0, len(arr) - 1)
    return operation_count


def plot_algorithm(sizes, steps, name, complexity_type, color, marker='o'):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, steps, f'{marker}-', label=name, color=color, linewidth=2)
    
    # Calculate scaling constant to fit theoretical curve to actual data
    # Use middle data points for better fit
    mid_idx = len(sizes) // 2
    if complexity_type == 'n2':
        # Find constant c such that c * n² ≈ actual operations
        c = steps[mid_idx] / (sizes[mid_idx] ** 2)
        theoretical = [c * n**2 for n in sizes]
        plt.plot(sizes, theoretical, '--', label=f'O(n²) scaled', color='red', alpha=0.6)
    elif complexity_type == 'nlogn':
        # Find constant c such that c * n log n ≈ actual operations
        c = steps[mid_idx] / (sizes[mid_idx] * math.log2(sizes[mid_idx]))
        theoretical = [c * n * math.log2(n) for n in sizes]
        plt.plot(sizes, theoretical, '--', label=f'O(n log n) scaled', color='red', alpha=0.6)
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Number of Operations')
    plt.title(f'{name} Performance')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f'{name.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_comparison(sizes, data_dict):
    plt.figure(figsize=(12, 7))
    for name, (steps, marker, color) in data_dict.items():
        plt.plot(sizes, steps, f'{marker}-', label=name, linewidth=2, color=color)
    
    plt.xlabel('Input Size (n)', fontsize=12)
    plt.ylabel('Number of Operations', fontsize=12)
    plt.title('Comparison of Sorting Algorithm Complexities', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.savefig('sorting_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


# Correctness test
base_arr = [2, 8, 7, 1, 3, 5, 6, 4]
arr = base_arr.copy()
insertion_sort(arr)
assert arr == [1, 2, 3, 4, 5, 6, 7, 8], "Insertion sort failed"
print(f"Correctness check passed: {base_arr} -> {arr}\n")

# Performance testing with varying input sizes
sizes = [10, 20, 30, 50, 75, 100, 150, 200, 300, 400, 500, 750, 1000, 1500, 2000]
insertion_steps = []
merge_steps = []
heap_steps = []
quicksort_steps = []

print("Running performance tests...")
for size in sizes:
    # Use worst case: reverse sorted array
    test_arr = list(range(size, 0, -1))
    
    arr = test_arr.copy()
    insertion_steps.append(insertion_sort(arr))
    
    arr = test_arr.copy()
    merge_steps.append(merge_sort_wrapper(arr))
    
    arr = test_arr.copy()
    heap_steps.append(heap_sort(arr))
    
    arr = test_arr.copy()
    quicksort_steps.append(quicksort_wrapper(arr))
    
    print(f"n={size:4d}: ins={insertion_steps[-1]:7d}, merge={merge_steps[-1]:6d}, "
          f"heap={heap_steps[-1]:6d}, quick={quicksort_steps[-1]:7d}")

print("\nGenerating plots...")
plot_algorithm(sizes, insertion_steps, 'Insertion Sort', 'n2', 'blue', 'o')
plot_algorithm(sizes, merge_steps, 'Merge Sort', 'nlogn', 'green', 's')
plot_algorithm(sizes, heap_steps, 'Heap Sort', 'nlogn', 'orange', '^')
plot_algorithm(sizes, quicksort_steps, 'Quicksort', 'n2', 'purple', 'd')

comparison_data = {
    'Insertion Sort': (insertion_steps, 'o', 'blue'),
    'Merge Sort': (merge_steps, 's', 'green'),
    'Heap Sort': (heap_steps, '^', 'orange'),
    'Quicksort': (quicksort_steps, 'd', 'purple')
}
plot_comparison(sizes, comparison_data)
