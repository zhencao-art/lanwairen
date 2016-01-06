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
            fprintf(stderr, "%s: cannot read config file: %s\n", argv[0], strerror(-err));
            exit(EXIT_FAILURE);
    } else {
            printf("\nRead the config file.\n");
    }

    /* Read command line arguments */
    err = rados_conf_parse_argv(cluster, argc, argv);
    if (err < 0) {
            fprintf(stderr, "%s: cannot parse command line arguments: %s\n", argv[0], strerror(-err));
            exit(EXIT_FAILURE);
    } else {
            printf("\nRead the command line arguments.\n");
    }

    /* Connect to the cluster */
    err = rados_connect(cluster);
    if (err < 0) {
            fprintf(stderr, "%s: cannot connect to cluster: %s\n", argv[0], strerror(-err));
            exit(EXIT_FAILURE);
    } else {
            printf("\nConnected to the cluster.\n");
    }	

	err = rados_ioctx_create(cluster, pool_name, &io);
	if (err < 0) {
	        fprintf(stderr, "%s: cannot open rados pool %s: %s\n", argv[0], pool_name, strerror(-err));
			goto shutdown;
	} else {
	        printf("\nCreated I/O context.\n");
	}
	
	/* Write data to the cluster synchronously. */
	err = rados_write(io, "hw", "Hello World!", 12, 0);
	if (err < 0) {
	        fprintf(stderr, "%s: Cannot write object \"hw\" to pool %s: %s\n", argv[0], pool_name, strerror(-err));
			goto ioctx_destroy;
	} else {
	        printf("\nWrote \"Hello World\" to object \"hw\".\n");
	}

	err = rados_write(io, "hw_1", "Hello World!_1", 13, 0);
	if (err < 0) {
	        fprintf(stderr, "%s: Cannot write object \"hw\" to pool %s: %s\n", argv[0], pool_name, strerror(-err));
			goto ioctx_destroy;
	} else {
	        printf("\nWrote \"Hello World\" to object \"hw\".\n");
	}

	

ioctx_destroy:	
	rados_ioctx_destroy(io);
shutdown:
	rados_shutdown(cluster);
	return EXIT_SUCCESS;
}
