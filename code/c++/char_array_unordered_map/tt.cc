#include <unordered_map>
#include <iostream>
#include <iomanip>

using namespace std;

const char *p1 = "cao";
const char *p2 = "cao";
const char *p3 = "caozhen";

int main(int argc,char **argv)
{
    unordered_map<const char*,int> set;
    set["cao"] = 26;
    set["zhen"] = 28;

    cout << std::setbase(16) << "p1 = " << (long)p1
         << " p2 = " << (long)p2 << " p3 = " << (long)p3
         << endl;

    return 0;
}
