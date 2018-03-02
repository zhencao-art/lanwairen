#include <mutex>
#include <iostream>

int main(int argc, char **argv)
{
    std::mutex mt;
    mt.lock();
    std::cout << "lock-1" << std::endl;
    // mt.lock();
    // std::cout << "lock-2" << std::endl;
    mt.unlock();
    std::cout << "unlock-1" << std::endl;
    mt.unlock();
    std::cout << "unlock-2" << std::endl;
    return 0;
}
