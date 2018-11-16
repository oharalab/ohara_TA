/* 
 * p6_5
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int ans;
  printf("1日の睡眠時間を整数値で入力してください\n");
  scanf("%d", &ans);
  switch(ans){
  case 8:
  case 9: printf("健康的ですね\n");
    break;
  case 10: printf("ゆったり眠れていますね\n");
    break;
  default: printf("規則正しい生活をしましょう\n");
  }

  return(0);
}
