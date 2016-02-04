#include <alg_0_1.h>
#include <stdio.h>

void test_0_1() {
	int max_volume = 10;
	int count = 3;
	int weight[] = {3,4,5};
	int value[] = {3,4,5};
	int result = 0;

	result = result_0_1_recur(weight,value,count-1,max_volume);

	printf("(%d,%d) = %d\n",count,max_volume,result);
}

void run_all_test() {
	test_0_1();
}

int main(int argc,char **argv) 
{
	run_all_test();
	return 0;
}
