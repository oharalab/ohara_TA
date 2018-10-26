/*
 * p4_5
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main() {

  int num1, num2;
  printf("カンマで区切って2つの整数を入力してください：");
  scanf("%d,%d", &num1, &num2);
  printf("1番目の数：%d\n", num1);
  printf("2番目の数：%d\n", num2);

  return 0;
}
