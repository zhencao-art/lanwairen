PWD = `pwd`
KERNEL_TREE = /lib/modules/`uname -r`/build

obj-m = foo.o

modules:
	$(MAKE) -C $(KERNEL_TREE) M=$(PWD) modules

clean:
	$(MAKE) -C $(KERNEL_TREE) M=$(PWD) clean
