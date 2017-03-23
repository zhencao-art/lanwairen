#include <unordered_set>
#include <functional>
#include <iostream>

using namespace std;

struct pos_t {
	int offset;
	int length;
};

struct my_hash {
	size_t operator() (const pos_t &p) const {
		// hash<int> hasher;
		// return hasher(p.offset);
		return p.offset;
	}
};

int main(int argc,char **argv)
{
	unordered_set<pos_t,my_hash> positions;
	return 0;
}
