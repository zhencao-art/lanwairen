#ifndef CEPH_CONTEXT_H
#define CEPH_CONTEXT_H

#include <boost/function.hpp>
#include <list>
#include <set>

/*
 * GenContext - abstract callback class
 */
template <typename T>
class GenContext {
  GenContext(const GenContext& other);
  const GenContext& operator=(const GenContext& other);

 protected:
  virtual void finish(T t) = 0;

 public:
  GenContext() {}
  virtual ~GenContext() {}       // we want a virtual destructor!!!
  virtual void complete(T t) {
    finish(t);
    delete this;
  }
};

/*
 * Context - abstract callback class
 */
class Context {
  Context(const Context& other);
  const Context& operator=(const Context& other);

 protected:
  virtual void finish(int r) = 0;

 public:
  Context() {}
  virtual ~Context() {}       // we want a virtual destructor!!!
  virtual void complete(int r) {
    finish(r);
    delete this;
  }
};

/**
 * Simple context holding a single object
 */
template<class T>
class ContainerContext : public Context {
  T obj;
public:
  ContainerContext(T &obj) : obj(obj) {}
  void finish(int r) {}
};

template <class T>
struct Wrapper : public Context {
  Context *to_run;
  T val;
  Wrapper(Context *to_run, T val) : to_run(to_run), val(val) {}
  void finish(int r) {
    if (to_run)
      to_run->complete(r);
  }
};
struct RunOnDelete {
  Context *to_run;
  RunOnDelete(Context *to_run) : to_run(to_run) {}
  ~RunOnDelete() {
    if (to_run)
      to_run->complete(0);
  }
};


class C_NoopContext : public Context {
public:
  void finish(int r) { }
};


struct C_Lock : public Context {
  Mutex *lock;
  Context *fin;
  C_Lock(Mutex *l, Context *c) : lock(l), fin(c) {}
  ~C_Lock() {
    delete fin;
  }
  void finish(int r) {
    if (fin) {
      lock->Lock();
      fin->complete(r);
      fin = NULL;
      lock->Unlock();
    }
  }
};

#endif
