#include <iostream>
#include <string>
#include <map>
#include <leveldb/db.h>

using namespace std;

static const char *db_path = "/tmp/testdb";
static leveldb::DB *db;

static map<string,string> data;

int main(int argc,char **argv)
{
	leveldb::Options options;
	leveldb::Status status;
	int ret = 0;

	options.create_if_missing = true;

	status = leveldb::DB::Open(options,db_path,&db);
	if (!status.ok()) {
		cerr << status.ToString() << endl;	
		return -1;
	}

	// init data
	data.insert(pair<string,string>("key1","value1"));
	data.insert(pair<string,string>("key2","value2"));
	data.insert(pair<string,string>("key3","value3"));
	data.insert(pair<string,string>("key4","value4"));


	for (map<string,string>::iterator i = data.begin();
			i != data.end();++i) {
		db->Put(leveldb::WriteOptions(),i->first,i->second);
	}

	delete db;
	db = NULL;

	return ret;
}
