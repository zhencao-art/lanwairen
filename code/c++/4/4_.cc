#include <stdio.h>

class Singleton {
private:
    Singleton() {}
    Singleton(const Singleton&);
public:
    static Singleton* instance() {
        static Singleton a;
        return &a;
    }
};

int main(int argc,char **argv)
{
    for (int i = 0;i < 5;++i) {
        printf("%d %ld\n",i,Singleton::instance());
    }
    return 0;
}
