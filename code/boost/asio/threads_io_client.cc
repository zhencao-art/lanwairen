#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

#include <iostream>

using namespace std;

int main(int ragc,char **argv)
{
	int fd = 0;

	if ((fd = socket(AF_INET,SOCK_STREAM,0)) < 0) {
		cerr << strerror(errno) << endl;
		return errno;
	}

	struct sockaddr_in server_addr;
	memset(&server_addr,0,sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(50000);
	server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

	if (connect(fd,(struct sockaddr*)&server_addr,sizeof(server_addr)) < 0) {
		cerr << strerror(errno) << endl;
		close(fd);
		return errno;
	}
	char buffer[512];
	ssize_t count = 0;
	while((count = read(fd,buffer,512))) {
		if (count < 0) {
			cerr << strerror(errno) << endl;
			break;
		}
		cout << "read " << count << "bytes" << endl;
	}
	close(fd);
	return 0;
}
