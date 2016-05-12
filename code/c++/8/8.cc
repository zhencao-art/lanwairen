#include <iostream>

class Base {
public:
    void print() {
        std::cout << "print" << std::endl;
    }
    int x;
};

int main(int argc,char **argv)
{
    Base a;
    a.x = 99;

    void (*fun)();
    int *p;
   
    p = (int*)(&a); 
    //fun = (void (*)())(*(&a));
    //fun();

    std::cout << *p << std::endl;

    return 0;
}
