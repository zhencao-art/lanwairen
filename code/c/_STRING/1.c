#include <stdio.h>

#define _STRING(x) #x

int main(int argc,char **argv) 
{
    const char *str = _STRING(x+y);

    printf("%s",str);
    return 0;
}
