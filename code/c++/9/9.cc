#include <iostream>

using namespace std;

void xxx(int a,int b) {
    cout << "a = " << a << " b = " << b << endl;
}


int main(int argc,char **argv)
{
    int i = 0;

    xxx(++i,i++);

    return 0;
}
