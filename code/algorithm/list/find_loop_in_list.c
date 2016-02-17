
/**
 * if ret == 0,it has loop
 */
int check_loop_list(struct list_node *head) {
	struct list_node *i,*j;

	if (!head) {
		return -1;
	}

	i = head;
	j = head->next;

	while(!i && !j) {
		i = i->next;
		j = j->next->next;

		if (i == j) {
			return 0;
		}
	}

	return -1;
}
