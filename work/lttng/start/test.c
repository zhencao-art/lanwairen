#include <stdio.h>
#include "my_template.h"

static void foo() {
	tracepoint(my_provider,my_first_tracepoint,10,"tracepoint");
}

int main(int argc,char **argv)
{
	foo();

	return 0;
}
