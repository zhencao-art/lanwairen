
class B;

class A {
private:
    A() {}
    A(const A&);
friend class B;
};

class B : virtual public A {
};

class C : public B {
};

int main(int argc,char **argv)
{
    C c;
    return 0;
}
