
struct radix_node {
    union {
        struct tmp {
            unsigned long tmp_x;
        };
        int union_x;
    };
};

int main(int argc,char **argv)
{
    struct radix_node root;

    root.union_x = 10;

    return 0;
}
