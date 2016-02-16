#include "sort.h"

/**
 * array_1 < array_2
 */
static void merge(int *array_1,size_t count_1,int *array_2,size_t count_2) {
	size_t i,j,k;
	int *temp = (int*)calloc(sizeof(int),count_1 + count_2);
	
	if (!temp) {
		return;	
	}

	for (i = 0,j = 0,k = 0; k < count_1 + count_2;++k) {
		if (i >= count_1) {
			temp[k] = array_2[j++];
			continue;
		}

		if (j >= count_2) {
			temp[k] = array_1[i++];
			continue;
		}

		if (array_1[i] < array_2[j]) {
			temp[k] = array_1[i++];
		} else {
			temp[k] = array_2[j++];
		}	
	}

	for (k = 0; k < count_1 + count_2;++k) {
		array_1[k] = temp[k];
	}

	free(temp);
}

void merge_sort(int *array,size_t count) {
	if (count == 1) {
		return;
	}

	merge_sort(array,count/2);
	merge_sort(array + count/2,(count+1)/2);
	merge(array,count/2,array + count/2,(count+1)/2);
}

