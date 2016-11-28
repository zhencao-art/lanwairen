#include <stdio.h>
#include <sys/prctl.h>
#include <string.h>

char process_name[32];

int main(int argc,char **argv)
{

	int ret = 0;

	memset(process_name,0,sizeof(process_name));
	if ((ret = prctl(PR_GET_NAME,process_name)) < 0) {
		fprintf(stderr,"prctl error,%d",ret);
		return -ret;
	}

	fprintf(stdout,"process_name = %s\n",process_name);

	return 0;
}
