#include <stdio.h>

#define OPTION_INT(name) int name; 

#define OPTION(name,type,init) \
    OPTION_##type(name)

OPTION(max_msg_count,INT,0)

int main(int argc,char **argv)
{
    printf("%d\n",max_msg_count);
    return 0;
}
