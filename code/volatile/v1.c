
int foo(int x) {
    return x + 1;
}

int main(int argc, char **argv)
{
    int a = 5;
    int b = 10;
    int c = 20;

    a = foo(c);

    return 0;
}
