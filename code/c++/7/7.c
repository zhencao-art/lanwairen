#include <stdio.h>

#pragma pack(4)

struct a_a {
    int x;
    char y;
    short z;
};

int main(int argc,char **argv)
{
    struct a_a a;
    printf("%d\n",sizeof(struct a_a));
    return 0;
}
