#include <stdio.h>
// dp(i, j) = dp(i-1, j) if j < w[i]
// dp(i, j) = dp(i-1, j) + v[i] if j >= w[i]
//

int select(int *w, int *v, int count, int ca) {
    if (count <= 1) {
        if (w[count - 1] < ca) {
            return v[count - 1];
        } else {
            return 0;
        }
    }
    if (w[count - 1] > ca) {
        return select(w, v, count - 1, ca);
    } else {
        return select(w, v, count - 1, ca - w[count - 1]) + v[count - 1];
    }
}

int main(int argc, char **argv)
{
    int c = 2;
    int w[] = {2,3,1};
    int v[] = {4, 6, 2};

    printf("%d\n", select(w, v, 3, c));
    return 0;
}
