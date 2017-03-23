#include <list>
#include <string>

using namespace std;

class Observer;

class Topic {
public:
	explicit Topic(const string &name) : m_name(name) {}
	void register_observer(Observer *observer) {
		m_observers.push_back(observer);
	}
	void unregister_observer(Observer *observer) {
	}
	string m_name;
	list<Observer*> m_observers;
};

class Observer {
public:
	Observer(Topic *topic,const string &name) : m_topic(topic),m_name(name) {
		m_topic->register_observer(this);
	}
	~Observer() {
		m_topic->unregister_observer(this);
	}
	string m_name;
	Topic *m_topic;
};

class XXObserver : public Observer {
public:
	XXObserver(Topic *topic,const string &name) : Observer(topic,name) {}
};

extern Topic g_topic;

XXObserver g_obs(&g_topic,"my_observer");
Topic g_topic("my_topic");

int main(int argc,char **argv) {
	return 0;
}
