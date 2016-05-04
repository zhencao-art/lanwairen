#include <iostream>

#include <boost/statechart/state_machine.hpp>
#include <boost/statechart/simple_state.hpp>
#include <boost/statechart/event.hpp>

using namespace std;

namespace sc = boost::statechart;

struct EvStartStop : sc::event< EvStartStop > {};
struct EvReset : sc::event< EvReset > {};

struct Active;
struct StopWatch : sc::state_machine< StopWatch,Active > {};

struct Stopped;
struct Active : sc::simple_state< Active,StopWatch,Stopped > {};

struct Running : sc::simple_state< Running,Active > {};
struct Stopped : sc::simple_state< Stopped,Active > {};

int main(int argc,char **argv)
{
    StopWatch mywatch;

    mywatch.initiate();

    return 0;
}
