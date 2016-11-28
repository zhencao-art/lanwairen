#include <iostream>
#include <chrono>
#include <ctime>

#include <boost/statechart/state_machine.hpp>
#include <boost/statechart/simple_state.hpp>
#include <boost/statechart/event.hpp>
#include <boost/statechart/transition.hpp>

using namespace std;
using namespace std::chrono;
using std::chrono::system_clock;

namespace sc = boost::statechart;

struct EvStartStop : sc::event< EvStartStop > {};
struct EvReset : sc::event< EvReset > {};

struct Active;
struct StopWatch : sc::state_machine< StopWatch,Active > {};

struct Stopped;
struct Active : sc::simple_state< Active,StopWatch,Stopped > {
	typedef sc::transition<EvReset,Stopped> reactions;

	Active() {
		cout << "Active" << endl;
		m_elapsed_time = system_clock::time_point();
	}
	~Active() {
		cout << "~Active" << endl;
	}

	system_clock::time_point elapsed_time() const {
		return m_elapsed_time;
	}

	system_clock::time_point& elapsed_time() {
		return m_elapsed_time;
	}

	private:
	system_clock::time_point m_elapsed_time;
};

struct Running : sc::simple_state< Running,Active > {
	typedef sc::transition<EvStartStop,Stopped> reactions;

	Running() {
		cout << "Running" << endl;
		start_time = system_clock::now();
	}
	~Running() {
		cout << "~Running" << endl;
		system_clock::time_point end_time = system_clock::now();
		context<Active>().elapsed_time() += end_time - start_time;
	}

	private:
	system_clock::time_point start_time;
};

struct Stopped : sc::simple_state< Stopped,Active > {
	typedef sc::transition<EvStartStop,Running> reactions;

	Stopped() {
		cout << "Stopped" << endl;	
	}
	
	~Stopped() {
		cout << "~Stopped" << endl;	
	}
};

int main(int argc,char **argv)
{
    StopWatch mywatch;

    mywatch.initiate();

		mywatch.process_event(EvStartStop());
	
		sleep(5);

		mywatch.process_event(EvStartStop());

    return 0;
}
