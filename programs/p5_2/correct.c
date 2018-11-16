/*
 * p5_2
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int a;
  printf("整数を入力してください：");
  scanf("%d", &a);
  if(a > 10){
    printf("a > 10\n");
  } else {
    printf("a <= 10\n");
  }

  return 0;
}
