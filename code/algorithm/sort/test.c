#include "sort.h"
#include <stdio.h>

static size_t count = 10;
static int array[10] = {2,1,8,3,4,0,6,9,7,5};

static void print() {
    int i = 0;

    for (i = 0;i < count;++i) {
        printf("%d \t",array[i]);
    }
    printf("\n");
}

static void test_heap() {
	heap_sort(array,count);
}

static void test_quick() {
	//position(array,count,3);
	quick_sort(array,count);
}

static void test_merge() {
	merge_sort(array,count);
}

static void run_all_test() {
	test_quick();
	//test_merge();
	//test_heap();
}

int main(int argc,char **argv)
{
	run_all_test();
    print();
	return 0;
}
