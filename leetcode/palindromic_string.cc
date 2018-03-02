#include <iostream>
#include <cstring>

using namespace std;

bool IsPalindromicString(const char *str, int l) {
    if (l == 0 || l == 1) {
        return true;
    }
    if (str[0] == str[l - 1]) {
        return IsPalindromicString(str + 1, l -2);
    } else {
        return false;
    }
}

int main(int argc, char **argv)
{
    cout << IsPalindromicString(argv[1], strlen(argv[1])) << endl;
    return 0;
}
