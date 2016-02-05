#include "sort.h"

size_t position(int *array,size_t count,int seed) {
	int i = -1;
	int j = 0;
	int temp = 0;

	for (j = 0;j < count;++j) {
		if (array[j] < seed) {
			if (j > (i+1)) {
			//swap(array[i+1],array[j])
				temp = array[i+1];
				array[i+1] = array[j];
				array[j] = temp;
			}
			i++;
		}
	}

	temp = array[i+1];
	array[i+1] = array[count-1];
	array[count-1] = temp;

	return i+1;
}

void quick_sort(int *array,size_t count) {
	size_t mid;

	if (count <= 1) {
		return;
	}

	mid = position(array,count,array[count-1]);
	quick_sort(array,mid);
	quick_sort(array + mid + 1,count - mid - 1);
}

