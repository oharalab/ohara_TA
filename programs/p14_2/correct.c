/* 
 * p15_2
 */

#include <stdio.h>

void putd(int a);

int main(){

  int dt = 500;
  putd(100);
  putd(dt);

  return (0);
}

void putd(int a){

  printf("%d\n", a);

}
