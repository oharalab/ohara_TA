/* 
 * p9_5
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int point[3][4];
  int total[3];
  int loop, loop2;

  for(loop = 0; loop < 4; loop++){
    for(loop2 = 0;loop2 < 3; loop2++){
      switch(loop2){
      case 0: printf("A君"); break;
      case 1: printf("B君"); break;
      case 2: printf("C君"); break;
      }
      printf("のゲーム%dの得点を入力してください\n", loop + 1);
      scanf("%d", &point[loop2][loop]);
    }
  }

  for(loop2 = 0; loop2 < 3; loop2++){
    total[loop2] = 0;
    for(loop = 0; loop < 4; loop++){
      total[loop2] = total[loop2] + point[loop2][loop];
    }
  }

  for(loop2 = 0; loop2 < 3; loop2++){
    for(loop = 0; loop < 4; loop++){
      printf("%4d|", point[loop2][loop]);
    }
    printf("%4d|\n", total[loop2]);
  }

  return 0;
}
