/* 
 * p7_3
 */

#include <stdio.h>

int main() {

  int i;
  for(i = 1; i <= 100; i++){
    printf("%5d", i);
    if((i % 5) == 0) printf("\n");
  }

  return(0);
}
