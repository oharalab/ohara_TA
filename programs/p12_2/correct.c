/* 
 * p13_2
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){
  char ss[80];
  printf("半角の文字列（空白なし）を入力してください\n");
  scanf("%[^\n]", ss);   //  gets(ss);
  puts(ss);

  return (0);
} 
