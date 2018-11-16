/* 
 * p12_5
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  char input;
  input = '\0';
  printf("半角文字を1文字入力してください\n") ;
  scanf("%c", &input);
  if( ( input >= 'a' ) && ( input <= 'z' ) ) {
    printf("小文字英字です\n");
  }
  else{
    if( ( input >= (char) 65 ) && ( input <= (char) 90 ) ) {
      printf("大文字英字です\n");
    }else{
      printf("英字以外の文字です\n");
    }
  }

  return(0);
} 
