/* 
 * p5_5
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int x;
  printf("成績を入力してください：");
  scanf("%d", &x);
  if(x >= 90){
    printf("AA\n");
  }else if(x >= 80){
    printf("A\n");
  }else if(x >= 70){
    printf("B\n");
  }else if(x >= 60){
    printf("C\n");
  }else{
    printf("来年頑張ってください\n");
  }

  return 0;
}
