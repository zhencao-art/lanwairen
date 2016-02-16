#ifndef _SORT_H_
#define _SORT_H_

#include <stdlib.h>

#define SWAP(x,y) do {x = x + y;y = x - y;x = x - y;} while(0)

extern void quick_sort(int *array,size_t count);

extern void merge_sort(int *array,size_t count);
#endif
