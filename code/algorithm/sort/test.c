#include "sort.h"

static size_t count = 10;
static int array[10] = {2,1,8,3,4,0,6,9,7,5};

static void test_quick() {
	//position(array,count,3);
	quick_sort(array,count);
}

static void run_all_test() {
	test_quick();
}

int main(int argc,char **argv)
{
	run_all_test();

	return 0;
}
