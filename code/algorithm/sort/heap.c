#include "sort.h"

static inline size_t right_index(size_t index) {
	return 2*(index+1);
}

static inline size_t left_index(size_t index) {
	return 2*(index+1) - 1;
}

static void max_heapify(int *array,size_t count,size_t index) {
	size_t left,right,largest;

	left = left_index(index);
	right = right_index(index);
	largest = index;

	if (left < count && array[left] > array[index]) {
		largest = left;
	}

	if (right < count && array[right] > array[largest]) {
		largest = right;
	}

	if (largest != index) {
		SWAP(array[largest],array[index]);
		max_heapify(array,count,largest);
	}
}

static void build_max_heap(int *array,size_t count) {
	int it;

	for (it = DOWN_INT(count,2)-1;it >= 0;--it) {
		max_heapify(array,count,it);
	}
}

void heap_sort(int *array,size_t count) {
	size_t it;

	build_max_heap(array,count);

	for (it = count-1;it >=1;--it) {
		SWAP(array[0],array[it]);
		max_heapify(array,it,0);
	}
}
