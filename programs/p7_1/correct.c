/* 
 * p8_1
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int num, total;
  num = -1;
  total = 0;
  while (num != 0){
    printf("整数値を入力");
    scanf("%d", &num);
    total = total + num;
    printf("現合計: %d\n", total);
  }

  return(0);
}
