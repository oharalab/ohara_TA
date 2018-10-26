/* 
 * p5_4
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int x, y;
  printf("整数を入力してください：");
  scanf("%d", &x);
  if((y = x % 10) > 4){
    x = x - y + 10;
  }
  printf("一の位を5以上で切り上げた結果：%d\n", x);

  return 0;
}
