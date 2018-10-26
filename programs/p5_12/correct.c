/* 
 * p6_6
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int ans;
  printf("1日の睡眠時間を整数値で入力してください\n");
  scanf("%d", &ans);
  if(ans == 8 || ans == 9){
    printf("健康的ですね\n");
  } else if(ans == 10){
    printf("ゆったり眠れていますね\n");
  } else{
    printf("規則正しい生活をしましょう\n");
  }

  return(0);
}
