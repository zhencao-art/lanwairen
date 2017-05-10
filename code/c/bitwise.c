#include <stdio.h>
#define __CHECK_ENDIAN__
#include <linux/types.h>

int main(int argc,char **argv)
{
    __le16 l16 = 0x0f;
    __be16 b16 = 0x0f;

    printf("%x %x\n",l16,b16);

    return 0;
}
