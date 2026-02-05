package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func insertionSort(arr []int) {
	for j := 1; j < len(arr); j++ {
		key := arr[j]
		i := j - 1
		for i >= 0 && arr[i] > key {
			arr[i+1] = arr[i]
			i = i - 1
		}
		arr[i+1] = key
	}
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "Usage: %s <array_size>\n", os.Args[0])
		os.Exit(1)
	}

	n, err := strconv.Atoi(os.Args[1])
	if err != nil || n <= 0 {
		fmt.Fprintf(os.Stderr, "Array size must be a positive integer\n")
		os.Exit(1)
	}

	// Allocate and fill array with reverse sorted data (worst case)
	arr := make([]int, n)
	for i := 0; i < n; i++ {
		arr[i] = n - i
	}

	// Measure execution time
	start := time.Now()
	insertionSort(arr)
	elapsed := time.Since(start)

	// Print result in seconds
	fmt.Printf("%.6f\n", elapsed.Seconds())
}
