/* 
 * p10_3
 */

#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

int main(){

  int total, num, price;
  printf("単価と数量をカンマで区切って入力してください：");
  scanf("%d,%d", &price, &num);
  total = num * price;
  printf("単価と数量をカンマで区切って入力してください：");
  scanf("%d,%d", &price, &num);
  total += num * price;
  // total = total + num * price;
  printf("総売り上げ：%d円\n", total);

  return 0;
}
