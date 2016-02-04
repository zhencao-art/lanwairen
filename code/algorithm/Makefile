CC     = gcc
CFLAGS = -g

0_1:test_0_1.o alg_0_1.o
	$(CC) $^ -o $@

%.o:%.c
	$(CC) $(CFLAGS) -c $^ -o $@

.PHONY:clean
clean:
	rm -f *.o 0_1
