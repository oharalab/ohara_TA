/* 
 * p9_3
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int i, height1, height2, height3, height4, height5;
  printf("1番目の身長(cm)を入力してください：");
  scanf("%d", &height1);
  printf("2番目の身長(cm)を入力してください：");
  scanf("%d", &height2);
  printf("3番目の身長(cm)を入力してください：");
  scanf("%d", &height3);
  printf("4番目の身長(cm)を入力してください：");
  scanf("%d", &height4);
  printf("5番目の身長(cm)を入力してください：");
  scanf("%d", &height5);
  printf("1番目の身長：%dcm\n", height1);
  printf("2番目の身長：%dcm\n", height2);
  printf("3番目の身長：%dcm\n", height3);
  printf("4番目の身長：%dcm\n", height4);
  printf("5番目の身長：%dcm\n", height5);

  return (0);
}
