#include <iostream>
#include <functional>

using namespace std;

void print() {
    cout << "print cb" << endl;
}

typedef int (*cb_t) (void *,int,int);

void do_cb(cb_t cb,void *context) {
    int x = cb(context,1,2);
    cout << "x = " << x << endl; 
}

class Test {
public:
    int add(int a,int b) {
        return a + b;
    }
};

int cb(void *context,int a,int b) {
    return static_cast<Test*>(context)->add(a,b);
}


int main()
{
    Test test;

    do_cb(cb,&test);

    return 0;
}
