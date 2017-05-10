#include <unistd.h>
#include <sys/syscall.h>   /* For SYS_xxx definitions */
#include <errno.h>
#include <algorithm>

#include "io_priority.h"

pid_t gettid() {
  return syscall(SYS_gettid);
}

int ioprio_set(int which, pid_t who, int ioprio)
{
  return syscall(SYS_ioprio_set, which, who, ioprio);
}

int ioprio_string_to_class(const std::string& s)
{
  std::string l = s;
  std::transform(l.begin(), l.end(), l.begin(), ::tolower);

  if (l == "idle")
    return IOPRIO_CLASS_IDLE;
  if (l == "be" || l == "besteffort" || l == "best effort")
    return IOPRIO_CLASS_BE;
  if (l == "rt" || l == "realtime" || l == "real time")
    return IOPRIO_CLASS_RT;
  return -EINVAL;
}
