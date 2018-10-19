#include <stdio.h>

int main() {
  int i, num, score, pass = 0;

  printf("何人ですか？");
  scanf("%d", &num);

  for (i = 1; i <= num; i ++) {
    printf("%d番の点数は？", i);
    scanf("%d", &score);

    while (score < 0 || score > 100) {
      printf("マイナス点や100点を越える点数は入力できません\n");
      printf("再入力してください\n");
      printf("%d番の点数は？", i);
      scanf("%d", &score);
    }

    if (score >= 60) {
      pass += 1;
    }
  }

  printf("合格者数は%d名です\n", pass);

  return 0;
}
