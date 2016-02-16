#include "sort.h"
#include "binary_tree.h"

static size_t count = 10;
static int array[10] = {2,1,8,3,4,0,6,9,7,5};

struct TNode {
	int x;
	int y;
	struct t_node tnode;
};

static void test_container_of() {
	struct TNode t;
	struct TNode *t_p = NULL;

	t.x = 1;
	t.y = 2;

	binary_tree_init(&t.tnode);
	
	t_p = container_of(&(t.tnode),struct TNode,tnode);
}

static void test_quick() {
	//position(array,count,3);
	quick_sort(array,count);
}

static void test_merge() {
	merge_sort(array,count);
}

static void run_all_test() {
	//test_quick();
//	test_merge();
	test_container_of();
}

int main(int argc,char **argv)
{
	run_all_test();

	return 0;
}
