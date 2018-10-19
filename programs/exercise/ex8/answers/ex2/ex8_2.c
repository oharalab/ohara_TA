#include <stdio.h>

int main() {
  float sum = 0;
  int score[5], i;

  for (i = 0; i < 5; i ++) {
    printf("点を入力[%d人目]:", i+1);
    scanf("%d", &score[i]);
  }

  printf("\n");

  for (i = 0; i < 5; i ++) {
    printf("%d人目の点数: %d\n", i+1, score[i]);
    sum += score[i];
  }

  printf("平均点:      %.2f\n", sum / 5.0);

  return 0;
}
