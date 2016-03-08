#include <iostream>

using namespace std;


class A {
public:
	A() {}
	void foo() {
		delete this;
	}
};


int main(int argc,char **argv)
{
	return 0;
}
