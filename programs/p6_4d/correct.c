/* 
 * p7_4d
 */

#include <stdio.h>

int main() {

  int i, j;
  printf("(i, j)=\n");
  for(i = 0; i < 5; i++){
    for(j =0; j < 5; j++){
      printf("(%2d, %2d) ", i, j);
    }
    printf("\n");
  }

  return(0);
}
