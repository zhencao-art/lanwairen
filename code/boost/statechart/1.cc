#include <boost/statechart/state_machine.hpp>
#include <boost/statechart/simple_state.hpp>

#include <iostream>

class Greenting;

class MyMachine : boost::statechart::state_machine<MyMachine,Greeting> {
public:
};

class Greeting : boost::statechart::simple_state<Greeting,MyMachine> {
public:
	Greeting() {
		std::cout <<"enter Greeting"<<std::endl;
	}
	~Greeting() {
		std::cout <<"enter Greeting"<<std::endl;
	}
};


int main(int argc,char **argv)
{
	MyMachine machine;

	machine.initiate();

	return 0;
}
