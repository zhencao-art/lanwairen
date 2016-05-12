#include <iostream>

using namespace std;

class T {
private:
    int x;
public:
    T() {
        x = 99;
        p = 88;
    }
    void print() {
        cout << x << endl;
        delete this;
        cout << x << endl;
    }
    int p;
};

int main(int argc,char **argv)
{
    T *p = new T;

    cout << "p = " << p->p << endl;
    p->print();

    delete p;

    p->p = 77;
    cout << "p = " << p->p << endl;

    return 0;
}
