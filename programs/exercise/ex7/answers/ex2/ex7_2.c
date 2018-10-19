#include <stdio.h>

int main() {
  int i = 1, num, score, pass = 0;

  printf("%d番の点数は？", i++);
  scanf("%d", &score);
  while (score > 0 && score < 100) {
    if (score >= 60) {
      pass += 1;
    }
    printf("%d番の点数は？", i++);
    scanf("%d", &score);

  } 
  printf("合格者数は%d名です\n", pass);

  return 0;
}
