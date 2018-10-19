/* 
 * p13_3
 */

#include<stdio.h>

int main(){

  char input[81];
  int loop;
  for(loop=0; loop<81; loop++){
    input[loop]='\0'; /* 文字型配列の初期化 */
  }
  scanf("%[^\n]", input);   //  gets(input);
  loop = 0;
  while((input[loop] != '\0') && (loop < 81 )) /* 長くても配列サイズまで */
    {
      if(( input[loop] >= 'a' ) && ( input[loop] <= 'z' )) {/* 英小文字の判定 */
        printf("%c", (char)((int)input[loop]-32));
      }
      else{
        printf("%c", input[loop]);
      }
      loop++;
    }
  printf("\n");

  return(0);
}
