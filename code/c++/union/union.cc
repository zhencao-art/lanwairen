#include <string>

union {
    int i;
    std::string s; // illegal: std::string is not a POD type!
} u;
