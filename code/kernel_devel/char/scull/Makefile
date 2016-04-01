KERNEL_TREE = /lib/modules/`uname -r`/build

scull-y := scull.o

obj-m = scull.o

modules:
	$(MAKE) -C $(KERNEL_TREE) M=`pwd` $@

clean:

