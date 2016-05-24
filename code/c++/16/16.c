#include <stdio.h>

int main(int argc,char **argv)
{
    int index = 1;

    switch(index) {
    case 0 ... 9:
        printf("0-9\n");
    default:
        printf("other case\n");
    }

    return 0;
}
