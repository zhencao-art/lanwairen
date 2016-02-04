#include "alg_0_1.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

/**
 * The recursive implementation of the 0-1 quresion
 *
 * dp(i,j) = Max(dp(i-1,j),dp(i-1,j-w[i])+v[i]) if i>=0
 */
int result_0_1_recur(int *weight,int *value,int max_index,int volume) {
	int no_choice,choiced;

	if (max_index < 0) {
		return 0;
	}
	
	no_choice = result_0_1_recur(weight,value,max_index-1,volume);

	if (volume >= weight[max_index]) {
		choiced = result_0_1_recur(weight,value,max_index-1,
				volume-weight[max_index]) + value[max_index];
	} else {
		return no_choice;
	}

	return MAX(no_choice,choiced);
}

static int r_p[5][11] = {0};

/**
 *
 * dp(i,j) = Max(dp(i-1,j),dp(i-1,j-w[i])+v[i]) if i>=0
 *
 */
int result_0_1_v1(int *weight,int *value,int count,int volume) {
	int i,j,result;
	int vol;
//	int *r_p = NULL;
//	
//	r_p = (int*)calloc(sizeof(int),(count+1)*(volume+1));
//	if (!r_p) {
//		return -ENOMEM;
//	}
//
	vol = volume + 1;	

	for (i = 1;i <= count;++i) {
		//for (j = weight[i-1];j <= volume;++j) {
		for (j = 1;j <= volume;++j) {
		//	r_p[i*vol + j] = MAX(r_p[(i-1)*vol + j],(r_p[(i-1)*vol + j - weight[i-1]] + value[i-1]));
			if (j >= weight[i-1]) {
				r_p[i][j] = MAX(r_p[i-1][j],r_p[i-1][j-weight[i-1]] + value[i-1]);
			} else {
				r_p[i][j] = r_p[i-1][j];
			}
			printf("(%d,%d) = %d\n",i,j,r_p[i][j]);
		}	
	}

	//result = r_p[count*volume + volume];
	result = r_p[count][volume];
	//free((void*)r_p);

	return result;
}

/**
 * dp(j) = Max(dp(j),dp(j-w[i])+v[i])
 */
int result_0_1_v2(int *weight,int *value,int count,int volume) {
	int i,j,result;
	int *r_p = NULL;
	
	r_p = (int*)calloc(sizeof(int),(volume+1));
	if (!r_p) {
		return -ENOMEM;
	}

	for (i = 1;i <= count;++i) {
		for (j = volume;j >= weight[i-1];--j) {
			r_p[j] = MAX(r_p[j],r_p[j-weight[i-1]] + value[i-1]);
			printf("(%d,%d) = %d\n",i,j,r_p[j]);
		}
	}

	result = r_p[volume];
	free((void*)r_p);

	return result;
}
