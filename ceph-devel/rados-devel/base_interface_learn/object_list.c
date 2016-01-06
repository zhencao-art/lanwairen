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
	rados_list_ctx_t list_ctx;
	uint32_t hash_position;
	
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
	
	err = rados_nobjects_list_open(io,&list_ctx);
	if (err < 0) {
		fprintf(stderr,"%s: can not open list ctx %s\n",argv[0],strerror(-err));
		goto ioctx_destroy;
	} else {
		printf("Open list\n");
	}

	hash_position = rados_nobjects_list_get_pg_hash_position(list_ctx);

	printf("hash_position = %u\n",hash_position);

	const char * entry = NULL;
	uint32_t obj_index = 0;
	
	while(1) {
		err = rados_nobjects_list_next(list_ctx,&entry,NULL,NULL);

		if (err == -ENOENT) {
			fprintf(stderr,"no more objects to list\n");
			break;
		}
		
		if (err < 0) {
			fprintf(stderr,"objects_list error,%s\n",strerror(-err));
			break;
		}

		printf("entry obj_%d = %s\n",obj_index++,entry);	
	}

list_ctx_close:	
	rados_nobjects_list_close(list_ctx);
ioctx_destroy:	
	rados_ioctx_destroy(io);
shutdown:
	rados_shutdown(cluster);

	return EXIT_SUCCESS;
}
