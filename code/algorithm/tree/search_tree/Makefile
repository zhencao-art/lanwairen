CC     = gcc
CFLAGS = -g

.PHONY:all
all:test

OBJS = test.o setree.o

test:$(OBJS)
	$(CC) $^ -o $@

%.o:%.c
	$(CC) $(CFLAGS) -c $^ -o $@

.PHONY:clean
clean:
	rm -f *.o test
