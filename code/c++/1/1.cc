
template <typename type>
class A {
public:
    type& x;
};

class B : public A<B> {
};


int main(int argc,char **argv)
{
    B b;

    return 0;
}
