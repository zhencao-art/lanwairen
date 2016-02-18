#include <stdlib.h>

#include "setree.h"

static int _insert(struct se_node *root,struct se_node *node) {
	int err = -1;

	if (node->key < root->key) {
		if (!root->left) {
			root->left = node;
			node->parent = root;
			err = 0;
		} else {
			err = _insert(root->left,node);
		}
	} else if (node->key == root->key) {
		err = -1;
	} else {
		if (!root->right) {
			root->right = node;
			node->parent = root;
			err = 0;
		} else {
			err = _insert(root->right,node);
		}
	}

	return err;
}

struct se_node* search(struct se_node *root,int key) {
	if (root && root->key == key) {
		return root;
	}

	if (root && key < root->key) {
		return search(root->left,key);
	}

	if (root && key > root->key) {
		return search(root->right,key);
	}

	return NULL;
}

struct se_node* insert(struct se_node **root,int key) {
	struct se_node *new_node = NULL;

	if (!root) {
		return NULL;
	}

	new_node = (struct se_node*)malloc(sizeof(struct se_node));
	if (!new_node) {
		return NULL;
	}
	new_node->left = NULL;
	new_node->right = NULL;
	new_node->key = key;

	if (!*root) {//null tree
		*root = new_node;
		new_node->parent = NULL;
	} else {
		if (_insert(*root,new_node) < 0) {
			free(new_node);
			new_node = NULL;
		}
	}

	return new_node;
}

void _earse(struct se_node **root,struct se_node *node) {
	/**
	 * has no children
	 */
	 if (!node->left && !node->right) {
		 if (node->parent) {
			*(node->parent->left == node?&(node->parent->left):&(node->parent->right)) = NULL;
		 } else {
			 *root = NULL;
		 }
	 }

	 if ((node->left && !node->right) || (!node->left && node->right)) {
		 if (node->parent) {
			 *(node->parent->left == node?&(node->parent->left):&(node->parent->right)) = (node->left?node->left:node->right);
			 (node->left?node->left:node->right)->parent = node->parent;
		 } else {
			 *root = (node->left?node->left:node->right);
			 (*root)->parent = NULL;
		 }
	 }

	 if (node->left && node->right) {
		 struct se_node *suc = _successor(node);

		 if (!suc->left && !suc->right) {
			 *(suc->parent->left == suc?&(suc->parent->left):&(suc->parent->right)) = NULL;
		 } else {
			 if (suc->parent->left == suc) {
				 suc->parent->left = suc->left?suc->left:suc->right;
			 } else {
				 suc->parent->left = suc->left?suc->left:suc->right;
			 }
			 (suc->left?suc->left:suc->right)->parent = suc->parent;
		 }
	 }

	 free(node);
}

void earse(struct se_node *root,int key) {
}

struct se_node* _predecessor(struct se_node *node) {
	if (!node) return NULL;

	return maximum(node->left);
}

struct se_node* predecessor(struct se_node *root,int key) {
	struct se_node *node = search(root,key);
	return _predecessor(node);
}

struct se_node* _successor(struct se_node *node) {
	struct se_node *parent,*iter;

	if (node->right) {
		return minimum(node->right);
	}

	parent = node->parent;
	iter = node;

	while (parent && iter == parent->right) {
		iter = parent;
		parent = parent->parent;
	}

	return parent;
}

struct se_node* successor(struct se_node *root,int key) {
	struct se_node *node = search(root,key);
	return _successor(node);
}

struct se_node* minimum(struct se_node *root) {
	struct se_node *iter = root;
	
	if (!root) {
		return NULL;
	}

	while(1) {
		if (!iter->left) {
			break;
		} else {
			iter = iter->left;
		}
	}

	return iter;
}

struct se_node* maximum(struct se_node *root) {
	struct se_node *iter = root;
	
	if (!root) {
		return NULL;
	}

	while(1) {
		if (!iter->right) {
			break;
		} else {
			iter = iter->right;
		}
	}

	return iter;
}
