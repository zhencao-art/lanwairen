#include <iostream>

using namespace std;

void xxx(int a,int b) {
    cout << "a = " << a << " b = " << b << endl;
}



class AA {
public:
    void kill_myself(AA *a) {
        delete a;
        a = NULL;
    }
};

AA *a = new AA;

int main(int argc,char **argv)
{
    // int i = 0;

    // xxx(++i,i++);

//    a->kill_myself(a);
    int *p = NULL;
    delete p;

    return 0;
}
