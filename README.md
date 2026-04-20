# Sorting Algorithm Performance Experiments
**Student Name:** Yarin Plotnik, Shay Tidhar 
## Overview
This project measures and analyzes the runtime performance of different sorting algorithms across arrays of varying configurations (random vs. nearly sorted). 
**Selected Algorithms Evaluated:**
1. **Bubble Sort**
2. **Selection Sort**
3. **Quick Sort**

## How to Run the Benchmark (CLI)

The benchmarking tool provides a flexible Command-Line Interface (CLI) to define your own experiment parameters.

### Basic Usage
Execute `run_experiments.py` from your terminal using Python:

```bash
python run_experiments.py -a <algorithms> -s <sizes> -e <noise> -r <runs>
```

### Arguments Table
| Flag | Name | Description | Example |
| :--- | :--- | :--- | :--- |
| `-a` | `--algorithms` | The IDs of the sorting algorithms to run. `1`=Bubble, `2`=Selection, `5`=Quick. Multiple IDs are separated by spaces. | `-a 1 2 5` |
| `-s` | `--sizes` | A space-separated list of array sizes ($n$) to test. | `-s 100 500 1000` |
| `-e` | `--experiment` | The percentage of elements out of order. Use `-1` for entirely random arrays, or `5` for 5% noise (nearly sorted). | `-e -1` |
| `-r` | `--runs` | The number of times to repeat each test size to compute an average and standard deviation. | `-r 3` |

### Examples

**1. Test all algorithms on small random arrays, repeating 5 times:**
```bash
python run_experiments.py -a 1 2 5 -s 100 250 500 -e -1 -r 5
```

**2. Test Quick Sort against Bubble Sort on a nearly sorted array (5% noise), repeating once:**
```bash
python run_experiments.py -a 1 5 -s 500 1000 2000 -e 5 -r 1
```

*Note: Running $\mathcal{O}(n^2)$ algorithms (like Bubble or Selection Sort) on sizes greater than 3,000 will trigger a confirmation prompt.*

---
## Results on Random Arrays
**Figure 1** displays the empirical performance of the sorting algorithms scaling over different array sizes when filled with completely *random* integers.
![Random Arrays Plot](result1.png)
### Explanation:
- **Bubble Sort & Selection Sort:** Both algorithms follow a strict $\mathcal{O}(n^2)$ growth rate logic in random sequences. Selection Sort scans the whole remainder of the array every operation, while Bubble Sort executes heavy numbers of individual element swaps to push figures to the end, resulting in the high upward curves.
- **Quick Sort:** Follows an $\mathcal{O}(n \log n)$ distribution. As a vastly superior divide-and-conquer strategy, its runtime hugs strongly against the horizontal axis compared to the slower $\mathcal{O}(n^2)$ approaches.
---
## Results on Nearly Sorted Arrays (5% Noise)
**Figure 2** displays how the exact same algorithm codebases react when handling *nearly sorted* arrays where only 5% of elements are randomly swapped out of order.
![Nearly Sorted Plot](result2.png)
### How Running Times Changed & Why:
- **Bubble Sort Improvement:** Notice how the Bubble Sort curve flattened entirely compared to Figure 1! Our Bubble Sort implementation incorporates an "early exit" optimization (`if not swapped: break`). Because only 5% of elements were out of place, Bubble Sort quickly fixed the few local errors and broke its execution almost identically fast as Quick Sort.
- **Selection Sort Performance:** Selection Sort *did not* noticeably change its structure compared to the random sequence plot. This is because Selection Sort is completely ignorant of the array's "sortedness". It mathematically must compare every remaining element continuously scanning for the absolute minimum, locking it into the exact same worst-case $\mathcal{O}(n^2)$ evaluations regardless of the 5% noise level.
- **Quick Sort:** Quick Sort continues to operate at peak optimal efficiency. Its $\mathcal{O}(n \log n)$ divide-and-conquer logic isn't heavily impacted by the array already being mostly sorted because our implementation safely chooses the middle element as the pivot, meaning it maintains a beautifully balanced recursion tree and stays firmly at the bottom of the graph alongside Bubble Sort!

---

## Appendix: Large Input Evaluation ($n = 1,000,000$)

An extra experiment was conducted strictly for evaluating Quick Sort on massive inputs. The other two algorithms were deliberately skipped due to their excessive computational requirements at this scale.

### 1. Empirical Results for Quick Sort
- **Quick Sort ($n = 1,000,000$ random elements):** `~3.94 seconds`

Despite processing a million elements, execution completes very quickly. This perfectly reflects its highly efficient $\mathcal{O}(n \log n)$ temporal growth rate.

### 2. Runtime Estimations for $\mathcal{O}(n^2)$ Algorithms
To understand why Bubble Sort and Selection Sort were bypassed for inputs of $1,000,000$, we can extrapolate their expected runtimes based on their empirical speeds for a smaller size like $n = 3,000$.
Because both algorithms grow quadratically $(\mathcal{O}(n^2))$, scaling an array by a factor of $\approx 333.33$ (from $3,000$ to $1,000,000$) increases the runtime by a factor of $(333.33)^2 \approx 111,111$.

Based on baseline tests at $n=3,000$:
- **Bubble Sort Estimation:** `~47,155 seconds` (*approx. 13.1 hours*)
- **Selection Sort Estimation:** `~20,566 seconds` (*approx. 5.7 hours*)

Attempting to actually run these quadratic algorithms for arrays of $1,000,000$ items would genuinely take far too long!
