#include <stdio.h>


int* foo() {
    static int uu;
    return &uu;
}

int main(int argc,char **argv)
{
    int i = 0;
    int *p = NULL;

    for ( i = 0;i <5;++i) {
        p = foo();
        printf("%d: %ld\n",i,p);
    }
    return 0;
}
