/* 
 * p9_2
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int number, price[5];
  price[0] = 100; price[1] = 200; price[2] = 300; price[3] = 400; price[4] = 500;
  do
    {
      printf("値段を知りたい棚の番号を入力してください");
      printf("[1-5以外なら終了]\n");
      scanf("%d", &number);
      if((number > 0) && (number < 6)){
        printf("%d 番の棚は，%d 円です\n", number, price[number - 1]);
      }
    }while((number > 0) && (number < 6));

  return (0);
}