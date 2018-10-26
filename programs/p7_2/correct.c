/* 
 * p8_2
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int num;
  double inch;
  inch = 2.54;
  num = -1;
  while(num != 0){
    printf("インチ: ");
    scanf("%d", &num);
    printf("センチ: %.2f\n", num * inch);
  }
  printf("終了します\n");

  return(0);
}
