#include <stdio.h>
#include <math.h>

int main() {
  float x, y;

  printf("ｘのｙ乗を計算します\n");
  printf("ｘとｙの値を空白で区切って入力＞");

  scanf("%f %f", &x, &y);
  printf("%.3fの%.3f乗は%.3fです\n", x, y, pow(x, y));

  return 0;
}
