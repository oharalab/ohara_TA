/* 
 * p9_1
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main(){

  int number, price1, price2, price3, price4, price5;
  price1 = 100; price2 = 200; price3 = 300; price4 = 400; price5 = 500;
  do
    {
      printf("値段を知りたい棚の番号を入力してください");
      printf("[1-5以外なら終了]\n");
      scanf("%d", &number);
      switch(number)
        {
        case 1: printf("%d 番の棚は，%d 円です\n", number, price1); break;
        case 2: printf("%d 番の棚は，%d 円です\n", number, price2); break;
        case 3: printf("%d 番の棚は，%d 円です\n", number, price3); break;
        case 4: printf("%d 番の棚は，%d 円です\n", number, price4); break;
        case 5: printf("%d 番の棚は，%d 円です\n", number, price5); break;
        }
    }while((number > 0) && (number < 6));

  return (0);
}
