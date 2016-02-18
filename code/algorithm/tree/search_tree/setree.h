#ifndef _SE_TREE_H_
#define _SE_TREE_H_

/**
 * Support Operations: search minimum maximum predecessor successor
 * 					   insert delete
 */
struct se_node {
	struct se_node *left,*right,*parent;

	int key;
};

extern struct se_node* search(struct se_node *root,int key);
extern struct se_node* _predecessor(struct se_node *node);
extern struct se_node* _successor(struct se_node *node);
extern struct se_node* predecessor(struct se_node *root,int key);
extern struct se_node* successor(struct se_node *root,int key);
extern struct se_node* minimum(struct se_node *root);
extern struct se_node* maximum(struct se_node *root);
extern struct se_node* insert(struct se_node **root,int key);
extern void earse(struct se_node *root,int key);
extern void _earse(struct se_node **root,struct se_node *node);

#endif
