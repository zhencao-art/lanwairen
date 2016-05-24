#ifndef _HASH_TABLE_H_
#define _HASH_TABLE_H_

#define HASH(key,count) ((key)%(count))

struct hash_item_data {
};

struct hash_item {
    struct hash_item_data data;
    struct hash_item *next;
};

struct hash_slot {
    struct hash_item *root;
};

struct hash_table {
    struct hash_slot *slots;
    unsigned long count;
    unsigned long cur_count;
};

int hash_table_init(struct hash_table *table,unsigned long count);

#endif
