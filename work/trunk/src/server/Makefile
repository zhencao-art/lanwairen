.PHONY:all
all:*_pb2.py

*_pb2.py:*.proto
	protoc $< --python_out=.

.PHONY:clean
clean:
	rm -f *_pb2.py *_pb2.pyc
