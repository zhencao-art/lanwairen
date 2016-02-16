#ifndef _BINARY_TREE_H_
#define _BINARY_TREE_H_

#include <stdlib.h>

struct t_node {
	struct t_node *left;
	struct t_node *right;
};

#define BINARY_TREE_INIT(name) {.left = NULL;.right = NULL;}

static inline void binary_tree_node_init(struct t_node *node) {
	node->left  = NULL;
	node->right = NULL;
}

#define BINARY_TREE(name) \
	struct t_node name = BINARY_TREE_INIT(name)

#define container_of(ptr,type,member) ((type*)((void*)ptr - (void*)&(((type*)0)->member)))
#define tree_entry(ptr,type,member) \
	container_of(ptr,type,member)

static inline void add_left_child(struct t_node *parent,struct t_node *child) {
	parent->left = child;
}

static inline void splice_left_child(struct t_node *parent) {
	parent->left = NULL;
}


static inline void add_right_child(struct t_node *parent,struct t_node *child) {
	parent->right = child;
}

static inline void splice_right_child(struct t_node *parent) {
	parent->right = NULL;
}

extern struct t_node* mid_next(struct t_node *root);
extern struct t_node* mid_next_v2(struct t_node *root);

#endif
