#include <stdio.h>

int main(){
  int n;
  float ave=0, num;

  n = 0;

  for (n=1; n<=4; n++) {
    printf("%dつ目の数値を入力してください：", n);
    scanf("%f", &num);
    ave += num;
  }

  n--;
  printf("%dつの値の平均値：%.3f\n", n, ave/n);

  return(0);
}
