/* 
 * p10_4
 */

#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main(){

  int a, b, diff;
  printf("2つの聖数値を空白で区切って入力してください：");
  scanf("%d %d", &a, &b);
  if((diff = a - b) < 0) diff = -diff;
  printf("%d と %d の差分：%d\n", a, b, diff);

  return 0;
}
