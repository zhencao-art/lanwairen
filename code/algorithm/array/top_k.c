
void top_k(const int *in, int len, int *out, int k) {
    int i = k - 1;
    for (; i >= 0; --i) {
        out[i] = in[0];
        int j = 0;
        for (; j < len; ++j) {
            if (in[j] > out[i]) {
                int x = in[j];
                in[j] = out[i];
                out[i] = x;
            }
        }
    }
}

int paration(int *arr, int len) {
    return 0;
}

void quick_select(int *arr, int len, int k) {
    if (!arr || len <= k) {
        return;
    }

    int rc = paration(arr, len);
    if (rc < k) {
        quick_select(arr + rc, len - rc, k);
    } else if (rc > k) {
        quick_select(arr, rc + 1, k);
    }
}
