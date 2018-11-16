/* 
 * ex5_2
 */

#include <stdio.h>

int main() {

  int price;

  printf("定価=");
  scanf("%d", &price);

  if (price >= 10000) {
    printf("代金=%d\n", price - 1000);

  } else if (price >= 5000){
    printf("代金=%d\n", price - 500);    

  } else {
    printf("代金=%d\n", price);        
  }

  return 0;
}
