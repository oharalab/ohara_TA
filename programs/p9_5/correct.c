/* 
 * p10_5
 */

#include <stdio.h>

int main(){

  int i;
  double sum;
  for(i = 1, sum = 0.0; i <= 5; i++){
    printf("%d\n", i);
    sum += i;
  }
  printf("平均値：%.1f\n", sum / (i - 1));

  return 0;
}
