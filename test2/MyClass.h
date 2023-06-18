
#include <stdio.h>

namespace myns {

class Foo {
  int i;
public:
  int getVal() { return i; }
  void setVal(int v) { i  = v;}
};

class Bar : public Foo {
public:
  Bar(long val) { setVal(val); }
  void doSomething() { printf("%d\n", getVal()); }

  static void staticFunc() {
    printf("staticFunc\n");
  }
};

}

void globalFunc() {
  printf("globalFunc\n");
}
