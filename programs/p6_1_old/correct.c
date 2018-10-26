/* 
 * p6_1
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main() {

  int num;
  printf("整数値を入力してください: ");
  scanf("%d", &num);
  if(num % 2 == 0){
    printf("%dは偶数です\n", num);
  } else {
    printf("%dは奇数です\n", num);
  }

  return(0);
}
