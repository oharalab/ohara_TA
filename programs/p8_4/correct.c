/* 
 * p9_4
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int i, height[5];
  for(i = 0; i < 5; i++){
    printf("%d番目の身長(cm)を入力してください：", i + 1);
    scanf("%d", &height[i]);
  }
  for(i = 0; i < 5; i++){
    printf("%d番目の身長：%dcm\n", i + 1, height[i]);
  }

  return (0);
}
