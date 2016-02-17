
#define INT_BITS 32
#define INT_MAX (1<<(INT_BITS-1)-1)
#define INT_MIN (-INT_MAX-1)

int find_sec_max(int array[],int length) {
	int i;
	int max = array[0];
	int sec_max = INT_MIN;

	for (i = 1;i < length;++i) {
		if (array[i] > max) {
			sec_max = max;
			max = array[i];
		} else {
			if (array[i] > sec_max) {
				sec_max = array[i];
			}
		}
	}

	return sec_max;
}

static int length = 5;
static int array[] = {1,2,3,4,5};

int main(int argc,char **argv)
{
	int sec_max;

	sec_max = find_sec_max(array,length);

	return 0;
}
