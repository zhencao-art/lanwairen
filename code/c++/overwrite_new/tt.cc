#include <iostream>

class Test {
public:
    void* operator new(size_t size) throw() {
        return nullptr;
    }

    void operator delete(void *ptr) {
    }
};

int main(int argc,char **argv) 
{
    Test *obj = new Test;
    return 0;
}
