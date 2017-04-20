#include <event2/event.h>
#include <event2/thread.h>
#include <unistd.h>
#include <stdio.h>

void timer_cb(int fd, short event, void *arg)
{
    printf("%d %d %lx\n",fd,event,(long unsigned int)arg);
}

int main()
{
    evthread_use_pthreads();

    struct event_base *base = event_base_new();

    // evthread_set_lock_callbacks(NULL);

   // struct timeval tv;
   // tv.tv_sec = 5;
   // tv.tv_usec = 0;

   // struct event *timer_event = evtimer_new(base,timer_cb,base);
   // evtimer_add(timer_event,&tv);
//    struct event *ev = event_new(base,-1,0,timer_cb,base);
//    event_add(ev,NULL);
    event_base_once(base,-1,EV_TIMEOUT,timer_cb,NULL,NULL);

    event_base_dispatch(base);

    return 0;
}
