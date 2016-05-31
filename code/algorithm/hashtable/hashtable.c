#include <errno.h>
#include <stdlib.h>

#include "hashtable.h"

int hash_table_init(struct hash_table *table,unsigned long count) {
    struct hash_slot *slots = NULL;
    unsigned long index = 0;

    slots = (struct hash_slot*)malloc(sizeof(*slots) * count);
    if (!slots) {
        return ENOMEM;
    }
    
    table->slots = slots;
    table->count = count;
    table->cur_count = 0;

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

    index = HASH(key,table->count);
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

    item = (struct hash_item*)malloc(sizeof(struct hash_item));
    if (!item) {
        return ENOMEM;
    }
    item->data = data;
    item->next = NULL;

    *parent_next = item;

    table->cur_count++;

    return 0;
}



int main(int argc,char **argv)
{
    struct hash_table table;
    struct hash_item_data data_1 = {999};
    struct hash_item_data data_2 = {7777};

    hash_table_init(&table,10);

    hash_table_insert(&table,7,data_1);
    hash_table_insert(&table,17,data_2);

    return 0;
}
