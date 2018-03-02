#include <functional>
#include <iostream>

void print(int x) {
    std::cout << x << std::endl; 
}

void dispatch_fun(std::function<void()> fun) {
    fun();
}

int main(int argc, char **argv) {
    dispatch_fun(std::bind(&print, 1));
}
