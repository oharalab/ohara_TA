/* 
 * p13_6
 */

#include <stdio.h>
#include <string.h>

int main(){

  char input1[10], input2[10];
  printf("1つ目の文字列を入力: ");
  scanf("%[^\n]", input1); getchar();  //gets(input1);
  printf("2つ目の文字列を入力: ");
  scanf("%[^\n]", input2); getchar();  //gets(input2);
  if((strlen(input1) + strlen(input2)) < 10){
    strcat(input1, input2);
    printf("%s\n", input1);
  }
  else{
    printf("入力した文字列が長くて連結できません\n");
  }

  return(0);
}
