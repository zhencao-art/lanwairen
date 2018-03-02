hhhhhhhinclude <iostream>

using namespace std;

class Base {
 public:
     Base() {
         foo();
     }

     virtual ~Base() {
         foo();
     }

     virtual void foo() {
         cout << "Base:foo" << endl;
     }
};

class BaseA : public Base {
 public:
     void foo() {
         cout << "BaseA:foo" << endl;
     }
};

int main(int argc, char **argv)
{
    BaseA a;

    cout << sizeof(a) << endl;
    return 0;
}

ab --> ba --> ab --> ba --> ab
       1      2       3     4

abc --> cab --> bca --> abc
         1       2       3
