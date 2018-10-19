#include <stdio.h>
#include <math.h>

int main() {
  double ans;
  int angle = 30;
  double pi = 3.14159;

  double rad = pi / 180 * angle;

  ans = pow(sin(rad), 2) + pow(cos(rad), 2);

  printf("答えは%.2fです\n", ans);

  return 0;
}
