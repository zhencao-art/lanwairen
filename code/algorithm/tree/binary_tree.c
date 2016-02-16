#include "binary_tree.h"

struct t_node* mid_next(struct t_node *root) {
	if (!root) {
		return NULL;
	}
	if (!root->left) {
		return root;
	}

	return mid_next(root->left);
}

struct t_node* mid_next_v2(struct t_node *root) {
	if (!root) {
		return NULL;
	}
	while(root->left) {
		root = root->left;
	}
	return root;
}
