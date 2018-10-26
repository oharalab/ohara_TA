/* 
 * p15_1
 */

#include<stdio.h>

int ruijyo(int a, int b);

int main(){

  int n;
  n = ruijyo(2, 3);
  printf("%d\n", n);
  printf("%d\n", ruijyo(3, 4));

  return (0);
}

int ruijyo(int a, int b){
  int n, ans;
  ans = 1;
  for(n = 1; n <= b; n++){
    ans = ans * a;
  }

  return ans;
}
