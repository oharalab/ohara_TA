/* 
 * p7_4c
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main() {

  int i, num, ans;
  printf("正の整数値を入力してください：");
  scanf("%d", &num);
  for(i = ans = 1; i <= num; i++){
    ans *= i;
  }
  printf("%d!=%d\n", num, ans);

  return(0);
}
