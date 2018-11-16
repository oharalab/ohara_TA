/* 
 * p7_5
 */

#include <stdio.h>

int main(){

  int i, x;
  for ( i = 0, x = 10; ; i++ ) {
    if(x < 10000){
      printf("10の%d乗: %d\n", i+1, x);
    }else{
      break;
    }
    x *= 10;
  }

  return(0);
}
