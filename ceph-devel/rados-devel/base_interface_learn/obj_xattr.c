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

	//set the xattr of the object

	err = rados_setxattr(io,"hw","xatrr_1","xattr_1_val",strlen("xattr_1_val"));	
	err = rados_setxattr(io,"hw","xatrr_2","xattr_2_val",strlen("xattr_2_val"));	
	err = rados_setxattr(io,"hw","xatrr_3","xattr_3_val",strlen("xattr_3_val"));	
	if (err < 0) {
		fprintf(stderr,"set xattr error %s\n",strerror(-err));
		goto obj_remove;
	}

	//get the all xattrs of the object	
	rados_xattrs_iter_t xattr_iter;
	const char *xattr_name = NULL;
	const char *xattr_value = NULL;
	size_t xattr_len = 0;

	err = rados_getxattrs(io,"hw",&xattr_iter);
	if (err < 0) {
	    fprintf(stderr, "%s: Cannot get attrs of the object \"hw\" to pool %s: %s\n",
			argv[0], pool_name, strerror(-err));
		goto obj_remove;
	}

	while (1) {
		err = rados_getxattrs_next(xattr_iter,&xattr_name,&xattr_value,&xattr_len);
		if (err < 0) {
			fprintf(stderr,"rados_getxattrs_next error,%s\n",strerror(-err));	
			break;
		}
		
		if (!xattr_name && !xattr_value && !xattr_len) {
			printf("obj %s did not found xattrs\n","hw");		
			break;
		}

		printf("xattr %s = %s value_len %d\n",xattr_name,xattr_value,xattr_len);
	}
	rados_getxattrs_end(xattr_iter);

	//remove the object
obj_remove:
	err = rados_remove(io,"hw");
	if (err < 0) {
		fprintf(stderr,"can not remove the obj %s,%s\n","hw",strerror(-err));	
	}

ioctx_destroy:	
	rados_ioctx_destroy(io);
shutdown:
	rados_shutdown(cluster);
	return EXIT_SUCCESS;
}
