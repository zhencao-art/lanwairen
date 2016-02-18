#include <stdio.h>
#include "setree.h"

static void run_test() {
	struct se_node *root = NULL;
	struct se_node *iter = NULL;

	insert(&root,8);
	_earse(&root,root);
//	insert(&root,5);
//	insert(&root,4);
//	insert(&root,6);
//	insert(&root,9);
//
//	iter = minimum(root);
//
//	while (iter) {
//		printf("%d\t",iter->key);
//		iter = _successor(iter);
//	}
//
//	printf("\n");
}

int main(int argc,char **argv)
{
	run_test();
	return 0;
}
