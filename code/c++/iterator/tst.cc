#include <iostream>
#include <list>

using namespace std;


int main(int argc,char **argv)
{
	int items[] = {1,2,3,4,5,6};
	list<int> item_list;


	for (int i = 0; i < sizeof(items);++i) {
		item_list.push_back(items[i]);
	}

	for (list<int>::iterator i = item_list.begin();
			i != item_list.end() && (*i % 2);
			item_list.erase(i++)) {
		cout << *i << endl;
	}


	return 0;
}
