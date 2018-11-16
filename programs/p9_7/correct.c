/* 
 * p10_7
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main() {

  int i, v1[4], v2[4], dot;
  printf("4つの整数値をカンマで区切って入力してください（1つ目）：");
  scanf("%d,%d,%d,%d", &v1[0], &v1[1], &v1[2], &v1[3]);
  printf("4つの整数値をカンマで区切って入力してください（2つ目）：");
  scanf("%d,%d,%d,%d", &v2[0], &v2[1], &v2[2], &v2[3]);
  for (i = 0, dot = 0; i < 4; i++)
    dot += v1[i] * v2[i];
  printf("2つのベクトルの内積：%d\n", dot);

  return(0);
}
