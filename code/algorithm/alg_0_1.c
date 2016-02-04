#include "alg_0_1.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

/**
 * The recursive implementation of the 0-1 quresion
 */
int result_0_1_recur(int *weight,int *value,int max_index,int volume) {
	int no_choice,choiced;

	if (max_index < 0) {
		return 0;
	}
	
	no_choice = result_0_1_recur(weight,value,max_index-1,volume);

	if (volume >= weight[max_index]) {
		choiced = result_0_1_recur(weight,value,max_index-1,volume-weight[max_index]) + value[max_index];
	} else {
		return no_choice;
	}

	return MAX(no_choice,choiced);
}

int result_0_1_v1(int *weight,int *value,int count,int volume) {
	int *r_p = (int*)calloc(sizeof(int),(count+1)*(volume+1));

	int i,j,result;

	if (!r_p) {
		return -ENOMEM;
	}

	for (i = 1;i <= count;++i) {
		for (j = weight[i-1];j <= volume;++j) {
			if (r_p[(i-1)*volume + j] > (r_p[(i-1)*volume + (j-weight[i-1])] + value[i-1])) {
				r_p[i*volume + j] = r_p[(i-1)*volume + j];
			} else {
				r_p[i*volume + j] = r_p[(i-1)*volume + (j-weight[i-1])] + value[i-1];
			}
		}	
	}

	result = r_p[count*volume + volume];
	free((void*)r_p);

	return result;
}
