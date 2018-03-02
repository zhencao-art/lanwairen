
template <typename T>
struct Point {
    T x;
    T y;

    T foo();
//     T foo() {
//         return x + y;
//     }
};

// template <typename T>
// T Point<T>::foo() {
//     return x + y;
// }
