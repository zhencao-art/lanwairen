#include <iostream>
#include <list>
#include <algorithm>

using namespace std;

template<typename type,type upper>
class Big {
public:
    bool operator()(type a) {
        return a > upper;
    }
};

int main(int argc,char **argv)
{
    list<int> a;

    a.push_back(1);
    a.push_back(2);
    a.push_back(3);
    a.push_back(4);

    list<int>::const_iterator it = find_if(a.begin(),a.end(),Big<int,3>());

    cout << *it << endl;

    return 0;
}
