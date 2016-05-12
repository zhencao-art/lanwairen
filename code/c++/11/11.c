#include <stdio.h>

struct a_a {
    int x;
};

#define xxx(ptr) \
(\
    typeof((ptr) + 1) __tmp = (ptr); \
    __tmp.x == 0;\
)


int main(int argc,char **argv)
{
    struct a_a a = {.x = 0,};

    if (xxx(a)) {
        printf("xxx");
    }

    return 0;
}
