/* 
 * p15_3
 */

#include <stdio.h>

void func(void);
int glb;

int main() {

  int loc;
  glb = 1000;
  loc = 2222;
  printf("main glb = %d\n", glb);
  printf("main loc = %d\n", loc);
  func();

  return (0);
}

void func(void){

  int loc;
  loc = 9999;
  printf("func glb = %d\n", glb);
  printf("func loc = %d\n", loc);

}
