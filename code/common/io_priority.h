#ifndef COMMON_IO_PRIORITY_H
#define COMMON_IO_PRIORITY_H

#include <string>

#ifndef IOPRIO_WHO_PROCESS
# define IOPRIO_WHO_PROCESS 1
#endif
#ifndef IOPRIO_PRIO_VALUE
# define IOPRIO_CLASS_SHIFT 13
# define IOPRIO_PRIO_VALUE(class, data) \
		(((class) << IOPRIO_CLASS_SHIFT) | (data))
#endif
#ifndef IOPRIO_CLASS_RT
# define IOPRIO_CLASS_RT 1
#endif
#ifndef IOPRIO_CLASS_BE
# define IOPRIO_CLASS_BE 2
#endif
#ifndef IOPRIO_CLASS_IDLE
# define IOPRIO_CLASS_IDLE 3
#endif

extern pid_t gettid();

extern int ioprio_set(int which, pid_t who, int ioprio);

extern int ioprio_string_to_class(const std::string& s);

#endif
