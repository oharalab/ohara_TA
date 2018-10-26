#include <stdio.h>

int main() {
  int i, j, kuku[9][9];

  for (i = 0; i < 9; i ++) {
    for (j = 0; j < 9; j ++) {
      kuku[i][j] = (i+1) * (j+1);
    }
  }

  printf("  ");
  for (i = 0; i < 9; i ++) {
    printf(" %2d", i+1);
  }
  printf("\n");

  for (i = 0; i < 9; i ++) {
    printf("%d ", i+1);
    for (j = 0; j < 9; j ++) {
      printf(" %2d", kuku[i][j]);
    }
    printf("\n");
  }

  return 0;
}
