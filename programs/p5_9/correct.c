/* 
 * p6_3
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main() {

  int ans1;
  printf("一日の平均睡眠時間は?\n");
  printf("1: 6時間以下 2: 6～時間 3: 8～時間 4: 10時間以上\n");
  scanf("%d", &ans1);
  switch(ans1) {
  case 1: printf("20点です\n");
    break;
  case 2: printf("30点です\n");
    break;
  case 3: printf("60点です\n");
    break;
  case 4: printf("40点です\n");
    break;
  default: printf("入力が間違いです\n");
  }

  return(0);
}
