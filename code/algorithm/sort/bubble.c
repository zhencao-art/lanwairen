void bubble_sort(int *items, int len) {
    int i, j;

    for (i = 0; i < len; ++i) {
        for (j = i + 1; j < len; ++j) {
            if (items[i] > items[j]) {
                int temp = items[i];
                items[i] = items[j];
                items[j] = temp;
            }
        }
    }
}
