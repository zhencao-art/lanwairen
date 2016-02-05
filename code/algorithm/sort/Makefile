CC     = gcc
CFLAGS = -g

.PHONY:all
all:test

test:test.o quick.o
	$(CC) $^ -o $@

%.o:%.c
	$(CC) $(CFLAGS) -c $^ -o $@

.PHONY:clean
clean:
	rm -f *.o test
