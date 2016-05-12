#include <iostream>
#include <stdlib.h>

int main(int argc,char **argv)
{
    int *p = 0;
    delete p;
    free(p);
    return 0;
}
