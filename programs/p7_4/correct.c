/* 
 * p8_4
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int num;
  double inch;
  inch = 2.54;
  while(1){
    printf("インチ: ");
    scanf("%d", &num);
    if(num == 0) break;
    printf("センチ: %.2f\n", num * inch);
  }
  printf("終了します\n");

  return(0);
}
