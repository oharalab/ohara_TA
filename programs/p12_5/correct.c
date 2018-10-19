/* 
 * p13_5
 */

#include <stdio.h>
#include <string.h>

int main(){

  char input[10];
  printf("Yes と入力してください: ");
  scanf("%[^\n]", input); //gets(input);
  if(strcmp(input, "Yes") == 0){
    printf("Yesが入力されました\n");
  }else{
    printf("入力が間違っています\n");
  }

  return (0);
}
