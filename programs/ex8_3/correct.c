#include <stdio.h>

int main() {
  int i, squar[20], cube[20];

  for (i = 0; i < 20; i ++) {
    squar[i] = i * i;
    cube[i] = i * i * i;
  }

  printf("数  2乗  3乗\n");
  for (i = 0; i < 20; i ++) {
    printf("%2d %3d %4d\n", i, squar[i], cube[i]);
  }

  return 0;
}
