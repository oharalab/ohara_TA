/* 
 * p7_2
 */

#include <stdio.h>

int main(){

  int i;
  double inch;
  inch = 2.54;
  for ( i = 1; i <= 5; i++ ) {
    printf("%d inch: %.2f\n", i, i * inch);
  }

  return(0);
}
