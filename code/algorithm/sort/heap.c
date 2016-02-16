#include "sort.h"

void heap_sort(int *array,size_t count) {
	struct heap_node *root = NULL;

	root = build_max_heap(array,count);

	for (i = 0;i < count-1;++i) {
		array[i] = heap_remove_root(root);
	}
}
