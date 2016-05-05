
class noncopyable {
private:
    noncopyable(const noncopyable& inst);
    noncopyable& operator = (const noncopyable& inst);
protected:
    noncopyable() {}
};


class A : noncopyable {
};


int main(int argc,char **argv)
{
    A a;

    return 0;
}
