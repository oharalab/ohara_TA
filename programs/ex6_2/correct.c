#include <stdio.h>

int main() {
  int i, j;

  /* 列名の出力 */
  printf("%3s|", " ");
  for (i = 1; i <= 9; i ++) {
    printf("%3d", i);
  }
  printf("\n");

  /* ----の出力 */
  printf("%s|", "---");
  for (i = 1; i <= 9; i ++) {
    printf("%s", "---");
  }
  printf("\n");

  /* 99表の出力 */
  for (i = 1; i <= 9; i ++) {
    printf("%3d|", i);
    for (j = 1; j <= 9; j ++) {
      printf("%3d", i * j);
    }
    printf("\n");
  }
  
  return 0;
}
