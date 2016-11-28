#include <linux/errno.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/string.h>

struct foo_device {
	struct device dev;
	uint32_t id;
};


static struct foo_device* create_device(uint32_t id) {
	struct foo_device *foo_dev = kmalloc(sizeof(struct foo_device),GFP_KERNEL);

	if (!foo_dev) {
		return NULL;
	}

	foo_dev->id = id;

	return foo_dev;
}

// static unsigned int foo_char_major;
static struct class *foo_class;
static char *foo_name = "hello";


ssize_t name_show(struct class *class,struct class_attribute *attr,char *buf) {
	ssize_t len = strlen(foo_name);

	memcpy(buf,foo_name,len);
	buf[len] = '\n';

	return len + 1;
}

CLASS_ATTR_RO(name);

int __init foo_init(void)
{
	int result;

	foo_class = class_create(THIS_MODULE, "foo");
	if (IS_ERR(foo_class)) {
		result = PTR_ERR(foo_class);
		goto out;
	}
	printk("register class foo successfully");

	result = class_create_file(foo_class,&class_attr_name);

	return 0;

out:
	return result;
}

void foo_exit(void)
{
	class_destroy(foo_class);
}

MODULE_LICENSE("GPL");
MODULE_VERSION("1.0");
module_init(foo_init);
module_exit(foo_exit);
