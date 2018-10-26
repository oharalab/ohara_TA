/* 
 * p13_4
 */

#include <stdio.h>
#include <string.h>

int main(){

  char moji[21];
  char moji2[30];
  printf("20 文字以内の半角英数字（空白含む）を入力してください:");
  scanf("%[^\n]", moji);   //gets(moji);
  strcpy(moji2, moji);
  puts(moji2);

  return(0);
}
