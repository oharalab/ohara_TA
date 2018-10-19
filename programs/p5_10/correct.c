/* 
 * p6_4
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main() {

  int ans1, ans2;
  int total;

  printf("一日の平均睡眠時間は?\n");
  printf("1: 6時間以下 2: 6～時間 3: 8～時間 4: 10時間以上\n");
  scanf("%d", &ans1);
  printf("就寝時間は何時?\n");
  printf("1: 22時以前 2: 22～時 3: 24～時間 4: 26時以降\n");
  scanf("%d", &ans2);

  switch(ans1) {
  case 1: total = 20;
    break;
  case 2: total = 30;
    break;
  case 3: total = 60;
    break;
  default: total = 40;
    break;
  }

  switch(ans2) {
  case 1: total = total + 30; // total += 30 でもよい
    break;
  case 2: total = total + 40;
    break;
  case 3: total = total + 20;
    break;
  default: total = total + 10;
    break;
  }
  printf("あなたの健康生活度は%d点です\n", total);

  return(0);
}
