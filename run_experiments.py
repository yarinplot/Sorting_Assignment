import random
import time
import statistics
import argparse
import matplotlib.pyplot as plt

# --- Sorting Algorithms ---

def bubble_sort(arr):
    """
    Sorts an array using the classic Bubble Sort algorithm.
    Includes an early exit optimization if the array is completely sorted.
    Time Complexity: O(n^2) worst case, O(n) best case.
    """
    n = len(arr)
    # Loop through all array elements
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no two elements were swapped by inner loop, then break
        if not swapped:
            break
    return arr

def selection_sort(arr):
    """
    Sorts an array using the Selection Sort algorithm.
    Continuously scans for the minimum element and swaps it to the front.
    Time Complexity: O(n^2) across all cases.
    """
    # Traverse through all array elements
    for i in range(len(arr)):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

def quick_sort(arr):
    """
    Sorts an array using a recursive Quick Sort algorithm.
    Note: Uses list comprehensions (out-of-place) for readability.
    Time Complexity: O(n log n) average case.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- Experiment Helpers ---

def measure_runtime(func, arr):
    """
    Executes a sorting algorithm on a given array and returns 
    the exact execution runtime in seconds using perf_counter.
    """
    start = time.perf_counter()
    func(arr)
    return time.perf_counter() - start

def add_noise(arr, noise_level):
    """
    Takes a perfectly sorted base array and partially scrambles it by 
    randomly swapping a percentage of its internal elements.
    """
    noisy_arr = arr.copy()
    n = len(noisy_arr)
    num_swaps = int(n * noise_level / 2)
    for _ in range(num_swaps):
        idx1, idx2 = random.sample(range(n), 2)
        noisy_arr[idx1], noisy_arr[idx2] = noisy_arr[idx2], noisy_arr[idx1]
    return noisy_arr

# --- CLI Entrypoint ---

def main():
    """
    Main orchestration function.
    Parses dynamic flags from the terminal (-a, -s, -e, -r), validates safety constraints, 
    executes tests mapped to requested algorithms, and plots the results.
    """
    parser = argparse.ArgumentParser(description="Sorting Algorithm Runtime Experiments")
    parser.add_argument('-a', '--algorithms', type=int, nargs='+', required=True, 
                        help="Algorithms to compare: 1=Bubble, 2=Selection, 5=Quick")
    parser.add_argument('-s', '--sizes', type=int, nargs='+', required=True, 
                        help="Array sizes, e.g., 100 500 1000")
    parser.add_argument('-e', '--experiment', type=int, required=True, 
                        help="Noise percentage (e.g., 5 for 5%% noise). Use -1 for entirely random arrays.")
    parser.add_argument('-r', '--runs', type=int, required=True, 
                        help="Number of repetitions per size")
    args = parser.parse_args()

    algo_map = {
        1: ("Bubble Sort", bubble_sort),
        2: ("Selection Sort", selection_sort),
        5: ("Quick Sort", quick_sort)
    }

    selected_algos = []
    for a in args.algorithms:
        if a in algo_map:
            selected_algos.append(a)
        else:
            print(f"WARNING: Unknown algorithm ID {a} ignored. Valid options: 1, 2, 5.")
    
    if not selected_algos:
        print("ERROR: No valid algorithms selected. Exiting.")
        return

    if any(s > 3000 for s in args.sizes):
        print("\nWARNING: You selected an array size larger than 3000. This might take a very long time!")
        choice = input("Do you want to continue? (y/n): ").strip().lower()
        if choice != 'y':
            print("Terminating experiment. Please run again with smaller sizes.")
            return

    if args.experiment >= 0:
        noise_level = args.experiment / 100.0
        title_suffix = f" (Nearly sorted, noise Level: {args.experiment}%)"
        out_file = "result2.png"
    else: 
        noise_level = None
        title_suffix = ""
        out_file = "result1.png"
        
    print(f"\nRunning experiment {args.experiment} with target arrays: {args.sizes}")
    print(f"Repetitions: {args.runs}\n")

    results = {a: {'avg': [], 'std': []} for a in selected_algos}

    for size in args.sizes:
        times = {a: [] for a in selected_algos}
        
        for _ in range(args.runs):
            if args.experiment < 0:
                base_arr = [random.randint(1, size) for _ in range(size)]
            else:
                base_arr = list(range(size))
                base_arr = add_noise(base_arr, noise_level)
            
            for a in selected_algos:
                algo_name, algo_func = algo_map[a]
                times[a].append(measure_runtime(algo_func, base_arr.copy()))
                
        print(f"Size: {size:5d}", end="")
        for a in selected_algos:
            avg_time = statistics.mean(times[a])
            std_time = statistics.stdev(times[a]) if args.runs > 1 else 0.0
            results[a]['avg'].append(avg_time)
            results[a]['std'].append(std_time)
            short_name = algo_map[a][0].split()[0]
            print(f" | {short_name}: {avg_time:.5f}s (±{std_time:.5f})", end="")
        print()

    plt.figure(figsize=(10, 5))
    plt.rcParams.update({'font.size': 9})

    colors_markers = {
        1: ('#1f77b4', 'o'),  # Blue
        2: ('#ff7f0e', 's'),  # Orange
        5: ('#2ca02c', '^')   # Green
    }

    for a in selected_algos:
        algo_name = algo_map[a][0]
        avg_list = results[a]['avg']
        std_list = results[a]['std']
        
        lower_bound = [avg - std for avg, std in zip(avg_list, std_list)]
        upper_bound = [avg + std for avg, std in zip(avg_list, std_list)]
        
        c, m = colors_markers.get(a, ('gray', 'x'))
        plt.plot(args.sizes, avg_list, label=algo_name, marker=m, color=c)
        plt.fill_between(args.sizes, lower_bound, upper_bound, alpha=0.2, color=c)

    plt.xlabel('Array Size (n)')
    plt.ylabel('Average Runtime (seconds)')
    plt.title(f'Sorting Algorithm Runtime Comparison{title_suffix}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_file)
    print(f"\nPlot saved as '{out_file}'")
    plt.show()

if __name__ == '__main__':
    main()