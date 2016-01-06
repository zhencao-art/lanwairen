#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <rados/librados.h>

//cluster
static rados_t cluster;
static const char *cluster_name = "ceph";
static const char *user_name = "client.admin";
static uint64_t flags = 0;

//read write
static const char *pool_name = "rbd";
static rados_ioctx_t io;

#define BUF_SIZE 512
static char buf[BUF_SIZE];

int main(int argc,const char **argv)
{
	int err = EXIT_SUCCESS;
	
	err = rados_create2(&cluster,cluster_name,user_name,flags);
	if (err < 0) {
		fprintf(stderr,"Couldn't create the cluster handle %s\n",strerror(-err));	
		exit(EXIT_FAILURE);
	}

	 /* Read a Ceph configuration file to configure the cluster handle. */
    err = rados_conf_read_file(cluster, "/etc/ceph/ceph.conf");
    if (err < 0) {
            fprintf(stderr, "%s: cannot read config file: %s\n", argv[0], 
					strerror(-err));
            exit(EXIT_FAILURE);
    } else {
            printf("\nRead the config file.\n");
    }

    /* Read command line arguments */
    err = rados_conf_parse_argv(cluster, argc, argv);
    if (err < 0) {
            fprintf(stderr, "%s: cannot parse command line arguments: %s\n",
					argv[0], strerror(-err));
            exit(EXIT_FAILURE);
    } else {
            printf("\nRead the command line arguments.\n");
    }

    /* Connect to the cluster */
    err = rados_connect(cluster);
    if (err < 0) {
            fprintf(stderr, "%s: cannot connect to cluster: %s\n", argv[0],
					strerror(-err));
            exit(EXIT_FAILURE);
    } else {
            printf("\nConnected to the cluster.\n");
    }	

	err = rados_ioctx_create(cluster, pool_name, &io);
	if (err < 0) {
	        fprintf(stderr, "%s: cannot open rados pool %s: %s\n", argv[0],
					pool_name, strerror(-err));
			goto shutdown;
	} else {
	        printf("\nCreated I/O context.\n");
	}
	
	const char *write_buf = "hw: Hello World!";
	
	/* Write data to the cluster synchronously. */
	err = rados_write(io, "hw", write_buf, strlen(write_buf), 0);
	if (err < 0) {
	        fprintf(stderr, "%s: Cannot write object \"hw\" to pool %s: %s\n",
				argv[0], pool_name, strerror(-err));
			goto ioctx_destroy;
	} else {
	        printf("\nWrote \"%s\" to object \"hw\".\n",write_buf);
	}

	memset(buf,BUF_SIZE,0);
	err = rados_read(io,"hw",buf,BUF_SIZE,0);
	if (err < 0) {
		fprintf(stderr,"read obj %s error,%s\n","hw",strerror(-err));
	} else {
		printf("read obj %s suuccess,its content is \n\t\t%s\n","hw",buf);
	}


	write_buf = "hw_1: Hello World!";

	err = rados_write(io, "hw_1", write_buf ,strlen(write_buf), 0);
	if (err < 0) {
	        fprintf(stderr, "%s: Cannot write object \"hw\" to pool %s: %s\n",
				argv[0], pool_name, strerror(-err));
			goto ioctx_destroy;
	} else {
	        printf("\nWrote \"%s\" to object \"hw_1\".\n",write_buf);
	}

	memset(buf,BUF_SIZE,0);
	err = rados_read(io,"hw_1",buf,BUF_SIZE,0);
	if (err < 0) {
		fprintf(stderr,"read obj %s error,%s\n","hw",strerror(-err));
	} else {
		printf("read obj %s suuccess,its content is \n\t\t%s\n","hw",buf);
	}
	

	err = rados_remove(io,"hw");
	if (err < 0) {
		fprintf(stderr,"can not remove the obj %s,%s\n","hw",strerror(-err));	
	}

	err = rados_remove(io,"hw_1");
	if (err < 0) {
		fprintf(stderr,"can not remove the obj %s,%s\n","hw_1",strerror(-err));	
	}

ioctx_destroy:	
	rados_ioctx_destroy(io);
shutdown:
	rados_shutdown(cluster);
	return EXIT_SUCCESS;
}
