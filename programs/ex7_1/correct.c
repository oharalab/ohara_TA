/* 
 * p8_2
 */

#include <stdio.h>

int main(){

  int num;
  double inch;
  inch = 2.54;
  do {
    printf("インチ: ");
    scanf("%d", &num);
    printf("センチ: %.2f\n", num * inch);
  } while (num != 0);
  printf("終了します\n");

  return(0);
}
