#include <stdio.h>

int main() {
  int i, sum = 0, seki = 1;

  for (i = 1; i <= 5; i ++) {
    sum += i;
    seki *= i;
  }
  printf("和=%d\n", sum);
  printf("積=%d\n", seki);

  return 0;
}
