#include <vector>
#include <stdlib.h>
#include <stdint.h>
#include <iostream>

using namespace std;

struct node_info {
	int64_t node_id;
};

struct node {
	struct node_info info;
	vector<struct node*> childs;
};

struct node* create_tree() {
	struct node *root = NULL;	
	
	root = new struct node;

	root->info.node_id = -1;

	return root;
}

void destroy_tree(struct node *root) {
	if (root) {
		for (vector<struct node*>::const_iterator iter = root->childs.begin();
			iter != root->childs.end();++iter) {
			destroy_tree(*iter);
		}
		delete root;
	}
	
	return;
}

struct node *find_node_by_id(struct node *root,int64_t id) {
    if (root) {
        if (root->info.node_id == id) {
            return root;
        } 
        
        for (vector<struct node*>::const_iterator iter = root->childs.begin();
                iter != root->childs.end();++iter) {
            struct node *found = find_node_by_id(*iter,id);

            if (found) {
                return found;
            }
        }
    }

    return NULL;
}

void add_node_by_node(struct node *parent,struct node *item) {
    if (parent) {
        parent->childs.push_back(item);
    }
}

struct node *add_node_by_id(struct node *root,int64_t parent_id,int64_t id) {
    struct node *parent = NULL;
    
    parent = find_node_by_id(root,parent_id);

    if (parent) {
        struct node *item = new struct node;
        item->info.node_id = id;
        add_node_by_node(parent,item);
        return item;
    }
    
    return NULL;
}


void TEST_ADD_ITEM() {
    struct node *root = create_tree();
    
    if (!root) {
        cerr << "Can not create a tree\n";
        exit(-1);
    }

    struct node *node_0 = add_node_by_id(root,root->info.node_id,0);

    if (node_0) {
        cout << "Add node_0 success\n";
    }
    struct node *node_1 = add_node_by_id(root,root->info.node_id,1);

    if (node_1) {
        cout << "Add node_1 success\n";
    }

    struct node *node_2 = add_node_by_id(root,node_0->info.node_id,2);

    if (node_2) {
        cout << "Add node_2 success\n";
    }

    if (node_0 == find_node_by_id(root,0)) {
        cout << "Find node_0 success\n";
    }

    if (node_1 == find_node_by_id(root,1)) {
        cout << "Find node_1 success\n";
    }

    if (node_2 == find_node_by_id(root,2)) {
        cout << "Find node_2 success\n";
    }

    destroy_tree(root);
}


int main(int argc,const char **argv) {    
    TEST_ADD_ITEM();
    return EXIT_SUCCESS;
}
