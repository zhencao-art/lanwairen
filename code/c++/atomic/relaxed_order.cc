#include <thread>
#include <atomic>
#include <iostream>

std::atomic<int> x;
std::atomic<int> y;
int r1,r2;

void thread_1() {
    r1 = y.load(std::memory_order_relaxed);
    x.store(r1,std::memory_order_relaxed);
    std::cout << "thread_1 r1 = " << r1
              << "r2 = " << r2 << std::endl;
}

void thread_2() {
    r2 = x.load(std::memory_order_relaxed);
    y.store(42,std::memory_order_relaxed);
    std::cout << "thread_2 r1 = " << r1
              << "r2 = " << r2 << std::endl;
}

int main(int argc,char **argv)
{
    std::thread th_1(thread_1);
    std::thread th_2(thread_2);

    th_1.join();
    th_2.join();

    return 0;
}
