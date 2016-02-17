#ifndef _LIST_H_
#define _LIST_H_

struct list_node {
	struct list_node *next;
};

static inline void add_node(struct list_node *prev,struct list_node *node) {
	prev->next = node;
}

#endif
