#include <stdio.h>

struct t_a {
};

int main(int argc,char **argv)
{
    struct t_a a;

    printf("%d\n",sizeof(a));

    return 0;
}
