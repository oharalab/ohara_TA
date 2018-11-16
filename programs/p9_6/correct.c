/* 
 * p10_6
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int i, num;
  double total;
  while(1){
    printf("正の整数値を入力してください：");
    scanf("%d", &num);
    if(num == 0) break;
    for(i = 1, total = 0.0; i <= num; i++){
      total += i;
    }
    printf("総和：%.0f 平均：%.1f\n", total, total / num);
  }
  printf("終了\n");

  return 0;
}
