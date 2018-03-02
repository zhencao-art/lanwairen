#include <stdio.h>

void my_strcpy(const char *src, char *dst) {
    if (!src || !dst) {
        return;
    }
    while ('\0' != *src) {
        *dst = *src;
        src++;
        dst++;
    }
    *dst = '\0';
}

void my_strncpy(const char *src, int len, char *dst) {
    if (!src || !len || !dst) {
        return;
    }
    int i = 0;
    for (; i < len; ++i) {
        dst[i] = src[i];
    }
    dst[i] = '\0';
}

void *my_memcpy(const void *src, void *dst, int count) {
    int i = count - 1;
    for (; i >= 0; --i) {
        ((char *)dst)[i] = ((const char *)src)[i];
    }
    return dst;
}

int my_atoi(const char *in) {
    int ret = 0;

    while (*in != '\0') {
        ret = 10 * ret + (*in - '0');
        in++;
    }
    return ret;
}

int main(int argc, char **argv)
{
    printf("%d\n", my_atoi("10123"));
    return 0;
}
