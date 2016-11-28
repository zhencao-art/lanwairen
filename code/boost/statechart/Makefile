LDFLAGS  =
CXXFLAGS = -g -Werror --std=c++11

2:2.o
	$(CXX) $(LDFLAGS) -o $@ $^

%.o:%.cc
	$(CXX) $(CXXFLAGS) -c -o $@ $^

.PHONY:
clean:
	rm -f *.o 2
