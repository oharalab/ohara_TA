/* 
 * p12_4
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  char input;
  printf("半角文字を1文字入力してください\n") ;
  scanf("%c", &input);
  printf("入力された文字[%c][%d]\n", input, (int)input) ;

  return(0);
}
