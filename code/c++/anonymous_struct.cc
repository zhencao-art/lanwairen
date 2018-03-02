#include <iostream>

using namespace std;

int main(int argc, char **argv) {
    struct {
        int x;
        int y;
    } p1 = {0, 100};
    cout << p1.x << ", " << p1.y << endl;
    return 0;
}
