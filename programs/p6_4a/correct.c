/* 
 * p7_4a
 */

#include <stdio.h>

int main() {

  int i, total;

  for(i = 50, total = 0; i <= 100; i++){
    total += i;
  }
  printf("50から100までの数の総和：%d\n", total);

  return(0);
}
