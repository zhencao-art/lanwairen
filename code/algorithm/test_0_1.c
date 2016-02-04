#include <stdio.h>

#include "alg_0_1.h"

void test_0_1_v2() {
	int max_volume = 10;
	int count = 4;
	int weight[] = {2,4,5,3};
	int value[] = {2,4,5,3};
	int result = 0;

	result = result_0_1_v2(weight,value,count,max_volume);

	printf("(%d,%d) = %d\n",count,max_volume,result);
}

void test_0_1_v1() {
	int max_volume = 10;
	int count = 4;
	int weight[] = {2,4,5,3};
	int value[] = {2,4,5,3};
	int result = 0;

	result = result_0_1_v1(weight,value,count,max_volume);

	printf("(%d,%d) = %d\n",count,max_volume,result);
}

void test_0_1() {
	int max_volume = 10;
	int count = 4;
	int weight[] = {2,4,5,3};
	int value[] = {2,4,5,3};
	int result = 0;

	result = result_0_1_recur(weight,value,count-1,max_volume);

	printf("(%d,%d) = %d\n",count,max_volume,result);
}

void run_all_test() {
	//test_0_1();
	//test_0_1_v1();
	test_0_1_v2();
}

int main(int argc,char **argv) 
{
	run_all_test();
	return 0;
}
