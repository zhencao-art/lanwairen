#include <errno.h>

#include "hashtable.h"

int hash_table_init(struct hash_table *table,unsigned long count) {
    struct hash_slot *slots = NULL;
    unsigned long index = 0;

    slots = (struct hash_slot*)alloc(sizeof(*slots) * count);
    if (!slots) {
        return ENOMEM;
    }
    
    table->slots = slots;
    table->count = count;

    for (index = 0;index < count;++index) {
        slots[index].root = NULL;
    }

    return 0;
}

int hash_table_insert(struct hash_table *table,unsigned long key,struct hash_item_data data) {
    unsigned long index = 0;
    struct hash_slot *slot = NULL;
    struct hash_item *item = NULL,**parent_next = NULL;

    if (!table->slots || !table->count) {
        return -1;
    }

    index = HASH(key,count);
    slot = &table->slots[index];

    if (slot->root) {
        //hit
        item = slot->root;
        while(item->next) {
            item = item->next;
        }
        parent_next = &item->next;
    } else {
        parent_next = &slot->root;
    }

    item = (struct hash_item*)alloc(sizeof(struct item));
    if (!item) {
        return ENOMEM;
    }
    item->data = data;
    item->next = NULL;

    parent_next = item;

    return 0;
}
