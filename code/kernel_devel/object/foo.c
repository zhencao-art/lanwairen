#include <linux/errno.h>
#include <linux/slab.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/kobject.h>
#include <linux/sysfs.h>
#include <linux/string.h>

struct foo_object {
	struct kobject object;
	uint32_t id;
};

struct foo_attribute {
	struct attribute attr;
	ssize_t (*show)(struct kobject *obj,char *buff);
	ssize_t (*store)(struct kobject *obj,char *buff,ssize_t size);
};

struct kobj_type foo_kobj_type = {
};

static struct foo_object *create_foo_obj(uint32_t id) {
	int ret = 0;

	struct foo_object *obj = kmalloc(GFP_KERNEL,sizeof(struct foo_object));
	
	if (NULL == obj) {
		return NULL;
	}

	kobject_init(&obj->object,&foo_kobj_type);

	ret = kobject_add(&obj->object,NULL,"foo-%d",id);
	if (ret) {
		goto free;
	}

	obj->id = id;

	return obj;

free:
	kfree(obj);
	return NULL;
}

static void free_foo_obj(struct foo_object *obj) {
	if (obj) {
		kobject_del(&obj->object);
		kfree(obj);
	}
}


static int add_foo_attr(struct foo_object *obj,struct foo_attribute *attr) {
	int ret = 0;

	if (attr && obj) {
		ret = sysfs_create_file(&obj->object,&attr->attr);
	} else {
		ret = -EINVAL;
	}

	return ret;
}

static int remove_foo_attr(struct foo_object *obj,struct foo_attribute *attr) {
	int ret = 0;

	if (attr && obj) {
		sysfs_remove_file(&obj->object,&attr->attr);
	} else {
		ret = -EINVAL;
	}

	return ret;
}

static ssize_t id_show(struct kobject *obj,char *buff) {
	struct foo_object *foo_obj = container_of(obj,struct foo_object,object);

	sprintf(buff,"id = %d\n",foo_obj->id);

	return 0;
}

static ssize_t id_store(struct kobject *obj,char *buff,ssize_t size) {
	struct foo_object *foo_obj = container_of(obj,struct foo_object,object);
	uint32_t i_id;

	kstrtouint(buff,0,&i_id);

	foo_obj->id =  i_id;

	return 0;
}

static struct foo_attribute id = {
	.attr  = {.name = "id",.mode=0644},
	.show  = id_show,
	.store = id_store,
};


int __init foo_init(void)
{
	return 0;
}

void foo_exit(void)
{
}

MODULE_LICENSE("GPL");
MODULE_VERSION("1.0");
module_init(foo_init);
module_exit(foo_exit);
