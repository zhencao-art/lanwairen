#include <stdlib.h>
#include "binary_tree.h"

static size_t count = 10;
static int array[] = {1,2,3,4,5,6,7,8,9,10};

struct test_node {
	int x;
	struct t_node tnode;
};


struct test_node* build_tree(int *array,size_t count) {
	size_t i;
	struct test_node *root = NULL,*node_p = NULL;

	for (i = 0;i < count;++i) {
		node_p = (struct test_node*)malloc(sizeof(struct test_node));
		if (!node_p) {
			break;
		}
		node_p->x = array[i];
		binary_tree_node_init(&node_p->tnode);

		if (!root) {
			root = node_p;
		} else {
			if (i%2) {
				add_left_child(&root->tnode,&node_p->tnode);
			} else {
				add_right_child(&root->tnode,&node_p->tnode);
			}
		}
	}

	return root;
}

void mid_print(struct test_node *root,int *out) {
	struct t_node *iter = &root->tnode;
	int i = 0;

	while(iter = mid_next(iter)) {
		out[i++] = container_of(iter,struct test_node,tnode)->x;
	}
}

int main(int argc,char **argv)
{
	struct test_node *root = NULL;
	root = build_tree(array,count);

	mid_print(root,array);

	return 0;
}
