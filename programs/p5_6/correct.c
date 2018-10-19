/* 
 * p5_6
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int x;
  printf("成績を入力してください：");
  scanf("%d", &x);
  if((100 >= x) && (x >= 90)){
    printf("AA\n");
  }else if((90 > x) && (x >= 80)){
    printf("A\n");
  }else if((80 > x) && (x >= 70)){
    printf("B\n");
  }else if((70 > x) && (x >= 60)){
    printf("C\n");
  }else if((60 > x) && (x >= 0)){
    printf("不合格\n");
  }else {
    printf("入力が正しくありません\n");
  }

  return 0;
}
