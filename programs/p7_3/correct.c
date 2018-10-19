/* 
 * p8_3
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int num, total;
  total = 0;
  do{
    printf("整数値を入力\n");
    scanf("%d", &num);
    total = total + num;
    printf("現合計: %d\n", total);
  }while(num != 0);

  return(0);
}
